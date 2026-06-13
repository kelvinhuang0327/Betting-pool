# P202G-B Stable Revision-Identity Fix — Independent Read-Only Re-Review

Date: 2026-06-14

Final classification:
`P202G_B_STABLE_IDENTITY_REREVIEW_BLOCKED_BY_CROSS_PROVIDER_IDENTITY`

> Scope note: this is an independent, read-only re-review of the reported
> stable-identity narrow fix. No implementation, test, fixture, governance, or
> prior report was modified. The original reorder blocker is genuinely
> resolved. A separate cross-provider identity hazard, surfaced by the now
> source-position-independent revision grouping, blocks commit packaging under
> this task's own gating rule.

---

## 1. Governance and Phase 0

### Required governance reads

- `00-Plan/roadmap/agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` — read. Standard
  Phase 0 / STOP / whitelist framework; no conflict.
- `00-Plan/roadmap/agent_bootstrap/CURRENT_STATE.md` — read. Records an older
  HEAD baseline `2a7aa134…` (stale relative to current `6de072b…`) and a
  tolerated-dirty + authorized-uncommitted-governance list.
- `00-Plan/roadmap/active_task.md` — read. Still `P199 AUTHORIZED_PLAN_ONLY`.
  It does **not** authorize a competing implementation. The explicit re-review
  prompt is the controlling authority for this task.
- `00-Plan/roadmap/agent_bootstrap/TASK_TEMPLATES.md`, `roadmap.md`,
  `CTO-Analysis.md` — present; governance is stale but untouched.
- `report/p202f_live_transport_authorization_and_dry_run_design_audit_20260613.md`
  — present. Final classification `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`;
  MLB live transport remains **HOLD**. Unchanged by this task.
- Both P202G-B reports — read in full.

Governance is stale (phase labels lag the merged P202D/E and the P202F audit),
but staleness is a documented, tolerated condition and the prompt's read-only
authorization explicitly covers it. No governance file was edited. This is
**not** a STOP condition for a read-only re-review.

### Phase 0 actual-state verification

| Check | Observed | Expected | Result |
|---|---|---|---|
| repo top-level | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | same | PASS |
| branch / symbolic HEAD | `main` / `main` | `main`, not detached | PASS |
| git-dir | `.git` | `.git` | PASS |
| local HEAD | `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9` | = origin/main | PASS |
| origin/main | `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9` | = local HEAD | PASS |
| baseline ancestor | `6de072b…` is ancestor of HEAD | ancestor | PASS |
| open PR count | 0 | 0 | PASS |
| staged files | none | none | PASS |
| Python | 3.13.8 | ≥ 3.11 | PASS |
| five P202G-B files | present, untracked | present, uncommitted | PASS |
| P202F report | present | present | PASS |
| P202D/P202E source + tests | present | present | PASS |
| `data/mlb_pitcher_game_events` runtime dir | absent | absent | PASS |
| `data/mlb_probable_starters` runtime dir | absent | absent | PASS |
| P202D `mlb_probable_starter_snapshots.py` diff | empty | unchanged | PASS |
| P202E `mlb_probable_starter_collector.py` diff | empty | unchanged | PASS |

Dirty/untracked state is confined to: tolerated runtime/data files, authorized
uncommitted governance + bootstrap files, the earlier excluded P19x/P20x
reports, the P202F report, and exactly the five P202G-B files. No STOP
condition triggered.

---

## 2. Fix Diff Review

The current implementation in `data/mlb_pitcher_game_events.py` implements the
reported stable-identity contract:

- **Logical event key** (`logical_event_key`, lines 158-166): returns
  `(game_pk, pitcher_id)`. `appearance_sequence` is documented as observed
  source-ordering metadata that "must never partition revision history." ✔
- **Generated `source_record_id`** (adapter, line 708):
  `f"{raw_game_pk}:pitcher:{raw_pitcher_id}"` — independent of
  `appearance_sequence`, home/away side, pitcher-list position, statistics, and
  collection timestamp. ✔
- **Revision grouping** (selection, lines 880-882): groups eligible records by
  `logical_event_key`, i.e. `(game_pk, pitcher_id)` — not by mutable ordering. ✔
- **`appearance_sequence` retained only as ordering/diagnostic content**: it
  appears in `EVENT_FIELDS`, the normalized schema, the fingerprint inputs
  (line 414), the exact-duplicate `dedup_key` (line 153), and the final result
  sort key (line 920). It does **not** appear in `logical_event_key`. This is
  exactly the Phase 1 allowance ("may remain in normalized schema, fingerprint,
  observed-order diagnostics, stored revision contents; must not remain part of
  logical revision identity"). ✔
- **Same-pitcher duplicate within one side** (lines 635-649): detected and the
  affected side is failed closed with `ambiguous_duplicate_pitcher`. ✔
- **Same pitcher on both sides** (lines 557-583): pre-scan computes the
  intersection of home/away pitcher IDs and fails the **whole game** closed with
  `ambiguous_pitcher_both_sides` *before any side emits a row*. ✔
- **Strict collected-at PIT gates** (line 876): unchanged.

Residual-use search for `appearance_sequence`: it is used in (a) the dataclass
field, (b) the fingerprint, (c) the dedup key, (d) the adapter side-local
enumeration, and (e) the result sort key. It is **not** used in logical revision
grouping, source identity, revision selection, or ambiguity resolution. The
removal from logical identity is complete.

---

## 3. Original-Defect Post-Fix Reproduction

Reproduced independently in memory using only public functions and synthetic
data (no file or network I/O):

1. Original finalized game, pitcher 880101 at list position 1 →
   `appearance_sequence = 1`, `source_record_id = 9901001:pitcher:880101`,
   `record_status = final`, K = 8.
2. Corrected payload reorders the home pitcher list (880101 moves to position 2)
   and bumps K to 9 → `appearance_sequence = 2`,
   `source_record_id = 9901001:pitcher:880101` (identical),
   `record_status = corrected`, collected later.
3. Both rows known before the cutoff `2099-06-04T00:00:00Z`.

Observed result:

```
orig seq = 1 | corr seq = 2
source_record_id stable?  True   (9901001:pitcher:880101)
logical_event_key equal?  True   ((9901001, 880101))
selection status = ok | n_selected = 1
selected record_status = corrected | K = 9 | seq = 2
```

The original review's `status=ok / [(seq=1,K=8),(seq=2,K=9)]` (two appearances)
no longer reproduces. The selector returns **exactly one** logical row, the
corrected one. **Original reorder defect: RESOLVED.**

---

## 4. Stable Logical Identity

- `source_record_id` is stable across pitcher-list reorder, side, statistics,
  and collection time. Confirmed by reproduction and by
  `test_source_record_id_is_stable_across_pitcher_list_reorder`.
- `logical_event_key = (game_pk, pitcher_id)` is the sole revision-grouping key.
- Append-only history still retains every physical observation; logical
  selection collapses them to one row per pitcher-game.

This is correct and internally coherent **within a single provider**. See §7 for
the cross-provider dimension, which is the blocker.

---

## 5. Cutoff and Revision Semantics

Strict gates in `select_prior_pitcher_events` (line 876) — a record is excluded
unless all hold:

```
game_start_utc       <  target_information_cutoff_utc
game_finalized_at_utc <= target_information_cutoff_utc
collected_at_utc      <= target_information_cutoff_utc
```

Independent scenario verification (code + named tests; reproductions run):

| Scenario | Expected | Result | Evidence |
|---|---|---|---|
| A. Correction before cutoff | corrected selected | PASS | `test_later_correction_replaces_earlier_record`; reproduced |
| B. Correction after cutoff | earlier final selected | PASS | `test_correction_after_cutoff_does_not_replace_known_record`, `test_reordered_correction_after_cutoff_keeps_known_record` |
| C. Reorder-only later observation | one logical row | PASS | `test_reorder_only_later_observation_selects_single_row` |
| D. Same-time conflicting revisions | `ambiguous_revision`, fail closed | PASS | `test_ambiguous_latest_corrections_fail_closed`, `test_direct_repeated_appearance_for_one_pitcher_game_fails_closed` |
| E. Superseded latest row | excluded | PASS | `test_latest_superseded_marker_excludes_appearance` |
| F. Target game | always excluded | PASS | `test_target_game_is_explicitly_excluded` |
| G. Future game | always excluded | PASS | `test_future_game_is_excluded` |
| H. Post-hoc backfill (2024 game collected 2026, cutoff 2025) | excluded | PASS | `test_post_hoc_2024_game_collected_in_2026_excluded_before_2025_cutoff` |
| I. Use after actual collection (cutoff 2026-07, collected 2026-06) | eligible | PASS | `test_post_hoc_event_eligible_after_actual_collection_time` |

Strict collected-at PIT gating is **unchanged** and correct. The post-hoc
limitation (a finalized historical game collected only later is not
contemporaneously-available evidence at an earlier cutoff; `game_finalized_at_utc`
alone does not prove availability) is preserved in code and now documented in the
skeleton report §9.

Minor over-conservatism (non-blocking): because `appearance_sequence` is part of
the fingerprint, a hypothetical *reorder-only re-observation collected at the
exact same `collected_at_utc`* would be flagged `ambiguous_revision` (different
fingerprints at the same latest collection time) even though the statistics are
identical. This is fail-closed (safe), an unusual edge case, and the realistic
later-collection path (Scenario C) resolves correctly. Noted as a limitation,
not a defect.

---

## 6. Duplicate and Repeated-Appearance Behavior

| Case | Behavior | Result |
|---|---|---|
| Duplicate `pitcher_id` within one side | `ambiguous_duplicate_pitcher`; that side fails closed (`continue`), no rows emitted from it | PASS (`test_adapter_rejects_ambiguous_duplicate_pitcher_list`) |
| Same `pitcher_id` on home and away | `ambiguous_pitcher_both_sides`; whole game fails closed before any side emits | PASS (`test_adapter_rejects_same_pitcher_on_both_sides`) |
| Malformed decoded pitcher list | `malformed_pitcher_list`; side rejected | PASS (`test_adapter_diagnoses_malformed_pitcher_list`) |
| Direct normalized rows, same `(game_pk, pitcher_id)`, same time, conflicting content | `ambiguous_revision`, fail closed, returns none | PASS (`test_direct_repeated_appearance_for_one_pitcher_game_fails_closed`) |

Contract v1 = one row per `(game_pk, pitcher_id)`. Genuine repeated appearances
(a pitcher who leaves and returns in one game) are **unsupported** and fail
closed rather than being silently created from sequence differences. No second
logical appearance is fabricated from ordering. No partial accepted rows escape
from a game-level cross-side identity conflict.

Diagnostic codes are deterministic and specific:
`ambiguous_duplicate_pitcher`, `ambiguous_pitcher_both_sides`,
`ambiguous_revision`.

Minor (non-blocking) accounting imprecision: when a side fails closed on a
within-side duplicate, `rejected_records` is incremented only by the count of
duplicate IDs, not by the full count of pitchers on the skipped side. This
under-reports rejected count but does **not** let any row escape; safety is
unaffected. Note for a future cleanup.

---

## 7. Cross-Provider Identity Review — **BLOCKER**

The fix made revision grouping source-position independent. This re-review's
mandate is to determine whether that introduces a cross-provider ambiguity. It
does.

### Findings

- `logical_event_key = (game_pk, pitcher_id)` does **not** include
  `source_provider`.
- The generated `source_record_id = "{game_pk}:pitcher:{pitcher_id}"` does
  **not** include `source_provider`, so it **collides across providers** for the
  same pitcher-game.
- `select_prior_pitcher_events` groups eligible records purely by
  `logical_event_key` (lines 880-882) and resolves each group by latest
  `collected_at_utc`. Provider is never consulted in grouping, selection, or
  ambiguity resolution.
- `source_provider` *is* a separate validated dimension for **storage** (it is
  part of `dedup_key`, line 149, and the fingerprint), so two providers' rows
  are physically retained. But **selection** ignores it.

### Reproduced silent overwrite

Two independent `final` observations of the same pitcher-game from two different
providers, the second collected later:

```
provA: provider = statsapi_decoded_final_boxscore | final | K = 8 | collected 2099-06-02T04:30:00Z | srid 9901001:pitcher:880101
provB: provider = rival_provider_beta            | final | K = 3 | collected 2099-06-03T12:00:00Z | srid 9901001:pitcher:880101
same logical_event_key?                True
same source_record_id (collides)?      True
selection status = ok | n_selected = 1
selected provider = rival_provider_beta | K = 3 | status = final
```

The later-collected **different provider's** `final` row silently replaces the
first provider's `final` row, as if it were a correction — with no `corrected`
status, no provider precedence, and no diagnostic. Reversing collection order
makes the other provider win (no precedence rule). When the two providers'
conflicting rows share the same `collected_at_utc`, the conflict surfaces as
`ambiguous_revision` (fail-closed, but mislabeled as a same-pitcher revision
conflict rather than a cross-provider conflict).

### Contract determination

| Question | Answer |
|---|---|
| Single-provider input an explicit contract invariant? | **No** — not stated or validated anywhere in source or either report. |
| Cross-provider rows fail closed? | **No** (only the same-collection-time sub-case does, and only incidentally). |
| Provider precedence defined? | **No**. |
| Does the selector silently treat one provider as a correction of another? | **Yes** — confirmed empirically. |

The task's allowance — "a `source_record_id` string may repeat across providers
only if `source_provider` remains a separate validated identity dimension **and**
selection semantics remain safe" — is **not** satisfied: storage keeps provider
distinct, but selection drops it and silently overwrites. The task's explicit
rule then applies: *"Commit readiness must be blocked if conflicting providers
can silently overwrite one another without an explicit contract."*

This is the single remaining blocker.

---

## 8. Fingerprint, Deduplication, and Append-Only Behavior

| Property | Result |
|---|---|
| Fingerprint = deterministic SHA-256 over canonical sorted compact JSON | PASS |
| Key-order independence | PASS |
| `appearance_sequence` change alters stored content/fingerprint | PASS (in fingerprint inputs) |
| Logical identity stable despite fingerprint change | PASS |
| Exact duplicate is a no-op | PASS (`test_jsonl_store_appends_loads_and_suppresses_exact_duplicates`, `…deduplicates_within_one_append`) |
| Later identical content at a new collection time appends | PASS — documented observation-history semantics (collected time in dedup key + fingerprint) |
| Corrections append, original preserved | PASS (`test_jsonl_store_appends_correction_and_preserves_prior_row`) |
| Malformed JSONL fails closed before append | PASS (`test_jsonl_store_rejects_corrupt_line`, `…rejects_unknown_contract_field`) |
| No default path / no import-time write / missing parent fails explicitly | PASS (`test_jsonl_store_requires_existing_parent`, `test_module_has_no_network_import_or_default_store_path`) |
| Tampered supplied fingerprint rejected | PASS (`test_tampered_payload_fingerprint_is_rejected`) |

The fix did not weaken field validation, fingerprint validation, append-only
behavior, or malformed-store protection. No concurrency-safety claim is made
(append, not atomic replace); acceptable for a fixture skeleton.

---

## 9. Test and Fixture Quality

- Direct suite: **110 tests** (was 103; +7 for the fix).
- New fix-specific tests (all meaningful, all exercise selection, not just
  helpers):
  - `test_reordered_corrected_payload_resolves_to_single_revision`
  - `test_source_record_id_is_stable_across_pitcher_list_reorder`
  - `test_reordered_correction_after_cutoff_keeps_known_record`
  - `test_reorder_only_later_observation_selects_single_row`
  - `test_direct_repeated_appearance_for_one_pitcher_game_fails_closed`
  - `test_adapter_rejects_same_pitcher_on_both_sides`
  - `test_post_hoc_2024_game_collected_in_2026_excluded_before_2025_cutoff`,
    `test_post_hoc_event_eligible_after_actual_collection_time`
- No surviving test asserts sequence-based **logical** identity. The reorder
  tests explicitly assert that sequence differs while identity stays stable —
  the correct post-fix invariant.
- Fixture catalog: 38 scenario names, 8 reusable payload groups, `fixture_notice`
  marked synthetic. Several scenarios are constructed inline in tests rather than
  as standalone payloads — acceptable, but "38" must not be read as 38 full
  payloads.

**Coverage gap (tied to §7 blocker):** there is **no** cross-provider test. No
test constructs two events with the same `(game_pk, pitcher_id)` and differing
`source_provider`. The silent-overwrite behavior is therefore unverified and
unguarded by the suite.

Pre-existing weak test (unchanged): `test_stake_changes_cannot_change_pitcher_event_or_selection`
mostly confirms stake absence and deterministic repetition; low value but
harmless.

The number 110 alone does not establish readiness — the suite passes but does
not cover the cross-provider hazard.

---

## 10. Report Accuracy

Skeleton report `report/p202g_b_pitcher_event_backfill_skeleton_20260614.md`
(updated header + §3, §5, §7, §9) accurately states:

- logical identity is `(game_pk, pitcher_id)` ✔
- `source_record_id` is stable across reorder ✔
- `appearance_sequence` is ordering metadata only ✔
- repeated same-pitcher appearances are unsupported in v1, fail closed ✔
- corrected list reorder resolves to one revision ✔
- post-hoc historical rows are observational only before collection;
  `game_finalized_at_utc` does not prove availability; trustworthy historical
  PIT eligibility needs a verified publication/archive timestamp ✔
- direct/combined counts are 110 / 405 ✔
- P202F live transport remains HOLD; production readiness false ✔
- bullpen aggregate row count corrected to **2,429** — verified actual
  `data/mlb_context/bullpen_usage_3d.jsonl` line count = 2,429 ✔

The original post-implementation review
(`report/p202g_b_post_implementation_review_20260614.md`,
`NEEDS_SMALL_FIX`) is the historical pre-fix record and is left unmodified, as
required.

**Report accuracy gap (tied to §7):** neither report documents the
single-provider contract assumption or the provider-blind selection behavior.
The skeleton report §7 mentions `source_provider` is part of the dedup key but
does not state that selection ignores provider or that input must be
single-provider. This is an accuracy/completeness gap that must be closed
alongside the §7 fix.

---

## 11. Independent Validation

Using only `.venv/bin/python`:

| Suite | Command | Result |
|---|---|---|
| P202G-B direct | `pytest tests/test_mlb_pitcher_game_events.py -q` | **110 passed** |
| P202E collector | `pytest tests/test_mlb_probable_starter_collector.py -q` | **49 passed** |
| P202D snapshot intake | `pytest tests/test_mlb_probable_starter_snapshot_intake.py -q` | **89 passed** |
| Workflow guards (5 files) | leaderboard + sim-gate + evaluator + evaluation-runner + daily-scheduler | **157 passed** |
| Combined relevant | all eight suites above | **405 passed** |
| Compile | `py_compile` of pitcher-events + collector + snapshots | **PASS** |
| `git diff --check` | — | **PASS** |

All counts match the reported validation (110 / 49 / 89 / 157 / 405). The
passing suite does **not** cover the cross-provider hazard.

---

## 12. Full Regression Status

Full repository regression: **NOT RUN.**

Rationale: the module is an isolated, uncommitted, no-network fixture skeleton;
the mandated 405-test combined set is proportional; and the blocker is a
deterministic, reproduced design issue that a full regression would not surface.
Consistent with the prompt's "NOT RUN unless clearly safe and proportional."

---

## 13. Side-Effect Verification

Pre-test and post-test states are identical except for this single authorized
review report (the only intended new file):

- dirty/untracked lines (excluding this report): **24 → 24** (unchanged)
- staged files: **0**
- HEAD: `6de072b…` unchanged
- `data/mlb_pitcher_game_events` runtime dir: absent
- `data/mlb_probable_starters` runtime dir: absent
- P202D `mlb_probable_starter_snapshots.py` / P202E
  `mlb_probable_starter_collector.py` diffs: empty
- original P202G-B review report: unchanged
- P202F report: unchanged
- no stray JSONL output; tests use `tmp_path`; no network/API call; no
  DB/provider/production/registry/model/strategy mutation

In-memory reproductions wrote nothing to disk.

---

## 14. Risks and Limitations

1. **Cross-provider silent overwrite (BLOCKING).** A later-collected row from a
   different `source_provider` for the same `(game_pk, pitcher_id)` silently
   wins selection as if a correction; no single-provider invariant, no
   precedence, no fail-closed, no test, no documentation.
2. Same-time reorder-only re-observation would be flagged `ambiguous_revision`
   (fail-closed over-conservatism; edge case). Non-blocking.
3. `rejected_records` under-counts when a side fails closed on a within-side
   duplicate (diagnostic-count imprecision only; no row escapes). Non-blocking.
4. Post-hoc historical rows are observational only before their collection time;
   safe and now documented.
5. The decoded contract presumes complete FIP components and explicit
   role/provenance; this is a future decoded-input requirement, not proven
   real-source availability. The real StatsAPI boxscore branch remains
   unimplemented.
6. Store append is not atomic/concurrency-safe (no such claim made).
7. P202F live-transport authorization remains HOLD; nothing here unlocks it.

---

## 15. Commit-Readiness Decision

**Classification: `BLOCKED_BY_CROSS_PROVIDER_IDENTITY`. Packaging is NOT allowed.**

`READY_FOR_COMMIT_PACKAGING` requires "no unsafe cross-provider overwrite." That
condition fails. Every other readiness criterion is met:

- original reorder defect no longer reproduces — ✔
- stable `source_record_id` across reorder — ✔
- one selected logical event — ✔
- correction-as-of-cutoff behavior correct — ✔
- strict collected-at PIT unchanged — ✔
- unsupported repeated appearances fail closed — ✔
- same-pitcher duplicate / cross-side conflict fail closed — ✔
- append-only and idempotency coherent — ✔
- direct and combined tests pass — ✔
- reports accurately state limitations (except the cross-provider gap) — partial
- no persistent side effect / no network path / no production overclaim — ✔
- **no unsafe cross-provider overwrite — ✗ (FAILS)**

### Single smallest blocker

`SELECTION_SILENTLY_MERGES_CONFLICTING_PROVIDERS_WITH_NO_SINGLE_PROVIDER_CONTRACT`
— `select_prior_pitcher_events` groups by provider-blind `(game_pk, pitcher_id)`
and `source_record_id` collides across providers, so a later-collected different
provider silently overwrites another during as-of selection.

### Recommended narrow fix scope (do **not** apply in this task)

Smallest safe option — make the existing single-provider assumption explicit and
enforced, rather than redesigning identity:

1. In `select_prior_pitcher_events`, when a logical group spans more than one
   distinct `source_provider`, **fail closed** with a specific diagnostic
   (e.g. `ambiguous_cross_provider`), or define and validate an explicit
   provider-precedence rule. (Alternatively, include `source_provider` in
   `logical_event_key` and add a cross-provider conflict diagnostic.)
2. Add a cross-provider test: same `(game_pk, pitcher_id)`, two providers,
   differing collection times and content → must not silently overwrite.
3. Document the single-provider contract invariant in the skeleton report §7/§9.
4. Retain the strict collected-at PIT gates and the stable
   `(game_pk, pitcher_id)` reorder fix unchanged.

Keep the change within the four P202G-B whitelist files (source, test, fixture
if needed, skeleton report).

---

## 16. Required Completion Check

| Item | Result |
|---|---|
| 是否真的完成 | YES — independent read-only re-review complete |
| Test result | PASS (all run suites) |
| P202G-B direct test count | 110 |
| P202E test count | 49 |
| P202D test count | 89 |
| Workflow test count | 157 |
| Combined relevant test count | 405 |
| Full regression | NOT RUN |
| Commit-readiness classification | `BLOCKED_BY_CROSS_PROVIDER_IDENTITY` |
| Original reorder defect status | RESOLVED (reproduced: 1 corrected row) |
| Logical revision identity | `(game_pk, pitcher_id)` |
| `source_record_id` stability | STABLE across reorder (`{game_pk}:pitcher:{pitcher_id}`); collides across providers |
| `appearance_sequence` role | ordering/diagnostic metadata only; not in logical identity |
| Correction-before-cutoff result | corrected row selected (PASS) |
| Correction-after-cutoff result | earlier final retained (PASS) |
| Same-time ambiguity result | `ambiguous_revision`, fail closed (PASS) |
| Duplicate-pitcher rejection | `ambiguous_duplicate_pitcher`, side fails closed (PASS) |
| Cross-side duplicate result | `ambiguous_pitcher_both_sides`, whole game fails closed, no partial rows (PASS) |
| Repeated-appearance support status | UNSUPPORTED in v1; fails closed |
| Cross-provider identity status | **UNSAFE — silent overwrite; no contract (BLOCKER)** |
| Strict collected-at PIT status | UNCHANGED, correct |
| Post-hoc historical eligibility status | observational only before collection; excluded at earlier cutoff |
| Target/future-game exclusion status | PASS / PASS |
| Idempotency status | PASS (exact duplicate no-op) |
| Revision-history status | append-only physical history; logical collapse PASS (single provider) |
| Append-only status | PASS, non-concurrent skeleton |
| No-network status | PASS |
| Persistent runtime-write status | NONE (tests use `tmp_path`; reproductions in-memory) |
| P202F report unchanged status | UNCHANGED (`P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED`, HOLD) |
| Original P202G-B review unchanged status | UNCHANGED |
| P202D/P202E unchanged status | UNCHANGED (empty diffs) |
| Single remaining blocker | cross-provider silent overwrite / no single-provider contract |
| Modified files | `report/p202g_b_stable_revision_identity_fix_review_20260614.md` only |
| Untracked files | agent_bootstrap/, 5× P202G-B files, P19x/P20x reports, P202F report, this review report |
| Staged files | NONE |
| Current branch | `main` |
| Local HEAD / origin/main | `6de072b…` / `6de072b…` (equal) |
| Open PR count | 0 |
| active_task.md status | STALE P199 PLAN-ONLY; no competing implementation authorization |
| DB/API/provider/production/registry/controlled_apply status | NOT USED / UNCHANGED |
| Model/strategy/champion mutation status | NONE |
| Commit/push status | NONE / NONE |
| Whether packaging is allowed | NO — apply the narrow cross-provider fix first |
| Whether next round is allowed | YES — narrow cross-provider fix only, within the four P202G-B whitelist files |
| Worker model recommendation | OPUS-CLASS |
| Thinking level recommendation | MEDIUM-TO-STRONG |
| Same/new conversation recommendation | NEW CONVERSATION for the scoped fix |
| Final Classification | `P202G_B_STABLE_IDENTITY_REREVIEW_BLOCKED_BY_CROSS_PROVIDER_IDENTITY` |

### CTO Conclusion

The reorder blocker is genuinely fixed: identity is now
`(game_pk, pitcher_id)`, `source_record_id` is reorder-stable, and a corrected
reordered payload resolves to one logical revision while strict collected-at PIT
gating is preserved. However, the coarser, provider-blind grouping makes
`source_record_id` collide across providers, and `select_prior_pitcher_events`
will silently let a later-collected different provider overwrite another
provider's row with no `corrected` status, precedence, or diagnostic. For an
intended pitcher-game SSOT this is a latent integrity hazard. Per this task's
explicit gating rule, commit packaging must wait for a small single-provider
invariant (fail-closed or precedence) plus a cross-provider test and a one-line
contract note. No live data, betting, model, or production work is involved.

### CEO Conclusion

The specific bug we asked about — an official correction that reorders pitchers
duplicating one appearance — is fixed and proven by tests and an independent
re-run. The skeleton is otherwise safe, offline, and honest about its limits.
It is not yet ready to package because, if two different data sources ever
describe the same pitcher's game, the newer one silently overwrites the older
with no rule saying it may. The repair is small and contained. Nothing here
touches betting, live data, or production, and the MLB live-data authorization
hold from P202F is unchanged.
