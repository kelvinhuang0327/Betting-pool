# P0+P1+P2 MLB→TSL Live Source & Paper Smoke Report
**Date:** 2026-05-11  
**Agent:** P0+P1+P2 MLB→TSL Live Source Readiness and Recommendation Smoke-Run  
**Final Marker:** `P0_P1_P2_MLB_TSL_LIVE_SOURCE_AND_PAPER_SMOKE_READY`

---

## 1. Repo + Branch + Environment Evidence

| Item | Value |
|------|-------|
| Repo path | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` |
| Branch | `main` |
| Git status | ahead 38, behind 1 (dirty working tree — not cleaned per instructions) |
| Python | `Python 3.13.8` |
| pytest | `pytest 9.0.3` |

```
pwd   → /Users/kelvin/Kelvin-WorkSpace/Betting-pool
branch → main
```

---

## 2. Live Source Diagnostic

### MLB Stats API — READY ✅

- **Endpoint:** `https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-05-11`
- **HTTP status:** 200
- **Games today (2026-05-11):** 6 games returned
- **First game:** `gamePk=824441` — Los Angeles Angels @ Cleveland Guardians, 22:10 UTC (Scheduled)
- **No fallback to replay**: `data/mlb_live_pipeline.fetch_schedule()` hits the live API directly; it only falls back to local JSON cache (TTL=300s for in-progress, 86400s for final). No replay pathway in the MLB live pipeline.

**Root cause of "today/current fallback":** The WBC `replay_build_registry.py` fallback is scoped exclusively to WBC matches (Pool A/B/C/D). The MLB live pipeline (`mlb_live_pipeline.py`) does **not** fall back to replay — it returns an empty list if the API call fails. Since the API is reachable today, there is no fallback.

### TSL Crawler V2 — BLOCKED ❌

- **Modern blob URL:** `https://blob3rd.sportslottery.com.tw/apidata/...` → **HTTP 403 Forbidden**
- **Legacy API:** `https://www.sportslottery.com.tw/api/v1/game/list` → **HTTP 403 Forbidden**
- **Frontend probe:** Unable to locate TSL frontend bundle URL
- **Diagnosis:** TSL blocks automated access with 403 on both endpoints. This is not a code bug — it is an external auth/rate-limit policy change. The curl fallback in `_request_json_via_curl` also receives 403. **Not fixable in < 50 LoC** without session cookie injection or API key.

### Env vars / config flags / cache TTLs involved

| Variable | Location | Value / Role |
|----------|----------|--------------|
| `_CACHE_TTL_SECONDS` | `mlb_live_pipeline.py` | 300s (in-progress games) |
| `_FINAL_CACHE_TTL` | `mlb_live_pipeline.py` | 86400s (completed games) |
| `use_mock` | `TSLCrawlerV2.__init__` | `False` (live mode) |
| `deployment_mode` | `MLBLeagueAdapter.rules()` | `"paper"` (hard-coded) |
| `_MLB_PAPER_ONLY` | `run_mlb_tsl_paper_recommendation.py` | `True` (hard gate) |

---

## 3. Patch Summary

**No patch applied.**

- **MLB live source**: Already works correctly — `fetch_schedule()` returns 6 real games today with HTTP 200.
- **TSL live source**: HTTP 403 on all endpoints. Root cause is external server-side auth policy. A real fix would require session cookie extraction or API key provisioning — neither is safe to implement in < 50 LoC. **Blocker documented.**

---

## 4. Recommendation Row Contract

**File:** `wbc_backend/recommendation/recommendation_row.py`  
**Class:** `MlbTslRecommendationRow`

| Field | Type | Notes |
|-------|------|-------|
| `game_id` | `str` | `{date}-{away}-{home}-{gamePk}` |
| `game_start_utc` | `datetime` | UTC-aware datetime |
| `model_prob_home` | `float` | [0.0, 1.0] validated |
| `model_prob_away` | `float` | [0.0, 1.0] validated |
| `model_ensemble_version` | `str` | e.g. `v1-mlb-moneyline-trained` |
| `tsl_market` | `Literal[...]` | `moneyline`, `run_line`, `total`, `f5`, `f5_total`, `odd_even` |
| `tsl_line` | `Optional[float]` | spread / total line |
| `tsl_side` | `Literal[...]` | `home`, `away`, `over`, `under`, `odd`, `even` |
| `tsl_decimal_odds` | `float` | decimal format |
| `edge_pct` | `float` | model_prob − implied_prob |
| `kelly_fraction` | `float` | capped at 5% in paper mode |
| `stake_units_paper` | `float` | kelly × 100 units |
| `gate_status` | `Literal[...]` | 9 valid statuses |
| `gate_reasons` | `list[str]` | default `[]` |
| `paper_only` | `bool` | default `True`; raises `ValueError` if `False` |
| `generated_at_utc` | `datetime` | auto-filled |
| `source_trace` | `dict` | data source provenance |

**Methods:** `to_dict()` (ISO-8601 datetimes), `to_jsonl_line()` (no trailing newline)

**Hard-gate invariants (enforced in `__post_init__`):**
- `paper_only` must be `True` — raises `ValueError` otherwise
- `gate_status` must be in `VALID_GATE_STATUSES` — raises `ValueError` otherwise
- Both probs must be in [0, 1]

---

## 5. Smoke Run Result

**Mode:** LIVE (MLB live source used — no replay fallback)  
**TSL:** BLOCKED_TSL_SOURCE (403 Forbidden)

**Stdout output:**
```
Error fetching TSL data: modern_fetch_failed=HTTP Error 403: Forbidden; frontend_probe_failed=Unable to locate TSL frontend bundle URL; legacy_fetch_failed=HTTP Error 403: Forbidden
[PAPER-ONLY] LIVE | 2026-05-11-LAA-CLE-824441 | home_prob=0.5403 | market=moneyline | side=home | odds=1.8886 | edge=0.0108 | kelly=0.0000 | stake=0.0u | gate=BLOCKED_TSL_SOURCE | output=/Users/kelvin/Kelvin-WorkSpace/Betting-pool/outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl
```

**Output file:** `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

**Output content:**
```json
{
  "game_id": "2026-05-11-LAA-CLE-824441",
  "game_start_utc": "2026-05-11T22:10:00+00:00",
  "model_prob_home": 0.540299,
  "model_prob_away": 0.459701,
  "model_ensemble_version": "v1-mlb-moneyline-trained",
  "tsl_market": "moneyline",
  "tsl_line": null,
  "tsl_side": "home",
  "tsl_decimal_odds": 1.8886,
  "edge_pct": 0.010806,
  "kelly_fraction": 0.0,
  "stake_units_paper": 0.0,
  "gate_status": "BLOCKED_TSL_SOURCE",
  "gate_reasons": [
    "BLOCKED: TSL live source unavailable (403 Forbidden)",
    "TSL live: 0 games returned (possible 403 or empty market)",
    "TSL live source unavailable — estimated odds used"
  ],
  "paper_only": true,
  "generated_at_utc": "2026-05-11T02:42:59.824947+00:00",
  "source_trace": {
    "mlb_api": "statsapi.mlb.com/api/v1",
    "tsl_live": false,
    "tsl_note": "TSL live: 0 games returned (possible 403 or empty market)",
    "model_version": "v1-mlb-moneyline-trained",
    "paper_only_reason": "CLV 仍為代理值（無真實歷史賠率時間軸）；無 Statcast pitch-level 數據；Brier Skill Score = -14.1%（模型落後市場基準）"
  }
}
```

**Model used:** `v1-mlb-moneyline-trained` (fitted on `data/mlb_2025/mlb_odds_2025_real.csv`)  
**Kelly = 0.0 / Stake = 0.0**: Correct — gate is `BLOCKED_TSL_SOURCE`, so no real position recommended.

---

## 6. Test Results

**Command:** `.venv/bin/pytest tests/test_recommendation_row_contract.py tests/test_run_mlb_tsl_paper_recommendation_smoke.py -q`

```
...........................
27 passed in 0.66s
```

### Test names

**`tests/test_recommendation_row_contract.py`** (21 tests):
- `TestFieldPresence::test_all_required_fields_exist`
- `TestDefaults::test_paper_only_default_is_true`
- `TestDefaults::test_paper_only_cannot_be_false`
- `TestDefaults::test_gate_reasons_defaults_empty_list`
- `TestDefaults::test_source_trace_defaults_empty_dict`
- `TestToDict::test_to_dict_returns_dict`
- `TestToDict::test_to_dict_game_id`
- `TestToDict::test_to_dict_datetimes_are_strings`
- `TestToDict::test_to_dict_model_probs`
- `TestToDict::test_to_dict_paper_only_true`
- `TestToDict::test_to_dict_all_required_fields_present`
- `TestToJsonlLine::test_to_jsonl_line_is_valid_json`
- `TestToJsonlLine::test_to_jsonl_line_no_trailing_newline`
- `TestToJsonlLine::test_to_jsonl_roundtrip_game_id`
- `TestGateStatus::test_all_valid_gate_statuses_accepted`
- `TestGateStatus::test_invalid_gate_status_raises`
- `TestGateStatus::test_blocked_paper_only_is_valid`
- `TestGateStatus::test_pass_is_valid`
- `TestProbabilityValidation::test_home_prob_out_of_range_raises`
- `TestProbabilityValidation::test_away_prob_out_of_range_raises`
- `TestProbabilityValidation::test_boundary_probabilities_accepted`

**`tests/test_run_mlb_tsl_paper_recommendation_smoke.py`** (6 tests):
- `TestSmokeOneRowProduced::test_smoke_produces_one_row`
- `TestSmokeOneRowProduced::test_smoke_paper_only_is_true`
- `TestSmokeOneRowProduced::test_smoke_output_file_written_under_paper_path`
- `TestSmokeOneRowProduced::test_smoke_replay_suffix_when_flagged`
- `TestSmokeOneRowProduced::test_smoke_gate_status_blocked_when_tsl_down`
- `TestScriptRefusals::test_refuses_when_no_games_without_allow_flag`

---

## 7. Status Flags

| Flag | Status |
|------|--------|
| **live MLB source ready today** | ✅ **true** — 6 games, HTTP 200, `statsapi.mlb.com` reachable |
| **live TSL source ready today** | ❌ **false** — HTTP 403 on all endpoints (external blocker) |
| **recommendation row contract landed** | ✅ **true** — `wbc_backend/recommendation/recommendation_row.py` |
| **paper smoke produced** | ✅ **true** — `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl` |
| **production enablement attempted** | ✅ **false** (must be false) |
| **replay-default-validation modified** | ✅ **false** (must be false) |
| **branch protection modified** | ✅ **false** (must be false) |
| **LotteryNew touched** | ✅ **false** (must be false) |

---

## 8. Blockers for Tomorrow's P3 (Strategy Simulation Spine)

1. **TSL live odds blocked (403)** — Without real TSL odds, `edge_pct` and `kelly_fraction` are estimated. Phase 6C team name bridge (Chinese → 3-letter) is incomplete. P3 walk-forward backtest requires either: (a) TSL access restored, or (b) a historical odds CSV covering MLB games.

2. **Brier Skill Score = −14.1%** — The moneyline model underperforms market baseline. Walk-forward backtest will need a regime-gated model (the `mlb_regime_paper` model exists but requires feature rebuild from phase 48–72).

3. **No Statcast pitch-level data** — The MLB moneyline model uses market-implied probs as features (circular). Proper feature engineering needs pitch-velocity / spin-rate / xFIP data (Phase 48 feature builder partially built in `scripts/run_phase48_p0_feature_builder.py`).

4. **CLV pipeline incomplete** — `data/derived/odds_snapshots_2026-04-29.jsonl` exists but carries `LEAGUE_INFERRED` flag; team-name normalization table (Phase 6C) is needed to join predictions to real CLV.

5. **Model output contract not fully validated** — `scripts/validate_model_output_contract.py` exists but the contract validation summary shows `LEAGUE_INFERRED` issues.

---

## 9. CEO-Readable Summary

**P0**: MLB live source is ready today (6 games, API reachable) — no fallback to replay. TSL live source is blocked (403 Forbidden) on all endpoints — external blocker, not a code bug, not fixable in < 50 LoC.  
**P1**: `MlbTslRecommendationRow` dataclass contract is live in `wbc_backend/recommendation/recommendation_row.py` with full validation, serialisation, and 21 passing unit tests.  
**P2**: One paper recommendation produced — `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl` — LAA @ CLE, home_prob=0.5403, gate=BLOCKED_TSL_SOURCE, stake=0.0u (correctly blocked). Production enablement is still NO_GO. Next task: P3 strategy simulation spine.
