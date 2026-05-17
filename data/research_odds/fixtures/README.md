# data/research_odds/fixtures

Fixture-only datasets for schema and join smoke checks.

## Rules

1. Only synthetic/template data can be stored here.
2. Do not place third-party raw odds exports in this directory.
3. Real downloaded odds must stay in data/research_odds/local_only/ and remain uncommitted.
4. Any fixture used for validation must keep `import_scope=approved_fixture`.
5. No fixture may be used for edge claims or production betting decisions.

## Current Files

- EXAMPLE_TEMPLATE.csv: canonical header template for research odds import contract.

**Marker:** FIXTURE_ONLY_DATA_STRUCTURE_READY_20260513
