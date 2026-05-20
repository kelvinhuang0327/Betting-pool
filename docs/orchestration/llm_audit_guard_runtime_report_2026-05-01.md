# LLM Audit Guard Runtime Report

**Date**: 2026-05-01  
**Phase**: A2 — Audit Guard Runtime Smoke & Coverage  
**Verdict**: ✅ `LLM_AUDIT_GUARD_RUNTIME_VERIFIED`

---

## 1. Coverage Checker Result

**Tool**: `python3 -m orchestrator.llm_audit_coverage`

```json
{
  "coverage_status": "FULL",
  "covered_paths": [
    "orchestrator/worker_tick.py::execute_task_with_claude [claude] — Claude subprocess guarded by AuditGuard",
    "orchestrator/worker_tick.py::execute_task_with_codex [codex] — Codex subprocess guarded by AuditGuard",
    "orchestrator/copilot_daemon.py::_execute_task [github-copilot] — gh copilot + codex-fallback both audited in _execute_task AuditGuard block"
  ],
  "uncovered_paths": [],
  "excluded_paths": [
    "telegram_bot/bot.py::(openai calls) [openai] — Telegram bot: intentionally excluded — not orchestrator-controlled path"
  ],
  "warnings": []
}
```

All 3 orchestrator-controlled external LLM paths have `AuditGuard` wrapping.  
1 path (Telegram bot OpenAI) intentionally excluded — outside orchestrator control boundary.

---

## 2. Audit Event Counts (at time of report)

No real LLM calls have been made since deployment. Audit JSONL is empty — expected baseline state.

| Event Type       | Count |
|------------------|-------|
| LLM_CALL_ATTEMPT | 0     |
| LLM_CALL_RESULT  | 0     |
| LLM_CALL_BLOCKED | 0     |

**Note**: Counts will populate on first real Worker or Copilot-Daemon execution.

---

## 3. Usage Event Counts (at time of report)

| Window | Total Calls | Blocked |
|--------|-------------|---------|
| today  | 0           | 0       |

---

## 4. Blocked Smoke Result

**Scenario**: Planner role attempts to use `claude` provider.

| Step | Result |
|------|--------|
| `ProviderFactory.assert_role_allowed("planner", "claude")` | ✅ raised `ProviderRoleViolationError` |
| `write_blocked(runner="planner", provider="claude", ...)` | ✅ 1 `LLM_CALL_BLOCKED` record written |
| ATTEMPT events written | ✅ 0 (no external call attempted) |
| subprocess.run called | ✅ NOT called |
| Planner external usage | ✅ 0 |

Outcome: **BLOCKED smoke PASS** — policy enforcement confirmed at both ProviderFactory and audit lifecycle layers.

---

## 5. Allowed Mocked Smoke Result

**Scenario**: Worker executes `execute_task_with_claude` with mocked subprocess (no real Claude).

| Step | Result |
|------|--------|
| subprocess.run called | ✅ exactly 1 time (mock) |
| `LLM_CALL_ATTEMPT` written to audit JSONL | ✅ |
| `LLM_CALL_RESULT` written to audit JSONL | ✅ |
| `correlation_id` matches ATTEMPT→RESULT | ✅ |
| Usage record written to llm_usage.jsonl | ✅ 1 record |
| Worker task `success=True` | ✅ |
| Real external LLM command executed | ✅ NOT executed (mock only) |

Outcome: **ALLOWED mocked smoke PASS** — full audit lifecycle (ATTEMPT→RESULT) verified with zero quota consumption.

---

## 6. Decision Card Evidence

**Command**: `python3 scripts/ops_decision_card.py`

The `🔐 LLM AUDIT 稽核生命週期` section renders correctly:

```
🔐 LLM AUDIT 稽核生命週期
----------------------------------------
今日總事件數  : 0  (ATTEMPT 0 / RESULT 0 / BLOCKED 0)

AuditGuard 覆蓋率  : ✅ FULL  (3 covered / 1 excluded)

========================================
```

- Coverage status is visible at a glance  
- Event counts update from live `llm_audit.jsonl`  
- Recent 5 events displayed when available  
- Role-level breakdown table shown when populated

---

## 7. API Schema Stability

All 4 endpoints verified via direct module import (no HTTP server required):

| Endpoint | Schema Keys | Status |
|----------|------------|--------|
| `GET /api/orchestrator/llm-audit/today` | `date`, `total_events`, `attempts`, `results`, `blocked`, `succeeded`, `failed`, `by_role`, `by_provider` | ✅ STABLE |
| `GET /api/orchestrator/llm-audit/recent` | list of audit event dicts | ✅ STABLE |
| `GET /api/orchestrator/llm-usage/today` | `window`, `total`, `roles`, `warnings`, `recent`, `malformed_count` | ✅ STABLE |
| `GET /api/orchestrator/llm-usage/recent` | same as today schema | ✅ STABLE |

---

## 8. Validation Script

**File**: `scripts/run_llm_audit_guard_runtime_validation.py`

Run: `python3 scripts/run_llm_audit_guard_runtime_validation.py`

Executes 13 checks across 4 categories, exits 0 on full pass:

```
Total: 13  Passed: 13  Failed: 0
✅ LLM_AUDIT_GUARD_RUNTIME_VERIFIED
```

---

## 9. Architecture Summary (Phase A1 + A2)

```
External LLM Request Flow:
─────────────────────────────────────────────────────────────
Planner        → local-only (ProviderFactory blocks external)
                 ↳ write_blocked() if policy violation detected

Worker (Claude) → _assert_llm_execution_allowed()
                  ↳ AuditGuard(runner, provider, task_id) ← ATTEMPT written
                     → subprocess.run(claude ...) ← real call
                  ↳ audit_guard.set_result(success=...)   ← RESULT written
                  ↳ _log_exec_result()                    ← usage written

Worker (Codex)  → same pattern

Copilot-Daemon  → _execute_task()
                  ↳ _execute_with_gh_copilot() + fallback
                  ↳ AuditGuard block (post-execution)     ← ATTEMPT+RESULT
                  run_once() scheduler block:
                  ↳ write_blocked()                       ← BLOCKED

Audit write failure (ATTEMPT returns None):
                  ↳ AuditGuardBlockedError raised
                  ↳ subprocess.run NEVER called (fail-closed)
─────────────────────────────────────────────────────────────
```

---

## 10. Remaining Limitations

| Limitation | Risk | Mitigation |
|-----------|------|------------|
| Telegram bot OpenAI calls not audited | LOW — separate service, no budget control | Documented as intentional exclusion |
| Copilot-Daemon AuditGuard placed post-execution (not pre-subprocess) | MEDIUM — a crash between subprocess and AuditGuard init could lose ATTEMPT | Mitigate: move AuditGuard to pre-execution in future phase |
| AuditGuard only performs AST scan for coverage — dynamic paths not tracked | LOW — all known paths documented | Update `_KNOWN_PATHS` when adding new providers |
| No real-time alerting on `BLOCKED` spike | LOW — visible in Decision Card | Future: add alert threshold to ops_decision_card |

---

**Final Status**: ✅ `LLM_AUDIT_GUARD_RUNTIME_VERIFIED`

All external LLM paths in the orchestrator are guarded. No external quota consumed during validation. Blocked and allowed lifecycle events confirmed via mocked smoke tests.
