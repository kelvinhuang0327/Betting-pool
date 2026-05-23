"""
heartbeat_schema.py
P28C: Enriched heartbeat row schema for the MLB odds capture daemon.

Replaces the ambiguous ``status: "captured"`` signal with explicit semantic
fields that distinguish:
  - daemon alive / heartbeat written
  - fetch attempted vs skipped
  - source returned empty vs fetch produced data
  - closing odds truly captured vs blocked by quota
  - quota reserved for future closing window

Design reference: P27A design item — Heartbeat-vs-Fetch schema disambiguation
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

# Bump this when the schema changes to allow consumers to detect old rows.
SEMANTIC_STATUS_VERSION: str = "v2"

# Status codes from daily_closing_capture that signal quota exhaustion.
_QUOTA_HARD_STATUSES: frozenset[str] = frozenset(
    {"skipped_daily_cap_reached", "quota_hard_cap"}
)

# Status codes from daily_closing_capture that signal quota reservation.
_QUOTA_RESERVED_STATUSES: frozenset[str] = frozenset(
    {"skipped_quota_reserved_for_closing"}
)


@dataclass
class SemanticHeartbeatRow:
    """
    Enriched heartbeat row written to logs/daemon_heartbeat.jsonl.

    Fields
    ------
    Preserved (backward-compatible):
        timestamp, status, fetched, api_calls_today, next_trigger_minutes

    New semantic fields (semantic_status_version="v2"):
        heartbeat_written               — always True; confirms daemon is alive
        odds_fetch_attempted            — True when a live-odds fetch was executed
        fetch_success                   — True when fetch returned ≥1 snapshot
        source_empty                    — True when fetch ran but returned 0 snapshots
        target_games_seen               — count of timelines updated by this cycle
        target_games_missing            — count of scheduled games absent from fetch
        closing_odds_captured           — True when daily closing capture completed
        external_fetch_blocked_by_quota — True when quota hard-cap prevented fetch
        quota_reserved_for_closing      — True when quota was held for future closing
        fetch_skip_reason               — human-readable reason when fetch was skipped
        semantic_status_version         — schema version tag ("v2")
    """

    # ---- Preserved fields ---------------------------------------------------
    timestamp: str
    status: str
    fetched: bool
    api_calls_today: int
    next_trigger_minutes: float | None

    # ---- New semantic fields -------------------------------------------------
    semantic_status_version: str = SEMANTIC_STATUS_VERSION
    heartbeat_written: bool = True
    odds_fetch_attempted: bool = False
    fetch_success: bool = False
    source_empty: bool = False
    target_games_seen: int = 0
    target_games_missing: int = 0
    closing_odds_captured: bool = False
    external_fetch_blocked_by_quota: bool = False
    quota_reserved_for_closing: bool = False
    fetch_skip_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_semantic_heartbeat_row(
    result: dict[str, Any],
    existing_state: dict[str, Any],
    timestamp: str,
    next_trigger_minutes: float | None = None,
) -> dict[str, Any]:
    """
    Build an enriched heartbeat row dict from a ``run_scheduled_capture()``
    result, the persisted external-closing state, and the current timestamp.

    Parameters
    ----------
    result:
        Return value of ``run_scheduled_capture()`` (or
        ``{"status": "exception"}`` on unhandled exceptions).
    existing_state:
        Contents of ``data/mlb_context/external_closing_state.json``.
    timestamp:
        ISO 8601 UTC timestamp for this heartbeat row.
    next_trigger_minutes:
        Minutes until next expected closing-capture trigger (caller-derived).

    Returns
    -------
    dict
        Ready-to-serialise heartbeat row.
    """
    result = result or {}
    existing_state = existing_state or {}

    outer_status: str = result.get("status", "unknown")

    # Inner result from capture_live_odds() — guard against non-dict values
    _inner_raw = result.get("result")
    inner: dict[str, Any] = _inner_raw if isinstance(_inner_raw, dict) else {}

    # External-closing daily result lives under inner["external_closing"].
    # (Historically the daemon looked at result["daily_closing"] which was
    # always empty — this is the P28C fix.)
    ec: dict[str, Any] = inner.get("external_closing") or {}
    ec_status: str = ec.get("status", "")

    # ---- Derive new fields ---------------------------------------------------

    odds_fetch_attempted: bool = outer_status == "captured"

    snapshots_received: int = (
        int(inner.get("snapshots_received", 0)) if isinstance(inner, dict) else 0
    )
    fetch_success: bool = odds_fetch_attempted and snapshots_received > 0
    source_empty: bool = odds_fetch_attempted and snapshots_received == 0

    target_games_seen: int = (
        int(inner.get("games_updated", 0)) if isinstance(inner, dict) else 0
    )

    closing_odds_captured: bool = bool(
        ec_status == "ok" and int(ec.get("games_updated", 0)) > 0
    )

    external_fetch_blocked_by_quota: bool = ec_status in _QUOTA_HARD_STATUSES
    quota_reserved_for_closing: bool = ec_status in _QUOTA_RESERVED_STATUSES

    fetch_skip_reason: str | None = None
    if outer_status == "skipped":
        fetch_skip_reason = result.get("reason") or "no_capture_window"
    elif outer_status == "exception":
        fetch_skip_reason = "exception"
    elif source_empty:
        fetch_skip_reason = "source_returned_empty"
    elif external_fetch_blocked_by_quota:
        fetch_skip_reason = ec_status
    elif quota_reserved_for_closing:
        fetch_skip_reason = ec_status

    # ---- Preserved fields ---------------------------------------------------

    fetched: bool = bool(existing_state.get("fetched", False))
    api_calls_today: int = int(existing_state.get("api_calls_today", 0))
    # Use fine-grained ec_status when available; fall back to outer_status
    status_for_row: str = ec_status if ec_status else outer_status

    row = SemanticHeartbeatRow(
        timestamp=timestamp,
        status=status_for_row,
        fetched=fetched,
        api_calls_today=api_calls_today,
        next_trigger_minutes=next_trigger_minutes,
        heartbeat_written=True,
        odds_fetch_attempted=odds_fetch_attempted,
        fetch_success=fetch_success,
        source_empty=source_empty,
        target_games_seen=target_games_seen,
        target_games_missing=0,  # not derivable without an external schedule
        closing_odds_captured=closing_odds_captured,
        external_fetch_blocked_by_quota=external_fetch_blocked_by_quota,
        quota_reserved_for_closing=quota_reserved_for_closing,
        fetch_skip_reason=fetch_skip_reason,
        semantic_status_version=SEMANTIC_STATUS_VERSION,
    )
    return row.to_dict()
