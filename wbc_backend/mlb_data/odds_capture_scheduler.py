"""
MLB Odds Capture Scheduler

Schedules odds captures at critical time points for each MLB game:
  T_open     = when odds first appear (continuous polling)
  T_decision = commence_time - 2 hours
  T_pregame  = commence_time - 5 minutes
  T_close    = commence_time (final snapshot)

Integrates with existing AutoScheduler or runs standalone via cron.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from .live_odds_collector import (
    DECISION_LEAD_MINUTES,
    PREGAME_LEAD_MINUTES,
    TIMELINE_PATH,
    capture_live_odds,
    _load_timelines,
)

logger = logging.getLogger(__name__)

# Schedule file tracks which captures have been completed
SCHEDULE_PATH = Path("data/mlb_context/odds_capture_schedule.json")


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _load_schedule() -> dict[str, Any]:
    if not SCHEDULE_PATH.exists():
        return {"games": {}, "last_run": None}
    try:
        return json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"games": {}, "last_run": None}


def _save_schedule(schedule: dict[str, Any]) -> None:
    SCHEDULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    schedule["last_run"] = _now_utc().isoformat().replace("+00:00", "Z")
    SCHEDULE_PATH.write_text(
        json.dumps(schedule, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def get_todays_mlb_schedule() -> list[dict[str, Any]]:
    """
    Get today's MLB games from the existing timeline or TSL crawler.
    Returns list of dicts with game_id, commence_time, home_team, away_team.
    """
    # First check existing timeline for games
    timelines = _load_timelines(TIMELINE_PATH)
    now = _now_utc()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_end = today_start + timedelta(days=2)

    games: list[dict[str, Any]] = []
    for tl in timelines.values():
        from .normalization import parse_ts
        ct = parse_ts(tl.commence_time)
        if ct and today_start <= ct <= tomorrow_end:
            games.append({
                "game_id": tl.game_id,
                "commence_time": tl.commence_time,
            })

    return games


def determine_capture_windows(
    now: datetime | None = None,
) -> dict[str, bool]:
    """
    Determine which capture windows should be active right now.

    Returns dict of capture types that are currently actionable:
      - "continuous": always True for opening odds
      - "decision": True if any game is 2-3 hours away
      - "pregame": True if any game is 0-30 minutes away
      - "closing": True if any game is 0-5 minutes away
    """
    if now is None:
        now = _now_utc()

    timelines = _load_timelines(TIMELINE_PATH)
    windows = {
        "continuous": True,
        "decision": False,
        "pregame": False,
        "closing": False,
    }

    from .normalization import parse_ts

    for tl in timelines.values():
        ct = parse_ts(tl.commence_time)
        if ct is None:
            continue
        delta_minutes = (ct - now).total_seconds() / 60.0
        if delta_minutes < 0:
            continue
        if DECISION_LEAD_MINUTES <= delta_minutes <= DECISION_LEAD_MINUTES + 60:
            windows["decision"] = True
        if 0 <= delta_minutes <= 30:
            windows["pregame"] = True
        if 0 <= delta_minutes <= PREGAME_LEAD_MINUTES:
            windows["closing"] = True

    return windows


def should_capture_now() -> bool:
    """Quick check: is there any reason to run a capture right now?"""
    windows = determine_capture_windows()
    return any(windows.values())


def run_scheduled_capture(
    *,
    odds_api_key: str | None = None,
    timeline_path: Path = TIMELINE_PATH,
    force: bool = False,
) -> dict[str, Any]:
    """
    Run a scheduled odds capture if appropriate timing.

    This is the function that cron or the scheduler should call.
    It handles:
    1. Checking if capture is needed
    2. Running the capture
    3. Recording what was captured
    4. Returning summary

    Args:
        odds_api_key: Optional API key for The Odds API fallback
        timeline_path: Path to timeline JSONL
        force: If True, capture regardless of timing
    """
    schedule = _load_schedule()
    now = _now_utc()

    if not force and not should_capture_now():
        return {
            "status": "skipped",
            "reason": "no games in capture window",
            "timestamp": now.isoformat().replace("+00:00", "Z"),
        }

    # Determine which windows are active
    windows = determine_capture_windows(now)

    # Run capture
    if odds_api_key is None:
        odds_api_key = os.environ.get("ODDS_API_KEY")

    result = capture_live_odds(
        timeline_path=timeline_path,
        odds_api_key=odds_api_key,
    )

    # Record capture in schedule
    capture_record = {
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "windows": windows,
        "result": result,
    }

    if "captures" not in schedule:
        schedule["captures"] = []
    schedule["captures"].append(capture_record)

    # Keep only last 100 capture records
    if len(schedule["captures"]) > 100:
        schedule["captures"] = schedule["captures"][-100:]

    _save_schedule(schedule)

    return {
        "status": "captured",
        "timestamp": now.isoformat().replace("+00:00", "Z"),
        "windows": windows,
        "result": result,
    }


def get_capture_status() -> dict[str, Any]:
    """
    Get current status of odds capture pipeline.
    Shows which games have complete timelines and which are missing data.
    """
    timelines = _load_timelines(TIMELINE_PATH)
    schedule = _load_schedule()

    now = _now_utc()
    from .normalization import parse_ts

    stats = {
        "total_games": len(timelines),
        "games_with_opening": 0,
        "games_with_decision": 0,
        "games_with_pregame": 0,
        "games_with_closing": 0,
        "games_with_full_timeline": 0,
        "games_clv_ready": 0,
        "upcoming_games": 0,
        "last_capture": schedule.get("last_run"),
    }

    for tl in timelines.values():
        has_opening = tl.opening_ts is not None
        has_decision = tl.decision_ts is not None
        has_pregame = tl.latest_pregame_ts is not None
        has_closing = tl.closing_ts is not None

        stats["games_with_opening"] += int(has_opening)
        stats["games_with_decision"] += int(has_decision)
        stats["games_with_pregame"] += int(has_pregame)
        stats["games_with_closing"] += int(has_closing)
        stats["games_with_full_timeline"] += int(
            has_opening and has_decision and has_pregame and has_closing
        )
        stats["games_clv_ready"] += int(has_decision and has_closing)

        ct = parse_ts(tl.commence_time)
        if ct and ct > now:
            stats["upcoming_games"] += 1

    return stats
