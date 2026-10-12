"""Focused deterministic offline tests for the P280-A capture boundary."""
from __future__ import annotations

import csv
import json
import os
import socket
from copy import deepcopy
from pathlib import Path

import pytest

from wbc_backend.recommendation import moneyline_shadow_capture as capture


AS_OF = "2099-01-01T00:00:00.123456Z"
START_LATER_A = "2099-01-01T00:00:00.123457Z"
START_LATER_B = "2099-01-01T00:01:00.123456Z"
START_EXACT = AS_OF
START_EARLIER = "2099-01-01T00:00:00.123455Z"
SOURCE_COMMIT = "a" * 40
MODEL_ID = "synthetic_future_moneyline_shadow"
MODEL_VERSION = "p280a_synthetic_future_v1"
MODEL_FINGERPRINT = "b" * 64
STATE_FINGERPRINT = "c" * 64
INPUT_FINGERPRINT = "d" * 64


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_network(*args, **kwargs):
        raise AssertionError("P280-A tests must make zero network calls")

    monkeypatch.setattr(socket, "create_connection", forbidden_network)
    monkeypatch.setattr(socket, "socket", forbidden_network)


def _row(game_id: str, probability: object = 0.61) -> dict[str, object]:
    probability_float = float(probability)
    return {
        "game_id": game_id,
        "game_date": "2099-01-01",
        "away_team": f"Away {game_id}",
        "home_team": f"Home {game_id}",
        "shadow_home_win_probability": probability,
        "predicted_side": "HOME" if probability_float >= 0.5 else "AWAY",
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
    }


def _write_fixture(
    root: Path,
    *,
    rows: list[dict[str, object]] | None = None,
    manifest_mutation=None,
) -> dict[str, object]:
    report = root / "report"
    report.mkdir(parents=True)
    artifact = report / "future_predictions.csv"
    manifest_path = report / "future_manifest.json"
    rows = rows or [_row("future-game-a", 0.61), _row("future-game-b", 0.39)]
    with artifact.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    artifact_hash = capture._sha256_file(artifact)
    manifest = {
        "artifact_version": MODEL_VERSION,
        "source_git_commit": SOURCE_COMMIT,
        "generation": {
            "runtime_metadata": {"generated_at_utc": "2098-12-31T23:59:00Z"}
        },
        "model": {
            "model_id": MODEL_ID,
            "model_version": MODEL_VERSION,
            "model_code_config_fingerprint": MODEL_FINGERPRINT,
        },
        "training": {"final_state_fingerprint": STATE_FINGERPRINT},
        "prediction_input": {"prediction_input_fingerprint": INPUT_FINGERPRINT},
        "artifacts": {
            "predictions_csv": "report/future_predictions.csv",
            "predictions_csv_sha256": artifact_hash,
            "manifest_json": "report/future_manifest.json",
            "prediction_row_count": len(rows),
        },
    }
    if manifest_mutation is not None:
        manifest_mutation(manifest)
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return {
        "root": root,
        "prediction_artifact_relative_path": "report/future_predictions.csv",
        "prediction_artifact_sha256": artifact_hash,
        "prediction_manifest_relative_path": "report/future_manifest.json",
        "prediction_manifest_sha256": capture._sha256_file(manifest_path),
        "source_git_commit": SOURCE_COMMIT,
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "model_code_config_fingerprint": MODEL_FINGERPRINT,
        "final_state_fingerprint": STATE_FINGERPRINT,
        "prediction_input_fingerprint": INPUT_FINGERPRINT,
        "prediction_row_count": len(rows),
        "prediction_as_of_utc": AS_OF,
        "scheduled_starts": [
            {
                "game_id": "future-game-a",
                "scheduled_start_utc": START_LATER_A,
                "trusted": True,
            },
            {
                "game_id": "future-game-b",
                "scheduled_start_utc": START_LATER_B,
                "trusted": True,
            },
        ],
        "created_runtime_metadata": {
            "created_at_utc": "2099-01-01T00:00:00.123456Z",
            "execution_context": "pytest-temporary-root",
        },
    }


def _success_capture(tmp_path: Path) -> tuple[dict[str, object], dict[str, object]]:
    kwargs = _write_fixture(tmp_path)
    return capture.register_prospective_capture(**kwargs), kwargs


def _synthetic_verification(record: dict[str, object]) -> dict[str, object]:
    return {
        "status": "PASSED",
        "fixture_storage": "TEST_FRAMEWORK_MANAGED_TEMPORARY_ROOTS",
        "capture_id": record["capture_id"],
        "deterministic_payload_sha256": record["deterministic_payload_sha256"],
        "all_rows_pregame_eligible": True,
        "one_microsecond_before_scheduled_start": "ELIGIBLE",
        "exact_scheduled_start": "NOT_ELIGIBLE",
        "one_microsecond_after_scheduled_start": "NOT_ELIGIBLE",
        "missing_scheduled_start": "NOT_ELIGIBLE",
        "conflicting_duplicate_game_id": "FAIL_CLOSED",
        "tampered_prediction": "FAIL_CLOSED",
        "tampered_manifest": "FAIL_CLOSED",
        "repeated_capture_deterministic": True,
    }


def _normalized_readiness(payload: dict[str, object]) -> dict[str, object]:
    normalized = deepcopy(payload)
    normalized["runtime_metadata"] = "NORMALIZED"
    return normalized


def _normalized_markdown(value: str) -> str:
    return "\n".join(
        line
        for line in value.splitlines()
        if not line.startswith("- Generated at:")
    )


def test_synthetic_future_fixture_registers_pregame_capture(tmp_path: Path) -> None:
    record, _ = _success_capture(tmp_path)

    assert record["capture_schema_version"] == capture.CAPTURE_SCHEMA_VERSION
    assert record["capture_semantics"] == "LOCAL_OBSERVATION_LOWER_BOUND"
    assert record["retroactive_certification"] is False
    assert record["prediction_as_of_utc"] == AS_OF
    assert record["prediction_row_count"] == 2
    assert record["pregame_certified"] is True
    assert record["pregame_eligible_row_count"] == 2
    assert record["non_pregame_or_missing_schedule_row_count"] == 0
    assert record["reason_counts"] == {capture.PREGAME_ELIGIBLE: 2}
    assert record["paper_only"] is True
    assert record["production_ready"] is False
    assert record["deterministic_payload_sha256"] == (
        capture.deterministic_payload_hash(record)
    )


@pytest.mark.parametrize(
    "bad_as_of",
    [
        None,
        "",
        "2099-01-01",
        "2099-01-01T00:00:00",
        "2099-01-01T08:00:00+08:00",
        "2099-01-01T00:00:00.123Z",
        "not-a-time",
    ],
)
def test_explicit_canonical_z_prediction_as_of_is_required(
    tmp_path: Path, bad_as_of: object
) -> None:
    kwargs = _write_fixture(tmp_path)
    kwargs["prediction_as_of_utc"] = bad_as_of
    with pytest.raises(capture.CaptureContractError, match="prediction_as_of_utc"):
        capture.register_prospective_capture(**kwargs)


def test_generation_time_and_mtime_are_never_as_of_fallbacks(tmp_path: Path) -> None:
    kwargs = _write_fixture(tmp_path)
    artifact = tmp_path / str(kwargs["prediction_artifact_relative_path"])
    os.utime(artifact, (4_070_908_800, 4_070_908_800))
    kwargs["prediction_artifact_sha256"] = capture._sha256_file(artifact)
    kwargs["prediction_as_of_utc"] = None

    with pytest.raises(capture.CaptureContractError, match="prediction_as_of_utc"):
        capture.register_prospective_capture(**kwargs)


def test_schedule_boundaries_fail_closed_per_row(tmp_path: Path) -> None:
    rows = [
        _row("future-after", 0.51),
        _row("future-before", 0.52),
        _row("future-exact", 0.53),
        _row("future-missing", 0.54),
    ]
    kwargs = _write_fixture(tmp_path, rows=rows)
    kwargs["scheduled_starts"] = [
        {
            "game_id": "future-after",
            "scheduled_start_utc": START_EARLIER,
            "trusted": True,
        },
        {
            "game_id": "future-before",
            "scheduled_start_utc": START_LATER_A,
            "trusted": True,
        },
        {
            "game_id": "future-exact",
            "scheduled_start_utc": START_EXACT,
            "trusted": True,
        },
    ]
    record = capture.register_prospective_capture(**kwargs)

    decisions = {row["game_id"]: row for row in record["row_schedule_decisions"]}
    assert decisions["future-before"]["reason"] == capture.PREGAME_ELIGIBLE
    assert decisions["future-exact"]["reason"] == (
        capture.PREDICTION_NOT_BEFORE_SCHEDULED_START
    )
    assert decisions["future-after"]["reason"] == (
        capture.PREDICTION_NOT_BEFORE_SCHEDULED_START
    )
    assert decisions["future-missing"]["reason"] == capture.MISSING_SCHEDULED_START
    assert record["pregame_eligible_row_count"] == 1
    assert record["non_pregame_or_missing_schedule_row_count"] == 3
    assert record["pregame_certified"] is False


def test_malformed_and_untrusted_schedules_are_not_eligible(tmp_path: Path) -> None:
    kwargs = _write_fixture(tmp_path)
    kwargs["scheduled_starts"] = [
        {
            "game_id": "future-game-a",
            "scheduled_start_utc": "2099-01-01T08:00:00+08:00",
            "trusted": True,
        },
        {
            "game_id": "future-game-b",
            "scheduled_start_utc": START_LATER_B,
            "trusted": False,
        },
    ]
    record = capture.register_prospective_capture(**kwargs)

    assert record["pregame_eligible_row_count"] == 0
    assert record["reason_counts"] == {
        capture.INVALID_SCHEDULED_START: 1,
        capture.UNTRUSTED_SCHEDULE_EVIDENCE: 1,
    }
    assert record["schedule_evidence_status"] == "NO_TRUSTED_CANONICAL_COVERAGE"


def test_conflicting_duplicate_schedule_game_id_fails_closed(tmp_path: Path) -> None:
    kwargs = _write_fixture(tmp_path)
    kwargs["scheduled_starts"] = [
        {
            "game_id": "future-game-a",
            "scheduled_start_utc": START_LATER_A,
            "trusted": True,
        },
        {
            "game_id": "future-game-a",
            "scheduled_start_utc": START_LATER_B,
            "trusted": True,
        },
    ]
    with pytest.raises(capture.CaptureContractError, match="conflicting duplicate"):
        capture.register_prospective_capture(**kwargs)


def test_duplicate_prediction_game_id_fails_closed(tmp_path: Path) -> None:
    kwargs = _write_fixture(
        tmp_path,
        rows=[_row("future-game-a", 0.51), _row("future-game-a", 0.52)],
    )
    kwargs["scheduled_starts"] = []
    with pytest.raises(capture.CaptureContractError, match="duplicate game IDs"):
        capture.register_prospective_capture(**kwargs)


@pytest.mark.parametrize("probability", [-0.01, 1.01, "nan", "inf"])
def test_probability_must_be_finite_and_within_unit_interval(
    tmp_path: Path, probability: object
) -> None:
    kwargs = _write_fixture(tmp_path, rows=[_row("future-game-a", probability)])
    kwargs["scheduled_starts"] = []
    with pytest.raises(capture.CaptureContractError, match="probability"):
        capture.register_prospective_capture(**kwargs)


def test_prediction_and_manifest_tampering_fail_closed(tmp_path: Path) -> None:
    prediction_root = tmp_path / "prediction"
    prediction_kwargs = _write_fixture(prediction_root)
    artifact = prediction_root / "report/future_predictions.csv"
    artifact.write_bytes(artifact.read_bytes() + b"tampered")
    with pytest.raises(capture.CaptureContractError, match="artifact SHA-256 mismatch"):
        capture.register_prospective_capture(**prediction_kwargs)

    manifest_root = tmp_path / "manifest"
    manifest_kwargs = _write_fixture(manifest_root)
    manifest = manifest_root / "report/future_manifest.json"
    manifest.write_bytes(manifest.read_bytes() + b" ")
    with pytest.raises(capture.CaptureContractError, match="manifest SHA-256 mismatch"):
        capture.register_prospective_capture(**manifest_kwargs)


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    [
        ("prediction_artifact_sha256", "0" * 64, "artifact SHA-256 mismatch"),
        ("prediction_manifest_sha256", "0" * 64, "manifest SHA-256 mismatch"),
        ("source_git_commit", "e" * 40, "source_git_commit"),
        ("model_code_config_fingerprint", "e" * 64, "model_code_config"),
        ("final_state_fingerprint", "e" * 64, "final_state"),
        ("prediction_input_fingerprint", "e" * 64, "prediction_input"),
        ("prediction_row_count", 3, "prediction_row_count"),
    ],
)
def test_caller_supplied_provenance_must_exactly_match_manifest(
    tmp_path: Path, field: str, replacement: object, message: str
) -> None:
    kwargs = _write_fixture(tmp_path)
    kwargs[field] = replacement
    with pytest.raises(capture.CaptureContractError, match=message):
        capture.register_prospective_capture(**kwargs)


def test_paths_are_exact_canonical_relative_paths(tmp_path: Path) -> None:
    kwargs = _write_fixture(tmp_path)
    kwargs["prediction_artifact_relative_path"] = "report/../report/future_predictions.csv"
    with pytest.raises(capture.CaptureContractError, match="canonical relative path"):
        capture.register_prospective_capture(**kwargs)


def test_capture_identity_and_payload_ignore_runtime_metadata(tmp_path: Path) -> None:
    first, kwargs = _success_capture(tmp_path)
    kwargs["created_runtime_metadata"] = {
        "created_at_utc": "2099-01-01T00:00:01.123456Z",
        "execution_context": "different-runtime",
    }
    second = capture.register_prospective_capture(**kwargs)

    assert first["capture_id"] == second["capture_id"]
    assert (
        first["deterministic_payload_sha256"]
        == second["deterministic_payload_sha256"]
    )
    assert first["created_runtime_metadata"] != second["created_runtime_metadata"]


def test_capture_identity_excludes_runtime_output_root(tmp_path: Path) -> None:
    first, _ = _success_capture(tmp_path / "first-root")
    second, _ = _success_capture(tmp_path / "second-root")

    assert first["capture_id"] == second["capture_id"]
    assert (
        first["deterministic_payload_sha256"]
        == second["deterministic_payload_sha256"]
    )


def test_current_artifacts_are_not_retroactively_certified_and_reports_reproduce(
    tmp_path: Path,
) -> None:
    synthetic_root = tmp_path / "synthetic"
    record, _ = _success_capture(synthetic_root)
    verification = _synthetic_verification(record)
    before = {
        path: capture._sha256_file(path)
        for path in (
            capture.DEFAULT_PREDICTION_ARTIFACT_PATH,
            capture.DEFAULT_PREDICTION_MANIFEST_PATH,
            capture.DEFAULT_PREDICTION_SUMMARY_PATH,
            capture.DEFAULT_DIVERGENCE_LEDGER_PATH,
            capture.DEFAULT_DIVERGENCE_SUMMARY_JSON_PATH,
            capture.DEFAULT_DIVERGENCE_SUMMARY_MD_PATH,
        )
    }
    first = capture.build_current_readiness(
        synthetic_contract_verification=verification,
        generated_at_utc="2026-07-14T14:00:00Z",
        generator_source_git_commit="92f7d34bea46dbe7548016aabace04930e091ff0",
    )
    second = capture.build_current_readiness(
        synthetic_contract_verification=verification,
        generated_at_utc="2026-07-14T14:00:01Z",
        generator_source_git_commit="92f7d34bea46dbe7548016aabace04930e091ff0",
    )
    first_paths = capture.write_readiness_reports(first, tmp_path / "first/report")
    second_paths = capture.write_readiness_reports(second, tmp_path / "second/report")

    assert first["status"] == "NO_RETROACTIVE_PROSPECTIVE_CAPTURE"
    assert first["current_coverage"] == {
        "retrospective_prediction_row_count": 828,
        "prospective_registered_row_count": 0,
        "explicit_prediction_as_of_row_count": 0,
        "scheduled_start_row_count": 0,
        "pregame_eligible_row_count": 0,
        "future_prospective_cohort_row_count": 0,
    }
    assert first["claims"]["historical_prospective_cohort_created"] is False
    assert first["claims"]["current_artifacts_pregame_certified"] is False
    assert first["synthetic_contract_verification"]["status"] == "PASSED"
    assert first["deterministic_payload_sha256"] == second["deterministic_payload_sha256"]
    assert _normalized_readiness(first) == _normalized_readiness(second)
    assert _normalized_markdown(
        first_paths["markdown"].read_text(encoding="utf-8")
    ) == _normalized_markdown(
        second_paths["markdown"].read_text(encoding="utf-8")
    )
    assert {
        path: capture._sha256_file(path) for path in before
    } == before


def test_readiness_validator_rejects_prospective_claim_for_current_artifacts(
    tmp_path: Path,
) -> None:
    record, _ = _success_capture(tmp_path / "synthetic")
    payload = capture.build_current_readiness(
        synthetic_contract_verification=_synthetic_verification(record),
        generated_at_utc="2026-07-14T14:00:00Z",
        generator_source_git_commit="92f7d34bea46dbe7548016aabace04930e091ff0",
    )
    payload["current_coverage"]["pregame_eligible_row_count"] = 1
    payload["deterministic_payload_sha256"] = capture._readiness_payload_hash(payload)

    with pytest.raises(capture.CaptureContractError, match="prospective/pregame"):
        capture.validate_readiness_payload(payload)


def test_committed_readiness_report_has_zero_current_prospective_rows() -> None:
    path = capture.REPO_ROOT / "report" / capture.READINESS_JSON_FILENAME
    payload = json.loads(path.read_text(encoding="utf-8"))

    capture.validate_readiness_payload(payload)
    assert payload["status"] == "NO_RETROACTIVE_PROSPECTIVE_CAPTURE"
    assert payload["current_coverage"] == {
        "retrospective_prediction_row_count": 828,
        "prospective_registered_row_count": 0,
        "explicit_prediction_as_of_row_count": 0,
        "scheduled_start_row_count": 0,
        "pregame_eligible_row_count": 0,
        "future_prospective_cohort_row_count": 0,
    }
    assert payload["synthetic_contract_verification"]["status"] == "PASSED"
    assert payload["claims"] == {
        "historical_prospective_cohort_created": False,
        "current_artifacts_pregame_certified": False,
        "model_performance_claim": False,
        "betting_claim": False,
        "model_activated": False,
        "deployed": False,
        "registry_mutated": False,
        "published": False,
    }


def test_capture_registration_has_no_persistent_side_effect(tmp_path: Path) -> None:
    record, _ = _success_capture(tmp_path)
    files = sorted(
        str(path.relative_to(tmp_path)) for path in tmp_path.rglob("*") if path.is_file()
    )

    assert files == ["report/future_manifest.json", "report/future_predictions.csv"]
    assert record["created_runtime_metadata"]["execution_context"] == (
        "pytest-temporary-root"
    )
