# Phase 41 Metrics SSOT Report

**Verdict**: `PASS`  
**Pass**: 18 | **Fail**: 0 | **Skip**: 0

## Check Results

| ID | Status | Summary |
|---|---|---|
| `C01_ODDS_EVEN` | ✅ PASS | +100 → 0.500000 (expected 0.500000) |
| `C02_ODDS_MINUS150` | ✅ PASS | -150 → 0.600000 (expected 0.600000) |
| `C03_ODDS_PLUS120` | ✅ PASS | +120 → 0.454545 (expected 0.454545) |
| `C04_NO_VIG_SUM` | ✅ PASS | normalize_no_vig(0.6, 0.55) sum = 1.0000000000 (expected 1.0) |
| `C05_NO_VIG_ZERO` | ✅ PASS | normalize_no_vig(0, 0) raises ValueError: True |
| `C06_BRIER_FIXTURE` | ✅ PASS | brier_score([0.9,0.8],[1,1]) = 0.025000 (expected 0.025) |
| `C07_BSS_REPORT_CONSTANTS` | ✅ PASS | BSS(0.2796, 0.2451) = -0.1408 (expected ≈ -0.141) |
| `C08_BSS_POSITIVE` | ✅ PASS | brier_skill_score(0.22, 0.25) = 0.12 (expected > 0) |
| `C09_BSS_BASELINE_ZERO` | ✅ PASS | brier_skill_score(0.2, 0.0) = None (expected None) |
| `C10_LOG_LOSS_CLIP` | ✅ PASS | log_loss_score([1.0, 0.0], [1, 0]) no crash: True |
| `C11_BRIER_PROB_RANGE` | ✅ PASS | brier_score([1.1], [1]) raises ValueError: True |
| `C12_ECE_RETURNS_DICT` | ✅ PASS | ECE returns dict with required keys: True |
| `C13_RELIABILITY_BINS` | ✅ PASS | reliability_bins returns list[dict] with all required keys: True |
| `C14_COMPARE_KEYS` | ✅ PASS | compare_model_to_market has all required keys: True |
| `C15_PERSISTENCE_USES_SSOT` | ✅ PASS | prediction_persistence.recompute_metrics_from_rows uses metrics SSOT: True |
| `C16_PHASE37_DELEGATES` | ✅ PASS | Phase 37 script imports metrics SSOT: True |
| `C17_PHASE38_DELEGATES` | ✅ PASS | Phase 38 script imports metrics SSOT: True |
| `C18_NO_EXTERNAL_API` | ✅ PASS | metrics.py contains no external API calls: True |

## Details

### C01_ODDS_EVEN
- **Status**: PASS
- **Summary**: +100 → 0.500000 (expected 0.500000)
- **Detail**: american_odds_to_implied_prob('+100') must return exactly 0.5
- **Expected**: `0.5`
- **Actual**: `0.5`

### C02_ODDS_MINUS150
- **Status**: PASS
- **Summary**: -150 → 0.600000 (expected 0.600000)
- **Detail**: american_odds_to_implied_prob('-150') must return 150/250 = 0.6
- **Expected**: `0.6`
- **Actual**: `0.6`

### C05_NO_VIG_ZERO
- **Status**: PASS
- **Summary**: normalize_no_vig(0, 0) raises ValueError: True
- **Detail**: Must raise ValueError, not return a silent fallback
- **Expected**: `True`
- **Actual**: `True`

### C07_BSS_REPORT_CONSTANTS
- **Status**: PASS
- **Summary**: BSS(0.2796, 0.2451) = -0.1408 (expected ≈ -0.141)
- **Detail**: 1 - 0.2796/0.2451 must match REPORT_BSS within 0.001
- **Expected**: `-0.141`
- **Actual**: `-0.14075887392900865`

### C10_LOG_LOSS_CLIP
- **Status**: PASS
- **Summary**: log_loss_score([1.0, 0.0], [1, 0]) no crash: True
- **Detail**: returned 0.000000
- **Expected**: `finite ≥ 0`
- **Actual**: `9.992007221626415e-16`

### C11_BRIER_PROB_RANGE
- **Status**: PASS
- **Summary**: brier_score([1.1], [1]) raises ValueError: True
- **Detail**: Probabilities outside [0, 1] must raise ValueError (not be silently clipped)
- **Expected**: `True`
- **Actual**: `True`

### C12_ECE_RETURNS_DICT
- **Status**: PASS
- **Summary**: ECE returns dict with required keys: True
- **Detail**: keys found: {'n_bins', 'bins', 'ece', 'sample_size'}
- **Expected**: `['bins', 'ece', 'n_bins', 'sample_size']`
- **Actual**: `['bins', 'ece', 'n_bins', 'sample_size']`

### C13_RELIABILITY_BINS
- **Status**: PASS
- **Summary**: reliability_bins returns list[dict] with all required keys: True
- **Detail**: first bin keys: {'bin_upper', 'count', 'bin_lower', 'gap', 'mean_confidence', 'mean_accuracy'}
- **Expected**: `['bin_lower', 'bin_upper', 'count', 'gap', 'mean_accuracy', 'mean_confidence']`
- **Actual**: `['bin_lower', 'bin_upper', 'count', 'gap', 'mean_accuracy', 'mean_confidence']`

### C15_PERSISTENCE_USES_SSOT
- **Status**: PASS
- **Summary**: prediction_persistence.recompute_metrics_from_rows uses metrics SSOT: True
- **Detail**: Source should reference _metrics_brier_score (delegating to metrics.py)
- **Expected**: `True`
- **Actual**: `True`
