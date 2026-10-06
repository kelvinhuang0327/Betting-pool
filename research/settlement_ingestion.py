from __future__ import annotations

import copy
import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .config import ensure_research_dirs
from .daily_run_registry import DailyRunRegistry
from .insight_engine import InsightEngine
from .postmortem_engine import PostmortemEngine
from .roi_tracker import ROITracker
from .skip_day_diagnostics import SkipDayDiagnostics
from .skip_day_policy import ACTIVE_DAY, PARTIAL_DAY, SKIPPED_DAY, classify_day
from .trade_journal import TradeJournal, TradeRecord
from .trigger_engine import TriggerEngine
from .utils import load_json, save_json, utc_now_iso


@dataclass
class SettlementInput:
    game_id: str
    result: str
    settlement_time: str
    final_score: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def _parse_timestamp(value: str) -> datetime:
    raw = str(value).strip().replace("Z", "+00:00")
    return datetime.fromisoformat(raw).astimezone(timezone.utc)


def _settlement_date(value: str) -> str:
    return _parse_timestamp(value).date().isoformat()


def _safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except Exception:
        return default


def _normalize_game_result(value: Any) -> str:
    raw = str(value or "").strip().lower()
    aliases = {
        "home_win": "home_win",
        "home": "home_win",
        "home_win ": "home_win",
        "away_win": "away_win",
        "away": "away_win",
    }
    if raw in aliases:
        return aliases[raw]
    raise ValueError(f"Unsupported result value: {value!r}")


def _load_json_records(path: Path) -> List[Dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        for key in ("settlements", "rows", "data", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
        if "game_id" in payload and "result" in payload:
            return [payload]
    raise ValueError(f"Unsupported JSON settlement payload structure: {path}")


def _load_csv_records(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return [dict(row) for row in reader]


def load_settlement_inputs(path: Path) -> List[SettlementInput]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        rows = _load_json_records(path)
    elif suffix == ".csv":
        rows = _load_csv_records(path)
    else:
        raise ValueError(f"Unsupported settlement input format: {path.suffix}")

    settlements: List[SettlementInput] = []
    for row in rows:
        game_id = str(row.get("game_id", "")).strip()
        if not game_id:
            raise ValueError("Each settlement row must include game_id")
        result = _normalize_game_result(row.get("result"))
        settlement_time = str(row.get("settlement_time", "")).strip()
        if not settlement_time:
            raise ValueError(f"Settlement row for {game_id} is missing settlement_time")
        final_score = row.get("final_score")
        settlements.append(
            SettlementInput(
                game_id=game_id,
                result=result,
                settlement_time=settlement_time,
                final_score=str(final_score).strip() if final_score not in (None, "") else None,
                raw=row,
            )
        )
    return settlements


def _prediction_rows(rows: Iterable[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for row in rows:
        if row.get("event_type") != "prediction":
            continue
        game_id = str(row.get("game_id", "")).strip()
        if not game_id:
            continue
        grouped.setdefault(game_id, []).append(row)
    for game_id in grouped:
        grouped[game_id] = sorted(
            grouped[game_id],
            key=lambda row: (
                str(row.get("timestamp", "")),
                str(row.get("event_id", "")),
            ),
        )
    return grouped


def _latest_active_prediction(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not rows:
        return None
    active_rows = [row for row in rows if str(row.get("decision", "PASS")).upper() == "BET"]
    candidates = active_rows if active_rows else rows
    return candidates[-1]


def _existing_settlement_games(rows: Iterable[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    existing: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if row.get("event_type") != "settlement":
            continue
        game_id = str(row.get("game_id", "")).strip()
        if not game_id:
            continue
        existing[game_id] = row
    return existing


def _prediction_side(prediction: Dict[str, Any]) -> Optional[str]:
    metadata = prediction.get("metadata") or {}
    if isinstance(metadata, dict):
        side = metadata.get("recommended_side")
        if side in {"home", "away"}:
            return str(side)
    side = prediction.get("recommended_side")
    if side in {"home", "away"}:
        return str(side)
    return None


def _prediction_odds(prediction: Dict[str, Any], side: str) -> Optional[float]:
    odds = prediction.get("odds")
    if isinstance(odds, dict):
        keys = (
            ("home", ("home_ml", "home_moneyline", "moneyline_home", "home_odds")),
            ("away", ("away_ml", "away_moneyline", "moneyline_away", "away_odds")),
        )
        for key_side, key_names in keys:
            if key_side != side:
                continue
            for key in key_names:
                value = odds.get(key)
                parsed = _safe_float(value)
                if parsed is not None:
                    return parsed
        for value in odds.values():
            parsed = _safe_float(value)
            if parsed is not None:
                return parsed
    return _safe_float(odds)


def _moneyline_profit(stake: float, odds: float) -> float:
    if stake <= 0:
        return 0.0
    if odds < 0:
        return stake * (100.0 / abs(odds))
    if odds > 0:
        return stake * (odds / 100.0)
    return 0.0


def _build_settlement_record(
    prediction: Dict[str, Any],
    settlement: SettlementInput,
) -> TradeRecord:
    side = _prediction_side(prediction)
    if side not in {"home", "away"}:
        raise ValueError(f"Prediction {prediction.get('event_id')} is missing a bet side")

    stake = _safe_float(prediction.get("stake"), 0.0) or 0.0
    if stake <= 0:
        raise ValueError(f"Prediction {prediction.get('event_id')} has no active stake")

    odds_value = _prediction_odds(prediction, side)
    if odds_value is None:
        raise ValueError(f"Prediction {prediction.get('event_id')} is missing odds for side {side}")

    actual_side = "home" if settlement.result == "home_win" else "away"
    is_win = side == actual_side
    pnl = _moneyline_profit(stake, odds_value) if is_win else -stake
    roi = pnl / stake if stake else 0.0

    metadata = copy.deepcopy(prediction.get("metadata") or {})
    if not isinstance(metadata, dict):
        metadata = {}
    metadata.update(
        {
            "settlement_result": settlement.result,
            "final_score": settlement.final_score,
            "prediction_event_id": prediction.get("event_id"),
            "settlement_source": "research_settlement_ingestion",
        }
    )

    return TradeRecord(
        event_id=f"{prediction.get('event_id', settlement.game_id)}:settlement",
        timestamp=settlement.settlement_time,
        game_id=str(prediction.get("game_id", settlement.game_id)),
        league=str(prediction.get("league", "UNK")),
        regime=str(prediction.get("regime", "unknown")),
        predicted_prob=float(prediction.get("predicted_prob") or 0.0),
        market_prob=_safe_float(prediction.get("market_prob")),
        edge=_safe_float(prediction.get("edge")),
        decision=str(prediction.get("decision", "PASS")),
        stake=stake,
        odds=copy.deepcopy(prediction.get("odds")) if isinstance(prediction.get("odds"), dict) else None,
        result="win" if is_win else "loss",
        pnl=round(pnl, 4),
        roi=round(roi, 4),
        clv=_safe_float(prediction.get("clv")),
        execution_mode=str(prediction.get("execution_mode", "PAPER_ONLY")),
        event_type="settlement",
        metadata=metadata,
    )


class SettlementIngestionEngine:
    def __init__(self, base_dir: Optional[str] = None, pending_after_hours: float = 24.0):
        self.paths = ensure_research_dirs(base_dir)
        self.pending_after_hours = float(pending_after_hours)
        self.trade_journal = TradeJournal(base_dir)
        self.roi_tracker = ROITracker(base_dir)
        self.trigger_engine = TriggerEngine(base_dir)
        self.postmortem_engine = PostmortemEngine(base_dir)
        self.insight_engine = InsightEngine(base_dir)
        self.daily_run_registry = DailyRunRegistry(base_dir)
        self.skip_day_diagnostics = SkipDayDiagnostics(base_dir)

    @property
    def trigger_index_path(self) -> Path:
        return self.paths["trigger_index"]

    @property
    def pending_path(self) -> Path:
        return self.paths["pending_settlements"]

    @property
    def daily_registry_path(self) -> Path:
        return self.paths["daily_run_registry"]

    @property
    def missed_prediction_days_path(self) -> Path:
        return self.paths["missed_prediction_days"]

    def ingest_file(self, input_path: str) -> dict[str, Any]:
        path = Path(input_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        settlements = load_settlement_inputs(path)
        return self.ingest(settlements, source_path=str(path))

    def ingest(self, settlements: List[SettlementInput], source_path: Optional[str] = None) -> dict[str, Any]:
        initial_rows = self.trade_journal.load()
        predictions_by_game = _prediction_rows(initial_rows)
        existing_settlements = _existing_settlement_games(initial_rows)
        day_stats: dict[str, dict[str, Any]] = {}

        summary = {
            "active": True,
            "captured": True,
            "source_path": source_path,
            "input_count": len(settlements),
            "settled_count": 0,
            "skipped_existing_settlement": 0,
            "skipped_missing_prediction": 0,
            "skipped_inactive_prediction": 0,
            "skipped_missing_odds": 0,
            "invalid_rows": 0,
            "trigger_count": 0,
            "postmortem_reports": [],
        }

        for settlement in settlements:
            settlement_day = _settlement_date(settlement.settlement_time)
            stat = day_stats.setdefault(
                settlement_day,
                {
                    "games_found": 0,
                    "prediction_events": 0,
                    "results_ingested": 0,
                    "settled_count": 0,
                    "missing_prediction": 0,
                    "inactive_prediction": 0,
                    "existing_settlement": 0,
                    "invalid_rows": 0,
                },
            )
            stat["games_found"] += 1
            stat["results_ingested"] += 1
            if settlement.game_id in existing_settlements:
                summary["skipped_existing_settlement"] += 1
                stat["existing_settlement"] += 1
                continue

            game_predictions = predictions_by_game.get(settlement.game_id, [])
            if game_predictions:
                stat["prediction_events"] += 1

            prediction = _latest_active_prediction(game_predictions)
            if prediction is None:
                summary["skipped_missing_prediction"] += 1
                stat["missing_prediction"] += 1
                continue

            if str(prediction.get("decision", "PASS")).upper() != "BET":
                summary["skipped_inactive_prediction"] += 1
                stat["inactive_prediction"] += 1
                continue

            try:
                settlement_record = _build_settlement_record(prediction, settlement)
            except Exception as exc:
                message = str(exc)
                if "odds" in message.lower():
                    summary["skipped_missing_odds"] += 1
                else:
                    summary["invalid_rows"] += 1
                    stat["invalid_rows"] += 1
                continue

            self.trade_journal.append(settlement_record)
            existing_settlements[settlement.game_id] = settlement_record.to_dict()
            summary["settled_count"] += 1
            stat["settled_count"] += 1

        roi_summary = self.roi_tracker.rebuild()
        rows = self.trade_journal.load()
        triggers = self.trigger_engine.evaluate(roi_summary)
        summary["trigger_count"] = len(triggers)

        trigger_index_entries = self._update_trigger_index(triggers, roi_summary)
        postmortem_paths: List[str] = []
        for trigger in triggers:
            report_path = self.postmortem_engine.generate(roi_summary, rows, trigger)
            postmortem_paths.append(str(report_path))
            self._append_trigger_index_entry(trigger, report_path)
        summary["postmortem_reports"] = postmortem_paths
        self.insight_engine.generate(roi_summary, rows)

        registry_events: List[Dict[str, Any]] = []
        for settlement_day, stat in sorted(day_stats.items()):
            all_existing = (
                stat["existing_settlement"] == stat["games_found"]
                and stat["settled_count"] == 0
                and stat["missing_prediction"] == 0
                and stat["inactive_prediction"] == 0
                and stat["invalid_rows"] == 0
            )
            if all_existing:
                continue

            status_info = classify_day(
                system_online=stat["prediction_events"] > 0,
                daily_pipeline_ran=stat["prediction_events"] > 0,
                prediction_count=stat["prediction_events"],
                game_count_detected=stat["games_found"],
                research_mode=True,
                reason=(
                    "predictions_present"
                    if stat["prediction_events"] >= stat["games_found"] and stat["prediction_events"] > 0
                    else "incomplete_coverage"
                    if stat["prediction_events"] > 0
                    else "system_offline"
                ),
            )
            snapshot = self.daily_run_registry.record_day(
                date=settlement_day,
                system_online=bool(status_info["system_online"]),
                daily_pipeline_ran=bool(status_info["daily_pipeline_ran"]),
                prediction_count=int(status_info["prediction_count"]),
                game_count_detected=int(status_info["game_count_detected"]),
                research_mode=bool(status_info["research_mode"]),
                reason=str(status_info.get("reason") or ""),
                source="settlement_ingestion",
                mode="snapshot",
            )
            registry_events.append(snapshot)
            if snapshot.get("status") in {SKIPPED_DAY, PARTIAL_DAY}:
                self.skip_day_diagnostics.record_day(
                    date=settlement_day,
                    status=str(snapshot.get("status")),
                    reason=str(snapshot.get("reason") or ""),
                    games_found=int(snapshot.get("game_count_detected") or 0),
                    prediction_events=int(snapshot.get("prediction_count") or 0),
                    results_ingested=bool(stat["results_ingested"]),
                    notes=(
                        "no_prediction_events_detected"
                        if snapshot.get("status") == SKIPPED_DAY
                        else "partial_coverage_or_interrupted_pipeline"
                    ),
                )

        pending_summary = self._update_pending_settlements(rows)
        summary["pending_count"] = pending_summary["pending_count"]
        summary["roi_path"] = str(self.roi_tracker.roi_path)
        summary["ledger_path"] = str(self.trade_journal.ledger_path)
        summary["trigger_index_path"] = str(self.trigger_index_path)
        summary["pending_path"] = str(self.pending_path)
        summary["daily_registry_path"] = str(self.daily_registry_path)
        summary["missed_prediction_days_path"] = str(self.missed_prediction_days_path)
        summary["daily_registry_summary"] = self.daily_run_registry.summary()
        summary["skip_day_diagnostics_summary"] = self.skip_day_diagnostics.summary()
        summary["registry_events"] = registry_events
        summary["updated_at"] = utc_now_iso()
        summary["trigger_index_entries"] = self._load_trigger_index()
        return summary

    def _load_trigger_index(self) -> List[Dict[str, Any]]:
        payload = load_json(self.trigger_index_path, [])
        if isinstance(payload, list):
            return [row for row in payload if isinstance(row, dict)]
        return []

    def _append_trigger_index_entry(self, trigger: Dict[str, Any], report_path: Path) -> None:
        entries = self._load_trigger_index()
        signature = str(trigger.get("signature") or f"{trigger.get('bucket')}:{trigger.get('period')}:{trigger.get('roi')}")
        if any(str(row.get("signature")) == signature for row in entries if isinstance(row, dict)):
            return
        entries.append(
            {
                "timestamp": trigger.get("timestamp", utc_now_iso()),
                "trigger_type": trigger.get("bucket", "unknown"),
                "roi": round(float(trigger.get("roi") or 0.0), 4),
                "report_path": str(report_path),
                "period": trigger.get("period"),
                "signature": signature,
            }
        )
        save_json(self.trigger_index_path, entries)

    def _update_trigger_index(self, triggers: List[Dict[str, Any]], roi_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        existing = self._load_trigger_index()
        if not triggers and existing:
            return existing
        if not triggers and not existing:
            save_json(self.trigger_index_path, [])
            return []
        return existing

    def _update_pending_settlements(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        predictions = _prediction_rows(rows)
        settled_games = set(_existing_settlement_games(rows).keys())
        now = datetime.now(timezone.utc)
        pending: List[Dict[str, Any]] = []
        for game_id, game_rows in predictions.items():
            if game_id in settled_games:
                continue
            prediction = _latest_active_prediction(game_rows)
            if prediction is None:
                continue
            if str(prediction.get("decision", "PASS")).upper() != "BET":
                continue
            timestamp = str(prediction.get("timestamp", "")).strip()
            if not timestamp:
                continue
            try:
                age_hours = (now - _parse_timestamp(timestamp)).total_seconds() / 3600.0
            except Exception:
                continue
            if age_hours < self.pending_after_hours:
                continue
            pending.append(
                {
                    "game_id": game_id,
                    "prediction_event_id": prediction.get("event_id"),
                    "prediction_timestamp": timestamp,
                    "age_hours": round(age_hours, 2),
                    "decision": prediction.get("decision"),
                    "regime": prediction.get("regime"),
                    "execution_mode": prediction.get("execution_mode"),
                }
            )
        pending.sort(key=lambda row: (str(row.get("prediction_timestamp", "")), str(row.get("game_id", ""))))
        summary = {
            "updated_at": utc_now_iso(),
            "threshold_hours": float(self.pending_after_hours),
            "pending_count": len(pending),
            "entries": pending,
        }
        save_json(self.pending_path, summary)
        return summary


def ingest_settlements(input_path: str, base_dir: Optional[str] = None, pending_after_hours: float = 24.0) -> dict[str, Any]:
    engine = SettlementIngestionEngine(base_dir=base_dir, pending_after_hours=pending_after_hours)
    return engine.ingest_file(input_path)
