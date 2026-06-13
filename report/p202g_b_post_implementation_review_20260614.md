# P202G-B Post-Implementation Review and Commit-Readiness Audit

Date: 2026-06-14

Final classification:
`P202G_B_POST_IMPLEMENTATION_REVIEW_NEEDS_SMALL_FIX`

## 1. Governance and Phase 0

All required governance and evidence files were read. Governance remains stale:
`CURRENT_STATE.md` records an older HEAD and `active_task.md` remains P199
`AUTHORIZED_PLAN_ONLY`. It does not authorize a competing implementation.
The explicit review-only prompt controlled this audit; no governance file was
modified.

Phase 0 passed:

- repo: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- branch / symbolic HEAD: `main` / `main`
- git-dir: `.git`
- local HEAD: `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`
- `origin/main`: `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`
- expected baseline ancestor: PASS
- open PR count: 0
- staged files: none
- Python: 3.13.8
- all four P202G-B files: present and untracked
- P202D/P202E source files: unchanged
- real pitcher-event/probable-starter runtime paths: absent

Dirty state was limited to the task-authorized P202G-B files, tolerated
runtime/data files, authorized governance files, bootstrap files, and excluded
earlier reports. No STOP condition was triggered.

## 2. Full File Review

The following files were read directly in full:

- `data/mlb_pitcher_game_events.py`
- `tests/test_mlb_pitcher_game_events.py`
- `tests/fixtures/mlb_pitcher_game_event_fixtures.json`
- `report/p202g_b_pitcher_event_backfill_skeleton_20260614.md`

The implementation is pure stdlib, import-side-effect free, fixture-only, and
isolated from runtime prediction, recommendation, evaluation, scheduler,
provider, model, and DB paths.

One commit-readiness defect was independently reproduced:

> A corrected payload that reorders the pitcher list changes
> `appearance_sequence` and the generated `source_record_id`. Selection then
> treats the old and corrected rows as two different appearances and returns
> both instead of resolving one revision.

Observed reproduction for one pitcher:

```text
status=ok
[(sequence=1, status=final, K=8),
 (sequence=2, status=corrected, K=9)]
```

This contradicts the report claim that a later correction replaces the earlier
row deterministically.

## 3. Source-Shape Grounding

Grounding result: PASS WITH EXPLICIT SYNTHETIC EXTENSIONS.

Existing evidence directly supports:

- `teams.{home,away}.pitchers`
- `teams.{home,away}.players.ID{id}.person.{id,fullName}`
- `stats.pitching.inningsPitched`
- `stats.pitching.numberOfPitches`
- `stats.pitching.strikes`
- pitcher-list ordering and side ordering
- fixture-level `game_pk` metadata

Synthetic decoded-contract extensions include:

- K / BB / HBP / HR / BF / hits / ER / runs
- explicit `starterFlag`
- team IDs in the decoded envelope
- game start/finalization and collection timestamps
- record status and source provenance

Those extensions are reasonable future decoded-input requirements. The
implementation report correctly says the older Phase62 fixture does not supply
the complete contract and makes no real-season completeness claim.

Existing Phase58 schedule fallback is estimated/averaged and is rejected.
Phase63 output is fixture-only. `data/mlb_context/bullpen_usage_3d.jsonl`
contains 2,429 team-level aggregate rows, not pitcher-game observations. The
implementation report says 2,430, which is a small documentation error and not
the commit-readiness blocker.

## 4. Exact Schema Review

Schema result: PASS.

`EVENT_FIELDS` contains exactly the intended 34 fields. Normalized output:

- fixes `diagnostic_only=true`
- fixes `production_ready=false`
- rejects unknown normalized fields
- rejects `learning_eligible`
- requires game, pitcher, team/opponent, side, and appearance identity
- requires explicit `starter_flag`
- permits normalized `final`, `corrected`, and `superseded`
- keeps `malformed` and `source_unavailable` as diagnostic-only states

Odds, recommendation, winner, settlement, and named model-output fields cannot
enter a normalized record.

Historical pitcher performance fields are valid prior-game observations.
They are distinct from prohibited target-game winner/score/settlement/model
fields and are eligible only through the later cutoff gate.

## 5. Innings and Statistical Semantics

Result: PASS.

- `X.0 -> 3X`
- `X.1 -> 3X+1`
- `X.2 -> 3X+2`
- `.3`, floats, annotations, signs, and malformed displays are rejected
- display and canonical outs must agree
- zero-out appearances are valid
- observed counts must be non-negative integers
- K / BB / HBP / HR are mandatory
- `earned_runs <= runs_allowed`
- `strikes <= pitches_thrown`
- pitch count and strikes must both be present or both null
- no appearance statistic is estimated or inferred

The stored fields are sufficient for a later FIP calculation, but this module
correctly performs no FIP calculation.

## 6. Identity and Appearance Semantics

Game, pitcher, team, side, doubleheader, and explicit-role behavior is mostly
coherent:

- `game_pk` is canonical
- pitcher ID is mandatory and never inferred from name
- team and opponent must differ
- home/away is explicit
- doubleheaders remain separate by `game_pk`
- duplicate pitcher IDs in one decoded side are rejected
- direct normalized input can represent distinct repeated appearances through
  distinct sequences

Commit-readiness blocker:

- Adapter sequence is assigned from current pitcher-list order.
- Adapter `source_record_id` embeds that sequence.
- Revision grouping is `(game_pk, pitcher_id, appearance_sequence)`.
- A corrected source reorder therefore changes both source and revision
  identity, leaving the original row active and adding a second appearance.

The current key is insufficient unless the decoder guarantees immutable
appearance order across all corrections. No such guarantee is documented or
validated.

Secondary non-blocking observation: a side with two explicit
`starterFlag=true` rows is accepted. The contract requires explicit role
metadata but does not enforce side-level role consistency.

## 7. Fingerprint, Deduplication, and Store

Result: PASS WITH DOCUMENTED LIMITATIONS.

- canonical sorted compact JSON is used
- SHA-256 is deterministic and key-order independent
- all normalized semantic fields except the fingerprint itself are included
- a supplied stale fingerprint is recalculated and rejected
- exact duplicates are no-ops
- changed status/stat/time appends
- malformed JSONL, field sets, and fingerprints fail closed before append
- caller path is mandatory
- parent creation is not implicit
- UTF-8 JSONL is used
- tests write only under `tmp_path`
- no concurrency-safety claim is made

Because collection time is fingerprinted and included in the dedup key,
identical source content collected later appends another revision. This is
consistent with preserving observation history and is honestly implied by the
report, although it may increase storage volume.

The store uses physical append rather than atomic replacement or locking.
That is acceptable for this fixture skeleton because no concurrency claim is
made.

## 8. Adapter and Diagnostics

Result: PASS WITH BOUNDED INPUT EXPECTATION.

The adapter:

- performs no network or file I/O
- requires explicit collection/provenance/parser arguments
- accepts only final/completed/game-over source games
- supports corrected/superseded revisions
- rejects live/provisional/cancelled games
- rejects aggregate-only, proxy, estimated, and incomplete sources
- reports deterministic diagnostic codes and record counts
- preserves game, home/away, and pitcher-list order
- does not infer IDs or stats

Malformed pitchers can coexist with accepted rows, but accepted/rejected counts
and diagnostics expose that partial result. Callers must not interpret
`accepted_records > 0` as whole-game completeness.

Outcome-field behavior is intentionally mixed:

- generic nested `teams.home.score` is ignored and not normalized
- explicit `homeScore` or `winner` fields reject the whole payload

This is acceptable only for an explicitly minimized decoded payload, as the
module/report state. It is not a drop-in adapter for every raw finalized
boxscore envelope.

## 9. Temporal and Prior-Only Semantics

Result: STRICT PIT SAFETY PASS.

Selection requires:

```text
game_start_utc < target_information_cutoff_utc
game_finalized_at_utc <= target_information_cutoff_utc
collected_at_utc <= target_information_cutoff_utc
```

Independent scenario results:

| Scenario | Result |
|---|---|
| A. Finalized and collected before later cutoff | eligible |
| B. 2024 event collected in 2026, target cutoff in 2025 | excluded |
| C. Same row, cutoff after its 2026 collection | eligible |
| D. Correction collected after cutoff | earlier known final selected |
| E. Latest known revision is superseded | appearance excluded |
| F. Differing latest revisions at same collection time | fail closed |
| G. Target `game_pk` | excluded |
| H. Game start at/after cutoff | excluded |

The collected-at gate is intentional in code and documented as a selection
rule. It correctly prevents retrospective rows from masquerading as
contemporaneously available evidence.

Consequences:

- The module is useful today as an observational pitcher-game SSOT.
- A post-hoc historical backfill cannot support leakage-free evaluation at an
  earlier historical cutoff merely because the game finalized then.
- The same rows can be used for targets after their actual collection time,
  subject to the other gates.
- Legitimate historical PIT eligibility would require trustworthy source
  archive evidence such as `source_published_at_utc`,
  `source_effective_at_utc`, or an archive-availability timestamp.
- Such availability must not be inferred from `game_finalized_at_utc` alone.

The implementation report states the collected-at rule but does not explicitly
spell out this post-hoc limitation. The name "backfill skeleton" is accurate
for observational storage but overstates support for historical PIT
backtesting.

No weakening of the collected-at rule is recommended.

## 10. Correction and Superseded Behavior

Normal as-of behavior passes:

- corrections append
- later corrections do not rewrite earlier cutoff knowledge
- superseded latest revisions are excluded
- same-time differing corrections fail closed

However, those guarantees only hold while appearance sequence remains stable.
The reproduced reorder case silently bypasses revision resolution. This is the
single blocker.

Smallest fix:

1. Define a stable source appearance identity that does not change merely
   because pitcher-list order changes.
2. Group revisions by that stable identity, with game/pitcher/source guards.
3. Preserve `appearance_sequence` as observed ordering metadata.
4. Fail closed when one correction cannot be mapped unambiguously.
5. Add tests for reordered corrections and genuine repeated appearances.

## 11. No-Network and Integration Boundary

Result: PASS.

AST inspection found only:

- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `pathlib`
- `typing`

There are no network clients, StatsAPI calls, acquisition imports, dynamic
imports, `eval`, `exec`, module-level calls, DB clients, scheduler hooks,
probable-starter integration, recommendation/evaluator/model imports, default
runtime paths, or import-time writes.

## 12. Fixture and Test-Quality Review

The 103 direct tests are generally meaningful and cover the reported schema,
time, innings, statistics, adapter, store, correction, superseded, target,
future, and no-network boundaries.

Gaps:

- no corrected-pitcher-list reorder regression
- no explicit 2024/2026 post-hoc backfill test, although
  `test_late_collection_is_excluded` proves the same gate generically
- no side-level multiple-starter consistency test
- no actual import-in-a-clean-directory side-effect test; current no-network
  checks are largely static

The fixture catalog contains 34 scenario names, but several scenarios are
constructed directly in tests rather than represented by standalone payloads.
This is acceptable, though the catalog should not be interpreted as 34 full
fixture payloads.

One weak test is the stake-independence loop, which mostly confirms that stake
is absent and repeated selection is deterministic. It does not affect core
coverage.

## 13. Independent Validation

| Validation | Result |
|---|---|
| P202G-B direct suite | PASS, 103 |
| P202E collector | PASS, 49 |
| P202D snapshot intake | PASS, 89 |
| Workflow guards | PASS, 157 |
| Combined relevant suites | PASS, 398 |
| Required compile | PASS |
| `git diff --check` | PASS |

The passing suite does not cover the independently reproduced reorder defect.

## 14. Full Regression Status

Full repository regression: NOT RUN.

The direct and mandated 398-test combined set was proportional for this
isolated uncommitted module. The blocker is deterministic and does not require
a full regression to establish.

## 15. Side-Effect Verification

Post-test state matched pre-test state except for this authorized review report:

- no staged files
- HEAD unchanged
- P202D/P202E unchanged
- no pitcher-event runtime directory
- no probable-starter runtime directory
- no stray JSONL output
- tests used `tmp_path`
- no network/API call
- no DB/provider/production/registry/model/strategy mutation

## 16. Risks and Limitations

1. Revision identity is unstable under corrected source reordering. Blocking.
2. Post-hoc backfill is observational, not historical-PIT eligible before its
   real collection timestamp. Safe but insufficiently explicit in the
   implementation report.
3. Complete FIP and explicit role/provenance fields are decoded-contract
   requirements, not proven existing real-source availability.
4. Raw finalized envelopes may require minimization before adaptation.
5. Side-level starter-role consistency is not enforced.
6. Store append is not atomic/concurrency-safe and makes no such claim.
7. The implementation report's aggregate row count is off by one: actual
   `bullpen_usage_3d.jsonl` line count is 2,429.

## 17. Commit-Readiness Decision

Commit-readiness classification:

`NEEDS_SMALL_FIX_BEFORE_COMMIT`

Packaging is not allowed yet.

Single blocker:

`UNSTABLE_APPEARANCE_REVISION_IDENTITY_ON_CORRECTED_PITCHER_REORDER`

Recommended narrow next worker:

- modify only the P202G-B module, tests, fixture if needed, and implementation
  report
- establish stable correction identity independent of current list position
- add reordered-correction and ambiguous-repeat tests
- retain strict collected-at PIT gating
- update the report with explicit post-hoc backfill limitations

## 18. Required Completion Check

| Item | Result |
|---|---|
| 是否真的完成 | YES, independent review complete |
| Test result | PASS |
| P202G-B direct test count | 103 |
| P202E test count | 49 |
| P202D test count | 89 |
| Workflow test count | 157 |
| Combined relevant test count | 398 |
| Full regression | NOT RUN |
| Commit-readiness classification | NEEDS_SMALL_FIX_BEFORE_COMMIT |
| Source-shape evidence | GROUNDED, WITH SYNTHETIC DECODED EXTENSIONS |
| Pitcher-event schema | PASS, EXACTLY 34 FIELDS |
| Innings validation | PASS |
| FIP-component status | PASS, K/BB/HBP/HR REQUIRED |
| Proxy/aggregate rejection | PASS |
| Adapter diagnostics | PASS |
| Identity/appearance status | FAIL ON CORRECTED LIST REORDER |
| Idempotency | PASS |
| Revision history | APPEND PASS; REVISION LINKAGE NEEDS FIX |
| Append-only | PASS, NON-CONCURRENT SKELETON |
| Prior-only selection | TEMPORAL GATES PASS |
| Post-hoc backfill PIT | EXCLUDED BEFORE ACTUAL COLLECTION; OBSERVATIONAL ONLY |
| Correction as-of cutoff | PASS WHEN APPEARANCE IDENTITY IS STABLE |
| Target-game exclusion | PASS |
| Future-game exclusion | PASS |
| Actual target-outcome leakage | NO NORMALIZED TARGET OUTCOME; PRIOR OBSERVATIONS ONLY |
| No-network | PASS |
| Persistent runtime write | NONE |
| Single remaining blocker | UNSTABLE APPEARANCE REVISION IDENTITY |
| Modified files by review | `report/p202g_b_post_implementation_review_20260614.md` only |
| Original P202G-B untracked files | 4 |
| Staged files | NONE |
| Current branch | `main` |
| Local HEAD | `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9` |
| origin/main HEAD | `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9` |
| Open PR count | 0 |
| `active_task.md` | STALE P199 PLAN-ONLY; NO COMPETING IMPLEMENTATION |
| P202D/P202E unchanged | PASS |
| DB/API/provider/production/registry/controlled_apply | NONE |
| Model/strategy/champion mutation | NONE |
| Commit/push | NONE / NONE |
| Whether packaging is allowed | NO, APPLY NARROW FIX FIRST |
| Whether next round is allowed | YES, NARROW P202G-B FIX ONLY |
| Worker model recommendation | OPUS-CLASS |
| Thinking level recommendation | STRONG |
| Continue same conversation | NEW CONVERSATION RECOMMENDED |
| Final Classification | `P202G_B_POST_IMPLEMENTATION_REVIEW_NEEDS_SMALL_FIX` |

### CTO Conclusion

The strict collected-at gate is correct and prevents retrospective leakage; it
must remain unchanged. The implementation is otherwise coherent, no-network,
and well tested, but correction identity depends on mutable pitcher-list order.
A reordered correction can cause one pitcher-game to be selected twice.
Commit packaging should wait for a narrow stable-identity fix and regression
test.

### CEO Conclusion

This local skeleton safely stores completed pitcher observations without
pretending late-collected history was known earlier. It is not yet ready to
package because an official correction that changes ordering can duplicate one
pitcher's appearance during selection. The required repair is small and
contained; no live data, betting, model, or production work is involved.
Historical backfill remains useful for observation, but not for earlier
point-in-time evaluation unless trustworthy archive-availability evidence is
added later.
