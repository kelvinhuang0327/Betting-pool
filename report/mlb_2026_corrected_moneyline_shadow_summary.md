# P278-A Corrected Moneyline Local Shadow Prediction Handoff

> Retrospectively generated from committed local data. Paper-only and diagnostic-only; not a live or pregame publication, not production-ready, not deployment, and not betting readiness.

## Model and refit

- Selected model: `retrained_team_history_smooth`
- Model/version: `corrected_moneyline_shadow` / `p278a_corrected_moneyline_shadow_v1`
- Training period: `2025-03-18` to `2025-09-28`
- Training cutoff: `after_complete_date_2025-09-28`
- Eligible training rows/dates: `2430` / `184`
- State transition: `PREDICT_FULL_DATE_THEN_UPDATE`
- Final state fingerprint: `03e03dae83bbda5e3b8101f1a139b7155c021bfd78b8ec5357c58cf4b6524f1d`
- Model code/config fingerprint: `7776f2f303289430f41fcb7a18940caab79ee6b9875a9140859a45962c088700`
- Training input fingerprint: `56ee44889c3cb9430c60dbbba5bab6f692dc32620eadfa9cc062cda4d2078c6c`

## 2026 shadow generation

- Existing committed input rows: `828`
- Shadow prediction rows: `828`
- 2026 input fingerprint: `74c4a5498f80b2e7335b472d742bffac4313922aa4d0f35f89f2c9c220df73bb`
- State mode: `frozen_final_2025_state`
- Source Git commit: `77bca9d939cc361b6a1b3ef586d1417071f46a28`
- Generator/version: `p278a.moneyline_shadow_prediction.v1`
- Generated at: `2026-07-14T08:54:03.347569Z`
- Execution command: `python3 -m wbc_backend.recommendation.moneyline_shadow_prediction --source-git-commit 77bca9d939cc361b6a1b3ef586d1417071f46a28 --out-dir report`
- Execution output root: `report`
- No row supplied a trustworthy explicit canonical feature-as-of; no game date, current time, or file mtime was substituted.

## P275 availability and state-update policy

- Policy: `P275_EXACT_GAME_ID_AND_CANONICAL_ROW_AS_OF_COMPLETE_DATE_BATCH_ONLY`
- P274 verified record count: `1`
- Attempted / allowed / denied updates: `0` / `0` / `0`
- Applied 2026 outcome updates: `0`
- Denial counts by reason: `{}`
- Raw outcome-available candidates not attempted without a trustworthy as-of: `808`
- Coverage limitation: P274 currently contains one prospective availability record; it does not establish season-wide PIT coverage or replay readiness.

## Separation and evaluation

- Existing baseline remains separate: `p84b_diagnostic_baseline_v1`.
- Existing P84-B predictions remain byte-unchanged and were not relabeled or replaced.
- Corrected shadow source: `p278a_corrected_moneyline_shadow_v1`; no champion activation.
- Outcome-evaluation denominator: `0`
- Accuracy: `N/A`
- Brier: `N/A`
- ROI / EV / Kelly: `N/A` / `N/A` / `N/A`
- No outcome-based comparative winner is declared.
- Corrected historical performance does not establish future predictive ability.
