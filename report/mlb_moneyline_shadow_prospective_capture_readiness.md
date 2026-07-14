# MLB Moneyline Shadow Prospective Capture Readiness

**Status:** `NO_RETROACTIVE_PROSPECTIVE_CAPTURE`

**Scope:** paper-only, diagnostic-only contract readiness. No model performance or betting claim.

## Current Artifact Truthfulness

- P278 remains a retrospective frozen-state paper-only prediction artifact.
- P279 remains an outcome-free divergence baseline, not performance evidence.
- No historical prospective cohort was created and no current artifact was retroactively certified.
- Current retrospective prediction rows: `828`
- Prospective registered rows: `0`
- Explicit prediction-as-of rows: `0`
- Trusted scheduled-start rows: `0`
- Pregame-eligible rows: `0`

## Future Prospective Contract

- Runner available: `True`
- Capture semantics: `LOCAL_OBSERVATION_LOWER_BOUND`
- Pregame boundary: `prediction_as_of_utc < scheduled_start_utc`
- Missing, malformed, inferred, untrusted, equal, or later schedule evidence fails closed.
- Runtime metadata is excluded from deterministic capture hashes.

## Synthetic Verification

- Status: `PASSED`
- Capture ID: `p280a-c46f89e81e82d64bbeb72c0b91b6aaf4580f2e1ab507815eb49c5161541cbcf4`
- Deterministic payload SHA-256: `a3f698b21b990e749515176593c7d048a0960b659876c88cbe21611b578ee361`
- Fixture storage: `TEST_FRAMEWORK_MANAGED_TEMPORARY_ROOTS`
- Canonical future fixture, boundary checks, duplicate conflict, and tamper checks passed.

## Safety

- Model activation: `false`
- Deployment: `false`
- Registry mutation: `false`
- Publication: `false`
- Real betting: `false`
- Readiness deterministic payload SHA-256: `d36f919cb22b16218852dc54cce16f8d76957c400a6cce3f3a07ae71b6a9e5a8`

## Runtime Metadata (Excluded From Deterministic Hash)

- Generated at: `2026-07-14T14:12:33Z`
- Generator source Git commit: `92f7d34bea46dbe7548016aabace04930e091ff0`
