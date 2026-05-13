> ⚠️ RESCUED FROM STALE WORKTREE on 2026-05-13.
> Original location: Betting-pool/main (untracked).
> Superseded by betting_roadmap_20260513_v5_ceo.md.

# Betting-pool Roadmap v4 — MLB Prediction + Strategy Optimization

**Date:** 2026-05-13  
**Owner:** CTO agent  
**Supersedes:** `00-BettingPlan/roadmap/betting_roadmap_20260504.md` and the 2026-05-12 / 2026-05-13 interim realignments where they conflict.  
**Implementation worktree used as current truth:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` on branch `p13-clean`  
**Latest committed implementation evidence inspected:** `333cf80 docs(betting): add P37.5 manual odds approval package`  
**Mode:** `PAPER_ONLY=true`, `production_ready=false`

---

## 1. CTO Decision

The system should now be managed around two product goals, not around the raw phase number sequence:

1. **MLB prediction to Taiwan Sports Lottery recommendation**  
   Generate auditable MLB betting recommendations aligned to Taiwan Sports Lottery market types. Current implementation proves moneyline paper recommendations can be produced historically; the next gap is multi-season reliability and future market expansion.

2. **Strategy simulation and optimization**  
   Optimize policies by simulation evidence before recommendations are trusted: edge threshold, Kelly fraction, stake cap, odds cap, drawdown, Sharpe, hit rate, bootstrap CI, exposure, turnover, and settlement quality.

**CTO call:** the next highest-value optimization is no longer more roadmap/governance documentation. It is a paired unblock:

- **Code-owned P0:** build the 2024 Retrosheet-to-prediction feature adapter and OOF rebuild path.
- **Data/approval-owned P1:** complete licensed 2024 moneyline odds approval and manual import.

These two unlock the 2024 joined input, which is the only credible route out of the 324-active-entry sample wall.

---

## 2. Current Implementation Status

### 2.1 Product Axis A — MLB prediction to TSL recommendation

| Capability | Current status | Evidence / note |
|---|---:|---|
| 2025 historical moneyline model probability | Ready in PAPER | P13 walk-forward logistic path exists in p13 worktree. |
| Historical odds-aware moneyline simulation | Ready in PAPER | P15 joined OOF + historical odds: 1,575 / 1,577 joined, 99.87% coverage. |
| Risk-aware paper recommendation rows | Ready in PAPER | P16.6 produced 324 eligible rows using P18 risk-repaired policy. |
| Identity join and settlement | Ready after repair | P19 enriched ledger with 100% `game_id`; P17 replay settled 171 wins / 153 losses. |
| Daily PAPER orchestrator | Ready | P20 gate ready: 324 active, 0 unsettled, +10.78% paper ROI, hit rate 52.78%. |
| Multi-day PAPER backfill orchestrator | Ready but data sparse | P21 ready for existing dates; missing dates are explicit, not fabricated. |
| 2024 game identity/outcome spine | Partially ready | P32 processed 2,429 game rows from Retrosheet game log. Raw `gl2024.txt` remains governed and should not be casually committed. |
| 2024 prediction probability source | Blocked | P33 found 0 ready 2024 prediction files; P35 confirms 2024 Retrosheet adapter missing. |
| 2024 closing odds source | Blocked | P36/P37/P37.5 approval gate ready, but no filled approval record or licensed odds CSV. |
| TSL live/snapshot source | Deferred | No production/live TSL bridge; keep PAPER_ONLY. |
| TSL market coverage beyond moneyline | Not implemented | Need market taxonomy + labels for run line, totals, F5, odd/even, team totals. |

### 2.2 Product Axis B — strategy simulation optimization

| Capability | Current status | Evidence / note |
|---|---:|---|
| Basic odds-aware strategy simulation | Ready in PAPER | P15 activated capped Kelly once historical odds were joined. |
| Risk metrics and policy repair | Ready in PAPER | P18 evaluated 400 candidates; selected `edge=5%`, `stake_cap=0.25%`, `kelly=0.10`, `odds_max=2.50`. |
| Paper ledger and P/L | Ready for 2025 sample | P19/P17 replay closed settlement and generated paper P/L. |
| Stability certification | Blocked | P28 blocked: 324 active entries vs 1,500 advisory minimum. |
| Policy density expansion | Blocked | P29 best relaxed policy produced 563 active entries, still below 1,500. |
| Multi-season strategy optimization | Blocked | Needs 2024 joined prediction + odds input. |
| CLV / live market validation | Deferred | Requires live or approved closing snapshots; not ready. |

---

## 3. Roadmap Alignment Gaps

### 3.1 Gap vs `betting_roadmap_20260504.md`

The 20260504 roadmap was valuable as a long-term architecture document, but it is now behind reality:

- It over-emphasizes league abstraction and governance as near-term P0.
- It underweights the already-completed 2025 moneyline paper recommendation chain.
- It does not reflect P28/P29's hard sample wall.
- It does not reflect P31-P37.5's conclusion that 2024 odds licensing, not code plumbing, is the hard blocker.

### 3.2 Gap vs 2026-05-12 P16-first roadmap

The 2026-05-12 direction was correct at the time: convert P15 evidence into paper recommendation rows and force strategy risk metrics into the gate. That work has effectively advanced:

- P16.6 gate ready with 324 eligible paper recommendations.
- P18 risk policy repaired max drawdown from 44.80% to 1.85%.
- P19/P20 closed identity join and daily paper orchestration.

The problem has moved. Repeating P16/P18 work now gives less leverage than unlocking more data.

### 3.3 Gap vs 2026-05-13 P37.5 latest handoff

P37.5 correctly protects the project from unlicensed odds usage, but it can over-focus the roadmap on an administrative gate. The CTO roadmap must keep two parallel lanes alive:

- While odds approval waits for human/provider action, engineering should build the 2024 prediction adapter and OOF rebuild.
- When approval arrives, the system should be ready to immediately ingest licensed odds and build joined input.

---

## 4. Critical Blockers

| Blocker | Severity | Owner type | Blocks | Current evidence | Required resolution |
|---|---:|---|---|---|---|
| 2024 licensed closing odds missing | Critical | Human/data owner | EV, Kelly, joined input, multi-season simulation | P37.5 checker returns `P37_5_MANUAL_ODDS_PACKAGE_MISSING`. | Fill `data/mlb_2024/manual_import/odds_approval_record.json` and `odds_2024_approved.csv`; pass P37 gate. |
| 2024 prediction OOF source missing | Critical | Engineering | multi-season model quality, strategy replay | P33 `P33_BLOCKED_NO_VERIFIED_PREDICTION_SOURCE`; P35 adapter missing. | Build Retrosheet feature adapter + OOF model rebuild. |
| Sample wall | Critical | Engineering + data | production confidence, stability audit | P28: 324 active < 1,500; P29 best relaxed = 563. | Add 2024 season rows and rerun true-date replay/stability audit. |
| Moneyline-only product surface | High | Product/engineering | user goal: TSL market recommendations | Current end-to-end recommendation is moneyline only. | Add TSL market taxonomy + paper schemas for HDC, OU, F5, odd/even, team total. |
| Live TSL source unavailable | High but deferred | Data/source owner | production/live shadow | Existing docs cite TSL 403/unavailable. | Build approved snapshot/CSV bridge before any production proposal. |
| Workspace drift | Medium | Engineering hygiene | safe execution | Current main repo is dirty/untracked; p13 also has uncommitted data/output/runtime artifacts. | Keep implementation in p13; stage only whitelisted source/docs/tests; never commit raw odds/runtime/outputs. |

---

## 5. Reordered P0-P10 Roadmap

This is a priority list, not a historical phase-number list. Implementation phase labels are suggested and can be adjusted, but priority order should hold.

| Priority | Proposed phase | Track | Objective | Done condition |
|---:|---|---|---|---|
| **P0** | **P38A — 2024 Retrosheet Feature Adapter + OOF Rebuild** | Prediction | Convert P32 2024 game logs into pregame-safe features and generate 2024 OOF probabilities. | `p_oof` exists for 2024 rows, no y_true leakage, Brier/ECE/BSS reported, deterministic tests pass. |
| **P1** | **P37.6 / P38B — Licensed Odds Approval + Import Artifact** | Data / governance | Move from approval package to actual licensed 2024 moneyline odds artifact. | Filled approval record + approved odds CSV pass P37; P38 import artifact has `p_market`, `odds_decimal`, license refs, no forbidden columns. |
| **P2** | **P39 — 2024 Joined Input Certification** | Prediction + data | Join P0 prediction OOF + P1 odds + P32 outcomes into a canonical 2024 training/replay table. | Joined input has required fields, high `game_id` coverage, provenance hashes, no duplicate game ids, no look-ahead fields. |
| **P3** | **P40 — Multi-Season True-Date Replay** | Strategy | Run 2024+2025 replay with strict date separation and settlement. | Active entries target >= 1,500 or honest blocker; all settlements joined by identity, not position. |
| **P4** | **P41 — Strategy Optimization v2** | Strategy | Re-run policy grid on expanded sample: edge, Kelly, stake cap, odds cap, abstention, market de-risk. | Policy selected only if drawdown <= 25%, Sharpe >= 0, n_bets >= 1,500 target or documented sample exception, bootstrap CI included. |
| **P5** | **P42 — Recommendation Gate v2 + Paper Ledger Closure** | Product A + B | Reissue moneyline PAPER recommendation rows using v2 model/policy and close ledger. | Recommendation rows include risk profile, gate reasons, expected value, paper stake; ledger has 0 unsettled rows where outcomes exist. |
| **P6** | **P43 — TSL Market Taxonomy + Schema Pack** | Product A | Define Taiwan Sports Lottery market contracts beyond moneyline. | Schemas and labels for moneyline, run line/HDC, totals/OU, first 5, odd/even, team total; blocked markets explicit. |
| **P7** | **P44 — Run Line + Totals PAPER Prototype** | Product A | Add first non-moneyline markets in paper mode. | HDC and OU have labels, market odds fields, no-lookahead features, simulator integration, abstention rules. |
| **P8** | **P45 — Live/Approved TSL Snapshot Bridge** | Data / ops | Ingest approved snapshots without placing orders or writing production DB. | Snapshot freshness, source refs, timestamps, and TSL-vs-historical provenance surfaced in rows. |
| **P9** | **P46 — Daily Ops + Drift Monitoring** | Ops | Monitor multi-market daily outputs, data freshness, blocked reasons, model drift, risk drift. | Daily dashboard/report with Brier/ECE/ROI/CLV proxy where available, gate reason changes, source outages. |
| **P10** | **P47 — Production Proposal Gate** | Governance | Only after paper and live-shadow evidence. | Human approval, rollback plan, no-bet fail-safe, live shadow window, multi-day stability evidence. |

---

## 6. Immediate Execution Plan

### Next 24 hours

1. **Run P37.5 checker and produce operator action packet**  
   Confirm missing `odds_approval_record.json` and `odds_2024_approved.csv`; provide a fill-in checklist. This is quick and keeps the data owner unblocked.

2. **Start P38A feature adapter design**  
   Build a contract mapping P32 Retrosheet fields to pregame-safe model features. Do not use final scores, home/away runs, winner, or any postgame field as features.

3. **Define OOF rebuild acceptance gate**  
   Required outputs: `p_model`, `p_oof`, `fold_id`, `model_version`, `source_prediction_ref`, `generated_without_y_true=true`.

### Next 72 hours

1. Implement `p38a_retrosheet_feature_adapter.py` and tests.
2. Run 2024 OOF prediction rebuild with deterministic folds.
3. If manual odds files arrive, run P37 gate and build P38B licensed odds import artifact.
4. If odds files do not arrive, continue prediction rebuild and keep odds path blocked with explicit operator action.

### Next 7 days

1. Build 2024 joined input if P0 + P1 both clear.
2. Run 2024+2025 true-date replay and sample-density audit.
3. Re-run strategy policy grid on expanded sample.
4. Update moneyline recommendation gate v2.
5. Begin TSL market taxonomy/schema pack for HDC/OU/F5/odd-even/team total.

---

## 7. P0 Task Spec — 2024 Retrosheet Feature Adapter + OOF Rebuild

**Mission:** produce a leakage-safe 2024 prediction probability source from P32 game logs.

**Inputs:**
- `data/mlb_2024/processed/mlb_2024_game_identity_outcomes_joined.csv`
- Existing model patterns in `wbc_backend/models/walk_forward_logistic.py`
- Existing P13/P15/P16 contracts for `p_oof`, `game_id`, `paper_only`, `production_ready`

**Required modules:**
- `wbc_backend/recommendation/p38a_retrosheet_feature_adapter.py`
- `wbc_backend/recommendation/p38a_oof_prediction_builder.py`
- `scripts/run_p38a_2024_oof_prediction_rebuild.py`
- Tests for leakage, determinism, required fields, and CLI output

**Must not use as features:**
- `home_score`, `away_score`, `y_true_home_win`, `winner`, `run_diff`, `total_runs`, postgame outcome fields.

**Feature candidates allowed for first version:**
- rolling team win rate using games strictly before current date
- rolling run differential using games strictly before current date
- home/away indicator
- rest days computed from prior game dates only
- simple season-to-date team strength deltas

**Gate outcomes:**
- `P38A_2024_OOF_PREDICTION_READY`
- `P38A_BLOCKED_FEATURE_COVERAGE_INSUFFICIENT`
- `P38A_BLOCKED_LEAKAGE_RISK`
- `P38A_FAIL_INPUT_MISSING`
- `P38A_FAIL_NON_DETERMINISTIC`

---

## 8. P1 Task Spec — Licensed Odds Approval + Import Artifact

**Mission:** move from P37.5 documentation to a real, license-safe 2024 moneyline odds artifact.

**Inputs expected from operator/data owner:**
- `data/mlb_2024/manual_import/odds_approval_record.json`
- `data/mlb_2024/manual_import/odds_2024_approved.csv`

**Required checks:**
- approval record fields complete
- `internal_research_allowed=true`
- `redistribution_allowed=false` is accepted and raw odds are not committed
- odds CSV has required 11 columns
- no forbidden outcome columns
- moneyline market only for this phase
- `paper_only=true`, `production_ready=false`

**Gate outcomes:**
- `P37_MANUAL_ODDS_PROVISIONING_GATE_READY`
- `P37_BLOCKED_APPROVAL_RECORD_MISSING`
- `P37_BLOCKED_MANUAL_ODDS_FILE_MISSING`
- `P37_BLOCKED_LICENSE_NOT_ALLOWED_FOR_RESEARCH`
- `P37_BLOCKED_MANUAL_ODDS_INVALID`

---

## 9. Stop Rules

Do not proceed to production, live betting, or live TSL integration until all of the following are true:

- Expanded historical sample clears stability audit or explicitly documents a statistically acceptable exception.
- Odds source is licensed and approval is documented.
- Recommendation rows and ledgers are fully identity-joined and settled.
- Strategy policy passes drawdown, Sharpe, bootstrap CI, and exposure rules.
- Multi-market schemas are paper-validated before any live source is trusted.
- Human approval exists for any production proposal.

---

## 10. Marker

`CTO_MLB_BETTING_ROADMAP_V4_20260513_READY`

