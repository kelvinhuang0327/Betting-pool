# Active Task: NEXT_TASK_NOT_DEFINED_AFTER_P180_MERGE

## Governance Status

P180 Offline Paper Strategy Attribution and Performance Leaderboard is
**COMPLETE and MERGED**.

- PR #14 is merged.
  URL: https://github.com/kelvinhuang0327/Betting-pool/pull/14
  Merge commit: `d01fa79d64f3afcf240f1fc9fab66b543f53cb49`
- P179 + P180 are on `main`.
- P180 local test validation:
  `python3 -m pytest tests/test_p180_strategy_leaderboard.py tests/test_mlb_paper_evaluator.py tests/test_mlb_paper_evaluation_runner.py -q`
  Result: **56/56 PASS**
- Merge path used: branch-protection PR path (direct push to main was blocked
  by GH006; PR #14 was the correct route).
- No DB writes were performed.
- No live API calls were made.
- No registry mutation occurred.
- No `controlled_apply` was executed.

Prior completed tasks still on `main`:
- PR #13 merged: P172 bot-branch daily workflow persistence.
- P176/P177 are `WAITING` for the first post-P172 scheduled run.
  Do not start more Git polling or Git architecture work unless scheduled
  persistence later fails.

## Current State

No new implementation task is authorized.

Next task state: **NEXT_TASK_NOT_DEFINED_AFTER_P180_MERGE**

Do not begin any new product, strategy, or diagnostic implementation until the
next task is explicitly authorized by the user.

## Standing Governance Rules

These rules remain in effect for all future tasks unless explicitly superseded:

- No DB writes unless explicitly authorized.
- No production/provider/live API access.
- No registry mutation.
- No `controlled_apply`.
- No push unless separately authorized.
- No branch creation or deletion unless explicitly authorized.
- No workflow trigger, workflow rerun, or `workflow_dispatch` unless
  explicitly authorized.
- No GitHub Actions settings or branch-protection changes.
- No strategy weight changes.
- No production champion replacement.
- No EV, CLV, or Kelly unlock.

## Tolerated Runtime Dirty Files

These pre-existing files may be modified by background processes but must not
be staged, committed, restored, cleaned, deleted, moved, or reset by any
authorized task unless separately approved:

- `data/.live_cache/tsl_dedup_state.json`
- `data/derived/tsl_market_availability_state.json`
- `data/mlb_context/external_closing_state.json`
- `data/mlb_context/odds_capture_schedule.json`
- `data/mlb_context/odds_timeline.jsonl`
- `data/tsl_fetch_status.json`
- `data/tsl_odds_history.jsonl`
- `data/tsl_odds_snapshot.json`
- `logs/daemon_heartbeat.jsonl`
- `runtime/agent_orchestrator/training_memory.json`

## STOP Conditions (Persistent)

Stop any future task immediately if:

- The repo is not `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`.
- The current branch is not `main` (or the authorized branch for that task).
- HEAD is detached.
- Any files are staged before implementation begins.
- Any untracked files exist before implementation begins.
- The dirty tree contains files outside the tolerated runtime list.
- Implementation requires live API calls, DB writes, provider access, or
  production betting unlock.
- Implementation requires a workflow trigger, rerun, GitHub settings change,
  or Git architecture change without explicit authorization.
- Implementation requires registry mutation, deployment changes, or
  `controlled_apply` without explicit authorization.
