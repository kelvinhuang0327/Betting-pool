# Research Odds Join Smoke Report — 2026-05-13

**Status:** FIXTURE-ONLY SMOKE
**Author:** CTO Agent
**Date:** 2026-05-13

---

## 1. Execution Mode

- Mode: Fixture-only / template-based smoke
- Real external odds dataset: Not used
- Reason: No ACCEPTABLE_FOR_LOCAL_RESEARCH source passed manual approval in P1.5

---

## 2. Inputs Used

- Contract reference: research_odds_manual_import_contract_20260513.md
- Join plan reference: research_odds_join_certification_plan_20260513.md
- Fixture template: data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv

---

## 3. Smoke Validation Performed

1. Header contract alignment check
- EXAMPLE_TEMPLATE.csv header contains the required canonical columns.

2. Join-key field presence check
- Required join fields are present in template: game_date, home_team, away_team, market.

3. Odds conversion rule sanity check
- Contract-level rule retained: American odds must convert to implied probability in (0,1).
- No real-data rows executed in this report.

4. Duplicate / unmatched report readiness
- Schema and reason codes are defined in join certification plan.
- Execution against real source deferred.

5. Leakage gate check
- Fixture/template path contains no postgame outcome fields by design.

---

## 4. Result Metrics

| Metric | Value |
|---|---:|
| sample_count | 0 |
| matched_count | 0 |
| unmatched_count | 0 |
| duplicate_count | 0 |
| parse_error_count | 0 |
| leakage_violation_count | 0 |

Interpretation:
- This report validates contract and fixture structure only.
- It does not certify real-data join readiness.

---

## 5. Readiness Statement

- JOIN_CERT_RESEARCH_ODDS_READY: **NOT achieved**
- Current achieved status: **FIXTURE_ONLY_JOIN_SMOKE_READY**

Blockers to full join cert:
- Need at least one manual-review candidate promoted to ACCEPTABLE_FOR_LOCAL_RESEARCH
- Need local-only sample (5-20 rows) with verified terms

---

**Acceptance Marker:** FIXTURE_ONLY_JOIN_SMOKE_READY
