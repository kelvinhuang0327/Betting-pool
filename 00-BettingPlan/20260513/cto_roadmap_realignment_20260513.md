# CTO Roadmap Realignment — 2026-05-13
## MLB Betting Prediction Platform: Honest Status Reset

**Date**: 2026-05-13
**Author**: Transition Agent (P30→P31)
**Version**: v3 (supersedes v2 from 2026-05-12)
**Scope**: MLB prediction pipeline, PAPER_ONLY mode
**PAPER_ONLY**: True
**production_ready**: False

---

## Executive Summary

The roadmap has drifted. Three honest findings require a reset:

1. **P28 + P29 confirmed a hard sample wall**: Only 324 active entries exist.
   No policy combination reaches the 1,500-entry model training threshold with
   current data. This wall was known but the subsequent P30 plan did not
   acknowledge it as a fundamental blocker.

2. **P30 "READY" is misleading nomenclature**: The P30 contract accepted
   `n_ready_sources=348` as the gate. However, the majority of those 348
   sources are derived pipeline outputs in `outputs/` — not new raw historical
   data. The plan is technically correct by its own contract but does not
   advance the real goal of increasing model training samples.

3. **The roadmap has entered an "auditing the audit" loop**: P28 audited P27,
   P29 audited P28's density, P30 planned acquisition of sources already known
   to be derived. P31 must end this loop with an honest classification and a
   binary acquisition decision.

This document resets the roadmap with an honest P0–P10 ordering and a clear
statement of the single highest-leverage action.

---

## Section 1 — Acknowledged Issues

### 1.1 P28/P29 Sample Wall (324 < 1,500) — HARD BLOCKER

| Metric | Measured value |
|--------|---------------|
| Active entries (P28 audit) | 324 |
| Training threshold (minimum viable) | 1,500 |
| Gap | −1,176 |
| Any current policy combination that reaches 1,500 | **None** |

**Impact**: Model training with OOF cross-validation cannot be statistically
validated below 1,500 entries. All model quality metrics from P28 onward are
computed on insufficient sample. They should be treated as INDICATIVE only,
not as production-grade estimates.

**Resolution path**: 2024 MLB full-season ingestion (P32). If 2024 provides
~2,430 regular-season games, combined with existing 324 entries, it pushes
active entries to ~2,750+ (pending schema validation).

### 1.2 P30 "READY" Misleading Nomenclature — FLAGGED

| P30 metric | Reported | Reality |
|------------|----------|---------|
| `n_ready_sources` | 348 | Majority are DERIVED_OUTPUT, not raw historical |
| `expected_sample_gain` | 54,675 | Theoretical upper bound; 0 delivered |
| Gate outcome | READY | Should be READY_WITH_CAVEAT |

**Remediation**: P31 will produce an honest source classification that
separates `RAW_PRIMARY + RAW_SECONDARY` from `DERIVED_OUTPUT`. The P30 report
must be retroactively annotated.

### 1.3 "Auditing the Audit" Pattern — TERMINATED

The following phases were meta-audits that did not advance training data:
- P28: Audit of P27 backfill stability → valuable, but revealed sample wall
- P29: Density expansion of P28 audit → confirmed wall, no new data
- P30: Acquisition plan for sources already known to be derived → not advancing

P31 is the final meta step. After P31 issues GO/NO-GO, P32 must execute
or the project acknowledges an irresolvable data deficit.

---

## Section 2 — Corrected P0–P10 Priority Ordering

| Priority | Phase | Title | Status |
|----------|-------|-------|--------|
| **P0** | P30 | Commit Recovery | ✅ DONE (this session) |
| **P1** | P31 | Honest Data Reality Audit & 2024 Acquisition Gate | 🔲 PLANNING (this session) |
| **P2** | P32 | 2024 Historical Game Logs + Closing Odds Ingestion | 🔲 BLOCKED on P31 GO decision |
| **P3** | P33 | Model Quality Improvement (OOF BSS +0.020 target) | 🔲 BLOCKED on P32 sample unlock |
| **P4** | P34 | Strategy Optimization Hardening (deep P18 sweeps) | 🔲 BLOCKED on P33 |
| **P5** | P35 | P28 Re-audit Pass (1,500 active entries unlock) | 🔲 BLOCKED on P32 |
| **P6** | P36 | P17 Ledger Settlement Closure | 🔲 Independent; can run parallel to P32 |
| **P7** | P37 | TSL Market Expansion (run line + totals) | 🔲 BLOCKED on P33 |
| **P8** | P38 | Live TSL Snapshot Bridge (PAPER snapshot, no orders) | 🔲 BLOCKED on P35 |
| **P9** | P39 | Daily Ops & Drift Monitoring | 🔲 BLOCKED on P38 |
| **P10** | P40 | Production Proposal Gate | 🔲 BLOCKED on ALL of above |

### Critical Blocker Chain

```
P31 (Audit Decision)
  └── P32 (2024 Ingestion)  ← HIGHEST LEVERAGE
        └── P35 (Re-audit: 1500 unlock)
        └── P33 (Model Quality)
              └── P34 (Strategy Hardening)
              └── P37 (Market Expansion)
                    └── P38 (PAPER Snapshot)
                          └── P39 (Daily Ops)
                                └── P40 (Production Gate)
```

**P36 (Ledger Settlement)** is independent and can run in parallel with P32.

---

## Section 3 — Explicit Critical Blockers

The following are hard blockers that prevent production readiness:

### BLOCKER-1: No Raw 2024 Historical Data (CRITICAL — blocks P33–P40)
- **Status**: Unresolved
- **Detail**: Zero 2024 MLB game records exist in `data/` as RAW_PRIMARY or
  RAW_SECONDARY. The 348 "ready" P30 sources are derived outputs.
- **Resolution**: P31 GO decision → P32 ingestion

### BLOCKER-2: Sample Wall 324 < 1,500 (CRITICAL — model metrics unreliable)
- **Status**: Confirmed by P28 + P29
- **Detail**: OOF BSS, AUC, and Kelly metrics computed on 324 entries are
  statistically insufficient for deployment confidence.
- **Resolution**: P32 ingestion expected to unlock 2,430+ new entries

### BLOCKER-3: Closing Odds Provenance Unresolved (HIGH — may block P32)
- **Status**: Unknown
- **Detail**: No licensed provider identified for 2024 closing moneyline odds.
  Retrosheet provides game outcomes but not odds.
- **Resolution**: P31 audit must evaluate The Odds API, Pinnacle, or alternative

### BLOCKER-4: P17 Ledger Not Settled (MEDIUM — independent)
- **Status**: Open from P36 scope
- **Detail**: PAPER bets from P17 cycles have open ledger entries not
  reconciled against final game outcomes.
- **Resolution**: P36 can run independently; does not block P32–P35

### BLOCKER-5: TSL Production Bridge Not Built (LOW — far future)
- **Status**: Deferred to P38
- **Detail**: No PAPER-mode TSL snapshot ingestion pipeline exists.
  This is intentionally deferred until model quality is validated.
- **Resolution**: P38, gated on P35

---

## Section 4 — Highest-Leverage Action Statement

> **P32 — 2024 MLB Historical Ingestion is the single highest-leverage move.**
>
> Without new raw historical data, all model improvements, strategy
> optimizations, and ledger audits are operating on a 324-entry dataset
> that cannot support statistically reliable production claims.
>
> P33 (Model Quality Improvement) is the second highest-leverage action,
> but it cannot execute until P32 provides the sample unlock.
>
> Everything else in the P0–P10 ordering is gated on this foundation.
>
> P36 (Ledger Settlement) is the only work that can proceed in parallel
> without waiting for P32.

---

## Section 5 — P31 Scope Confirmation

P31 is **planning and audit only**. It does not:
- Download any data files
- Build joined input artifacts (old P31 goal, now deprecated)
- Run model training
- Fabricate source paths or counts

P31 produces exactly:
1. Source classification audit (RAW vs DERIVED)
2. Provenance + license documentation for 2024 candidates
3. GO / NO-GO acquisition decision with justification
4. Gate constant: `P31_HONEST_DATA_AUDIT_READY` or a BLOCKED variant

---

## Section 6 — Deprecated Scope Notes

The following were previously listed as P31 goals and are now **deprecated**:

| Old P31 goal | Reason deprecated |
|-------------|------------------|
| Build joined input artifacts from P30 acquisition plan | Presupposed raw data that doesn't exist; moved to P32 |
| Validate n_ready_sources=348 as training-ready | Classification audit in P31 will show majority are derived |
| Execute acquisition dry-run pipeline | Dry-run was done in P30; full run requires P31 GO decision first |

---

## Roadmap Version History

| Version | Date | Key change |
|---------|------|-----------|
| v1 | 2026-05-07 | Initial roadmap after P27 |
| v2 | 2026-05-12 | P30 READY acknowledged; P31 scoped as build step |
| **v3** | **2026-05-13** | **Honest reset: P30 READY caveat, P31 re-scoped as audit, blocker chain corrected** |

---

## Marker

```
CTO_MLB_P30_P31_ROADMAP_REALIGNMENT_20260513_READY
```

CTO_MLB_P30_P31_ROADMAP_REALIGNMENT_20260513_READY
