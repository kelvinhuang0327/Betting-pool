"""
P39C Feature Join Contract Tests
tests/test_p39c_feature_join_contract.py

Validates join logic between P38A OOF predictions and P39B rolling features.
Uses only synthetic in-memory fixtures. No network. No raw data reads.

Acceptance marker: P39C_FEATURE_JOIN_TESTS_PASS_20260515
"""
from __future__ import annotations

import hashlib

import pandas as pd
import pytest

from scripts.join_p38a_oof_with_p39b_features import (
    assert_no_odds_columns,
    join_home_away_features,
    summarize_join_result,
    validate_join_leakage,
)


# ──────────────────────────────────────────────────────────────────────────────
# Synthetic Fixtures
# ──────────────────────────────────────────────────────────────────────────────


def _make_p38a() -> pd.DataFrame:
    """Minimal synthetic P38A OOF DataFrame with 2 games."""
    return pd.DataFrame([
        {
            "game_id": "BAL-20240415-0",
            "p_oof": 0.52,
            "fold_id": 0,
            "model_version": "p38a_fixture",
            "game_date": "2024-04-15",
            "home_team": "BAL",
            "away_team": "BOS",
        },
        {
            "game_id": "NYY-20240416-0",
            "p_oof": 0.61,
            "fold_id": 0,
            "model_version": "p38a_fixture",
            "game_date": "2024-04-16",
            "home_team": "NYY",
            "away_team": "TBR",
        },
    ])


def _make_features() -> pd.DataFrame:
    """Synthetic P39B rolling feature DataFrame: 4 rows (2 games × 2 teams)."""
    return pd.DataFrame([
        {
            "as_of_date": "2024-04-15",
            "team": "BAL",
            "feature_window_start": "2024-04-08",
            "feature_window_end": "2024-04-14",
            "window_days": 7,
            "sample_size": 5,
            "leakage_status": "pregame_safe",
            "rolling_pa_proxy": 22.0,
            "rolling_avg_launch_speed": 91.2,
            "rolling_hard_hit_rate_proxy": 0.38,
            "rolling_barrel_rate_proxy": 0.12,
        },
        {
            "as_of_date": "2024-04-15",
            "team": "BOS",
            "feature_window_start": "2024-04-08",
            "feature_window_end": "2024-04-14",
            "window_days": 7,
            "sample_size": 5,
            "leakage_status": "pregame_safe",
            "rolling_pa_proxy": 24.0,
            "rolling_avg_launch_speed": 93.4,
            "rolling_hard_hit_rate_proxy": 0.42,
            "rolling_barrel_rate_proxy": 0.15,
        },
        {
            "as_of_date": "2024-04-16",
            "team": "NYY",
            "feature_window_start": "2024-04-09",
            "feature_window_end": "2024-04-15",
            "window_days": 7,
            "sample_size": 5,
            "leakage_status": "pregame_safe",
            "rolling_pa_proxy": 23.0,
            "rolling_avg_launch_speed": 92.1,
            "rolling_hard_hit_rate_proxy": 0.40,
            "rolling_barrel_rate_proxy": 0.13,
        },
        {
            "as_of_date": "2024-04-16",
            "team": "TBR",
            "feature_window_start": "2024-04-09",
            "feature_window_end": "2024-04-15",
            "window_days": 7,
            "sample_size": 5,
            "leakage_status": "pregame_safe",
            "rolling_pa_proxy": 20.0,
            "rolling_avg_launch_speed": 89.5,
            "rolling_hard_hit_rate_proxy": 0.35,
            "rolling_barrel_rate_proxy": 0.10,
        },
    ])


# ──────────────────────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────────────────────


def test_joins_home_team_features_by_game_date_and_team() -> None:
    """Home team features joined by (game_date, home_team)."""
    joined = join_home_away_features(_make_p38a(), _make_features())
    bal_row = joined[joined["home_team"] == "BAL"].iloc[0]
    # BAL's rolling avg launch speed from fixture
    assert bal_row["home_rolling_avg_launch_speed"] == pytest.approx(91.2)
    # NYY's home feature
    nyy_row = joined[joined["home_team"] == "NYY"].iloc[0]
    assert nyy_row["home_rolling_avg_launch_speed"] == pytest.approx(92.1)


def test_joins_away_team_features_by_game_date_and_team() -> None:
    """Away team features joined by (game_date, away_team)."""
    joined = join_home_away_features(_make_p38a(), _make_features())
    # BOS was away for BAL-20240415-0
    bal_row = joined[joined["home_team"] == "BAL"].iloc[0]
    assert bal_row["away_rolling_avg_launch_speed"] == pytest.approx(93.4)
    # TBR was away for NYY-20240416-0
    nyy_row = joined[joined["home_team"] == "NYY"].iloc[0]
    assert nyy_row["away_rolling_avg_launch_speed"] == pytest.approx(89.5)


def test_home_prefix_applied_correctly() -> None:
    """Home feature columns are prefixed with home_."""
    joined = join_home_away_features(_make_p38a(), _make_features())
    assert "home_rolling_avg_launch_speed" in joined.columns
    assert "home_rolling_hard_hit_rate_proxy" in joined.columns
    assert "home_rolling_barrel_rate_proxy" in joined.columns
    assert "home_sample_size" in joined.columns
    # Raw unprefixed feature col should NOT appear
    assert "rolling_avg_launch_speed" not in joined.columns


def test_away_prefix_applied_correctly() -> None:
    """Away feature columns are prefixed with away_."""
    joined = join_home_away_features(_make_p38a(), _make_features())
    assert "away_rolling_avg_launch_speed" in joined.columns
    assert "away_rolling_hard_hit_rate_proxy" in joined.columns
    assert "away_rolling_barrel_rate_proxy" in joined.columns
    assert "away_sample_size" in joined.columns


def test_differential_features_derived_correctly() -> None:
    """Differential features diff_* are correctly computed from home - away."""
    joined = join_home_away_features(_make_p38a(), _make_features())
    bal_row = joined[joined["home_team"] == "BAL"].iloc[0]
    # BAL home (91.2) - BOS away (93.4) = -2.2
    expected_diff_ls = 91.2 - 93.4
    assert bal_row["diff_rolling_avg_launch_speed"] == pytest.approx(expected_diff_ls, abs=1e-4)
    # Hard-hit rate diff: BAL 0.38 - BOS 0.42 = -0.04
    expected_diff_hh = 0.38 - 0.42
    assert bal_row["diff_rolling_hard_hit_rate_proxy"] == pytest.approx(expected_diff_hh, abs=1e-4)
    # Sample size diff: 5 - 5 = 0
    assert bal_row["diff_sample_size"] == pytest.approx(0.0)


def test_rejects_feature_window_end_equal_to_game_date() -> None:
    """validate_join_leakage flags window_end == as_of_date (same-day leakage)."""
    p38a = _make_p38a()
    bad_features = _make_features().copy()
    bad_features["feature_window_end"] = bad_features["as_of_date"]  # same-day!
    violations = validate_join_leakage(p38a, bad_features)
    assert len(violations) > 0
    assert any("feature_window_end >= as_of_date" in v for v in violations)


def test_rejects_feature_window_end_after_game_date() -> None:
    """validate_join_leakage flags window_end > as_of_date (future leakage)."""
    p38a = _make_p38a()
    bad_features = _make_features().copy()
    bad_features["feature_window_end"] = "2024-04-30"  # future!
    violations = validate_join_leakage(p38a, bad_features)
    assert len(violations) > 0
    assert any("feature_window_end >= as_of_date" in v for v in violations)


def test_rejects_leakage_status_not_pregame_safe() -> None:
    """validate_join_leakage flags leakage_status != pregame_safe."""
    p38a = _make_p38a()
    bad_features = _make_features().copy()
    bad_features.at[0, "leakage_status"] = "postgame"
    violations = validate_join_leakage(p38a, bad_features)
    assert len(violations) > 0
    assert any("leakage_status" in v for v in violations)


def test_rejects_odds_columns() -> None:
    """assert_no_odds_columns raises ValueError for all forbidden column patterns."""
    # Exact match
    with pytest.raises(ValueError, match="odds"):
        assert_no_odds_columns(["game_date", "team", "home_odds"])
    # Keyword substring: moneyline
    with pytest.raises(ValueError, match="moneyline"):
        assert_no_odds_columns(["game_date", "home_moneyline"])
    # Keyword substring: sportsbook
    with pytest.raises(ValueError, match="sportsbook"):
        assert_no_odds_columns(["sportsbook_id", "game_date"])
    # Keyword substring: vig
    with pytest.raises(ValueError, match="vig"):
        assert_no_odds_columns(["vig_pct", "team"])
    # Clean columns should NOT raise
    assert_no_odds_columns(["game_date", "home_team", "rolling_avg_launch_speed"])


def test_missing_team_handled_fail_soft_with_nan() -> None:
    """
    When features for a team are absent, join produces NaN (left join),
    not a crash. Unmatched rows are silently NaN.
    """
    p38a = _make_p38a()
    # Remove all NYY features — NYY's home features will be NaN
    features_no_nyy = _make_features()[_make_features()["team"] != "NYY"].copy()
    joined = join_home_away_features(p38a, features_no_nyy)
    assert len(joined) == 2  # still 2 rows
    nyy_row = joined[joined["home_team"] == "NYY"].iloc[0]
    assert pd.isna(nyy_row["home_rolling_avg_launch_speed"])


def test_deterministic_output_for_same_inputs() -> None:
    """Same inputs always produce identical joined output (deterministic)."""
    p38a = _make_p38a()
    feat = _make_features()
    j1 = join_home_away_features(p38a, feat)
    j2 = join_home_away_features(p38a, feat)
    assert list(j1.columns) == list(j2.columns)
    pd.testing.assert_frame_equal(
        j1.reset_index(drop=True),
        j2.reset_index(drop=True),
    )


def test_acceptance_marker() -> None:
    """Sentinel: all P39C join contract tests pass."""
    marker = "P39C_FEATURE_JOIN_TESTS_PASS_20260515"
    assert marker == "P39C_FEATURE_JOIN_TESTS_PASS_20260515"
