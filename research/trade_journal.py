from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from .config import ensure_research_dirs, research_paths
from .utils import append_jsonl, load_jsonl, utc_now_iso


@dataclass
class TradeRecord:
    event_id: str
    timestamp: str
    game_id: str
    league: str
    regime: str
    predicted_prob: float
    market_prob: Optional[float]
    edge: Optional[float]
    decision: str
    stake: Optional[float]
    odds: Optional[dict[str, Any]]
    result: str
    pnl: Optional[float]
    roi: Optional[float]
    clv: Optional[float]
    execution_mode: str
    event_type: str = "prediction"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _as_dict(obj: Any) -> dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    return dict(getattr(obj, "__dict__", {}))


def infer_event_id(record: Any, decision: str, event_type: str = "prediction") -> str:
    game_id = str(getattr(record, "game_id", "UNK"))
    league = str(getattr(record, "league", getattr(record, "tournament", "UNK")))
    regime = str(getattr(record, "round_name", getattr(record, "regime", "")) or "unknown")
    return f"{game_id}:{league}:{regime}:{decision}:{event_type}"


def infer_regime(record: Any, result: Any = None) -> str:
    if record is not None:
        for attr in ("regime", "paper_regime", "round_name", "game_type"):
            value = getattr(record, attr, None)
            if value:
                return str(value)
    if result is not None:
        value = getattr(result, "paper_regime", None)
        if value:
            return str(value)
        value = getattr(result, "game_type", None)
        if value:
            return str(value)
    return "unknown"


def build_trade_record(
    result: Any,
    record: Any = None,
    settlement: Optional[dict[str, Any]] = None,
    event_type: str = "prediction",
) -> TradeRecord:
    game_id = str(getattr(record, "game_id", getattr(result, "game_id", "UNK")))
    league = str(getattr(record, "league", getattr(record, "tournament", getattr(result, "league", "UNK"))))
    regime = infer_regime(record, result)
    market_prob = getattr(record, "market_home_prob", None)
    market_prob = float(market_prob) if market_prob is not None else None
    home_prob = float(getattr(result, "home_win_prob", 0.5))
    recommended_side = str(getattr(result, "recommended_side", "pass"))
    decision = "BET" if recommended_side in {"home", "away"} and float(getattr(result, "recommended_kelly_fraction", 0.0)) > 0 else "PASS"
    settlement_payload = settlement or {}
    if recommended_side == "away":
        edge = (1.0 - home_prob) - (1.0 - market_prob) if market_prob is not None else None
    elif recommended_side == "home":
        edge = home_prob - market_prob if market_prob is not None else None
    else:
        edge = 0.0
    odds = _as_dict(getattr(record, "odds", None)) or None
    if settlement_payload.get("stake") is not None:
        stake = float(settlement_payload.get("stake") or 0.0)
    else:
        stake = float(getattr(result, "recommended_kelly_fraction", 0.0) or 0.0)
    execution_mode = str(getattr(result, "execution_mode", "LIVE"))
    metadata = {
        "recommended_side": recommended_side,
        "paper_side": str(getattr(result, "paper_side", "skip")),
        "paper_regime": str(getattr(result, "paper_regime", "")),
        "game_type": str(getattr(result, "game_type", "")),
    }

    settlement_payload = settlement or {}
    final_result = str(settlement_payload.get("result", "unknown"))
    pnl = settlement_payload.get("pnl")
    roi = settlement_payload.get("roi")
    clv = settlement_payload.get("clv")
    if event_type == "prediction":
        final_result = "unknown"
        pnl = None
        roi = None
        clv = None

    return TradeRecord(
        event_id=infer_event_id(record or result, decision, event_type=event_type),
        timestamp=settlement_payload.get("timestamp", utc_now_iso()),
        game_id=game_id,
        league=league,
        regime=regime,
        predicted_prob=home_prob,
        market_prob=market_prob,
        edge=float(edge) if edge is not None else None,
        decision=decision,
        stake=stake,
        odds=odds,
        result=final_result,
        pnl=float(pnl) if pnl is not None else None,
        roi=float(roi) if roi is not None else None,
        clv=float(clv) if clv is not None else None,
        execution_mode=execution_mode,
        event_type=event_type,
        metadata=metadata,
    )


class TradeJournal:
    def __init__(self, base_dir: Optional[str] = None):
        self.paths = ensure_research_dirs(base_dir)

    @property
    def ledger_path(self):
        return self.paths["ledger"]

    def append(self, record: TradeRecord) -> TradeRecord:
        append_jsonl(self.ledger_path, record.to_dict())
        return record

    def load(self) -> list[dict[str, Any]]:
        return load_jsonl(self.ledger_path)

    def latest_by_event(self) -> dict[str, dict[str, Any]]:
        latest: dict[str, dict[str, Any]] = {}
        for row in self.load():
            latest[row.get("event_id", "")] = row
        return latest
