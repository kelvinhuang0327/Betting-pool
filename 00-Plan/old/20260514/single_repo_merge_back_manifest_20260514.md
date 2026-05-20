# Single Repo Merge-Back Manifest — 2026-05-14

**Purpose:** CTO merge-back assessment for consolidating all useful `Betting-pool-p13` work into `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` and retiring extra Betting-pool-named folders only after validation.  
**Target canonical repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`  
**Source worktree/branch:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13`, `p13-clean`  
**Latest source commit inspected:** `5775588 docs(betting): finalize P1.5 research odds fixture-only review`  
**Roadmap marker:** `CTO_BETTING_ROADMAP_V6_SINGLE_REPO_CONSOLIDATION_20260514_READY`

---

## 1. Workspace Inventory

| Path | Git/worktree state | Size / files | CTO classification |
|---|---|---:|---|
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | main worktree, `main...origin/main [ahead 38, behind 1]` | ~1.2 GB / 39,348 files | Target canonical. Must triage dirty worktree before merge. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-p13` | git worktree, branch `p13-clean` | ~123 MB / 2,734 files | Source to merge back. Do not delete yet. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-preserve-2026-05-11` | no `.git` | ~225 MB / 644 files | Preservation snapshot. Keep read-only until merge validation. |
| `/Users/kelvin/Kelvin-WorkSpace/Betting-pool-publication` | git worktree, branch `p1/replay-default-validation-publication` | ~4 MB / 272 files | Publication subset. Diff before retirement. |

---

## 2. p13 to main Diff Summary

Command basis: `git diff --name-only main..p13-clean`

| Category | Count | Merge classification |
|---|---:|---|
| `wbc_backend/*.py` code | 117 | Merge candidate |
| `scripts/*.py` | 39 | Merge candidate |
| `tests/*.py` | 153 | Merge candidate |
| `00-BettingPlan/` + `docs/` markdown | 62 | Merge candidate |
| `data/mlb_2024/processed/` artifacts/specs | 47 | Review candidate; most are small processed/spec artifacts, not raw logs |
| `data/research_odds/` fixtures/docs | 3 | Merge candidate; fixture-only, no local raw data |
| Rejected committed diff (`outputs/`, `runtime/`, raw, DB) | 0 | None observed in committed p13 diff |
| Other | 3 | Review candidate |
| **Total changed files** | **424** | — |

Program/test merge scope: **309 files** (`117 + 39 + 153`).

---

## 3. Raw / Forbidden Guard Result

The committed p13 diff does **not** include:

- `outputs/`
- `runtime/`
- `data/mlb_2024/raw/`
- `data/research_odds/local_only/`
- `.db`, `.db-wal`, `.db-shm`, `.sqlite`

CSV files in committed diff are limited to processed/spec/template fixtures, including:

- `data/mlb_2024/processed/*.csv`
- `data/mlb_2024/processed/p33_joined_input_gap/*.csv`
- `data/mlb_2024/processed/p34_dual_source_acquisition/*_template.csv`
- `data/mlb_2024/processed/p37_manual_odds_provisioning/odds_2024_approved_TEMPLATE.csv`
- `data/research_odds/fixtures/EXAMPLE_TEMPLATE.csv`

No raw real odds CSV is currently part of the p13 committed diff.

---

## 4. Target Main Worktree Risk

`/Users/kelvin/Kelvin-WorkSpace/Betting-pool` currently has approximately:

- 742 dirty entries
- 66 modified tracked entries
- 14 deleted tracked entries
- 662 untracked entries

Therefore, the merge-back cannot be a blind `merge` into the current dirty main worktree. The correct next move is a controlled consolidation branch inside the existing repo.

---

## 5. Merge-Back Recommendation

### Recommended path

1. In existing repo only, create a consolidation branch from current `main`.
2. Preserve current dirty state by inventory, not by creating another repo.
3. Apply/cherry-pick p13 commits or equivalent patch series.
4. Exclude raw/local-only/runtime/output/DB paths.
5. Run targeted smoke tests.
6. Produce retirement report for `p13`, `preserve`, and `publication`.

### Do not do

- Do not create another `Betting-pool*` repo.
- Do not delete p13/preserve/publication yet.
- Do not use `git reset --hard`, `git clean`, or destructive checkout against user dirty files.
- Do not push until merge branch and tests are reviewed.

---

## 6. CTO Gate

Current gate: `MERGE_BACK_READY_FOR_DRY_RUN_BRANCH`

Not yet ready for deletion:

- `Betting-pool-p13`: `RETIREMENT_BLOCKED_UNMERGED_SOURCE`
- `Betting-pool-preserve-2026-05-11`: `RETIREMENT_BLOCKED_UNVERIFIED_SNAPSHOT`
- `Betting-pool-publication`: `RETIREMENT_BLOCKED_UNDIFFED_WORKTREE`

**Acceptance marker:** `SINGLE_REPO_MERGE_BACK_MANIFEST_20260514_READY`

