from __future__ import annotations

from typing import Any, Dict, Optional


ACTIVE_DAY = "ACTIVE_DAY"
SKIPPED_DAY = "SKIPPED_DAY"
PARTIAL_DAY = "PARTIAL_DAY"


def classify_day(
    system_online: bool,
    daily_pipeline_ran: bool,
    prediction_count: int,
    game_count_detected: int,
    research_mode: bool,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    prediction_count = int(prediction_count or 0)
    game_count_detected = int(game_count_detected or 0)

    if prediction_count > 0:
        if game_count_detected > 0 and prediction_count < game_count_detected:
            status = PARTIAL_DAY
            reason = reason or "incomplete_coverage"
        else:
            status = ACTIVE_DAY
            reason = reason or "predictions_present"
    elif game_count_detected > 0 and not daily_pipeline_ran:
        status = SKIPPED_DAY
        reason = reason or "system_offline"
    elif daily_pipeline_ran and game_count_detected > 0:
        status = PARTIAL_DAY
        reason = reason or "pipeline_interrupted"
    elif daily_pipeline_ran and game_count_detected == 0:
        status = PARTIAL_DAY
        reason = reason or "no_games_detected"
    else:
        status = SKIPPED_DAY
        reason = reason or "system_offline"

    return {
        "status": status,
        "reason": reason,
        "system_online": bool(system_online),
        "daily_pipeline_ran": bool(daily_pipeline_ran),
        "prediction_count": prediction_count,
        "game_count_detected": game_count_detected,
        "research_mode": bool(research_mode),
    }
