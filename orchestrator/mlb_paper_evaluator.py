"""MLB Paper Recommendation Quality Evaluator.

Processes paper recommendation log files and matches them to ground truth game outcomes.
Calculates key metrics (evaluated_count, matched_count, hit_rate, Brier score, ROI)
and outputs structured, JSON-serializable summaries to evaluate model/strategy performance.

Safety Invariants:
  - Strict paper-only / offline execution.
  - No database writes.
  - No live API calls.
  - No real betting stake logic.
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PaperEvaluationMetrics:
    evaluated_count: int = 0
    matched_outcome_count: int = 0
    missing_outcome_count: int = 0
    coverage_rate: float = 0.0
    hit_rate: float = 0.0
    brier_score: float | None = None
    actual_paper_pnl: float = 0.0
    actual_paper_stake: float = 0.0
    actual_paper_roi: float = 0.0
    shadow_unit_pnl: float = 0.0
    shadow_unit_stake: float = 0.0
    shadow_unit_roi: float = 0.0
    binomial_p_value: float | None = None
    gate_segmentation: dict[str, Any] = field(default_factory=dict)
    confidence_segmentation: dict[str, Any] = field(default_factory=dict)


def calculate_binomial_p_value(hits: int, trials: int, p_null: float = 0.5) -> float:
    """Calculate the one-sided binomial p-value (probability of getting >= hits under H0)."""
    if trials == 0:
        return 1.0
    if hits > trials:
        return 0.0
    pval = 0.0
    for i in range(hits, trials + 1):
        try:
            comb = math.comb(trials, i)
            pval += comb * (p_null ** i) * ((1.0 - p_null) ** (trials - i))
        except (ValueError, OverflowError):
            continue
    return min(1.0, max(0.0, pval))


def _extract_pk(game_id: str) -> str:
    """Robustly extract the unique game PK suffix from a game ID string."""
    if not game_id:
        return ""
    if "_" in game_id:
        return game_id.split("_")[-1]
    if "-" in game_id:
        return game_id.split("-")[-1]
    return game_id


def load_paper_recommendations(paper_dir: str | Path) -> list[dict]:
    """Recursively load paper recommendations from JSONL files in the directory."""
    recommendations: list[dict] = []
    path = Path(paper_dir)
    if not path.exists():
        return recommendations

    for file_path in path.glob("**/*.jsonl"):
        try:
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if isinstance(data, dict):
                            recommendations.append(data)
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue
    return recommendations


def load_outcome_records(outcome_path: str | Path) -> list[dict]:
    """Load outcome records from an outcome-attached JSONL file."""
    outcomes: list[dict] = []
    path = Path(outcome_path)
    if not path.exists():
        return outcomes

    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if isinstance(data, dict):
                        outcomes.append(data)
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return outcomes


def evaluate_paper_recommendations(
    recommendations: list[dict],
    outcomes: list[dict],
) -> PaperEvaluationMetrics:
    """Evaluate paper recommendations against ground-truth outcomes."""
    metrics = PaperEvaluationMetrics()
    metrics.evaluated_count = len(recommendations)
    if not recommendations:
        return metrics

    # Index outcomes by unique game PK suffix
    outcome_index: dict[str, dict] = {}
    for o in outcomes:
        game_id = o.get("game_id", "")
        pk = _extract_pk(game_id)
        if pk:
            outcome_index[pk] = o

    matched_recs: list[tuple[dict, dict]] = []
    for r in recommendations:
        r_id = r.get("game_id", "")
        pk = _extract_pk(r_id)
        if pk in outcome_index:
            outcome = outcome_index[pk]
            # Match is valid if outcome is available and winner is declared
            if outcome.get("outcome_available") and outcome.get("actual_winner") in {"home", "away"}:
                matched_recs.append((r, outcome))
                metrics.matched_outcome_count += 1
            else:
                metrics.missing_outcome_count += 1
        else:
            metrics.missing_outcome_count += 1

    metrics.coverage_rate = (
        round(metrics.matched_outcome_count / metrics.evaluated_count, 4)
        if metrics.evaluated_count > 0
        else 0.0
    )

    if not matched_recs:
        return metrics

    # Standard calculations
    correct_count = 0
    brier_sum = 0.0
    brier_count = 0

    # PnL tracking
    actual_pnl = 0.0
    actual_stake = 0.0
    shadow_pnl = 0.0

    # Segmentation containers
    gate_data: dict[str, list[tuple[dict, dict]]] = {}
    conf_data: dict[str, list[tuple[dict, dict]]] = {
        "low (0.50-0.55)": [],
        "mid (0.55-0.65)": [],
        "high (0.65-1.00)": [],
    }

    for r, o in matched_recs:
        side = r.get("tsl_side", "").lower()
        winner = o.get("actual_winner", "").lower()
        is_hit = (side == winner)

        if is_hit:
            correct_count += 1

        # Brier Score calculation: using model_prob_home
        prob_home = r.get("model_prob_home")
        if prob_home is not None:
            actual_home_win = 1.0 if winner == "home" else 0.0
            brier_sum += (float(prob_home) - actual_home_win) ** 2
            brier_count += 1

        # Simulated actual paper PnL
        stake = r.get("stake_units_paper", 0.0)
        odds = r.get("tsl_decimal_odds", 1.0)
        actual_stake += stake
        if is_hit:
            actual_pnl += stake * (odds - 1.0)
            shadow_pnl += (odds - 1.0)
        else:
            actual_pnl -= stake
            shadow_pnl -= 1.0

        # Segmentation - Gate Status
        gate_status = r.get("gate_status", "UNKNOWN")
        gate_data.setdefault(gate_status, []).append((r, o))

        # Segmentation - Confidence bands
        max_prob = max(float(r.get("model_prob_home", 0.5)), float(r.get("model_prob_away", 0.5)))
        if max_prob < 0.55:
            conf_key = "low (0.50-0.55)"
        elif max_prob < 0.65:
            conf_key = "mid (0.55-0.65)"
        else:
            conf_key = "high (0.65-1.00)"
        conf_data[conf_key].append((r, o))

    metrics.hit_rate = round(correct_count / len(matched_recs), 4)
    metrics.binomial_p_value = round(calculate_binomial_p_value(correct_count, len(matched_recs)), 6)

    if brier_count > 0:
        metrics.brier_score = round(brier_sum / brier_count, 6)

    metrics.actual_paper_pnl = round(actual_pnl, 4)
    metrics.actual_paper_stake = round(actual_stake, 4)
    metrics.actual_paper_roi = (
        round(actual_pnl / actual_stake, 4) if actual_stake > 0.0 else 0.0
    )

    metrics.shadow_unit_pnl = round(shadow_pnl, 4)
    metrics.shadow_unit_stake = float(len(matched_recs))
    metrics.shadow_unit_roi = round(shadow_pnl / len(matched_recs), 4)

    # Segment calculations
    for gate_status, items in gate_data.items():
        metrics.gate_segmentation[gate_status] = _evaluate_subset(items)

    for conf_band, items in conf_data.items():
        metrics.confidence_segmentation[conf_band] = _evaluate_subset(items)

    return metrics


def _evaluate_subset(items: list[tuple[dict, dict]]) -> dict[str, Any]:
    """Helper to evaluate a specific subset of matched recommendations."""
    if not items:
        return {
            "count": 0,
            "correct_count": 0,
            "hit_rate": 0.0,
            "brier_score": None,
            "actual_paper_roi": 0.0,
            "shadow_unit_roi": 0.0,
        }

    correct = 0
    brier_sum = 0.0
    brier_count = 0
    actual_pnl = 0.0
    actual_stake = 0.0
    shadow_pnl = 0.0

    for r, o in items:
        side = r.get("tsl_side", "").lower()
        winner = o.get("actual_winner", "").lower()
        is_hit = (side == winner)

        if is_hit:
            correct += 1

        prob_home = r.get("model_prob_home")
        if prob_home is not None:
            actual_home_win = 1.0 if winner == "home" else 0.0
            brier_sum += (float(prob_home) - actual_home_win) ** 2
            brier_count += 1

        stake = r.get("stake_units_paper", 0.0)
        odds = r.get("tsl_decimal_odds", 1.0)
        actual_stake += stake
        if is_hit:
            actual_pnl += stake * (odds - 1.0)
            shadow_pnl += (odds - 1.0)
        else:
            actual_pnl -= stake
            shadow_pnl -= 1.0

    return {
        "count": len(items),
        "correct_count": correct,
        "hit_rate": round(correct / len(items), 4),
        "brier_score": round(brier_sum / brier_count, 6) if brier_count > 0 else None,
        "actual_paper_roi": round(actual_pnl / actual_stake, 4) if actual_stake > 0.0 else 0.0,
        "shadow_unit_roi": round(shadow_pnl / len(items), 4),
    }


def execute_evaluation(
    paper_dir: str | Path,
    outcome_path: str | Path,
    summary_output_path: str | Path | None = None,
) -> dict[str, Any]:
    """Execute evaluation and optionally write structured JSON summary file."""
    recs = load_paper_recommendations(paper_dir)
    outcomes = load_outcome_records(outcome_path)
    metrics = evaluate_paper_recommendations(recs, outcomes)

    result = {
        "evaluator_version": "p142_evaluator_v1",
        "timestamp_utc": getattr(metrics, "generated_at_utc", None) or "",
        "metrics": asdict(metrics),
    }

    if summary_output_path:
        out_p = Path(summary_output_path)
        try:
            out_p.parent.mkdir(parents=True, exist_ok=True)
            with open(out_p, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
        except OSError:
            pass

    return result
