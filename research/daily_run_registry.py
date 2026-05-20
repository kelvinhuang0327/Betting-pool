from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .skip_day_policy import ACTIVE_DAY, PARTIAL_DAY, SKIPPED_DAY, classify_day
from .utils import append_jsonl, load_jsonl, utc_now_iso


def _parse_ts(value: str) -> datetime:
    raw = str(value).strip().replace("Z", "+00:00")
    return datetime.fromisoformat(raw).astimezone(timezone.utc)


def _coerce_date(value: str) -> str:
    return _parse_ts(value).date().isoformat()


@dataclass
class DailyRunRecord:
    date: str
    system_online: bool
    daily_pipeline_ran: bool
    prediction_count: int
    game_count_detected: int
    research_mode: bool
    status: str
    reason: Optional[str] = None
    source: str = "unknown"
    timestamp: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DailyRunRegistry:
    def __init__(self, base_dir: Optional[str] = None):
        self.paths = ensure_research_dirs(base_dir)

    @property
    def registry_path(self) -> Path:
        return self.paths["daily_run_registry"]

    def load(self) -> list[dict[str, Any]]:
        return load_jsonl(self.registry_path)

    def latest_by_date(self) -> dict[str, dict[str, Any]]:
        latest: dict[str, dict[str, Any]] = {}
        for row in self.load():
            date = str(row.get("date", "")).strip()
            if not date:
                continue
            latest[date] = row
        return latest

    def record_day(
        self,
        *,
        date: str,
        system_online: bool,
        daily_pipeline_ran: bool,
        prediction_count: int,
        game_count_detected: int,
        research_mode: bool,
        reason: Optional[str] = None,
        source: str = "unknown",
        mode: str = "snapshot",
    ) -> dict[str, Any]:
        normalized_date = str(date).strip()
        if not normalized_date:
            raise ValueError("date is required")
        previous = self.latest_by_date().get(normalized_date)
        if mode == "increment" and previous:
            prediction_count = int(previous.get("prediction_count", 0)) + int(prediction_count or 0)
            game_count_detected = int(previous.get("game_count_detected", 0)) + int(game_count_detected or 0)
            system_online = bool(previous.get("system_online")) or bool(system_online)
            daily_pipeline_ran = bool(previous.get("daily_pipeline_ran")) or bool(daily_pipeline_ran)
            research_mode = bool(previous.get("research_mode")) or bool(research_mode)
            reason = reason or previous.get("reason")
        status_info = classify_day(
            system_online=system_online,
            daily_pipeline_ran=daily_pipeline_ran,
            prediction_count=prediction_count,
            game_count_detected=game_count_detected,
            research_mode=research_mode,
            reason=reason,
        )
        candidate = {
            "date": normalized_date,
            "system_online": bool(status_info["system_online"]),
            "daily_pipeline_ran": bool(status_info["daily_pipeline_ran"]),
            "prediction_count": int(status_info["prediction_count"]),
            "game_count_detected": int(status_info["game_count_detected"]),
            "research_mode": bool(status_info["research_mode"]),
            "status": str(status_info["status"]),
            "reason": status_info.get("reason"),
            "source": source,
        }
        if mode == "snapshot" and previous:
            comparable_keys = (
                "system_online",
                "daily_pipeline_ran",
                "prediction_count",
                "game_count_detected",
                "research_mode",
                "status",
                "reason",
                "source",
            )
            if all(previous.get(key) == candidate.get(key) for key in comparable_keys):
                return previous
        record = DailyRunRecord(
            date=normalized_date,
            system_online=candidate["system_online"],
            daily_pipeline_ran=candidate["daily_pipeline_ran"],
            prediction_count=candidate["prediction_count"],
            game_count_detected=candidate["game_count_detected"],
            research_mode=candidate["research_mode"],
            status=candidate["status"],
            reason=candidate["reason"],
            source=candidate["source"],
        )
        append_jsonl(self.registry_path, record.to_dict())
        return record.to_dict()

    def summary(self) -> dict[str, Any]:
        latest = self.latest_by_date()
        counts = Counter()
        skipped_dates: list[str] = []
        partial_dates: list[str] = []
        active_dates: list[str] = []
        total_prediction_count = 0
        total_game_count = 0
        for date, row in sorted(latest.items()):
            status = str(row.get("status", "UNKNOWN"))
            counts[status] += 1
            total_prediction_count += int(row.get("prediction_count", 0) or 0)
            total_game_count += int(row.get("game_count_detected", 0) or 0)
            if status == SKIPPED_DAY:
                skipped_dates.append(date)
            elif status == PARTIAL_DAY:
                partial_dates.append(date)
            elif status == ACTIVE_DAY:
                active_dates.append(date)
        return {
            "updated_at": utc_now_iso(),
            "total_days": len(latest),
            "status_counts": {
                ACTIVE_DAY: counts.get(ACTIVE_DAY, 0),
                SKIPPED_DAY: counts.get(SKIPPED_DAY, 0),
                PARTIAL_DAY: counts.get(PARTIAL_DAY, 0),
            },
            "active_dates": active_dates,
            "skipped_dates": skipped_dates,
            "partial_dates": partial_dates,
            "prediction_count_total": total_prediction_count,
            "game_count_detected_total": total_game_count,
            "sample_size_included_days": counts.get(ACTIVE_DAY, 0) + counts.get(PARTIAL_DAY, 0),
            "sample_size_excluded_days": counts.get(SKIPPED_DAY, 0),
            "skipped_days_affected_sample_size": counts.get(SKIPPED_DAY, 0) > 0,
        }


def parse_date(value: str) -> str:
    return _coerce_date(value)
