# data/research_odds/

Research-grade odds data storage. Governed by:
- `00-BettingPlan/20260513/research_odds_manual_import_contract_20260513.md`
- `00-BettingPlan/20260513/research_odds_license_risk_matrix_20260513.md`

## Directory Policy

| Subdirectory | Policy                                | Git Status         |
|--------------|---------------------------------------|--------------------|
| `local_only/` | Real odds data — NEVER commit       | .gitignore'd       |
| `fixtures/`   | Synthetic / CI fixture data only    | Can be committed   |

## Non-Negotiable Rules

1. Raw odds CSV files from third-party sources → `local_only/` ONLY
2. `local_only/` must remain in .gitignore at all times
3. Before placing any file in `local_only/`, verify license status is NOT UNKNOWN
4. Use synthetic fixtures in `fixtures/` for deterministic tests only
5. Never treat research odds as production odds

## Notes

- For this cycle, download remains deferred. See
	`00-BettingPlan/20260513/research_odds_dataset_download_deferred_20260513.md`.
- Future import tooling should validate against
	`00-BettingPlan/20260513/research_odds_manual_import_contract_20260513.md`.
