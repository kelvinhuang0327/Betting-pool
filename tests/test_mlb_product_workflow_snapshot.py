from __future__ import annotations

import csv
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from wbc_backend.recommendation import mlb_product_workflow_snapshot as wf


def _write_eval_csv(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "Date",
                "Away",
                "Away Score",
                "Home",
                "Home Score",
                "Status",
                "Away ML",
                "Home ML",
                "Home RL Spread",
                "RL Away",
                "RL Home",
                "O/U",
                "Over",
                "Under",
            ]
        )
        writer.writerow(
            [
                "2025-08-01",
                "Away A",
                "3",
                "Home A",
                "5",
                "Final",
                "+120",
                "-130",
                "-1.5",
                "-105",
                "-115",
                "8.5",
                "-110",
                "-110",
            ]
        )
        writer.writerow(
            [
                "2025-08-02",
                "Away B",
                "6",
                "Home B",
                "2",
                "Final",
                "-140",
                "+125",
                "+1.5",
                "-120",
                "+100",
                "9.0",
                "+100",
                "-120",
            ]
        )


def test_american_to_decimal_and_ev_kelly():
    assert wf.american_to_decimal("-150") == pytest.approx(1.666667)
    assert wf.american_to_decimal("+125") == pytest.approx(2.25)
    assert wf.american_to_decimal("0") is None

    result = wf.calculate_ev_kelly(probability=0.6, decimal_odds=2.0)
    assert result["expected_value_per_unit"] == pytest.approx(0.2)
    assert result["full_kelly_fraction"] == pytest.approx(0.2)
    assert result["used_kelly_fraction"] == pytest.approx(0.015)


def test_build_moneyline_backtest_scores_candidates(tmp_path: Path):
    eval_csv = tmp_path / "eval.csv"
    _write_eval_csv(eval_csv)
    predictions = [
        {
            "game_date": "2025-08-01",
            "away_team": "Away A",
            "home_team": "Home A",
            "model_name": "model_x",
            "predicted_home_win_probability": 0.66,
            "selected_side": "HOME",
            "confidence_band": "HIGH",
            "actual_home_win": 1,
            "correct": 1,
        },
        {
            "game_date": "2025-08-02",
            "away_team": "Away B",
            "home_team": "Home B",
            "model_name": "model_x",
            "predicted_home_win_probability": 0.44,
            "selected_side": "AWAY",
            "confidence_band": "MEDIUM",
            "actual_home_win": 0,
            "correct": 1,
        },
    ]

    result = wf.build_moneyline_backtest(
        scorecard_predictions=predictions,
        eval_path=eval_csv,
        model_name="model_x",
        min_ev=0.0,
        min_edge=0.0,
    )

    assert result["summary"]["prediction_rows_scored"] == 2
    assert result["summary"]["paper_candidate_count"] >= 1
    assert result["summary"]["hit_rate"] == pytest.approx(1.0)
    assert all(row["guard_status"] == "PAPER_ONLY_LOCAL_REPLAY" for row in result["rows"])


def test_market_coverage_reports_supported_and_pending_markets(tmp_path: Path):
    eval_csv = tmp_path / "eval.csv"
    _write_eval_csv(eval_csv)

    coverage = wf.build_market_coverage(eval_csv)

    assert coverage["markets"]["moneyline"]["status"] == "EVALUATED_IN_WORKFLOW"
    assert coverage["markets"]["moneyline"]["rows_with_lines"] == 2
    assert coverage["markets"]["run_line"]["rows_with_lines"] == 2
    assert coverage["markets"]["total_runs"]["rows_with_lines"] == 2
    assert coverage["markets"]["first_five"]["status"] == "NO_LOCAL_F5_LINES_OR_F5_RESULTS_IN_SOURCE"


def test_local_2026_snapshot_includes_outcome_accuracy(tmp_path: Path):
    pred = tmp_path / "pred.jsonl"
    out = tmp_path / "out.jsonl"
    rows = [
        {
            "game_date": "2026-05-20",
            "away_team": "Away",
            "home_team": "Home",
            "model_probability": 0.62,
            "predicted_side": "home",
            "source_prediction_version": "v1",
            "paper_only": True,
            "production_ready": False,
        }
    ]
    pred.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    out.write_text(
        json.dumps(
            {
                **rows[0],
                "outcome_available": True,
                "is_correct": True,
                "rule_primary_125_flag": True,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    snapshot = wf.build_local_2026_prediction_snapshot(
        prediction_path=pred,
        outcome_path=out,
    )

    assert snapshot["rows"] == 1
    assert snapshot["latest_local_prediction_date"] == "2026-05-20"
    assert snapshot["outcome_attached_summary"]["all_outcome_attached"]["accuracy"] == pytest.approx(1.0)
    assert snapshot["top_latest_predictions"][0]["selected_side_probability"] == pytest.approx(0.62)
    assert snapshot["generated_by_corrected_retrained_model"] is False
    assert snapshot["corrected_model_handoff_status"] == "NOT_PERFORMED"


def test_visible_reports_separate_corrected_2025_from_baseline_2026(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    eval_csv = tmp_path / "eval.csv"
    _write_eval_csv(eval_csv)
    prediction_path = tmp_path / "predictions_2026.jsonl"
    prediction_path.write_text(
        json.dumps(
            {
                "game_date": "2026-05-31",
                "away_team": "Away 2026",
                "home_team": "Home 2026",
                "model_probability": 0.57,
                "predicted_side": "home",
                "source_prediction_version": "p84b_diagnostic_baseline_v1",
                "paper_only": True,
                "production_ready": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    predictions = [
        {
            "game_date": "2025-08-01",
            "away_team": "Away A",
            "home_team": "Home A",
            "model_name": "corrected_model",
            "predicted_home_win_probability": 0.66,
            "selected_side": "HOME",
            "confidence_band": "HIGH",
            "actual_home_win": 1,
            "correct": 1,
        },
        {
            "game_date": "2025-08-02",
            "away_team": "Away B",
            "home_team": "Home B",
            "model_name": "corrected_model",
            "predicted_home_win_probability": 0.44,
            "selected_side": "AWAY",
            "confidence_band": "MEDIUM",
            "actual_home_win": 0,
            "correct": 1,
        },
    ]
    scorecard = SimpleNamespace(
        warmup_rows=10,
        eval_rows=20,
        split={
            "train_period": ["2025-04-01", "2025-07-31"],
            "test_period": ["2025-08-01", "2025-09-30"],
            "train_rows": 12,
            "test_rows": 8,
            "train_date_count": 10,
            "test_date_count": 8,
            "requested_train_frac": 0.6,
            "effective_train_frac": 0.6,
            "split_strategy": "complete_date_boundary_nearest_requested_row_fraction",
            "tie_rule": "earlier boundary (smaller train partition) wins equal-distance ties",
            "selected_boundary_date": "2025-07-31",
            "selected_test_start_date": "2025-08-01",
        },
        best_by_brier="corrected_model",
        train_home_win_prior=0.55,
        platt={"A": 1.0, "B": 0.0},
        comparison=[
            {
                "model_name": "corrected_model",
                "accuracy": 0.625,
                "brier_score": 0.24,
                "log_loss": 0.68,
                "calibration_error": 0.04,
                "coverage": 1.0,
            }
        ],
        confidence_band_breakdown={"MEDIUM": {"n": 8, "correct": 5}},
        selected_side_distribution={"HOME": 4, "AWAY": 4},
        predictions=predictions,
    )
    monkeypatch.setattr(wf, "run_scorecard", lambda *_args, **_kwargs: scorecard)

    payload = wf.run_workflow_snapshot(
        warmup_path=tmp_path / "warmup.csv",
        eval_path=eval_csv,
        prediction_2026_path=prediction_path,
    )
    paths = wf.write_workflow_reports(payload, tmp_path / "report")
    markdown = paths["markdown"].read_text(encoding="utf-8")
    json_payload = json.loads(paths["json"].read_text(encoding="utf-8"))

    assert "Corrected 2025 Local Retrain and Evaluation" in markdown
    assert "Existing 2026 Prediction Snapshot (Separate and Stale)" in markdown
    assert "p84b_diagnostic_baseline_v1" in markdown
    assert "Corrected 2025 retrained model generated these 2026 predictions: `False`" in markdown
    assert "not a verified betting edge" in markdown
    snapshot = json_payload["local_2026_prediction_snapshot"]
    assert snapshot["source_prediction_version"] == "p84b_diagnostic_baseline_v1"
    assert snapshot["generated_by_corrected_retrained_model"] is False
    assert json_payload["claim_status"]["verified_betting_edge_established"] is False
