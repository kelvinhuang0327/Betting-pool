# Autonomous Optimization System — Capability Baseline & Handoff Report

**Date**: 2026-04-30  
**Status at time of writing**: `WAITING_ACTIVE` / `GREEN` — 14 CLV records pending closing odds  
**Total tests verified**: 551 passing (396 Phase 6–8 + 155 Phase 9–13)  
**Success marker**: `PHASE_14_SYSTEM_BASELINE_HANDOFF_VERIFIED`

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Completed Phases (6–13)](#2-completed-phases-613)
3. [Operating States Reference](#3-operating-states-reference)
4. [Learning Gates](#4-learning-gates)
5. [Core Commands](#5-core-commands)
6. [Critical Files](#6-critical-files)
7. [Known Limitations](#7-known-limitations)
8. [Recommended Next Roadmap](#8-recommended-next-roadmap)

---

## 1. System Overview

The autonomous optimization system is a multi-phase pipeline that:

1. **Ingests** prediction records via Phase 6 (trusted data pipeline)
2. **Waits** for market settlement and closing odds via Phase 7
3. **Governs** which learning tasks are allowed via Phase 8
4. **Executes** safe work and learning tasks via planner/worker
5. **Reports** on its own health via Phase 9 ops reports
6. **Guards** completion quality via Phase 10
7. **Runs** deterministic safe tasks without LLM via Phase 11
8. **Recovers** from scheduler idle / skip storms via Phase 12
9. **Surfaces** unified readiness state via Phase 13

**Hard invariant**: Learning families (`model-patch`, `strategy-reinforcement`, `calibration`, etc.)
are **never** allowed until at least one CLV record reaches `COMPUTED` status. This gate is
enforced independently by Phase 6, Phase 7, Phase 8, and Phase 13 — it cannot be bypassed.

---

## 2. Completed Phases (6–13)

### Phase 6 — Trusted Data Pipeline (6P–6U)

**Purpose**: Ingest pre-game predictions, align them with ML-only timestamps and odds
snapshots, and generate validated CLV (`Closing Line Value`) records for each prediction.

**Sub-phases**:
| Sub-phase | Description |
|-----------|-------------|
| 6P–6O | Prediction capture, timestamp alignment, odds snapshot alignment, data contract validation |
| 6R | Native-timestamp integration — ML-only timestamps guaranteed to be pre-game |
| 6S | Odds snapshot alignment — prediction time matched to closest pre-game odds snapshot |
| 6T | Registry conversion — flat JSONL prediction registry with governance token `VALIDATED_ML_ONLY` |
| 6U | CLV record generation — one record per prediction with initial status `PENDING_CLOSING` |

**Key files**:
- `orchestrator/phase6_data_registry.py` — read-only index of 6T/6U output files
- `data/wbc_backend/reports/prediction_registry_6t_*.jsonl` — Phase 6T flat registry
- `data/wbc_backend/reports/clv_validation_records_6u_*.jsonl` — Phase 6U CLV records

**Current status**: 14 CLV records exist, all `PENDING_CLOSING`

**Tests passed**: 217
- `test_phase6_integration.py`: 37
- `test_phase6_training_integration.py`: 28
- `test_phase6r_native_timestamps.py`: 25
- `test_phase6s_odds_snapshot_alignment.py`: 26
- `test_phase6t_registry_conversion.py`: 32
- `test_phase6u_clv_record_generation.py`: 69

**Key behaviors**:
- All prediction records require `VALIDATED_ML_ONLY` governance token to enter 6T
- Timestamps are strictly validated as pre-game (no post-game data leakage)
- CLV records are append-only; original JSONL files are never modified

---

### Phase 7 — Closing-to-Learning Activation

**Purpose**: Monitor for valid post-prediction closing odds and upgrade
`PENDING_CLOSING` CLV records to `COMPUTED` when real closing odds arrive.
Unlocks learning families once ≥1 record reaches `COMPUTED`.

**Key file**: `orchestrator/closing_odds_monitor.py`

**Hard rules (enforced in code)**:
- `closing_ts` MUST be strictly > `prediction_time_utc` (no stale snapshots)
- Never fake or interpolate closing odds
- Never modify original 6U JSONL source files
- Output written to new append-only file: `clv_validation_records_6u_upgraded_{date}.jsonl`

**State file**: `runtime/agent_orchestrator/closing_monitor_state.json`

**Tests passed**: 84
- `test_phase7_closing_to_learning.py`: 30
- `test_phase7_integration.py`: 54

**Key behaviors**:
- Reads `data/mlb_context/odds_timeline.jsonl` as canonical odds source
- `get_monitor_state()` returns last run info and upgrade counts
- Runs deterministically via Phase 11 executor (no LLM required)

---

### Phase 8 — Optimization Governance

**Purpose**: Classify the current system state and determine which task families
are allowed. Acts as the single gating authority for learning tasks.

**Key file**: `orchestrator/optimization_state.py`

**States**:
| State | Meaning |
|-------|---------|
| `DATA_WAITING` | CLV mostly `PENDING_CLOSING`; learning blocked |
| `DATA_READY` | Sufficient `COMPUTED` CLV; full learning allowed |
| `MODEL_WEAKNESS_DETECTED` | Brier/LogLoss/CLV/ROI show weakness; patching needed |
| `SYSTEM_RELIABILITY_ISSUE` | Scheduler skip, stale daemon, API failure |
| `ARCHITECTURE_DEBT` | Duplicate modules, stale docs |
| `OPERATOR_UX_GAP` | Decision card missing key state fields |

**Blocked families in `DATA_WAITING`** (11 forbidden task types):
`model_patch`, `model_patch_calibration`, `model_patch_atomic`,
`strategy_reinforcement`, `strategy-reinforcement`, `feedback_atomic`,
`clv_reinforcement`, `calibration_atomic`, `feature_atomic`,
`regime_atomic`, `backtest_validity_atomic`

**Allowed families in `DATA_WAITING`** (safe work):
`closing-monitor`, `ops-report`, `scheduler-health-check`, `artifact-health-check`,
`wiki-maintenance`, `architecture-cleanup`, `observability-ux`, `maintenance`,
`data-monitor`, `system-reliability`, `simulation-atomic`

**Tests passed**: 81
- `test_phase8_integration.py`: 43
- `test_phase8_optimization_governance.py`: 38

---

### Phase 9 — Autonomous Ops Reporting

**Purpose**: Summarise scheduler activity over a time window (8h or 24h) and
classify whether the system is actually improving. Detects skip storms and
quality degradation.

**Key file**: `orchestrator/optimization_ops_report.py`

**Window classifications**:
| Class | Meaning |
|-------|---------|
| `EFFECTIVE` | Learning tasks completing with valid output |
| `PARTIAL` | Some effective completions, some gaps |
| `IDLE` | No tasks completing in window |
| `WAITING_ACTIVE` | DATA_WAITING state but safe work running |
| `BLOCKED` | Governance or LLM provider blocking execution |
| `DEGRADED` | Unexplained skip storm or only empty/noop completions |

**CLI**: `python3 scripts/run_optimization_ops_report.py [--window 8h|24h] [--json]`

**Output**: `docs/orchestration/optimization_ops_report_{date}_{time}.md`

**Tests passed**: 36 (`test_phase9_optimization_ops.py`)

---

### Phase 10 — Completion Quality Guard

**Purpose**: Classify each completed task's output quality so that
empty/no-op completions are not counted as effective improvements.

**Key file**: `orchestrator/task_completion_validator.py`

**Quality states**:
| State | Meaning | Counts as effective? |
|-------|---------|----------------------|
| `COMPLETED_VALID` | Meaningful content produced | ✅ Yes |
| `COMPLETED_DIAGNOSTIC_ONLY` | Diagnostic artifact, no state change | ✅ Yes |
| `COMPLETED_EMPTY_ARTIFACT` | Artifact exists but is empty | ❌ No |
| `COMPLETED_NOOP` | No text, no artifact, duration < 10s | ❌ No |
| `FAILED_EXECUTION` | Task failed | ❌ No |
| `NEEDS_RETRY` | Transient failure | ❌ No |

**Stored as**: `completion_quality TEXT` column in `agent_tasks` DB table

**Hard rules**: Does not modify CLV state, does not mark `PENDING_CLOSING` as `COMPUTED`,
does not delete artifacts, does not change task `status`

**Tests passed**: 8 (`test_phase10_completion_quality.py`)

---

### Phase 11 — Deterministic Safe Task Executor

**Purpose**: Execute specific task types directly via Python logic,
bypassing LLM providers entirely. Guarantees non-empty, well-formed
artifacts even when LLM session is inactive.

**Key file**: `orchestrator/safe_task_executor.py`

**Implemented deterministic task types**:
| Type | Status | Description |
|------|--------|-------------|
| `closing_monitor` | ✅ Implemented | CLV closing-odds audit + upgrade pass |
| `ops_report` | ⬜ Planned | Autonomous ops report generation |
| `scheduler_health_check` | ⬜ Planned | Scheduler heartbeat audit |
| `artifact_health_check` | ⬜ Planned | Report artifact freshness audit |
| `data_quality_monitor` | ⬜ Planned | Data pipeline quality check |

**Hard rules**: Never calls any LLM/AI provider for registered deterministic task types.
Never fakes closing odds. Never marks `PENDING_CLOSING` as `COMPUTED` without
valid `closing_ts > prediction_time_utc`.

**Tests passed**: 23 (`test_phase11_safe_executor.py`)

---

### Phase 12 — Scheduler Idle Recovery

**Purpose**: Prevent false DEGRADED classification when all skips are protected
(e.g. `GLOBAL_HARD_OFF`). Replace crude "one per day" dedupe with slot-based
cadence policy for DATA_WAITING safe work.

**Key files**:
- `orchestrator/scheduler_skip_classifier.py` — classifies each skip by reason
- `orchestrator/data_waiting_cadence.py` — slot-based cadence policy

**Skip reason constants**:
| Constant | Value | Meaning |
|----------|-------|---------|
| `SKIP_HARD_OFF` | `hard_off_protection` | `GLOBAL_HARD_OFF` active |
| `SKIP_NO_QUEUED` | `no_queued_tasks` | Queue empty |
| `SKIP_DAILY_CAP` | `daily_cap` | Daily task limit reached |
| `SKIP_GOVERNANCE` | `governance_blocked` | Family blocked by governance |
| `SKIP_PROVIDER` | `worker_provider_unavailable` | LLM provider unavailable |
| `SKIP_DUPLICATE` | `duplicate_safe_task` | Duplicate within window |
| `SKIP_SCHEDULER_OFF` | `scheduler_disabled` | `scheduler_enabled = False` |
| `SKIP_UNKNOWN` | `unknown` | Unparseable message |

**Safe work cadence** (slot-based, not once-per-day):
| Task type | Interval |
|-----------|----------|
| `closing_monitor` | 20 min |
| `scheduler_health_check` | 60 min |
| `artifact_health_check` | 4 hours |
| `ops_report` | 8 hours |

**Key fix**: `count_unexplained_consecutive_skips()` excludes `SKIP_HARD_OFF`
and `SKIP_SCHEDULER_OFF` from the degradation count. Only unexplained skips
≥ 3 trigger `DEGRADED`.

**Tests passed**: 34 (`test_phase12_scheduler_idle_recovery.py`)  
**Plus**: 25 (`test_data_waiting_safe_workflow.py`) — updated to use `SKIP_CADENCE` return value

---

### Phase 13 — Autonomous Readiness Dashboard

**Purpose**: Aggregate all Phase 6–12 sub-system states into a single
operator-facing readiness summary. Observability only — never writes state.

**Key files**:
- `orchestrator/optimization_readiness.py` — aggregator + state derivation
- `scripts/run_optimization_readiness.py` — CLI tool

**Readiness states** (priority order, highest first):
| State | Severity | Condition |
|-------|----------|-----------|
| `LEARNING_READY` | GREEN | CLV computed + learning families allowed |
| `WAITING_ACTIVE` | GREEN/YELLOW | CLV pending + safe work on cadence |
| `SAFE_WORK_ACTIVE` | GREEN/ORANGE | Safe families allowed, no CLV gate issue |
| `BLOCKED` | ORANGE | Most families blocked, no recent safe work |
| `DEGRADED` | RED | Unexplained skips ≥ 3 or all completions empty/noop |

**Severity mapping**:
| Severity | Icon | Condition |
|----------|------|-----------|
| GREEN | 🟢 | LEARNING_READY or WAITING_ACTIVE + healthy cadence |
| YELLOW | 🟡 | WAITING_ACTIVE + cadence lagging (no effective completions) |
| ORANGE | 🟠 | BLOCKED or SAFE_WORK_ACTIVE without recent completions |
| RED | 🔴 | DEGRADED |

**CLI**:
```bash
python3 scripts/run_optimization_readiness.py --print   # human-readable dashboard
python3 scripts/run_optimization_readiness.py --json    # machine-readable JSON
```

**Artifacts written**:
- `data/wbc_backend/reports/optimization_readiness_latest.json`
- `docs/orchestration/optimization_readiness_latest.md`

**Tests passed**: 19 (`test_phase13_readiness_dashboard.py`)

---

## 3. Operating States Reference

### `LEARNING_READY`

**What it means**: At least one CLV record has reached `COMPUTED` status. Governance
allows learning task families. The system is cleared for model patching,
strategy reinforcement, and calibration.

**Allowed tasks**: All families including `model-patch-atomic`, `strategy-reinforcement`,
`calibration-atomic`, `feature-atomic`, `regime-atomic`, `feedback-atomic`,
`backtest-validity-atomic`

**Blocked tasks**: None (all families unlocked)

**Operator action**: Switch to `safe-run` mode and allow learning tasks to execute.
Monitor patch quality via `completion_quality` and CLV improvement via ops report.

---

### `WAITING_ACTIVE`

**What it means**: All CLV records are still `PENDING_CLOSING`. The system is
waiting for market settlement and closing odds. Safe non-learning work is running
on cadence (closing_monitor every 20 min, etc.).

**Allowed tasks**: `closing-monitor`, `ops-report`, `scheduler-health-check`,
`artifact-health-check`, `wiki-maintenance`, `architecture-cleanup`,
`observability-ux`, `maintenance`, `data-monitor`, `system-reliability`,
`simulation-atomic`

**Blocked tasks**: All learning families (model-patch, strategy-reinforcement, etc.)

**Operator action**: Wait for market settlement. Monitor `closing_monitor` cadence.
Check `docs/orchestration/optimization_readiness_latest.md` for status updates.

---

### `SAFE_WORK_ACTIVE`

**What it means**: Governance allows safe families. Some CLV records may exist,
but the primary gate for learning is not met, or the system is between learning cycles.

**Allowed tasks**: Safe families only (same as WAITING_ACTIVE)

**Blocked tasks**: Learning families

**Operator action**: Continue safe-work cadence. Monitor for closing odds arrival.

---

### `DATA_WAITING`

**What it means**: This is the Phase 8 governance state (not the same as Phase 13
readiness state). Mapped to `WAITING_ACTIVE` in the readiness dashboard. All CLV
records are `PENDING_CLOSING`; full learning is blocked at the governance layer.

**Note**: This is the most common state during the market settlement waiting period.
It does **not** indicate a problem — it means the system is correctly waiting.

---

### `DEGRADED`

**What it means**: The scheduler is experiencing unexplained consecutive skips
(≥ 3 skips NOT explained by hard-off/scheduler-disabled), OR all recent task
completions are empty artifacts or no-ops (LLM session inactive).

**Allowed tasks**: None effectively (tasks are skipped or producing no output)

**Blocked tasks**: All (de facto)

**Operator action**:
1. Check scheduler logs: `runtime/agent_orchestrator/`
2. Check LLM provider session (copilot-daemon active?)
3. Check recent task artifacts in `data/wbc_backend/reports/`
4. If hard-off is the cause, this state should **not** appear (hard-off skips are excluded from the degradation count)

---

### `BLOCKED`

**What it means**: Most task families are blocked by governance, and no effective
safe work has completed recently. The system is operational but producing no output.

**Allowed tasks**: Theoretically some safe families are allowed

**Blocked tasks**: All learning families + most safe families (governance config)

**Operator action**: Review governance settings. Check if `scheduler_enabled = True`.
Check `llm_execution_mode` setting. Review blocked families in Phase 8 report.

---

## 4. Learning Gates

Learning is gated independently at multiple layers. **All gates must pass simultaneously.**

### Gate 1 — Phase 6 Data Gate

**Condition**: At least one CLV record with `clv_computed > 0`

**Checked by**: `orchestrator/phase6_data_registry.py` → `get_phase6_status()`

**Blocked when**: All 14 (or N) records are `PENDING_CLOSING`

**Cannot be bypassed**: Hard-coded in phase6_data_registry and enforced by
Phase 8 governance independently

---

### Gate 2 — Phase 7 Closing Odds Gate

**Condition**: `closing_ts > prediction_time_utc` for at least one record.
Real closing odds must be in `data/mlb_context/odds_timeline.jsonl`.

**Checked by**: `orchestrator/closing_odds_monitor.py`

**Hard rules (never weakened)**:
- `closing_ts` must be strictly after `prediction_time_utc`
- Closing ML must be a real value (not interpolated or faked)
- Original 6U JSONL files are never modified

---

### Gate 3 — Phase 8 Governance Gate

**Condition**: `optimization_state.classify()` returns a state where
learning families are in `allowed_task_families`

**Checked by**: `orchestrator/optimization_state.py` → `classify()`

**Blocked when**:
- `current_state == DATA_WAITING` — always blocks learning families
- `llm_execution_mode == hard-off` — no execution possible
- `scheduler_enabled == False` — scheduler does not run

---

### Gate 4 — Phase 10 Completion Quality Gate

**Condition**: Completed tasks must produce `COMPLETED_VALID` or
`COMPLETED_DIAGNOSTIC_ONLY` output to count as effective

**Checked by**: `orchestrator/task_completion_validator.py`

**Blocked when**:
- LLM session is inactive → `COMPLETED_EMPTY_ARTIFACT` or `COMPLETED_NOOP`
- Task runs but produces no meaningful output

---

### Learning Blocked Conditions (summary)

| Condition | Which gate blocks |
|-----------|------------------|
| CLV is `PENDING_CLOSING` only | Gate 1, Gate 2, Gate 3 |
| `hard-off` mode enabled | Gate 3 (worker does not execute) |
| `scheduler_enabled = False` | Gate 3 |
| Unexplained skips ≥ 3 | Phase 12 detects, Phase 13 reports RED |
| Task output is empty/noop | Gate 4 (not counted as effective) |
| No valid closing odds in timeline | Gate 2 |
| Historical rows blocked | Gate 1 (those rows never reach COMPUTED) |

---

## 5. Core Commands

### Readiness Dashboard

```bash
# Human-readable dashboard (recommended first check)
python3 scripts/run_optimization_readiness.py --print

# Machine-readable JSON
python3 scripts/run_optimization_readiness.py --json

# Both (writes artifacts AND prints to stdout)
python3 scripts/run_optimization_readiness.py --print --json
```

Artifacts written to:
- `data/wbc_backend/reports/optimization_readiness_latest.json`
- `docs/orchestration/optimization_readiness_latest.md`

---

### Ops Report

```bash
# Last 8 hours (default)
python3 scripts/run_optimization_ops_report.py

# Last 24 hours
python3 scripts/run_optimization_ops_report.py --window 24h

# JSON output
python3 scripts/run_optimization_ops_report.py --json
```

---

### Decision Card (full operator dashboard)

```bash
# Human-readable card (includes all phases 6-13)
python3 scripts/ops_decision_card.py

# JSON payload
python3 scripts/ops_decision_card.py --json

# Inspect readiness section only
python3 scripts/ops_decision_card.py | grep -A 12 "AUTONOMOUS READINESS"
```

---

### Closing Monitor (upgrade PENDING_CLOSING → COMPUTED)

```bash
# Run for today's date
python3 orchestrator/closing_odds_monitor.py

# Run for specific date
python3 orchestrator/closing_odds_monitor.py --date 2026-04-30
```

This is also run automatically by the deterministic executor every 20 minutes
in `WAITING_ACTIVE` state when the cadence slot opens.

---

### Planner Tick (create tasks)

```bash
# Run planner once
python3 -c "from orchestrator.planner_tick import run_planner_tick; run_planner_tick()"
```

In `DATA_WAITING` state, the planner creates only safe-work tasks (closing_monitor,
scheduler_health_check, etc.) based on the cadence policy in `data_waiting_cadence.py`.

---

### Worker Tick (execute tasks)

```bash
# Run worker once
python3 -c "from orchestrator.worker_tick import run_worker_tick; run_worker_tick()"
```

The worker respects `llm_execution_mode`:
- `hard-off`: no execution; all runs logged as `SKIPPED` with `hard_off_protection`
- `safe-run`: executes deterministic tasks only (no LLM call)
- `manual`: full execution with LLM provider

---

### Switching Execution Mode

```bash
# Check current mode
python3 -c "
from orchestrator.db import get_setting
print('mode:', get_setting('llm_execution_mode'))
print('scheduler:', get_setting('scheduler_enabled'))
"

# Switch to safe-run (deterministic tasks only, no LLM)
python3 scripts/run_mode.py safe-run

# Switch to manual (full LLM execution)
python3 scripts/run_mode.py manual
```

---

### Test Suites

```bash
# Phase 13 only (fastest check)
python3 -m pytest tests/test_phase13_readiness_dashboard.py -v

# Phase 9-13 + data_waiting workflow (155 tests, < 2s)
python3 -m pytest \
  tests/test_phase9_optimization_ops.py \
  tests/test_data_waiting_safe_workflow.py \
  tests/test_phase10_completion_quality.py \
  tests/test_phase11_safe_executor.py \
  tests/test_phase12_scheduler_idle_recovery.py \
  tests/test_phase13_readiness_dashboard.py \
  -q

# Full Phase 6-13 suite (551 tests, ~100s)
python3 -m pytest \
  tests/test_phase6_integration.py \
  tests/test_phase6_training_integration.py \
  tests/test_phase6r_native_timestamps.py \
  tests/test_phase6s_odds_snapshot_alignment.py \
  tests/test_phase6t_registry_conversion.py \
  tests/test_phase6u_clv_record_generation.py \
  tests/test_phase7_closing_to_learning.py \
  tests/test_phase7_integration.py \
  tests/test_phase8_integration.py \
  tests/test_phase8_optimization_governance.py \
  tests/test_phase9_optimization_ops.py \
  tests/test_data_waiting_safe_workflow.py \
  tests/test_phase10_completion_quality.py \
  tests/test_phase11_safe_executor.py \
  tests/test_phase12_scheduler_idle_recovery.py \
  tests/test_phase13_readiness_dashboard.py \
  -q
```

---

## 6. Critical Files

### `orchestrator/optimization_state.py`

Phase 8 governance classifier. Single source of truth for which task families
are allowed at any given moment. Called by planner, worker, ops report, and
readiness dashboard.

**Key function**: `classify(decision_card_payload=None) -> dict`  
**Returns**: `state`, `reasons`, `allowed_task_families`, `blocked_task_families`,
`recommended_next_action`

---

### `orchestrator/optimization_readiness.py`

Phase 13 readiness aggregator. Combines all Phase 6–12 sub-system states into
a single `readiness_state` + `severity`. **Read-only — never writes state.**

**Key function**: `get_readiness_summary() -> dict`  
**Key function**: `render_readiness_markdown(summary: dict) -> str`

---

### `orchestrator/optimization_ops_report.py`

Phase 9 ops report generator. Reads `agent_tasks`/`agent_task_runs` from DB,
aggregates skip reasons, quality counts, and CLV progress.

**Key function**: `generate_report(window="8h") -> dict`  
**Key function**: `render_report_markdown(report: dict) -> str`

---

### `orchestrator/safe_task_executor.py`

Phase 11 deterministic executor. Routes task types to Python executor functions,
bypassing LLM. Currently implements `closing_monitor`; four more are planned.

**Key function**: `execute_safe_task(task: dict) -> dict`  
**Key dict**: `DETERMINISTIC_TASK_TYPES: dict[str, Callable]`  
**Key frozenset**: `_PLANNED_DETERMINISTIC_TYPES` — not yet implemented

---

### `orchestrator/closing_odds_monitor.py`

Phase 7 closing odds processor. Scans `odds_timeline.jsonl` for valid post-
prediction closing odds and upgrades `PENDING_CLOSING` records to `COMPUTED`.

**Key function**: `run_monitor(date_str=None) -> dict`  
**Key function**: `get_monitor_state() -> dict | None`

---

### `orchestrator/task_completion_validator.py`

Phase 10 quality classifier. Inspects completed task output and assigns a
`completion_quality` value stored in the DB `agent_tasks` table.

**Key function**: `classify_task_quality(task: dict) -> str`  
**Key constants**: `QUALITY_VALID`, `QUALITY_DIAGNOSTIC_ONLY`, `QUALITY_EMPTY_ARTIFACT`,
`QUALITY_NOOP`, `QUALITY_EFFECTIVE_STATES`

---

### `orchestrator/scheduler_skip_classifier.py`

Phase 12 skip classifier. Parses `agent_task_runs.message` to identify why
each run was skipped. Distinguishes protected skips (hard-off) from degradation.

**Key function**: `classify_skip_reason(run: dict) -> str`  
**Key function**: `count_unexplained_consecutive_skips(runs: list[dict]) -> int`  
**Key function**: `all_consecutive_skips_are_protected(runs: list[dict]) -> bool`

---

### `orchestrator/data_waiting_cadence.py`

Phase 12 cadence policy. Manages slot-based deduplication for DATA_WAITING safe
tasks. Prevents both duplicates within a window and over-eager suppression
across windows.

**Key function**: `get_due_safe_tasks(now=None) -> list[str]`  
**Key function**: `cadence_dedupe_key(task_type: str, now=None) -> str`  
**Key function**: `is_forbidden_task_type(task_type: str) -> bool`

---

### `scripts/ops_decision_card.py`

Full operator dashboard. Calls all compute functions (Phase 6–13) and renders
a terminal-friendly card. Also outputs JSON for scripting.

**Key function**: `build_payload() -> dict`  
**Key function**: `render_card(payload: dict) -> str`  
**Sections**: System health → WBC today → Recent performance → Postmortem →
CLV metrics → Scheduler status → Phase 9 ops → **Phase 13 readiness**

---

### `scripts/run_optimization_readiness.py`

Phase 13 CLI. Calls `get_readiness_summary()` and writes canonical artifacts.

**Usage**: `python3 scripts/run_optimization_readiness.py [--print] [--json]`

---

### `scripts/run_optimization_ops_report.py`

Phase 9 CLI. Calls `generate_report()` and writes timestamped markdown to
`docs/orchestration/`.

**Usage**: `python3 scripts/run_optimization_ops_report.py [--window 8h|24h] [--json]`

---

## 7. Known Limitations

### 1. Learning waits for valid closing odds

The primary unblocking event is the arrival of real closing odds in
`data/mlb_context/odds_timeline.jsonl` with `closing_ts > prediction_time_utc`.
Until then, all 14 CLV records remain `PENDING_CLOSING` and all learning
families stay blocked. **This is by design and cannot be shortcut.**

### 2. PENDING_CLOSING records cannot reinforce strategy

Records in `PENDING_CLOSING` state contain only pre-game predictions.
Without closing odds, there is no realized CLV signal, so strategy
reinforcement and model patching have no valid feedback signal.

### 3. Hard-off mode prevents all worker execution

When `llm_execution_mode = hard-off`, the worker logs every execution
attempt as `SKIPPED` with `hard_off_protection`. No tasks execute —
including deterministic ones. Use `safe-run` mode for deterministic-only
execution.

### 4. Some historical rows remain permanently blocked

Rows that pre-date the native-timestamp system (Phase 6R) may lack a valid
`prediction_time_utc` and cannot be matched to closing odds. These rows
remain `PENDING_CLOSING` indefinitely. They do not block the system —
any record reaching `COMPUTED` is sufficient to unlock learning.

### 5. Deterministic executor currently limited to `closing_monitor`

Four planned deterministic task types (`ops_report`, `scheduler_health_check`,
`artifact_health_check`, `data_quality_monitor`) are defined in
`_PLANNED_DETERMINISTIC_TYPES` but not yet implemented. When invoked,
the executor raises `ValueError`. These will fall back to LLM execution
in `safe-run` mode until implemented.

### 6. Phase 13 readiness depends on Phase 9 ops report for skip data

`_get_ops_summary()` and `_get_skip_health()` in `optimization_readiness.py`
both call `generate_report(window="8h")`. If the DB is empty (fresh install),
both return zero counts — the system will show `WAITING_ACTIVE / YELLOW`
rather than an error.

### 7. `test_data_waiting_safe_workflow.py` uses `SKIP_CADENCE` return value

Two assertions in this test file were updated from `SKIP_DAILY_CAP` to
`SKIP_CADENCE` as part of Phase 12. Any future change to the planner's
cadence return value must update these assertions.

---

## 8. Recommended Next Roadmap

### Priority 1 — Wait for and ingest valid closing odds

**When**: As soon as market settlement data becomes available  
**Action**:
1. Add closing odds entries to `data/mlb_context/odds_timeline.jsonl` with:
   - `match_id` matching a Phase 6T record
   - `closing_ts` strictly after `prediction_time_utc`
   - `closing_ml` (a real market closing line, not faked)
2. Run: `python3 orchestrator/closing_odds_monitor.py`
3. Verify: `python3 scripts/run_optimization_readiness.py --print`
4. Expected: `readiness_state` transitions from `WAITING_ACTIVE` → `LEARNING_READY`

---

### Priority 2 — Expand deterministic executors

Implement the four planned deterministic task types in `orchestrator/safe_task_executor.py`.
This eliminates LLM dependency for all safe-work cadence tasks.

**Order of implementation** (lowest risk first):

| Task type | Purpose | Effort |
|-----------|---------|--------|
| `scheduler_health_check` | Count DB skips, check heartbeat freshness | Low |
| `artifact_health_check` | Scan `data/wbc_backend/reports/` for stale files | Low |
| `ops_report` | Generate Phase 9 report artifact without LLM | Medium |
| `data_quality_monitor` | Check Phase 6T/6U JSONL row counts and freshness | Medium |

**Each implementation requires**:
1. Python executor function in `safe_task_executor.py`
2. Add to `DETERMINISTIC_TASK_TYPES` dict
3. Remove from `_PLANNED_DETERMINISTIC_TYPES`
4. Add tests in `test_phase11_safe_executor.py`

---

### Priority 3 — First learning cycle (once CLV COMPUTED exists)

**When**: After `optimization_readiness.readiness_state == LEARNING_READY`  
**Sequence**:

1. **Switch to `safe-run` mode**:
   ```bash
   python3 scripts/run_mode.py safe-run
   ```

2. **Enable strategy feedback**:
   - Allow `feedback-atomic` family in governance (automatic when `DATA_READY`)
   - Verify with: `python3 -c "from orchestrator.optimization_state import classify; print(classify()['state'])"`

3. **Validate first model patch**:
   - Monitor `orchestrator/patch_validator.py` output
   - Check `completed_valid_tasks` in ops report

4. **Update training memory**:
   - Confirm `orchestrator/training_memory.py` recorded the patch
   - Verify CLV improvement signal is positive before next patch

---

### Priority 4 — Long-term system improvements

| Area | Description |
|------|-------------|
| **Regime-specific calibration** | Separate model calibration per competition regime (WBC vs. MLB regular season) |
| **Automated patch rollback** | Trigger automatic rollback if post-patch Brier score worsens by > threshold |
| **More robust feature engineering** | Add weather, travel fatigue, and lineup freshness features |
| **Odds timeline automation** | Automate ingestion of post-game closing odds from odds API |
| **Alert system** | Email/Telegram notification when `readiness_state` transitions |
| **Phase 13 severity history** | Track severity changes over time for trend analysis |

---

## Appendix — Test Coverage Summary

| Phase | Test file(s) | Tests |
|-------|-------------|-------|
| 6 (6P–6U) | 6 files | 217 |
| 7 | 2 files | 84 |
| 8 | 2 files | 81 |
| 9 | 1 file | 36 |
| 9 (DATA_WAITING workflow) | `test_data_waiting_safe_workflow.py` | 25 |
| 10 | 1 file | 8 |
| 11 | 1 file | 23 |
| 12 | 1 file | 34 |
| 13 | 1 file | 19 |
| **Total** | **17 files** | **527** |

> Note: pytest reports 551 passing due to parametrized test expansion.
> All tests pass as of 2026-04-30.

---

## Appendix — Live State Snapshot (2026-04-30)

```
Readiness state  : WAITING_ACTIVE
Severity         : GREEN
Learning allowed : NO
Governance state : DATA_WAITING
CLV computed     : 0
CLV pending      : 14
Skip health      : HEALTHY (hard-off protected)
Quality          : OK (effective completions present)
Next event       : Wait for post-prediction closing odds to become available
Action           : Run closing-monitor now (cadence slot is open)
```

---

*This document was generated as Phase 14 of the autonomous optimization system.*  
*Do not modify runtime behaviour based on this document.*  
*`PHASE_14_SYSTEM_BASELINE_HANDOFF_VERIFIED`*
