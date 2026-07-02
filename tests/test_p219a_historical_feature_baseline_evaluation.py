from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "build_historical_feature_baseline_evaluation.py"


def _load_script_module():
    spec = importlib.util.spec_from_file_location("p219a_script", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_payload_computes_deterministic_historical_baselines(tmp_path, monkeypatch):
    script = _load_script_module()
    source_csv = tmp_path / "p218.csv"
    source_json = tmp_path / "p218.json"
    source_md = tmp_path / "p218.md"

    source_csv.write_text(
        "\n".join(
            [
                "source_row_id,game_date,game_pk,home_team,away_team,inning,inning_topbot,pitcher,batter,pitch_type,event_category,is_in_play,is_strike_like,is_ball_like,release_speed,release_speed_bucket,zone,zone_bucket",
                "1,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,FF,strike_like,False,True,False,94.2,90_to_94_9,5,in_zone",
                "2,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,FF,strike_like,False,True,False,94.5,90_to_94_9,8,in_zone",
                "3,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,CH,ball_like,False,False,True,87.8,85_to_89_9,13,out_of_zone",
                "4,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,CH,in_play_out,True,False,False,87.9,85_to_89_9,4,in_zone",
                "5,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,SI,in_play_hit,True,False,False,95.0,95_plus,7,in_zone",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    source_json.write_text(
        json.dumps(
            {
                "task": "P218-A Historical Sample Feature Table Prototype",
                "status": "PASS_P216A_P217A_ARTIFACT_ONLY_HISTORICAL_SAMPLE_FEATURE_TABLE_PROTOTYPE",
                "disclaimer": "Historical sample feature table prototype only. Not live predictions, not betting advice.",
                "historical_only_disclaimer": "Historical sample feature table prototype only. Not live predictions, not betting advice.",
                "row_count": 5,
                "column_count": 18,
                "feature_columns": ["source_row_id", "pitch_type", "event_category"],
                "limitations": [
                    "Feature rows are derived only from the fixed P216/P217 artifact snapshots and do not refresh upstream data."
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    source_md.write_text(
        "# P218\n\nHistorical sample feature table prototype only. Not live predictions, not betting advice.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(script, "ROOT", tmp_path)
    monkeypatch.setattr(script, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(script, "SOURCE_CSV", source_csv)
    monkeypatch.setattr(script, "SOURCE_JSON", source_json)
    monkeypatch.setattr(script, "SOURCE_MD", source_md)
    monkeypatch.setattr(
        script,
        "SOURCE_REQUIRED_HASHES",
        {
            "p218.csv": script._sha256(source_csv),
            "p218.json": script._sha256(source_json),
            "p218.md": script._sha256(source_md),
        },
    )

    payload = script.build_payload()

    assert payload["disclaimer"] == script.DISCLAIMER
    assert payload["historical_only_disclaimer"] == script.DISCLAIMER
    assert payload["row_count"] == 5
    assert payload["column_count"] == len(script.OUTPUT_COLUMNS)
    assert payload["source_artifacts"] == ["p218.csv", "p218.json", "p218.md"]
    assert payload["source_summary"]["p218_markdown_mentions_disclaimer"] is True
    assert payload["target_definition"]["class_support"] == [
        {"value": "strike_like", "count": 2, "fraction": 0.4},
        {"value": "ball_like", "count": 1, "fraction": 0.2},
        {"value": "in_play_hit", "count": 1, "fraction": 0.2},
        {"value": "in_play_out", "count": 1, "fraction": 0.2},
    ]

    baseline_a = payload["baseline_definitions"]["baseline_a_global_majority"]
    baseline_b = payload["baseline_definitions"]["baseline_b_pitch_type_majority_with_global_fallback"]
    metrics_a = payload["metric_summary"]["baseline_a_global_majority"]
    metrics_b = payload["metric_summary"]["baseline_b_pitch_type_majority_with_global_fallback"]

    assert baseline_a["resolved_prediction"] == "strike_like"
    assert baseline_b["global_fallback_prediction"] == "strike_like"
    assert baseline_b["pitch_type_resolution_table"] == [
        {
            "pitch_type": "CH",
            "support": 2,
            "event_category_distribution": [
                {"value": "ball_like", "count": 1, "fraction": 0.5},
                {"value": "in_play_out", "count": 1, "fraction": 0.5},
            ],
            "resolved_prediction": "strike_like",
            "prediction_source": "global_fallback_due_to_tie",
            "fallback_to_global_majority": True,
        },
        {
            "pitch_type": "FF",
            "support": 2,
            "event_category_distribution": [
                {"value": "strike_like", "count": 2, "fraction": 1.0},
            ],
            "resolved_prediction": "strike_like",
            "prediction_source": "pitch_type_majority",
            "fallback_to_global_majority": False,
        },
        {
            "pitch_type": "SI",
            "support": 1,
            "event_category_distribution": [
                {"value": "in_play_hit", "count": 1, "fraction": 1.0},
            ],
            "resolved_prediction": "in_play_hit",
            "prediction_source": "pitch_type_majority",
            "fallback_to_global_majority": False,
        },
    ]
    assert metrics_a["accuracy"] == 0.4
    assert metrics_a["correct_count"] == 2
    assert metrics_a["coverage_fraction"] == 1.0
    assert metrics_b["accuracy"] == 0.6
    assert metrics_b["correct_count"] == 3
    assert metrics_b["coverage_rows"] == 3
    assert metrics_b["coverage_fraction"] == 0.6
    assert metrics_b["confusion_matrix"] == {
        "ball_like": {
            "ball_like": 0,
            "in_play_hit": 0,
            "in_play_out": 0,
            "strike_like": 1,
        },
        "in_play_hit": {
            "ball_like": 0,
            "in_play_hit": 1,
            "in_play_out": 0,
            "strike_like": 0,
        },
        "in_play_out": {
            "ball_like": 0,
            "in_play_hit": 0,
            "in_play_out": 0,
            "strike_like": 1,
        },
        "strike_like": {
            "ball_like": 0,
            "in_play_hit": 0,
            "in_play_out": 0,
            "strike_like": 2,
        },
    }

    assert payload["records"][2]["baseline_b_prediction_source"] == "global_fallback_due_to_tie"
    assert payload["records"][4]["baseline_b_pitch_type_prediction"] == "in_play_hit"
    assert "do not train or score a production model" in payload["limitations"][1]
    assert "No betting advice claim." in payload["prohibited_claims"]


def test_main_writes_deterministic_outputs(tmp_path, monkeypatch, capsys):
    script = _load_script_module()
    source_csv = tmp_path / "p218.csv"
    source_json = tmp_path / "p218.json"
    source_md = tmp_path / "p218.md"
    out_csv = tmp_path / "p219.csv"
    out_json = tmp_path / "p219.json"
    out_md = tmp_path / "p219.md"

    source_csv.write_text(
        "\n".join(
            [
                "source_row_id,game_date,game_pk,home_team,away_team,inning,inning_topbot,pitcher,batter,pitch_type,event_category,is_in_play,is_strike_like,is_ball_like,release_speed,release_speed_bucket,zone,zone_bucket",
                "1,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,FF,strike_like,False,True,False,94.2,90_to_94_9,5,in_zone",
                "2,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,SI,in_play_hit,True,False,False,95.0,95_plus,7,in_zone",
                "3,2024-04-01,1,SEA,CLE,1,Top,Pitcher A,10,FF,strike_like,False,True,False,94.7,90_to_94_9,6,in_zone",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    source_json.write_text(
        json.dumps(
            {
                "task": "P218-A Historical Sample Feature Table Prototype",
                "status": "PASS_P216A_P217A_ARTIFACT_ONLY_HISTORICAL_SAMPLE_FEATURE_TABLE_PROTOTYPE",
                "disclaimer": "Historical sample feature table prototype only. Not live predictions, not betting advice.",
                "historical_only_disclaimer": "Historical sample feature table prototype only. Not live predictions, not betting advice.",
                "row_count": 3,
                "column_count": 18,
                "feature_columns": ["source_row_id", "pitch_type", "event_category"],
                "limitations": [],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    source_md.write_text(
        "# P218\n\nHistorical sample feature table prototype only. Not live predictions, not betting advice.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(script, "ROOT", tmp_path)
    monkeypatch.setattr(script, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(script, "SOURCE_CSV", source_csv)
    monkeypatch.setattr(script, "SOURCE_JSON", source_json)
    monkeypatch.setattr(script, "SOURCE_MD", source_md)
    monkeypatch.setattr(script, "OUT_CSV", out_csv)
    monkeypatch.setattr(script, "OUT_JSON", out_json)
    monkeypatch.setattr(script, "OUT_MD", out_md)
    monkeypatch.setattr(
        script,
        "SOURCE_REQUIRED_HASHES",
        {
            "p218.csv": script._sha256(source_csv),
            "p218.json": script._sha256(source_json),
            "p218.md": script._sha256(source_md),
        },
    )

    assert script.main() == 0
    first_csv = out_csv.read_text(encoding="utf-8")
    first_json = out_json.read_text(encoding="utf-8")
    first_md = out_md.read_text(encoding="utf-8")

    assert script.main() == 0
    assert out_csv.read_text(encoding="utf-8") == first_csv
    assert out_json.read_text(encoding="utf-8") == first_json
    assert out_md.read_text(encoding="utf-8") == first_md

    assert script.DISCLAIMER in first_json
    assert script.DISCLAIMER in first_md

    payload = json.loads(first_json)
    assert payload["target_definition"]["name"] == "event_category"
    assert payload["metric_summary"]["baseline_a_global_majority"]["accuracy"] == 0.666667
    assert payload["metric_summary"]["baseline_b_pitch_type_majority_with_global_fallback"]["accuracy"] == 1.0

    with out_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == script.OUTPUT_COLUMNS
        rows = list(reader)
    assert rows[0]["baseline_a_global_prediction"] == "strike_like"
    assert rows[1]["baseline_b_pitch_type_prediction"] == "in_play_hit"
    assert rows[2]["baseline_a_global_prediction"] == "strike_like"

    captured = capsys.readouterr()
    assert "P219-A HISTORICAL FEATURE BASELINE EVALUATION PROTOTYPE PASS" in captured.out
