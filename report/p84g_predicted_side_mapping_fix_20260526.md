# P84G — Fix Predicted-Side Mapping + Regenerate Canonical Prediction Rows

**Date**: 2026-05-27  
**Classification**: `P84G_SIDE_MAPPING_FIXED_METRICS_REGENERATED`  
**Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`

---

## 1. Mapping Convention Decision

Derived from P84F JSON evidence + P83E source code inspection:

```
sp_fip_delta = home_sp_fip - away_sp_fip  (P83C formula — unchanged)
FIP is lower-is-better:
  delta > 0 → home pitcher FIP > away pitcher FIP → home pitcher WORSE → predicted_side='away'
  delta < 0 → home pitcher FIP < away pitcher FIP → away pitcher WORSE → predicted_side='home'
```

P84F evidence chain:
- `fip_signal=VALID_AWAY_EDGE_WHEN_DELTA_POSITIVE`
- `pos_delta_away_win_rate=0.545455` (when delta>0, away wins 54.5%)
- `neg_delta_home_win_rate=0.592233` (when delta<0, home wins 59.2%)
- Pre-fix: `predicted_side_fip_consistency_rate=0.0` (fully inverted)

P83E v1 bug: returned `'home'` when `delta > 0` — backwards from FIP convention.

---

## 2. Code Change Applied

**File**: `scripts/_p83e_2026_canonical_prediction_row_producer.py`
**Function**: `compute_predicted_side(sp_fip_delta)`

```python
# BEFORE (P83E v1 — inverted):
if sp_fip_delta > 0.0:
    return 'home'
if sp_fip_delta < 0.0:
    return 'away'

# AFTER (P84G fix — correct FIP convention):
if sp_fip_delta > 0.0:
    return 'away'  # home pitcher worse (higher FIP)
if sp_fip_delta < 0.0:
    return 'home'  # away pitcher worse (higher FIP)
```

---

## 3. Regeneration Results

| Artifact | Status |
|---|---|
| P83E canonical rows | 828 rows (expected 828) |
| P83E mapping correct | delta>0→away: True |
| P84E outcome-attached | 808 outcome-available |
| P84F rerun | `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` |

---

## 4. Before / After Metrics

| Metric | Before (P84F bug) | After (P84G fix) | Delta |
|---|---|---|---|
| hit_rate (all, n=808) | 0.430693 | 0.569307 | +0.138614 |
| AUC(prob, home_win) | 0.594315 | 0.594315 | 0.000000 |
| AUC(prob, is_correct) | 0.475337 | 0.524663 | +0.049326 |
| mapping_pattern | PROB_GE_05_MAPS_TO_AWAY | PROB_GE_05_MAPS_TO_HOME | — |
| n_consistent | 0 | 808 | — |
| n_inverted | 808 | 0 | — |
| FIP consistency rate | 0.0000 | 1.0 | — |

### Subset Metrics (After P84G Fix)

| Subset | hit_rate | AUC |
|---|---|---|
| all (n=808) | 0.569307 | 0.594315 |
| primary_125 | 0.602851 | — |
| shadow_100 | 0.595149 | — |
| Brier (all) | 0.249408 | — |
| ECE (all) | 0.069682 | — |

---

## 5. Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| production_ready | False |
| live_api_calls | 0 |
| odds_api_called | False |
| ev | False |
| clv | False |
| kelly | False |
| fabricated_outcomes | False |

---

## 6. CTO Agent Summary (5 lines)

1. P84F commit (9175759) confirmed `P84F_SIDE_MAPPING_INVERTED` — `predicted_side` was fully inverted relative to FIP convention.
2. Root fix: `compute_predicted_side()` in `scripts/_p83e_2026_canonical_prediction_row_producer.py` corrected — `delta>0 → 'away'`, `delta<0 → 'home'`.
3. All three downstream artefacts regenerated: P83E canonical rows (828), P84E outcome-attached rows (808 available), P84F diagnostic rerun.
4. Hit rate improved 0.4307 → 0.5693 (+0.1386); AUC(prob, is_correct) improved 0.4753 → 0.5247.
5. P84F rerun now classifies `P84F_MODEL_SIGNAL_PRESENT_CALIBRATION_WEAK` — inversion resolved; model signal preserved at AUC=0.5943.

## 7. CEO Agent Summary (5 lines)

1. The FIP-based prediction system had a direction bug since P83E v1: picking the wrong team 56.9% of the time.
2. P84G fixes the bug — hit rate goes from 43.1% → 56.9% (diagnostic baseline, no odds, no real bets).
3. Primary-125 subset (highest-confidence picks) now shows 60.3% hit rate (diagnostic only).
4. All governance invariants preserved: paper_only=true, no EV/CLV/Kelly, no odds API, no betting recommendation.
5. Next step: calibration analysis (P84H) to assess ECE=0.070 and evaluate if confidence scores need recalibration.

---

> **Governance**: paper_only=True | diagnostic_only=True | production_ready=False  
> No odds. No EV. No CLV. No Kelly. No betting recommendation. No champion replacement.