# Research Odds Dataset Download — DEFERRED (2026-05-13)

**Status:** DOWNLOAD DEFERRED — NO ACCEPTABLE_FOR_RESEARCH REAL-DATA SOURCE FOUND  
**Author:** CTO Agent  
**Date:** 2026-05-13  
**Scope:** Deferred path documentation for P1 investigation  
**Acceptance Marker:** RESEARCH_ODDS_DOWNLOAD_DEFERRED_20260513_READY

---

## 1. Reason for Deferral

At the time of this investigation (2026-05-13), no freely downloadable,
license-clear MLB 2022–2024 moneyline closing odds dataset was found.

### Candidate Status Summary

| Source                             | Deferral Reason                                               |
|------------------------------------|---------------------------------------------------------------|
| SBRO MLB Archive                   | REJECTED — data stops at 2021; ToS prohibits reproduction    |
| Kaggle 50-row sample               | NOT SUFFICIENT — structural validation only; need full dataset |
| Kaggle full dataset                | MANUAL_REVIEW_REQUIRED — requires paid purchase (user decision) |
| AusSportsBetting.com               | MANUAL_REVIEW_REQUIRED — site inaccessible; ToS unverified   |
| GitHub community repos             | REJECTED — no viable repos found                             |

**Bottom line:** 2 sources are pending human action. Until those are unlocked,
the download path is deferred.

---

## 2. Deferred Path Actions Required

| Action                                      | Owner           | Priority | Unblocks                  |
|---------------------------------------------|-----------------|----------|---------------------------|
| Navigate AusSportsBetting.com manually: confirm ToS, check 2024 coverage, note CSV schema | User | HIGH | MANUAL_REVIEW_SOURCE-04 |
| Decide whether to purchase Kaggle full dataset (CC BY-NC 4.0, ~$5-20 on Gumroad) | User | MEDIUM | MANUAL_REVIEW_SOURCE-03b |
| Provide manual-import CSV from personal sportsbook history | User | HIGH | Immediate P38A replay |

---

## 3. Directory Structure Established (Even Without Data)

The following directories and gitkeep files have been created to define the
local-only data storage path for when data eventually arrives.

```
data/research_odds/
├── local_only/           <- real odds data; .gitignore'd; never committed
│   └── .gitkeep          <- placeholder; documents path existence
├── fixtures/             <- synthetic / approved fixture data; can commit
│   └── EXAMPLE_TEMPLATE.csv  <- empty template for schema reference
└── README.md             <- explains the directory policy
```

---

## 4. When Data Becomes Available

When any ACCEPTABLE_FOR_RESEARCH odds source is provisioned, execute:

### Step 1: Store locally
```bash
# Real data → local_only ONLY
cp ~/Downloads/mlb_odds_2024.csv \
  /path/to/Betting-pool-p13/data/research_odds/local_only/
```

### Step 2: Validate against schema
```bash
python scripts/validate_research_odds_import.py \
  data/research_odds/local_only/mlb_odds_2024.csv
```
Expected output: `{"valid": true, "errors": [], "row_count": NNNN}`

### Step 3: Run fixture smoke test
```bash
pytest tests/test_research_odds_join_fixture.py -v
```
All 5 assertions must pass before proceeding to real data join.

### Step 4: Run date-range sample join
```bash
python scripts/research_odds_join_certifier.py \
  --retrosheet data/mlb_2024/processed/mlb_2024_game_identity.csv \
  --odds data/research_odds/local_only/mlb_odds_2024.csv \
  --date-range 2024-04-01 2024-04-30 \
  --output data/mlb_2024/processed/join_report_2024_april.json
```

### Step 5: Update join certification status
- Update `research_odds_join_certification_plan_20260513.md` checklist
- If join rate ≥ 90%: mark `JOIN_CERT_RESEARCH_ODDS_READY`
- If join rate < 90%: triage `RETROSHEET_ONLY_NO_ODDS` cases and remediate

### Step 6: Create LOCAL_ONLY_MANIFEST.md
```
data/research_odds/local_only/LOCAL_ONLY_MANIFEST.md

Source: [source name]
License: [CC BY-NC 4.0 | user_owned | personal_noncommercial]
Attribution: [required attribution text]
Downloaded: [YYYY-MM-DD]
Scope: research_only
Do NOT commit this directory.
```

---

## 5. .gitignore Rules Required

The following entries must be present in `.gitignore`:

```gitignore
# Research odds — local only, never commit raw data
data/research_odds/local_only/
# Keep fixtures visible but not raw data
!data/research_odds/fixtures/
!data/research_odds/README.md
# Retrosheet raw game log — large file, not needed in CI
data/mlb_2024/raw/
```

Check current .gitignore coverage:
```bash
grep -n "research_odds\|mlb_2024/raw" .gitignore || echo "NOT YET IN GITIGNORE"
```

---

## 6. Current State

- [ ] Kaggle full dataset: **PENDING USER PURCHASE DECISION**
- [ ] AusSportsBetting: **PENDING MANUAL SITE CHECK**
- [ ] Manual user-provided CSV: **PENDING USER ACTION**
- [x] `data/research_odds/local_only/` directory: **CREATED (empty)**
- [x] `data/research_odds/fixtures/` directory: **CREATED (EXAMPLE_TEMPLATE.csv)**
- [x] Join certification plan: **CREATED (see TRACK 4)**
- [x] Manual import contract: **CREATED (see TRACK 3)**

---

## 7. Acceptance Criteria for Unblocking

| Criterion                                    | Status                   |
|----------------------------------------------|--------------------------|
| At least 1 ACCEPTABLE real-data source with 2024 MLB coverage | ❌ NOT YET |
| Schema validation script exists               | ❌ Planned, not built     |
| Fixture smoke test passes                     | ❌ Planned, not built     |
| Sample join rate ≥ 90% on April 2024          | ❌ Blocked on data        |
| `JOIN_CERT_RESEARCH_ODDS_READY` achieved       | ❌ NOT YET               |

---

**Acceptance Marker:** RESEARCH_ODDS_DOWNLOAD_DEFERRED_20260513_READY
