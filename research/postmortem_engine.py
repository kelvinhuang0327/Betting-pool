from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .utils import save_json, utc_now_iso


def _decision_quality_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter()
    seen_games = set()
    for row in rows:
        if row.get("event_type") != "settlement":
            continue
        game_id = str(row.get("game_id", ""))
        if not game_id or game_id in seen_games:
            continue
        seen_games.add(game_id)
        decision = str(row.get("decision", "PASS"))
        result = str(row.get("result", "unknown"))
        edge = float(row.get("edge") or 0.0)
        if decision == "PASS":
            counts["NO_BET"] += 1
            continue
        good_signal = edge > 0
        win = result == "win"
        if good_signal and win:
            counts["GOOD_BET_WIN"] += 1
        elif good_signal and not win:
            counts["GOOD_BET_LOSS"] += 1
        elif not good_signal and win:
            counts["BAD_BET_WIN"] += 1
        else:
            counts["BAD_BET_LOSS"] += 1
    for key in ("GOOD_BET_WIN", "GOOD_BET_LOSS", "BAD_BET_WIN", "BAD_BET_LOSS", "NO_BET"):
        counts.setdefault(key, 0)
    return dict(counts)


def _regime_roi(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    buckets = defaultdict(lambda: {"pnl": 0.0, "stake": 0.0, "samples": 0.0})
    seen_games = set()
    for row in rows:
        if row.get("event_type") != "settlement":
            continue
        game_id = str(row.get("game_id", ""))
        if not game_id or game_id in seen_games:
            continue
        seen_games.add(game_id)
        regime = str(row.get("regime", "unknown"))
        pnl = float(row.get("pnl") or 0.0)
        stake = float(row.get("stake") or 0.0)
        buckets[regime]["pnl"] += pnl
        buckets[regime]["stake"] += stake
        buckets[regime]["samples"] += 1
    out: dict[str, dict[str, float]] = {}
    for regime, payload in buckets.items():
        stake = payload["stake"]
        out[regime] = {
            "roi": round(payload["pnl"] / stake if stake else 0.0, 4),
            "samples": int(payload["samples"]),
            "pnl": round(payload["pnl"], 4),
            "stake": round(stake, 4),
        }
    return dict(sorted(out.items()))


class PostmortemEngine:
    def __init__(self, base_dir: Optional[str] = None):
        self.paths = ensure_research_dirs(base_dir)

    @property
    def reports_dir(self) -> Path:
        return self.paths["postmortem_dir"]

    def generate(self, roi_summary: dict[str, Any], rows: list[dict[str, Any]], trigger: dict[str, Any]) -> Path:
        ts = trigger.get("timestamp", utc_now_iso()).replace(":", "-")
        report_path = self.reports_dir / f"{ts}.md"
        decision_counts = _decision_quality_counts(rows)
        regime_roi = _regime_roi(rows)
        sample_size = int(roi_summary.get("sample_size", 0))
        bankroll_change = float(roi_summary.get("bankroll_change", 0.0))
        drawdown = float(roi_summary.get("max_drawdown_pct", 0.0))
        total_roi = 0.0
        current_bankroll = float(roi_summary.get("current_bankroll", roi_summary.get("initial_bankroll", 100.0)))
        initial_bankroll = float(roi_summary.get("initial_bankroll", 100.0))
        if initial_bankroll:
            total_roi = (current_bankroll - initial_bankroll) / initial_bankroll

        top_regimes = sorted(regime_roi.items(), key=lambda item: item[1]["roi"], reverse=True)
        worst_regimes = sorted(regime_roi.items(), key=lambda item: item[1]["roi"])

        lines = [
            "# Research Postmortem Report",
            "",
            f"- Generated at: {utc_now_iso()}",
            f"- Trigger bucket: {trigger.get('bucket', 'unknown')}",
            f"- Trigger period: {trigger.get('period', 'unknown')}",
            f"- Trigger ROI: {float(trigger.get('roi', 0.0)):.4f}",
            "",
            "## 1. Performance Summary",
            f"- ROI: {total_roi:.4f}",
            f"- Sample size: {sample_size}",
            f"- Bankroll change: {bankroll_change:.4f}",
            f"- Drawdown: {drawdown:.4f}",
            "",
            "## 2. Regime Breakdown",
        ]
        if regime_roi:
            for regime, payload in regime_roi.items():
                lines.append(f"- {regime}: roi={payload['roi']:.4f}, samples={payload['samples']}")
        else:
            lines.append("- No settled trades yet")
        lines.extend([
            "",
            "## 3. Decision Quality",
        ])
        for key in ("GOOD_BET_WIN", "GOOD_BET_LOSS", "BAD_BET_WIN", "BAD_BET_LOSS", "NO_BET"):
            lines.append(f"- {key}: {decision_counts.get(key, 0)}")
        lines.extend([
            "",
            "## 4. Root Cause Analysis",
            "- Model vs market: compare settled edge sign against realized outcome; persistent negative ROI on positive-edge bets indicates market mismatch or stale priors.",
            "- Edge vs outcome: if good bets lose repeatedly, inspect calibration rather than strategy intent.",
            "- Regime failure: look for regimes with repeated negative ROI or sharp sample swings.",
            "- Calibration drift: compare recent ROI vs older settled ROI to detect deterioration.",
            "- Randomness vs structural issue: small samples with mixed signs lean random; repeated same-pattern losses are structural.",
            "",
            "## 5. Key Failing Patterns",
        ])
        if worst_regimes:
            worst_name, worst_payload = worst_regimes[0]
            lines.append(f"- Worst regime: {worst_name} (roi={worst_payload['roi']:.4f}, samples={worst_payload['samples']})")
        else:
            lines.append("- No regime data yet")
        if top_regimes:
            best_name, best_payload = top_regimes[0]
            lines.append(f"- Best regime: {best_name} (roi={best_payload['roi']:.4f}, samples={best_payload['samples']})")
        lines.extend([
            "",
            "## 6. Actionable Recommendations",
            "- reduce exposure? reduce if drawdown rises or positive-edge bets keep losing.",
            "- disable regime? disable regimes with persistent negative ROI and enough sample size.",
            "- recalibrate? recalibrate when GOOD_BET_LOSS dominates.",
            "- collect more data? yes, if sample size is still too small to separate signal from noise.",
            "- keep unchanged? yes, if positive ROI is stable and drawdown is bounded.",
        ])
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return report_path
