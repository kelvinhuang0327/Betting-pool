"""Manual one-shot recorder for prospective official MLB result availability.

The recorder has exactly two modes:

* capture performs one unauthenticated request for one explicit numeric gamePk and
  records the UTC time immediately after the complete response has been received.
* offline-verify reads saved response bytes and permits a fixed observation time for
  deterministic offline verification.

A current observation establishes availability no earlier than its own observation
timestamp.  It does not claim globally earliest official availability.  File mtimes,
feed-generated metadata, retries, polling, season fetches, and caller-controlled
timestamps in capture mode are deliberately excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


OBSERVATION_CONTRACT_VERSION = "p272-prospective-result-availability.v1"
SOURCE_INDEX_CONTRACT_VERSION = "p272-prospective-source-index.v1"
SOURCE_NAME = "MLB_STATSAPI_GAME_FEED_LIVE"
SOURCE_ENDPOINT_ID = "GET statsapi.mlb.com/api/v1.1/game/{gamePk}/feed/live"
OFFICIAL_HOST = "statsapi.mlb.com"
OFFICIAL_ENDPOINT_TEMPLATE = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
REQUEST_TIMEOUT_SECONDS = 20
USER_AGENT = "Betting-pool-P272-prospective-result-recorder/1.0"
OBSERVATION_FILENAME = "observation.json"
SOURCE_INDEX_FILENAME = "source_index.json"
CHECKSUM_FILENAME = "SHA256SUMS"

ALLOWED_STATUSES = frozenset(
    {
        "SCHEDULED",
        "IN_PROGRESS",
        "SUSPENDED",
        "FINAL",
        "POSTPONED",
        "CANCELLED",
        "FORFEIT",
    }
)
RESOLVED_STATUSES = frozenset({"FINAL", "FORFEIT"})
ALLOWED_PROVENANCE_STATUSES = frozenset({"COMPLETE", "INCOMPLETE"})

# This is the complete identity-alias allowlist.  The official response spelling is
# always retained in evidence; aliases are used only when validating identity.
TEAM_IDENTITY_ALIAS_GROUPS: Mapping[str, frozenset[str]] = {
    "ARI": frozenset({"ARI", "AZ"}),
}

OBSERVATION_FIELDS = frozenset(
    {
        "observation_contract_version",
        "game_id",
        "official_game_pk",
        "season",
        "scheduled_start_utc",
        "official_status",
        "status_reason",
        "away_team",
        "home_team",
        "away_score",
        "home_score",
        "source_name",
        "source_endpoint_id",
        "source_observed_at_utc",
        "result_available_at_utc",
        "raw_sha256",
        "source_fingerprint",
        "record_fingerprint",
        "provenance_status",
    }
)
SOURCE_INDEX_FIELDS = frozenset(
    {
        "source_index_contract_version",
        "observation_contract_version",
        "game_id",
        "official_game_pk",
        "source_name",
        "source_endpoint_id",
        "source_observed_at_utc",
        "relative_raw_path",
        "relative_observation_path",
        "raw_sha256",
        "source_fingerprint",
        "record_fingerprint",
        "provenance_status",
    }
)

_DETAILED_STATUS_MAP = {
    "scheduled": "SCHEDULED",
    "pre-game": "SCHEDULED",
    "pregame": "SCHEDULED",
    "warmup": "SCHEDULED",
    "delayed start": "SCHEDULED",
    "in progress": "IN_PROGRESS",
    "manager challenge": "IN_PROGRESS",
    "review": "IN_PROGRESS",
    "delayed": "IN_PROGRESS",
    "rain delay": "IN_PROGRESS",
    "suspended": "SUSPENDED",
    "final": "FINAL",
    "game over": "FINAL",
    "completed early": "FINAL",
    "postponed": "POSTPONED",
    "cancelled": "CANCELLED",
    "canceled": "CANCELLED",
    "forfeit": "FORFEIT",
    "forfeited": "FORFEIT",
}
_CODED_STATUS_MAP = {
    "S": "SCHEDULED",
    "P": "SCHEDULED",
    "W": "SCHEDULED",
    "I": "IN_PROGRESS",
    "M": "IN_PROGRESS",
    "U": "SUSPENDED",
    "F": "FINAL",
    "O": "FINAL",
    "D": "POSTPONED",
    "C": "CANCELLED",
}
_ABSTRACT_STATUS_MAP = {
    "preview": "SCHEDULED",
    "live": "IN_PROGRESS",
    "final": "FINAL",
}
_ABSTRACT_CODE_MAP = {
    "P": "SCHEDULED",
    "L": "IN_PROGRESS",
    "F": "FINAL",
}


class P272Error(RuntimeError):
    """Fail-closed validation, network-boundary, or write-once error."""


def normalize_nfc(value: Any) -> Any:
    """Recursively normalize JSON strings and mapping keys to Unicode NFC."""
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [normalize_nfc(item) for item in value]
    if isinstance(value, tuple):
        return [normalize_nfc(item) for item in value]
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise P272Error("Canonical JSON mappings require string keys")
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized:
                raise P272Error("Unicode NFC normalization produced a duplicate key")
            normalized[normalized_key] = normalize_nfc(item)
        return normalized
    return value


def canonical_json_bytes(value: Any, *, trailing_newline: bool = False) -> bytes:
    """Return deterministic compact UTF-8 JSON using the P271-approved rules."""
    encoded = json.dumps(
        normalize_nfc(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return encoded + (b"\n" if trailing_newline else b"")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def utc_now() -> str:
    """Return the current UTC time; capture calls this only after response.read()."""
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def normalize_utc_timestamp(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise P272Error(f"{field_name} must be a non-empty timestamp string")
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise P272Error(f"{field_name} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise P272Error(f"{field_name} must include an explicit UTC offset")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise P272Error(f"{field_name} must be an object")
    return value


def _optional_string(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise P272Error(f"{field_name} must be a string or null")
    normalized = unicodedata.normalize("NFC", value).strip()
    return normalized or None


def _strict_positive_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise P272Error(f"{field_name} must be a positive integer")
    return value


def _strict_nonnegative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise P272Error(f"{field_name} must be a non-negative integer")
    return value


def _parse_game_pk_argument(value: str) -> int:
    if not re.fullmatch(r"[0-9]+", value) or int(value) <= 0:
        raise argparse.ArgumentTypeError("gamePk must contain only digits and be positive")
    return int(value)


def validate_single_game_pk(game_pks: Sequence[int]) -> int:
    """Require exactly one explicit gamePk and reject batch-shaped input."""
    if len(game_pks) != 1:
        raise P272Error("Exactly one explicit numeric gamePk is required")
    return _strict_positive_int(game_pks[0], "gamePk")


def _parse_official_json(raw: bytes) -> Mapping[str, Any]:
    if not isinstance(raw, bytes) or not raw:
        raise P272Error("Official raw response must be non-empty bytes")

    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        normalized_keys: set[str] = set()
        for key, value in pairs:
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized_keys:
                raise P272Error("Official JSON contains duplicate or NFC-equivalent keys")
            normalized_keys.add(normalized_key)
            result[key] = value
        return result

    try:
        parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P272Error("Official response must be valid UTF-8 JSON") from exc
    return _require_mapping(parsed, "official response")


def _team_code(value: Any, field_name: str) -> tuple[str, str]:
    if not isinstance(value, str) or not value.strip():
        raise P272Error(f"{field_name} must be a non-empty abbreviation")
    preserved = unicodedata.normalize("NFC", value).strip()
    validation_code = preserved.upper()
    if not re.fullmatch(r"[A-Z0-9]{2,4}", validation_code):
        raise P272Error(f"{field_name} is not a valid team abbreviation")
    return preserved, validation_code


def _team_identity_key(code: str) -> str:
    normalized = unicodedata.normalize("NFC", code).strip().upper()
    for canonical, aliases in TEAM_IDENTITY_ALIAS_GROUPS.items():
        if normalized in aliases:
            return canonical
    return normalized


def validate_expected_team(official: str, expected: str, field_name: str) -> None:
    _, official_code = _team_code(official, field_name)
    _, expected_code = _team_code(expected, f"expected {field_name}")
    if _team_identity_key(official_code) != _team_identity_key(expected_code):
        raise P272Error(
            f"Official {field_name} identity mismatch: expected {expected_code}, "
            f"observed {official_code}"
        )


def _optional_team_id(value: Any, field_name: str) -> int | None:
    if value is None:
        return None
    return _strict_positive_int(value, field_name)


def _extract_team_identity(
    root: Mapping[str, Any], game_data: Mapping[str, Any], side: str
) -> tuple[str, int | None]:
    teams = _require_mapping(game_data.get("teams"), "gameData.teams")
    primary = _require_mapping(teams.get(side), f"gameData.teams.{side}")
    preserved, primary_code = _team_code(
        primary.get("abbreviation"), f"gameData.teams.{side}.abbreviation"
    )
    primary_id = _optional_team_id(primary.get("id"), f"gameData.teams.{side}.id")

    live_data = root.get("liveData")
    if live_data is not None:
        live = _require_mapping(live_data, "liveData")
        boxscore = live.get("boxscore")
        if boxscore is not None:
            boxscore_obj = _require_mapping(boxscore, "liveData.boxscore")
            box_teams = boxscore_obj.get("teams")
            if box_teams is not None:
                box_team_map = _require_mapping(box_teams, "liveData.boxscore.teams")
                side_payload = box_team_map.get(side)
                if side_payload is not None:
                    side_obj = _require_mapping(
                        side_payload, f"liveData.boxscore.teams.{side}"
                    )
                    box_team = _require_mapping(
                        side_obj.get("team"), f"liveData.boxscore.teams.{side}.team"
                    )
                    box_id = _optional_team_id(
                        box_team.get("id"), f"liveData.boxscore.teams.{side}.team.id"
                    )
                    if primary_id is not None and box_id is not None and primary_id != box_id:
                        raise P272Error(f"Conflicting official {side} team identity evidence")
                    box_abbreviation = box_team.get("abbreviation")
                    if box_abbreviation is not None:
                        _, box_code = _team_code(
                            box_abbreviation,
                            f"liveData.boxscore.teams.{side}.team.abbreviation",
                        )
                        if _team_identity_key(primary_code) != _team_identity_key(box_code):
                            raise P272Error(
                                f"Conflicting official {side} team abbreviation evidence"
                            )
    return preserved, primary_id


def _mapped_status(
    raw_value: Any, field_name: str, mapping: Mapping[str, str], *, uppercase: bool
) -> str | None:
    if raw_value is None:
        return None
    if not isinstance(raw_value, str):
        raise P272Error(f"{field_name} must be a string")
    key = raw_value.strip().upper() if uppercase else raw_value.strip().casefold()
    mapped = mapping.get(key)
    if mapped is None:
        raise P272Error(f"Unrecognized official status evidence in {field_name}: {raw_value!r}")
    return mapped


def _abstract_compatible(abstract: str, selected: str) -> bool:
    if abstract == "SCHEDULED":
        return selected == "SCHEDULED"
    if abstract == "IN_PROGRESS":
        return selected in {"IN_PROGRESS", "SUSPENDED"}
    return selected in {"FINAL", "FORFEIT", "POSTPONED", "CANCELLED", "SUSPENDED"}


def resolve_official_status(status_payload: Mapping[str, Any]) -> str:
    """Resolve official status and fail closed on contradictory status fields."""
    status = _require_mapping(status_payload, "gameData.status")
    detailed = _mapped_status(
        status.get("detailedState"),
        "gameData.status.detailedState",
        _DETAILED_STATUS_MAP,
        uppercase=False,
    )
    coded_values = [
        mapped
        for mapped in (
            _mapped_status(
                status.get("statusCode"),
                "gameData.status.statusCode",
                _CODED_STATUS_MAP,
                uppercase=True,
            ),
            _mapped_status(
                status.get("codedGameState"),
                "gameData.status.codedGameState",
                _CODED_STATUS_MAP,
                uppercase=True,
            ),
        )
        if mapped is not None
    ]
    if len(set(coded_values)) > 1:
        raise P272Error("Conflicting official coded status evidence")
    coded = coded_values[0] if coded_values else None

    abstract_values = [
        mapped
        for mapped in (
            _mapped_status(
                status.get("abstractGameState"),
                "gameData.status.abstractGameState",
                _ABSTRACT_STATUS_MAP,
                uppercase=False,
            ),
            _mapped_status(
                status.get("abstractGameCode"),
                "gameData.status.abstractGameCode",
                _ABSTRACT_CODE_MAP,
                uppercase=True,
            ),
        )
        if mapped is not None
    ]
    if len(set(abstract_values)) > 1:
        raise P272Error("Conflicting official abstract status evidence")
    abstract = abstract_values[0] if abstract_values else None

    selected = detailed or coded or abstract
    if selected is None:
        raise P272Error("Official status evidence is missing")
    if detailed is not None and coded is not None and detailed != coded:
        if not (detailed == "FORFEIT" and coded == "FINAL"):
            raise P272Error("Conflicting official detailed/coded status evidence")
    if abstract is not None and not _abstract_compatible(abstract, selected):
        raise P272Error("Conflicting official abstract status evidence")
    return selected


def _optional_timestamp(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    return normalize_utc_timestamp(value, field_name)


def _optional_season(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise P272Error("gameData.game.season must be a four-digit year or null")
    if isinstance(value, str) and re.fullmatch(r"[0-9]{4}", value.strip()):
        season = int(value.strip())
    elif isinstance(value, int):
        season = value
    else:
        raise P272Error("gameData.game.season must be a four-digit year or null")
    if season < 1800 or season > 9999:
        raise P272Error("gameData.game.season is outside the accepted year range")
    return season


def _score_candidates(root: Mapping[str, Any], side: str) -> list[int]:
    candidates: list[int] = []
    game_data = _require_mapping(root.get("gameData"), "gameData")
    teams = _require_mapping(game_data.get("teams"), "gameData.teams")
    team = _require_mapping(teams.get(side), f"gameData.teams.{side}")
    if team.get("score") is not None:
        candidates.append(
            _strict_nonnegative_int(team["score"], f"gameData.teams.{side}.score")
        )

    live_data = root.get("liveData")
    if live_data is not None:
        live = _require_mapping(live_data, "liveData")
        linescore = live.get("linescore")
        if linescore is not None:
            linescore_obj = _require_mapping(linescore, "liveData.linescore")
            line_teams = linescore_obj.get("teams")
            if line_teams is not None:
                line_team_map = _require_mapping(line_teams, "liveData.linescore.teams")
                line_side = line_team_map.get(side)
                if line_side is not None:
                    line_side_obj = _require_mapping(
                        line_side, f"liveData.linescore.teams.{side}"
                    )
                    if line_side_obj.get("runs") is not None:
                        candidates.append(
                            _strict_nonnegative_int(
                                line_side_obj["runs"],
                                f"liveData.linescore.teams.{side}.runs",
                            )
                        )

        boxscore = live.get("boxscore")
        if boxscore is not None:
            boxscore_obj = _require_mapping(boxscore, "liveData.boxscore")
            box_teams = boxscore_obj.get("teams")
            if box_teams is not None:
                box_team_map = _require_mapping(box_teams, "liveData.boxscore.teams")
                box_side = box_team_map.get(side)
                if box_side is not None:
                    box_side_obj = _require_mapping(
                        box_side, f"liveData.boxscore.teams.{side}"
                    )
                    team_stats = box_side_obj.get("teamStats")
                    if team_stats is not None:
                        stats_obj = _require_mapping(
                            team_stats, f"liveData.boxscore.teams.{side}.teamStats"
                        )
                        batting = stats_obj.get("batting")
                        if batting is not None:
                            batting_obj = _require_mapping(
                                batting,
                                f"liveData.boxscore.teams.{side}.teamStats.batting",
                            )
                            if batting_obj.get("runs") is not None:
                                candidates.append(
                                    _strict_nonnegative_int(
                                        batting_obj["runs"],
                                        "liveData.boxscore.teams."
                                        f"{side}.teamStats.batting.runs",
                                    )
                                )
    return candidates


def _resolved_score(root: Mapping[str, Any], side: str) -> int | None:
    candidates = _score_candidates(root, side)
    distinct = set(candidates)
    if len(distinct) > 1:
        raise P272Error(f"Conflicting official {side} score evidence")
    return next(iter(distinct)) if distinct else None


def _source_fingerprint(record: Mapping[str, Any]) -> str:
    source_identity = {
        "official_game_pk": record["official_game_pk"],
        "raw_sha256": record["raw_sha256"],
        "source_endpoint_id": record["source_endpoint_id"],
        "source_name": record["source_name"],
        "source_observed_at_utc": record["source_observed_at_utc"],
    }
    return sha256_bytes(canonical_json_bytes(source_identity))


def _record_fingerprint(record: Mapping[str, Any]) -> str:
    logical_record = {
        key: value for key, value in record.items() if key != "record_fingerprint"
    }
    return sha256_bytes(canonical_json_bytes(logical_record))


def build_observation_record(
    raw: bytes,
    game_pk: int,
    source_observed_at_utc: str,
    *,
    expected_away_team: str | None = None,
    expected_home_team: str | None = None,
) -> dict[str, Any]:
    """Build one logical observation from exact official response bytes."""
    requested_game_pk = _strict_positive_int(game_pk, "gamePk")
    observed_at = normalize_utc_timestamp(
        source_observed_at_utc, "source_observed_at_utc"
    )
    if (expected_away_team is None) != (expected_home_team is None):
        raise P272Error("Expected away and home teams must be supplied together")

    root = _parse_official_json(raw)
    game_data = _require_mapping(root.get("gameData"), "gameData")
    game = _require_mapping(game_data.get("game"), "gameData.game")
    official_game_pk = _strict_positive_int(game.get("pk"), "gameData.game.pk")
    if official_game_pk != requested_game_pk:
        raise P272Error(
            f"Official game identity mismatch: requested {requested_game_pk}, "
            f"observed {official_game_pk}"
        )
    top_level_pk = root.get("gamePk")
    if top_level_pk is not None:
        parsed_top_level_pk = _strict_positive_int(top_level_pk, "gamePk")
        if parsed_top_level_pk != official_game_pk:
            raise P272Error("Conflicting top-level and nested official game identity")

    away_team, away_team_id = _extract_team_identity(root, game_data, "away")
    home_team, home_team_id = _extract_team_identity(root, game_data, "home")
    if away_team_id is not None and home_team_id is not None and away_team_id == home_team_id:
        raise P272Error("Official away and home team identities conflict")
    if expected_away_team is not None and expected_home_team is not None:
        validate_expected_team(away_team, expected_away_team, "away_team")
        validate_expected_team(home_team, expected_home_team, "home_team")

    status_payload = _require_mapping(game_data.get("status"), "gameData.status")
    official_status = resolve_official_status(status_payload)
    status_reason = _optional_string(
        status_payload.get("reason"), "gameData.status.reason"
    )
    datetime_payload = game_data.get("datetime")
    if datetime_payload is None:
        scheduled_start = None
    else:
        datetime_obj = _require_mapping(datetime_payload, "gameData.datetime")
        scheduled_start = _optional_timestamp(
            datetime_obj.get("dateTime"), "gameData.datetime.dateTime"
        )
    season = _optional_season(game.get("season"))

    away_score_candidate = _resolved_score(root, "away")
    home_score_candidate = _resolved_score(root, "home")
    if official_status in RESOLVED_STATUSES:
        away_score = away_score_candidate
        home_score = home_score_candidate
        result_available = observed_at
    else:
        away_score = None
        home_score = None
        result_available = None

    game_id = (
        f"mlb_{season}_{official_game_pk}"
        if season is not None
        else f"mlb_{official_game_pk}"
    )
    required_logical_values = [season, scheduled_start, away_team, home_team]
    if official_status in RESOLVED_STATUSES:
        required_logical_values.extend([away_score, home_score])
    provenance_status = (
        "COMPLETE" if all(value is not None for value in required_logical_values) else "INCOMPLETE"
    )

    record: dict[str, Any] = {
        "observation_contract_version": OBSERVATION_CONTRACT_VERSION,
        "game_id": game_id,
        "official_game_pk": official_game_pk,
        "season": season,
        "scheduled_start_utc": scheduled_start,
        "official_status": official_status,
        "status_reason": status_reason,
        "away_team": away_team,
        "home_team": home_team,
        "away_score": away_score,
        "home_score": home_score,
        "source_name": SOURCE_NAME,
        "source_endpoint_id": SOURCE_ENDPOINT_ID,
        "source_observed_at_utc": observed_at,
        "result_available_at_utc": result_available,
        "raw_sha256": sha256_bytes(raw),
        "source_fingerprint": None,
        "record_fingerprint": None,
        "provenance_status": provenance_status,
    }
    record["source_fingerprint"] = _source_fingerprint(record)
    record["record_fingerprint"] = _record_fingerprint(record)
    normalized = normalize_nfc(record)
    validate_observation_record(normalized)
    return normalized


def validate_observation_record(record: Mapping[str, Any]) -> None:
    if set(record) != OBSERVATION_FIELDS:
        missing = sorted(OBSERVATION_FIELDS - set(record))
        extra = sorted(set(record) - OBSERVATION_FIELDS)
        raise P272Error(f"Observation schema mismatch; missing={missing}, extra={extra}")
    if record["observation_contract_version"] != OBSERVATION_CONTRACT_VERSION:
        raise P272Error("Unexpected observation_contract_version")

    official_game_pk = _strict_positive_int(record["official_game_pk"], "official_game_pk")
    season = record["season"]
    if season is not None:
        season = _optional_season(season)
    expected_game_id = (
        f"mlb_{season}_{official_game_pk}" if season is not None else f"mlb_{official_game_pk}"
    )
    if record["game_id"] != expected_game_id:
        raise P272Error("game_id does not match the official game identity")

    status = record["official_status"]
    if status not in ALLOWED_STATUSES:
        raise P272Error(f"official_status is not allowed: {status!r}")
    if record["source_name"] != SOURCE_NAME:
        raise P272Error("source_name is not the approved official source")
    if record["source_endpoint_id"] != SOURCE_ENDPOINT_ID:
        raise P272Error("source_endpoint_id is not the approved endpoint")

    observed_at = normalize_utc_timestamp(
        record["source_observed_at_utc"], "source_observed_at_utc"
    )
    if observed_at != record["source_observed_at_utc"]:
        raise P272Error("source_observed_at_utc is not in canonical UTC form")
    scheduled_start = record["scheduled_start_utc"]
    if scheduled_start is not None:
        normalized_start = normalize_utc_timestamp(scheduled_start, "scheduled_start_utc")
        if normalized_start != scheduled_start:
            raise P272Error("scheduled_start_utc is not in canonical UTC form")

    result_available = record["result_available_at_utc"]
    if status in RESOLVED_STATUSES:
        if result_available != observed_at:
            raise P272Error(
                "FINAL/FORFEIT result availability must equal the observation timestamp"
            )
    elif result_available is not None:
        raise P272Error("Non-final result availability must remain null")

    for field in ("away_team", "home_team"):
        _team_code(record[field], field)
    if record["status_reason"] is not None and not isinstance(record["status_reason"], str):
        raise P272Error("status_reason must be a string or null")
    for field in ("away_score", "home_score"):
        if record[field] is not None:
            _strict_nonnegative_int(record[field], field)
    if status not in RESOLVED_STATUSES and (
        record["away_score"] is not None or record["home_score"] is not None
    ):
        raise P272Error("Non-final observations must not expose partial scores as results")

    provenance = record["provenance_status"]
    if provenance not in ALLOWED_PROVENANCE_STATUSES:
        raise P272Error("provenance_status is not allowed")
    if provenance == "COMPLETE":
        required = [season, scheduled_start, record["away_team"], record["home_team"]]
        if status in RESOLVED_STATUSES:
            required.extend([record["away_score"], record["home_score"]])
        if any(value is None for value in required):
            raise P272Error("COMPLETE provenance is missing required official evidence")

    for field in ("raw_sha256", "source_fingerprint", "record_fingerprint"):
        if not _is_sha256(record[field]):
            raise P272Error(f"{field} must be a lowercase SHA-256")
    if record["source_fingerprint"] != _source_fingerprint(record):
        raise P272Error("source_fingerprint does not match canonical source evidence")
    if record["record_fingerprint"] != _record_fingerprint(record):
        raise P272Error("record_fingerprint does not match canonical record content")


def _raw_relative_path(record: Mapping[str, Any]) -> str:
    return f"raw/{record['game_id']}.feed.live.json"


def build_bundle_bytes(raw: bytes, record: Mapping[str, Any]) -> dict[str, bytes]:
    """Build the complete deterministic four-file observation bundle in memory."""
    validate_observation_record(record)
    if sha256_bytes(raw) != record["raw_sha256"]:
        raise P272Error("Raw response bytes do not match observation raw_sha256")
    raw_relative_path = _raw_relative_path(record)
    observation_bytes = canonical_json_bytes(record, trailing_newline=True)
    source_index = {
        "source_index_contract_version": SOURCE_INDEX_CONTRACT_VERSION,
        "observation_contract_version": OBSERVATION_CONTRACT_VERSION,
        "game_id": record["game_id"],
        "official_game_pk": record["official_game_pk"],
        "source_name": SOURCE_NAME,
        "source_endpoint_id": SOURCE_ENDPOINT_ID,
        "source_observed_at_utc": record["source_observed_at_utc"],
        "relative_raw_path": raw_relative_path,
        "relative_observation_path": OBSERVATION_FILENAME,
        "raw_sha256": record["raw_sha256"],
        "source_fingerprint": record["source_fingerprint"],
        "record_fingerprint": record["record_fingerprint"],
        "provenance_status": record["provenance_status"],
    }
    if set(source_index) != SOURCE_INDEX_FIELDS:
        raise P272Error("Internal source index schema mismatch")
    source_index_bytes = canonical_json_bytes(source_index, trailing_newline=True)
    artifacts = {
        raw_relative_path: raw,
        OBSERVATION_FILENAME: observation_bytes,
        SOURCE_INDEX_FILENAME: source_index_bytes,
    }
    checksum_lines = [
        f"{sha256_bytes(artifacts[path])}  {path}" for path in sorted(artifacts)
    ]
    artifacts[CHECKSUM_FILENAME] = ("\n".join(checksum_lines) + "\n").encode("utf-8")
    return artifacts


def _existing_inventory(output_root: Path) -> tuple[set[str], set[str]]:
    files: set[str] = set()
    directories: set[str] = set()
    if not output_root.exists():
        return files, directories
    if output_root.is_symlink() or not output_root.is_dir():
        raise P272Error("Output root must be a real directory, not a file or symlink")
    for path in output_root.rglob("*"):
        relative = path.relative_to(output_root).as_posix()
        if path.is_symlink():
            raise P272Error(f"Bundle path may not be a symlink: {relative}")
        if path.is_file():
            files.add(relative)
        elif path.is_dir():
            directories.add(relative)
        else:
            raise P272Error(f"Unsupported bundle filesystem entry: {relative}")
    return files, directories


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_once_atomic(path: Path, data: bytes) -> bool:
    """Atomically create path without overwrite; return False if identical existed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise P272Error(f"Refusing to write through symlink: {path}")
    if path.exists():
        if not path.is_file() or path.read_bytes() != data:
            raise P272Error(f"Existing bundle path differs; overwrite refused: {path}")
        return False

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as temporary_file:
            temporary_file.write(data)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        try:
            os.link(temporary_path, path)
        except FileExistsError:
            if path.is_symlink() or not path.is_file() or path.read_bytes() != data:
                raise P272Error(f"Concurrent differing bundle path refused: {path}")
            return False
        _fsync_directory(path.parent)
        return True
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def write_bundle(output_root: Path, artifacts: Mapping[str, bytes]) -> str:
    """Write or idempotently verify an immutable deterministic bundle."""
    root = Path(output_root)
    expected_files = set(artifacts)
    expected_directories = {str(Path(path).parent.as_posix()) for path in artifacts}
    expected_directories.discard(".")
    existing_files, existing_directories = _existing_inventory(root)
    unexpected_files = sorted(existing_files - expected_files)
    unexpected_directories = sorted(existing_directories - expected_directories)
    if unexpected_files or unexpected_directories:
        raise P272Error(
            "Output root contains paths outside the immutable bundle; "
            f"files={unexpected_files}, directories={unexpected_directories}"
        )
    for relative_path in sorted(existing_files):
        if (root / relative_path).read_bytes() != artifacts[relative_path]:
            raise P272Error(
                f"Existing bundle differs; write-once overwrite refused: {relative_path}"
            )

    already_complete = existing_files == expected_files
    root.mkdir(parents=True, exist_ok=True)
    write_order = sorted(expected_files - {CHECKSUM_FILENAME}) + [CHECKSUM_FILENAME]
    for relative_path in write_order:
        _write_once_atomic(root / relative_path, artifacts[relative_path])

    final_files, final_directories = _existing_inventory(root)
    if final_files != expected_files or final_directories != expected_directories:
        raise P272Error("Final bundle inventory differs from the deterministic contract")
    for relative_path, expected_bytes in artifacts.items():
        if (root / relative_path).read_bytes() != expected_bytes:
            raise P272Error(f"Final bundle verification failed: {relative_path}")
    return "VERIFIED_IDENTICAL" if already_complete else "CREATED"


def validate_official_request(
    url: str, game_pk: int, headers: Mapping[str, str]
) -> None:
    """Enforce the exact unauthenticated official MLB request boundary."""
    requested_game_pk = _strict_positive_int(game_pk, "gamePk")
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise P272Error("Official endpoint URL is malformed") from exc
    if parsed.scheme.lower() != "https":
        raise P272Error("Official endpoint must use HTTPS")
    if parsed.username is not None or parsed.password is not None:
        raise P272Error("URL userinfo/authentication is forbidden")
    if parsed.hostname is None or parsed.hostname.lower() != OFFICIAL_HOST:
        raise P272Error("Only the official statsapi.mlb.com host is allowed")
    if port is not None:
        raise P272Error("Custom endpoint ports are forbidden")
    expected_path = f"/api/v1.1/game/{requested_game_pk}/feed/live"
    if parsed.path != expected_path or parsed.query or parsed.fragment:
        raise P272Error("Endpoint must be the exact one-game MLB live-feed path")

    normalized_headers = {name.strip().lower(): value for name, value in headers.items()}
    if set(normalized_headers) != {"accept", "user-agent"}:
        raise P272Error("Authentication, cookies, credentials, and extra headers are forbidden")
    if normalized_headers["accept"] != "application/json":
        raise P272Error("Official request Accept header must be application/json")
    if normalized_headers["user-agent"] != USER_AGENT:
        raise P272Error("Official request User-Agent is fixed by the recorder contract")


def build_official_request(
    game_pk: int,
    *,
    url: str | None = None,
    headers: Mapping[str, str] | None = None,
) -> urllib.request.Request:
    requested_game_pk = _strict_positive_int(game_pk, "gamePk")
    endpoint = url or OFFICIAL_ENDPOINT_TEMPLATE.format(game_pk=requested_game_pk)
    request_headers = dict(
        headers or {"Accept": "application/json", "User-Agent": USER_AGENT}
    )
    validate_official_request(endpoint, requested_game_pk, request_headers)
    return urllib.request.Request(endpoint, headers=request_headers, method="GET")


def fetch_official_response_once(game_pk: int) -> tuple[bytes, str]:
    """Perform exactly one request and timestamp after the complete body is read."""
    request = build_official_request(game_pk)
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status = int(response.getcode())
            content_type = response.headers.get("Content-Type")
            raw = response.read()
        observed_at = utc_now()
    except urllib.error.HTTPError as exc:
        raise P272Error(f"Official MLB request failed with HTTP {exc.code}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise P272Error("Official MLB request failed; automatic retry is forbidden") from exc

    if status != 200:
        raise P272Error(f"Official MLB response status must be 200, observed {status}")
    if not content_type or not content_type.lower().startswith("application/json"):
        raise P272Error("Official MLB response Content-Type must be application/json")
    return raw, observed_at


def capture(
    *,
    game_pk: int,
    output_root: Path,
    expected_away_team: str | None = None,
    expected_home_team: str | None = None,
) -> tuple[dict[str, Any], str]:
    """Capture one game; intentionally has no caller-supplied timestamp parameter."""
    raw, observed_at = fetch_official_response_once(game_pk)
    record = build_observation_record(
        raw,
        game_pk,
        observed_at,
        expected_away_team=expected_away_team,
        expected_home_team=expected_home_team,
    )
    state = write_bundle(output_root, build_bundle_bytes(raw, record))
    return record, state


def offline_verify(
    *,
    raw_response: Path,
    game_pk: int,
    observed_at_utc: str,
    output_root: Path,
    expected_away_team: str | None = None,
    expected_home_team: str | None = None,
) -> tuple[dict[str, Any], str]:
    """Build or verify a bundle from already saved bytes without any network call."""
    source_path = Path(raw_response)
    if source_path.is_symlink() or not source_path.is_file():
        raise P272Error("--raw-response must be an existing regular file")
    raw = source_path.read_bytes()
    record = build_observation_record(
        raw,
        game_pk,
        observed_at_utc,
        expected_away_team=expected_away_team,
        expected_home_team=expected_home_team,
    )
    state = write_bundle(output_root, build_bundle_bytes(raw, record))
    return record, state


def _add_shared_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "--game-pk",
        action="append",
        dest="game_pks",
        type=_parse_game_pk_argument,
        required=True,
        help="Exactly one explicit numeric MLB gamePk",
    )
    command.add_argument("--output-root", type=Path, required=True)
    command.add_argument("--expected-away-team")
    command.add_argument("--expected-home-team")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record prospective official MLB result availability for one game"
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    capture_parser = subparsers.add_parser("capture")
    _add_shared_arguments(capture_parser)

    offline_parser = subparsers.add_parser("offline-verify")
    _add_shared_arguments(offline_parser)
    offline_parser.add_argument("--raw-response", type=Path, required=True)
    offline_parser.add_argument("--observed-at-utc", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        game_pk = validate_single_game_pk(args.game_pks)
        if args.mode == "capture":
            record, bundle_state = capture(
                game_pk=game_pk,
                output_root=args.output_root,
                expected_away_team=args.expected_away_team,
                expected_home_team=args.expected_home_team,
            )
        else:
            record, bundle_state = offline_verify(
                raw_response=args.raw_response,
                game_pk=game_pk,
                observed_at_utc=args.observed_at_utc,
                output_root=args.output_root,
                expected_away_team=args.expected_away_team,
                expected_home_team=args.expected_home_team,
            )
    except P272Error as exc:
        print(f"P272_FAIL_CLOSED: {exc}", file=sys.stderr)
        return 2

    result = {
        "bundle_state": bundle_state,
        "game_id": record["game_id"],
        "mode": args.mode,
        "official_game_pk": record["official_game_pk"],
        "record_fingerprint": record["record_fingerprint"],
        "source_observed_at_utc": record["source_observed_at_utc"],
    }
    print(canonical_json_bytes(result).decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
