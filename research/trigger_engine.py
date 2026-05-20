from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from .config import ensure_research_dirs
from .utils import load_json, save_json, utc_now_iso


DEFAULT_TRIGGER_THRESHOLD = 0.05


class TriggerEngine:
    def __init__(self, base_dir: Optional[str] = None, threshold: float = DEFAULT_TRIGGER_THRESHOLD):
        self.paths = ensure_research_dirs(base_dir)
        self.threshold = float(threshold)

    @property
    def triggers_path(self) -> Path:
        return self.paths["triggers"]

    def _load(self) -> list[dict[str, Any]]:
        payload = load_json(self.triggers_path, [])
        return payload if isinstance(payload, list) else []

    def evaluate(self, roi_summary: dict[str, Any]) -> list[dict[str, Any]]:
        triggers: list[dict[str, Any]] = []
        existing = self._load()
        seen = {row.get("signature") for row in existing if isinstance(row, dict)}
        for bucket in ("daily", "weekly", "monthly"):
            for period_key, payload in (roi_summary.get(bucket) or {}).items():
                roi = float(payload.get("roi") or 0.0)
                if abs(roi) < self.threshold:
                    continue
                direction = "positive" if roi >= self.threshold else "negative"
                signature = f"{bucket}:{period_key}:{direction}:{round(roi, 4)}"
                if signature in seen:
                    continue
                event = {
                    "event_id": f"trigger:{bucket}:{period_key}:{utc_now_iso()}",
                    "timestamp": utc_now_iso(),
                    "bucket": bucket,
                    "period": period_key,
                    "roi": round(roi, 4),
                    "direction": direction,
                    "samples": int(payload.get("samples", 0)),
                    "signature": signature,
                }
                triggers.append(event)
                existing.append(event)
                seen.add(signature)
        if triggers:
            save_json(self.triggers_path, existing)
        return triggers
