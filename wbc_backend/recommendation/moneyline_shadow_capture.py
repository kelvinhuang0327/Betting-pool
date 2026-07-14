"""P280-A explicit-as-of prospective Moneyline shadow capture contract.

The capture boundary is deliberately local and paper-only.  It accepts a
prediction observation only when the caller supplies an explicit canonical UTC
prediction as-of plus exact artifact/provenance hashes.  Schedule evidence can
upgrade an observation to pregame-certified only when every row has trusted,
canonical evidence strictly later than the prediction as-of.

This module never infers time from a game date, file metadata, generation
metadata, or wall time.  It does not fetch data, read outcomes/odds, write a
database, activate a model, or publish a capture.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from copy import deepcopy
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

from scripts import _p274_prospective_result_availability_index as p274
from wbc_backend.recommendation import moneyline_shadow_divergence as divergence
from wbc_backend.recommendation import moneyline_shadow_prediction as shadow_prediction


CAPTURE_SCHEMA_VERSION = "p280a.moneyline_shadow_capture.v1"
READINESS_SCHEMA_VERSION = "p280a.moneyline_shadow_capture_readiness.v1"
CAPTURE_SEMANTICS = "LOCAL_OBSERVATION_LOWER_BOUND"
CURRENT_READINESS_STATUS = "NO_RETROACTIVE_PROSPECTIVE_CAPTURE"
PAPER_SCOPE = "PAPER_ONLY_DIAGNOSTIC_PROSPECTIVE_CAPTURE_CONTRACT"

PREGAME_ELIGIBLE = "PREGAME_ELIGIBLE"
MISSING_SCHEDULED_START = "MISSING_SCHEDULED_START"
INVALID_SCHEDULED_START = "INVALID_SCHEDULED_START"
UNTRUSTED_SCHEDULE_EVIDENCE = "UNTRUSTED_SCHEDULE_EVIDENCE"
PREDICTION_NOT_BEFORE_SCHEDULED_START = (
    "PREDICTION_NOT_BEFORE_SCHEDULED_START"
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PREDICTION_ARTIFACT_PATH = (
    REPO_ROOT / "report/mlb_2026_corrected_moneyline_shadow_predictions.csv"
)
DEFAULT_PREDICTION_MANIFEST_PATH = (
    REPO_ROOT / "report/mlb_2026_corrected_moneyline_shadow_manifest.json"
)
DEFAULT_PREDICTION_SUMMARY_PATH = (
    REPO_ROOT / "report/mlb_2026_corrected_moneyline_shadow_summary.md"
)
DEFAULT_DIVERGENCE_LEDGER_PATH = (
    REPO_ROOT / "report/mlb_2026_moneyline_shadow_divergence.csv"
)
DEFAULT_DIVERGENCE_SUMMARY_JSON_PATH = (
    REPO_ROOT / "report/mlb_2026_moneyline_shadow_divergence_summary.json"
)
DEFAULT_DIVERGENCE_SUMMARY_MD_PATH = (
    REPO_ROOT / "report/mlb_2026_moneyline_shadow_divergence_summary.md"
)
READINESS_JSON_FILENAME = "mlb_moneyline_shadow_prospective_capture_readiness.json"
READINESS_MD_FILENAME = "mlb_moneyline_shadow_prospective_capture_readiness.md"

_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_GIT_COMMIT_RE = re.compile(r"[0-9a-f]{40}")
_PREDICTION_FIELDS = {
    "game_id",
    "game_date",
    "away_team",
    "home_team",
    "shadow_home_win_probability",
    "predicted_side",
    "model_id",
    "model_version",
}


class CaptureContractError(ValueError):
    """Fail-closed validation error for the P280-A capture boundary."""


def _canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    """Reuse the P278 protected-artifact byte-hash helper."""
    return shadow_prediction._sha256_file(Path(path))


def _require_sha256(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise CaptureContractError(f"{field_name} must be a lowercase SHA-256")
    return value


def _require_git_commit(value: Any, field_name: str = "source_git_commit") -> str:
    if not isinstance(value, str) or _GIT_COMMIT_RE.fullmatch(value) is None:
        raise CaptureContractError(f"{field_name} must be a full lowercase Git commit")
    return value


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CaptureContractError(f"{field_name} must be explicit non-empty text")
    if value != value.strip():
        raise CaptureContractError(f"{field_name} must not contain outer whitespace")
    return value


def _canonical_utc(value: Any, field_name: str) -> tuple[str, Any]:
    """Reuse P274 strict canonical UTC parsing and normalize its error type."""
    try:
        return p274.parse_canonical_utc(value, field_name)
    except p274.P274Error as exc:
        raise CaptureContractError(str(exc)) from exc


def _strict_json_object(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CaptureContractError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    try:
        payload = json.loads(
            Path(path).read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicates,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CaptureContractError(f"invalid JSON manifest: {path}") from exc
    if not isinstance(payload, dict):
        raise CaptureContractError(f"JSON manifest must be an object: {path}")
    return payload


def _resolve_exact_relative_path(
    root: Path, relative_path: Any, field_name: str
) -> tuple[str, Path]:
    root = Path(root).resolve()
    value = _require_text(relative_path, field_name)
    if "\\" in value:
        raise CaptureContractError(f"{field_name} must use POSIX separators")
    pure = PurePosixPath(value)
    if pure.is_absolute() or value != pure.as_posix() or ".." in pure.parts:
        raise CaptureContractError(f"{field_name} must be a canonical relative path")
    resolved = root.joinpath(*pure.parts).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise CaptureContractError(f"{field_name} escapes capture root") from exc
    if not resolved.is_file():
        raise CaptureContractError(f"{field_name} does not exist: {value}")
    return value, resolved


def _load_prediction_rows(
    path: Path,
    *,
    expected_model_id: str,
    expected_model_version: str,
) -> tuple[dict[str, divergence.NormalizedPrediction], str]:
    """Load P278-shaped rows using P279 validation/fingerprint helpers."""
    normalized: list[divergence.NormalizedPrediction] = []
    ordered_game_ids: list[str] = []
    try:
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise CaptureContractError("prediction CSV is missing a header")
            missing = sorted(_PREDICTION_FIELDS - set(reader.fieldnames))
            if missing:
                raise CaptureContractError(
                    f"prediction CSV missing required columns: {missing}"
                )
            for raw in reader:
                game_id = divergence._require_text(raw, "game_id", source="capture")
                probability = divergence._probability(
                    raw.get("shadow_home_win_probability"),
                    field="capture shadow_home_win_probability",
                    game_id=game_id,
                )
                model_id = divergence._require_text(
                    raw, "model_id", source="capture"
                )
                model_version = divergence._require_text(
                    raw, "model_version", source="capture"
                )
                if model_id != expected_model_id:
                    raise CaptureContractError(
                        f"prediction model_id mismatch for {game_id}"
                    )
                if model_version != expected_model_version:
                    raise CaptureContractError(
                        f"prediction model_version mismatch for {game_id}"
                    )
                normalized.append(
                    divergence.NormalizedPrediction(
                        game_id=game_id,
                        game_date=divergence._require_text(
                            raw, "game_date", source="capture"
                        ),
                        away_team=divergence._require_text(
                            raw, "away_team", source="capture"
                        ),
                        home_team=divergence._require_text(
                            raw, "home_team", source="capture"
                        ),
                        model_id=model_id,
                        model_version=model_version,
                        home_win_probability=probability,
                        predicted_side=divergence._side(
                            raw.get("predicted_side"),
                            probability=probability,
                            game_id=game_id,
                            source="capture",
                        ),
                    )
                )
                ordered_game_ids.append(game_id)
    except CaptureContractError:
        raise
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        raise CaptureContractError(str(exc)) from exc

    if not normalized:
        raise CaptureContractError("prediction CSV has no rows")
    try:
        indexed = divergence._index_unique(normalized, source="capture")
    except ValueError as exc:
        raise CaptureContractError(str(exc)) from exc
    if ordered_game_ids != sorted(ordered_game_ids):
        raise CaptureContractError(
            "prediction rows must use deterministic ascending game_id ordering"
        )
    return indexed, divergence._semantic_fingerprint(indexed)


def _manifest_provenance(
    manifest: Mapping[str, Any],
    *,
    artifact_relative_path: str,
    manifest_relative_path: str,
    artifact_sha256: str,
    expected_source_git_commit: str,
    expected_model_id: str,
    expected_model_version: str,
    expected_model_code_config_fingerprint: str,
    expected_final_state_fingerprint: str,
    expected_prediction_input_fingerprint: str,
    expected_prediction_row_count: int,
) -> dict[str, Any]:
    artifacts = manifest.get("artifacts")
    model = manifest.get("model")
    training = manifest.get("training")
    prediction_input = manifest.get("prediction_input")
    if not all(isinstance(value, dict) for value in (artifacts, model, training, prediction_input)):
        raise CaptureContractError("prediction manifest provenance sections are missing")
    if manifest.get("source_git_commit") != expected_source_git_commit:
        raise CaptureContractError("source_git_commit does not match prediction manifest")
    if manifest.get("artifact_version") != expected_model_version:
        raise CaptureContractError("artifact_version does not match model_version")
    checks = {
        "prediction artifact path": (
            artifacts.get("predictions_csv"),
            artifact_relative_path,
        ),
        "prediction manifest path": (
            artifacts.get("manifest_json"),
            manifest_relative_path,
        ),
        "prediction artifact SHA-256": (
            artifacts.get("predictions_csv_sha256"),
            artifact_sha256,
        ),
        "model_id": (model.get("model_id"), expected_model_id),
        "model_version": (model.get("model_version"), expected_model_version),
        "model_code_config_fingerprint": (
            model.get("model_code_config_fingerprint"),
            expected_model_code_config_fingerprint,
        ),
        "final_state_fingerprint": (
            training.get("final_state_fingerprint"),
            expected_final_state_fingerprint,
        ),
        "prediction_input_fingerprint": (
            prediction_input.get("prediction_input_fingerprint"),
            expected_prediction_input_fingerprint,
        ),
        "prediction_row_count": (
            artifacts.get("prediction_row_count"),
            expected_prediction_row_count,
        ),
    }
    for label, (actual, expected) in checks.items():
        if actual != expected:
            raise CaptureContractError(f"{label} does not match prediction manifest")
    return {
        "model_id": expected_model_id,
        "model_version": expected_model_version,
        "model_code_config_fingerprint": expected_model_code_config_fingerprint,
        "final_state_fingerprint": expected_final_state_fingerprint,
        "prediction_input_fingerprint": expected_prediction_input_fingerprint,
        "prediction_row_count": expected_prediction_row_count,
    }


def _schedule_index(
    scheduled_starts: Iterable[Mapping[str, Any]],
    *,
    prediction_game_ids: set[str],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for position, raw in enumerate(scheduled_starts, start=1):
        if not isinstance(raw, Mapping):
            raise CaptureContractError(
                f"schedule evidence row {position} must be an object"
            )
        game_id = _require_text(raw.get("game_id"), f"schedule row {position} game_id")
        current = {
            "game_id": game_id,
            "scheduled_start_utc": raw.get("scheduled_start_utc"),
            "trusted": raw.get("trusted") is True,
        }
        if game_id in indexed:
            if indexed[game_id] != current:
                raise CaptureContractError(
                    f"conflicting duplicate schedule game_id: {game_id}"
                )
            raise CaptureContractError(f"duplicate schedule game_id: {game_id}")
        indexed[game_id] = current
    extras = sorted(set(indexed) - prediction_game_ids)
    if extras:
        raise CaptureContractError(f"schedule evidence has unknown game IDs: {extras}")
    return indexed


def _schedule_decisions(
    *,
    game_ids: Sequence[str],
    prediction_as_of: Any,
    scheduled_starts: Iterable[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, int], str]:
    indexed = _schedule_index(
        scheduled_starts,
        prediction_game_ids=set(game_ids),
    )
    decisions: list[dict[str, Any]] = []
    reasons: Counter[str] = Counter()
    trusted_canonical_count = 0
    for game_id in game_ids:
        evidence = indexed.get(game_id)
        raw_start = None if evidence is None else evidence["scheduled_start_utc"]
        trusted = False if evidence is None else evidence["trusted"]
        canonical_start: str | None = None
        if evidence is None or raw_start is None or raw_start == "":
            reason = MISSING_SCHEDULED_START
        elif not trusted:
            reason = UNTRUSTED_SCHEDULE_EVIDENCE
        else:
            try:
                canonical_start, start_dt = _canonical_utc(
                    raw_start, f"scheduled_start_utc[{game_id}]"
                )
            except CaptureContractError:
                reason = INVALID_SCHEDULED_START
            else:
                trusted_canonical_count += 1
                reason = (
                    PREGAME_ELIGIBLE
                    if prediction_as_of < start_dt
                    else PREDICTION_NOT_BEFORE_SCHEDULED_START
                )
        reasons[reason] += 1
        decisions.append(
            {
                "game_id": game_id,
                "scheduled_start_utc": canonical_start,
                "trusted_schedule_evidence": trusted,
                "pregame_eligible": reason == PREGAME_ELIGIBLE,
                "reason": reason,
            }
        )
    if trusted_canonical_count == len(game_ids):
        evidence_status = "FULL_TRUSTED_CANONICAL_COVERAGE"
    elif trusted_canonical_count == 0:
        evidence_status = "NO_TRUSTED_CANONICAL_COVERAGE"
    else:
        evidence_status = "PARTIAL_TRUSTED_CANONICAL_COVERAGE"
    return decisions, dict(sorted(reasons.items())), evidence_status


def deterministic_payload_hash(payload: Mapping[str, Any]) -> str:
    deterministic = deepcopy(dict(payload))
    deterministic.pop("created_runtime_metadata", None)
    deterministic.pop("deterministic_payload_sha256", None)
    return _sha256_bytes(_canonical_json_bytes(deterministic))


def register_prospective_capture(
    *,
    root: Path,
    prediction_artifact_relative_path: str,
    prediction_artifact_sha256: str,
    prediction_manifest_relative_path: str,
    prediction_manifest_sha256: str,
    source_git_commit: str,
    model_id: str,
    model_version: str,
    model_code_config_fingerprint: str,
    final_state_fingerprint: str,
    prediction_input_fingerprint: str,
    prediction_row_count: int,
    prediction_as_of_utc: str,
    scheduled_starts: Iterable[Mapping[str, Any]],
    created_runtime_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and return a deterministic local observation capture record.

    The returned record is not persisted.  A caller must explicitly supply the
    prediction as-of; there is no default and no inference path.
    """
    artifact_relative, artifact_path = _resolve_exact_relative_path(
        root, prediction_artifact_relative_path, "prediction_artifact_relative_path"
    )
    manifest_relative, manifest_path = _resolve_exact_relative_path(
        root, prediction_manifest_relative_path, "prediction_manifest_relative_path"
    )
    expected_artifact_sha256 = _require_sha256(
        prediction_artifact_sha256, "prediction_artifact_sha256"
    )
    expected_manifest_sha256 = _require_sha256(
        prediction_manifest_sha256, "prediction_manifest_sha256"
    )
    if _sha256_file(artifact_path) != expected_artifact_sha256:
        raise CaptureContractError("prediction artifact SHA-256 mismatch")
    if _sha256_file(manifest_path) != expected_manifest_sha256:
        raise CaptureContractError("prediction manifest SHA-256 mismatch")

    source_commit = _require_git_commit(source_git_commit)
    expected_model_id = _require_text(model_id, "model_id")
    expected_model_version = _require_text(model_version, "model_version")
    model_fingerprint = _require_sha256(
        model_code_config_fingerprint, "model_code_config_fingerprint"
    )
    state_fingerprint = _require_sha256(
        final_state_fingerprint, "final_state_fingerprint"
    )
    input_fingerprint = _require_sha256(
        prediction_input_fingerprint, "prediction_input_fingerprint"
    )
    if (
        isinstance(prediction_row_count, bool)
        or not isinstance(prediction_row_count, int)
        or prediction_row_count <= 0
    ):
        raise CaptureContractError("prediction_row_count must be a positive integer")
    canonical_as_of, as_of_dt = _canonical_utc(
        prediction_as_of_utc, "prediction_as_of_utc"
    )

    if not isinstance(created_runtime_metadata, Mapping):
        raise CaptureContractError("created_runtime_metadata must be an object")
    runtime_metadata = deepcopy(dict(created_runtime_metadata))
    _canonical_utc(runtime_metadata.get("created_at_utc"), "created_at_utc")

    manifest = _strict_json_object(manifest_path)
    provenance = _manifest_provenance(
        manifest,
        artifact_relative_path=artifact_relative,
        manifest_relative_path=manifest_relative,
        artifact_sha256=expected_artifact_sha256,
        expected_source_git_commit=source_commit,
        expected_model_id=expected_model_id,
        expected_model_version=expected_model_version,
        expected_model_code_config_fingerprint=model_fingerprint,
        expected_final_state_fingerprint=state_fingerprint,
        expected_prediction_input_fingerprint=input_fingerprint,
        expected_prediction_row_count=prediction_row_count,
    )
    rows, row_fingerprint = _load_prediction_rows(
        artifact_path,
        expected_model_id=expected_model_id,
        expected_model_version=expected_model_version,
    )
    if len(rows) != prediction_row_count:
        raise CaptureContractError("prediction row count does not match artifact")
    game_ids = sorted(rows)
    decisions, reason_counts, schedule_status = _schedule_decisions(
        game_ids=game_ids,
        prediction_as_of=as_of_dt,
        scheduled_starts=scheduled_starts,
    )
    schedule_evidence_sha256 = _sha256_bytes(_canonical_json_bytes(decisions))
    eligible_count = reason_counts.get(PREGAME_ELIGIBLE, 0)

    identity_material = {
        "capture_schema_version": CAPTURE_SCHEMA_VERSION,
        "capture_semantics": CAPTURE_SEMANTICS,
        "source_git_commit": source_commit,
        "prediction_artifact_sha256": expected_artifact_sha256,
        "prediction_manifest_sha256": expected_manifest_sha256,
        "prediction_as_of_utc": canonical_as_of,
        "model_id": expected_model_id,
        "model_version": expected_model_version,
        "model_code_config_fingerprint": model_fingerprint,
        "final_state_fingerprint": state_fingerprint,
        "prediction_input_fingerprint": input_fingerprint,
        "prediction_row_count": prediction_row_count,
        "prediction_rows_fingerprint": row_fingerprint,
        "schedule_evidence_sha256": schedule_evidence_sha256,
        "row_identities": game_ids,
        "retroactive_certification": False,
    }
    capture_id = f"p280a-{_sha256_bytes(_canonical_json_bytes(identity_material))}"
    record: dict[str, Any] = {
        "capture_schema_version": CAPTURE_SCHEMA_VERSION,
        "capture_id": capture_id,
        "scope": PAPER_SCOPE,
        "paper_only": True,
        "diagnostic_only": True,
        "production_ready": False,
        "prediction_artifact_relative_path": artifact_relative,
        "prediction_artifact_sha256": expected_artifact_sha256,
        "prediction_manifest_relative_path": manifest_relative,
        "prediction_manifest_sha256": expected_manifest_sha256,
        "source_git_commit": source_commit,
        **provenance,
        "prediction_rows_fingerprint": row_fingerprint,
        "prediction_as_of_utc": canonical_as_of,
        "capture_semantics": CAPTURE_SEMANTICS,
        "retroactive_certification": False,
        "schedule_evidence_status": schedule_status,
        "schedule_evidence_sha256": schedule_evidence_sha256,
        "pregame_certified": eligible_count == prediction_row_count,
        "pregame_eligible_row_count": eligible_count,
        "non_pregame_or_missing_schedule_row_count": (
            prediction_row_count - eligible_count
        ),
        "reason_counts": reason_counts,
        "row_schedule_decisions": decisions,
        "created_runtime_metadata": runtime_metadata,
    }
    record["deterministic_payload_sha256"] = deterministic_payload_hash(record)
    return record


def _readiness_payload_hash(payload: Mapping[str, Any]) -> str:
    deterministic = deepcopy(dict(payload))
    deterministic.pop("runtime_metadata", None)
    deterministic.pop("deterministic_payload_sha256", None)
    return _sha256_bytes(_canonical_json_bytes(deterministic))


def validate_readiness_payload(payload: Mapping[str, Any]) -> None:
    if payload.get("readiness_schema_version") != READINESS_SCHEMA_VERSION:
        raise CaptureContractError("unexpected P280 readiness schema version")
    if payload.get("status") != CURRENT_READINESS_STATUS:
        raise CaptureContractError("current artifacts were not kept retrospective")
    coverage = payload.get("current_coverage")
    if not isinstance(coverage, Mapping):
        raise CaptureContractError("P280 readiness coverage is missing")
    zero_fields = (
        "prospective_registered_row_count",
        "explicit_prediction_as_of_row_count",
        "scheduled_start_row_count",
        "pregame_eligible_row_count",
        "future_prospective_cohort_row_count",
    )
    if any(coverage.get(field) != 0 for field in zero_fields):
        raise CaptureContractError("current artifacts claim prospective/pregame coverage")
    claims = payload.get("claims")
    required_false = (
        "historical_prospective_cohort_created",
        "current_artifacts_pregame_certified",
        "model_performance_claim",
        "betting_claim",
        "model_activated",
        "deployed",
        "registry_mutated",
        "published",
    )
    if not isinstance(claims, Mapping) or any(
        claims.get(field) is not False for field in required_false
    ):
        raise CaptureContractError("P280 readiness contains a forbidden claim")
    recorded = _require_sha256(
        payload.get("deterministic_payload_sha256"),
        "deterministic_payload_sha256",
    )
    if recorded != _readiness_payload_hash(payload):
        raise CaptureContractError("P280 readiness deterministic hash mismatch")


def build_current_readiness(
    *,
    synthetic_contract_verification: Mapping[str, Any],
    generated_at_utc: str,
    generator_source_git_commit: str,
    prediction_artifact_path: Path = DEFAULT_PREDICTION_ARTIFACT_PATH,
    prediction_manifest_path: Path = DEFAULT_PREDICTION_MANIFEST_PATH,
    prediction_summary_path: Path = DEFAULT_PREDICTION_SUMMARY_PATH,
    divergence_ledger_path: Path = DEFAULT_DIVERGENCE_LEDGER_PATH,
    divergence_summary_json_path: Path = DEFAULT_DIVERGENCE_SUMMARY_JSON_PATH,
    divergence_summary_md_path: Path = DEFAULT_DIVERGENCE_SUMMARY_MD_PATH,
) -> dict[str, Any]:
    """Build a truthful current-artifact readiness result without registration."""
    generated_at, _ = _canonical_utc(generated_at_utc, "generated_at_utc")
    generator_commit = _require_git_commit(
        generator_source_git_commit, "generator_source_git_commit"
    )
    paths = [
        Path(prediction_artifact_path),
        Path(prediction_manifest_path),
        Path(prediction_summary_path),
        Path(divergence_ledger_path),
        Path(divergence_summary_json_path),
        Path(divergence_summary_md_path),
    ]
    if any(not path.is_file() for path in paths):
        raise CaptureContractError("required P278/P279 readiness artifact is missing")

    prediction_manifest = _strict_json_object(Path(prediction_manifest_path))
    artifacts = prediction_manifest.get("artifacts", {})
    prediction_hash = _sha256_file(Path(prediction_artifact_path))
    if artifacts.get("predictions_csv_sha256") != prediction_hash:
        raise CaptureContractError("current P278 prediction hash mismatch")
    with Path(prediction_artifact_path).open(newline="", encoding="utf-8") as handle:
        prediction_rows = list(csv.DictReader(handle))
    if len(prediction_rows) != artifacts.get("prediction_row_count"):
        raise CaptureContractError("current P278 prediction row-count mismatch")
    explicit_as_of_rows = sum(
        1 for row in prediction_rows if str(row.get("feature_as_of_utc") or "").strip()
    )
    scheduled_start_rows = sum(
        1 for row in prediction_rows if str(row.get("scheduled_start_utc") or "").strip()
    )
    if explicit_as_of_rows or scheduled_start_rows:
        raise CaptureContractError(
            "current P278 artifact unexpectedly contains prospective time evidence"
        )

    divergence_summary = _strict_json_object(Path(divergence_summary_json_path))
    divergence_outputs = divergence_summary.get("output_artifacts", {})
    if divergence_outputs.get("ledger_csv_sha256") != _sha256_file(
        Path(divergence_ledger_path)
    ):
        raise CaptureContractError("current P279 ledger hash mismatch")
    recorded_divergence_hash = divergence_outputs.get(
        "summary_deterministic_payload_sha256"
    )
    if recorded_divergence_hash != divergence.deterministic_summary_fingerprint(
        divergence_summary
    ):
        raise CaptureContractError("current P279 deterministic hash mismatch")

    synthetic = deepcopy(dict(synthetic_contract_verification))
    if synthetic.get("status") != "PASSED":
        raise CaptureContractError("synthetic prospective contract has not passed")
    _require_sha256(synthetic.get("deterministic_payload_sha256"), "synthetic hash")
    capture_id = synthetic.get("capture_id")
    if not isinstance(capture_id, str) or not capture_id.startswith("p280a-"):
        raise CaptureContractError("synthetic capture ID is missing")

    payload: dict[str, Any] = {
        "task": "P280-A explicit-as-of prospective shadow capture contract",
        "readiness_schema_version": READINESS_SCHEMA_VERSION,
        "status": CURRENT_READINESS_STATUS,
        "scope": PAPER_SCOPE,
        "paper_only": True,
        "diagnostic_only": True,
        "current_artifacts": {
            "p278_corrected_shadow": {
                "classification": "RETROSPECTIVE_FROZEN_STATE_PAPER_ONLY",
                "prediction_artifact_path": str(
                    Path(prediction_artifact_path).resolve().relative_to(REPO_ROOT)
                ),
                "prediction_artifact_sha256": prediction_hash,
                "prediction_manifest_path": str(
                    Path(prediction_manifest_path).resolve().relative_to(REPO_ROOT)
                ),
                "prediction_manifest_sha256": _sha256_file(
                    Path(prediction_manifest_path)
                ),
                "prediction_summary_path": str(
                    Path(prediction_summary_path).resolve().relative_to(REPO_ROOT)
                ),
                "prediction_summary_sha256": _sha256_file(
                    Path(prediction_summary_path)
                ),
                "prediction_row_count": len(prediction_rows),
                "retroactively_registered": False,
                "pregame_certified": False,
            },
            "p279_divergence": {
                "classification": "OUTCOME_FREE_DIVERGENCE_NOT_PERFORMANCE",
                "ledger_path": str(
                    Path(divergence_ledger_path).resolve().relative_to(REPO_ROOT)
                ),
                "ledger_sha256": _sha256_file(Path(divergence_ledger_path)),
                "summary_json_path": str(
                    Path(divergence_summary_json_path).resolve().relative_to(REPO_ROOT)
                ),
                "summary_json_sha256": _sha256_file(
                    Path(divergence_summary_json_path)
                ),
                "summary_markdown_path": str(
                    Path(divergence_summary_md_path).resolve().relative_to(REPO_ROOT)
                ),
                "summary_markdown_sha256": _sha256_file(
                    Path(divergence_summary_md_path)
                ),
                "prospective_capture_evidence": False,
            },
        },
        "current_coverage": {
            "retrospective_prediction_row_count": len(prediction_rows),
            "prospective_registered_row_count": 0,
            "explicit_prediction_as_of_row_count": 0,
            "scheduled_start_row_count": 0,
            "pregame_eligible_row_count": 0,
            "future_prospective_cohort_row_count": 0,
        },
        "future_capture_contract": {
            "runner_available": True,
            "runner_entrypoint": (
                "wbc_backend.recommendation.moneyline_shadow_capture."
                "register_prospective_capture"
            ),
            "capture_schema_version": CAPTURE_SCHEMA_VERSION,
            "capture_semantics": CAPTURE_SEMANTICS,
            "prediction_as_of_must_be_explicit_canonical_utc": True,
            "scheduled_start_must_be_explicit_trusted_canonical_utc": True,
            "pregame_boundary": "prediction_as_of_utc < scheduled_start_utc",
            "runtime_metadata_excluded_from_deterministic_payload_hash": True,
            "retroactive_certification": False,
        },
        "synthetic_contract_verification": synthetic,
        "claims": {
            "historical_prospective_cohort_created": False,
            "current_artifacts_pregame_certified": False,
            "model_performance_claim": False,
            "betting_claim": False,
            "model_activated": False,
            "deployed": False,
            "registry_mutated": False,
            "published": False,
        },
        "limitations": [
            "Current P278/P279 artifacts have no trustworthy row-level prediction as-of.",
            "Current P278/P279 artifacts have no trusted row-level scheduled-start evidence.",
            "Only captures created prospectively through the explicit boundary can "
            "form a future cohort.",
            "This readiness result makes no model-performance or betting claim.",
        ],
        "runtime_metadata": {
            "generated_at_utc": generated_at,
            "generator_source_git_commit": generator_commit,
            "excluded_from_deterministic_payload_hash": True,
        },
    }
    payload["deterministic_payload_sha256"] = _readiness_payload_hash(payload)
    validate_readiness_payload(payload)
    return payload


def render_readiness_markdown(payload: Mapping[str, Any]) -> str:
    validate_readiness_payload(payload)
    coverage = payload["current_coverage"]
    future = payload["future_capture_contract"]
    synthetic = payload["synthetic_contract_verification"]
    runtime = payload["runtime_metadata"]
    lines = [
        "# MLB Moneyline Shadow Prospective Capture Readiness",
        "",
        f"**Status:** `{payload['status']}`",
        "",
        "**Scope:** paper-only, diagnostic-only contract readiness. No model "
        "performance or betting claim.",
        "",
        "## Current Artifact Truthfulness",
        "",
        "- P278 remains a retrospective frozen-state paper-only prediction artifact.",
        "- P279 remains an outcome-free divergence baseline, not performance evidence.",
        "- No historical prospective cohort was created and no current artifact was "
        "retroactively certified.",
        "- Current retrospective prediction rows: "
        f"`{coverage['retrospective_prediction_row_count']}`",
        f"- Prospective registered rows: `{coverage['prospective_registered_row_count']}`",
        f"- Explicit prediction-as-of rows: `{coverage['explicit_prediction_as_of_row_count']}`",
        f"- Trusted scheduled-start rows: `{coverage['scheduled_start_row_count']}`",
        f"- Pregame-eligible rows: `{coverage['pregame_eligible_row_count']}`",
        "",
        "## Future Prospective Contract",
        "",
        f"- Runner available: `{future['runner_available']}`",
        f"- Capture semantics: `{future['capture_semantics']}`",
        f"- Pregame boundary: `{future['pregame_boundary']}`",
        "- Missing, malformed, inferred, untrusted, equal, or later schedule "
        "evidence fails closed.",
        "- Runtime metadata is excluded from deterministic capture hashes.",
        "",
        "## Synthetic Verification",
        "",
        f"- Status: `{synthetic['status']}`",
        f"- Capture ID: `{synthetic['capture_id']}`",
        f"- Deterministic payload SHA-256: `{synthetic['deterministic_payload_sha256']}`",
        f"- Fixture storage: `{synthetic['fixture_storage']}`",
        "- Canonical future fixture, boundary checks, duplicate conflict, and tamper "
        "checks passed.",
        "",
        "## Safety",
        "",
        "- Model activation: `false`",
        "- Deployment: `false`",
        "- Registry mutation: `false`",
        "- Publication: `false`",
        "- Real betting: `false`",
        f"- Readiness deterministic payload SHA-256: `{payload['deterministic_payload_sha256']}`",
        "",
        "## Runtime Metadata (Excluded From Deterministic Hash)",
        "",
        f"- Generated at: `{runtime['generated_at_utc']}`",
        f"- Generator source Git commit: `{runtime['generator_source_git_commit']}`",
        "",
    ]
    return "\n".join(lines)


def write_readiness_reports(payload: Mapping[str, Any], out_dir: Path) -> dict[str, Path]:
    validate_readiness_payload(payload)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / READINESS_JSON_FILENAME
    markdown_path = out_dir / READINESS_MD_FILENAME
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    markdown_path.write_text(render_readiness_markdown(payload), encoding="utf-8")
    return {"json": json_path, "markdown": markdown_path}
