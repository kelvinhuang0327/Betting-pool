# Phase 55 — SP Functional Form Redesign vs Bullpen Feature Investigation

**Report Date**: 2026-05-05
**Phase**: 55 — SP vs Bullpen Diagnosis
**Version**: phase55_sp_vs_bullpen_diagnosis_v1
**Audit Hash**: `b96f6b6f2cd779f2`

## Executive Summary

**Conclusion**: ⚾ `BULLPEN_FEATURE_INVESTIGATION`

**Rationale**: bullpen_missing_score=0.6000 >= 0.6; failure_pattern=HEAVY_FAVORITE_CONCENTRATED; no SP form resolves heavy_favorite/high_confidence failures but overall BSS can improve. Bullpen features recommended.

**Bullpen Missing Score**: 0.6000 / 1.0
**Failure Pattern**: `HEAVY_FAVORITE_CONCENTRATED`
**Best SP Form**: `tanh_current` (failure_count=8)
**Phase54 Baseline Failure Count**: 6

| Hard Rule | Value |
|-----------|-------|
| candidate_patch_created | `False` |
| production_modified | `False` |
| diagnostic_only | `True` |

## Why Phase54 Failed

Phase 54 applied safe coefficient (scale=0.25x, effective=0.00075) to Phase52 SP context rows.
Despite conservative coefficient, Phase45 re-run showed **6 failure segments**.

**Phase54 failure segments**:
- `odds_bucket:heavy_favorite`
- `odds_bucket:mid`
- `disagreement:low`
- `month:2025-04`
- `month:2025-06`
- `month:2025-08`

Key observations from Phase54:
- `heavy_fav_ece_no_longer_failure = False` → heavy_favorite ECE issue persists
- `high_conf_improved = False` → high_confidence segment not resolved
- Phase43 BSS delta vs baseline = -2.6e-05 (slight degradation)
- failure_count_delta = +6 (all failures new vs Phase43 baseline)

Phase 55 investigates whether this is due to:
1. **SP functional form** (tanh shape, scale, sign, bucket)
2. **Missing bullpen / late-game features** (fatigue, leverage, ERA proxy)
3. **Insufficient sample size** (bootstrap still not significant)

## SP Functional Form Comparison

| Form | adj_rows | adj_rate | max_abs_adj | overall_bss | overall_ece | heavy_fav_ece | high_conf_bss | month_04_bss | failure_count |
|------|----------|----------|-------------|-------------|-------------|---------------|---------------|--------------|---------------|
| `tanh_current` ⭐ | 1347 | 66.5% | 0.000537 | +0.021217 | +0.029817 | +0.089202 | +0.097218 | +0.113307 | 8 |
| `tanh_stronger` | 1347 | 66.5% | 0.001074 | +0.021255 | +0.030217 | +0.092915 | +0.097300 | +0.113475 | 8 |
| `linear_capped` | 1347 | 66.5% | 0.000900 | +0.021235 | +0.029819 | +0.089163 | +0.097258 | +0.113380 | 8 |
| `sign_only` | 217 | 10.7% | 0.001000 | +0.021228 | +0.031010 | +0.092947 | +0.097234 | +0.113446 | 8 |
| `bucketed_delta` | 535 | 26.4% | 0.003000 | +0.021349 | +0.031203 | +0.089969 | +0.096456 | +0.113129 | 8 |
| `shrink_to_market` | 1347 | 66.5% | 0.000537 | +0.021213 | +0.029818 | +0.089222 | +0.097204 | +0.113293 | 8 |

**Phase54 reference**: failure_count=6

### Functional Form Descriptions

- **`tanh_current`**: tanh(delta × 0.5) × 0.003 × 0.25 — Phase54 safe coefficient (reference)
- **`tanh_stronger`**: tanh(delta × 0.5) × 0.003 × 0.50 — 2× the safe coefficient
- **`linear_capped`**: clip(delta × 0.0005, -0.008, +0.008) — linear form with hard cap
- **`sign_only`**: ±0.001 if |delta| > 1.0 else 0 — sign-only advantage
- **`bucketed_delta`**: 5 buckets: large/small home/away edge (±0.003/±0.001), neutral
- **`shrink_to_market`**: tanh_current but 50% shrinkage when |model - 0.5| >= 0.15 (high confidence)

## Bullpen Missing-Feature Evidence

| Indicator | Value |
|-----------|-------|
| bullpen_missing_score | 0.6000 |
| bullpen_feature_likely_missing | `True` |
| failure_pattern | `HEAVY_FAVORITE_CONCENTRATED` |

**Evidence:**
- heavy_favorite segment failing: late-inning lead protection driven by bullpen leverage
- Monthly failures (['month:2025-04', 'month:2025-06']): seasonal bullpen usage patterns likely differ
- No SP functional form meaningfully reduces failure segments or fixes heavy_favorite/high_confidence: structural feature gap likely

**Recommended Bullpen Features** (for Phase56 if BULLPEN_FEATURE_INVESTIGATION):
- `bullpen_fatigue_3d`
- `bullpen_fatigue_7d`
- `reliever_back_to_back_count`
- `bullpen_recent_era_proxy`
- `late_game_leverage_usage_proxy`

## Decision Conclusion

```
conclusion = BULLPEN_FEATURE_INVESTIGATION
```

**Rationale**: bullpen_missing_score=0.6000 >= 0.6; failure_pattern=HEAVY_FAVORITE_CONCENTRATED; no SP form resolves heavy_favorite/high_confidence failures but overall BSS can improve. Bullpen features recommended.

### Bullpen Feature Investigation Path

bullpen_missing_score=0.6000 >= 0.6. All SP functional forms fail to resolve heavy_favorite / high_confidence failures. Market likely pricing in bullpen state information the model lacks.

## Recommended Phase56 Tasks

1. Phase 56A: Investigate and prototype: bullpen_fatigue_3d, bullpen_fatigue_7d, reliever_back_to_back_count, bullpen_recent_era_proxy, late_game_leverage_usage_proxy
2. Phase 56B: Design bullpen fatigue proxy from MLB historical relief pitcher usage data
3. Phase 56C: Build phase56_bullpen_feature_builder.py
4. Phase 56D: Backfill bullpen features for full 2025 MLB season (2,025 games)
5. Phase 56E: Run Phase43/44/45 audit with bullpen features injected
6. Phase 56F: Verify heavy_favorite ECE improves with bullpen features
7. Phase 56G: If significant → write Phase57 candidate patch blueprint

## Limitations

1. Functional form evaluation uses raw model BSS (not blended) for consistency across forms.
2. Segment failure count may differ from Phase45's blended analysis.
3. bootstrap significance was NOT_SIGNIFICANT in Phase54; Phase55 does not rerun bootstrap.
4. heavy_favorite ECE references Phase54 values; any improvement here is diagnostic-only and cannot be productionized without Phase43/44/45 re-audit.
5. All 6 forms are offline-only; no production JSONL is written.

## Hard-Rule Confirmation

```
candidate_patch_created = False
production_modified     = False
diagnostic_only         = True
conclusion              = BULLPEN_FEATURE_INVESTIGATION
audit_hash              = b96f6b6f2cd779f2
```

All hard rules satisfied:
- No production JSONL written in Phase 55
- No model retraining or ensemble
- No look-ahead leakage (p0_features computed pre-game)
- candidate_patch_created enforced by Phase55DiagnosisResult.__post_init__

## Completion Marker

```
PHASE_55_SP_VS_BULLPEN_DIAGNOSIS_VERIFIED
conclusion=BULLPEN_FEATURE_INVESTIGATION
bullpen_missing_score=0.6000
bullpen_feature_likely_missing=True
failure_pattern=HEAVY_FAVORITE_CONCENTRATED
best_form_name=tanh_current
best_form_failure_count=8
phase54_failure_count=6
candidate_patch_created=False
production_modified=False
diagnostic_only=True
audit_hash=b96f6b6f2cd779f2
```