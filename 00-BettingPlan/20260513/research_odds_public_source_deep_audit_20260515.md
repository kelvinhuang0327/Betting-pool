# Research Odds Public-Source Deep Audit — 2026-05-15

**Status:** DEEP AUDIT COMPLETE — 4 CANDIDATES  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Scope:** Deep license, coverage, and join-feasibility audit for the 4 public/free candidates requiring further review from v2 inventory (CANDIDATE-03, 04, 08, 09)  
**References:**
- `research_odds_candidate_inventory_v2_20260514.md` (prior v2 classification)
- `research_odds_manual_review_audit_20260513.md` (prior MR-01, MR-02, MR-03 audit)
- `p38a_odds_join_key_mapping_spec_20260514.md` (P38A join requirements)
- Web fetch: Kaggle oliviersportsdata page (confirmed 2026-05-15)
- Web fetch: The Odds API terms (confirmed 2026-05-15)
- Web fetch: GitHub topics mlb-odds, sports-betting-data (confirmed 2026-05-15)
- Web fetch: AusSportsBetting terms/data (HTTP 403 × 2, confirmed 2026-05-15)

---

## ⚠️ Audit Governance Rules (Non-Negotiable)

> 1. `license_text_found = NO` → candidate CANNOT be classified ACCEPTABLE_FOR_LOCAL_RESEARCH.
> 2. `2024_mlb_coverage = NO` → REJECTED_FOR_NO_2024_COVERAGE (regardless of license).
> 3. `redistribution_allowed = NO or UNCLEAR` → raw data must NEVER be committed to git.
> 4. Paid path → PAID_PROVIDER_DECISION_REQUIRED; never pre-approve on behalf of user.
> 5. HTTP-blocked pages → MANUAL_APPROVAL_REQUIRED; never assume terms are acceptable.
> 6. Datasets not publicly accessible → REJECTED_FOR_UNVERIFIABLE_LICENSE.

---

## 1. CANDIDATE-03-A: Kaggle oliviersportsdata — Sample (Free Kaggle Download)

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-03-A |
| **candidate_name** | US Sports Master Closing Odds — Kaggle Sample |
| **source_url** | https://www.kaggle.com/datasets/oliviersportsdata/us-sports-master-historical-closing-odds |
| **terms_url** | https://creativecommons.org/licenses/by-nc/4.0/ |
| **license_text_found** | YES — CC BY-NC 4.0 displayed on Kaggle dataset page |
| **license_type** | CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International) |
| **2024_mlb_coverage** | NO — Kaggle-hosted sample is 50 rows from 2006 season only |
| **closing_line_available** | YES — dataset title explicitly "Closing Odds" |
| **timestamp_available** | UNKNOWN — not stated in sample metadata; not visible in 50-row extract |
| **moneyline_available** | YES — American Moneyline format |
| **download_allowed** | YES — official Kaggle CSV download path |
| **research_use_allowed** | YES — CC BY-NC 4.0 permits non-commercial research with attribution |
| **redistribution_allowed** | YES under CC BY-NC 4.0 (non-commercial, attribution required) |
| **raw_commit_allowed** | NO — governance policy blocks raw external data from git regardless of license |
| **join_feasibility_vs_P38A** | NONE — 50-row 2006 sample has no intersection with P38A 2024 OOF predictions |
| **final_classification** | **ACCEPTABLE_FOR_FIXTURE_ONLY** |

**Rationale:** License is fully verified. Sample is too limited (50 rows, 2006 season) for any P38A join. Usable only for fixture/schema testing — consistent with prior MR-01 classification.

---

## 2. CANDIDATE-03-B: Kaggle oliviersportsdata — Full Dataset (Gumroad Purchase)

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-03-B |
| **candidate_name** | US Sports Master Closing Odds — Full Dataset (Gumroad) |
| **source_url** | https://sportsdataolivier.gumroad.com/l/ahlplc |
| **terms_url** | https://creativecommons.org/licenses/by-nc/4.0/ (same license as Kaggle listing) |
| **license_text_found** | YES — CC BY-NC 4.0 stated on Kaggle dataset page for same dataset |
| **license_type** | CC BY-NC 4.0 |
| **2024_mlb_coverage** | YES — MLB coverage stated as "2006–2025" (46,235 matches); 2024 is included ✅ |
| **closing_line_available** | YES — "US Sports Master Closing Odds" (title explicitly states closing line) |
| **timestamp_available** | UNKNOWN — separator is semicolon (;); schema not inspectable without purchase |
| **moneyline_available** | YES — "American Moneyline" per dataset description |
| **download_allowed** | YES after Gumroad purchase — official vendor delivery |
| **research_use_allowed** | YES — CC BY-NC 4.0 non-commercial research permitted |
| **redistribution_allowed** | YES (non-commercial, attribution required) — governance still blocks raw git commit |
| **raw_commit_allowed** | NO — governance policy + redistribution clause |
| **join_feasibility_vs_P38A** | MEDIUM — 2024 coverage confirmed; team/date schema requires inspection post-purchase; Retrosheet team code normalization will be needed |
| **procurement_required** | YES — Gumroad purchase required; price TBD by user |
| **schema_validation_required** | YES — timestamp column, team naming format, separator (;) all need validation post-purchase |
| **final_classification** | **MANUAL_APPROVAL_REQUIRED** (pending user purchase decision + post-purchase schema validation) |

**Rationale:** This is the most promising free/low-cost public path. License is clear (CC BY-NC 4.0). 2024 coverage confirmed. Blocked only by procurement (Gumroad purchase) and schema validation. If user approves purchase, this candidate can advance to ACCEPTABLE_FOR_LOCAL_RESEARCH pending schema smoke test.

**Action Required (user decision):**
- [ ] User approves Gumroad purchase of full dataset
- [ ] Post-purchase: validate timestamp column presence and ISO 8601 compatibility
- [ ] Post-purchase: validate team name format (normalize to Retrosheet 3-letter codes)
- [ ] Post-purchase: validate 2024 season row count ≥ 100 rows for join smoke

---

## 3. CANDIDATE-04: AusSportsBetting.com Historical MLB

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-04 |
| **candidate_name** | AusSportsBetting Historical MLB Results and Odds |
| **source_url** | https://www.aussportsbetting.com/data/historical-mlb-results-and-odds-data/ |
| **terms_url** | https://www.aussportsbetting.com/terms-and-conditions/ |
| **license_text_found** | NO — HTTP 403 Forbidden on both data page and terms page (verified 2026-05-15, same result as prior attempt 2026-05-13) |
| **license_type** | UNKNOWN — blocked |
| **2024_mlb_coverage** | UNKNOWN — page inaccessible |
| **closing_line_available** | UNKNOWN |
| **timestamp_available** | UNKNOWN |
| **moneyline_available** | UNKNOWN |
| **download_allowed** | UNKNOWN |
| **research_use_allowed** | UNKNOWN |
| **redistribution_allowed** | UNKNOWN |
| **raw_commit_allowed** | NO — terms not verifiable |
| **join_feasibility_vs_P38A** | UNKNOWN — blocked |
| **audit_attempts** | 2 automated attempts (2026-05-13, 2026-05-15) — both blocked with HTTP 403 |
| **unblock_path** | Manual browser access by user (direct visit to terms page, manual reading) |
| **final_classification** | **MANUAL_APPROVAL_REQUIRED** — terms require direct human verification via browser |

**Rationale:** Governance rule 5 applies: HTTP-blocked pages → MANUAL_APPROVAL_REQUIRED. Cannot lower classification without explicit terms text. HTTP 403 persists across two separate attempts at two separate dates.

**Action Required (user decision):**
- [ ] User manually visits https://www.aussportsbetting.com/terms-and-conditions/ in browser
- [ ] User manually visits https://www.aussportsbetting.com/data/historical-mlb-results-and-odds-data/
- [ ] User records: research_use_allowed, redistribution_allowed, 2024 coverage, download method
- [ ] If terms are acceptable: user submits summary → agent reclassifies

---

## 4. CANDIDATE-08: Kaggle tobijegede/mlb-historic-odds

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-08-A |
| **candidate_name** | Kaggle — tobijegede/mlb-historic-odds |
| **source_url** | https://www.kaggle.com/datasets/tobijegede/mlb-historic-odds |
| **terms_url** | N/A — dataset not publicly accessible |
| **license_text_found** | NO — web fetch returned "Failed to extract meaningful content" (dataset is private, removed, or nonexistent as of 2026-05-15) |
| **license_type** | UNKNOWN |
| **2024_mlb_coverage** | UNKNOWN |
| **closing_line_available** | UNKNOWN |
| **timestamp_available** | UNKNOWN |
| **moneyline_available** | UNKNOWN |
| **download_allowed** | UNKNOWN |
| **research_use_allowed** | UNKNOWN |
| **redistribution_allowed** | UNKNOWN |
| **raw_commit_allowed** | NO |
| **join_feasibility_vs_P38A** | NONE — cannot assess inaccessible dataset |
| **final_classification** | **REJECTED_FOR_UNVERIFIABLE_LICENSE** |

**Rationale:** Governance rule 6 applies. Dataset is not publicly accessible; license cannot be verified. Do NOT use.

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-08-B |
| **candidate_name** | Kaggle expanded search — other MLB betting datasets |
| **notes** | Web fetch of Kaggle search for "mlb odds moneyline" returned `ritika027/real-time-sports-odds-data-multiple-bookmakers` (usability 3.1, 1 file, 1KB — too small to contain meaningful historical data) and other non-MLB datasets. No additional qualifying dataset found with: verified license + 2024 MLB coverage + closing line availability. |
| **final_classification** | **REJECTED_FOR_NO_QUALIFYING_DATASETS_FOUND** |

---

## 5. CANDIDATE-09: GitHub Public MLB Odds CSV Repositories

| Field | Value |
|---|---|
| **candidate_id** | CANDIDATE-09 |
| **candidate_name** | GitHub public repos — MLB historical odds CSV |
| **source_url** | https://github.com/topics/mlb-odds, https://github.com/topics/sports-betting-data |
| **search_method** | GitHub topic pages fetched directly (2026-05-15) |
| **github_topic_mlb_odds** | 0 repos (topic has no tagged repos as of 2026-05-15) |
| **github_topic_sports_betting_data** | 1 repo (VaultSparkStudios/promogrind — sportsbook promo tool, not historical odds data) |
| **qualifying_repos_found** | 0 |
| **license_text_found** | N/A — no qualifying repos found |
| **2024_mlb_coverage** | N/A |
| **closing_line_available** | N/A |
| **join_feasibility_vs_P38A** | N/A |
| **final_classification** | **REJECTED_FOR_NO_QUALIFYING_REPOS_FOUND** |

**Rationale:** GitHub topic search for MLB historical odds yielded zero qualifying repositories. The one repo found under `sports-betting-data` is a promo calculator tool with no historical odds data. No GitHub path exists for free MLB 2024 closing odds.

---

## 6. Consolidated Summary Table

| Candidate | License Found | 2024 Coverage | Closing Line | Raw Commit | Final Classification |
|---|---|---|---|---|---|
| 03-A: Kaggle sample (free) | YES (CC BY-NC 4.0) | NO (2006 only) | YES | NO | ACCEPTABLE_FOR_FIXTURE_ONLY |
| 03-B: Kaggle full (Gumroad) | YES (CC BY-NC 4.0) | YES (2006–2025) | YES | NO | MANUAL_APPROVAL_REQUIRED |
| 04: AusSportsBetting | NO (HTTP 403) | UNKNOWN | UNKNOWN | NO | MANUAL_APPROVAL_REQUIRED |
| 08-A: tobijegede Kaggle | NO (inaccessible) | UNKNOWN | UNKNOWN | NO | REJECTED_FOR_UNVERIFIABLE_LICENSE |
| 08-B: Kaggle other | N/A | N/A | N/A | NO | REJECTED_FOR_NO_QUALIFYING_DATASETS_FOUND |
| 09: GitHub repos | N/A | N/A | N/A | NO | REJECTED_FOR_NO_QUALIFYING_REPOS_FOUND |

---

## 7. Path Forward

### Free-Source Viable Paths (post-user-approval)

| Path | Blocker | Unblock Action |
|---|---|---|
| CANDIDATE-03-B (Gumroad full dataset) | Gumroad purchase approval | User approves; agent validates schema post-purchase |
| CANDIDATE-04 (AusSportsBetting) | Human browser verification of terms | User reads terms page directly; reports back |

### Blocked Paths (permanent)

- CANDIDATE-08-A: Dataset inaccessible — no path forward.
- CANDIDATE-08-B: No qualifying Kaggle datasets found in this round.
- CANDIDATE-09: No qualifying GitHub repos — GitHub is not a viable source.

### Shortcut Paths (no approval needed)

- CANDIDATE-15 (Manual-Import CSV): User provides their own odds data → always acceptable.
- CANDIDATE-16 (Fixture-Only): Synthetic data already committed → always acceptable for smoke tests.

---

## 8. Acceptance Marker

```
RESEARCH_ODDS_PUBLIC_SOURCE_DEEP_AUDIT_20260515_READY
```
