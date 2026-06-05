# P145 Daily Paper Job Enablement Policy

## 1. Phase 0 Actual-State Summary
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- **Branch:** `main`
- **Local HEAD:** `24d2c038a6f8dd86a30f2ddb6bca7538df0301e5`
- **origin/main:** `24d2c038a6f8dd86a30f2ddb6bca7538df0301e5`
- **PR #9:** MERGED
- **Staged files:** 0
- **Untracked files:** 0
- **Dirty tree:** Contains only 9 expanded tolerated daemon/runtime files (e.g. `tsl_dedup_state.json`, `tsl_odds_snapshot.json`).
- **Conclusion:** Phase 0 passed successfully.

## 2. P144 Finding Summary
- P144 successfully integrated `run_paper_recommendation_job` and `run_paper_evaluation_job` into the core daily scheduler (`run_daily_mlb_scheduler`).
- To prevent naive tests or CLI invocations from unintentionally triggering live network fetches (`_pick_game` / `_probe_tsl`), these jobs were explicitly defaulted to `OFF` (`False`).
- Outcome-unavailable states for evaluations properly return `DATA_LIMITED` rather than throwing exceptions, meaning it is safe to run the evaluation step even when results are pending.
- **Blocker B5:** The current paper corpus consists of only 2 rows. We must explicitly enable these jobs in the daemon environment to start accumulating a statistically meaningful dataset on a daily basis.

## 3. Current Scheduler Defaults
- `run_daily_mlb_scheduler()`: Defaults `run_paper_recommendation=False` and `run_paper_evaluation=False`.
- `scripts/run_mlb_daily_scheduler.py`: Currently only exposes `--run-pregame` and `--run-postgame` arguments. It does **not** expose CLI arguments for the two new paper steps, meaning it falls back to the `False` defaults.

## 4. Daemon Startup Invocation
- The scheduler CLI (`scripts/run_mlb_daily_scheduler.py`) is the entry point for scheduling runs.
- Currently, automated executions (via GitHub actions or local cron scripts) run the CLI but cannot pass flags to turn on paper steps because the CLI arguments don't exist yet.

## 5. Proposed Safest Enablement Mechanism
**Step 1:** Modify the CLI entrypoint (`scripts/run_mlb_daily_scheduler.py`) to accept two new arguments:
  - `--run-paper-recommendation` (default: `"false"`)
  - `--run-paper-evaluation` (default: `"false"`)
**Step 2:** Parse these as booleans using the existing `_bool_arg` helper.
**Step 3:** Pass the parsed boolean values to `run_daily_mlb_scheduler(..., run_paper_recommendation=..., run_paper_evaluation=...)`.
**Step 4:** Ensure that the daily daemon runner (e.g. cron script, Airflow, or GitHub Action that executes the daily pipeline) is updated to include `--run-paper-recommendation=true` and `--run-paper-evaluation=true` when executing `run_mlb_daily_scheduler.py`.

## 6. Required Invariants
- **No DB write beyond existing paper-only outputs**: Evaluation metrics and paper recommendations are logged/serialized to the `data/` directory or `report/` artifacts, ensuring no real DB state mutations.
- **No production betting unlock**: All paper paths use `stake=0` or dry-run equivalent by design.
- **No EV/CLV/Kelly unlock**: Real stake sizing remains blocked by the existing paper-only guardrails.
- **No provider unlock**: Provider credentials and production systems are never engaged during the paper recommendation flow.
- **No live API call in tests**: By defaulting the new CLI arguments to `"false"`, existing test suites (`tests/`) invoking the CLI or the scheduler function directly will continue to run fully offline.
- **Paper-only / diagnostic-only semantics preserved**: The `DailyJobManifest` and `gate` logic remain unchanged (driven by pregame + postgame), ensuring systemic stability.

## 7. Offline Test Protection Strategy
- The python function `run_daily_mlb_scheduler` remains defaulted to `False`.
- The CLI arguments `--run-paper-recommendation` and `--run-paper-evaluation` will default to `"false"`.
- This dual-layer defaulting guarantees that any existing or future offline test that does not explicitly set these to `True` will not trigger live network calls.

## 8. Proposed Future Implementation Allowed Files
To implement this policy safely, the following files will need modification in the next task:
- `scripts/run_mlb_daily_scheduler.py` (CLI argument wiring)
- Optionally, any explicitly declared shell scripts / Github Action YAMLs that define the daily daemon execution.

## 9. Proposed Future Test Coverage
- Add a test in `tests/test_mlb_daily_scheduler.py` (or a dedicated CLI test) to verify that the new CLI arguments correctly parse and pass `True` to the underlying orchestrator function when provided, and remain `False` when omitted.

## 10. Rollback Plan
- If live fetches cause instability or unexpected side effects, the daemon runner script can simply remove the `--run-paper-recommendation=true` flag.
- Because the system defaults to `False`, removing the flag from the invoker instantly reverts the orchestrator to its pre-P145 offline/dry-run state.

## 11. Explicit Non-Goals
- We are **not** modifying the core evaluation math or metric generation.
- We are **not** changing the pregame or postgame jobs.
- We are **not** triggering actual live bets.
- We are **not** retroactively fetching historical data beyond the daily schedule.

## 12. Recommended Next Executable Implementation Prompt

```text
[Betting] 精簡版 Agent Task Prompt — P145 Daily Paper Job Enablement Implementation

Canonical Repo:
/Users/kelvin/Kelvin-WorkSpace/Betting-pool

Canonical Branch:
main

Worker是否需要強模型:
NO. This is a straightforward CLI wiring task based on an approved policy.

Task:
Implement the P145 daily paper job enablement policy by adding CLI arguments to `scripts/run_mlb_daily_scheduler.py` and passing them to `run_daily_mlb_scheduler`. Create the branch, implement, test, and commit locally.

Allowed Write Files:
- scripts/run_mlb_daily_scheduler.py
- tests/test_mlb_daily_scheduler.py (to add CLI parsing tests if necessary)

Phase 0 — Actual-State Verification First:
Run and inspect:
- git rev-parse --show-toplevel
- git branch --show-current
- git status --short

Verify:
- repo is /Users/kelvin/Kelvin-WorkSpace/Betting-pool
- branch is main
- no staged files
- dirty tree only contains tolerated daemon/runtime files

Implementation Instructions:
1. Create a new branch: `release/p145-daily-paper-job-enablement`
2. Modify `scripts/run_mlb_daily_scheduler.py` to add `--run-paper-recommendation` and `--run-paper-evaluation` (default `"false"`).
3. Pass these parsed booleans to `run_daily_mlb_scheduler(...)`.
4. Ensure default offline tests still pass without live fetches.
5. Commit the changes locally. Do NOT push.

Required Output:
- Phase 0 verification
- Changed files list
- Test results
- Commit hash and message
- Explicit statement of safety invariants (no live calls in tests, no DB writes)
```
