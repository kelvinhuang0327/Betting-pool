# P37.5 Provider ToS Review Template

**Phase**: P37.5
**Purpose**: Document the review of a potential odds data provider's Terms of Service
**PAPER_ONLY**: `true`
**PRODUCTION_READY**: `false`

---

## Instructions

Complete this template for each provider considered.
Keep a copy of this filled template alongside the `odds_approval_record.json`.
Do NOT commit this template with real provider data to the public git repository.

---

## Provider Information

| Field | Value |
|-------|-------|
| Provider Name | _(fill in)_ |
| Provider Website | _(fill in URL)_ |
| ToS URL | _(fill in URL)_ |
| ToS Last Updated | _(fill in date)_ |
| Date Reviewed | _(fill in ISO date)_ |
| Reviewed By | _(fill in name/role)_ |

---

## Licensing Assessment

### 1. Research Use

| Question | Answer | Evidence (quote from ToS) |
|----------|--------|--------------------------|
| Is internal/personal research explicitly permitted? | YES / NO / UNCLEAR | _(paste relevant clause)_ |
| Is academic use permitted? | YES / NO / UNCLEAR | _(paste relevant clause)_ |
| Is non-commercial use permitted? | YES / NO / UNCLEAR | _(paste relevant clause)_ |

### 2. Commercial Use

| Question | Answer |
|----------|--------|
| Is commercial use explicitly prohibited? | YES / NO |
| Is the intended use non-commercial? | YES / NO |

### 3. Redistribution

| Question | Answer |
|----------|--------|
| Is redistribution of raw data prohibited? | YES / NO |
| Does the research pipeline redistribute raw data? | NO (pipeline is paper-only) |

### 4. Attribution

| Question | Answer |
|----------|--------|
| Is attribution required? | YES / NO |
| What attribution format is required? | _(fill in)_ |

---

## Checklist

- [ ] Full ToS document read (not just summary)
- [ ] No clause prohibits internal research use
- [ ] No clause requires commercial license for research
- [ ] Redistribution is not intended (paper-only)
- [ ] Attribution requirement understood and noted
- [ ] Provider contact information saved (in case of questions)

---

## Recommended Field Values for Approval Record

Based on this review, the following values are appropriate for `odds_approval_record.json`:

```json
{
  "provider_name": "FILL_IN",
  "source_name": "FILL_IN",
  "source_url_or_reference": "FILL_IN",
  "license_terms_summary": "FILL_IN — summarize key permissions and restrictions",
  "allowed_use": "internal_research",
  "redistribution_allowed": false,
  "attribution_required": true,
  "internal_research_allowed": true,
  "commercial_use_allowed": false,
  "approved_by": "FILL_IN",
  "approved_at": "FILL_IN_ISO8601",
  "approval_scope": "mlb_2024_season",
  "source_file_expected_path": "data/mlb_2024/manual_import/odds_2024_approved.csv",
  "checksum_required": true,
  "checksum_sha256": "FILL_IN_AFTER_FILE_READY",
  "paper_only": true,
  "production_ready": false
}
```

---

## Approval Decision

- [ ] **APPROVED** — Provider ToS permits internal research use.  Proceed.
- [ ] **REJECTED** — Provider ToS prohibits research use or requires commercial license.  Choose another provider.
- [ ] **PENDING** — Awaiting clarification from provider legal team.

**Decision rationale**: _(fill in)_

---

## Important Reminders

- `paper_only` MUST be `true` — gate blocks if false
- `production_ready` MUST be `false` — gate blocks if true
- `raw_odds_commit_allowed` is ALWAYS `false` — never stage raw odds
- Do NOT commit filled approval records to git
- Do NOT share real provider credentials or API keys

---

*Template version: P37.5 | PAPER_ONLY=True | PRODUCTION_READY=False | SEASON=2024*
