# P11 Bullpen / Rest / Weather / Starter Context Key Reconciliation Report

Marker: `P11_BULLPEN_REST_CONTEXT_KEY_RECONCILIATION_READY`

## 1. Scope

Date: 2026-05-11  
Repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
Branch: `main`  
Status: P11 validation completed; production remains blocked.

P11 repaired the P10 context coverage blocker. The root issue was not absence of context data; it was column alias and game key mismatch between the P9/P10 CSV surface and the context builder.

## 2. P10 Baseline

P10 had independent baseball features, but the important context families were effectively unusable:

| Metric | P10 |
|---|---:|
| Context hit rate | 0% |
| Context hit count | 0 |
| Rest / weather / starter coverage | 0% on the critical context path |
| Gate | blocked |

P10 could therefore not prove that bullpen/rest/weather/starter context improved model quality.

## 3. P11 Root Cause and Repair

P11 fixed:

| Problem | Repair |
|---|---|
| Input CSV used `Date`, code expected `date` | `_resolve_col()` resolves aliases |
| Input CSV used `Home`, code expected `home_team` | `_resolve_col()` resolves aliases |
| Input CSV used `Away`, code expected `away_team` | `_resolve_col()` resolves aliases |
| Context rows used MLB-format game IDs | Builder now resolves canonical context lookup keys |
| Win-rate computation depended on fragile input outcome fields | Win rates use as-played CSV with reliable `home_win` |

Additional P11 repair done in this CTO pass:

- Fixed `context_hit_rate` metadata. It previously reported `0.3333` while `context_hit_count/context_miss_count` showed 2402/0. The metadata now uses hit / (hit + miss), so P11 coverage reports `1.0`.
- Updated P11 targeted tests from P10 feature-version expectations to `p11_context_reconciled_v1`.
- Added a unit assertion that no-context rows report `context_hit_rate = 0.0`.

## 4. Feature Coverage After Repair

Source: `outputs/predictions/PAPER/2026-05-11/independent_feature_coverage.json`

| Metric | Value |
|---|---:|
| input_count | 2402 |
| feature_count | 2402 |
| context_hit_count | 2402 |
| context_miss_count | 0 |
| context_hit_rate | 1.0 |
| feature_version | `p11_context_reconciled_v1` |
| date_col_resolved | `Date` |
| home_col_resolved | `Home` |
| away_col_resolved | `Away` |

Feature coverage:

| Feature | Coverage |
|---|---:|
| home_recent_win_rate | 2387/2402 (99.4%) |
| away_recent_win_rate | 2387/2402 (99.4%) |
| home_rest_days | 2284/2402 (95.1%) |
| away_rest_days | 2287/2402 (95.2%) |
| wind_kmh | 2080/2402 (86.6%) |
| temp_c | 2080/2402 (86.6%) |
| starter_era_proxy_home | 2080/2402 (86.6%) |
| starter_era_proxy_away | 2058/2402 (85.7%) |

## 5. Tests

Targeted P11 suite:

```text
.venv/bin/pytest \
  tests/test_mlb_independent_feature_builder.py \
  tests/test_run_mlb_independent_feature_candidate_export.py \
  tests/test_mlb_independent_features.py \
  tests/test_run_mlb_oof_calibration_validation.py \
  tests/test_run_mlb_strategy_simulation_spine.py \
  tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py \
  tests/test_run_mlb_tsl_paper_recommendation_smoke.py -q
```

Result:

```text
117 passed in 11.43s
```

Note: `tests/test_mlb_feature_context_keys.py` and `tests/test_mlb_feature_context_loader.py` were listed in the handoff prompt but do not exist in this checkout. Existing coverage for this slice is in the test files above.

## 6. OOF Calibration Result

Command:

```bash
.venv/bin/python scripts/run_mlb_oof_calibration_validation.py \
  --input-csv outputs/predictions/PAPER/2026-05-11/mlb_odds_with_feature_candidate_probabilities.csv \
  --output-dir outputs/predictions/PAPER/2026-05-11 \
  --n-bins 10 \
  --min-train-size 300 \
  --min-bin-size 30 \
  --initial-train-months 2
```

Result:

| Metric | Value |
|---|---:|
| original_bss | -0.050579 |
| oof_bss | -0.027668 |
| delta_bss | +0.022911 |
| original_ece | 0.081139 |
| oof_ece | 0.042928 |
| delta_ece | -0.038211 |
| oof_row_count | 1949 |
| skipped_row_count | 451 |
| recommendation | `OOF_IMPROVED_BUT_STILL_BLOCKED` |
| deployability_status | `PAPER_ONLY_CANDIDATE` |

CTO read: P11 improved calibration and BSS materially, but BSS remains negative. This is not promotable.

## 7. Strategy Simulation Result

Command:

```bash
.venv/bin/python scripts/run_mlb_strategy_simulation_spine.py \
  --date-start 2025-03-01 \
  --date-end 2025-12-31 \
  --strategy-name moneyline_edge_threshold_v0_p11_context_reconciled_oof \
  --edge-threshold 0.01 \
  --kelly-cap 0.05 \
  --input-csv outputs/predictions/PAPER/2026-05-11/mlb_odds_with_oof_calibrated_probabilities.csv \
  --output-dir outputs/simulation/PAPER/2026-05-11
```

Result:

| Metric | Value |
|---|---:|
| sample_size | 1949 |
| bet_count | 1127 |
| BSS | -0.027668 |
| ECE | 0.042928 |
| ROI proxy | +0.648% |
| gate_status | `BLOCKED_NEGATIVE_BSS` |

Output:

- `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl`
- `outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9_report.md`

CTO read: ROI proxy is positive, but BSS is still negative versus market baseline. The gate is correctly blocked.

## 8. Simulation-Gated Recommendation Result

Command:

```bash
.venv/bin/python scripts/run_mlb_tsl_paper_recommendation.py \
  --date 2026-05-11 \
  --simulation-result-path outputs/simulation/PAPER/2026-05-11/2025-03-01_2025-12-31_moneyline_edge_threshold_v0_p11_context_reconcil_5e6d90f9.jsonl \
  --allow-replay-paper
```

Result:

```text
simulation_gate=LOADED_FROM_PATH(...)
gate_status=BLOCKED_NEGATIVE_BSS
allow_recommendation=False
TSL live probe: HTTP 403 / unavailable
output gate=BLOCKED_SIMULATION_GATE
stake_units_paper=0.0
```

Output:

- `outputs/recommendations/PAPER/2026-05-11/2026-05-11-LAA-CLE-824441.jsonl`

CTO read: the recommendation pipeline is correctly wired to the simulation gate. It can write a paper row, but it blocks issuance and stake when simulation BSS is negative. TSL remains unavailable, so estimated odds are used for paper tracking only.

## 9. Context Safety Audit

Current context files are mostly generated from historical MLB / boxscore / odds ingestion sources, for example:

- `data/mlb_context/bullpen_usage_3d.jsonl`
- `data/mlb_context/injury_rest.jsonl`
- `data/mlb_context/weather_wind.jsonl`
- `data/mlb_context/odds_timeline.jsonl`
- `data/mlb_context_sources/*.jsonl`

Safety classification:

| Context family | Status | CTO note |
|---|---|---|
| as-played win rate | pregame-safe if computed strictly from prior games | Builder uses prior games only |
| starter ERA proxy | pregame-safe if computed strictly from prior starts | Builder uses prior starts only |
| rest days | needs source audit | Stored in historical context generated after games; field may be pregame concept but provenance is post-hoc |
| bullpen usage 3d | needs source audit | Generated from boxscore source; must prove only prior games are used |
| weather / wind | unknown-to-risk | Historical weather may be actual observed weather, not pregame forecast |
| lineups | postgame-risk unless confirmed timestamp is pregame | Do not use for production candidate without timestamp proof |
| closing odds | postgame / closing-only | Useful for settlement and CLV, not pregame recommendation input |

Conclusion: P11 is a valid paper-only candidate, but not a production candidate. P12 must include feature-family safety and ablation before promotion.

## 10. Status Flags

| Flag | Value |
|---|---|
| context hit rate improved | true |
| OOF calibration produced | true |
| simulation produced | true |
| simulation-gated recommendation produced | true |
| production enablement attempted | false |
| real bets placed | false |
| branch protection modified | false |
| replay-default-validation modified | false |
| production_launch_approved | false |
| paper_only | true |

## 11. Current Conclusion

P11 succeeded as a data-quality repair:

- The 0% context coverage blocker is fixed.
- P11 improves OOF BSS from -0.050579 to -0.027668 and ECE from 0.081139 to 0.042928.
- The model still underperforms market baseline, so promotion remains blocked.
- Recommendation gating is correctly conservative: simulation blocks recommendation issuance and stake.
- TSL 403 / unavailable market source remains an external blocker.

P11 is complete, but it is not a green-light. The next step is not production. The next step is P12 feature-family ablation plus context safety validation.

## 12. P12 Direction

Decision rule result:

- OOF BSS <= 0 but improved.
- Context safety is not fully proven.
- TSL remains unavailable / 403.

Therefore:

```text
P12 = feature family ablation + context safety audit + source provenance hardening
```

P12 must isolate whether recent form, rest, bullpen, starter proxy, or weather caused the improvement, and whether any family is unsafe or noisy.

## 13. Next Executable Task Prompt

```text
ROLE
You are Betting-pool's P12 Feature Family Ablation and Context Safety Agent.

MISSION
Use the completed P11 candidate outputs to determine which feature families are useful and safe.

REPO
/Users/kelvin/Kelvin-WorkSpace/Betting-pool

DO
- Build feature-family ablation runs for:
  1. recent win rate only
  2. rest only
  3. bullpen only
  4. starter ERA proxy only
  5. weather only
  6. all safe families excluding unknown-risk weather/lineups
- For each candidate, run OOF calibration and strategy simulation.
- Compare BSS, ECE, ROI proxy, bet_count, drawdown, and gate_status.
- Audit context provenance and classify each feature family as pregame-safe, postgame-risk, or unknown.
- Keep all outputs under PAPER paths.
- Keep production disabled.

DO NOT
- place real bets
- enable production
- claim profitability
- use postgame-only context in a production candidate
- bypass simulation gate

ACCEPTANCE
- P12 report identifies the best safe feature family combination.
- Any negative-BSS candidate remains blocked.
- TSL 403 keeps production NO_GO regardless of simulation result.

MARKER
P12_FEATURE_FAMILY_ABLATION_AND_CONTEXT_SAFETY_READY
```
