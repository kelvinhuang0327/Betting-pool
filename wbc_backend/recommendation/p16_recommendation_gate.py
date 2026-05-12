"""
wbc_backend/recommendation/p16_recommendation_gate.py

P16 Recommendation Gate — CEO-revised scope.

Applies per-row gate logic that integrates:
  - Paper-only invariants
  - BSS positivity check
  - Odds join status filter
  - Probability / odds validity
  - Edge threshold from sweep (NOT hardcoded)
  - Drawdown ceiling (max_drawdown_pct > 25 → block)
  - Sharpe floor (sharpe < 0.0 → block)
  - Sweep insufficient-samples guard

PAPER_ONLY: Paper simulation only. No production bets.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from wbc_backend.recommendation.p16_recommendation_input_adapter import P16InputRow
from wbc_backend.simulation.strategy_risk_metrics import StrategyRiskProfile

# ── Reason codes ──────────────────────────────────────────────────────────────

ELIGIBLE = "P16_ELIGIBLE_PAPER_RECOMMENDATION"
BLOCKED_NOT_PAPER_ONLY = "P16_BLOCKED_NOT_PAPER_ONLY"
BLOCKED_PRODUCTION = "P16_BLOCKED_PRODUCTION_NOT_ALLOWED"
BLOCKED_NEGATIVE_BSS = "P16_BLOCKED_NEGATIVE_OR_ZERO_BSS"
BLOCKED_ODDS_NOT_JOINED = "P16_BLOCKED_ODDS_NOT_JOINED"
BLOCKED_INVALID_PROB = "P16_BLOCKED_INVALID_PROBABILITY"
BLOCKED_INVALID_ODDS = "P16_BLOCKED_INVALID_ODDS"
BLOCKED_EDGE_BELOW = "P16_BLOCKED_EDGE_BELOW_THRESHOLD"
BLOCKED_INVALID_STAKE = "P16_BLOCKED_INVALID_STAKE"
BLOCKED_SWEEP_INSUFFICIENT = "P16_BLOCKED_SWEEP_INSUFFICIENT_SAMPLES"
BLOCKED_DRAWDOWN = "P16_BLOCKED_DRAWDOWN_EXCEEDS_LIMIT"
BLOCKED_SHARPE = "P16_BLOCKED_SHARPE_BELOW_FLOOR"
BLOCKED_UNKNOWN = "P16_BLOCKED_UNKNOWN"

# ── Gate result ───────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class GateResult:
    decision: str  # ELIGIBLE | BLOCKED_*
    reason_code: str
    passed: bool


# ── Gate logic ────────────────────────────────────────────────────────────────

def _is_valid_probability(p: float | None) -> bool:
    return p is not None and math.isfinite(p) and 0.0 < p < 1.0


def _is_valid_odds(o: float | None) -> bool:
    return o is not None and math.isfinite(o) and o > 1.0


def apply_gate(
    row: P16InputRow,
    selected_edge_threshold: float,
    risk_profile: StrategyRiskProfile,
    sweep_status: str,
    max_drawdown_limit: float = 0.25,
    sharpe_floor: float = 0.0,
) -> GateResult:
    """
    Apply P16 gate to a single input row.

    Parameters
    ----------
    row : P16InputRow
        Adapted input row from P15.
    selected_edge_threshold : float
        Threshold selected by edge sweep (NOT hardcoded).
    risk_profile : StrategyRiskProfile
        Strategy risk profile from sweep.
    sweep_status : str
        "SWEEP_OK" or "SWEEP_INSUFFICIENT_SAMPLES".
    max_drawdown_limit : float
        Maximum allowed drawdown fraction (0.0-1.0). Default 0.25 (25%).
    sharpe_floor : float
        Minimum required Sharpe ratio. Default 0.0.

    Returns
    -------
    GateResult
    """
    # Guard: sweep insufficient samples — block all rows
    if sweep_status == "SWEEP_INSUFFICIENT_SAMPLES":
        return GateResult(
            decision=BLOCKED_SWEEP_INSUFFICIENT,
            reason_code=BLOCKED_SWEEP_INSUFFICIENT,
            passed=False,
        )

    # production_ready must be False
    if row.production_ready:
        return GateResult(
            decision=BLOCKED_PRODUCTION,
            reason_code=BLOCKED_PRODUCTION,
            passed=False,
        )

    # paper_only must be True
    if not row.paper_only:
        return GateResult(
            decision=BLOCKED_NOT_PAPER_ONLY,
            reason_code=BLOCKED_NOT_PAPER_ONLY,
            passed=False,
        )

    # BSS > 0
    if row.source_bss_oof <= 0.0:
        return GateResult(
            decision=BLOCKED_NEGATIVE_BSS,
            reason_code=BLOCKED_NEGATIVE_BSS,
            passed=False,
        )

    # odds_join_status == JOINED
    if row.odds_join_status != "JOINED":
        return GateResult(
            decision=BLOCKED_ODDS_NOT_JOINED,
            reason_code=BLOCKED_ODDS_NOT_JOINED,
            passed=False,
        )

    # Probability validity
    if not _is_valid_probability(row.p_model) or not _is_valid_probability(row.p_market):
        return GateResult(
            decision=BLOCKED_INVALID_PROB,
            reason_code=BLOCKED_INVALID_PROB,
            passed=False,
        )

    # Odds validity
    if not _is_valid_odds(row.odds_decimal):
        return GateResult(
            decision=BLOCKED_INVALID_ODDS,
            reason_code=BLOCKED_INVALID_ODDS,
            passed=False,
        )

    # Edge threshold (from sweep)
    edge = row.edge if row.edge is not None else (row.p_model - row.p_market)  # type: ignore[operator]
    if edge < selected_edge_threshold:
        return GateResult(
            decision=BLOCKED_EDGE_BELOW,
            reason_code=BLOCKED_EDGE_BELOW,
            passed=False,
        )

    # Drawdown ceiling
    if risk_profile.max_drawdown_pct > (max_drawdown_limit * 100.0):
        return GateResult(
            decision=BLOCKED_DRAWDOWN,
            reason_code=BLOCKED_DRAWDOWN,
            passed=False,
        )

    # Sharpe floor
    if risk_profile.sharpe_ratio < sharpe_floor:
        return GateResult(
            decision=BLOCKED_SHARPE,
            reason_code=BLOCKED_SHARPE,
            passed=False,
        )

    return GateResult(
        decision=ELIGIBLE,
        reason_code=ELIGIBLE,
        passed=True,
    )


def compute_paper_stake(
    row: P16InputRow,
    gate: GateResult,
    risk_profile: StrategyRiskProfile,
    max_stake_cap: float = 0.02,
) -> float:
    """
    Compute paper stake fraction.

    Gate fail → 0.0
    Gate pass → min(kelly_fraction, max_stake_cap)
    """
    if not gate.passed:
        return 0.0

    # Kelly fraction: (edge * (decimal_odds - 1) - (1 - edge)) / (decimal_odds - 1)
    # Simplified: f = edge / (decimal_odds - 1) where edge = p_model - p_market
    # Using full Kelly: f = (p * (odds-1) - (1-p)) / (odds-1) = p - (1-p)/(odds-1)
    edge = row.edge if row.edge is not None else (row.p_model - row.p_market)  # type: ignore[operator]
    odds = row.odds_decimal
    assert odds is not None  # validated in gate

    b = odds - 1.0  # net odds
    p = row.p_model
    assert p is not None  # validated in gate

    kelly = (p * b - (1.0 - p)) / b if b > 0.0 else 0.0
    kelly = max(0.0, kelly)

    return float(min(kelly, max_stake_cap))
