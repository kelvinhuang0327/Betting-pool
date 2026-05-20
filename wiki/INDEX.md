# Betting-pool LLM-Wiki

## Purpose

This `wiki/` directory is the canonical knowledge layer for the repository.
It exists to remove ambiguity between active runtime code, historical documents, and generated artifacts.

This wiki does not replace code as the execution truth.
It provides the human-readable and agent-readable interpretation of what is currently authoritative.

## Single Source Of Truth

- Runtime behavior: source code and tests remain the executable truth.
- Operational guidance: this `wiki/` directory is the single source of truth for entrypoints, architecture boundaries, and cleanup rules.
- Historical context: `docs/` and `docs/archive/` remain the historical record.
- Generated outputs: `data/`, `report/`, `research/postmortem_reports/`, and `logs/` remain outside the wiki.

## Scope

This initial wiki layer is intentionally minimal.
It defines:

- authoritative entrypoints
- current architecture boundaries
- cleanup safety rules
- safe cleanup preparation

## Current Pages

- `ENTRYPOINTS.md` — canonical runners and usage scenarios
- `ARCHITECTURE.md` — root layer vs `wbc_backend` boundaries and current duplication
- `CLEANUP_POLICY.md` — artifact vs knowledge rules and deletion safety gates
- `CLEANUP_PLAN.md` — current file classification, duplication map, and backup strategy