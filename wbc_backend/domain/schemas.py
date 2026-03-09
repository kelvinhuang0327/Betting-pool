"""
Domain schemas — expanded to cover all data flowing through the prediction pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ── Team / Player Snapshots ──────────────────────────────────────────────────

@dataclass
class PitcherSnapshot:
    name: str
    team: str
    era: float
    fip: float
    whip: float
    k_per_9: float
    bb_per_9: float
    stuff_plus: float
    ip_last_30: float
    era_last_3: float
    pitch_count_last_3d: int
    fastball_velo: float
    high_leverage_era: float
    role: str = "SP"   # SP | RP | PB
    pitch_mix: Dict[str, float] = field(default_factory=dict)
    recent_fastball_velos: List[float] = field(default_factory=list)
    career_fastball_velo: float = 0.0
    woba_vs_left: float = 0.320
    woba_vs_right: float = 0.320
    innings_last_14d: float = 0.0
    season_avg_innings_per_14d: float = 0.0
    recent_spin_rate: float = 0.0
    career_spin_rate_mean: float = 0.0
    career_spin_rate_std: float = 0.0

    @property
    def fatigue_score(self) -> float:
        """0-1 fatigue index based on recent workload."""
        base = min(1.0, self.pitch_count_last_3d / 100.0)
        era_penalty = max(0, (self.era_last_3 - self.era)) / 3.0
        return min(1.0, base + era_penalty * 0.3)


@dataclass
class BatterSnapshot:
    name: str
    team: str
    avg: float
    obp: float
    slg: float
    woba: float
    ops_plus: float
    clutch_woba: float
    vs_left_avg: float
    vs_right_avg: float
    barrel_pct: float = 0.0


@dataclass
class TeamSnapshot:
    team: str
    elo: float
    batting_woba: float
    batting_ops_plus: float
    pitching_fip: float
    pitching_whip: float
    pitching_stuff_plus: float
    der: float
    bullpen_depth: float
    pitch_limit: int
    bullpen_era: float = 3.50
    bullpen_pitches_3d: int = 0
    runs_per_game: float = 4.5
    runs_allowed_per_game: float = 4.5
    clutch_woba: float = 0.320
    roster_strength_index: float = 80.0
    missing_core_batter: bool = False
    ace_pitch_count_limited: bool = False
    top50_stars: int = 0
    sample_size: int = 120
    league_prior_strength: float = 0.0
    win_pct_last_10: float = 0.5
    rest_days: int = 1
    time_zone_offset: float = 0.0          # Time zone difference relative to UTC
    dist_traveled_prev_7d: float = 0.0     # km traveled in last 7 days


@dataclass
class Matchup:
    game_id: str
    tournament: str
    game_time_utc: str
    home: TeamSnapshot
    away: TeamSnapshot
    home_sp: Optional[PitcherSnapshot] = None
    away_sp: Optional[PitcherSnapshot] = None
    home_bullpen: List[PitcherSnapshot] = field(default_factory=list)
    away_bullpen: List[PitcherSnapshot] = field(default_factory=list)
    home_lineup: List[BatterSnapshot] = field(default_factory=list)
    away_lineup: List[BatterSnapshot] = field(default_factory=list)
    venue: str = ""
    round_name: str = "Pool"
    neutral_site: bool = True
    weather: str = "dome"
    umpire_id: str = "generic_avg"         # For umpire strike zone profile
    elevation_m: float = 0.0               # Venue elevation (affects ball flight)
    temp_f: float = 72.0
    humidity_pct: float = 0.50
    wind_speed_mph: float = 0.0
    wind_direction: str = "none"
    is_dome: bool = False


# ── Odds ─────────────────────────────────────────────────────────────────────

@dataclass
class OddsLine:
    sportsbook: str
    market: str           # ML | RL | OU | OE | F5 | TT
    side: str
    line: Optional[float]
    decimal_odds: float
    source_type: str      # international | tsl
    timestamp: str = ""


@dataclass
class OddsTimeSeries:
    """Tracks odds movement over time for steam-move detection."""
    sportsbook: str
    market: str
    side: str
    snapshots: List[Dict] = field(default_factory=list)
    # Each snapshot: {"timestamp": ..., "odds": ..., "line": ...}


# ── Predictions ──────────────────────────────────────────────────────────────

@dataclass
class SubModelResult:
    model_name: str
    home_win_prob: float
    away_win_prob: float
    expected_home_runs: float = 0.0
    expected_away_runs: float = 0.0
    confidence: float = 0.5
    diagnostics: Dict = field(default_factory=dict)


@dataclass
class PredictionResult:
    game_id: str
    home_win_prob: float
    away_win_prob: float
    expected_home_runs: float
    expected_away_runs: float
    x_factors: List[str]
    diagnostics: Dict[str, float]
    sub_model_results: List[SubModelResult] = field(default_factory=list)
    confidence_score: float = 0.5
    market_bias_score: float = 0.0


# ── Simulation ───────────────────────────────────────────────────────────────

@dataclass
class SimulationSummary:
    home_win_prob: float
    away_win_prob: float
    over_prob: float
    under_prob: float
    home_cover_prob: float
    away_cover_prob: float
    mean_total_runs: float = 0.0
    std_total_runs: float = 0.0
    odd_prob: float = 0.5
    even_prob: float = 0.5
    home_f5_win_prob: float = 0.5
    away_f5_win_prob: float = 0.5
    score_distribution: Dict = field(default_factory=dict)
    scenarios: Dict = field(default_factory=dict)
    n_simulations: int = 50_000


# ── Betting ──────────────────────────────────────────────────────────────────

@dataclass
class BetRecommendation:
    market: str
    side: str
    line: Optional[float]
    sportsbook: str
    source_type: str
    win_probability: float
    implied_probability: float
    ev: float
    edge: float
    kelly_fraction: float
    stake_fraction: float
    stake_amount: float = 0.0
    confidence: float = 0.5
    reason: str = ""


# ── Backtest ─────────────────────────────────────────────────────────────────

@dataclass
class BacktestMetrics:
    total_bets: int = 0
    wins: int = 0
    losses: int = 0
    total_staked: float = 0.0
    total_return: float = 0.0
    roi: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    avg_ev: float = 0.0
    win_rate: float = 0.0
    profit_factor: float = 0.0
    kelly_growth_rate: float = 0.0


# ── Training Results ─────────────────────────────────────────────────────────

@dataclass
class TrainingResult:
    model_name: str
    accuracy: float
    logloss: float
    brier_score: float
    auc_roc: float = 0.0
    feature_importance: Dict[str, float] = field(default_factory=dict)
    training_time_seconds: float = 0.0
    n_samples: int = 0
    cv_scores: List[float] = field(default_factory=list)


# ── Game Output ──────────────────────────────────────────────────────────────

@dataclass
class GameOutput:
    """Final output for each game — all 10 required fields."""
    game_id: str
    home_team: str
    away_team: str
    home_win_prob: float
    away_win_prob: float
    predicted_home_score: float
    predicted_away_score: float
    market_bias_score: float
    ev_best: float
    best_bet_strategy: str
    confidence_index: float
    top_3_bets: List[BetRecommendation] = field(default_factory=list)


# ── API Contracts ────────────────────────────────────────────────────────────

@dataclass
class AnalyzeRequest:
    game_id: str
    line_total: float = 7.5
    line_spread_home: float = -1.5
    force_retrain: bool = False


@dataclass
class AnalyzeResponse:
    game_output: Optional[GameOutput] = None
    markdown_report: str = ""
    json_report: str = ""
    decision_report: Optional[Any] = None
    calibration_metrics: Optional[Dict[str, float]] = None
    portfolio_metrics: Optional[Dict[str, float]] = None
    deployment_gate_report: Optional[Dict[str, Any]] = None
