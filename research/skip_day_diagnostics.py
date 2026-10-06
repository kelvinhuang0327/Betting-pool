from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .skip_day_policy import ACTIVE_DAY, PARTIAL_DAY, SKIPPED_DAY
from .utils import load_json, save_json, utc_now_iso


class SkipDayDiagnostics:
    def __init__(self, base_dir: Optional[str] = None):
        self.paths = ensure_research_dirs(base_dir)

    @property
    def path(self) -> Path:
        return self.paths["missed_prediction_days"]

    def load(self) -> dict[str, Any]:
        payload = load_json(self.path, {})
        if isinstance(payload, dict) and "entries" in payload:
            return payload
        if isinstance(payload, list):
            return {"updated_at": utc_now_iso(), "entries": payload}
        return {"updated_at": utc_now_iso(), "entries": []}

    def record_day(
        self,
        *,
        date: str,
        status: str,
        reason: str,
        games_found: int,
        prediction_events: int,
        results_ingested: bool,
        notes: Optional[str] = None,
    ) -> dict[str, Any]:
        if status == ACTIVE_DAY:
            return {}
        payload = self.load()
        entries = {str(row.get("date", "")): row for row in payload.get("entries", []) if isinstance(row, dict)}
        entry = {
            "date": str(date),
            "status": str(status),
            "reason": str(reason),
            "games_found": int(games_found or 0),
            "prediction_events": int(prediction_events or 0),
            "results_ingested": bool(results_ingested),
            "notes": notes or "",
            "timestamp": utc_now_iso(),
        }
        previous = entries.get(entry["date"])
        if previous:
            comparable_keys = (
                "date",
                "status",
                "reason",
                "games_found",
                "prediction_events",
                "results_ingested",
                "notes",
            )
            if all(previous.get(key) == entry.get(key) for key in comparable_keys):
                return previous
        entries[entry["date"]] = entry
        summary_counts = Counter(row.get("status") for row in entries.values())
        skipped_dates = sorted(date for date, row in entries.items() if row.get("status") == SKIPPED_DAY)
        partial_dates = sorted(date for date, row in entries.items() if row.get("status") == PARTIAL_DAY)
        payload = {
            "updated_at": utc_now_iso(),
            "entries": [entries[key] for key in sorted(entries)],
            "summary": {
                "status_counts": {
                    ACTIVE_DAY: summary_counts.get(ACTIVE_DAY, 0),
                    SKIPPED_DAY: summary_counts.get(SKIPPED_DAY, 0),
                    PARTIAL_DAY: summary_counts.get(PARTIAL_DAY, 0),
                },
                "skipped_dates": skipped_dates,
                "partial_dates": partial_dates,
                "missed_count": summary_counts.get(SKIPPED_DAY, 0) + summary_counts.get(PARTIAL_DAY, 0),
            },
        }
        save_json(self.path, payload)
        return entry

    def summary(self) -> dict[str, Any]:
        payload = self.load()
        entries = [row for row in payload.get("entries", []) if isinstance(row, dict)]
        counts = Counter(row.get("status") for row in entries)
        return {
            "updated_at": payload.get("updated_at", utc_now_iso()),
            "total_entries": len(entries),
            "status_counts": {
                ACTIVE_DAY: counts.get(ACTIVE_DAY, 0),
                SKIPPED_DAY: counts.get(SKIPPED_DAY, 0),
                PARTIAL_DAY: counts.get(PARTIAL_DAY, 0),
            },
            "skipped_dates": sorted(row.get("date", "") for row in entries if row.get("status") == SKIPPED_DAY),
            "partial_dates": sorted(row.get("date", "") for row in entries if row.get("status") == PARTIAL_DAY),
        }
