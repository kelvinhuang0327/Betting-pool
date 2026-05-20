# MLB Post-game Review Report

> **⚠️ PAPER-ONLY — DRY-RUN — NO REAL BET — NO PROFIT CLAIM**
>
> 本報告為 paper-only post-game review。不代表任何真實下注、真實獲利、
> 或真實 edge 聲明。所有結果僅供研究與回測使用。

**review_date:** 2025-07-01
**source_mode:** replay
**run_timestamp_utc:** 2026-05-07T08:33:14.766513+00:00
**ledger_path:** reports/mlb_paper_betting_ledger.jsonl
**reviewed_snapshot_path:** reports/mlb_paper_betting_reviewed_snapshot_20250701.jsonl

---

## Safety Flags

- **production_modified**: `False`
- **candidate_patch_created**: `False`
- **alpha_modified**: `False`
- **prediction_jsonl_overwritten**: `False`
- **ledger_overwrite_blocked**: `True`
- **no_edge_claim**: `True`
- **no_profit_claim**: `True`
- **diagnostic_only**: `True`
- **paper_only**: `True`
- **no_real_bet**: `True`

---

## Review Summary

| Metric | Value |
|--------|-------|
| total_ledger_entries | 7 |
| matched_results | 7 |
| pending_results | 0 |
| reviewed_count | 4 |
| won_count | 3 |
| lost_count | 1 |
| push_count | 0 |
| pass_count | 0 |
| watch_only_count | 2 |
| lean_count | 4 |
| market_only_shadow_count | 1 |
| brier_score | 0.2323 |
| bss_vs_baseline | -0.2387 |
| recommendation_accuracy | 0.75 |
| human_review_required | `True` |

---

## Reviewed Entries

| game_id | date | mkt | rec | selection | result | review_status | P&L |
|---------|------|-----|-----|-----------|--------|---------------|-----|
| MLB2025_1266_2025-07-01_NEW_ | 2025-07-01 | moneyline | LEAN_HOME | HOME | WON | REVIEWED | +1.494 |
| MLB2025_1267_2025-07-01_ST._ | 2025-07-01 | moneyline | WATCH_ONLY | None | NO_BET | REVIEWED_NO_BET | — |
| MLB2025_1268_2025-07-01_MIN_ | 2025-07-01 | moneyline | LEAN_HOME | HOME | WON | REVIEWED | +1.283 |
| MLB2025_1271_2025-07-01_LOS_ | 2025-07-01 | moneyline | LEAN_AWAY | AWAY | WON | REVIEWED | +0.537 |
| MLB2025_1273_2025-07-01_BAL_ | 2025-07-01 | moneyline | LEAN_AWAY | AWAY | LOST | REVIEWED | -1.000 |
| MLB2025_1274_2025-07-01_HOU_ | 2025-07-01 | moneyline | WATCH_ONLY | None | NO_BET | REVIEWED_NO_BET | — |
| MLB2025_1277_2025-07-01_CHI_ | 2025-07-01 | moneyline | MARKET_ONLY_SHADOW | None | UNKNOWN | REVIEWED_NO_BET | — |

---

## Failure Notes

### `MODEL_MARKET_DISAGREEMENT_LOSS` (count=1)
- **suspected_failure_mode**: model_market_divergence_not_predictive: opening line gap may close before game time
- **proposed_next_audit**: Accumulate 30+ LEAN outcomes; test whether large model-market gap is predictive in held-out season data (n >= 1500 required)
- **human_review_required**: `True`
- **blocked_auto_change_reason**: human_review_required: governance rules prohibit automatic model/alpha/stake changes based on dry-run review results

### `NO_BET_REVIEW_ONLY` (count=2)
- **suspected_failure_mode**: pass_or_watch_only: no bet placed; outcome tracked for reference only
- **proposed_next_audit**: Monitor PASS/WATCH_ONLY outcome distributions to validate threshold calibration (LEAN_THRESHOLD=0.10, WATCH_THRESHOLD=0.05)
- **human_review_required**: `True`
- **blocked_auto_change_reason**: human_review_required: governance rules prohibit automatic model/alpha/stake changes based on dry-run review results

---

## Next Audit Proposal

- **Observation**: lean_count=4; accuracy=0.75
- **Observation**: brier=0.2323; bss=-0.2387
- **Observation**: 1 games in Phase71/72 de-risk band

- Accumulate >= 30 LEAN outcomes before drawing any conclusion about model edge
- Continue accumulating replay sessions; require n >= 1500 before interpreting Brier as stable
- Track shadow outcomes over >= 20 sessions to validate Phase71 market superiority hypothesis out-of-sample

**blocked_auto_change_reason**: human_review_required: no automatic model/alpha/stake/bet changes permitted; all proposals require human review and >= 1500 sample validation
**human_review_required**: `True`
**auto_model_change_blocked**: `True`
**auto_alpha_change_blocked**: `True`

---

## No Profit Claim

本系統不聲稱已找到可盈利的投注 edge。所有 paper review 均為研究目的，不代表任何真實獲利預期。

**NO_PROFIT_CLAIM = True**
**NO_EDGE_CLAIM = True**
**PAPER_ONLY = True**
**NO_REAL_BET = True**
**LEDGER_OVERWRITE_BLOCKED = True**

---

## Gate Conclusion

**Gate: `MLB_POSTGAME_REVIEW_READY`**

> result_ingestion + reviewed_snapshot + review_summary + brier_metrics + failure_notes all operational; paper-only safety flags complete

---

## Completion Marker

`MLB_POSTGAME_REVIEW_VERIFIED`

