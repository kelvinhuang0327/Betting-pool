# Active Task — P83D 2026 Upstream Data Availability Probe + Producer Activation Gate

> **[COMPLETED 2026-05-26]** `P83D_AWAITING_UPSTREAM_DATA`
> **Issued by**: P83C handoff (P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA, commit `01a38c4`)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=True`
>
> **P83D Result:** Local filesystem probe for upstream 2026 MLB data.
> Zero API calls made. Probe confirmed: no canonical 2026 schedule, pitcher FIP, or model output files.
> 6 readiness gates evaluated: GOVERNANCE_GATE=PASS (constants); remaining 5 gates FAIL.
>
> **Gate results (6 gates):**
> - SCHEDULE_GATE: FAIL — no data/mlb_2026/schedule/ with game_date + team identifiers
> - PITCHER_FEATURE_GATE: FAIL — no home_sp_fip / away_sp_fip for 2026 games
> - MODEL_OUTPUT_GATE: FAIL — no canonical model_probability in P83B schema format
> - PREDICTED_SIDE_GATE: FAIL — blocked by PITCHER_FEATURE_GATE (logic defined but data absent)
> - GOVERNANCE_GATE: PASS — constants always available
> - PRODUCER_ACTIVATION_GATE: FAIL — 4 prerequisite gates failing
>
> **Runtime PAPER files (noncanonical):**
> - outputs/recommendations/PAPER/2026-05-11/ has game_id + model_prob_home/away
> - Missing: game_date, home_team, away_team, sp_fip_delta, source_prediction_version (P83B format)
> - Classification: runtime_paper_candidate = noncanonical per P83B
>
> **Missing data checklist (3 HIGH priority items):**
> 1. data/mlb_2026/schedule/mlb_2026_schedule.jsonl (game_id, game_date, home_team, away_team)
> 2. data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl (home_sp_fip, away_sp_fip)
> 3. data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl (model_probability, source_prediction_version)
>
> **P83E trigger:** Rerun when all 3 HIGH priority missing items exist locally.
> **Forbidden scan:** CLEAN (0 violations) | live_api_calls=0
>
> **Output artifacts:**
> - `scripts/_p83d_2026_upstream_data_availability_probe.py`
> - `tests/test_p83d_2026_upstream_data_availability_probe.py`
> - `data/mlb_2026/derived/p83d_2026_upstream_data_availability_probe_summary.json`
> - `report/p83d_2026_upstream_data_availability_probe_20260526.md`
>
> **Tests:** 37 PASS (P83D) + 986 PASS (P72A→P83D full regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P83D_AWAITING_UPSTREAM_DATA`

---

# Prior Active Task — P83C 2026 Prediction Schema Producer Contract

> **[COMPLETED 2026-05-26]** `P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA`
> **Issued by**: P83B handoff (P83B_INGEST_CONTRACT_READY_AWAITING_DATA)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=True`
>
> **P83C Result:** 2026 prediction schema producer contract defined.
> No upstream data fetched. Schema-only dry-run validates 19-field schema in-memory.
> Snapshot unlock blocked (0 real rows in canonical path).
>
> **Contract deliverables:**
> - Upstream input contract: P83C_UPSTREAM_INPUT_CONTRACT_V1 (5 input groups, AWAITING)
> - Producer output schema: P83C_PRODUCER_OUTPUT_SCHEMA_V1 (19 required fields, jsonl)
> - Rule flag computation: P83C_RULE_FLAG_COMPUTATION_CONTRACT_V1 (5 cases, all deterministic)
> - Schema-only dry-run: 4 MOCK_SCHEMA_ONLY rows validated in-memory, not written to canonical
> - P83D prompt generated: triggers when upstream 2026 FIP data + schedule available
> - Forbidden scan: CLEAN (0 violations)
>
> **Output artifacts:**
> - `scripts/_p83c_2026_prediction_schema_producer_contract.py`
> - `tests/test_p83c_2026_prediction_schema_producer_contract.py`
> - `data/mlb_2026/derived/p83c_2026_prediction_schema_producer_contract_summary.json`
> - `report/p83c_2026_prediction_schema_producer_contract_20260526.md`
> - `00-BettingPlan/20260526/p83c_2026_prediction_schema_producer_contract_20260526.md`
>
> **Tests:** 38 PASS (P83C) + regression suite PASS
> **Forbidden scan:** 0 violations
> **Classification:** `P83C_SCHEMA_PRODUCER_READY_AWAITING_UPSTREAM_DATA`

---

# Active Task — P83B 2026 Prediction Data Ingest Contract / Awaiting Stub

> **[COMPLETED 2026-05-26]** `P83B_INGEST_CONTRACT_READY_AWAITING_DATA`
> **Issued by**: P83A handoff (P83A_AWAITING_2026_DATA)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=True`
>
> **P83B Result:** Full 2026 prediction data ingest contract defined.
> No live data processed. No market edge computed. Contract only — awaiting first 2026 rows.
>
> **Contract deliverables:**
> - Canonical paths (4 defined): `data/mlb_2026/predictions/mlb_2026_prediction_rows.jsonl` (primary)
> - Runtime PAPER output classified as NON_CANONICAL (lacks sp_fip_delta); adapter deferred
> - Row schema V1: 19 required fields + 5 optional outcome fields (P83B_2026_PREDICTION_ROW_SCHEMA_V1)
> - New fields vs 2025: rule_primary_125_flag, rule_shadow_100_flag, tier_b_candidate_flag, tier_a_watchlist_flag
> - 2025→2026 extension contract: no retraining required, no live API required; FIP formula preserved
> - Validator: P83B_ROW_VALIDATOR_V1 (8 checks: required fields, season=2026, governance, abs_fip tolerance, rule flags, no odds, outcomes pending, is_correct validation)
> - Snapshot triggers: smoke n=1, sample_limited n=10, checkpoint_1 n=50, checkpoint_2 n=100, operational n=200
> - P83C prompt generated: trigger = n≥1 rows in canonical JSONL
> - 2025 baseline reference: HOME_PLUS_AWAY_125 hit=0.6392, AUC=0.5787, n=316
> - P82 market-edge: BLOCKED_NO_REAL_DATASET (unchanged)
> - Forbidden scan: CLEAN (0 violations)
>
> **Output artifacts:**
> - `scripts/_p83b_2026_prediction_data_ingest_contract.py`
> - `tests/test_p83b_2026_prediction_data_ingest_contract.py`
> - `data/mlb_2026/derived/p83b_2026_prediction_data_ingest_contract_summary.json`
> - `report/p83b_2026_prediction_data_ingest_contract_20260526.md`
> - `00-BettingPlan/20260526/p83b_2026_prediction_data_ingest_contract_20260526.md`
>
> **Tests:** 67 PASS (P83B) + 830 PASS (P72A→P83A regression) = 897 total
> **Forbidden scan:** 0 violations
> **Classification:** `P83B_INGEST_CONTRACT_READY_AWAITING_DATA`

---

## Prior Active Task: P83A 2026 Live Accumulation First Snapshot / Awaiting Contract

> **[COMPLETED 2026-05-26]** `P83A_AWAITING_2026_DATA`
> **Issued by**: P82C handoff (P82C_STAGING_GUARD_DRYRUN_READY)
> **Branch**: `main` | **Mode**: `paper_only=true`
>
> **P83A Result:** Searched all local candidate paths for 2026 prediction-only rows
> (sp_fip_delta schema). No qualifying rows found → formal awaiting-data contract issued.
>
> **Discovery result:**
> - `data/mlb_2026/` does not exist (primary canonical path)
> - `outputs/recommendations/PAPER/2026-05-11/` contains 1 runtime file (LAA-CLE)
>   but uses market-pipeline schema (no sp_fip_delta / predicted_side) — NOT P83A-qualifying
> - Total 2026 rows with required schema: 0
>
> **Awaiting-data contract:**
> - Expected path: `data/mlb_2026/predictions/mlb_2026_prediction_only_sp_fip_delta_v1.jsonl`
> - Thresholds: smoke n=1 / sample_limited n=10 / checkpoint_1 n=50 / checkpoint_2 n=100 / operational n=200
> - Rerun trigger: any file matching P83A schema in data/mlb_2026/ or outputs/online_validation/
> - Primary rule: TIER_C_HOME_PLUS_AWAY_125 | Shadow: TIER_C_HOME_PLUS_AWAY_100
> - P82 market-edge: BLOCKED — requires external legal odds dataset
> - Next phase: P83B (ingest contract definition)
>
> **Tests:** 46 PASS (P83A) + 784 PASS (P72A→P82C regression) = 830 total
> **Forbidden scan:** 0 violations
> **Classification:** `P83A_AWAITING_2026_DATA`

---

## Prior Active Task: P82C Staging Guard Enforcement Dry-Run + Policy Drift Scanner

> **[COMPLETED 2026-05-26]** `P82C_STAGING_GUARD_DRYRUN_READY`
> **Issued by**: P82B handoff (P82B_RAW_PAID_DATA_POLICY_READY)
> **Branch**: `main` | **Mode**: `paper_only=true`
>
> **P82C Result:** Staging guard dry-run scanner implemented from P82B contract.
> All 6 P82B guard rules implemented as executable scanner functions.
> Current repo scan: STAGE_CLEAN — no staged violations, no real odds files.
>
> **Guard rules implemented:**
> - BLOCK_ENV_FILE → BLOCK_SECRET
> - BLOCK_API_KEY_PATTERN → BLOCK_SECRET (with redaction)
> - BLOCK_RAW_PAID_CSV → BLOCK_RAW_PAID_DATA (data/ prefix + filename pattern)
> - BLOCK_REAL_ODDS_FILENAME → BLOCK_RAW_PAID_DATA
> - BLOCK_CONTAINS_API_KEY_FLAG → BLOCK_SECRET
> - BLOCK_ROW_LEVEL_ODDS → BLOCK_ROW_LEVEL_LEAKAGE
>
> **Mock fixture results (8/8 PASS):**
> - 6 risky fixtures → correct guard states
> - 2 safe fixtures (derived summary + policy report) → STAGE_CLEAN
> - All in-memory only, no real files created
>
> **Current repo dry-run:**
> - Staged files: 0 violations → STAGE_CLEAN
> - Allowlisted paths (P-series JSONs): 0 violations → STAGE_CLEAN
> - Working tree runtime files: RUNTIME_OUT_OF_SCOPE (no forbidden patterns)
> - Overall: STAGE_CLEAN
>
> **P82 status:** BLOCKED_NO_REAL_DATASET (unchanged)
> P-series contract files exempt from filename-based rules via `_is_pseries_contract()`.
>
> **Tests:** 50 PASS (P82C) + 734 PASS (P72A→P82B regression) = 784 total
> **Forbidden scan:** 0 violations
> **Classification:** `P82C_STAGING_GUARD_DRYRUN_READY`

---

## Prior Active Task: P82B Raw Paid Odds Data Storage / Commit Policy Contract

> **[COMPLETED 2026-05-26]** `P82B_RAW_PAID_DATA_POLICY_READY`
> **Issued by**: P82A handoff (P82A_REAL_LEGAL_ODDS_INTAKE_GATE_READY, commit `555b52a`)
> **Branch**: `main` | **Mode**: `paper_only=True | diagnostic_only=True | NO_REAL_BET=True`
>
> **P82B Result:** Raw paid odds data storage and commit policy contract defined.
> No real odds files created. No API calls. No EV/CLV/Kelly computed.
> P82 remains BLOCKED_NO_REAL_DATASET.
>
> **Contract summary:**
> - 9 artifact classes defined (RAW_PAID_ODDS_DATA → MOCK_FIXTURE)
> - RAW_PAID_ODDS_DATA: can_commit=False, local_external_only
> - Commit policy matrix: 9 entries with can_commit, storage_location, stop_condition per class
> - Staging guard: 6 rules (BLOCK_ENV_FILE, BLOCK_API_KEY_PATTERN, BLOCK_RAW_PAID_CSV, BLOCK_REAL_ODDS_FILENAME, BLOCK_CONTAINS_API_KEY_FLAG, BLOCK_ROW_LEVEL_ODDS) → 6 guard states
> - Manifest integration: 4 allowed raw_data_policy values (LOCAL_ONLY_HASH_COMMITTED / DERIVED_ONLY_COMMIT / COMMIT_ALLOWED_LICENSE_VERIFIED / MOCK_ONLY); 4 forbidden (UNKNOWN / COMMIT_RAW_PAID_DATA / EMBED_SECRET / UNLICENSED_SOURCE)
> - Future workflow: 7 steps (acquire → store local → manifest+checksum → P81 validate → commit derived only → P82 dry-run → hard forbidden rule)
> - Forbidden scan: PASS (0 violations) | live_api_calls=0 | p82_unlocked=False
> - 69/69 tests PASS | Full regression: 679/679 PASS (P72A→P82B)
> - **P82 unlock status**: BLOCKED_NO_REAL_DATASET
> - **Commit**: `816c3df`

---

# Previous: P82A Real Legal Odds Dataset Intake Gate

> **[COMPLETED 2026-05-26]** `P82A_REAL_LEGAL_ODDS_INTAKE_GATE_READY`
> **Issued by**: P81 handoff (P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY, commit `da626c9`)
> **Branch**: `main` | **Mode**: `paper_only=True | diagnostic_only=True | NO_REAL_BET=True`
>
> **P82A Result:** Intake gate and blocker closure plan defined. No real odds pulled.
> No EV/CLV/Kelly computed. P82 remains BLOCKED_NO_REAL_DATASET.
>
> **Contract summary:**
> - 23-field intake manifest schema (requires dataset_type=REAL_LEGAL_ODDS_DATASET, source_license_status=LEGAL_OR_LICENSED, contains_api_key=False)
> - Allowed raw_data_policy: COMMIT_ALLOWED / LOCAL_ONLY_HASH_COMMITTED / DERIVED_ONLY_COMMIT
> - 12 blockers: 10 BLOCKED_PENDING_REAL_DATASET, 2 ACTIVE_GUARDRAIL
> - Unlock decision function: 7 conditions; 8 scenarios tested; only REAL_LEGAL passes
> - P82 dry-run scope: 6 allowed, 9 prohibited; CLV BLOCKED_UNTIL_P83
> - Source artifacts: 13/13 present (P72A→P81)
> - Forbidden scan: PASS (0 violations) | live_api_calls=0 | p82_unlocked=False
> - 69/69 tests PASS | Full regression: 664/664 PASS (P72A→P82A)
> - **P82 unlock status**: BLOCKED_NO_REAL_DATASET
> - **Commit**: `555b52a`

---

# Previous: P81 Legal Odds Dataset Validator Contract

> **[COMPLETED 2026-05-26]** `P81_VALIDATOR_CONTRACT_READY_MOCK_ONLY`
> **Issued by**: P80 handoff (P80_MARKET_EDGE_REENTRY_CONTRACT_READY, commit `ecbcc37`)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P81 Result:** Legal odds dataset schema, legality, and policy validator implemented.
> No real odds pulled. No EV/CLV/Kelly computed. Validator ready; awaiting real legal dataset.
>
> **Contract summary:**
> - 5 validator input types defined (REAL_LEGAL_ODDS_DATASET / MOCK / UNKNOWN / SCRAPING_PROHIBITED / RAW_PAID_UNPOLICIED)
> - Only REAL_LEGAL_ODDS_DATASET can unlock P82 (not available yet)
> - 21-field P80 schema validator implemented with type and range rules
> - 5 validator gates: LEGALITY, RAW_DATA_POLICY, TIMESTAMP, MONEYLINE, IDENTITY
> - Valid mock fixture: schema PASS, all gates PASS, P82 unlock=False
> - Invalid mock fixture: LEGALITY_GATE + RAW_DATA_POLICY_GATE both FAIL (expected)
> - 9 output decision states defined; current=BLOCKED_NO_REAL_DATASET
> - Forbidden scan: PASS (0 violations) | live_api_calls=0
> - 64/64 tests PASS | Full regression: 595/595 PASS (P72A→P81)
> - **Commit**: `da626c9`

---

# Previous: P80 Market-Edge Lane Re-entry Readiness Contract

> **[COMPLETED 2026-05-26]** `P80_MARKET_EDGE_REENTRY_CONTRACT_READY`
> **Issued by**: P79B handoff (P79B_TIER_B_FIXTURE_RESEARCH_ONLY)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P80 Result:** Contract-only phase. Defines readiness gates and data contract required
> before market-edge lane may resume. No odds pulled, no EV/CLV/Kelly computed.
>
> **Contract summary:**
> - 6 active market-edge blockers (EDGE_STABLE_NEGATIVE, NO_LEGAL_2024_ODDS, ODDSPORTAL_TOS, API_KEY_MISSING, RAW_DATA_POLICY_MISSING, PRODUCTION_GOVERNANCE)
> - 21-field legal odds data contract defined (schema, legality, timestamp, side-mapping requirements)
> - 4 candidates: primary_125 (ELIGIBLE), shadow_100 (ELIGIBLE), tier_b_conditional (CONDITIONAL), baseline_50 (BENCHMARK)
> - 6 validation gates (A→B→C→D→E→F) defined; Gate F (governance) currently open; Gates A-E blocked
> - Future path: P81 (validator) → P82 (edge dry-run) → P83 (CLV) → P84 (cross-year synthesis)
> - Prediction-only lane remains ACTIVE; Tier B remains RESEARCH_ONLY
> - Forbidden scan: PASS (0 violations) | live_api_calls=0
> - 53/53 tests PASS | Full regression: 531/531 PASS (P72A→P80)
> - **Commit**: `ecbcc37`

---

# Previous: P79B Tier B vs Tier C Comparison Harness Fixture Dry-Run

> **[COMPLETED 2026-05-26]** `P79B_TIER_B_FIXTURE_RESEARCH_ONLY`
> **Issued by**: P79A handoff (P79A_TIER_B_TRIGGER_READINESS_CONTRACT_READY)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P79B Result:** Comparison harness implemented and validated on 2025 fixture frozen snapshot.
> Tier B (n=219, abs_fip∈[0.25,0.50)): hit_rate=0.534, AUC=0.552, stability=MODERATE.
> Primary 125 (n=247): hit_rate=0.583, AUC=0.570. Gate fails on `performance_ok`.
> Fixture classification: TIER_B_RESEARCH_ONLY_FIXTURE (not a 2026 live claim).
>
> **Contract summary:**
> - 4 candidates: tier_b, primary_125, shadow_100, baseline_50
> - 10 metrics per candidate: n, hit_rate (+ CI), AUC (+ CI), Brier, log_loss, ECE, monthly stability, rolling 100, home/away split, concentration risk
> - 6-condition operational research gate (gate fails on `performance_ok`)
> - Future P79 execution prompt generated (trigger: 2026 live Tier B n≥200)
> - Market-edge lane: blocked (deferred to P80)
> - Forbidden scan: PASS (0 violations)
> - **Commit**: `520206c`

---

# Previous Task — P79A Tier B Trigger Readiness + 2026 Live Data Intake Contract

> **[COMPLETED 2026-05-26]** `P79A_TIER_B_TRIGGER_READINESS_CONTRACT_READY`
> **Issued by**: P78 handoff (P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P79A Result:** Tier B trigger readiness contract defined + 2026 live data intake contract.
> State machine: 6 states (NOT_READY → EARLY_OBSERVATION → ACCUMULATING → TRIGGER_READY → FROZEN/REJECTED).
> Fixture confirms trigger fires at 2025-07 (cumulative Tier B n=219 ≥ 200).
>
> **Contract summary:**
> - Intake row contract: 30 fields, governance enforcement (paper_only=True, production_ready=False)
> - Tier B trigger states: 6 (trigger threshold n=200)
> - Comparison metrics: 18 (Tier B vs Tier C finalists)
> - Handoff package schema: 13 required fields (schema p79a-v1)
> - Fixture trigger month: 2025-07 (n=219), frozen snapshot generated
> - Snapshot ID: tier_b_snapshot_2025_202507
> - Market-edge lane: blocked (deferred to P80)
> - Forbidden scan: PASS (0 violations)
>
> **Tests:** 60/60 PASS (P79A) + 328/328 PASS (regression P72A→P78) = 388 total
> **Commit**: `be682ea`

---

# Previous Task — P78 Monthly Rule Monitoring Template + Shadow Tracker Report Pack

> **[COMPLETED 2026-05-26]** `P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY`
> **Issued by**: P77 handoff (P77_SHADOW_TRACKER_CONTRACT_READY)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P78 Result:** Monthly monitoring template defined, validated against 2025 fixture data.
> Template produces monthly reports for all 4 tracking lanes with governance-frozen schema.
>
> **Template summary:**
> - Schema: 7 sections, 42 fields per monthly report (p78-v1)
> - Fixture period: 2025-04 through 2025-09 (6 months validated)
> - Alert levels: GREEN / YELLOW / RED (sample limitation ≠ model failure)
> - Primary lane: TIER_C_HOME_PLUS_AWAY_125 (primary_total_n=407 over fixture)
> - Shadow lane: TIER_C_HOME_PLUS_AWAY_100 (shadow_total_n=445 over fixture)
> - Tier B cumulative at 2025-09: 363 ≥ 200 → **Tier B n≥200 trigger fires in fixture!**
> - Tier A watchlist: cumulative 24 through fixture period (watchlist_only)
> - Market-edge lane: blocked (P80 deferred)
>
> **Key fixture findings:**
> - Primary avg monthly hit_rate: 0.5814 (across 6 months)
> - Shadow avg monthly hit_rate: 0.5771
> - Primary monthly hit range: 0.50 (April n=14) to 0.6508 (September n=63)
> - Rolling 100 ranged 0.55–0.61 in months with sufficient sample
>
> **Pack synthesis:** All 6 months schema-valid | All 6 months governance-clean
>
> **Research Roadmap:** P79 (Tier B n≥200, expected ~2026-09 for live 2026 data) → P80 (Odds-Lane) → P81 (Finalize)
>
> **Tests:** 73 PASS (P78) + 255 PASS (P72A→P77 regression) = 328 total
> **Forbidden scan:** 0 violations (governance invariants verified directly)
> **Classification:** `P78_MONTHLY_SHADOW_TRACKER_TEMPLATE_READY`

---

# Prior Active Task — P77 2026 Prediction-Only Shadow Tracker Contract

> **[COMPLETED 2026-05-26]** `P77_SHADOW_TRACKER_CONTRACT_READY`
> **Issued by**: P76 handoff (P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA)
> **Branch**: `main` | **Mode**: `paper_only=true | diagnostic_only=true | NO_REAL_BET=true`
>
> **P77 Result:** Formal 2026 shadow tracker contract defined and validated.
> P76 dual-finalist decision verified (score_125=0.5543, score_100=0.5540, delta=0.0003 < threshold=0.02).
>
> **Contract summary:**
> - Row schema: 28 fields, 8 governance booleans frozen (paper_only=True, production_ready=False, etc.)
> - Primary tracking rule: `TIER_C_HOME_PLUS_AWAY_125` (home threshold=0.50, away threshold=1.25)
> - Shadow tracking rule: `TIER_C_HOME_PLUS_AWAY_100` (home threshold=0.50, away threshold=1.00)
> - Tier B accumulation: abs_sp_fip_delta in [0.25, 0.50) → P78 trigger at n≥200 (~2026-09)
> - Tier A watchlist: abs_sp_fip_delta ≥ 1.50 → track only, no operationalization before n≥50
> - Market-edge lane: DEFERRED (blocked in P77, requires odds API key for P80)
>
> **Semantic validation:** PASS — counts match P75B (HOME_ONLY=268, AWAY_100=373, AWAY_125=316)
>
> **Monthly metrics:** n, hit_rate, CI-95, AUC, Brier, ECE, home/away split, rolling-100
> **Re-evaluation triggers:** n≥50, n≥100, n≥200, end-of-season; downgrade on rolling-100 < 0.55
> **Downgrade criteria:** rolling_100_floor, consecutive_monthly_floor, ece_worsening
>
> **Research Roadmap:** P78 (Tier B n≥200 trigger ~2026-09) → P79 (Combined) → P80 (Odds-Lane) → P81 (Finalize)
>
> **Tests:** 69 PASS (P77) + 186 PASS (P72A→P76 regression) = 255 total
> **Forbidden scan:** 0 violations (governance invariants verified directly)
> **Classification:** `P77_SHADOW_TRACKER_CONTRACT_READY`

---

## Prior Active Task: P76 Corrected Tier C Final Rule Selection + 2026 Accumulation Plan

> **[COMPLETED 2026-05-26]** `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA`
> **Issued by**: P75B handoff (P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE)
> **Branch**: `main` | **Mode**: `paper_only=true`
>
> **P76 Result:** Weighted scorecard tie-break between TIER_C_HOME_PLUS_AWAY_125 vs TIER_C_HOME_PLUS_AWAY_100.
> Score delta = 0.0003 < threshold 0.02 → dual finalists retained.
>
> **Scorecard summary (5 axes):**
> - Directional (30%): 125 wins (AUC=0.579 vs 0.560, hit_delta=0.034 vs 0.027)
> - Calibration (25%): 100 wins (cal_brier=0.2254, cal_ece=0.071 vs 0.2274/0.088)
> - Coverage (20%): 100 wins (n=373, cov=0.70 vs n=316, cov=0.59)
> - Stability/Risk (15%): TIE (both MODERATE, no caveats)
> - Future Readiness (10%): 125 wins (AUC + temperature method)
> - Final: 125=0.5543 vs 100=0.5540 — too close to select
>
> **2026 Accumulation Plan:**
> - Primary tracking: TIER_C_HOME_PLUS_AWAY_125
> - Shadow tracking: TIER_C_HOME_PLUS_AWAY_100
> - Monthly cadence: Jun-Nov 2026
> - Stop criteria: rolling 100-game hit_rate < 0.55
> - Tier B trigger: n >= 200 (~2026-09) → P78
> - Market-edge: DEFERRED until odds API key acquired
>
> **Research Roadmap:** P77 (2026-06) → P78 (Tier B) → P79 (Combined) → P80 (Odds-Lane) → P81 (Finalize)
>
> **Tests:** 36 PASS (P76) + 150 PASS (P72A→P75B regression) = 186 total
> **Forbidden scan:** 0 violations
> **Classification:** `P76_DUAL_FINALISTS_RETAINED_UNTIL_2026_DATA`

---

## Prior Active Task: P75B Calibration Diagnostics for Corrected Tier C Candidates

> **[COMPLETED 2026-05-26]** `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`
> **Issued by**: P75A handoff (P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION)
> **HEAD**: `7773624` (P75A) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P75A `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`
>
> **P75B Result:** Calibration diagnostics applied to all 5 P75A candidate rules.
> Calibration module: `wbc_backend/calibration/probability_calibrator.py` (AVAILABLE).
> Methods tested per rule: no_calibration / Platt / Temperature / Isotonic (70/30 chrono split or K-fold).
>
> **Uncalibrated metrics (full sample):**
> - BASELINE: hit=0.606, AUC=0.583, brier=0.2385, ECE=~0.036
> - HOME_ONLY: hit=0.672, AUC=0.559, brier=0.2292, ECE=~0.040
> - HOME_PLUS_AWAY_100: hit=0.633, AUC=0.560, brier=0.2344, ECE=~0.040
> - HOME_PLUS_AWAY_125: hit=0.639, AUC=0.579, brier=0.2340, ECE=~0.035
> - BAND_FILTERED: hit=0.637, AUC=0.630, brier=0.2312, ECE=~0.037
>
> **Calibration gate results (test-split Platt/Temp calibration):**
> - HOME_ONLY: OPERATIONAL_WITH_CAVEATS (cal_brier=0.220, cal_ece=0.059 — severe home-only dep)
> - HOME_PLUS_AWAY_100: OPERATIONAL_CALIBRATED (cal_brier=0.225, cal_ece=0.071 ✅)
> - HOME_PLUS_AWAY_125: OPERATIONAL_CALIBRATED (cal_brier=0.227, cal_ece=0.088 ✅)
> - BAND_FILTERED: RESEARCH_ONLY (n=168 < 200)
>
> **Preferred rule:** `TIER_C_HOME_PLUS_AWAY_125`
> Best AUC balance (0.579), OPERATIONAL_CALIBRATED, no concentration risk.
> HOME_PLUS_AWAY_100 is close rival (within 0.015 hit) → multi-candidate declared.
>
> **Tests:** 29 PASS (P75B) + 150 PASS (P72A+P72B+P73+P74+P75A+P75B regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P75B_MULTI_CANDIDATE_KEEP_FOR_NEXT_PHASE`

---

## Prior Active Task: P75A Tier C Corrected Rule Validator

> **[COMPLETED 2026-05-26]** `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`
> **Issued by**: P74 handoff (P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED)
> **HEAD**: `fb2af84` (P74) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P74 `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`
>
> **P75A Result:** Formal validation of P74 top corrected Tier C rules.
> All 5 P74 candidate rules reconstructed and matched within tolerance (all_valid=True).
>
> **Operational Gate Results:**
> - TIER_C_HOME_ONLY: OPERATIONAL_WITH_CAVEATS (n=268, hit=0.672, CI_low=0.616 ✅ — but severe home-only dependency)
> - TIER_C_HOME_PLUS_AWAY_100: OPERATIONAL_CANDIDATE (n=373, hit=0.633, CI_low=0.585 ✅)
> - TIER_C_HOME_PLUS_AWAY_125: OPERATIONAL_CANDIDATE (n=316, hit=0.639, CI_low=0.585 ✅)
> - TIER_C_BAND_FILTERED: RESEARCH_ONLY (n=168 < 200, good AUC=0.630)
>
> **Head-to-Head vs Baseline (hit=0.606, AUC=0.583, STABLE):**
> - HOME_ONLY: +0.066 hit, −0.024 AUC (home-only subset explanation provided)
> - HOME_PLUS_AWAY_125: +0.034 hit, −0.005 AUC (best AUC balance)
> - HOME_PLUS_AWAY_100: +0.027 hit, −0.023 AUC
> - BAND_FILTERED: +0.031 hit, +0.047 AUC (best AUC overall but n<200)
>
> **Preferred rule:** `TIER_C_HOME_ONLY` (highest hit_rate=0.672)
> **Multi-candidate note:** HOME_PLUS_AWAY_100 and HOME_PLUS_AWAY_125 also pass operational gate.
> Calibration diagnostics (P75B) needed to break tie.
> **Correction robustness:** True — improvement is statistically robust.
>
> **Tests:** 29 PASS (P75A) + 121 PASS (P72A+P72B+P73+P74+P75A regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P75A_MULTI_CANDIDATE_REQUIRES_CALIBRATION`

---

## Prior Active Task: P74 Tier C Home/Away Bias Correction Research

> **[COMPLETED 2026-05-26]** `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`
> **Issued by**: P73A/B handoff (home/away gap = 0.132 identified as primary research direction)
> **HEAD**: `5fda71b` (P73A/B) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P73 `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`
>
> **P74 Result:** Home/away bias confirmed and corrected rules evaluated.
> Tier C (n=535) reconstructed with hit_rate=0.606, AUC=0.583 — exact P73A match.
> Home hit_rate=0.672 (n=268, MODERATE stability), away hit_rate=0.539 (n=267, MODERATE stability).
> Hit gap = 0.132. Away weakness is GENERAL (not month/band-specific).
>
> **Away rescue filters (8 tested):**
> Best n>=75 filter: AWAY_HIGH_CONF_DELTA_075 — no single filter clearly beats baseline by >2pp with n>=75.
> away_rescue_found=False — no rescue filter met the improvement threshold.
>
> **Home robustness:** KEEP_FULL_HOME_TIER_C — narrowing threshold does not improve meaningfully.
> Home stable at full threshold (0.50) = MODERATE.
>
> **Candidate corrected rules (best performers):**
> - TIER_C_HOME_ONLY: n=268, hit=0.672, AUC=0.559, MODERATE → STRONG_CANDIDATE
> - TIER_C_HOME_PLUS_AWAY_125: n=316, hit=0.639, AUC=0.579, MODERATE → STRONG_CANDIDATE
> - TIER_C_HOME_PLUS_AWAY_100: n=373, hit=0.633, AUC=0.560, MODERATE → STRONG_CANDIDATE
> - TIER_C_ALL_BASELINE: n=535, hit=0.606, AUC=0.583, STABLE → CANDIDATE
>
> **Classification: `P74_TIER_C_HOME_AWAY_CORRECTION_CONFIRMED`**
> Multiple corrected rules (HOME_ONLY, HOME_PLUS_AWAY_100, HOME_PLUS_AWAY_125) beat baseline hit rate
> with n>=200 and MODERATE+ stability. Home correction is confirmed as the primary improvement lever.
>
> **Tests:** 24 PASS (P74) + 92 PASS (P72A+P72B+P73+P74 regression)
> **Forbidden scan:** 0 violations
> **Governance:** paper_only=True, diagnostic_only=True, live_api_calls=0, production_ready=False

---

## Prior Active Task: P73A/B Tier Stability Deep-Dive + Sample Expansion

> **[COMPLETED 2026-05-26]** `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`
> **Issued by**: P72B handoff (P73A + P73B recommended as PRIMARY next steps)
> **HEAD**: `9c04e50` (P72B) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P72B `P72B_OBJECTIVE_CONTRACT_READY`
>
> **P73A Result:** Tier C (n=535) full stability deep-dive.
> Monthly stability: STABLE (range=0.099, 6/6 months). Hit rate=0.606, AUC=0.583.
> Home/away split: home hit=0.672 vs away hit=0.539. Home picks ~50% of Tier C.
> Delta bands: band_050_075 highest (hit=0.637), band_125_150 weakest (hit=0.554).
> Concentration risk: single_band_dominance=True (spread >0.15), home_home_advantage_warning=False.
> Rolling windows: 10 windows of 50 games, step=25 — stable trend.
> Tier C classification: `TIER_C_OPERATIONAL_STABLE`
>
> **P73B Result:** 5 Tier B threshold variants analyzed.
> TB_ORIGINAL: n=98, AUC=0.646, monthly UNSTABLE. Best AUC variant: TB_EXCL_WEAK_BAND (AUC=0.651).
> All 5 variants show UNSTABLE monthly stability (small per-month n=14–23).
> original_tier_b_signal: `SAMPLE_EXPANSION_CONFIRMED` (n>=75, AUC>=0.62, AUC_CI_low>0.50).
> tier_b_can_be_operational: False (n=98 < 200 AND monthly UNSTABLE).
>
> **Decision Matrix:**
> - S01 Tier C Directional → TIER_C_OPERATIONAL_STABLE (PRIMARY_OPERATIONAL_CANDIDATE)
> - S02 Tier B Directional → RESEARCH_ONLY_SAMPLE_EXPANSION_CONFIRMED
> - S03 Tier A Directional → WATCHLIST_ONLY (n=24)
> - S04 Tier C Platt Calibrated → CALIBRATION_REFERENCE (AUC=0.593, better probability quality)
>
> **Tests:** 23 PASS (P73) + 68 PASS (P72A+P72B+P73 regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P73_TIER_C_OPERATIONAL_STABLE_TIER_B_RESEARCH_CONFIRMED`

---

## Prior Active Task: P72B Prediction-vs-Market Objective Contract

> **[COMPLETED 2026-05-26]** `P72B_OBJECTIVE_CONTRACT_READY`
> **Issued by**: CTO governance direction after P72A
> **HEAD**: `5c2a26b` (P72A) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P72A `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED` (commit `5c2a26b`)
>
> **P72B Result:** 5-lane objective contract defined. P72A strategies classified.
> Tier C = PRIMARY_OPERATIONAL_CANDIDATE. Tier B = BEST_AUC_RESEARCH. Tier A = SAMPLE_LIMITED.
> Production BLOCKED (7/8 gates pending). Recommended next: P73A + P73B.
> **Tests:** 23 PASS (P72B) + regression PASS
> **Forbidden scan:** 0 violations
> **Classification:** `P72B_OBJECTIVE_CONTRACT_READY`

---

## Prior Active Task: P72A Odds-Free Strategy Accuracy Backtest

> **[COMPLETED 2026-05-26]** `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`
> **Issued by**: CTO direction — API key NOT required for accuracy backtest
> **HEAD**: `1d8adb8` (P71) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P71 `P71_PATH_A_STILL_AWAITING_API_KEY` (commit `1d8adb8`)
>
> **P72A Result:** 7 strategies evaluated. Best: S02_TIER_B_DIRECTIONAL (AUC=0.646, n=98).
> Tier C directional: hit_rate=0.606, AUC=0.583. All without odds. No EV/CLV/Kelly.
> **Tests:** P72A PASS + regression PASS
> **Forbidden scan:** 0 violations
> **Classification:** `P72A_ODDS_FREE_PREDICTIVE_SIGNAL_CONFIRMED`

---

## Prior Active Task: P72 (Pending)

> **Next recommended scope**: P72 — Live Pull Re-execution on Key Configuration
> **Status**: Awaiting `THE_ODDS_API_KEY` in `.env` (same blocker as P71)
> **Mode**: `paper_only=true`, `diagnostic_only=true`
>
> P71 confirmed API_KEY_MISSING and executed awaiting-key closure.
> Classification: `P71_PATH_A_STILL_AWAITING_API_KEY`.
> P70 pull script ready to auto-switch to LIVE mode on key detection.
>
> **To unblock P72 / execute actual 2024 MLB data pull:**
> 1. Register at https://the-odds-api.com and purchase historical data access
> 2. Add to `.env`: `THE_ODDS_API_KEY=<your_key>`
> 3. Run P70: `.venv/bin/python scripts/_p70_path_a_the_odds_api_historical_pull.py`
> 4. Script auto-switches to LIVE mode → writes `data/mlb_2025/mlb_odds_2024_real.csv`
> 5. Re-run P71: `.venv/bin/python scripts/_p71_the_odds_api_live_pull_execution.py`
> 6. P71 auto-advances to `P71_PATH_A_PULL_COMPLETE` once CSV validates
>
> **Alternatively**: If deferring API key purchase permanently, P72 documents the
> 2024 real-odds gap as a permanent research limitation and closes the PATH_A track.

---

## Prior Completed Task: P71

> **[COMPLETED 2026-05-26]** `P71_PATH_A_STILL_AWAITING_API_KEY`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P70 `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`
>
> **P71 Result:** Awaiting-key closure (Step 3A).
> API key status confirmed: API_KEY_MISSING (no `THE_ODDS_API_KEY` in `.env`).
> P70 context loaded and verified: `P70_PATH_A_AUTHORIZED_AWAITING_API_KEY`.
> live_api_calls=0, paid_api_called=False.
> CEO authorization confirmed (inherited from P70).
> Setup instructions documented: 7-step process to configure key and execute pull.
> CSV validator implemented: schema validation, row count ≥500, moneyline numeric.
> Forbidden scan: 0 violations. No API calls. Governance fully preserved.
> **Tests:** 48 PASS (P71) + 437 PASS (P43+P59–P71 cumulative regression)
> **Classification:** `P71_PATH_A_STILL_AWAITING_API_KEY`

---

## Prior Completed Task: P69

> **[COMPLETED 2026-05-26]** `P69_CEO_DECISION_MEMO_READY`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P68 `P68_ODDSPORTAL_BLOCKED_BY_TOS`
>
> **P69 Result:** CEO decision memo drafted for P61 PATH_A authorization.
> Evidence trail P61→P67→P68 verified: all 3 prior-phase classifications confirmed.
> Free-source PATH_B exhausted: 6 sources evaluated, 0 usable 2024 ML odds found.
> OddsPortal block confirmed: ToS Section 2.11 scraping prohibition + robots.txt `*-2024*`.
> PATH_A spec: The Odds API, ~$30–50 one-time, HIGH data quality, 9 required fields documented.
> CEO decision options: APPROVE / REJECT / DEFER — exact copy-paste phrases provided.
> Allowed use: paper-only, diagnostic-only, research validation only.
> Prohibited use: live betting, Kelly, production, champion replacement, redistribution.
> 2024 gap: UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A.
> Forbidden scan: 0 violations. No API calls. Governance fully preserved.
> **Tests:** 42 PASS (P69) + 338 PASS (P43+P59–P69 cumulative regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P69_CEO_DECISION_MEMO_READY`

---

## Prior Completed Task: P68

> **[COMPLETED 2026-05-26]** `P68_ODDSPORTAL_BLOCKED_BY_TOS`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P67 `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`
>
> **P68 Result:** OddsPortal ToS and scraping feasibility probe.
> ToS Section 2.11 explicitly prohibits scraping and automated requests.
> ToS Section 2.10 prohibits database extraction without express consent.
> robots.txt `Disallow: *-2024*` for `User-agent: *` covers `/baseball/usa/mlb-2024/results/`.
> Page probe (single manual load): data visible, 50 pages, decimal odds present, WS sample rows confirmed.
> Schema: 6/9 required fields technically observable. Closing label absent. Doubleheader disambiguation absent.
> 2024 gap: UNRESOLVED_PENDING_CEO_DECISION_ON_PATH_A.
> Forbidden scan: 0 violations. No bulk scraping. No anti-bot bypass. Governance fully preserved.
> **Tests:** 36 PASS (P68) + 296 PASS (P43+P59–P68 cumulative regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P68_ODDSPORTAL_BLOCKED_BY_TOS`

---

## Prior Completed Task: P67

> **[COMPLETED 2026-05-26]** `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P66 `P66_ODDS_MAPPING_INTEGRITY_CONFIRMED`
>
> **P67 Result:** Exhaustive free-source search (PATH_B execution) — 13 search queries across
> Kaggle, GitHub, OddsPortal, SportsbookReviewsOnline.com, aussportsbetting.com.
> SBRO archive frozen at 2021 (SOURCE_NO_2024). Kaggle: 27 MLB 2024 datasets, all game stats,
> no betting odds (SOURCE_NO_MONEYLINE). GitHub: 0 repos for 3 MLB odds queries; topic mlb-betting
> = 0 public repos (SOURCE_UNUSABLE). Kaggle synthetic dataset (Faker, SOURCE_UNUSABLE).
> OddsPortal: **2024 data confirmed in web UI** (WS Game 1 LAD 1.71/NYY 2.37);
> no bulk CSV, requires JS scraping, ToS Section 5 restricts automated extraction.
> OddsPortal classified SOURCE_PARTIAL_NEEDS_SCHEMA_PROBE.
> aussportsbetting.com: HTTP 403 blocked, SOURCE_LICENSE_UNCLEAR.
> 2024 data gap: UNRESOLVED_PENDING_P68_SCRAPE_FEASIBILITY.
> Forbidden scan: 0 violations (CLEAN). All governance invariants enforced.
> **Tests:** 33 PASS (P67) + 260 PASS (P43+P59–P67 cumulative regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P67_PATH_B_PARTIAL_SOURCE_FOUND_NEEDS_REVIEW`

---

## Prior Completed Task: P66

> **[COMPLETED 2026-05-26]** `P66_ODDS_MAPPING_INTEGRITY_CONFIRMED`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P65 `P65_EDGE_STABLE_NEGATIVE`
>
> **P66 Result:** 5-step odds mapping integrity audit of 535 P64 paper simulation rows.
> Join: 0 unmatched, 28 doubleheader duplicate keys (last-row-wins dedup, documented not an error).
> Side mapping: 535/535 PASS — no inversions.
> Odds conversion: 535/535 PASS — American ML → decimal exact to 6 dp.
> Edge recalculation: 535/535 PASS — max delta = 0.000000, mean edge −0.032473 (original = recomputed).
> Positive edge rows: 200/535 (original) = 200/535 (recomputed).
> Forbidden scan: 0 violations (CLEAN). All governance invariants enforced.
> 2024 data gap: UNRESOLVED. Negative edge confirmed genuine after full mapping validation.
> **Tests:** 36 PASS (P66) + 227 PASS (P43+P59+P60+P61+P62+P63+P64+P65+P66 regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P66_ODDS_MAPPING_INTEGRITY_CONFIRMED`

---

## Prior Completed Task: P65

> **[COMPLETED 2026-05-26]** `P65_EDGE_STABLE_NEGATIVE`
> **Branch**: `main` | **Mode**: `paper_only=true`, `diagnostic_only=true`
> **Prior phase**: P64 `P64_PAPER_SIMULATION_FIRST_RUN_READY`
>
> **P65 Result:** Walk-forward validation of 535 P64 paper simulation rows.
> 6 monthly windows (2025-04 → 2025-09) + 3 chronological thirds + 10 rolling windows + half split.
> All thirds show mean_edge < -0.01. Classification: `P65_EDGE_STABLE_NEGATIVE`.
> Edge is consistently negative across all temporal windows — no unstable regime detected.
> Third means: third_1=-0.0301, third_2=-0.0242, third_3=-0.0431.
> Rolling window range: edge_mean from -0.0104 (best) to -0.0685 (worst).
> Forbidden scan: 0 violations (CLEAN). All governance invariants enforced.
> 2024 data gap: UNRESOLVED.
> **Tests:** 36 PASS (P65) + 191 PASS (P43+P59+P60+P61+P62+P63+P64+P65 regression)
> **Classification:** `P65_EDGE_STABLE_NEGATIVE`

---

## Prior Completed Task: P64

> **[COMPLETED 2026-05-26]** `P64_PAPER_SIMULATION_FIRST_RUN_READY`
> **Commit**: `c4a3375`
> First paper-only simulation run. 535 Tier C rows. Edge mean = -0.032473. 200/535 positive edge.
> P45 Platt constants locked: A=0.435432, B=0.245464.

---

## P63 Prior Completion Record

> **[COMPLETED 2026-05-26]** `P63_READY_FOR_CEO_REVIEW`
> **Issued by**: CTO Agent (CEO review readiness gate for P62)
> **HEAD**: `25fb2e3` | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P62 `P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW`
>
> **P63 Result:** CEO-review readiness audit of P62 contract. All 17 gates audited (13 CEO-blocking
> gates pass, 3 NOT_TESTABLE_YET pending row emission). All 33 schema fields present and classified.
> All 9 status values safe. All 12 governance flags preserved. Forbidden scan: 0 violations.
> P45 Platt constants locked. P52 thresholds unchanged. 2024 data gap = UNRESOLVED_AS_OF_P62.
> **Tests:** 31 PASS (P63) + 119 PASS (P43+P59+P60+P61+P62+P63 regression)
> **Forbidden scan:** 0 violations
> **Classification:** `P63_READY_FOR_CEO_REVIEW`

---

## P62 Prior Completion Record

> **[COMPLETED 2026-05-26]** `P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW`
> **Issued by**: CEO P2 directive (after P61 completion)
> **HEAD**: `d8b3ef5` (P61) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P61 `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT` (commit `d8b3ef5`)
>
> **P62 Result:** Contract schema fully defined — 17-condition eligibility gate, 33-field row schema,
> 9 allowed status values, 10 governance exclusions, P61 data gap documented.
> No live rows emitted. No production deployment proposed. Paper-only diagnostic contract.
> **Tests:** 20 PASS (P62) + regression PASS
> **Forbidden scan:** 0 violations
> **Classification:** `P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW`

---

## P61 Prior Completion Record

> **[COMPLETED 2026-05-26]** `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT`
> **Issued by**: CEO P1 directive (elevated after P60 completion)
> **HEAD**: `36a40f4` (P60) | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P60 `P60_EDGE_STABLE_ACROSS_MONTHS` (commit `36a40f4`)
>
> **P61 Result:** 6 sources evaluated, 2 viable resolution paths (PATH_A: The Odds API ~$30-50;  
> PATH_B: Kaggle/GitHub free search). Recommended: PATH_B first, PATH_A if PATH_B fails.  
> **Tests:** 15 PASS (P61) + 68 PASS (P43+P59+P60+P61 regression)  
> **Forbidden scan:** 0 violations  
> **Classification:** `P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT`

---

## P60 Prior Completion Record

> **[COMPLETED 2026-05-26]** `P60_EDGE_STABLE_ACROSS_MONTHS`
> **Issued by**: CEO Second-Level Review 2026-05-26
> **CEO classification**: `CEO_DECISION_PARTIALLY_APPROVED`
> **HEAD**: `b1332b3` | **Branch**: `main` | **Mode**: `paper_only=true`
> **Prior phase**: P59 `P59_FIRST_MONTHLY_REPORT_SAMPLE_LIMITED` (commit `b1332b3`)
> **CTO P0 status**: **COMPLETED — EDGE_STABLE_ACROSS_MONTHS (6/6 months)**
>
> **P60 Result:** 6/6 月份 EDGE_WITHIN_THRESHOLD，avg edge=0.1046，CI_low > 0 所有月份。  
> **Tests:** 22 PASS (P60) + 53 PASS (P43+P59+P60 regression)  
> **Forbidden scan:** 0 violations  
> **Classification:** `P60_EDGE_STABLE_ACROSS_MONTHS`

---

## CEO Override Notes

1. CTO P0 (P60 Historical Monthly Report Pack) **採納** — 但 CEO **reframe 為 EDGE-FIRST**：主指標必須是 edge_status 跨月一致性。
2. CTO P1 (Validator SSOT) **降為 P3** — 未來再做。
3. CEO 升級：2024 closing-line data gap → P1，將於 P60 完成後處理。
4. CEO 升級：Paper Recommendation Contract Draft → P2，將於 P60 完成後處理。
5. CEO 新規則：未來 P61+ 若是新 monitoring meta-layer，需先過 CEO gate。

---

## Task Prompt（直接交給 Planner / Worker）

```md
[P60 — Historical Monthly Report Pack (EDGE-FIRST Validation)]

# Branch Governance (MANDATORY)
## Canonical Repo
/Users/kelvin/Kelvin-WorkSpace/Betting-pool
## Canonical Branch
main
## Current HEAD
b1332b3
## Rules
- Do NOT create a new branch
- Do NOT create a new worktree
- Do NOT checkout another branch
- Do NOT clone another repo
- Do NOT use detached HEAD
- Do NOT modify TSL crawler
- Do NOT make live API calls
- Do NOT change champion strategy `fixed_edge_5pct`
- Do NOT remove promotion_freeze
- Do NOT modify P45 Platt constants (A=0.435432, B=0.245464)
- Do NOT modify P52 global thresholds
- Do NOT modify runtime recommendation logic
- Do NOT overwrite P52/P53/P54/P55/P56/P57/P58/P59 artifacts
- Keep paper_only=true, diagnostic_only=true
- Keep promotion_freeze=true, kelly_deploy_allowed=false
- Keep live_api_calls=0
- 嚴禁 stage runtime / DB / PID / log / raw feed / daemon output
- 嚴禁宣稱 profitability / guaranteed profit / production ready
- 嚴禁開新 monitoring meta-layer 超出 P60 範圍

# Required Pre-flight
git rev-parse --show-toplevel          # 預期: /Users/kelvin/Kelvin-WorkSpace/Betting-pool
git branch --show-current               # 預期: main
git rev-parse HEAD                      # 預期: b1332b3
git status --short                      # 記錄 dirty files 但不依此 stage

# STOP Conditions
- Repo / branch / HEAD 不符 → STOP
- 偵測到 live odds API call / TSL crawler 修改 / champion replacement → STOP
- 偵測到 P52 thresholds 或 P45 Platt constants 修改 → STOP
- 偵測到 runtime recommendation logic 修改 → STOP

---

## 1. Task Name
P60 — Historical Monthly Report Pack (EDGE-FIRST Validation, Paper-Only Diagnostic)

## 2. Background

P59 completed at commit `b1332b3`:
- First real monthly report for 2025-09
- Sep batch_n=98 → SAMPLE_INSUFFICIENT
- Sep platt_ece=0.122929 → CALIBRATION_ALERT
- Sep edge_status=EDGE_WITHIN_THRESHOLD（raw_edge_mean=0.108, CI=[0.092, 0.125]）
- global_status=MONITORING_ALERT_DIAGNOSTIC (RED)
- VAL01-VAL10 all PASS
- P40-P59 cumulative 460/460 PASS

CRITICAL PARTIAL-CONFIRMATION MILESTONE (應於 P60 report 顯著引用):
- P43 在 2025-only strong-edge subset (Tier C, n=535, |sp_fip_delta|>=0.50) 已 `EDGE_CONFIRMED`:
  - mean_edge=0.1059, CI=[0.0989, 0.1132], positive_rate=89.5%
- But P43 final_classification=`P43_BLOCKED_BY_DATA_GAP` 因 2024 closing-line 缺失

P60 的核心問題（CEO directive）:
- **Apr–Sep 2025 模型是否「穩定」優於 closing line？**
- 主指標：edge_status 跨月一致性 (PRIMARY)
- 副指標：calibration_status / sample_status (SECONDARY)

## 3. Goal

產出 Apr–Sep 2025 所有可用月份的 monthly monitoring report pack，
驗證 P58/P59 template 跨月可用性，**並以 EDGE-FIRST framing 給出 edge_status 跨月穩定性結論**。

## 4. Allowed Modification Scope (whitelist)

- `scripts/_p60_historical_monthly_report_pack_validation.py` (NEW)
- `tests/test_p60_historical_monthly_report_pack_validation.py` (NEW)
- `data/mlb_2025/derived/p60_historical_monthly_report_pack_validation_summary.json` (NEW)
- `report/p60_historical_monthly_report_pack_validation_20260526.md` (NEW)
- `00-BettingPlan/20260526/p60_historical_monthly_report_pack_validation_20260526.md` (NEW)
- `00-Plan/roadmap/active_task.md` (本檔，完成後狀態更新)

## 5. Forbidden Modification Scope (hard blocks)

- 禁止修改 P52/P53/P54/P55/P56/P57/P58/P59 artifacts
- 禁止修改 `data/mlb_2025/derived/p52_monitoring_contract_v2_summary.json`
- 禁止修改 `data/mlb_2025/derived/p45_platt_recalibration_summary.json`
- 禁止修改 `data/mlb_2025/derived/p58_monitoring_contract_v2_monthly_report_template_summary.json`
- 禁止修改 `data/mlb_2025/derived/p59_monitoring_contract_v2_first_monthly_report_summary.json`
- 禁止修改 `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`
- 禁止修改 `data/mlb_2025/mlb_odds_2025_real.csv`
- 禁止修改 `wbc_backend/clv/outcome_matching.py` (P26 contract frozen)
- 禁止修改 `wbc_backend/pipeline/prediction_orchestrator.py`
- 禁止修改 TSL crawler / live API
- 禁止替換 champion `fixed_edge_5pct`
- 禁止修改 P45 Platt constants 或 P52 thresholds
- 禁止修改 runtime recommendation logic
- 禁止呼叫 live odds API
- 禁止 promotion / champion replacement / optimizer promotion
- 禁止輸出 "guaranteed profit" / "profitability claim" / "production proposal" / "live odds api call"

## 6. Required Work

### Step 1 — Source artifact loading (no fetch)
1. Load P52 thresholds: `data/mlb_2025/derived/p52_monitoring_contract_v2_summary.json`
2. Load P58 template schema: `data/mlb_2025/derived/p58_monitoring_contract_v2_monthly_report_template_summary.json`
3. Load P59 reference: `data/mlb_2025/derived/p59_monitoring_contract_v2_first_monthly_report_summary.json`
4. Load P45 Platt constants reference (do not modify)
5. Load predictions: `data/mlb_2025/derived/mlb_2025_per_game_predictions_phase56_sp_bullpen_context_v1.jsonl`

### Step 2 — Identify available months (Apr–Sep 2025)
- 對每月：Apr, May, Jun, Jul, Aug, Sep
- 取得 Tier C (|sp_fip_delta| >= 0.50) 該月所有 records
- 若某月 batch_n < 10 → 標記 `DATA_GAP_BLOCKED`，仍進入 pack 但 explicitly flagged

### Step 3 — Per-month monthly report (reuse P58/P59 schema)
For each available month, compute:

**PRIMARY (EDGE axis — CEO directive)**:
- `raw_edge_mean`
- `raw_edge_ci_low`, `raw_edge_ci_high` (bootstrap n_boot=5000)
- `edge_status` (EDGE_WITHIN_THRESHOLD / EDGE_WARNING / EDGE_CRITICAL based on P52 V2)
- `positive_rate`

**SECONDARY**:
- `platt_ece`, `platt_brier`
- `calibration_status`
- `sample_status` (SAMPLE_INSUFFICIENT if n<100)
- `data_gap_status`

**GLOBAL**:
- `global_status` (per P52 V2 dominance rule, NOT modified)
- `global_alert_level` (GREEN/YELLOW/RED)
- `global_alert_reasons`

**BAND ANNOTATIONS**:
- Carry-forward Sep mid-band annotation if month=Sep
- For other months, generate fresh BandAnnotationRecord per P57 schema

### Step 4 — VAL01–VAL10 validation per month
- Run VAL01–VAL10 for each generated monthly report
- Record per-month pass/fail
- Pack-level: `months_all_val_pass` boolean

### Step 5 — Pack-level synthesis (EDGE-FIRST)
**MUST INCLUDE**:
- `total_months` (expected 6: Apr–Sep)
- `months_with_edge_within_threshold` (count)
- `months_with_edge_alert` (count)
- `cross_month_edge_stability` classification:
  - `EDGE_STABLE_ACROSS_MONTHS`: all months EDGE_WITHIN_THRESHOLD AND CI_low > 0
  - `EDGE_MOSTLY_STABLE`: >=4/6 months OK
  - `EDGE_INCONSISTENT`: 2-3/6 months OK
  - `EDGE_UNSTABLE`: <=1/6 months OK
- `months_sample_limited`
- `months_calibration_alert`
- `months_data_gap_blocked`
- `synthesis_conclusion` (text, must answer:「Apr–Sep 2025 模型是否穩定優於 closing line？」)

### Step 6 — Tests (P26/P39/P59 style)
Required tests (≥15):
1. P52/P58/P59 source artifacts load
2. Apr–Sep months processing complete (or blocked-flagged)
3. Per-month edge_status correctly classified per P52 V2 thresholds
4. Per-month bootstrap CI deterministic (seed=42)
5. Per-month VAL01–VAL10 all PASS (where data available)
6. Sep 2025 report values match P59 reference exactly
7. P52 thresholds_used_flag matches P52 (unchanged check)
8. P45 Platt constants unchanged check
9. paper_only=true, diagnostic_only=true, kelly_deploy_allowed=false in JSON
10. live_api_calls=0
11. runtime_recommendation_logic_changed=false
12. P52-P59 overwrite flags all False
13. Pack-level cross_month_edge_stability classification logic
14. Synthesis conclusion includes EDGE-FIRST framing
15. Forbidden affirmative scan: no "guaranteed profit" / "profitability claim" / "production proposal" / "live odds api call" / "champion replacement"

### Step 7 — Report (must include)
- Pre-flight result
- Source artifacts loaded with hashes
- Available months table
- Per-month metrics table (EDGE-FIRST: edge_mean, CI, status FIRST)
- Per-month calibration/sample table (SECONDARY)
- VAL01-VAL10 per month
- Pack-level synthesis
- **EDGE-FIRST CONCLUSION**: "Apr–Sep 2025 模型是否穩定優於 closing line？"
- Sep 2025 cross-reference to P59
- Framing note: "2024 closing-line data gap remains; this pack is 2025-only"
- Files created
- Tests results
- Forbidden scan result
- Commit hash or reason not committed

## 7. Constraints

- `paper_only=true`
- `diagnostic_only=true`
- `promotion_freeze=true`
- `kelly_deploy_allowed=false`
- `T_LOCKED=0.50` (must NOT re-optimize)
- No live API call
- No TSL crawler modification
- No champion replacement
- No production proposal
- No branch / worktree / clone
- 不依賴 P42 brier=None 的 JSON 欄位
- 不修改 P45 Platt constants
- 不修改 P52 thresholds
- 不修改 runtime recommendation logic
- 不開新 monitoring meta-layer 超出 P60 範圍

## 8. Validation / Test Commands

- `./.venv/bin/pytest tests/test_p60_historical_monthly_report_pack_validation.py -v`
- `./.venv/bin/pytest tests/test_p43*.py tests/test_p59_*.py tests/test_p60_*.py -q`
- Expected: P60 ≥15 tests PASS, P40–P60 cumulative PASS
- Forbidden affirmative scan: 0 hits

## 9. Output Report Locations

- `data/mlb_2025/derived/p60_historical_monthly_report_pack_validation_summary.json`
- `report/p60_historical_monthly_report_pack_validation_20260526.md`
- `00-BettingPlan/20260526/p60_historical_monthly_report_pack_validation_20260526.md`

## 10. Allowed Final Classifications

選擇符合實際結果者:
- `P60_EDGE_STABLE_ACROSS_MONTHS` — Apr–Sep 所有月份 edge_status=EDGE_WITHIN_THRESHOLD AND CI_low>0
- `P60_EDGE_MOSTLY_STABLE` — 4-5/6 月 OK
- `P60_EDGE_INCONSISTENT` — 2-3/6 月 OK
- `P60_EDGE_UNSTABLE` — ≤1/6 月 OK
- `P60_HISTORICAL_MONTHLY_PACK_BLOCKED` — 資料缺失嚴重無法產出
- `P60_HISTORICAL_MONTHLY_PACK_INCOMPLETE` — 部分月份無法產出但其他月份完成

## 11. Handoff Report Required Sections

- Pre-flight result
- Dirty file assessment
- Files created / modified
- Source artifacts loaded
- Months included / excluded
- Monthly status table (EDGE-FIRST)
- VAL01–VAL10 summary
- Cross-month edge stability synthesis
- Sep 2025 vs P59 consistency check
- Final P60 classification
- Tests PASS / FAIL
- Forbidden scan result
- Commit hash or reason not committed
- Whether P52–P59 artifacts preserved
- Whether P52 thresholds and P45 Platt constants unchanged
- 10 行內 CTO summary
- Next 24h prompt
```

---

# Strict Reminder

- 本任務由 **CEO 指派**，採納 CTO P0 方向但**reframe 為 EDGE-FIRST**
- CTO P1 (Validator SSOT) 已降為 P3，本任務**不做** Validator 抽取
- 2024 closing-line data gap 升為 P1，但**今日不動**（明日處理）
- Paper Recommendation Contract Draft 升為 P2，但**今日不動**（明日後處理）
- 嚴格 diagnostic-only，不得轉為 production / promotion / champion replacement
- 任何 STOP condition 觸發 → 停止並回報，不嘗試 workaround
- 未來 P61+ 若是新 monitoring meta-layer，需先過 CEO gate
