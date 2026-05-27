    # P84F — Predicted-Side Direction / Calibration Diagnostic
    *Generated: 2026-05-27T05:41:03Z*

    ---

    ## Executive Summary

    | Metric | Value |
    |---|---|
    | Classification | **P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK** |
    | AUC(prob, home_win) | 0.594315 |
    | AUC(prob, is_correct) | 0.524663 |
    | model_probability interpretation | P_HOME_WIN |
    | Current hit_rate | 0.569307 |
    | Flipped hit_rate | 0.430693 |
    | Probability-threshold hit_rate | 0.569307 |
    | Hit-rate improvement if flipped | +-0.138614 |
    | Mapping pattern | PROB_GE_05_MAPS_TO_HOME |

    ---

    ## Step 1 — P84E State Verification

    - P84E summary: EXISTS
    - P84E derived rows: EXISTS
    - P84E classification: P84E_OUTCOME_ATTACHMENT_READY_WITH_METRICS
    - n_outcome_available: 808
    - auc_direction (from P84E): home_positive
    - odds_api_called: False
    - production_ready: False

    ---

    ## Step 2 — Score / Label Interpretation Audit

    | AUC Variant | Value |
    |---|---|
    | AUC(model_probability, home_win) | 0.594315 |
    | AUC(1 - model_probability, home_win) | 0.405685 |
    | AUC(model_probability, away_win) | 0.405685 |
    | AUC(model_probability, is_correct) | 0.524663 |

    **model_probability interpretation**: P_HOME_WIN

    auc_prob_home_win > 0.5 confirms model_probability = P(home wins). auc_prob_is_correct < 0.5 exposes direction inversion in predicted_side.

    ---

    ## Step 3 — Predicted-Side Consistency Audit

    ### Mapping pattern: `PROB_GE_05_MAPS_TO_HOME`

    | prob bucket | n | predicted home | predicted away |
    |---|---|---|---|
    | prob >= 0.5 | 412 | 412 | 0 |
    | prob < 0.5  | 396 | 0 | 396 |

    | Hit-rate variant | Value |
    |---|---|
    | Current (as-stored) | 0.569307 |
    | Flipped predicted_side | 0.430693 |
    | Probability-threshold (home if prob≥0.5) | 0.569307 |
    | Home-predicted subset | 0.592233 |
    | Away-predicted subset | 0.545455 |

    ---

    ## Step 4 — FIP Delta Sign Audit

    **Convention**: `sp_fip_delta = home_sp_fip - away_sp_fip`
    - delta > 0 → home pitcher worse → FIP favours AWAY
    - delta < 0 → home pitcher better → FIP favours HOME

    | Subset | n | Away win rate | Home win rate |
    |---|---|---|---|
    | delta > 0 (away favoured) | 396 | 0.545455 | 0.454545 |
    | delta < 0 (home favoured) | 412 | 0.407767 | 0.592233 |

    - FIP direction hit_rate (correct direction): **0.569307**
    - predicted_side FIP consistency rate: **1.0**
    - FIP signal: `VALID_AWAY_EDGE_WHEN_DELTA_POSITIVE`

    fip_direction_hit_rate = win rate if we bet 'away' when delta>0 and 'home' when delta<0 (the FIP-correct direction).

    ---

    ## Step 5 — Rule Subset Audit

    | Subset               | n (+sample flag) | current HR |  flipped HR | thresh HR |
    |---|---|---|---|---|
    | all                  |    808                 | 0.569307 | 0.430693 | 0.569307 |
| primary_125          |    491                 | 0.602851 | 0.397149 | 0.602851 |
| shadow_100           |    536                 | 0.595149 | 0.404851 | 0.595149 |
| tier_b               |     94                 |  0.56383 |  0.43617 |  0.56383 |
| home_predicted       |    412                 | 0.592233 | 0.407767 | 0.592233 |
| away_predicted       |    396                 | 0.545455 | 0.454545 | 0.545455 |

    ---

    ## Step 6 — Calibration Bucket Table

    | prob bucket  |   n   | home win rate | away win rate |
    |---|---|---|---|
    | 0.3-0.4      |   276 | 0.4384 | 0.5616 |
| 0.4-0.5      |   120 | 0.4917 | 0.5083 |
| 0.5-0.6      |   121 | 0.5289 | 0.4711 |
| 0.6-0.7      |   128 | 0.5781 | 0.4219 |
| 0.7-0.8      |   163 | 0.6503 | 0.3497 |

    ---

    ## Step 7 — Diagnostic Classification

    **Classification**: `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK`

    ### Evidence Chain

  - AUC(prob, home_win)=0.5943 > 0.5 → model_probability = P(home wins)
  - FIP delta sign valid: delta>0 → away wins more often (correct FIP edge direction)

    ### Remediation Path (P84G)

    P84G: Apply Platt scaling or isotonic regression to recalibrate model_probability to genuine win probabilities.

    ---

    ## Governance

    | Invariant | Value |
    |---|---|
    | paper_only | True |
    | diagnostic_only | True |
    | production_ready | False |
    | live_api_calls (odds) | 0 |
    | ev | False |
    | clv | False |
    | kelly | False |
    | fabricated_outcomes | False |
