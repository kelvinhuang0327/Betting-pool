# P202G-B Cross-Provider / Source-Lineage Fix — Final Independent Re-Review

Date: 2026-06-14

Final classification:
`P202G_B_CROSS_PROVIDER_REREVIEW_READY_FOR_COMMIT_PACKAGING`

> Independent, read-only final re-review of the cross-provider/source-lineage
> fail-closed fix. No implementation, test, fixture, prior report, or governance
> file was modified. Both the original reorder defect and the cross-provider
> silent-overwrite defect are confirmed resolved with no new identity, revision,
> temporal, normalization, or write-boundary regression. The four-file
> implementation is ready for commit packaging together with the three review
> reports (seven files total). The P202F live-transport HOLD is unchanged and is
> not part of this package.

---

## 1. Governance and Phase 0

### Required governance reads

- `SHARED_AGENT_BOOTSTRAP.md`, `TASK_TEMPLATES.md`, `CURRENT_STATE.md`,
  `active_task.md`, `roadmap.md`, `CTO-Analysis.md` — read. Governance remains
  stale: `active_task.md` is still `P199 AUTHORIZED_PLAN_ONLY`;
  `CURRENT_STATE.md` records an older HEAD baseline `2a7aa13…`. Neither
  authorizes a competing implementation. The explicit re-review prompt is the
  controlling authority. No governance file was modified.
- `report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`
  — read. `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`; live transport HOLD.
  Unchanged.
- Skeleton report and both prior P202G-B review reports — read in full.

### Phase 0 actual-state verification

| Check | Observed | Result |
|---|---|---|
| repo top-level | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | PASS |
| branch / symbolic HEAD | `main` / `main` (not detached) | PASS |
| git-dir | `.git` | PASS |
| local HEAD = origin/main | `6de072b…` = `6de072b…` | PASS |
| baseline ancestor | `6de072b…` ancestor of HEAD | PASS |
| open PR count | 0 | PASS |
| staged files | 0 | PASS |
| Python | 3.13.8 | PASS |
| six P202G-B files | present | PASS |
| P202F report | present | PASS |
| P202D/P202E source + tests | present, tracked diff empty | PASS |
| pitcher-event / probable-starter runtime dirs | absent | PASS |
| allowed-write target | absent before this task | PASS |

Dirty/untracked state is confined to tolerated runtime/data files, authorized
governance/bootstrap files, the earlier excluded P19x/P20x reports, P202F, and
the six P202G-B files. No STOP condition triggered.

---

## 2. Source-Lineage Fix Inspection

The current implementation in `data/mlb_pitcher_game_events.py`:

- **`logical_event_key`** (property) = `(game_pk, pitcher_id)` — unchanged.
- **`source_lineage_key`** (new property, lines 168-179) =
  `(source_provider, source_endpoint_or_feed_id)`, drawn only from validated
  normalized fields (both pass `_required_text`, which strips and rejects empty
  values).
- **`select_prior_pitcher_events`** (lines ~893-955): builds `eligible` via the
  strict temporal gates first, then groups by `logical_event_key`, then runs a
  dedicated **cross-source pass** over `sorted(groups)`: if a logical
  pitcher-game has more than one distinct `source_lineage_key`, it returns
  immediately with `status="ambiguous_cross_source_lineage"`, `events=()`, and a
  deterministic diagnostic naming `game_pk` and `pitcher_id` and the sorted
  lineage list. Only if every logical event is single-lineage does the existing
  within-lineage revision resolution run.

Verified invariants:

- lineage comes only from validated normalized fields — yes (`_required_text`).
- revisions are not resolved across lineages — yes (multi-lineage returns before
  revision resolution).
- lineage ambiguity is judged **after** the cutoff/time filter — yes (`eligible`
  is filtered first; the cross-source pass iterates groups built from `eligible`).
- lineage ambiguity is judged **before** within-lineage revision resolution —
  yes (separate earlier loop, immediate return).
- same provider + different feed = different lineage — yes (tuple includes feed).
- same provider + same feed = same lineage — yes.
- no provider precedence — yes (`sorted(...)` is only for determinism; no ranking,
  no preferred name).
- no hardcoded provider name — yes (grep confirms none).
- no matching-fingerprint bypass — yes (identical content across lineages still
  fails closed; fingerprint is never consulted in the cross-source pass).
- no latest-provider-wins — yes (no `max(collected)` across lineages).
- `source_record_id` may repeat across lineages but full source identity is
  lineage-scoped — yes (documented and enforced by the cross-source pass).
- `appearance_sequence` not in logical identity — yes (still ordering/diagnostic
  metadata; in fingerprint/dedup/sort only).

Token search (`source_provider`, `source_endpoint_or_feed_id`,
`source_lineage_key`, `logical_event_key`, `source_record_id`,
`appearance_sequence`) found no selection/grouping path that bypasses the lineage
gate. The gate is the first thing evaluated after grouping and returns before any
selection can occur.

---

## 3. Independent Cross-Provider Reproduction

In-memory, public functions only, no I/O:

| Case | Setup | Result | Verdict |
|---|---|---|---|
| A. cross-provider before cutoff | provA(final,K8) + provB(final,K3,later), same game/pitcher | `ambiguous_cross_source_lineage`, 0 rows | PASS |
| B. cross-provider same timestamp | provA + provB at identical `collected_at_utc`, conflicting | `ambiguous_cross_source_lineage` (NOT `ambiguous_revision`), 0 rows | PASS |
| C. cross-provider identical content | provA + provB, byte-identical stats | `ambiguous_cross_source_lineage`, 0 rows (no silent dedup) | PASS |
| D. same provider, different feed | feed_a + feed_two | `ambiguous_cross_source_lineage`, 0 rows | PASS |

The diagnostic for A was:
`selection failed closed: multiple source lineages [('prov_a', 'feed_a'), ('prov_b', 'feed_b')] for pitcher-game (game_pk=9901001, pitcher_id=880101); different providers/feeds are not automatic revisions of one another`

provider B never overwrote provider A in any case. The pre-fix silent
latest-lineage-wins behavior no longer reproduces.

---

## 4. Cutoff-Aware Lineage Semantics

| Scenario | Expected | Result |
|---|---|---|
| A. provB collected after cutoff | provA selectable; no historical ambiguity | PASS (status ok, provA, K8) |
| B. later cutoff now includes provB | event becomes cross-source ambiguous | PASS (`ambiguous_cross_source_lineage`) |
| C. same-lineage correction before cutoff | corrected selected | PASS (K9) |
| D. same-lineage correction after cutoff | original selected | PASS (K8) |
| E. same-lineage reordered correction | one corrected logical row | PASS (existing tests + reproduction) |
| F. same-lineage same-time conflict | `ambiguous_revision` | PASS (`test_same_lineage_same_time_conflict_remains_ambiguous_revision`) |
| G. cross-lineage + within-lineage interaction | cross-source precedence, deterministic; not bypassed by `corrected` status | PASS |

Strict gates remain (selection line ~889):

```
game_start_utc        <  target_information_cutoff_utc
game_finalized_at_utc <= target_information_cutoff_utc
collected_at_utc      <= target_information_cutoff_utc
```

Because lineage detection runs only over rows already known by the cutoff, a
later-collected second lineage cannot retroactively make earlier single-lineage
knowledge ambiguous (Scenario A), and is correctly surfaced only once the cutoff
advances to include it (Scenario B).

---

## 5. Fail-Closed Scope

The cross-source pass returns immediately with `events=()` — the **whole
selection** fails closed, identical in shape to the existing `ambiguous_revision`
path. This was verified to be deliberate and documented:

- **Intentional**: a dedicated pre-pass that returns before revision resolution.
- **Consistent with existing ambiguity semantics**: `ambiguous_revision` also
  returns immediately with empty events.
- **Documented**: skeleton report fixture inventory states "cross-source
  ambiguity blocking the **whole selection** (no partial escape)", and §9 states
  it "fails closed … and returns nothing".
- **Callers cannot misread failure as success**: `status="ambiguous_cross_source_lineage"`
  with `events=()`; there is never a failure status accompanied by partial rows.
- **No partial escape**: `test_cross_source_ambiguity_blocks_whole_selection_no_partial_escape`
  proves that even a clean second game for the same pitcher is withheld when any
  logical event is cross-source ambiguous.

Program behavior and report description of the fail-closed granularity are
consistent. This is a conservative design choice; a future enhancement could
instead exclude only the ambiguous event while returning clean ones, but that
would also change `ambiguous_revision` semantics and is intentionally out of
scope. Noted as a limitation, not a blocker.

---

## 6. Lineage Normalization

| Input | Behavior | Verdict |
|---|---|---|
| empty / whitespace-only `source_provider` | rejected at `normalize_pitcher_game_event` (`_required_text`) — fail closed | PASS |
| empty / whitespace-only `source_endpoint_or_feed_id` | rejected at normalization — fail closed | PASS |
| case-variant providers (`ProviderX` vs `providerx`) | treated as **distinct** lineages → `ambiguous_cross_source_lineage` (no silent merge) | PASS |
| leading/trailing whitespace (`prov_a ` vs `prov_a`) | `_required_text` strips to a canonical value → same lineage | deterministic (see note) |
| alias-like / malformed feed IDs | distinct literal strings → distinct lineages → fail closed | PASS |

Findings:

- Empty or whitespace-only lineage values fail closed at normalization; they
  cannot reach the selector, so they cannot bypass the ambiguity gate.
- Distinct literal lineage values are never silently merged; case differences
  fail closed (the safe direction). No provider alias resolution and no case
  normalization are performed, which the contract does not require.
- **Note (deterministic canonicalization, non-blocking):** because every text
  field is `.strip()`-normalized uniformly, two rows whose lineage differs only
  by surrounding whitespace collapse to one canonical lineage and are treated as
  the same stream. This is consistent, deterministic whitespace canonicalization
  — not an alias/case bypass — and only affects whitespace artifacts of the
  *same* literal provider/feed. Genuinely distinct providers or feeds never
  merge. This behavior should be noted in the contract if stricter
  byte-exactness is ever required, but it is safe for v1.

No malformed-lineage path can bypass the ambiguity gate.

---

## 7. Identity and Store Regression

No regression in identity or store behavior (existing tests green, spot-checked):

- stable `source_record_id` across reorder — `test_source_record_id_is_stable_across_pitcher_list_reorder`
- `appearance_sequence` = metadata only — confirmed (not in `logical_event_key`)
- one-row-per-pitcher-game v1 — enforced
- duplicate pitcher in one side rejected — `ambiguous_duplicate_pitcher`
- same pitcher on both sides rejected — `ambiguous_pitcher_both_sides` (whole game)
- exact-duplicate idempotency — `dedup_key` no-op
- append-only correction; prior rows retained — store tests green
- deterministic SHA-256 fingerprint — green
- malformed JSONL fails closed before append — green
- no default output path / zero import-time write — green
- store retains multiple lineages physically; ambiguity is resolved at selection
  (the store neither deletes nor overwrites another lineage) — confirmed by
  design (`append` only suppresses exact `dedup_key` duplicates; lineage
  distinctions survive via provider + fingerprint).

---

## 8. Temporal / PIT Regression

| Check | Result |
|---|---|
| 2024 game, 2026 collected, 2025 cutoff → excluded | PASS (`test_post_hoc_2024_…`) |
| cutoff after actual collection → eligible (absent lineage ambiguity) | PASS (`test_post_hoc_event_eligible_after_actual_collection_time`) |
| target game excluded | PASS |
| future game excluded | PASS |
| correction after cutoff does not rewrite earlier knowledge | PASS |
| provider after cutoff does not create earlier ambiguity | PASS (Phase 4 Scenario A) |
| `game_finalized_at_utc` does not substitute for availability | PASS (documented) |
| no fabricated archive/publication timestamp | PASS (no such field added) |

Strict collected-at PIT gating is unchanged.

---

## 9. Test and Fixture Quality

Direct suite = **119 tests** (was 110; +9 for this fix). The 9 new tests:

- `test_cross_provider_later_row_does_not_silently_overwrite` — selection, asserts diagnostic + game_pk/pitcher_id
- `test_cross_provider_same_timestamp_is_cross_source_not_revision` — selection
- `test_cross_provider_identical_content_is_not_silently_deduped` — selection
- `test_second_provider_after_cutoff_does_not_create_historical_ambiguity` — selection
- `test_same_provider_different_feed_fails_closed` — selection
- `test_cross_source_diagnostic_is_order_independent` — selection, determinism
- `test_cross_source_ambiguity_blocks_whole_selection_no_partial_escape` — selection, no partial escape
- `test_same_lineage_same_time_conflict_remains_ambiguous_revision` — selection, regression guard
- `test_source_lineage_completes_source_identity` — identity/contract documentation

Quality assessment:

- Eight of nine new tests exercise `select_prior_pitcher_events` directly (not
  just properties). The ninth documents the lineage identity contract.
- No vacuous assertions found; each cross-source test asserts both `status` and
  `events`, and several assert diagnostic content/determinism.
- No surviving test permits provider overwrite; the prior suite had no
  cross-provider test, and the new ones close that gap.
- Fixture catalog gained six cross-source scenario names (38 → 44). Several
  cross-source scenarios are constructed inline from the reusable payloads rather
  than as standalone payloads; the report now states the catalog count is not a
  count of full payloads.
- Existing correction/reorder/superseded/target/future/PIT/duplicate/both-sides
  tests are retained and green.

119 is a count, not proof; the substantive coverage above supports readiness.

---

## 10. Report Accuracy

The skeleton report accurately records:

- logical event identity `(game_pk, pitcher_id)`; source lineage
  `(source_provider, source_endpoint_or_feed_id)`; `source_record_id` scoped by
  lineage (§3, §9, 2026-06-14 header note)
- revisions resolve only within one lineage; multiple eligible lineages fail
  closed; cutoff-aware detection; no precedence/consensus/voting/averaging/silent
  dedup (§9, header note)
- whole-selection fail-closed granularity (fixture inventory line; §9)
- strict collected-at PIT; post-hoc observational limitation; repeated-appearance
  limitation; no-network / no-production / live HOLD (§9, §13)
- direct tests = 119; combined = 414 (§11, §15)
- full regression = NOT RUN (§12)

No production/historical readiness is overclaimed; `diagnostic_only=true`,
`production_ready=false` remain fixed. The two prior review reports are
unmodified historical records.

---

## 11. Independent Validation

Using only `.venv/bin/python`:

| Suite | Result |
|---|---|
| `tests/test_mlb_pitcher_game_events.py` | **119 passed** |
| `tests/test_mlb_probable_starter_collector.py` | **49 passed** |
| `tests/test_mlb_probable_starter_snapshot_intake.py` | **89 passed** |
| Workflow guards (5 files) | **157 passed** |
| Combined relevant (8 suites) | **414 passed** |
| `py_compile` (pitcher-events + collector + snapshots) | **PASS** |
| `git diff --check` | **PASS** |
| AST import scan of source | stdlib only (`dataclasses, datetime, hashlib, json, pathlib, typing`); no network/DB roots |

---

## 12. Full Regression Status

Full repository regression: **NOT RUN.** The module is an isolated, uncommitted,
no-network fixture skeleton; the mandated 414-test combined set is proportional;
the change is local and deterministic. Consistent with the prompt's "NOT RUN
unless clearly safe and proportional."

---

## 13. Side-Effect Verification

Pre-test and post-test states are identical except for this single authorized
review report:

- HEAD `6de072b…` unchanged; 0 staged; 0 open PRs
- P202D/P202E tracked diff empty
- pitcher-event / probable-starter runtime dirs absent
- untracked count 14 before writing this report (the four whitelist files were
  already untracked and were modified in place by the prior fix turn; no new
  source/test/fixture file was created by this re-review)
- P202F report, original post-implementation review, and stable-identity
  re-review all intact (classification strings present)
- no network/API call; in-memory reproductions wrote nothing; tests use
  `tmp_path`; no stray output; no tolerated runtime/governance file modified by
  this task

---

## 14. Risks and Limitations

1. **Whole-selection fail-closed scope** — any cross-source (or same-time)
   ambiguity withholds *all* of the pitcher's prior games, not just the ambiguous
   one. Deliberate, documented, consistent with `ambiguous_revision`; a future
   per-event variant is possible but out of scope. Non-blocking.
2. **Whitespace canonicalization** — lineage values are `.strip()`-normalized, so
   whitespace-only differences in provider/feed collapse to one lineage.
   Deterministic and safe (distinct providers never merge); note in the contract
   if byte-exact lineage is ever required. Non-blocking.
3. **Case sensitivity** — case-variant providers are distinct and fail closed
   (safe, possibly over-conservative); no alias/case normalization by design.
   Non-blocking.
4. **Decoded-contract assumptions** — complete FIP components and explicit
   role/provenance are required of decoded input; the real StatsAPI boxscore
   branch remains unimplemented; no real-season completeness claim.
5. **Post-hoc rows are observational only** before their collection time; safe
   and documented.
6. **Store append is not concurrency-safe** (no such claim).
7. **P202F live-transport authorization remains HOLD**; nothing here unlocks it.

---

## 15. Commit-Readiness Decision

**Classification: `READY_FOR_COMMIT_PACKAGING`.**

All READY criteria are satisfied:

- no cross-provider silent overwrite — ✔ (reproduced fail-closed)
- no cross-feed silent overwrite — ✔
- cutoff-aware lineage detection correct — ✔
- same-lineage correction/reorder correct — ✔
- ambiguity diagnostics deterministic — ✔ (order-independent test)
- fail-closed granularity intentional and documented — ✔ (whole-selection)
- malformed lineage cannot bypass the gate — ✔ (empty/whitespace fail closed;
  distinct/case fail closed)
- strict PIT unchanged — ✔
- append-only / idempotency unchanged — ✔
- tests all green — ✔ (119/49/89/157/414)
- reports accurate — ✔
- zero persistent side effect — ✔
- zero network path — ✔ (AST stdlib only)
- no production-readiness overclaim — ✔

**Single remaining blocker: NONE.**

### Packaging set (exactly 7 files; P202F excluded)

1. `data/mlb_pitcher_game_events.py`
2. `tests/test_mlb_pitcher_game_events.py`
3. `tests/fixtures/mlb_pitcher_game_event_fixtures.json`
4. `report/p202g_b_pitcher_event_backfill_skeleton_20260614.md`
5. `report/p202g_b_post_implementation_review_20260614.md`
6. `report/p202g_b_stable_revision_identity_fix_review_20260614.md`
7. `report/p202g_b_cross_provider_identity_fix_review_20260614.md`

Packaging itself (branch/stage/commit/PR) is a separate authorized action and was
not performed in this read-only re-review.

---

## 16. Required Completion Check

| Item | Result |
|---|---|
| 是否真的完成 | YES — independent read-only final re-review complete |
| Test result | PASS |
| P202G-B direct count | 119 |
| P202E count | 49 |
| P202D count | 89 |
| Workflow count | 157 |
| Combined count | 414 |
| Full regression | NOT RUN |
| Commit-readiness classification | `READY_FOR_COMMIT_PACKAGING` |
| Cross-provider defect status | RESOLVED (reproduced fail-closed; no silent overwrite) |
| Logical event identity | `(game_pk, pitcher_id)` |
| Source lineage identity | `(source_provider, source_endpoint_or_feed_id)` |
| source_record_id scope | scoped by lineage; same string may recur across lineages; never a cross-lineage revision |
| Cross-provider before-cutoff | `ambiguous_cross_source_lineage`, 0 rows |
| Cross-provider after-cutoff | other lineage filtered first; earlier lineage selectable; no historical ambiguity |
| Cross-feed | `ambiguous_cross_source_lineage`, 0 rows |
| Identical cross-provider | fail closed, no silent dedup |
| Same-lineage correction | corrected selected (before cutoff) / original (after cutoff) |
| Reordered correction | one corrected logical row (unchanged) |
| Same-time revision ambiguity | within-lineage → `ambiguous_revision` (cross-source precedence above it) |
| Fail-closed scope | WHOLE selection, intentional, documented, no partial escape |
| Lineage normalization | empty/whitespace fail closed; case-distinct fail closed; whitespace canonicalized deterministically; no gate bypass |
| Strict PIT | unchanged |
| Post-hoc historical eligibility | observational only before collection; excluded at earlier cutoff |
| Target/future exclusions | PASS / PASS |
| Idempotency | PASS (exact-duplicate no-op) |
| Revision history | append-only; logical collapse within lineage |
| Append-only | PASS |
| No-network | PASS (AST stdlib only) |
| Persistent runtime write | NONE (tmp_path; in-memory reproductions) |
| P202F unchanged | YES (`P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`, HOLD) |
| Prior reviews unchanged | YES (NEEDS_SMALL_FIX + BLOCKED_BY_CROSS_PROVIDER intact) |
| P202D/P202E unchanged | YES (empty diff) |
| Single blocker or NONE | NONE |
| Modified files (this task) | `report/p202g_b_cross_provider_identity_fix_review_20260614.md` only |
| Untracked files | agent_bootstrap/×3, 4 P202G-B impl/test/fixture/skeleton, P19x/P20x reports, P202F, 3 review reports |
| Staged files | NONE |
| Current branch | `main` |
| Local HEAD / origin/main | `6de072b…` / `6de072b…` (equal) |
| Open PR count | 0 |
| active_task.md status | STALE P199 plan-only; no competing implementation authorization |
| DB/API/provider/production/registry/controlled_apply | NOT USED / UNCHANGED |
| Model/strategy/champion mutation | NONE |
| Commit/push | NONE / NONE |
| Whether packaging allowed | YES (separate authorized action) |
| Exact packaging file count | 7 (P202F excluded) |
| Whether next round allowed | YES — commit packaging of the 7-file set; live transport remains P202G-A HOLD |
| Worker model recommendation | OPUS-CLASS |
| Thinking level recommendation | MEDIUM |
| Same/new conversation | NEW CONVERSATION for the packaging action |
| Final Classification | `P202G_B_CROSS_PROVIDER_REREVIEW_READY_FOR_COMMIT_PACKAGING` |

### CTO Conclusion

The cross-provider/source-lineage fail-closed fix resolves the silent-overwrite
blocker without regressing the stable reorder identity, the strict collected-at
PIT gates, or the store's append-only behavior. Cross-provider and cross-feed
conflicts now fail closed with a deterministic `ambiguous_cross_source_lineage`
diagnostic; there is no latest-wins, precedence, consensus, averaging, or silent
dedup, and even identical cross-lineage content stays ambiguous. Lineage
detection runs after the cutoff filter, so future lineages cannot create
historical ambiguity, and malformed/empty lineage values fail closed at
normalization. The whole-selection fail-closed granularity is intentional,
consistent with `ambiguous_revision`, and documented. The four-file change is
ready to package with the three review reports (seven files); P202F's
live-transport HOLD is separate and unchanged.

### CEO Conclusion

The earlier problem — a second data source silently overwriting the first — is
fixed and proven by independent reproduction and tests. When two sources describe
the same pitcher's game, the system now refuses to guess and returns nothing
rather than silently trusting the newer one. Everything else still works:
corrections within one source, the reorder fix, and the strict "only use what was
truly known beforehand" rule. It is safe to package. No live data, betting,
model, or production change is involved, and the MLB live-data hold is unchanged.
