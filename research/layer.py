from __future__ import annotations

from typing import Any, Optional
from datetime import datetime, timezone

from .config import ensure_research_dirs, is_research_mode_enabled, research_paths
from .daily_run_registry import DailyRunRegistry
from .insight_engine import InsightEngine
from .postmortem_engine import PostmortemEngine
from .roi_tracker import ROITracker
from .trade_journal import TradeJournal, build_trade_record
from .trigger_engine import TriggerEngine


class ResearchLayer:
    def __init__(self, base_dir: Optional[str] = None, enabled: Optional[bool] = None):
        self.base_dir = base_dir
        self.enabled = is_research_mode_enabled() if enabled is None else bool(enabled)
        self.paths = research_paths(base_dir)
        self._ready = False
        self.trade_journal = None
        self.roi_tracker = None
        self.trigger_engine = None
        self.postmortem_engine = None
        self.insight_engine = None
        self.daily_run_registry = None

    def _ensure_ready(self) -> None:
        if self._ready:
            return
        self.paths = ensure_research_dirs(self.base_dir)
        self.trade_journal = TradeJournal(self.base_dir)
        self.roi_tracker = ROITracker(self.base_dir)
        self.trigger_engine = TriggerEngine(self.base_dir)
        self.postmortem_engine = PostmortemEngine(self.base_dir)
        self.insight_engine = InsightEngine(self.base_dir)
        self.daily_run_registry = DailyRunRegistry(self.base_dir)
        self._ready = True

    @staticmethod
    def _extract_game_date(record: Any, result: Any = None) -> str:
        candidates = [
            getattr(record, "game_time_utc", None) if record is not None else None,
            getattr(result, "game_time_utc", None) if result is not None else None,
        ]
        for candidate in candidates:
            if not candidate:
                continue
            raw = str(candidate).strip().replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(raw).astimezone(timezone.utc).date().isoformat()
            except Exception:
                continue
        return datetime.now(timezone.utc).date().isoformat()

    def capture(
        self,
        result: Any,
        record: Any = None,
        settlement: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        if not self.enabled:
            return {"active": False, "captured": False}

        self._ensure_ready()
        assert self.trade_journal and self.roi_tracker and self.trigger_engine and self.postmortem_engine and self.insight_engine and self.daily_run_registry

        prediction = self.trade_journal.append(build_trade_record(result, record=record, event_type="prediction"))
        game_date = self._extract_game_date(record, result)
        daily_snapshot = self.daily_run_registry.record_day(
            date=game_date,
            system_online=True,
            daily_pipeline_ran=True,
            prediction_count=1,
            game_count_detected=1,
            research_mode=True,
            reason="prediction_captured",
            source="research_layer_capture",
            mode="increment",
        )
        settlement_record = None
        if settlement is not None:
            settlement_record = self.trade_journal.append(build_trade_record(
                result,
                record=record,
                settlement=settlement,
                event_type="settlement",
            ))

        roi_summary = self.roi_tracker.rebuild()
        rows = self.trade_journal.load()
        triggers = self.trigger_engine.evaluate(roi_summary)
        postmortem_paths = []
        if triggers:
            for trigger in triggers:
                postmortem_paths.append(str(self.postmortem_engine.generate(roi_summary, rows, trigger)))
        self.insight_engine.generate(roi_summary, rows)

        return {
            "active": True,
            "captured": True,
            "prediction_event_id": prediction.event_id,
            "settlement_event_id": settlement_record.event_id if settlement_record else None,
            "triggers": triggers,
            "postmortem_reports": postmortem_paths,
            "insights_path": str(self.insight_engine.latest_path),
            "roi_path": str(self.roi_tracker.roi_path),
            "ledger_path": str(self.trade_journal.ledger_path),
            "daily_registry_path": str(self.daily_run_registry.registry_path),
            "daily_registry_snapshot": daily_snapshot,
        }


default_research_layer = ResearchLayer()


def capture(result: Any, record: Any = None, settlement: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return default_research_layer.capture(result, record=record, settlement=settlement)
