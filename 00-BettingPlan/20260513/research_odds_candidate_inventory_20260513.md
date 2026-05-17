# Research Odds Candidate Inventory — 2026-05-13

**Status:** RESEARCH FEASIBILITY — P1 CANDIDATE INVESTIGATION  
**Author:** CTO Agent  
**Date:** 2026-05-13  
**Scope:** MLB 2022–2024 moneyline odds, research-only, non-production  
**Acceptance Marker:** RESEARCH_ODDS_CANDIDATE_INVENTORY_20260513_READY

---

## ⚠️ Scope Declaration

> This inventory is a research feasibility assessment ONLY.
> It does NOT constitute approval to import any odds source.
> No odds data is written to any ledger, database, or prediction artifact.
> All findings are for planning and governance only.

---

## 1. Investigation Methodology

Web search + direct URL inspection was performed on the following source categories:
- Kaggle sports betting datasets
- SportsBookReviewsOnline.com historical archives
- AusSportsBetting.com historical data
- GitHub topic searches (mlb-odds, sports-betting-odds)
- Retrosheet.org (game logs — known no-odds source)

---

## 2. Candidate Inventory

---

### CANDIDATE-01: Retrosheet.org — Game Logs (GL2024.TXT)

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | Retrosheet 2024 Game Logs                                       |
| **source_url**                 | https://www.retrosheet.org/gamelogs/gl2024.zip                  |
| **provider / maintainer**      | Retrosheet (nonprofit, volunteers)                              |
| **available seasons**          | 1919–2024 (game logs)                                           |
| **markets included — moneyline** | ❌ NOT INCLUDED                                               |
| **markets included — run line** | ❌ NOT INCLUDED                                                |
| **markets included — totals**  | ❌ NOT INCLUDED                                                 |
| **closing line included**      | ❌ NO — game results only, no odds data                        |
| **opening line included**      | ❌ NO                                                           |
| **timestamp / snapshot time**  | ❌ NO odds; game date / time present                           |
| **team naming format**         | 3-letter Retrosheet code (e.g., LAN, SDN, NYA, BOS)            |
| **date format**                | YYYYMMDD (positional column 1)                                  |
| **game identifier**            | Derived: game_date + away_team + home_team + game_number        |
| **home/away availability**     | ✅ YES — positions 4 (visitor) and 7 (home)                    |
| **odds format**                | N/A — no odds                                                   |
| **license / terms**            | Retrosheet Notice: free for any use including commercial; attribution required |
| **redistribution risk**        | ✅ LOW — explicitly permitted                                  |
| **research-only suitability**  | ✅ YES — but no odds, only game results                        |
| **join risk vs odds**          | Provides the JOIN TARGET (game_key); odds source must map to this |
| **recommendation**             | **ACCEPTABLE_FOR_RESEARCH** — as join anchor only, no odds content |
| **notes**                      | GL2024.TXT already present in repo at `data/mlb_2024/raw/gl2024.txt` (2,429 rows, untracked) |

---

### CANDIDATE-02: SportsbookReviewsOnline.com (SBRO) — MLB Odds Archive

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | SBRO MLB Historical Odds Archive                                |
| **source_url**                 | https://www.sportsbookreviewsonline.com/scoresoddsarchives/mlb/ |
| **provider / maintainer**      | Sportsbook Reviews Online (commercial sportsbook review site)   |
| **available seasons**          | 2010–2021 ONLY (archive frozen; "will not be updated")         |
| **markets included — moneyline** | ✅ Opening + Closing moneyline per game                       |
| **markets included — run line** | ✅ YES (listed in description)                                 |
| **markets included — totals**  | ✅ YES (listed in description)                                  |
| **closing line included**      | ✅ YES                                                          |
| **opening line included**      | ✅ YES                                                          |
| **timestamp / snapshot time**  | ❌ UNKNOWN — not confirmed in documentation                    |
| **team naming format**         | Human-readable team names (e.g., "New York Yankees")           |
| **date format**                | UNKNOWN from external inspection                               |
| **game identifier**            | ❌ NO standardized game_id — requires manual construction       |
| **home/away availability**     | ✅ YES                                                          |
| **odds format**                | American moneyline                                             |
| **license / terms**            | RESTRICTIVE: "All content protected by copyright... You may not use or reproduce without express written consent" |
| **redistribution risk**        | ⚠️ HIGH — terms explicitly prohibit reproduction               |
| **research-only suitability**  | ❌ NO — license prohibits reproduction of content              |
| **join risk vs Retrosheet**    | HIGH — team name normalization required; no Retrosheet game_id |
| **recommendation**             | **REJECTED_FOR_NO_2024_COVERAGE** (primary) + LICENSE concern  |
| **notes**                      | 2022, 2023, 2024 data is completely absent. Archive explicitly states it will not be updated. Even if license were permissive, 2022-2024 data gap is disqualifying. |

---

### CANDIDATE-03: Kaggle — US Sports Master Closing Odds (oliviersportsdata)

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | US Sports Master — Closing Odds 9 Sports                       |
| **source_url**                 | https://www.kaggle.com/datasets/oliviersportsdata/us-sports-master-historical-closing-odds |
| **provider / maintainer**      | Olivier Sports Data (individual researcher)                     |
| **available seasons**          | MLB: 2006–2025 (46,235 matches)                                 |
| **markets included — moneyline** | ✅ American Moneyline ONLY                                    |
| **markets included — run line** | ❌ NOT INCLUDED for MLB                                        |
| **markets included — totals**  | ❌ NOT INCLUDED for MLB                                         |
| **closing line included**      | ✅ YES — closing moneyline confirmed                           |
| **opening line included**      | ❌ UNKNOWN — described as "closing odds" collection            |
| **timestamp / snapshot time**  | ❌ UNKNOWN — not documented in free sample metadata            |
| **team naming format**         | UNKNOWN — not visible in free 50-row sample description        |
| **date format**                | UNKNOWN — need to inspect sample                               |
| **game identifier**            | ❌ UNKNOWN — not documented; likely date + team               |
| **home/away availability**     | ✅ LIKELY — moneyline typically includes H/A                   |
| **odds format**                | American moneyline                                             |
| **license / terms**            | CC BY-NC 4.0 — Attribution-NonCommercial 4.0 International     |
| **redistribution risk**        | MEDIUM — allowed for non-commercial use with attribution; raw dataset redistribution requires license compliance |
| **research-only suitability**  | ✅ YES (CC BY-NC 4.0 permits non-commercial research)          |
| **join risk vs Retrosheet**    | MEDIUM — team name mapping required; no Retrosheet game_id    |
| **recommendation**             | **MANUAL_REVIEW_REQUIRED**                                     |
| **notes**                      | Free tier: 50-row structural sample only — insufficient for 2022-2024 replay. Full dataset (218,700 matches) requires paid purchase on Gumroad. License is CC BY-NC 4.0 — non-commercial research use permitted. Attribution required. Raw dataset should NOT be committed to git; reference download instructions only. Need to verify: (1) cost of full dataset, (2) team naming format, (3) game identifier availability, (4) whether 2024 MLB is confirmed in full dataset. |

---

### CANDIDATE-04: AusSportsBetting.com — Historical MLB Results and Odds

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | AusSportsBetting MLB Historical Odds                           |
| **source_url**                 | https://www.aussportsbetting.com/data/historical-mlb-results-and-odds-data/ |
| **provider / maintainer**      | AusSportsBetting.com (Australian-based sports data site)       |
| **available seasons**          | UNKNOWN — site inaccessible during investigation                |
| **markets included — moneyline** | LIKELY — based on site description from indirect sources      |
| **markets included — run line** | LIKELY                                                         |
| **markets included — totals**  | LIKELY                                                          |
| **closing line included**      | UNKNOWN — site inaccessible                                    |
| **opening line included**      | UNKNOWN                                                         |
| **timestamp / snapshot time**  | UNKNOWN                                                         |
| **team naming format**         | UNKNOWN                                                         |
| **date format**                | UNKNOWN                                                         |
| **game identifier**            | UNKNOWN                                                         |
| **home/away availability**     | UNKNOWN                                                         |
| **odds format**                | UNKNOWN                                                         |
| **license / terms**            | Previously documented as "personal, non-commercial use" — UNVERIFIED |
| **redistribution risk**        | UNKNOWN — needs manual review                                  |
| **research-only suitability**  | UNKNOWN — site was unreachable                                 |
| **join risk vs Retrosheet**    | HIGH UNKNOWN — needs manual inspection                        |
| **recommendation**             | **MANUAL_REVIEW_REQUIRED**                                     |
| **notes**                      | Site was inaccessible during this investigation. AusSportsBetting is historically known to publish seasonal CSV/XLSX odds files for MLB. Must manually navigate site to: (1) confirm 2022-2024 availability, (2) read terms of use, (3) inspect CSV schema. Do NOT download until terms are confirmed. |

---

### CANDIDATE-05: GitHub Community MLB Historical Odds Repositories

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | GitHub Community MLB Odds Repositories                         |
| **source_url**                 | https://github.com/topics/mlb-odds (and general search)        |
| **provider / maintainer**      | Various community contributors                                  |
| **available seasons**          | NONE FOUND                                                      |
| **markets included**           | N/A — no repos found                                           |
| **closing line included**      | N/A                                                             |
| **license / terms**            | N/A                                                             |
| **recommendation**             | **REJECTED_FOR_INCOMPLETE_FIELDS**                             |
| **notes**                      | GitHub topic `mlb-odds` has ZERO public repositories. GitHub topic `sports-betting-odds` has 4 repos — none contain historical MLB CSV datasets. No viable community MLB odds repo found on GitHub as of 2026-05-13. This path is effectively a dead end. |

---

### CANDIDATE-06: Manual-Import CSV (User-Provided)

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | Manual-Import CSV (User-Provided Odds Data)                    |
| **source_url**                 | N/A — user-owned                                               |
| **provider / maintainer**      | User / researcher                                              |
| **available seasons**          | USER-DEFINED — any season the user captures manually           |
| **markets included — moneyline** | ✅ USER-DEFINED                                               |
| **markets included — run line** | USER-DEFINED                                                   |
| **markets included — totals**  | USER-DEFINED                                                    |
| **closing line included**      | ✅ YES if user captures at game close                          |
| **opening line included**      | ✅ YES if user captures at market open                         |
| **timestamp / snapshot time**  | USER-DEFINED                                                    |
| **team naming format**         | USER-DEFINED — contract schema defines normalization           |
| **date format**                | ISO 8601 per contract                                          |
| **game identifier**            | Optional retrosheet_game_id_optional field per contract        |
| **home/away availability**     | ✅ YES — required per contract                                 |
| **odds format**                | American moneyline required per contract                       |
| **license / terms**            | NONE — user-owned data                                         |
| **redistribution risk**        | NONE                                                            |
| **research-only suitability**  | ✅ YES — ACCEPTABLE_FOR_RESEARCH                               |
| **join risk vs Retrosheet**    | LOW — user controls team naming and date format per contract   |
| **recommendation**             | **ACCEPTABLE_FOR_RESEARCH**                                    |
| **notes**                      | Zero license risk. User controls all data. Safest path per P37.5 fallback spec. Requires user action to provision data. Schema defined in TRACK 3 manual import contract. |

---

### CANDIDATE-07: Synthetic Fixture Data (In-Repo Generated)

| Field                          | Value                                                           |
|--------------------------------|-----------------------------------------------------------------|
| **candidate_name**             | Synthetic Fixture Odds (hardcoded, in-repo)                    |
| **source_url**                 | N/A — generated in-repo                                        |
| **provider / maintainer**      | CTO Agent / repo maintainer                                    |
| **available seasons**          | ANY — generated on demand for specific test games              |
| **markets included — moneyline** | ✅ FULL CONTROL                                               |
| **markets included — run line** | ✅ FULL CONTROL                                                |
| **markets included — totals**  | ✅ FULL CONTROL                                                 |
| **closing line included**      | ✅ YES (synthetic, not ground truth)                           |
| **opening line included**      | ✅ YES (synthetic)                                              |
| **timestamp / snapshot time**  | ✅ FULL CONTROL                                                |
| **team naming format**         | Retrosheet 3-letter code (zero mapping risk)                   |
| **date format**                | ISO 8601                                                       |
| **game identifier**            | ✅ YES — fully controlled Retrosheet-compatible game_key       |
| **home/away availability**     | ✅ YES                                                          |
| **odds format**                | American moneyline                                             |
| **license / terms**            | NONE                                                            |
| **redistribution risk**        | NONE                                                            |
| **research-only suitability**  | ✅ YES — smoke tests and schema validation ONLY                |
| **join risk vs Retrosheet**    | ZERO — fixture is designed to match Retrosheet game_key format |
| **recommendation**             | **ACCEPTABLE_FOR_RESEARCH** (smoke tests only)                 |
| **notes**                      | MUST flag `is_synthetic=True` in all prediction artifacts. NOT ground truth. Cannot be used for EV analysis or edge claims. Limited to pipeline validation and smoke tests. Safe to commit as test fixture. |

---

## 3. Summary Table

| # | Candidate                         | 2024 Coverage | Recommendation                         |
|---|-----------------------------------|---------------|----------------------------------------|
| 1 | Retrosheet GL2024 (join anchor)   | ✅ YES         | ACCEPTABLE_FOR_RESEARCH (no odds)      |
| 2 | SBRO MLB Odds Archive             | ❌ NO (stops 2021) | REJECTED_FOR_NO_2024_COVERAGE     |
| 3 | Kaggle US Sports Master (full)    | ✅ YES (2006-2025) | MANUAL_REVIEW_REQUIRED (paid)      |
| 4 | AusSportsBetting.com              | UNKNOWN       | MANUAL_REVIEW_REQUIRED (site down)     |
| 5 | GitHub Community Repos            | ❌ NONE FOUND  | REJECTED_FOR_INCOMPLETE_FIELDS         |
| 6 | Manual-Import CSV (user-provided) | USER-DEFINED  | ACCEPTABLE_FOR_RESEARCH                |
| 7 | Synthetic Fixture                 | ANY (synthetic) | ACCEPTABLE_FOR_RESEARCH (smoke only) |

---

## 4. Classification Count

| Classification                   | Count | Candidates                          |
|----------------------------------|-------|-------------------------------------|
| ACCEPTABLE_FOR_RESEARCH          | 3     | #1 (anchor), #6 (manual), #7 (synthetic) |
| MANUAL_REVIEW_REQUIRED           | 2     | #3 (Kaggle full), #4 (AusSportsBetting) |
| REJECTED_FOR_NO_2024_COVERAGE    | 1     | #2 (SBRO)                           |
| REJECTED_FOR_INCOMPLETE_FIELDS   | 1     | #5 (GitHub)                         |
| REJECTED_FOR_LICENSE_RISK        | 0     | —                                   |

---

## 5. Critical Gap Summary

**For real-world (non-synthetic) 2022–2024 MLB moneyline closing odds with an
acceptable research license:**

- **0 sources confirmed ACCEPTABLE_FOR_RESEARCH with actual data**
- **2 sources require manual review** (Kaggle full dataset cost + AusSportsBetting access)
- **Best confirmed path**: Manual-import CSV (user-provided)

**Bottom line**: There is currently no freely downloadable, license-clear,
2022–2024 MLB moneyline dataset that can be automatically provisioned.
The P1 investigation must be classified as:

> **CANDIDATE_LICENSE_REVIEW_PENDING**
>
> Pending items:
> 1. User reviews AusSportsBetting.com directly (check accessibility + terms)
> 2. User decides whether to purchase Kaggle US Sports Master full dataset
> 3. User provides manual-import CSV (safest, zero-cost path)

---

**Acceptance Marker:** RESEARCH_ODDS_CANDIDATE_INVENTORY_20260513_READY
