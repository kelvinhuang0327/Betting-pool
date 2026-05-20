# Phase 68 — Model Architecture and Ensemble Failure Audit

**Date**: 2026-05-06  
**Status**: COMPLETE  
**Gate**: `CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`  
**Completion Marker**: `PHASE_68_MODEL_ARCHITECTURE_ENSEMBLE_FAILURE_AUDIT_VERIFIED`  
**Phase Version**: `phase68_model_architecture_ensemble_failure_audit_v1`

---

## 1. Objective

Audit the MARL stacking ensemble's internal architecture for systematic sources of prediction failure, focusing on:
- Calibration residual patterns (overconfidence / underconfidence by blend fav_prob band)
- Model vs market vs blend Brier comparison across all confidence segments
- Blend dilution effect (does market alone outperform blend at heavy-fav bands?)
- Model-market disagreement analysis
- Architecture instability (walk-forward window weight variability)
- Expected Calibration Error (ECE) by source
- Negative controls to verify signal authenticity

**Safety constants (ALL FROZEN — unchanged):**

| Constant | Value |
|---|---|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |
| `ALPHA` | `0.40` |

---

## 2. Phase Chain Anchors

| Phase | Gate | Meaning |
|---|---|---|
| 64b | `BULLPEN_GRANULAR_FEATURE_NOT_PROMISING` | Bullpen granularity adds no edge |
| 65 | `OVERFIT_RISK` | Bullpen load signal is noise-level |
| 66 | `MARKET_MICROSTRUCTURE_NOT_PROMISING` | Line movement / CLV / opening direction: data limited + no signal |
| 67 | `OVERFIT_RISK` | Context dimensions (lineup/rest/schedule/ballpark) show noise-level BSS |
| **68** | **`CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`** | **Non-monotone calibration residual detected; genuine signal confirmed** |

---

## 3. Data Source

| Source | Path | Records |
|---|---|---|
| Walk-forward predictions (Phase 56 SP+Bullpen) | `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl` | 2025 games |

**Model versions**: 5 walk-forward windows × 405 games each (no overlap).

---

## 4. Blend Formula (frozen)

```
blend = (1 - 0.40) × model_home_prob + 0.40 × market_home_prob_no_vig
fav_prob = max(blend, 1 - blend)
fav_win  = home_win  if blend >= 0.5  else  1 - home_win
BSS      = 1 - blend_brier / market_brier   (direct ratio vs market reference)
```

---

## 5. Segment Sizes

| Segment | N | Definition |
|---|---|---|
| All games | 2025 | Full 2025 MLB regular season |
| Heavy Favorite | 60 | `fav_prob >= 0.70` |
| High Confidence | 10 | `fav_prob >= 0.75` |
| Extreme Favorite | 1 | `fav_prob >= 0.80` |
| Phase 45 Failure | 170 | `fav_prob >= 0.60 AND fav_win == 0` |

---

## 6. All-Games Segment Metrics

| Source | Brier | BSS vs Market | Mean Fav Prob | Fav Win Rate | ECE |
|---|---|---|---|---|---|
| Model | 0.2446 | −0.0021 | 0.5718 | 0.5506 | 0.0268 |
| Market | 0.2441 | 0.0000 (ref) | 0.5788 | 0.5506 | 0.0266 |
| **Blend** | **0.2434** | **+0.0028** | **0.5705** | **0.5506** | **0.0258** |

Model is **less sharp** than market (mean fav_prob: 0.5718 < 0.5788). Blend partially corrects by pulling toward the sharper market signal.

---

## 7. Heavy-Favorite Segment (fav_prob ≥ 0.70)

| Source | Brier | BSS vs Market |
|---|---|---|
| Model | 0.1792 | **−0.0119** |
| Market | 0.1771 | 0.0000 (ref) |
| Blend | 0.1777 | **−0.0033** |

**Key finding**: At heavy-fav games (n=60), market beats both model (by −0.0119 BSS) and blend (by −0.0033 BSS). The model is actively degrading blend accuracy at the most confident games.

---

## 8. Calibration Residual Analysis — Primary Signal

Residual = `blend_pred − actual_win_rate`. Positive = overconfident; negative = underconfident.

### 8a. Blend Fav-Prob Bands

| Band | N | Blend Pred | Actual | **Residual** | Flag |
|---|---|---|---|---|---|
| 0.50–0.55 | 885 | 0.5251 | 0.5153 | **+0.0098** | — |
| **0.55–0.60** | **640** | **0.5728** | **0.5141** | **+0.0587** | ⚠️ OVERCONFIDENT |
| 0.60–0.65 | 312 | 0.6227 | 0.6090 | **+0.0138** | — |
| **0.65–0.70** | **128** | **0.6740** | **0.7344** | **−0.0603** | ⚠️ UNDERCONFIDENT |
| 0.70–0.75 | 50 | 0.7148 | 0.7400 | **−0.0252** | — |
| 0.75+ | 10 | 0.7716 | 0.9000 | **−0.1284** | DATA LIMITED |

**Non-monotone residual pattern**:
- Model is **overconfident** at 0.55–0.60 (+5.87pp, n=640) — systematically inflating mid-range confidence
- Model is **underconfident** at 0.65–0.70 (−6.03pp, n=128) — failing to fully commit at high-confidence games

This non-monotone shape is consistent with **logit/0.85 sharpening** in `stacking_model.py`, which compresses the full probability range and creates a mismatch between predicted and actual confidence levels.

### 8b. Model Fav-Prob Band Calibration (Brier Comparison)

| Model Band | N | model_brier | market_brier | blend_brier | Winner |
|---|---|---|---|---|---|
| 0.65–0.70 | 134 | 0.1966 | 0.1846 | 0.1906 | **Market** |
| 0.70–0.75 | 42 | 0.2249 | 0.2151 | 0.2200 | **Market** |

At every high-confidence model band, market outperforms model and blend. This confirms that the model's high-confidence signals are **miscalibrated**, not just imprecise.

---

## 9. Architecture Instability

| Model Version | N | w_elo | w_market (internal) |
|---|---|---|---|
| `marl_w_elo=0.494_w_market=0.400` | 405 | 0.494 | 0.400 |
| `marl_w_elo=0.636_w_market=0.371` | 405 | 0.636 | 0.371 |
| `marl_w_elo=0.543_w_market=0.243` | 405 | 0.543 | 0.243 |
| `marl_w_elo=0.413_w_market=0.384` | 405 | 0.413 | 0.384 |
| `marl_w_elo=0.400_w_market=0.350` | 405 | 0.400 | 0.350 |

| Metric | Value |
|---|---|
| `w_market` CV | **0.1595** (> threshold 0.10) |
| `w_elo` CV | **0.1751** (> threshold 0.10) |
| `instability_detected` | **True** |

The internal stacking weights vary substantially across walk-forward windows. The w_market internal weight ranges from 0.243 to 0.400 — a 65% relative spread. This instability means the model **re-discovers different ensemble compositions** on each training window, suggesting the optimization landscape is flat and the weights are not reliable.

Note: The internal `w_market` (stacking coefficient) is **distinct** from `ALPHA = 0.40` (the post-hoc blend weight). The stacking model already incorporates market via `steam * 0.25`, and the blend then adds another 40% market weight — **double-counting market information**.

---

## 10. Ensemble Sharpness

| Source | Mean Fav Prob | Std |
|---|---|---|
| Model | 0.5718 | 0.0557 |
| Market | **0.5788** | **0.0582** |
| Blend | 0.5705 | 0.0540 |

`model_less_sharp_than_market = True` (mean model confidence 0.5718 < market confidence 0.5788). The blend pulls the model toward the sharper market, but at high-confidence bands the model's **incorrect** calibration still drags blend below market accuracy.

---

## 11. Blend Dilution Analysis

| Segment | N | Market Brier | Blend Brier | Dilution Magnitude | Dilution? |
|---|---|---|---|---|---|
| All games | 2025 | 0.2441 | 0.2434 | −0.0007 | No (blend better) |
| **Heavy fav ≥ 0.70** | **60** | **0.1771** | **0.1777** | **+0.0006** | **Yes** |
| fav ≥ 0.60 | 500 | 0.2200 | 0.2202 | +0.0003 | Yes |
| fav ≥ 0.65 | 188 | 0.1872 | 0.1899 | +0.0027 | Yes |

Across all games, blend beats market. But at confidence ≥ 0.60, the blend **dilutes** market accuracy — the model is pulling the blend away from the better market signal at exactly the games where we care most.

---

## 12. Model-Market Disagreement Analysis

| Disagreement Bucket | N | model_brier | market_brier | blend_brier | Market beats Model? |
|---|---|---|---|---|---|
| `model_large_fav` (model >> market by >5pp) | 499 | 0.2515 | 0.2499 | 0.2491 | **Yes** |
| `mkt_large_fav` (market >> model by >5pp) | 350 | 0.2460 | 0.2426 | 0.2425 | **Yes** |
| `agree` (diff < 5pp) | 1176 | 0.2414 | 0.2415 | 0.2413 | Tie |

Market beats model in **both disagreement directions**. Even when the model is uniquely bullish on a team (model_large_fav), the market is still the better predictor. The model brings no directional value beyond what the market already prices.

---

## 13. Negative Controls

| Control | Real BSS | Null Mean | Gap | Overfit Risk? |
|---|---|---|---|---|
| `shuffled_confidence_bucket` | +0.0263 | −0.0032 | **+0.0295** | **No** (gap >> 0.02 threshold) |
| `random_disagreement_assignment` | +0.0078 | −0.0002 | +0.0076 | — (informational) |
| `irrelevant_odd_even_split` | +0.0052 | +0.0030 | +0.0022 | — (informational) |

The **shuffled confidence control** shows that the real blend BSS (+0.0263 vs naive 0.5) is far above the null distribution mean (−0.0032 when confidence ordering is destroyed). The gap of +0.0295 >> threshold (0.02) confirms the calibration signal is **genuine** — not noise or overfit.

---

## 14. Root Cause Hypotheses

The calibration evidence points to 3 specific architecture decisions in `stacking_model.py`:

### H1: logit/0.85 sharpening (PRIMARY)
```python
# stacking_model.py (approximate excerpt)
logit_prob = logit(raw_prob) / 0.85
sharpened_prob = sigmoid(logit_prob)
```
Dividing the logit by 0.85 (< 1) **inflates the logit magnitude**, pushing predictions further from 0.5. This creates artificial overconfidence in the 55–60% range by amplifying already-high predictions beyond their calibration. The non-monotone residual pattern (+5.87pp at 55-60, −6.03pp at 65-70) is consistent with a compression artifact from this sharpening.

### H2: away_wp × 0.9 dampening
```python
if away_wp < 0.3:
    away_wp = away_wp * 0.9
```
Artificially dampening the away team win probability when away_wp < 0.3 creates a systematic bias toward home favorites, contributing to overconfidence in the moderate confidence range.

### H3: Double market incorporation (STRUCTURAL)
```python
# In stacking model: steam * 0.25 (partial market)
away_wp += steam * 0.25
# Then in blend: ALPHA = 0.40 (full market)
blend = 0.60 * model_home_prob + 0.40 * market_home_prob_no_vig
```
Market information enters twice: once inside the stacking model via `steam * 0.25`, and again in the blend via `ALPHA = 0.40`. This double-counting may be appropriate for stable market priors but makes the calibration analysis harder to interpret and could amplify market mispricing.

---

## 15. Expected Calibration Error (ECE)

| Source | ECE (All Games) | ECE (Heavy Fav ≥ 0.70) |
|---|---|---|
| Blend | **0.0258** | 0.0424 |
| Model | 0.0268 | 0.0742 |
| Market | 0.0266 | 0.0840 |

Blend achieves the best overall ECE (0.0258). At heavy-fav, model ECE is high (0.0742) though below the `_ABSTENTION_ECE_THRESHOLD = 0.06` at the blend level (0.0424). Calibration redesign targets reducing model-level ECE, which would further improve blend ECE.

---

## 16. Gate Decision

### Gate: `CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`

**Primary trigger**: Non-monotone calibration residual  
- Band 0.55–0.60: residual = **+0.0587** > threshold (0.04), n=640 ✓  
- Band 0.65–0.70: residual = **−0.0603** < −threshold (−0.04), n=128 ✓  

**Overfit risk**: CLEAR (shuffled control gap = +0.0295 >> 0.02 threshold)  

**Supporting evidence**:
- Market beats blend at heavy_fav (blend BSS vs market = −0.0033)
- Architecture instability (w_market CV = 0.1595 > 0.10)
- Blend dilution at fav ≥ 0.65 (blend worse than market by +2.7pp Brier)
- Model never beats market in any disagreement scenario

**Gate rationale (from report JSON)**:  
> Overconfident band '0.55-0.60': blend_pred=0.5728 actual=0.5141 residual=+0.0587 (n=640) | Underconfident band '0.65-0.70': blend_pred=0.6740 actual=0.7344 residual=-0.0603 (n=128) | Probable causes: logit/0.85 sharpening + away_wp*0.9 artifact in stacking_model.py.

---

## 17. Phase 69 Recommendation

**Task**: Calibration objective redesign — remove artificial sharpening, add isotonic or Platt-scaling calibration layer.

**Specific changes to evaluate**:
1. Remove `logit / 0.85` sharpening from `stacking_model.py`
2. Remove `away_wp * 0.9` dampening when `away_wp < 0.3`
3. Add a post-hoc calibration layer (Platt scaling or isotonic regression) fitted on walk-forward validation data
4. Re-evaluate double market incorporation (steam * 0.25 + ALPHA 0.40)

**Success criteria**:
- ECE(blend) improvement ≥ 25% vs current (0.0258 → < 0.0194)
- Calibration residual in 0.55–0.60 band drops below +0.04 (from +0.0587)
- Calibration residual in 0.65–0.70 band rises above −0.04 (from −0.0603)
- n ≥ 1500 validation samples in hold-out window

**Safety**: All changes must be validated in `tests/` before any production modification. `ALPHA` must remain 0.40 during diagnostic Phase 69. `CANDIDATE_PATCH_CREATED` stays `False` until validation complete.

---

## 18. Summary

| Finding | Value | Status |
|---|---|---|
| n_predictions | 2025 | ✓ |
| All-games blend BSS vs market | +0.0028 | Marginal improvement |
| Heavy-fav blend BSS vs market | −0.0033 | ⚠️ Market beats blend |
| Calibration overconfidence (0.55–0.60) | +0.0587 | ⚠️ Detected |
| Calibration underconfidence (0.65–0.70) | −0.0603 | ⚠️ Detected |
| Architecture instability (w_market CV) | 0.1595 | ⚠️ Unstable |
| Blend dilution at heavy_fav | +0.0006 | ⚠️ Detected |
| Negative control gap (shuffled) | +0.0295 | ✅ Genuine signal |
| Overfit risk | False | ✅ Clear |
| **Gate** | **`CALIBRATION_OBJECTIVE_REDESIGN_PROMISING`** | **Phase 69 warranted** |

---

*Report generated from `reports/phase68_model_architecture_ensemble_failure_audit_20260506.json`*  
*Completion marker: `PHASE_68_MODEL_ARCHITECTURE_ENSEMBLE_FAILURE_AUDIT_VERIFIED`*
