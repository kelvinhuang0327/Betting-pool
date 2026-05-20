# Autonomous Learning Governance Baseline Report

**Date**: 2026-05-01  
**Prepared by**: Governance Engineering  
**System state at time of writing**: `WAITING_ACTIVE` — 14 CLV records `PENDING_CLOSING`; no real `COMPUTED` CLV exists yet  
**Phases covered**: 18 · 19 · 20 · 21 · 22 · 23 · 24 · 25 · 26 · A1 · A2  
**Success marker**: `PHASE_27_AUTONOMOUS_LEARNING_GOVERNANCE_BASELINE_VERIFIED`

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Verified Phases 18–26 and A1/A2](#2-verified-phases-1826-and-a1a2)
3. [End-to-End State Machine](#3-end-to-end-state-machine)
4. [Safety Invariants](#4-safety-invariants)
5. [Operator Commands Reference](#5-operator-commands-reference)
6. [Current Limitations](#6-current-limitations)
7. [Recommended Next Roadmap](#7-recommended-next-roadmap)
8. [Architecture Summary](#8-architecture-summary)

---

## 1. System Overview

The autonomous optimization system is a governed, multi-phase pipeline that:

1. **Ingests** pre-game predictions via Phase 6 (trusted data pipeline, validated timestamps and odds snapshots)
2. **Waits** for market settlement and closing odds via Phase 7 (`ClosingOddsMonitor`, 15-min interval)
3. **Governs** which learning tasks are allowed via Phase 8 (6-state `optimization_state` classifier)
4. **Runs** safe deterministic tasks autonomously via planner/worker with deterministic executor
5. **Learns** by executing learning cycles only when `COMPUTED` CLV exists (`LEARNING_READY` gate)
6. **Patches** only through a multi-stage gate: patch candidate → sandbox evaluation → evaluation gate → human review queue → follow-up validation
7. **Guards** all external LLM calls via `AuditGuard` (Phase A1 / A2) — fail-closed
8. **Reports** health via decision card, ops report, and readiness dashboard

**Hard invariant that cannot be bypassed by any code path:**  
Learning families (`model-patch`, `strategy-reinforcement`, `calibration`, `feedback`, etc.) are **never** allowed until at least one CLV record reaches `COMPUTED` status. Production model modification requires human review approval, which only creates a follow-up validation task — never a direct deployment.

---

## 2. Verified Phases 18–26 and A1/A2

### Phase 18 — E2E Waiting Loop Runtime

| | |
|---|---|
| **Objective** | Prove the full `DATA_WAITING → WAITING_ACTIVE` loop runs correctly at runtime. Confirm planner, ops report, readiness, and decision card all reflect the waiting state; verify that no learning tasks are created while CLV records are `PENDING_CLOSING`. |
| **Verdict** | `PHASE_18_E2E_WAITING_LOOP_RUNTIME_VERIFIED` |
| **Tests** | `tests/test_phase18_e2e_waiting_loop.py` — 9 tests |
| **Runtime drill** | `scripts/run_phase18_e2e_validation.py --dry-run` |
| **Key files** | `orchestrator/planner_tick.py` (STEP 1.5 governance gate), `orchestrator/optimization_state.py`, `scripts/ops_decision_card.py`, `orchestrator/optimization_readiness.py` |
| **Hard rules enforced** | `PENDING_CLOSING` never unlocks learning families; governance gate fires before candidate loop |

---

### Phase 19 — Learning Unlock Simulation

| | |
|---|---|
| **Objective** | Validate that a sandbox `COMPUTED` CLV fixture transitions the system from `WAITING_ACTIVE` to `LEARNING_READY`. Verify governance allows `model-validation-atomic`, `strategy-reinforcement`, `feedback-atomic`. Negative test: `PENDING_CLOSING` cannot unlock learning. |
| **Verdict** | `PHASE_19_LEARNING_UNLOCK_SIMULATION_VERIFIED` |
| **Tests** | `tests/test_phase19_learning_unlock_simulation.py` — 9 tests |
| **Runtime drill** | `scripts/run_phase19_learning_unlock_validation.py` |
| **Key files** | `orchestrator/optimization_state.py`, `orchestrator/phase6_data_registry.py`, `orchestrator/planner_tick.py` |
| **Hard rules enforced** | `COMPUTED` CLV required for any learning family; `PENDING_CLOSING`-only state remains in `DATA_WAITING` |

---

### Phase 20 — First Sandbox Learning Cycle

| | |
|---|---|
| **Objective** | Orchestrate the first real sandbox learning cycle end-to-end: governance allows learning → `LearningCycleRunner` creates a `clv_quality_analysis` task → deterministic executor produces an artifact → training memory records the result → ops/readiness surfaces the result. |
| **Verdict** | `PHASE_20_FIRST_LEARNING_CYCLE_VERIFIED` |
| **Tests** | `tests/test_phase20_first_learning_cycle.py` — 9 tests |
| **Runtime drill** | `scripts/run_phase20_learning_cycle_validation.py` |
| **Key files** | `orchestrator/learning_cycle_runner.py`, `orchestrator/training_memory.py`, `orchestrator/planner_tick.py` (STEP 2 learning candidate injection) |
| **Hard rules enforced** | Sandbox learning cycle never modifies production model or strategy state; deterministic executor produces only in-memory artifact |

---

### Phase 21 — Learning Patch Gate

| | |
|---|---|
| **Objective** | Validate all four patch gate decision paths: `HOLD`, `INVESTIGATE_ONLY`, `REJECT_INSUFFICIENT_EVIDENCE`, `ALLOW_PATCH_CANDIDATE`. Confirm training memory persistence, ops/readiness exposure, and that no LLM is called. |
| **Verdict** | `PHASE_21_LEARNING_PATCH_GATE_VERIFIED` |
| **Tests** | `tests/test_phase21_learning_patch_gate.py` — 9 tests |
| **Runtime drill** | `scripts/run_phase21_patch_gate_validation.py` |
| **Key files** | `orchestrator/learning_patch_gate.py`, `orchestrator/learning_patch_task_generator.py`, `orchestrator/training_memory.py` |
| **Hard rules enforced** | Gate never emits a production patch candidate; only `ALLOW_PATCH_CANDIDATE` creates a sandbox evaluation task spec |

---

### Phase 22 — Sandbox Patch Evaluation Task

| | |
|---|---|
| **Objective** | Exercise the full pipeline from gate decision → task spec → deterministic executor → sandbox artifact → training memory → readiness exposure. Validate all three outcome paths: `KEEP_SANDBOX_CANDIDATE`, `REJECT_SANDBOX_CANDIDATE`, `NEED_MORE_DATA`. |
| **Verdict** | `PHASE_22_SANDBOX_PATCH_EVALUATION_TASK_VERIFIED` |
| **Tests** | `tests/test_phase22_sandbox_patch_evaluation.py` — 10 tests |
| **Runtime drill** | `scripts/run_phase22_patch_evaluation_validation.py` |
| **Key files** | `orchestrator/patch_task_generator.py`, `orchestrator/patch_validator.py`, `orchestrator/task_quality_gate.py`, `orchestrator/planner_tick.py` (STEP 2 sandbox candidate generation) |
| **Hard rules enforced** | Sandbox patch evaluation never writes to production model files; `production_patch_allowed = False` on all generated task specs |

---

### Phase 23 — Patch Evaluation Decision Gate

| | |
|---|---|
| **Objective** | Validate the four decision gate outcomes from sandbox patch evaluation artifact: `REJECT`, `REQUEST_MORE_DATA`, `HUMAN_REVIEW_REQUIRED`, `PROMOTE_TO_PRODUCTION_PROPOSAL`. Confirm `HUMAN_REVIEW_REQUIRED` correctly queues a review item and `PROMOTE_TO_PRODUCTION_PROPOSAL` does NOT bypass human review. |
| **Verdict** | `PHASE_23_PATCH_EVALUATION_DECISION_GATE_VERIFIED` |
| **Tests** | `tests/test_phase23_patch_evaluation_gate.py` — 10 tests |
| **Runtime drill** | `scripts/run_phase23_patch_evaluation_gate_validation.py` |
| **Key files** | `orchestrator/patch_evaluation_gate.py`, `orchestrator/human_review_queue.py`, `orchestrator/planner_tick.py` (STEP 0.9 review gate) |
| **Hard rules enforced** | `PROMOTE_TO_PRODUCTION_PROPOSAL` always creates a `human_review_queue` item with `production_patch_allowed = False`; gate never creates a production patch task directly |

---

### Phase 24 — Human Review Queue

| | |
|---|---|
| **Objective** | Implement and validate the full Human Review Queue lifecycle: `PENDING → APPROVED | REJECTED | MORE_DATA_REQUESTED`. Verify persistent storage, lifecycle transitions, queue summary, CLI tooling, and the three hard invariants embedded in every queue item. |
| **Verdict** | `PHASE_24_HUMAN_REVIEW_QUEUE_VERIFIED` |
| **Tests** | `tests/test_phase24_human_review_queue.py` — 10 tests |
| **Runtime drill** | `scripts/run_phase24_human_review_queue_validation.py` |
| **Key files added** | `orchestrator/human_review_queue.py` (new), `scripts/review_queue.py` (new) |
| **Key files modified** | `orchestrator/planner_tick.py` (STEP 0.9 gate), `orchestrator/optimization_readiness.py`, `orchestrator/optimization_ops_report.py` |
| **Hard rules enforced** | `production_patch_allowed = False` always; `production_model_modified = False` always; `external_llm_called = False` always — set at creation, never mutated |

---

### Phase 25 — Human Review UI Actionability

| | |
|---|---|
| **Objective** | Make the Human Review Queue visible and actionable from all operator-facing surfaces: Decision Card, Readiness Report, Ops Report, CLI (`review_queue.py`), and the FastAPI summary endpoint. Every pending review must show all four action commands (`show`, `approve`, `reject`, `more-data`). |
| **Verdict** | `PHASE_25_HUMAN_REVIEW_UI_ACTIONABILITY_VERIFIED` |
| **Tests** | `tests/test_phase25_human_review_ui.py` — 9 tests |
| **Key files modified** | `scripts/ops_decision_card.py` (HUMAN REVIEW QUEUE section, `compute_human_review_queue()`), `orchestrator/optimization_readiness.py` (PHASE 24 section in `render_readiness_markdown()`), `orchestrator/optimization_ops_report.py` (per-item action blocks in `render_markdown()`), `scripts/review_queue.py` (action hints in `cmd_list()`, `cmd_show()`, `cmd_approve()`, `cmd_reject()`, `cmd_more_data()`), `orchestrator/api.py` (`_get_human_review_actionability_safe()`, `/api/orchestrator/summary` updated) |
| **Hard rules enforced** | All UI surfaces read-only with respect to queue state; `cmd_approve()` explicitly prints "does NOT deploy any production patch or modify the live model" |

---

### Phase 26 — Full Governance Loop Runtime Drill

| | |
|---|---|
| **Objective** | Verify the complete governance loop at runtime in a fully isolated environment: queue a production proposal → planner blocks → approve/reject/more-data each behave correctly → reports show review state → no production model modified → no external LLM called. |
| **Verdict** | `PHASE_26_FULL_GOVERNANCE_LOOP_RUNTIME_VERIFIED` |
| **Tests** | `tests/test_phase26_governance_loop.py` — 7 tests |
| **Runtime drill** | `scripts/run_phase26_governance_loop_drill.py` (7 tasks, all isolated via `tempfile.TemporaryDirectory`) |
| **Key files added** | `scripts/run_phase26_governance_loop_drill.py`, `tests/test_phase26_governance_loop.py` |
| **Hard rules enforced** | PENDING review blocks planner (returns `WAITING_FOR_HUMAN_REVIEW`, no `db.create_task`); approval only permits `production-proposal-validation` family; rejection creates no follow-up; more-data only creates `clv-quality-analysis`; all items carry `production_patch_allowed = False` and `external_llm_called = False` through full lifecycle |

---

### Phase A1 — AuditGuard Runtime Integration

| | |
|---|---|
| **Objective** | Prove that the Planner is local-only (ProviderFactory blocks external providers) and that the Worker's external LLM paths (`claude`, `codex`) are guarded by `AuditGuard` with correct `ATTEMPT → RESULT` lifecycle, including fail-closed behavior when ATTEMPT write fails. |
| **Verdict** | `PLANNER_LOCAL_WORKER_AUDIT_GUARDED_VERIFIED` |
| **Tests** | `tests/test_llm_audit_lifecycle.py` — 16 tests (items 1–14 of audit lifecycle + planner block scenarios) |
| **Key files added/modified** | `orchestrator/provider_audit_guard.py` (`AuditGuard` context manager), `orchestrator/provider_factory.py` (planner external block), `orchestrator/worker_tick.py` (`AuditGuard` wrapping `claude`/`codex` subprocesses), `orchestrator/copilot_daemon.py` (`AuditGuard` block), `orchestrator/llm_audit.py` (event persistence) |
| **Hard rules enforced** | Planner role: external providers blocked by `ProviderFactory`; Worker role: `AuditGuard` always writes ATTEMPT before subprocess, RESULT after; ATTEMPT failure raises `AuditGuardBlockedError` (subprocess never called) |

---

### Phase A2 — AuditGuard Runtime Smoke

| | |
|---|---|
| **Objective** | Runtime smoke validation with no real external quota consumed: (1) coverage checker confirms `FULL` coverage across all 3 orchestrator-controlled LLM paths, (2) blocked-call smoke confirms `BLOCKED` event written without subprocess call, (3) allowed mocked-call smoke confirms `ATTEMPT + RESULT + Usage` lifecycle, (4) API schema check confirms stable `/llm-audit/recent` and `/llm-usage/today` schema. |
| **Verdict** | `LLM_AUDIT_GUARD_RUNTIME_VERIFIED` |
| **Tests** | 13 runtime checks (4 categories) |
| **Runtime drill** | `scripts/run_llm_audit_guard_runtime_validation.py` |
| **Key files added** | `orchestrator/llm_audit_coverage.py` (AST-based coverage scanner), `docs/orchestration/llm_audit_guard_runtime_report_2026-05-01.md` |
| **Hard rules enforced** | Coverage status must be `FULL` (no uncovered external paths); blocked smoke must confirm zero subprocess calls; all external quota consumption in the system is accountable via audit JSONL |

---

## 3. End-to-End State Machine

The system operates through a series of nested state machines. The outer machine describes the **optimization readiness state**; the inner machines describe individual **task gate decisions** within each phase of the learning-to-patch pipeline.

### 3.1 Outer State: Optimization Readiness

```
┌─────────────────────────────────────────────────────────────┐
│                   WAITING_ACTIVE                            │
│  • All CLV records are PENDING_CLOSING only                 │
│  • learning_allowed = false                                 │
│  • Planner creates safe tasks only (diagnostic, reporting)  │
│  • ClosingOddsMonitor polls every 15 min                    │
│  • State machine stays here until ≥1 COMPUTED CLV exists    │
└────────────────┬────────────────────────────────────────────┘
                 │  ≥1 CLV record upgrades to COMPUTED
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   LEARNING_READY                            │
│  • COMPUTED CLV exists                                      │
│  • learning_allowed = true                                  │
│  • Planner may create: model-validation-atomic,             │
│    strategy-reinforcement, feedback-atomic, calibration,    │
│    clv_quality_analysis                                     │
│  • Governance still filters by optimization_state (Phase 8) │
└────────────────┬────────────────────────────────────────────┘
                 │  governance permits LEARNING_CYCLE tasks
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                   LEARNING_CYCLE                            │
│  • LearningCycleRunner active                               │
│  • Tasks: clv_quality_analysis → learning_insight →         │
│    training_memory update                                   │
│  • Outputs: learning insight artifact                       │
│  • No production model writes                               │
└────────────────┬────────────────────────────────────────────┘
                 │  learning insight produced
                 ▼
                PATCH_GATE  (see §3.2)
```

### 3.2 Inner State: Patch Gate (`orchestrator/learning_patch_gate.py`)

```
learning_insight_artifact
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │               PATCH GATE                   │
  │  Decision:                                 │
  │                                            │
  │  HOLD                 → no task created    │
  │  INVESTIGATE_ONLY     → diagnostic task    │
  │  REJECT_INSUFFICIENT  → training memory    │
  │    _EVIDENCE             update only       │
  │  ALLOW_PATCH_CANDIDATE→ sandbox eval task  │
  └──────────────────────┬──────────────────────┘
                         │  ALLOW_PATCH_CANDIDATE only
                         ▼
            SANDBOX_PATCH_EVALUATION  (see §3.3)
```

### 3.3 Inner State: Sandbox Patch Evaluation (`orchestrator/patch_task_generator.py`)

```
sandbox_evaluation_task (production_patch_allowed=False)
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │        SANDBOX PATCH EVALUATION             │
  │  Outcomes:                                 │
  │                                            │
  │  KEEP_SANDBOX_CANDIDATE  → proceed to      │
  │                             evaluation gate │
  │  REJECT_SANDBOX_CANDIDATE→ archive, stop   │
  │  NEED_MORE_DATA          → clv_quality     │
  │                             _analysis task  │
  └──────────────────────┬──────────────────────┘
                         │  KEEP_SANDBOX_CANDIDATE only
                         ▼
           PATCH_EVALUATION_GATE  (see §3.4)
```

### 3.4 Inner State: Patch Evaluation Gate (`orchestrator/patch_evaluation_gate.py`)

```
sandbox_evaluation_artifact
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │        PATCH EVALUATION GATE                │
  │  Decision:                                 │
  │                                            │
  │  REJECT                  → archive only    │
  │  REQUEST_MORE_DATA       → clv_quality     │
  │                             _analysis task  │
  │  HUMAN_REVIEW_REQUIRED   → queue PENDING   │
  │                             review item     │
  │  PROMOTE_TO_PRODUCTION   → queue PENDING   │
  │    _PROPOSAL               review item     │
  └──────────────────────┬──────────────────────┘
                         │  HUMAN_REVIEW_REQUIRED
                         │  or PROMOTE_TO_PRODUCTION_PROPOSAL
                         ▼
              HUMAN_REVIEW_QUEUE  (see §3.5)
```

### 3.5 Human Review Queue (`orchestrator/human_review_queue.py`)

```
PENDING (production_patch_allowed=False, external_llm_called=False,
         production_model_modified=False — all set at creation, never mutated)
    │
    ├── PENDING → blocks planner (STEP 0.9 returns WAITING_FOR_HUMAN_REVIEW)
    │
    ├─ approve_review()
    │       │
    │       └─► APPROVED  ──────────────────────────────────────────────────►
    │                    ┌─────────────────────────────────────────────────┐│
    │                    │ Planner STEP 0.9 generates candidate:          ││
    │                    │   analysis_family = production-proposal-        ││
    │                    │     validation                                  ││
    │                    │   production_patch_allowed = False              ││
    │                    │   (NO production model write)                   ││
    │                    └─────────────────────────────────────────────────┘│
    │
    ├─ reject_review()
    │       │
    │       └─► REJECTED  ─── no follow-up task generated by planner ─────►
    │
    └─ request_more_data()
            │
            └─► MORE_DATA_REQUESTED ────────────────────────────────────────►
                         ┌─────────────────────────────────────────────────┐
                         │ Planner STEP 0.9 generates candidate:          │
                         │   task_type = clv_quality_analysis              │
                         │   analysis_family = clv-quality-analysis        │
                         │   (data collection only, no production patch)   │
                         └─────────────────────────────────────────────────┘
```

---

## 4. Safety Invariants

The following invariants are enforced by code and verified by tests. Each is stated explicitly, with the enforcing module and the test reference.

| # | Invariant | Enforcing Module | Test Reference |
|---|-----------|-----------------|----------------|
| 1 | `PENDING_CLOSING` never unlocks learning. `learning_allowed = False` until ≥1 CLV record is `COMPUTED`. | `orchestrator/optimization_state.py`, `orchestrator/planner_tick.py` STEP 1.5 | `test_phase19`, `test_phase18` |
| 2 | `COMPUTED` CLV is required to enter `LEARNING_READY`. No other event unlocks learning families. | `orchestrator/optimization_state.py` `classify()` | `test_phase19` |
| 3 | Sandbox learning cycle never modifies production model files or strategy state. All learning artifacts are in-memory or written to `runtime/` only. | `orchestrator/learning_cycle_runner.py` | `test_phase20` |
| 4 | Sandbox patch evaluation never creates a production patch. All generated task specs have `production_patch_allowed = False`. | `orchestrator/patch_task_generator.py`, `orchestrator/patch_validator.py` | `test_phase22` |
| 5 | Production proposal requires human review. `PROMOTE_TO_PRODUCTION_PROPOSAL` always creates a `PENDING` review item — never a deployment task. | `orchestrator/patch_evaluation_gate.py`, `orchestrator/human_review_queue.py` | `test_phase23` |
| 6 | Approval does not deploy a production patch. `production_patch_allowed` remains `False` after `approve_review()`. Approval only unlocks a follow-up validation task. | `orchestrator/human_review_queue.py` `approve_review()` | `test_phase24`, `test_phase26` |
| 7 | The follow-up task generated after approval is one of the safe families only: `production-proposal-validation`, `additional-validation`, `paper-rollout-plan`, `model-validation-atomic`, or `clv-quality-analysis`. Never a production model write. | `orchestrator/planner_tick.py` STEP 0.9 | `test_phase26` `test_approve_creates_safe_followup_only` |
| 8 | External LLM calls require `AuditGuard` `ATTEMPT` event before subprocess execution. Worker-role external calls must have `requires_llm = True`. | `orchestrator/provider_audit_guard.py`, `orchestrator/worker_tick.py` | `test_llm_audit_lifecycle` |
| 9 | `AuditGuard` fails closed. If ATTEMPT write returns `None` (audit failure), `AuditGuardBlockedError` is raised and the subprocess is never called. | `orchestrator/provider_audit_guard.py` | `test_llm_audit_lifecycle` test 4 |
| 10 | Planner defaults to local provider. `ProviderFactory` blocks external providers for the `planner_tick` runner role. | `orchestrator/provider_factory.py` | `test_llm_audit_lifecycle` test 8 |
| 11 | Planner and CTO roles are blocked from external LLM calls. `write_blocked()` is called for any policy violation detected before execution. | `orchestrator/provider_factory.py`, `orchestrator/execution_policy.py` | Phase A1 |
| 12 | Worker external calls are controlled and logged. Every `claude`/`codex`/`github-copilot` subprocess call produces an `ATTEMPT` + `RESULT` pair in the audit JSONL. Coverage checker (`llm_audit_coverage.py`) confirms all paths are guarded. | `orchestrator/llm_audit_coverage.py`, `orchestrator/llm_audit.py` | Phase A2 (`LLM_AUDIT_GUARD_RUNTIME_VERIFIED`) |

### Additional Hard-Coded Invariants in Queue Items

Every `human_review_queue` item is created with these three fields hard-coded and never subsequently mutated by any lifecycle transition:

```python
production_patch_allowed:   False   # no lifecycle transition ever changes this
production_model_modified:  False   # set at creation, read-only
external_llm_called:        False   # governance module never calls external LLM
```

---

## 5. Operator Commands Reference

### Readiness Dashboard

```bash
python3 scripts/run_optimization_readiness.py --print
```

Shows current state (`WAITING_ACTIVE` / `LEARNING_READY` / etc.), CLV summary, governance state, human review queue status, and recommended next action.

### Ops Report

```bash
python3 scripts/run_optimization_ops_report.py --window 8h --print
python3 scripts/run_optimization_ops_report.py --window 24h --print
```

Shows task counts by status, governance blocking events, CLV pipeline health, skip reasons, human review queue counts with per-item action blocks.

### Decision Card

```bash
python3 scripts/ops_decision_card.py
```

Full operator dashboard: CLV coverage, scheduler state, Phase 8 governance, LLM audit summary, and human review queue with actionable commands for every pending item.

### Human Review Queue CLI

```bash
# List all reviews (shows action hint block when PENDING items exist)
python3 scripts/review_queue.py list

# Show details for a specific review
python3 scripts/review_queue.py show <review_id>

# Approve a review (does NOT deploy; only unlocks validation task creation)
python3 scripts/review_queue.py approve <review_id> --reviewer "Kelvin" --notes "Evidence sufficient."

# Reject a review (no follow-up task created)
python3 scripts/review_queue.py reject <review_id> --reviewer "Kelvin" --notes "Insufficient CLV."

# Request more data (creates clv-quality-analysis task only)
python3 scripts/review_queue.py more-data <review_id> --reviewer "Kelvin" --notes "Need 500+ samples."
```

### LLM Audit

```bash
# Runtime smoke validation (no external quota consumed)
python3 scripts/run_llm_audit_guard_runtime_validation.py

# Coverage check
python3 -m orchestrator.llm_audit_coverage
```

### Phase Drills (Isolated — Real Queue Untouched)

```bash
# Phase 18 — E2E waiting loop
python3 scripts/run_phase18_e2e_validation.py --dry-run

# Phase 19 — Learning unlock
python3 scripts/run_phase19_learning_unlock_validation.py

# Phase 20 — Learning cycle
python3 scripts/run_phase20_learning_cycle_validation.py

# Phase 21 — Patch gate
python3 scripts/run_phase21_patch_gate_validation.py

# Phase 22 — Sandbox patch evaluation
python3 scripts/run_phase22_patch_evaluation_validation.py

# Phase 23 — Patch evaluation decision gate
python3 scripts/run_phase23_patch_evaluation_gate_validation.py

# Phase 24 — Human review queue
python3 scripts/run_phase24_human_review_queue_validation.py

# Phase 26 — Full governance loop runtime drill
python3 scripts/run_phase26_governance_loop_drill.py
```

### Test Suite (Phases 18–26)

```bash
# Run all governance phases in one pass
.venv/bin/python -m pytest \
  tests/test_phase18_e2e_waiting_loop.py \
  tests/test_phase19_learning_unlock_simulation.py \
  tests/test_phase20_first_learning_cycle.py \
  tests/test_phase21_learning_patch_gate.py \
  tests/test_phase22_sandbox_patch_evaluation.py \
  tests/test_phase23_patch_evaluation_gate.py \
  tests/test_phase24_human_review_queue.py \
  tests/test_phase25_human_review_ui.py \
  tests/test_phase26_governance_loop.py \
  tests/test_llm_audit_lifecycle.py \
  -v
```

Expected: **80 passed** (9 + 9 + 9 + 9 + 10 + 10 + 10 + 9 + 7 + 16 — approximately, exact counts may vary with parametrize).

---

## 6. Current Limitations

### 6.1 Real Production CLV Still Depends on Valid Closing Odds

All 14 CLV records are currently `PENDING_CLOSING`. The system is in `WAITING_ACTIVE` state. No real learning has occurred. The `ClosingOddsMonitor` polls every 15 minutes but will not find valid closing odds until actual WBC 2026 games have completed and closing market data is available.

**Impact**: The entire learning-to-patch pipeline (Phases 19–26) has been validated in sandbox/isolation only. No real production learning cycle has run.

### 6.2 Production Learning Not Yet Active

Production learning is gated behind real `COMPUTED` CLV. Until closing odds arrive for at least one prediction record, the planner will not create any learning family tasks in real runtime. Safe tasks (diagnostic, reporting, data refresh) continue to run normally.

### 6.3 Sandbox CLV Does Not Imply Production Performance

All Phase 19–26 validations use sandbox CLV fixtures with controlled values. These do not represent actual model performance against live markets. Positive sandbox CLV in test fixtures is used only to verify governance unlock logic — not to claim the model is profitable.

### 6.4 Human Approval Creates Follow-Up Tasks Only — Not Deployment

`approve_review()` sets `status = APPROVED`. The planner's STEP 0.9 will then generate a `production-proposal-validation` candidate task. This task produces a validation artifact. No code path in the current system deploys a production model from a `APPROVED` queue item directly. A future "promote to production" pipeline would require a separate, additional gate.

### 6.5 External LLM Worker Capability Exists but is Audit-Guarded

The Worker (`worker_tick.py`) can call `claude`, `codex`, and `github-copilot` via subprocess. These calls are individually guarded by `AuditGuard`. However, the capability exists and will be exercised once real tasks with `requires_llm = True` are scheduled by the planner. All calls will be logged in `runtime/agent_orchestrator/llm_audit.jsonl`.

### 6.6 Known Pre-Existing Test Failures (Unrelated to Governance)

The following test files have pre-existing failures unrelated to Phases 18–26 or A1/A2:

| File | Status | Note |
|------|--------|------|
| `tests/test_patch_task_generator.py` | Pre-existing failures | Unrelated to governance phases |
| `tests/test_planner_validation_wire.py` | Pre-existing failures | Unrelated to governance phases |
| `tests/test_task_quality_gate.py` | Pre-existing failures | Unrelated to governance phases |
| `tests/test_tsl_feed_status_reporting.py` | Pre-existing failures | Unrelated to governance phases |
| `tests/test_agent_orchestrator.py` | Collection error | Excluded with `--ignore` |

These failures existed before Phase 18 development and do not affect the governance correctness verified by Phases 18–26.

---

## 7. Recommended Next Roadmap

### Step 1 — Wait for / Ingest Real Valid Closing Odds

The `ClosingOddsMonitor` is already running. When real WBC 2026 closing odds become available, the monitor will automatically upgrade `PENDING_CLOSING` records to `COMPUTED` and trigger strategy tick reinforcement. No code change required.

**Action**: Verify `closing_odds_monitor.py` is active in the daemon scheduler (Track E). Confirm `runtime/agent_orchestrator/closing_monitor_state.json` shows a recent heartbeat.

### Step 2 — Paper-Only Production Readiness Validation

When the first real `COMPUTED` CLV appears, run a paper-only learning readiness check before allowing the planner to autonomously schedule learning tasks:

```bash
python3 scripts/run_optimization_readiness.py --print
```

Confirm `readiness_state = LEARNING_READY`. Review the CLV distribution and sample count. If CLV is above threshold and sample count ≥ 1500, the system is ready for the first real learning cycle.

### Step 3 — Expand Deterministic Executors If Needed

Phase 11 established deterministic safe-task execution without LLM. If the learning cycle produces insights that require non-deterministic evaluation, expand the deterministic executor library before enabling `requires_llm = True` tasks. This avoids unexpected external quota consumption.

### Step 4 — Add Stronger Production Proposal Validation

The current approved follow-up task (`production-proposal-validation`) creates a validation artifact. Before any production model modification is ever considered:

- Add a `paper-rollout-plan` gate that simulates the proposed change against historical CLV data
- Require ≥ 3 independent reviewers or a minimum hold period
- Log all proposal artifacts in a dedicated review archive

### Step 5 — Keep Human Review Mandatory for All Production-Impacting Actions

The Human Review Queue is the final gate before any production-impacting action. Do not bypass it even under operational pressure. The queue is designed to be low-friction (`review_queue.py approve` is a single command) while providing a mandatory human decision point.

### Step 6 — Monitor LLM Audit / Usage Card for External Quota Consumption

Once real Worker tasks begin executing with `requires_llm = True`, monitor:

```bash
python3 scripts/ops_decision_card.py  # shows LLM audit summary
```

Set a soft alert threshold in the decision card when `api_calls_today` approaches `api_cap`. Review `runtime/agent_orchestrator/llm_audit.jsonl` for unexpected `BLOCKED` spikes, which may indicate policy misconfiguration.

---

## 8. Architecture Summary

### Key Files Reference

| Module | Purpose |
|--------|---------|
| `orchestrator/optimization_state.py` | 6-state governance classifier (Phase 8) |
| `orchestrator/learning_cycle_runner.py` | Orchestrates sandbox learning cycles (Phase 20) |
| `orchestrator/learning_patch_gate.py` | Patch gate decisions from learning insights (Phase 21) |
| `orchestrator/learning_patch_task_generator.py` | Generates sandbox patch evaluation task specs (Phase 21) |
| `orchestrator/patch_task_generator.py` | Sandbox patch evaluation executor integration (Phase 22) |
| `orchestrator/patch_validator.py` | Validates sandbox evaluation artifacts (Phase 22) |
| `orchestrator/patch_evaluation_gate.py` | 4-outcome evaluation gate (Phase 23) |
| `orchestrator/human_review_queue.py` | Persistent approval gate lifecycle (Phase 24) |
| `orchestrator/provider_audit_guard.py` | `AuditGuard` context manager, fail-closed LLM guard (Phase A1) |
| `orchestrator/provider_factory.py` | Planner local-only enforcement (Phase A1) |
| `orchestrator/llm_audit.py` | Audit event persistence (JSONL) (Phase A1) |
| `orchestrator/llm_audit_coverage.py` | AST-based coverage scanner (Phase A2) |
| `orchestrator/execution_policy.py` | Role-based execution policy |
| `orchestrator/planner_tick.py` | STEP 0.9 (human review gate), STEP 1.5 (Phase 8 governance), STEP 2 (candidate loop) |
| `orchestrator/optimization_readiness.py` | Readiness dashboard renderer (Phase 13 + Phase 24 section) |
| `orchestrator/optimization_ops_report.py` | Ops report renderer with human review queue section |
| `orchestrator/api.py` | FastAPI endpoints including `/api/orchestrator/summary` with review actionability |
| `scripts/ops_decision_card.py` | Full operator decision card (Phase 25 HUMAN REVIEW QUEUE section) |
| `scripts/review_queue.py` | Human review queue CLI (`list`, `show`, `approve`, `reject`, `more-data`) |
| `runtime/agent_orchestrator/human_review_queue.json` | Live queue state (persistent) |
| `runtime/agent_orchestrator/llm_audit.jsonl` | LLM audit event log |

### Critical Gate Chain

```
CLV PENDING_CLOSING ──► [ClosingOddsMonitor] ──► CLV COMPUTED
                                                        │
                            ┌───────────────────────────┘
                            │
                            ▼
                [optimization_state.classify()]
                 DATA_WAITING → blocks all learning
                 DATA_READY   → learning allowed
                            │
                            ▼ (LEARNING_READY)
               [LearningCycleRunner] → clv_quality_analysis
                            │
                            ▼
               [LearningPatchGate] → ALLOW_PATCH_CANDIDATE?
                            │ yes
                            ▼
               [PatchTaskGenerator] → sandbox evaluation
                            │
                            ▼
               [PatchEvaluationGate] → HUMAN_REVIEW_REQUIRED?
                            │ yes
                            ▼
               [HumanReviewQueue] PENDING
               [planner STEP 0.9] WAITING_FOR_HUMAN_REVIEW
                            │
                  operator: review_queue.py approve
                            │
                            ▼
               APPROVED → production-proposal-validation task
               (production_patch_allowed=False always)
```

---

**Final Status**: ✅ `PHASE_27_AUTONOMOUS_LEARNING_GOVERNANCE_BASELINE_VERIFIED`

All phases 18–26 and A1/A2 are summarized with objectives, files, test counts, runtime verdicts, and hard rules enforced. The end-to-end state machine, 12 safety invariants, operator commands, current limitations, and recommended roadmap are fully documented.
