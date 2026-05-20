# Phase 59 — Real Bullpen Boxscore Acquisition Report

> Generated: 2026-05-06T03:01:56.999058+00:00  
> Phase version: `phase59_real_bullpen_boxscore_acquisition_v1`  
> Audit hash: `319052672fd1d79f`

---

## § 1. Safety Flags

| Flag | Value |
|------|-------|
| `CANDIDATE_PATCH_CREATED` | `False` |
| `PRODUCTION_MODIFIED` | `False` |
| `ALPHA_MODIFIED` | `False` |
| `DIAGNOSTIC_ONLY` | `True` |

---

## § 2. Input Artifacts

| Artifact | Path |
|----------|------|
| Prediction JSONL | `2025 rows` |
| Bullpen JSONL | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/mlb_context/bullpen_usage_3d.jsonl` |
| Bullpen rows | `2430` |
| Bullpen date range | `2025-03-18` → `2025-09-28` |
| Prediction date range | `2025-04-27` → `2025-09-28` |

---

## § 3. Data Inventory & PIT-Safety Validation

**Bullpen data source**: `mlb_stats_api_boxscore`  
**PIT validated**: `True`  

> Source: mlb_stats_api_boxscore. bullpen_usage_last_3d = Σ(D-1, D-2, D-3) bullpen innings, computed from completed-game boxscores of PRIOR days only. Current game boxscore is stored but D is never included in the lookback. Validated via external_sources.py code review: recent = [(d - timedelta(days=i)) for i in (1, 2, 3)].

| Metric | Value |
|--------|-------|
| Missing home bullpen % | 3.5% |
| Missing away bullpen % | 3.4% |

**PIT Contract** (hard rule): `bullpen_usage_last_3d = Σ(D-1, D-2, D-3) innings pitched`.
The current game's boxscore is never included in its own lookback window.

---

## § 4. Acquisition Method

**Alignment method**: `(game_date, norm(away_team), norm(home_team))`

Game ID format mismatch between prediction JSONL and bullpen JSONL was resolved by
normalizing both team name columns with `re.sub(r'[_\s]+', ' ', s).strip().lower()`,
then joining on `(game_date, norm_away, norm_home)` — no dependency on game_id format.

---

## § 5. Bullpen Feature Schema

| Field | Type | Description | PIT-safe? |
|-------|------|-------------|-----------|
| `bullpen_usage_last_3d_home` | float | Home bullpen IP sum (D-1+D-2+D-3) | ✅ |
| `bullpen_usage_last_3d_away` | float | Away bullpen IP sum (D-1+D-2+D-3) | ✅ |
| `bullpen_fatigue_delta_3d` | float | home - away (positive = home tired) | ✅ |
| `fav_bull_fatigue` | float | Favorite team's fatigue relative to opponent | ✅ |
| `bullpen_available` | bool | Whether real bullpen data exists for this game | ✅ |

**Forbidden features** (never used): `home_win`, `final_score`, `game_result`,
`innings_pitched_today`, `era_after_game`, and all other post-game fields.

---

## § 6. Sample Size & Coverage

| Metric | Value |
|--------|-------|
| Total prediction rows | 2025 |
| Matched with bullpen | 1890 (93.3%) |
| Usable rows (non-null) | 1843 (91.0%) |
| Unmatched rows | 135 |
| Null bullpen values | 47 |

---

## § 7. Heavy-Fav & High-Conf Segment Coverage

| Segment | Total | With Bullpen | Coverage |
|---------|-------|--------------|----------|
| Heavy-fav (fav≥0.70) | 60 | 59 | 98.3% |
| High-conf (fav≥0.65) | — | 185 | 98.4% |

**Prior heavy_fav ECE baseline** (Phase 59-Pre): `0.0779`

---

## § 8. Baseline vs Bullpen Diagnostic

### Heavy-Fav Signal Analysis

n=59, mean_bull_delta=0.01, stdev_bull_delta=4.52

| Segment | n | Fav-win rate |
|---------|---|-------------|
| Tired fav (Δ ≥ +2 IP) | 16 | 0.688 |
| Rested fav (Δ ≤ -2 IP) | 21 | 0.714 |
| Delta (rested - tired) | — | +0.027 |
| Has signal? | — | `True` |

### ECE Comparison (Heavy-Fav)

| Metric | Baseline | Bullpen-adjusted | Δ |
|--------|----------|-----------------|---|
| ECE | 0.1663 | 0.1859 | -0.0196 |
| BSS | 0.3112 | 0.3115 | — |

### ECE Comparison (High-Conf)

| Metric | Baseline | Bullpen-adjusted | Δ |
|--------|----------|-----------------|---|
| ECE | 0.0819 | 0.0869 | -0.0050 |
| BSS | 0.2509 | 0.2545 | — |

---

## § 9. Historical Phase Context

| Phase | Gate | Bullpen Coverage |
|-------|------|-----------------|
| Phase 55 | `BULLPEN_FEATURE_INVESTIGATION` | N/A (investigation) |
| Phase 56 | `DATA_GAP_REMAINS` | 0.0% (neutral_fallback) |
| Phase 59-Pre | `BULLPEN_HYPOTHESIS_RETAINED` | N/A (heavy_fav ECE baseline) |
| **Phase 59** | **`INCONCLUSIVE`** | 98.3% (real data) |

---

## § 10. Gate Conclusion

### Gate: `INCONCLUSIVE`

Directional signal found (Δ_win_rate=0.027) but simple diagnostic adjustment did not improve ECE (0.1663 → 0.1859). Possibly needs: (a) more features, (b) non-linear relationship, (c) more data. Sample size heavy_fav_usable=59 may be limiting.

---

## § 11. Next Steps

INCONCLUSIVE: Collect additional bullpen features (B2B, closer usage) and expand to full season before deciding. Directional signal warrants further investigation.

---

<!-- PHASE_59_REAL_BULLPEN_BOXSCORE_ACQUISITION_VERIFIED -->
