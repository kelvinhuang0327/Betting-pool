from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wbc_backend.config.settings import AppConfig, DataSourceConfig
from wbc_backend.reporting.postgame_learning import (
    extract_sub_model_predictions,
    load_latest_prediction_record,
    record_postgame_outcome,
)
from wbc_backend.strategy import live_retrainer


def _make_prediction_record(game_id: str, home: str, away: str, home_prob: float) -> dict:
    return {
        "recorded_at_utc": "2026-03-09T07:08:58.203790+00:00",
        "game_id": game_id,
        "teams": {"home": home, "away": away},
        "verification": {
            "status": "VERIFIED_WITH_FALLBACK",
            "used_fallback_lineup": True,
        },
        "game_output": {
            "predicted_home_score": 2.41,
            "predicted_away_score": 6.72,
            "confidence_index": 0.542045,
        },
        "prediction": {
            "home_win_prob": home_prob,
            "away_win_prob": 1.0 - home_prob,
            "sub_model_results": [
                {"model_name": "elo", "home_win_prob": 0.3733},
                {"model_name": "bayesian", "home_win_prob": 0.2437},
                {"model_name": "neural_net", "home_win_prob": 0.2419},
            ],
        },
        "decision_report": {
            "decision": "NO_BET",
            "reasoning": ["Edge score below threshold"],
        },
    }


class TestPostgameLearning(unittest.TestCase):
    def test_load_latest_prediction_record_returns_last_match(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry_path = root / "prediction_registry.jsonl"
            registry_path.write_text(
                "\n".join(
                    [
                        json.dumps(_make_prediction_record("C09", "AUS", "KOR", 0.30)),
                        json.dumps(_make_prediction_record("C09", "AUS", "KOR", 0.26)),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            config = AppConfig(
                sources=DataSourceConfig(
                    prediction_registry_jsonl=str(registry_path),
                    postgame_results_jsonl=str(root / "postgame_results.jsonl"),
                )
            )

            record = load_latest_prediction_record(config=config, game_id="C09")
            self.assertIsNotNone(record)
            self.assertAlmostEqual(record["prediction"]["home_win_prob"], 0.26)

    def test_record_postgame_outcome_appends_result_and_updates_retrainer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            registry_path = root / "prediction_registry.jsonl"
            postgame_path = root / "postgame_results.jsonl"
            state_path = root / "retrainer_state.json"

            registry_path.write_text(
                json.dumps(_make_prediction_record("C09", "AUS", "KOR", 0.2635)) + "\n",
                encoding="utf-8",
            )

            config = AppConfig(
                sources=DataSourceConfig(
                    prediction_registry_jsonl=str(registry_path),
                    postgame_results_jsonl=str(postgame_path),
                )
            )

            original_state_file = live_retrainer.STATE_FILE
            live_retrainer.STATE_FILE = state_path
            try:
                payload = record_postgame_outcome(
                    config=config,
                    game_id="C09",
                    home_team="AUS",
                    away_team="KOR",
                    home_score=2,
                    away_score=7,
                    source_urls=["https://www.yonhapnewstv.co.kr/news/MYH20260309208700641"],
                    notes=["KOR won after Moon Bo-gyeong homered twice."],
                )
            finally:
                live_retrainer.STATE_FILE = original_state_file

            self.assertTrue(postgame_path.exists())
            lines = postgame_path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            stored = json.loads(lines[0])
            self.assertEqual(stored["game_id"], "C09")
            self.assertTrue(stored["evaluation"]["winner_correct"])
            self.assertTrue(stored["learning"]["applied"])
            self.assertIn("updated_weights", stored["learning"])
            self.assertTrue(state_path.exists())

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertIn("elo", state["performances"])
            self.assertEqual(payload["prediction_summary"]["decision"], "NO_BET")

    def test_extract_sub_model_predictions_ignores_invalid_rows(self):
        record = {
            "prediction": {
                "sub_model_results": [
                    {"model_name": "elo", "home_win_prob": 0.52},
                    {"model_name": "", "home_win_prob": 0.50},
                    {"model_name": "bad", "home_win_prob": "oops"},
                ]
            }
        }

        preds = extract_sub_model_predictions(record)
        self.assertEqual(preds, {"elo": 0.52})


if __name__ == "__main__":
    unittest.main()
