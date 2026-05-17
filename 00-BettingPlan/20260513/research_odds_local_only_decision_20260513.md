# Research Odds Local-Only Decision — 2026-05-13

**Status:** DECISION FINALIZED
**Author:** CTO Agent
**Date:** 2026-05-13

---

## 1. Decision Summary

From manual review audit:
- ACCEPTABLE_FOR_LOCAL_RESEARCH: **0**
- ACCEPTABLE_FOR_FIXTURE_ONLY: **1**
- MANUAL_APPROVAL_REQUIRED: **2**
- REJECTED: **0** (within this P1.5 manual-review subset)

Conclusion:
- No candidate is currently approved for real local-only raw odds ingestion.
- Fixture-only smoke is permitted and is the safe path this round.

---

## 2. Allowed Action

**FIXTURE_ONLY_SMOKE_ALLOWED_20260513**

This round permits:
- Synthetic/template fixture validation
- Join logic smoke against fixture semantics

This round does NOT permit:
- Downloading external raw odds into tracked artifacts
- Claiming real-data join readiness

---

## 3. Data Handling Policy

| Item | Policy |
|---|---|
| Raw data download | Deferred unless manual approval is completed |
| Raw data commit | Prohibited |
| Local-only directory | data/research_odds/local_only/ (gitignored) |
| Local-only manifest | Required if real data ever downloaded |
| Fixture data | Allowed only as synthetic/template minimal rows |

---

## 4. Explicit Prohibitions

- Do NOT commit raw dataset.
- Do NOT write to any production ledger.
- Do NOT modify P37.5 formal approval JSON.
- Do NOT treat community research source as licensed production odds replacement.

---

**Decision Marker:** FIXTURE_ONLY_SMOKE_ALLOWED_20260513
