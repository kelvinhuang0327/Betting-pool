# Free-Source Odds Feasibility Spike — 2026-05-13

**Status:** RESEARCH FEASIBILITY ONLY  
**Author:** CEO/CTO Agent  
**Date:** 2026-05-13  
**Acceptance Marker:** FREE_SOURCE_ODDS_FEASIBILITY_SPIKE_20260513_READY

---

## ⚠️ Scope Declaration

> **This document is a research feasibility assessment ONLY.**
> It is NOT a production odds source.
> It does NOT constitute an approved data import.
> It does NOT supersede or modify P37.5 Licensed Odds Approval Package.
> No odds data is written to any ledger, database, or artifact in this document.

---

## 1. Background

The P37.5 Licensed Odds Approval Package currently blocks the P38/P39 replay
pipeline due to the unavailability of 2024 licensed closing odds.

This spike evaluates whether a **research-grade, non-production, non-wagering
odds proxy** can be assembled from free or community sources to unblock
feasibility exploration while the formal approval path continues in parallel.

**Linked blocker:** `p37_5_manual_odds_approval_package_report.md`  
(in `00-BettingPlan/20260513/` — do NOT modify that file)

---

## 2. Source Type Evaluation

### 2.1 Historical Public Odds Archives

| Attribute                  | Assessment                                                    |
|----------------------------|---------------------------------------------------------------|
| **Source examples**        | The Odds Archive, Betmetrics historical, Pinnacle historical  |
| **Availability**           | Partial — some free tiers cover pre-2023; 2024 often behind paywall |
| **License risk**           | MEDIUM — free tiers typically allow personal/research use; commercial use prohibited |
| **Field completeness**     | Moderate — moneyline often available; spreads/totals may be missing |
| **Closing odds available** | Partial — opening lines common; true closing lines rarer in free tiers |
| **Date/game/team mapping** | MEDIUM RISK — team name normalization required (LAD vs Los Angeles Dodgers) |
| **P38/P39 replay use**     | CONDITIONAL — usable as proxy only; must be flagged as non-authoritative |
| **Research classification** | MANUAL_REVIEW_REQUIRED                                       |

---

### 2.2 Sportsbook Snapshot Archives (Wayback / Web Archive)

| Attribute                  | Assessment                                                    |
|----------------------------|---------------------------------------------------------------|
| **Source examples**        | Wayback Machine snapshots of DraftKings, FanDuel, BetMGM     |
| **Availability**           | VERY LIMITED — sporadic capture schedule, not game-complete  |
| **License risk**           | LOW (robots.txt compliance) — public web archiving           |
| **Field completeness**     | POOR — only captures visible page state, incomplete for all games |
| **Closing odds available** | VERY RARE — snapshots are time-point, not game-lifecycle      |
| **Date/game/team mapping** | HIGH RISK — requires OCR/scraping + normalization            |
| **P38/P39 replay use**     | NOT RECOMMENDED as primary source                            |
| **Research classification** | REJECTED_FOR_LICENSE_RISK (commercial site ToS concern)     |

---

### 2.3 Community Datasets

| Attribute                  | Assessment                                                    |
|----------------------------|---------------------------------------------------------------|
| **Source examples**        | Kaggle (MLB odds datasets), GitHub community scrapes, Reddit /r/sportsbook data posts |
| **Availability**           | GOOD — several 2020-2024 MLB moneyline datasets exist         |
| **License risk**           | LOW-MEDIUM — typically CC0 or MIT licensed; source scrape origin may vary |
| **Field completeness**     | VARIABLE — moneyline common; totals/run line coverage varies by dataset |
| **Closing odds available** | DATASET-SPECIFIC — best datasets include open + close        |
| **Date/game/team mapping** | MEDIUM RISK — game_id matching to Retrosheet format required |
| **P38/P39 replay use**     | ACCEPTABLE WITH VALIDATION — must join-certify against Retrosheet game log |
| **Research classification** | ACCEPTABLE_FOR_RESEARCH (with join-cert step)               |

**Recommended community datasets for investigation:**
- Baseball-Reference historical lines (partial, free tier)
- Retrospective odds from retrosheet.org community mirrors
- Kaggle: "MLB Game Odds 2012-2023" style datasets

---

### 2.4 Manual-Import CSV

| Attribute                  | Assessment                                                    |
|----------------------------|---------------------------------------------------------------|
| **Source examples**        | User-maintained CSV from sportsbook PDF exports, screenshots, manual entry |
| **Availability**           | ON REQUEST — requires user action                            |
| **License risk**           | NONE — user-owned data                                       |
| **Field completeness**     | USER-DEFINED — can include any fields user captures          |
| **Closing odds available** | YES — if user captures at close                              |
| **Date/game/team mapping** | LOW RISK — user controls mapping                             |
| **P38/P39 replay use**     | ACCEPTABLE — must follow `manual_import_artifact_contract.md` schema |
| **Research classification** | ACCEPTABLE_FOR_RESEARCH                                     |

**Note:** Manual import CSV is already the preferred fallback path per P37.5.
This confirms it remains the safest non-licensed route.

---

### 2.5 Synthetic / Fixture Fallback

| Attribute                  | Assessment                                                    |
|----------------------------|---------------------------------------------------------------|
| **Source examples**        | Hardcoded fixture odds for known games (e.g., World Series 2024), EV-neutral synthetic lines |
| **Availability**           | ALWAYS — generated in-repo                                   |
| **License risk**           | NONE                                                         |
| **Field completeness**     | FULL — we define the schema                                  |
| **Closing odds available** | SYNTHETIC ONLY — not ground truth                           |
| **Date/game/team mapping** | ZERO RISK — fixture-controlled                               |
| **P38/P39 replay use**     | ACCEPTABLE FOR SMOKE TESTS ONLY — must be flagged `is_synthetic=True` |
| **Research classification** | ACCEPTABLE_FOR_RESEARCH (smoke/fixture only, not production) |

---

## 3. Summary Classification Table

| Source Type                    | Classification                | Notes                                     |
|--------------------------------|-------------------------------|-------------------------------------------|
| Historical public odds archives | MANUAL_REVIEW_REQUIRED       | 2024 coverage gap; closing lines rare     |
| Sportsbook snapshot archives    | REJECTED_FOR_LICENSE_RISK    | ToS risk; poor coverage                   |
| Community datasets              | ACCEPTABLE_FOR_RESEARCH      | Requires join-cert step                   |
| Manual-import CSV               | ACCEPTABLE_FOR_RESEARCH      | Preferred safe path per P37.5 fallback    |
| Synthetic / fixture fallback    | ACCEPTABLE_FOR_RESEARCH      | Smoke tests only; `is_synthetic=True` tag |

---

## 4. Recommended Research Path

Based on this feasibility spike, the recommended non-production research path is:

```
Priority 1: Manual-import CSV (user-provided)
  → Already in P37.5 fallback spec
  → Zero license risk
  → Flexible schema

Priority 2: Community datasets (Kaggle / GitHub)
  → Must run join-cert against Retrosheet game_id
  → Must verify dataset license (CC0 / MIT)
  → Must flag as non-authoritative in all artifacts

Priority 3: Synthetic fixtures
  → For smoke tests and schema validation only
  → Must set is_synthetic=True in all prediction artifacts
```

---

## 5. Integration Constraints

Any odds data sourced from this feasibility path MUST adhere to:

1. **No production write** — Never write to any live betting system, TSL, or wagering interface.
2. **No production ledger** — Never write to `p37_5_manual_odds_approval_package_report.md` or any approved ledger.
3. **Research flag** — All artifacts must include `"source_type": "research_proxy"` or `"is_research": true`.
4. **Separate artifact namespace** — Store research odds in `data/research_odds/` or `data/fixtures/`, never in `data/approved/`.
5. **Join certification required** — Any community dataset must pass game-level join against Retrosheet before use in P38/P39.
6. **Edge claims prohibited** — Research-grade odds proxies cannot be used to make edge claims or wagering decisions.

---

## 6. Dependency on P37.5

This feasibility spike is **additive** to the formal P37.5 path, not a replacement:

| Path                        | Status      | Purpose                                    |
|-----------------------------|-------------|--------------------------------------------|
| P37.5 Licensed Odds         | BLOCKED     | Formal approval; required for production   |
| This feasibility spike      | ACTIVE      | Unblock research while P37.5 proceeds      |

P37.5 must still be completed before any production or wagering use of odds data.

---

## 7. Next Steps (Research Track)

- [ ] Identify 1-2 Kaggle/GitHub community MLB odds datasets (2022-2024)
- [ ] Verify license terms for each candidate dataset
- [ ] Run game-level join test: community dataset ↔ Retrosheet 2024 game log
- [ ] Produce `join_certification_report_research_odds.md`
- [ ] Flag all research artifacts with `is_research: true`
- [ ] DO NOT start P38A runtime until join cert passes

---

**Acceptance Marker:** FREE_SOURCE_ODDS_FEASIBILITY_SPIKE_20260513_READY

---

## 2026-05-13 P1 Candidate Investigation Update

**Agent:** CTO Agent  
**Session:** P1 — Free-Source Odds Community Dataset Investigation  
**Status:** CANDIDATE_LICENSE_REVIEW_PENDING

### Candidate Inventory Results

7 candidates were evaluated for MLB 2022-2024 moneyline closing odds:

| Category                    | Count | Sources                                             |
|-----------------------------|-------|-----------------------------------------------------|
| ACCEPTABLE_FOR_RESEARCH     | 3     | Retrosheet GL (join anchor), manual-import CSV, synthetic fixtures |
| MANUAL_REVIEW_REQUIRED      | 2     | Kaggle US Sports Master (paid), AusSportsBetting.com |
| REJECTED                    | 2     | SBRO (data stops 2021 + license), GitHub (no repos found) |

**Key finding:** No freely downloadable, license-clear 2022-2024 MLB moneyline closing odds dataset was found automatically. The download path has been deferred (see `research_odds_dataset_download_deferred_20260513.md`).

### Current Join Certification Status

- `JOIN_CERT_RESEARCH_ODDS_READY`: **NOT achieved**
- Blocker: No real-data odds source has been provisioned
- Join certification plan is ready and waiting for data (see TRACK 4 artifact)
- Fixture-only smoke test skeleton defined but not yet built

### Artifacts Produced in P1 Session

| Artifact                                                   | Status    | Acceptance Marker                                       |
|------------------------------------------------------------|-----------|----------------------------------------------------------|
| research_odds_candidate_inventory_20260513.md              | ✅ Created | RESEARCH_ODDS_CANDIDATE_INVENTORY_20260513_READY         |
| research_odds_license_risk_matrix_20260513.md              | ✅ Created | RESEARCH_ODDS_LICENSE_RISK_MATRIX_20260513_READY         |
| research_odds_manual_import_contract_20260513.md           | ✅ Created | RESEARCH_ODDS_MANUAL_IMPORT_CONTRACT_20260513_READY      |
| research_odds_join_certification_plan_20260513.md          | ✅ Created | RESEARCH_ODDS_JOIN_CERTIFICATION_PLAN_20260513_READY     |
| research_odds_dataset_download_deferred_20260513.md        | ✅ Created | RESEARCH_ODDS_DOWNLOAD_DEFERRED_20260513_READY           |
| data/research_odds/ directory structure                    | ✅ Created | local_only/.gitkeep + fixtures/EXAMPLE_TEMPLATE.csv      |
| .gitignore updated                                         | ✅ Updated | research_odds/local_only/ + mlb_2024/raw/                |

### Required Human Actions to Unblock

| Action                                           | Priority | Unblocks                          |
|--------------------------------------------------|----------|-----------------------------------|
| Manually check AusSportsBetting.com (ToS + 2024 data availability) | HIGH | Source-04 unlock |
| Decide whether to purchase Kaggle full dataset   | MEDIUM   | Source-03b unlock                 |
| Provide manual-import CSV from personal history  | HIGH     | Immediate P38A replay without waiting |

### Licensed Odds Approval Reminder

Even if a research-grade odds source is provisioned and join-certified, it does NOT replace the production-path licensed odds approval requirement. P37.5 licensed odds approval is still required before any production edge claims, live betting, or wagering decisions.

**Acceptance Marker:** FREE_SOURCE_ODDS_P1_INVESTIGATION_UPDATE_20260513_READY

---

## 2026-05-13 P1.5 License Review / Join Smoke Update

### Summary Counters

| Metric | Count |
|---|---:|
| manual review candidates count | 3 |
| ACCEPTABLE_FOR_LOCAL_RESEARCH count | 0 |
| ACCEPTABLE_FOR_FIXTURE_ONLY count | 1 |
| MANUAL_APPROVAL_REQUIRED count | 2 |
| rejected count | 0 |

### Decisions and Status

- local-only sample decision: `FIXTURE_ONLY_SMOKE_ALLOWED_20260513`
- join smoke status: `FIXTURE_ONLY_JOIN_SMOKE_READY`
- `JOIN_CERT_RESEARCH_ODDS_READY`: **NOT achieved**
- licensed odds approval still required: **YES** (P37.5 remains mandatory for production path)

### Supporting Artifacts (P1.5)

- `research_odds_manual_review_audit_20260513.md`
- `research_odds_local_only_decision_20260513.md`
- `research_odds_join_smoke_report_20260513.md`

**Acceptance Marker:** RESEARCH_ODDS_P15_LICENSE_JOIN_UPDATE_20260513_READY
