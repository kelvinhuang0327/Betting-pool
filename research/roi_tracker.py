from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .utils import load_json, load_jsonl, save_json, utc_now_iso


def _parse_ts(value: str) -> datetime:
    value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def _period_keys(dt: datetime) -> dict[str, str]:
    iso = dt.isocalendar()
    return {
        "daily": dt.strftime("%Y-%m-%d"),
        "weekly": f"{iso.year}-W{iso.week:02d}",
        "monthly": dt.strftime("%Y-%m"),
    }


class ROITracker:
    def __init__(self, base_dir: Optional[str] = None, initial_bankroll: float = 100.0):
        self.paths = ensure_research_dirs(base_dir)
        self.initial_bankroll = float(initial_bankroll)

    @property
    def roi_path(self) -> Path:
        return self.paths["roi"]

    def _settled_rows(self) -> list[dict[str, Any]]:
        rows = load_jsonl(self.paths["ledger"])
        settled: dict[str, dict[str, Any]] = {}
        for row in rows:
            if row.get("event_type") != "settlement":
                continue
            if row.get("result") not in {"win", "loss"}:
                continue
            game_id = str(row.get("game_id", ""))
            if not game_id:
                continue
            settled[game_id] = row
        return sorted(settled.values(), key=lambda row: row.get("timestamp", ""))

    def rebuild(self) -> dict[str, Any]:
        settled = self._settled_rows()
        bankroll = self.initial_bankroll
        peak = bankroll
        max_drawdown = 0.0
        curve: list[dict[str, Any]] = []
        daily: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
        weekly: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
        monthly: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
        regime: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})

        for row in settled:
            ts = _parse_ts(str(row["timestamp"]))
            keys = _period_keys(ts)
            pnl = float(row.get("pnl") or 0.0)
            stake = float(row.get("stake") or 0.0)
            regime_key = str(row.get("regime", "unknown"))

            bankroll += pnl
            peak = max(peak, bankroll)
            drawdown = 0.0 if peak <= 0 else (peak - bankroll) / peak
            max_drawdown = max(max_drawdown, drawdown)
            curve.append({
                "timestamp": ts.isoformat().replace("+00:00", "Z"),
                "bankroll": round(bankroll, 4),
                "pnl": round(pnl, 4),
                "event_id": row.get("event_id"),
            })

            for bucket, key, summary in (
                ("daily", keys["daily"], daily),
                ("weekly", keys["weekly"], weekly),
                ("monthly", keys["monthly"], monthly),
            ):
                summary[key]["pnl"] += pnl
                summary[key]["stake"] += stake
                summary[key]["samples"] += 1
            regime[regime_key]["pnl"] += pnl
            regime[regime_key]["stake"] += stake
            regime[regime_key]["samples"] += 1

        def finalize(bucket: dict[str, dict[str, float]]) -> dict[str, Any]:
            out: dict[str, Any] = {}
            for key, payload in bucket.items():
                stake = payload["stake"]
                pnl = payload["pnl"]
                roi = pnl / stake if stake else 0.0
                out[key] = {
                    "roi": round(roi, 4),
                    "pnl": round(pnl, 4),
                    "stake": round(stake, 4),
                    "samples": int(payload["samples"]),
                }
            return dict(sorted(out.items()))

        summary = {
            "updated_at": utc_now_iso(),
            "initial_bankroll": round(self.initial_bankroll, 4),
            "current_bankroll": round(bankroll, 4),
            "bankroll_change": round(bankroll - self.initial_bankroll, 4),
            "bankroll_curve": curve,
            "max_drawdown_pct": round(max_drawdown, 4),
            "sample_size": len(settled),
            "daily": finalize(daily),
            "weekly": finalize(weekly),
            "monthly": finalize(monthly),
            "regime_breakdown": finalize(regime),
        }
        save_json(self.roi_path, summary)
        return summary

    def current(self) -> dict[str, Any]:
        payload = load_json(self.roi_path, {})
        if payload:
            return payload
        return self.rebuild()
