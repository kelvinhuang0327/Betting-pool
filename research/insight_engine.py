from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .utils import save_json, utc_now_iso


class InsightEngine:
    def __init__(self, base_dir: Optional[str] = None):
        self.paths = ensure_research_dirs(base_dir)

    @property
    def latest_path(self) -> Path:
        return self.paths["latest_insights"]

    def generate(self, roi_summary: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
        regime_rollup: dict[str, dict[str, float]] = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
        edge_bins = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
        seen_games = set()
        for row in rows:
            if row.get("event_type") != "settlement":
                continue
            game_id = str(row.get("game_id", ""))
            if not game_id or game_id in seen_games:
                continue
            seen_games.add(game_id)
            regime = str(row.get("regime", "unknown"))
            edge = float(row.get("edge") or 0.0)
            pnl = float(row.get("pnl") or 0.0)
            stake = float(row.get("stake") or 0.0)
            regime_rollup[regime]["pnl"] += pnl
            regime_rollup[regime]["stake"] += stake
            regime_rollup[regime]["samples"] += 1
            edge_bucket = "positive_edge" if edge > 0 else "non_positive_edge"
            edge_bins[edge_bucket]["pnl"] += pnl
            edge_bins[edge_bucket]["stake"] += stake
            edge_bins[edge_bucket]["samples"] += 1

        def roi(payload: dict[str, float]) -> float:
            return payload["pnl"] / payload["stake"] if payload["stake"] else 0.0

        best_regime = None
        worst_regime = None
        if regime_rollup:
            best_regime = max(regime_rollup.items(), key=lambda item: roi(item[1]))
            worst_regime = min(regime_rollup.items(), key=lambda item: roi(item[1]))

        insight = {
            "updated_at": utc_now_iso(),
            "best_performing_regimes": (
                [{"regime": best_regime[0], "roi": round(roi(best_regime[1]), 4), "samples": int(best_regime[1]["samples"])}]
                if best_regime else []
            ),
            "worst_performing_regimes": (
                [{"regime": worst_regime[0], "roi": round(roi(worst_regime[1]), 4), "samples": int(worst_regime[1]["samples"])}]
                if worst_regime else []
            ),
            "edge_stability": {
                "positive_edge_roi": round(roi(edge_bins["positive_edge"]), 4) if edge_bins["positive_edge"]["stake"] else 0.0,
                "non_positive_edge_roi": round(roi(edge_bins["non_positive_edge"]), 4) if edge_bins["non_positive_edge"]["stake"] else 0.0,
            },
            "signal_decay": {
                "recent_sample_size": int(roi_summary.get("sample_size", 0)),
                "note": "compare recent vs historical buckets once enough settled trades accumulate",
            },
            "suspicious_patterns": [
                "positive_edge_bets_losing" if edge_bins["positive_edge"]["samples"] and roi(edge_bins["positive_edge"]) < 0 else None,
                "non_positive_edge_bets_winning" if edge_bins["non_positive_edge"]["samples"] and roi(edge_bins["non_positive_edge"]) > 0 else None,
            ],
        }
        insight["suspicious_patterns"] = [x for x in insight["suspicious_patterns"] if x]
        save_json(self.latest_path, insight)
        return insight
