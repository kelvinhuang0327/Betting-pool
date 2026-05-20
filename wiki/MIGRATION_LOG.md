# Migration Log (summary of archive/cleanup docs)

Purpose: Consolidate cleanup plans and phase documents into a single migration log and mark originals as ARCHIVE_ONLY.

Summary

- Several project cleanup phases exist under `docs/archive/cleanup/` (phases 1..6). These are preservation artifacts and remain archived.
- Migration approach: snapshot repo, tag `pre-migration`, copy key action items into `wiki/MIGRATION_LOG.md`, then perform per-file dependency inventory before any deletion.

Next steps

1. Create `archive/pre-cleanup-snapshots/` and store a git bundle + tar of critical folders.
2. Author per-file dependency maps for delete-candidates.
3. Execute deletions only after owner sign-off and CI green.

Source

docs/archive/cleanup/*
