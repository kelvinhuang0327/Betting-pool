from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wbc_backend.betting.optimizer import find_top_bets
from wbc_backend.config.settings import AppConfig
from wbc_backend.domain.schemas import OddsLine
from wbc_backend.research.runtime import run_research_cycle
from wbc_backend.scheduler.jobs import AutoScheduler


class DummyCLV:
    def __init__(self, *_args, **_kwargs):
        pass

    def predict_closing_odds(self, *_args, **_kwargs):
        return 1.85

    def get_market_efficiency_score(self, *_args, **_kwargs):
        return 0.90


class TestOptimizerRegression(unittest.TestCase):
    def test_confidence_not_cascading_between_candidates(self):
        odds = [
            OddsLine(
                sportsbook="BookA",
                market="ML",
                side="TPE",
                line=None,
                decimal_odds=2.2,
                source_type="intl",
            ),
            OddsLine(
                sportsbook="BookB",
                market="ML",
                side="TPE",
                line=None,
                decimal_odds=2.2,
                source_type="intl",
            ),
        ]
        true_probs = {"ML_TPE": 0.70}
        config = AppConfig()

        with patch("wbc_backend.betting.optimizer.ClosingLineModel", DummyCLV):
            bets = find_top_bets(
                odds_lines=odds,
                true_probs=true_probs,
                home_code="TPE",
                away_code="AUS",
                confidence_score=0.50,
                config=config,
            )

        self.assertEqual(len(bets), 2)
        self.assertAlmostEqual(bets[0].confidence, bets[1].confidence, places=4)


class TestRuntimeAndScheduler(unittest.TestCase):
    def test_research_cycle_writes_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            artifact = Path(td) / "v3_cycle.json"
            payload = run_research_cycle(seed=42, artifact_path=artifact)
            self.assertTrue(artifact.exists())
            self.assertTrue(payload["all_passed"])

            parsed = json.loads(artifact.read_text())
            self.assertEqual(parsed["phase_count"], 6)

    def test_scheduler_registers_research_cycle_task(self):
        scheduler = AutoScheduler(AppConfig())
        scheduler.setup_default_tasks()
        task_names = [t.name for t in scheduler.tasks]
        self.assertIn("research_cycle", task_names)


if __name__ == "__main__":
    unittest.main()
