from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from wbc_backend.config.settings import AppConfig
from wbc_backend.strategy.live_retrainer import GameResult, run_retraining_cycle


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def load_latest_prediction_record(
    *,
    config: AppConfig,
    game_id: str,
) -> dict[str, Any] | None:
    rows = _read_jsonl(Path(config.sources.prediction_registry_jsonl))
    matches = [row for row in rows if str(row.get("game_id")) == str(game_id)]
    if not matches:
        return None
    return matches[-1]


def extract_sub_model_predictions(record: dict[str, Any]) -> dict[str, float]:
    sub_models = record.get("prediction", {}).get("sub_model_results", [])
    predictions: dict[str, float] = {}
    for sub_model in sub_models:
        name = str(sub_model.get("model_name") or "").strip()
        home_win_prob = sub_model.get("home_win_prob")
        if not name or not isinstance(home_win_prob, (int, float)):
            continue
        predictions[name] = float(home_win_prob)
    return predictions


def _binary_log_loss(prob: float, actual: int) -> float:
    clipped = min(max(float(prob), 1e-6), 1.0 - 1e-6)
    return -(actual * math.log(clipped) + (1 - actual) * math.log(1 - clipped))


def _round_dict(values: dict[str, float], digits: int = 4) -> dict[str, float]:
    return {key: round(float(value), digits) for key, value in values.items()}


def _build_prediction_summary(record: dict[str, Any]) -> dict[str, Any]:
    prediction = record.get("prediction", {})
    game_output = record.get("game_output", {})
    verification = record.get("verification", {})
    decision_report = record.get("decision_report", {})
    return {
        "recorded_at_utc": record.get("recorded_at_utc"),
        "predicted_home_win_prob": round(float(prediction.get("home_win_prob", 0.0)), 4),
        "predicted_away_win_prob": round(float(prediction.get("away_win_prob", 0.0)), 4),
        "predicted_home_score": round(float(game_output.get("predicted_home_score", 0.0)), 2),
        "predicted_away_score": round(float(game_output.get("predicted_away_score", 0.0)), 2),
        "confidence_index": round(float(game_output.get("confidence_index", 0.0)), 4),
        "verification_status": verification.get("status"),
        "used_fallback_lineup": bool(verification.get("used_fallback_lineup", False)),
        "decision": decision_report.get("decision"),
        "decision_reasoning": decision_report.get("reasoning", []),
    }


def _build_evaluation(
    *,
    prediction_record: dict[str, Any],
    home_score: int,
    away_score: int,
) -> dict[str, Any]:
    game_output = prediction_record.get("game_output", {})
    prediction = prediction_record.get("prediction", {})
    actual_home_win = 1 if home_score > away_score else 0
    pred_home_win_prob = float(prediction.get("home_win_prob", 0.0))
    pred_home_score = float(game_output.get("predicted_home_score", 0.0))
    pred_away_score = float(game_output.get("predicted_away_score", 0.0))
    predicted_total = pred_home_score + pred_away_score
    actual_total = home_score + away_score
    predicted_home_win = pred_home_win_prob >= 0.5

    return {
        "predicted_home_win": predicted_home_win,
        "winner_correct": predicted_home_win == bool(actual_home_win),
        "home_win_brier": round((pred_home_win_prob - actual_home_win) ** 2, 6),
        "home_win_log_loss": round(_binary_log_loss(pred_home_win_prob, actual_home_win), 6),
        "score_error_home_abs": round(abs(pred_home_score - home_score), 2),
        "score_error_away_abs": round(abs(pred_away_score - away_score), 2),
        "score_error_total_abs": round(abs(predicted_total - actual_total), 2),
        "actual_total_runs": actual_total,
        "predicted_total_runs": round(predicted_total, 2),
    }


def record_postgame_outcome(
    *,
    config: AppConfig,
    game_id: str,
    home_team: str,
    away_team: str,
    home_score: int,
    away_score: int,
    source_urls: list[str] | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    prediction_record = load_latest_prediction_record(config=config, game_id=game_id)
    learning_payload: dict[str, Any] = {
        "applied": False,
        "summary": "Prediction record unavailable; learning skipped.",
    }

    record: dict[str, Any] = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "game_id": game_id,
        "teams": {
            "home": home_team,
            "away": away_team,
        },
        "actual_result": {
            "home_score": int(home_score),
            "away_score": int(away_score),
            "home_win": bool(home_score > away_score),
            "total_runs": int(home_score + away_score),
        },
        "source_urls": source_urls or [],
        "notes": notes or [],
        "prediction_summary": None,
        "evaluation": None,
        "learning": learning_payload,
    }

    if prediction_record:
        record["prediction_summary"] = _build_prediction_summary(prediction_record)
        record["evaluation"] = _build_evaluation(
            prediction_record=prediction_record,
            home_score=home_score,
            away_score=away_score,
        )

        sub_model_predictions = extract_sub_model_predictions(prediction_record)
        if sub_model_predictions:
            game_result = GameResult(
                game_id=game_id,
                home_team=home_team,
                away_team=away_team,
                home_score=home_score,
                away_score=away_score,
                home_win=home_score > away_score,
                total_runs=home_score + away_score,
            )
            health_report = run_retraining_cycle(
                [game_result],
                [sub_model_predictions],
            )
            learning_payload = {
                "applied": True,
                "model_count": len(sub_model_predictions),
                "overall_health": health_report.overall_health,
                "summary": health_report.summary,
                "updated_weights": _round_dict(health_report.updated_weights),
                "retired_models": health_report.retired_models,
            }
        else:
            learning_payload = {
                "applied": False,
                "summary": "Prediction record found but sub-model probabilities missing; learning skipped.",
            }

    record["learning"] = learning_payload

    target = Path(config.sources.postgame_results_jsonl)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False))
        fh.write("\n")

    return record
