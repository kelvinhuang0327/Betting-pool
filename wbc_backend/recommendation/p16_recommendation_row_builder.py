"""
wbc_backend/recommendation/p16_recommendation_row_builder.py

P16 Recommendation Row Builder — CEO-revised scope.

Constructs the canonical recommendation row including risk profile fields.

Row contract:
  - recommendation_id / game_id / date / side
  - p_model / p_market / edge / odds_decimal
  - paper_stake_fraction / strategy_policy
  - gate_decision / gate_reason
  - source_model / source_bss_oof / odds_join_status
  - paper_only / production_ready
  - created_from = "P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED"
  - strategy_risk_profile_roi_ci_low_95
  - strategy_risk_profile_roi_ci_high_95
  - strategy_risk_profile_max_drawdown
  - strategy_risk_profile_sharpe
  - strategy_risk_profile_n_bets
  - selected_edge_threshold

Stake rules:
  - Gate fail → stake = 0
  - Gate pass → paper stake per capped_kelly capped at min(kelly, 0.02)
    and respects strategy_risk_profile

PAPER_ONLY: Paper simulation only. No production bets.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

from wbc_backend.recommendation.p16_recommendation_gate import (
    GateResult,
    compute_paper_stake,
)
from wbc_backend.recommendation.p16_recommendation_input_adapter import P16InputRow
from wbc_backend.simulation.strategy_risk_metrics import StrategyRiskProfile

CREATED_FROM = "P16_RECOMMENDATION_GATE_REEVALUATION_RISK_HARDENED"
STRATEGY_POLICY = "capped_kelly"


# ── Row contract ──────────────────────────────────────────────────────────────

@dataclass
class P16RecommendationRow:
    recommendation_id: str
    game_id: str
    date: str
    side: str
    p_model: float | None
    p_market: float | None
    edge: float | None
    odds_decimal: float | None
    paper_stake_fraction: float
    strategy_policy: str
    gate_decision: str
    gate_reason: str
    source_model: str
    source_bss_oof: float
    odds_join_status: str
    paper_only: bool
    production_ready: bool
    created_from: str
    strategy_risk_profile_roi_ci_low_95: float
    strategy_risk_profile_roi_ci_high_95: float
    strategy_risk_profile_max_drawdown: float
    strategy_risk_profile_sharpe: float
    strategy_risk_profile_n_bets: int
    selected_edge_threshold: float

    def to_dict(self) -> dict:
        return asdict(self)


# ── Deterministic ID ──────────────────────────────────────────────────────────

def _make_recommendation_id(
    game_id: str,
    date: str,
    gate_decision: str,
    selected_edge_threshold: float,
) -> str:
    """
    Deterministic recommendation ID based on key fields.
    Uses SHA-256 truncated to 12 hex chars.
    """
    key = f"{game_id}|{date}|{gate_decision}|{selected_edge_threshold:.6f}"
    return "P16-" + hashlib.sha256(key.encode()).hexdigest()[:12].upper()


def _determine_side(row: P16InputRow) -> str:
    """
    Determine the side the model recommends based on edge direction.
    Positive edge → home team favoured by model.
    Negative edge → away team favoured by model.
    """
    if row.edge is None:
        return "UNKNOWN"
    return "HOME" if row.edge >= 0.0 else "AWAY"


# ── Builder ───────────────────────────────────────────────────────────────────

def build_recommendation_row(
    row: P16InputRow,
    gate: GateResult,
    risk_profile: StrategyRiskProfile,
    selected_edge_threshold: float,
    max_stake_cap: float = 0.02,
) -> P16RecommendationRow:
    """
    Build a P16 recommendation row.

    Parameters
    ----------
    row : P16InputRow
        Adapted P15 input row.
    gate : GateResult
        Gate decision for this row.
    risk_profile : StrategyRiskProfile
        Strategy risk profile from sweep.
    selected_edge_threshold : float
        Threshold selected by sweep.
    max_stake_cap : float
        Maximum paper stake cap. Default 0.02.

    Returns
    -------
    P16RecommendationRow
    """
    stake = compute_paper_stake(row, gate, risk_profile, max_stake_cap=max_stake_cap)
    side = _determine_side(row)
    rec_id = _make_recommendation_id(
        row.game_id, row.date, gate.decision, selected_edge_threshold
    )

    return P16RecommendationRow(
        recommendation_id=rec_id,
        game_id=row.game_id,
        date=row.date,
        side=side,
        p_model=row.p_model,
        p_market=row.p_market,
        edge=row.edge,
        odds_decimal=row.odds_decimal,
        paper_stake_fraction=stake,
        strategy_policy=STRATEGY_POLICY,
        gate_decision=gate.decision,
        gate_reason=gate.reason_code,
        source_model=row.source_model,
        source_bss_oof=row.source_bss_oof,
        odds_join_status=row.odds_join_status,
        paper_only=row.paper_only,
        production_ready=row.production_ready,
        created_from=CREATED_FROM,
        strategy_risk_profile_roi_ci_low_95=risk_profile.roi_ci_low_95,
        strategy_risk_profile_roi_ci_high_95=risk_profile.roi_ci_high_95,
        strategy_risk_profile_max_drawdown=risk_profile.max_drawdown_pct,
        strategy_risk_profile_sharpe=risk_profile.sharpe_ratio,
        strategy_risk_profile_n_bets=risk_profile.n_bets,
        selected_edge_threshold=selected_edge_threshold,
    )


def build_all_rows(
    input_rows: list[P16InputRow],
    gate_results: list[GateResult],
    risk_profile: StrategyRiskProfile,
    selected_edge_threshold: float,
    max_stake_cap: float = 0.02,
) -> list[P16RecommendationRow]:
    """
    Build all recommendation rows from parallel input_rows + gate_results lists.
    """
    assert len(input_rows) == len(gate_results), (
        f"input_rows ({len(input_rows)}) and gate_results ({len(gate_results)}) "
        "must have the same length"
    )
    return [
        build_recommendation_row(r, g, risk_profile, selected_edge_threshold, max_stake_cap)
        for r, g in zip(input_rows, gate_results)
    ]
