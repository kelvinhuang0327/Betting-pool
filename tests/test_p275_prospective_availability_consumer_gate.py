"""Focused offline tests for the P275 result-availability consumer gate."""
from __future__ import annotations

import json
import shutil
import socket
from pathlib import Path

import pytest

from scripts import _p274_prospective_result_availability_index as p274
from scripts import _p275_prospective_availability_consumer_gate as p275


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_ROOT = REPO_ROOT / "data/mlb_2026/derived/p274_prospective_result_availability_index_v1"
INDEX_PATH = INDEX_ROOT / p274.INDEX_FILENAME
GAME_ID = "mlb_2026_825108"
OBSERVED_AT = "2026-07-13T07:17:10.769880Z"
BEFORE = "2026-07-13T07:17:10.769879Z"
AFTER = "2026-07-13T07:17:10.769881Z"


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_network(*args, **kwargs):
        raise AssertionError("P275 tests must make zero network calls")

    monkeypatch.setattr(socket, "create_connection", forbidden_network)
    monkeypatch.setattr(socket, "socket", forbidden_network)


def test_before_observation_is_rejected() -> None:
    decision = p275.evaluate_result_availability(INDEX_PATH, GAME_ID, BEFORE)

    assert decision.result_usage_allowed is False
    assert decision.block_reason == p275.RESULT_NOT_YET_AVAILABLE
    assert decision.result_available_at_utc == OBSERVED_AT
    assert decision.availability_semantics == "LOCAL_OBSERVATION_LOWER_BOUND"
    assert decision.retroactive_certification is False


@pytest.mark.parametrize("feature_as_of_utc", [OBSERVED_AT, AFTER])
def test_exact_and_after_observation_are_accepted(feature_as_of_utc: str) -> None:
    decision = p275.evaluate_result_availability(
        INDEX_PATH,
        GAME_ID,
        feature_as_of_utc,
    )

    assert decision.result_usage_allowed is True
    assert decision.block_reason is None
    assert decision.feature_as_of_utc == feature_as_of_utc
    assert decision.result_available_at_utc == OBSERVED_AT


def test_missing_game_evidence_is_rejected_without_inference() -> None:
    decision = p275.evaluate_result_availability(
        INDEX_PATH,
        "mlb_2026_999999",
        AFTER,
    )

    assert decision.result_usage_allowed is False
    assert decision.block_reason == p275.MISSING_AVAILABILITY_EVIDENCE
    assert decision.result_available_at_utc is None
    assert decision.retroactive_certification is False


def test_missing_index_publication_is_rejected(tmp_path: Path) -> None:
    decision = p275.evaluate_result_availability(
        tmp_path / p274.INDEX_FILENAME,
        GAME_ID,
        AFTER,
    )

    assert decision.result_usage_allowed is False
    assert decision.block_reason == p275.MISSING_AVAILABILITY_EVIDENCE


def test_tampered_index_is_rejected(tmp_path: Path) -> None:
    copied_root = tmp_path / "p274-index"
    shutil.copytree(INDEX_ROOT, copied_root)
    copied_index = copied_root / p274.INDEX_FILENAME
    payload = json.loads(copied_index.read_text(encoding="utf-8"))
    payload["records"][0]["result_available_at_utc"] = AFTER
    copied_index.write_bytes(p274.canonical_json_bytes(payload, trailing_newline=True))

    decision = p275.evaluate_result_availability(copied_index, GAME_ID, AFTER)

    assert decision.result_usage_allowed is False
    assert decision.block_reason == p275.INVALID_AVAILABILITY_EVIDENCE
    assert decision.result_available_at_utc is None


def test_invalid_feature_timestamp_is_rejected() -> None:
    decision = p275.evaluate_result_availability(
        INDEX_PATH,
        GAME_ID,
        "2026-07-13T07:17:10.769880+00:00",
    )

    assert decision.result_usage_allowed is False
    assert decision.block_reason == p275.INVALID_FEATURE_AS_OF_UTC
    assert decision.feature_as_of_utc is None
