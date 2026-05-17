# Research Odds Manual Review Audit — 2026-05-13

**Status:** LICENSE / TERMS MANUAL AUDIT COMPLETE
**Author:** CTO Agent
**Date:** 2026-05-13
**Scope:** MANUAL_REVIEW_REQUIRED candidates from P1 inventory and risk matrix
**Acceptance Marker:** RESEARCH_ODDS_MANUAL_REVIEW_AUDIT_20260513_READY

---

## 1. Audit Scope

Manual-review targets from P1 artifacts:
- Kaggle US Sports Master (sample + full dataset path)
- AusSportsBetting MLB historical odds page

Primary references:
- Kaggle dataset page (license + coverage + sample constraints)
- CC BY-NC 4.0 legal deed
- AusSportsBetting data and terms pages (HTTP 403 during automated fetch)

---

## 2. Candidate-by-Candidate Audit

### Candidate MR-01 — Kaggle US Sports Master (Sample on Kaggle)

| Field | Value |
|---|---|
| candidate_name | Kaggle US Sports Master Closing Odds (Kaggle sample package) |
| source_url | https://www.kaggle.com/datasets/oliviersportsdata/us-sports-master-historical-closing-odds |
| source_type | Kaggle dataset sample |
| prior_classification | MANUAL_REVIEW_REQUIRED |
| license_or_terms_location | Kaggle dataset license section + https://creativecommons.org/licenses/by-nc/4.0/ |
| license_summary | CC BY-NC 4.0 permits sharing/adaptation for non-commercial use with attribution |
| download_allowed | YES (Kaggle sample files downloadable) |
| research_use_allowed | YES (non-commercial research allowed under CC BY-NC 4.0) |
| redistribution_allowed | YES (non-commercial, attribution required) |
| raw_data_commit_allowed | NO (policy gate: keep raw external data out of git by default) |
| derivative_report_allowed | YES (with attribution, non-commercial) |
| attribution_required | YES |
| local_only_required | YES (for any non-fixture rows from external source) |
| scraping_or_automation_restriction | Kaggle access controls apply; avoid custom scraping; use official download path |
| 2024_coverage_confirmed | NO (sample MLB file is 50 rows from 2006 season) |
| closing_line_confirmed | YES (dataset is closing odds oriented) |
| team_date_mapping_viability | PARTIAL (needs full schema inspection for robust mapping) |
| final_classification | ACCEPTABLE_FOR_FIXTURE_ONLY |

Rationale:
- License is clear for non-commercial research with attribution.
- But Kaggle-hosted sample has no 2024 MLB coverage and is structurally limited.
- Usable only for fixture/schema smoke, not replay-grade join certification.

---

### Candidate MR-02 — Kaggle US Sports Master (Full paid dataset via Gumroad)

| Field | Value |
|---|---|
| candidate_name | US Sports Master Full Dataset (paid path) |
| source_url | https://sportsdataolivier.gumroad.com/l/ahlplc |
| source_type | Paid external dataset (Gumroad delivery) |
| prior_classification | MANUAL_REVIEW_REQUIRED |
| license_or_terms_location | Kaggle license statement + CC BY-NC 4.0 deed |
| license_summary | CC BY-NC 4.0, non-commercial permitted with attribution |
| download_allowed | YES (after purchase) |
| research_use_allowed | YES (non-commercial only) |
| redistribution_allowed | YES under CC BY-NC terms, but repo policy still forbids committing raw source |
| raw_data_commit_allowed | NO (repo governance default: local-only for external raw odds) |
| derivative_report_allowed | YES (with attribution, non-commercial) |
| attribution_required | YES |
| local_only_required | YES |
| scraping_or_automation_restriction | No scraping required; use official vendor delivery |
| 2024_coverage_confirmed | YES (MLB listed 2006–2025 on source page) |
| closing_line_confirmed | YES |
| team_date_mapping_viability | MEDIUM (likely viable, still needs schema-level mapping check post-purchase) |
| final_classification | MANUAL_APPROVAL_REQUIRED |

Rationale:
- License is reasonably clear for non-commercial research.
- Gating factor is procurement + post-download schema confirmation.
- Until user approves purchase and local validation, cannot move to JOIN_CERT readiness.

---

### Candidate MR-03 — AusSportsBetting Historical MLB Odds

| Field | Value |
|---|---|
| candidate_name | AusSportsBetting MLB historical results and odds |
| source_url | https://www.aussportsbetting.com/data/historical-mlb-results-and-odds-data/ |
| source_type | Community historical odds website |
| prior_classification | MANUAL_REVIEW_REQUIRED |
| license_or_terms_location | https://www.aussportsbetting.com/terms-and-conditions/ |
| license_summary | UNVERIFIED (automated fetch blocked with HTTP 403) |
| download_allowed | UNKNOWN |
| research_use_allowed | UNKNOWN |
| redistribution_allowed | UNKNOWN |
| raw_data_commit_allowed | NO (blocked until terms explicitly verified) |
| derivative_report_allowed | UNKNOWN |
| attribution_required | UNKNOWN |
| local_only_required | YES if ever approved |
| scraping_or_automation_restriction | UNKNOWN; assume restricted until explicit confirmation |
| 2024_coverage_confirmed | UNKNOWN |
| closing_line_confirmed | UNKNOWN |
| team_date_mapping_viability | UNKNOWN |
| final_classification | MANUAL_APPROVAL_REQUIRED |

Rationale:
- Terms/location accessible by URL but not retrievable via automated fetch in current session.
- Under governance rule, unclear terms => MANUAL_APPROVAL_REQUIRED.

---

## 3. Audit Totals

| Classification | Count |
|---|---:|
| ACCEPTABLE_FOR_LOCAL_RESEARCH | 0 |
| ACCEPTABLE_FOR_FIXTURE_ONLY | 1 |
| MANUAL_APPROVAL_REQUIRED | 2 |
| REJECTED_FOR_LICENSE_RISK | 0 |
| REJECTED_FOR_INCOMPLETE_FIELDS | 0 |
| REJECTED_FOR_NO_2024_COVERAGE | 0 |
| REJECTED_FOR_NO_CLOSING_LINE | 0 |

---

## 4. Hard Gates Confirmed

- If license/terms unclear => MANUAL_APPROVAL_REQUIRED (applied to AusSportsBetting).
- If redistribution unclear/restricted => never commit raw dataset.
- If no 2024 real-data coverage in accessible sample => fixture-only at best.
- No gate was lowered to satisfy schedule pressure.

---

**Acceptance Marker:** RESEARCH_ODDS_MANUAL_REVIEW_AUDIT_20260513_READY
