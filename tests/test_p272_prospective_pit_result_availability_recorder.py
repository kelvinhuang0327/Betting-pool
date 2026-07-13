"""Focused offline tests for the P272 prospective availability recorder."""
from __future__ import annotations

import copy
import inspect
import json
import os
import urllib.error
from pathlib import Path

import pytest

from scripts import _p272_prospective_pit_result_availability_recorder as p272


OBSERVED_AT = "2026-07-13T03:00:00Z"
REPO_ROOT = Path(__file__).resolve().parents[1]
P271_RAW_ROOT = (
    REPO_ROOT / "data/mlb_2026/pit_replay/p271_official_result_status_v1/raw"
)
FINAL_FIXTURE = P271_RAW_ROOT / "mlb_2026_822834.feed.live.json"
ALIAS_FIXTURE = P271_RAW_ROOT / "mlb_2026_825108.feed.live.json"


@pytest.fixture(autouse=True)
def block_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_urlopen(*args, **kwargs):
        raise AssertionError("P272 tests must never call the network")

    monkeypatch.setattr(p272.urllib.request, "urlopen", forbidden_urlopen)


def fixture_payload(path: Path = FINAL_FIXTURE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_bytes(payload: dict) -> bytes:
    return p272.canonical_json_bytes(payload)


def bundle_bytes(output_root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(output_root).as_posix(): path.read_bytes()
        for path in output_root.rglob("*")
        if path.is_file()
    }


def test_canonical_json_is_sorted_compact_nfc_and_sha256_stable() -> None:
    decomposed = {"z": 1, "label": "Cafe\u0301"}
    composed = {"label": "Caf\u00e9", "z": 1}
    expected = b'{"label":"Caf\xc3\xa9","z":1}'

    assert p272.canonical_json_bytes(decomposed) == expected
    assert p272.canonical_json_bytes(composed) == expected
    assert p272.sha256_bytes(expected) == p272.sha256_bytes(expected)
    assert len(p272.sha256_bytes(expected)) == 64


def test_canonical_json_rejects_nfc_duplicate_keys_and_non_finite_values() -> None:
    with pytest.raises(p272.P272Error, match="duplicate key"):
        p272.canonical_json_bytes({"Cafe\u0301": 1, "Caf\u00e9": 2})
    with pytest.raises(ValueError):
        p272.canonical_json_bytes({"bad": float("nan")})


def test_final_availability_equals_observation_time_and_preserves_raw_hash() -> None:
    raw = FINAL_FIXTURE.read_bytes()
    record = p272.build_observation_record(raw, 822834, OBSERVED_AT)

    assert record["official_status"] == "FINAL"
    assert record["source_observed_at_utc"] == OBSERVED_AT
    assert record["result_available_at_utc"] == OBSERVED_AT
    assert record["raw_sha256"] == p272.sha256_bytes(raw)
    assert record["away_score"] == 14
    assert record["home_score"] == 5
    assert record["provenance_status"] == "COMPLETE"


@pytest.mark.parametrize(
    ("detail", "code", "abstract", "abstract_code", "expected"),
    [
        ("Scheduled", "S", "Preview", "P", "SCHEDULED"),
        ("In Progress", "I", "Live", "L", "IN_PROGRESS"),
        ("Suspended", "U", "Live", "L", "SUSPENDED"),
        ("Postponed", "D", "Final", "F", "POSTPONED"),
        ("Cancelled", "C", "Final", "F", "CANCELLED"),
    ],
)
def test_non_final_statuses_leave_result_availability_and_scores_null(
    detail: str,
    code: str,
    abstract: str,
    abstract_code: str,
    expected: str,
) -> None:
    payload = fixture_payload()
    payload["gameData"]["status"].update(
        {
            "detailedState": detail,
            "statusCode": code,
            "codedGameState": code,
            "abstractGameState": abstract,
            "abstractGameCode": abstract_code,
        }
    )
    record = p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)

    assert record["official_status"] == expected
    assert record["result_available_at_utc"] is None
    assert record["away_score"] is None
    assert record["home_score"] is None


def test_forfeit_is_resolved_at_observation_time() -> None:
    payload = fixture_payload()
    payload["gameData"]["status"].update(
        {
            "detailedState": "Forfeit",
            "statusCode": "F",
            "codedGameState": "F",
            "abstractGameState": "Final",
            "abstractGameCode": "F",
        }
    )
    record = p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)
    assert record["official_status"] == "FORFEIT"
    assert record["result_available_at_utc"] == OBSERVED_AT


def test_capture_has_no_backdating_parameter_or_cli_option(tmp_path: Path) -> None:
    assert "observed_at_utc" not in inspect.signature(p272.capture).parameters
    with pytest.raises(SystemExit):
        p272._parser().parse_args(
            [
                "capture",
                "--game-pk",
                "822834",
                "--output-root",
                str(tmp_path / "bundle"),
                "--observed-at-utc",
                "2000-01-01T00:00:00Z",
            ]
        )


def test_offline_verify_accepts_fixed_time_and_never_uses_feed_metadata(
    tmp_path: Path,
) -> None:
    record, state = p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc="2026-07-13T11:00:00+08:00",
        output_root=tmp_path / "bundle",
    )
    payload = fixture_payload()

    assert state == "CREATED"
    assert record["source_observed_at_utc"] == OBSERVED_AT
    assert record["source_observed_at_utc"] != payload["metaData"]["timeStamp"]
    assert record["result_available_at_utc"] == OBSERVED_AT


def test_official_request_rejects_non_mlb_host_and_broad_paths() -> None:
    with pytest.raises(p272.P272Error, match="official statsapi"):
        p272.build_official_request(
            822834,
            url="https://example.com/api/v1.1/game/822834/feed/live",
        )
    with pytest.raises(p272.P272Error, match="exact one-game"):
        p272.build_official_request(
            822834,
            url="https://statsapi.mlb.com/api/v1/schedule?sportId=1",
        )


def test_official_request_rejects_url_userinfo_authentication_and_cookies() -> None:
    endpoint = p272.OFFICIAL_ENDPOINT_TEMPLATE.format(game_pk=822834)
    with pytest.raises(p272.P272Error, match="userinfo"):
        p272.build_official_request(
            822834,
            url="https://user:secret@statsapi.mlb.com/api/v1.1/game/822834/feed/live",
        )
    with pytest.raises(p272.P272Error, match="Authentication"):
        p272.build_official_request(
            822834,
            url=endpoint,
            headers={
                "Accept": "application/json",
                "User-Agent": p272.USER_AGENT,
                "Authorization": "Bearer forbidden",
            },
        )
    with pytest.raises(p272.P272Error, match="Authentication"):
        p272.build_official_request(
            822834,
            url=endpoint,
            headers={
                "Accept": "application/json",
                "User-Agent": p272.USER_AGENT,
                "Cookie": "forbidden=true",
            },
        )


def test_exact_one_numeric_game_restriction() -> None:
    assert p272.validate_single_game_pk([822834]) == 822834
    with pytest.raises(p272.P272Error, match="Exactly one"):
        p272.validate_single_game_pk([])
    with pytest.raises(p272.P272Error, match="Exactly one"):
        p272.validate_single_game_pk([822834, 822835])
    with pytest.raises(SystemExit):
        p272._parser().parse_args(
            [
                "offline-verify",
                "--game-pk",
                "not-numeric",
                "--raw-response",
                str(FINAL_FIXTURE),
                "--observed-at-utc",
                OBSERVED_AT,
                "--output-root",
                "/tmp/unused",
            ]
        )


def test_capture_transport_failure_is_attempted_once_without_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = 0

    def fail_once(*args, **kwargs):
        nonlocal calls
        calls += 1
        raise urllib.error.URLError("offline test")

    monkeypatch.setattr(p272.urllib.request, "urlopen", fail_once)
    output_root = tmp_path / "bundle"
    with pytest.raises(p272.P272Error, match="retry is forbidden"):
        p272.capture(game_pk=822834, output_root=output_root)

    assert calls == 1
    assert not output_root.exists()


def test_capture_clock_runs_after_complete_response_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    read_completed = False
    raw = FINAL_FIXTURE.read_bytes()

    class FakeResponse:
        headers = {"Content-Type": "application/json;charset=UTF-8"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

        def getcode(self):
            return 200

        def read(self):
            nonlocal read_completed
            read_completed = True
            return raw

    def fake_urlopen(*args, **kwargs):
        return FakeResponse()

    def fake_clock() -> str:
        assert read_completed
        return OBSERVED_AT

    monkeypatch.setattr(p272.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(p272, "utc_now", fake_clock)

    observed_raw, observed_at = p272.fetch_official_response_once(822834)
    assert observed_raw == raw
    assert observed_at == OBSERVED_AT


def test_game_identity_validation_fails_closed() -> None:
    payload = fixture_payload()
    payload["gameData"]["game"]["pk"] = 999999
    with pytest.raises(p272.P272Error, match="identity mismatch"):
        p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)

    payload = fixture_payload()
    payload["gamePk"] = 999999
    with pytest.raises(p272.P272Error, match="Conflicting top-level"):
        p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)


def test_predeclared_alias_validates_identity_but_preserves_official_abbreviation() -> None:
    raw = ALIAS_FIXTURE.read_bytes()
    record = p272.build_observation_record(
        raw,
        825108,
        OBSERVED_AT,
        expected_away_team="DET",
        expected_home_team="ARI",
    )
    assert record["home_team"] == "AZ"

    with pytest.raises(p272.P272Error, match="identity mismatch"):
        p272.build_observation_record(
            raw,
            825108,
            OBSERVED_AT,
            expected_away_team="DET",
            expected_home_team="PHX",
        )


def test_unknown_optional_fields_remain_null() -> None:
    payload = fixture_payload()
    payload["gameData"]["status"].pop("reason", None)
    record = p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)
    assert record["status_reason"] is None

    payload["gameData"]["game"].pop("season")
    record = p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)
    assert record["season"] is None
    assert record["provenance_status"] == "INCOMPLETE"


def test_conflicting_status_team_and_score_evidence_fail_closed() -> None:
    payload = fixture_payload()
    payload["gameData"]["status"]["detailedState"] = "In Progress"
    with pytest.raises(p272.P272Error, match="detailed/coded"):
        p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)

    payload = fixture_payload()
    payload["liveData"]["boxscore"]["teams"]["away"]["team"]["id"] = 999
    with pytest.raises(p272.P272Error, match="team identity evidence"):
        p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)

    payload = fixture_payload()
    payload["gameData"]["teams"]["away"]["score"] = 99
    with pytest.raises(p272.P272Error, match="score evidence"):
        p272.build_observation_record(fixture_bytes(payload), 822834, OBSERVED_AT)


def test_atomic_write_publishes_complete_bytes_without_replace(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    target = tmp_path / "bundle" / "evidence.json"
    expected = b"immutable evidence\n"
    real_link = os.link
    linked = 0

    def observing_link(source, destination):
        nonlocal linked
        linked += 1
        assert Path(source).read_bytes() == expected
        assert not Path(destination).exists()
        return real_link(source, destination)

    monkeypatch.setattr(p272.os, "link", observing_link)
    assert p272._write_once_atomic(target, expected) is True
    assert p272._write_once_atomic(target, expected) is False
    assert target.read_bytes() == expected
    assert linked == 1
    assert list(target.parent.glob(".evidence.json.*.tmp")) == []


def test_differing_existing_bundle_is_rejected_without_overwrite(tmp_path: Path) -> None:
    output_root = tmp_path / "bundle"
    p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=output_root,
    )
    observation_path = output_root / p272.OBSERVATION_FILENAME
    observation_path.write_bytes(b'{"different":true}\n')

    with pytest.raises(p272.P272Error, match="write-once overwrite refused"):
        p272.offline_verify(
            raw_response=FINAL_FIXTURE,
            game_pk=822834,
            observed_at_utc=OBSERVED_AT,
            output_root=output_root,
        )
    assert observation_path.read_bytes() == b'{"different":true}\n'


def test_identical_existing_bundle_is_accepted_idempotently(tmp_path: Path) -> None:
    output_root = tmp_path / "bundle"
    first_record, first_state = p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=output_root,
    )
    first = bundle_bytes(output_root)
    second_record, second_state = p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=output_root,
    )

    assert first_state == "CREATED"
    assert second_state == "VERIFIED_IDENTICAL"
    assert first_record == second_record
    assert first == bundle_bytes(output_root)


def test_two_run_offline_bundles_are_byte_identical_and_lossless(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_record, _ = p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=first_root,
    )
    second_record, _ = p272.offline_verify(
        raw_response=FINAL_FIXTURE,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=second_root,
    )

    first = bundle_bytes(first_root)
    second = bundle_bytes(second_root)
    assert first_record == second_record
    assert first == second
    assert set(first) == {
        p272.CHECKSUM_FILENAME,
        p272.OBSERVATION_FILENAME,
        p272.SOURCE_INDEX_FILENAME,
        "raw/mlb_2026_822834.feed.live.json",
    }
    assert first["raw/mlb_2026_822834.feed.live.json"] == FINAL_FIXTURE.read_bytes()

    checksum_lines = first[p272.CHECKSUM_FILENAME].decode("utf-8").splitlines()
    assert checksum_lines == sorted(checksum_lines, key=lambda line: line.split("  ", 1)[1])
    for line in checksum_lines:
        digest, relative_path = line.split("  ", 1)
        assert digest == p272.sha256_bytes(first[relative_path])


def test_file_mtime_is_excluded_from_all_logical_fingerprints(tmp_path: Path) -> None:
    first_raw = tmp_path / "first.raw.json"
    second_raw = tmp_path / "second.raw.json"
    raw = FINAL_FIXTURE.read_bytes()
    first_raw.write_bytes(raw)
    second_raw.write_bytes(raw)
    os.utime(first_raw, (1, 1))
    os.utime(second_raw, (2_000_000_000, 2_000_000_000))

    first, _ = p272.offline_verify(
        raw_response=first_raw,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=tmp_path / "first-bundle",
    )
    second, _ = p272.offline_verify(
        raw_response=second_raw,
        game_pk=822834,
        observed_at_utc=OBSERVED_AT,
        output_root=tmp_path / "second-bundle",
    )
    assert first["source_fingerprint"] == second["source_fingerprint"]
    assert first["record_fingerprint"] == second["record_fingerprint"]


def test_offline_cli_has_exact_two_modes_and_is_deterministic(
    capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    parser = p272._parser()
    subparser_action = next(
        action for action in parser._actions if isinstance(action, p272.argparse._SubParsersAction)
    )
    assert set(subparser_action.choices) == {"capture", "offline-verify"}

    output_root = tmp_path / "cli-bundle"
    exit_code = p272.main(
        [
            "offline-verify",
            "--game-pk",
            "822834",
            "--raw-response",
            str(FINAL_FIXTURE),
            "--observed-at-utc",
            OBSERVED_AT,
            "--output-root",
            str(output_root),
        ]
    )
    result = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert result["mode"] == "offline-verify"
    assert result["bundle_state"] == "CREATED"
    assert result["source_observed_at_utc"] == OBSERVED_AT


def test_observation_schema_is_exact_and_fingerprints_are_content_sensitive() -> None:
    raw = FINAL_FIXTURE.read_bytes()
    first = p272.build_observation_record(raw, 822834, OBSERVED_AT)
    second = p272.build_observation_record(raw, 822834, "2026-07-13T03:00:01Z")
    assert set(first) == p272.OBSERVATION_FIELDS
    assert first["source_fingerprint"] != second["source_fingerprint"]
    assert first["record_fingerprint"] != second["record_fingerprint"]

    tampered = copy.deepcopy(first)
    tampered["away_score"] += 1
    with pytest.raises(p272.P272Error, match="record_fingerprint"):
        p272.validate_observation_record(tampered)
