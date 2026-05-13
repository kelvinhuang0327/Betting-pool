# Research Odds License Risk Matrix — 2026-05-13

**Status:** RESEARCH FEASIBILITY — LICENSE ASSESSMENT  
**Author:** CTO Agent  
**Date:** 2026-05-13  
**Scope:** MLB 2022–2024 odds candidate sources, license risk analysis  
**Acceptance Marker:** RESEARCH_ODDS_LICENSE_RISK_MATRIX_20260513_READY

---

## ⚠️ Scope Declaration

> This document assesses license risks for research-only use.
> It does NOT authorize any data import or production use.
> Raw dataset default: **DO NOT COMMIT** unless license is explicitly confirmed clear.
> If license is unclear → `MANUAL_REVIEW_REQUIRED` (non-negotiable).
> If terms prohibit scraping or redistribution → `REJECTED_FOR_LICENSE_RISK` or `LOCAL_ONLY_MANUAL_REVIEW`.

---

## 1. License Risk Matrix

---

### SOURCE-01: Retrosheet.org (Game Logs — No Odds)

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | Retrosheet Public Notice (at retrosheet.org/notice.txt)        |
| **License Summary**                 | "Recipients are free to make any desired use... including selling it, giving it away, or producing commercial products" |
| **Download allowed**                | ✅ YES — explicitly permitted                                  |
| **Research use allowed**            | ✅ YES — explicitly permitted                                  |
| **Redistribution allowed**          | ✅ YES — explicitly permitted                                  |
| **Commit raw dataset to git**       | ✅ YES — permissible, but large files should use .gitignore or LFS |
| **Derivative report allowed**       | ✅ YES                                                          |
| **Attribution required**            | ✅ YES — mandatory notice required (see below)                 |
| **Manual approval required**        | ❌ NO — open to all                                            |
| **Keep download-instructions only** | Preferred for large files (2.5MB) but not required            |
| **Usable in CI fixture**            | ✅ YES (with attribution)                                      |
| **Usable in local-only replay**     | ✅ YES                                                          |
| **Risk Classification**             | ✅ **LOW — ACCEPTABLE_FOR_RESEARCH**                          |
| **Required Attribution Text**       | "The information used here was obtained free of charge from and is copyrighted by Retrosheet. Interested parties may contact Retrosheet at www.retrosheet.org." |
| **Notes**                           | GL2024.TXT already present in repo (untracked). No odds data — use as join anchor only. |

---

### SOURCE-02: SportsbookReviewsOnline.com (SBRO) — MLB Odds Archive

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | SBRO Terms of Service                                          |
| **License Summary**                 | "All content and materials... are the property of our website or its licensors... You may not use or reproduce any content without our express written consent." |
| **Download allowed**                | ⚠️ UNCLEAR — ToS requires "express written consent" for reproduction |
| **Research use allowed**            | ❌ NOT CLEAR — no research exception stated                   |
| **Redistribution allowed**          | ❌ PROHIBITED without written consent                          |
| **Commit raw dataset to git**       | ❌ PROHIBITED — would constitute reproduction                  |
| **Derivative report allowed**       | ⚠️ UNCLEAR — safest to assume no without consent             |
| **Attribution required**            | N/A — reproduction prohibited                                  |
| **Manual approval required**        | Required — "express written consent"                          |
| **Keep download-instructions only** | N/A — data stops at 2021 anyway                               |
| **Usable in CI fixture**            | ❌ NO without written consent                                  |
| **Usable in local-only replay**     | ❌ RISKY without written consent                               |
| **Risk Classification**             | 🔴 **REJECTED_FOR_LICENSE_RISK** (secondary: REJECTED_FOR_NO_2024_COVERAGE) |
| **Notes**                           | Primary rejection reason is no 2022-2024 data. Secondary reason is copyright terms prohibiting reproduction. Even if data existed, license would require explicit written consent before any use. SBRO ToS does not include any research exception. |

---

### SOURCE-03: Kaggle — US Sports Master Closing Odds (oliviersportsdata) — FREE SAMPLE

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | Creative Commons CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International) |
| **License Summary**                 | Non-commercial use permitted with attribution. No derivatives with additional restrictions. |
| **Download allowed**                | ✅ YES (50-row sample on Kaggle, free)                         |
| **Research use allowed**            | ✅ YES — CC BY-NC explicitly permits research and educational use |
| **Redistribution allowed**          | ✅ YES for non-commercial purposes with attribution            |
| **Commit raw dataset to git**       | ⚠️ LOW RISK for sample — but caution: even CC BY-NC has redistribution terms; prefer not to commit |
| **Derivative report allowed**       | ✅ YES — CC BY-NC allows derivative works                      |
| **Attribution required**            | ✅ YES — "oliviersportsdata / kaggle.com/oliviersportsdata" + license statement |
| **Manual approval required**        | ❌ NO — CC BY-NC is self-executing for research               |
| **Keep download-instructions only** | ✅ RECOMMENDED — Kaggle API or web download; don't commit raw CSV |
| **Usable in CI fixture**            | ✅ YES (50-row sample only; must attribute)                    |
| **Usable in local-only replay**     | ✅ YES (sample) — full dataset requires paid purchase         |
| **Risk Classification**             | 🟡 **MANUAL_REVIEW_REQUIRED** (free sample only; full dataset is paid) |
| **Notes**                           | Free tier is 50-row sample (structural validation only, not sufficient for replay). Full dataset (46,235 MLB matches, 2006-2025) requires Gumroad purchase. CC BY-NC 4.0 license is clear for non-commercial research. Cost is the blocker, not the license. Next step: user decides whether to purchase. If purchased, archive at `data/research_odds/local_only/` — do NOT commit CSV. |

---

### SOURCE-03b: Kaggle — US Sports Master Closing Odds — FULL DATASET (paid)

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | CC BY-NC 4.0 (same as sample)                                  |
| **Download allowed**                | ✅ YES (after purchase on Gumroad)                              |
| **Research use allowed**            | ✅ YES — CC BY-NC                                              |
| **Redistribution allowed**          | ✅ YES for non-commercial with attribution                      |
| **Commit raw dataset to git**       | ❌ DO NOT COMMIT — raw dataset should be local-only; prefer download instructions |
| **Derivative report allowed**       | ✅ YES                                                          |
| **Attribution required**            | ✅ YES                                                          |
| **Manual approval required**        | ❌ NO — CC BY-NC is self-executing                             |
| **Keep download-instructions only** | ✅ YES — commit only download instructions + schema docs       |
| **Usable in CI fixture**            | ⚠️ Only if subset is hand-curated AND license attribution is in fixture |
| **Usable in local-only replay**     | ✅ YES (local-only, not committed)                             |
| **Risk Classification**             | 🟡 **MANUAL_REVIEW_REQUIRED** (cost barrier; license clear once purchased) |
| **Notes**                           | If purchased: (1) store at `data/research_odds/local_only/`, (2) add to .gitignore, (3) create `LOCAL_ONLY_MANIFEST.md` with source attribution, (4) extract 10-20 row fixture sample for CI (check license allows fixture extraction). |

---

### SOURCE-04: AusSportsBetting.com — MLB Historical Odds

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | UNVERIFIED — site was inaccessible during investigation        |
| **License Summary**                 | Previously documented (from secondary sources) as "personal, non-commercial use" — NOT CONFIRMED |
| **Download allowed**                | UNKNOWN                                                         |
| **Research use allowed**            | UNKNOWN                                                         |
| **Redistribution allowed**          | UNKNOWN                                                         |
| **Commit raw dataset to git**       | ❌ DO NOT COMMIT until terms verified                          |
| **Derivative report allowed**       | UNKNOWN                                                         |
| **Attribution required**            | UNKNOWN                                                         |
| **Manual approval required**        | UNKNOWN                                                         |
| **Keep download-instructions only** | YES — until terms verified                                     |
| **Usable in CI fixture**            | ❌ NO — do not use until terms verified                        |
| **Usable in local-only replay**     | ❌ NO — do not use until terms verified                        |
| **Risk Classification**             | 🟡 **MANUAL_REVIEW_REQUIRED (LOCAL_ONLY_MANUAL_REVIEW)**      |
| **Notes**                           | This is a candidate for the next review session. User must manually navigate the site to: (1) confirm site is accessible, (2) read ToS/Terms page, (3) check whether 2022-2024 data exists, (4) confirm CSV schema and field coverage, (5) report findings. DO NOT download or use until this review is complete. |

---

### SOURCE-05: GitHub Community Repos

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | N/A — no viable repos found                                    |
| **Risk Classification**             | **REJECTED_FOR_INCOMPLETE_FIELDS** (no repos exist)           |
| **Notes**                           | GitHub topic `mlb-odds` has zero public repositories. This path is a dead end. |

---

### SOURCE-06: Manual-Import CSV (User-Provided)

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | User-owned — no third-party license                            |
| **Download allowed**                | ✅ YES — user provides                                         |
| **Research use allowed**            | ✅ YES — user-owned data                                       |
| **Redistribution allowed**          | User decision — not relevant for local research               |
| **Commit raw dataset to git**       | ⚠️ CAUTION — only if user explicitly approves AND data is truly user-owned (not scraped from licensed source) |
| **Derivative report allowed**       | ✅ YES                                                          |
| **Attribution required**            | User decision                                                  |
| **Manual approval required**        | ✅ YES — requires user action to provide data                  |
| **Keep download-instructions only** | N/A — data comes from user                                     |
| **Usable in CI fixture**            | ✅ YES (with user consent; keep sample small)                  |
| **Usable in local-only replay**     | ✅ YES                                                          |
| **Risk Classification**             | ✅ **LOW — ACCEPTABLE_FOR_RESEARCH**                          |
| **Notes**                           | The only zero-risk path for real odds data. Schema defined in TRACK 3 manual import contract. User must explicitly mark `source_license_status` field in CSV. |

---

### SOURCE-07: Synthetic Fixture Odds

| License Field                       | Assessment                                                     |
|-------------------------------------|----------------------------------------------------------------|
| **License / Terms**                 | NONE — generated in-repo                                       |
| **Commit raw dataset to git**       | ✅ YES — safe to commit as test fixture                        |
| **Usable in CI fixture**            | ✅ YES — explicitly designed for this purpose                  |
| **Usable in local-only replay**     | ✅ YES (smoke tests only; is_synthetic=True required)          |
| **Risk Classification**             | ✅ **LOW — ACCEPTABLE_FOR_RESEARCH** (smoke/CI only)          |
| **Notes**                           | Must always flag `is_synthetic=True`. Must never use for EV or edge claims. |

---

## 2. Summary Risk Table

| Source                             | Download OK | Research OK | Can Commit | CI Fixture | Local Replay | Classification             |
|------------------------------------|-------------|-------------|------------|------------|--------------|----------------------------|
| Retrosheet GL2024 (game logs)      | ✅          | ✅          | ✅ (w/ attr) | ✅       | ✅           | ACCEPTABLE_FOR_RESEARCH    |
| SBRO MLB Archive (2010-2021)       | ⚠️          | ❌          | ❌         | ❌         | ❌           | REJECTED_FOR_LICENSE_RISK  |
| Kaggle 50-row sample               | ✅          | ✅          | ⚠️ cautious | ✅ (50 rows) | ✅         | MANUAL_REVIEW_REQUIRED     |
| Kaggle full dataset (paid)         | ✅ (paid)   | ✅          | ❌ (local only) | ⚠️  | ✅           | MANUAL_REVIEW_REQUIRED     |
| AusSportsBetting                   | UNKNOWN     | UNKNOWN     | ❌         | ❌         | ❌           | MANUAL_REVIEW_REQUIRED     |
| GitHub community repos             | N/A         | N/A         | N/A        | N/A        | N/A          | REJECTED (no repos)        |
| Manual-import CSV                  | ✅          | ✅          | ⚠️ (user-approved only) | ✅ | ✅      | ACCEPTABLE_FOR_RESEARCH    |
| Synthetic fixtures                 | N/A         | ✅          | ✅         | ✅         | ✅           | ACCEPTABLE_FOR_RESEARCH    |

---

## 3. Mandatory Rules (Non-Negotiable)

1. **Default: Do NOT commit raw dataset**
   - Raw odds CSV files go into `data/research_odds/local_only/` + `.gitignore` only
   - Exception: synthetic fixtures and manual-import fixtures explicitly approved by user

2. **License UNKNOWN → MANUAL_REVIEW_REQUIRED**
   - AusSportsBetting falls here until user manually confirms terms

3. **No license gate bypass**
   - Research urgency does NOT lower the license bar
   - If terms are ambiguous, assume restrictive

4. **No production use path from any research source**
   - All research sources remain `import_scope: research_only | local_only`
   - P37.5 licensed approval is still required for any production path

5. **Kaggle CC BY-NC attribution**
   - If Kaggle full dataset is used, all derivative reports must include:
     `Source: oliviersportsdata (Kaggle), CC BY-NC 4.0, kaggle.com/oliviersportsdata`

---

## 4. Pending Actions for Human Review

| Action Required                                        | Priority | Blocker For              |
|--------------------------------------------------------|----------|--------------------------|
| Navigate AusSportsBetting.com — read ToS + check 2024 coverage | HIGH | Source-04 unlock  |
| Decide whether to purchase Kaggle full dataset (Gumroad) | MEDIUM | Source-03b unlock  |
| Provide manual-import CSV with 2024 MLB odds           | HIGH     | P38A replay joins         |

---

**Acceptance Marker:** RESEARCH_ODDS_LICENSE_RISK_MATRIX_20260513_READY
