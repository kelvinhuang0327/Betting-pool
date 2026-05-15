# P3.1 Research Odds Source Decision — 2026-05-15

**Status:** SOURCE DECISION: PAID_PROVIDER_DECISION_REQUIRED  
**Author:** CTO Agent  
**Date:** 2026-05-15  
**Classification:** PAID_PROVIDER_DECISION_REQUIRED  
**References:**
- `research_odds_public_source_deep_audit_20260515.md` (TRACK 1 audit — all 4 public free candidates)
- `research_odds_paid_provider_decision_matrix_20260515.md` (TRACK 2 — 3 paid providers)
- `research_odds_candidate_inventory_v2_20260514.md` (full candidate landscape)

---

## 1. Decision Basis

### 1.1 Public Free Source Results (TRACK 1 Summary)

| Candidate | 2024 Coverage | License | Final Status | Can Use Now? |
|---|---|---|---|---|
| CANDIDATE-03-A (Kaggle sample) | NO | CC BY-NC 4.0 | ACCEPTABLE_FOR_FIXTURE_ONLY | NO (no 2024 data) |
| CANDIDATE-03-B (Gumroad full) | YES | CC BY-NC 4.0 | MANUAL_APPROVAL_REQUIRED | NO (needs purchase) |
| CANDIDATE-04 (AusSportsBetting) | UNKNOWN | UNVERIFIABLE | MANUAL_APPROVAL_REQUIRED | NO (terms blocked) |
| CANDIDATE-08-A (tobijegede) | UNKNOWN | UNVERIFIABLE | REJECTED | NO (inaccessible) |
| CANDIDATE-08-B (other Kaggle) | N/A | N/A | REJECTED | NO (none found) |
| CANDIDATE-09 (GitHub repos) | N/A | N/A | REJECTED | NO (none found) |

**No public free source is currently cleared for P38A join use with 2024 data.**

### 1.2 Paid Provider Results (TRACK 2 Summary)

| Provider | Coverage | Pricing | Research Use | Recommended? |
|---|---|---|---|---|
| The Odds API (PROVIDER-A) | ✅ YES (2020–present) | $30/month (20K plan) | ✅ YES | ✅ YES — Primary |
| SportsDataIO (PROVIDER-B) | ✅ YES | Enterprise (unknown) | ⚠️ UNCERTAIN | ⚠️ Secondary |
| Sportradar (PROVIDER-C) | ✅ YES | ~$1,000+/month | ❌ UNLIKELY | ❌ NO |

---

## 2. Decision Matrix — Full 4-Way

| Decision | Condition | Next Action | Track 4 Outcome |
|---|---|---|---|
| **REAL_LOCAL_ONLY_SOURCE_ALLOWED (Paid — Odds API)** | User approves $30/month The Odds API subscription | Agent creates download plan + implementation script | `p31_local_only_download_plan_20260515.md` |
| **REAL_LOCAL_ONLY_SOURCE_ALLOWED (Public — Gumroad)** | User purchases CANDIDATE-03-B from Gumroad | User downloads; agent validates schema + runs join | `p31_local_only_download_plan_20260515.md` |
| **REAL_LOCAL_ONLY_SOURCE_ALLOWED (Public — AusSportsBetting)** | User manually verifies terms and reports acceptable | Agent runs download + join on data user provides | `p31_local_only_download_plan_20260515.md` |
| **PAID_PROVIDER_DECISION_REQUIRED / NO_DOWNLOAD_BLOCKER** | No source approved by user | Document blocker; mark join smoke as PENDING_SOURCE | `p31_no_download_blocker_20260515.md` |

---

## 3. Agent's Source Decision (No User Input Present)

**Based on current session context — no user approval of any paid source has been received.**

**CURRENT CLASSIFICATION: `PAID_PROVIDER_DECISION_REQUIRED`**

**Rationale:**
1. All 4 public free candidates are blocked (either REJECTED or MANUAL_APPROVAL_REQUIRED).
2. No existing local-only odds data is present in `data/research_odds/local_only/` (gitignored directory is empty).
3. No user signal received in this session approving any paid subscription or purchase.
4. Agent cannot initiate any API subscription, Gumroad purchase, or external API call without explicit user approval.
5. The Odds API is the shortest, lowest-risk path to ≥100 rows of 2024 MLB closing odds — but it requires user to subscribe.

---

## 4. Recommended Source (If User Approves)

**RECOMMENDED: The Odds API — 20K plan ($30/month)**

| Criterion | Score | Notes |
|---|---|---|
| Pricing transparency | 5/5 | Public pricing page |
| Research use clarity | 5/5 | Terms explicitly permit analytical use |
| 2024 coverage | 5/5 | From June 6, 2020 → full 2024 season |
| Closing line availability | 5/5 | Historical endpoint with snapshot approach |
| Integration complexity | 4/5 | REST + JSON → 1–2 day implementation |
| Team normalization effort | 3/5 | Full team names → Retrosheet codes required |
| Time to ≥100 rows | 5/5 | Same day post-subscription (5 API calls) |
| **Total** | **32/35** | **Clear leader** |

---

## 5. Pending User Decision Required

### User Action Items (in priority order)

```
ACTION-1 [Recommended]:
  Subscribe to The Odds API 20K plan at https://the-odds-api.com/#get-access
  Cost: $30/month
  → Agent will immediately create download plan + implementation script.

ACTION-2 [Alternative]:
  Purchase CANDIDATE-03-B (Kaggle oliviersportsdata full dataset) via Gumroad.
  → Agent will validate schema; if timestamp + team format pass, advance to join smoke.

ACTION-3 [Alternative]:
  Manually visit https://www.aussportsbetting.com/terms-and-conditions/ in browser.
  Report back: is commercial data use allowed? Is redistribution allowed?
  → Agent will re-classify CANDIDATE-04 based on user's report.

ACTION-4 [No-cost alternative]:
  Provide your own odds data file manually (any source you already have access to).
  Drop CSV in: data/research_odds/local_only/
  → Agent will immediately validate schema + run ≥100 rows join smoke.
```

### Expected Next Track Given No User Input

**→ TRACK 4: `p31_no_download_blocker_20260515.md`** (no source approved = download blocked)  
**→ TRACK 5: `REAL_JOIN_SMOKE_NOT_EXECUTED_DATA_NOT_PRESENT`**

---

## 6. Acceptance Marker

```
P31_RESEARCH_ODDS_SOURCE_DECISION_20260515_READY
```

**Decision Classification:** `PAID_PROVIDER_DECISION_REQUIRED`
