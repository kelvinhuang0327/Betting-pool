from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Optional, Union


RESEARCH_MODE_ENV = "RESEARCH_MODE"
RESEARCH_DIR_ENV = "RESEARCH_DIR"


def is_research_mode_enabled() -> bool:
    value = os.getenv(RESEARCH_MODE_ENV, "false").strip().lower()
    return value in {"1", "true", "yes", "on"}


def research_root() -> Path:
    raw = os.getenv(RESEARCH_DIR_ENV)
    if raw:
        return Path(raw).expanduser().resolve()
    return Path(__file__).resolve().parent


def research_paths(base_dir: Optional[Union[str, os.PathLike[str]]] = None) -> Dict[str, Path]:
    root = Path(base_dir).expanduser().resolve() if base_dir else research_root()
    return {
        "root": root,
        "ledger": root / "trade_ledger.jsonl",
        "roi": root / "roi_tracking.json",
        "triggers": root / "triggers_log.json",
        "trigger_index": root / "trigger_index.json",
        "pending_settlements": root / "pending_settlements.json",
        "daily_run_registry": root / "daily_run_registry.jsonl",
        "missed_prediction_days": root / "missed_prediction_days.json",
        "postmortem_dir": root / "postmortem_reports",
        "insights_dir": root / "strategy_insights",
        "latest_insights": root / "strategy_insights" / "latest.json",
    }


def ensure_research_dirs(base_dir: Optional[Union[str, os.PathLike[str]]] = None) -> Dict[str, Path]:
    paths = research_paths(base_dir)
    paths["root"].mkdir(parents=True, exist_ok=True)
    paths["postmortem_dir"].mkdir(parents=True, exist_ok=True)
    paths["insights_dir"].mkdir(parents=True, exist_ok=True)
    for key in ("ledger", "roi", "triggers", "trigger_index", "pending_settlements", "daily_run_registry", "missed_prediction_days", "latest_insights"):
        path = paths[key]
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            if key in {"triggers", "trigger_index"}:
                path.write_text("[]\n", encoding="utf-8")
            elif key == "daily_run_registry":
                path.write_text("", encoding="utf-8")
            elif key == "pending_settlements":
                path.write_text("{}\n", encoding="utf-8")
            elif key == "missed_prediction_days":
                path.write_text("{}\n", encoding="utf-8")
            elif path.suffix == ".json":
                path.write_text("{}\n", encoding="utf-8")
            else:
                path.write_text("", encoding="utf-8")
    return paths
