# P202G-B Per-Game Pitcher Event Backfill Skeleton

Date: 2026-06-14

Final classification: `P202G_B_PITCHER_EVENT_BACKFILL_SKELETON_COMPLETE`

> Updated 2026-06-13: applied the P202G-B stable revision-identity narrow fix.
> Logical revision identity is now `(game_pk, pitcher_id)`; the generated
> `source_record_id` is `<game_pk>:pitcher:<pitcher_id>` and stable across
> pitcher-list reorder; `appearance_sequence` is ordering metadata only; repeated
> same-pitcher appearances in one game fail closed. Direct suite is now 110
> tests; combined relevant suites 405.
>
> Updated 2026-06-14: applied the P202G-B cross-provider/source-lineage
> fail-closed narrow fix. Logical event identity stays `(game_pk, pitcher_id)`;
> source lineage is the existing `(source_provider, source_endpoint_or_feed_id)`
> pair; `source_record_id` is scoped by source lineage. Revision resolution now
> happens only within a single lineage. When more than one eligible source
> lineage exists for one logical pitcher-game, selection fails closed with the
> deterministic diagnostic `ambiguous_cross_source_lineage` and returns nothing —
> no latest-provider-wins, no provider precedence, no voting/consensus, no
> averaging, and no silent cross-source dedup (even identical content from two
> lineages stays ambiguous). A different-lineage row collected after the cutoff
> is filtered out before lineage detection, so it cannot create historical
> ambiguity. No schema field was added. Direct suite is now 119 tests; combined
> relevant suites 414.

## 1. Governance and Phase 0

The task-specific prompt explicitly authorized a four-file, fixture-only
implementation. The repository governance files were read before substantive
inspection and modification.

Phase 0 passed:

- Canonical repository: `/Users/kelvin/Kelvin-WorkSpace/Betting-pool`
- Branch: `main`, non-detached
- Local HEAD: `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`
- `origin/main`: `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`
- Expected baseline is an ancestor
- P202D `b288b22b41ec747c729e386b9955cb398f7d90f7` is an ancestor
- P202E `e7ed5c01fede5d45c40c75e7cc9ec1d4cf6c1365` is an ancestor
- Open PR count: 0
- Staged file count: 0
- Project Python: 3.13.8
- P202F report exists
- All four P202G-B files were absent before implementation
- No pitcher-event or probable-starter runtime output directory existed

Governance is stale relative to this task: `active_task.md` remains on the
older P199 plan-only state. It did not authorize another implementation. The
task prompt's explicit authorization and whitelist controlled this work. No
governance file was modified.

## 2. Existing Phase58-64 Evidence

The prompt's illustrative `data/` paths do not exist in the actual repository.
The relevant implementation evidence is under `wbc_backend/features/` and
`scripts/`.

Observed evidence:

- `wbc_backend/features/mlb_relief_appearance_parser.py`
  - The StatsAPI real-boxscore branch
    `_parse_from_statsapi_boxscore` raises `NotImplementedError`.
  - Its schedule fallback distributes estimated values, including averaged
    innings/earned runs, and marks rows as estimated/proxy output.
  - That fallback is not a trusted pitcher-game event source and is rejected by
    the P202G-B contract.
- `tests/fixtures/phase62_boxscore_fixtures.json`
  - Supplies the grounded StatsAPI-shaped hierarchy used here:
    `teams.{home,away}.pitchers`, `players.ID{id}.person`, and
    `stats.pitching`.
  - Existing fields include pitcher identity, innings, pitch count, and
    strikes. P202G-B's synthetic decoded fixture extends the pitching line with
    the required standard FIP inputs and explicit role/provenance metadata.
- `wbc_backend/features/mlb_bullpen_granular_ingestion.py` and Phase62/63 tests
  - Establish side ordering, pitcher-list ordering, `gamePk`, team side, player
    ID, and per-player pitching-line parsing conventions.
  - Existing Phase63 fixture output is fixture-only and aggregated downstream;
    it is not treated as a real-season pitcher-event SSOT.
- `data/mlb_context/bullpen_usage_3d.jsonl`
  - Contains 2,429 team-level three-day aggregate rows, not one-row-per-pitcher-
    game observations.
- Phase63 evidence
  - Describes 26 fixture-only pitcher appearances and team aggregate features.
  - It does not establish historical pitcher-game completeness.

Source-shape conclusion: the normalized adapter is grounded in existing
boxscore fixtures and parser conventions, but no existing real-season
pitcher-event SSOT was found.

## 3. Exact Schema

Contract version: `p202g-b.v1`

Parser version: `p202g-b.statsapi-decoded.v1`

The exact normalized JSONL schema has 34 fields:

1. `contract_version`
2. `source_provider`
3. `source_endpoint_or_feed_id`
4. `source_record_id`
5. `payload_fingerprint`
6. `collected_at_utc`
7. `game_pk`
8. `game_start_utc`
9. `game_finalized_at_utc`
10. `official_game_date`
11. `pitcher_id`
12. `pitcher_name`
13. `team_id`
14. `opponent_team_id`
15. `home_away`
16. `appearance_sequence`
17. `starter_flag`
18. `record_status`
19. `innings_outs`
20. `innings_pitched_display`
21. `batters_faced`
22. `strikeouts`
23. `walks`
24. `intentional_walks`
25. `hit_by_pitch`
26. `home_runs_allowed`
27. `hits_allowed`
28. `earned_runs`
29. `runs_allowed`
30. `pitches_thrown`
31. `strikes`
32. `parser_version`
33. `diagnostic_only`
34. `production_ready`

`diagnostic_only` is fixed to `true`; `production_ready` is fixed to `false`.
`learning_eligible` is absent and rejected as outcome/decision leakage.
Unknown normalized-event fields are rejected.

`source_record_id` encodes the source game record and pitcher as
`<game_pk>:pitcher:<pitcher_id>` and is therefore stable across pitcher-list
reorder. `appearance_sequence` is observed source-ordering metadata only and
never participates in logical revision identity, which is `(game_pk,
pitcher_id)`. `source_record_id` is scoped by source lineage
`(source_provider, source_endpoint_or_feed_id)`; the same `source_record_id`
string may recur across lineages and is never treated as a cross-lineage
revision (see Section 9).

Normalized records may carry `final`, `corrected`, or `superseded`. The
contract recognizes `malformed` and `source_unavailable` as diagnostic states,
but those states cannot be materialized as normalized pitcher events.

## 4. Innings Semantics

`innings_outs` is canonical. Baseball display notation is parsed as:

- `0.0` = 0 outs
- `X.1` = `3X + 1` outs
- `X.2` = `3X + 2` outs

Any other suffix, numeric decimal input, sign, or annotation is invalid.
Display notation must exactly agree with `innings_outs`.

All required statistics are non-negative integers. Required FIP components are
strikeouts, walks, hit by pitch, and home runs allowed. Missing components fail
closed. `earned_runs <= runs_allowed` and `strikes <= pitches_thrown`.
Pitch-count fields may both be explicit null; one-sided availability is
rejected. `intentional_walks` may be explicit null.

## 5. Source Adapter

`adapt_finalized_boxscore_payload` is pure and accepts:

- a caller-supplied decoded payload
- explicit `collected_at_utc`
- explicit source provider
- explicit source endpoint/feed ID
- explicit parser version

It performs no network or file I/O. It preserves input game order, home then
away side order, and pitcher-list order. `appearance_sequence` is deterministic
within each side and is observed metadata only; the generated `source_record_id`
is `<game_pk>:pitcher:<pitcher_id>` and stays stable when a corrected payload
reorders the pitcher list. `starter_flag` must be explicit and is never inferred
from sequence. Contract v1 stores exactly one row per `(game_pk, pitcher_id)`: a
pitcher listed twice on one side, or on both sides of one game, fails the
affected side or whole game closed.

The adapter accepts finalized/corrected decoded boxscores, including a game
that was suspended and later finalized. It rejects current live, provisional,
cancelled, incomplete, aggregate-only, estimated, averaged, distributed, or
proxy source shapes. It does not infer IDs from names or infer `gamePk` from
date/team composites. It does not calculate FIP.

## 6. Diagnostics

Rejected inputs return explicit `AdapterDiagnostic` entries and counts.
Covered diagnostic classes include:

- malformed payload/game/pitcher list
- source unavailable
- game not final
- invalid record status
- missing team side or per-pitcher rows
- team aggregate without pitcher-game rows
- missing/incomplete pitcher line
- empty finalized-side pitcher list
- invalid innings notation
- ambiguous duplicate pitcher list
- same pitcher on both sides of one game
- malformed normalized pitcher event
- proxy or outcome-leakage rejection

Malformed pitchers are not silently discarded.

## 7. Fingerprint, Deduplication, and Revision

The payload fingerprint is SHA-256 over deterministic canonical JSON of all
normalized fields except the fingerprint itself.

The exact-duplicate key includes:

- source provider
- source record ID
- `game_pk`
- `pitcher_id`
- `appearance_sequence`
- collection timestamp
- payload fingerprint

An exact duplicate is a no-op. A correction with changed status, collection
time, content, or list position has a distinct fingerprint/key and appends as a
new physical revision. Physical storage history is intentionally finer-grained
than logical identity: it preserves every observation, while as-of selection
(Section 9) resolves all physical revisions of one `(game_pk, pitcher_id)` to a
single logical pitcher-game.

## 8. Append-Only Behavior

`PitcherGameEventStore` requires a caller-supplied path and has no default
runtime location. It writes UTF-8 JSONL only when `append` is called.

Behavior:

- no write on import
- no directory creation
- missing parent fails explicitly
- exact duplicates are skipped
- corrections append
- prior rows remain present
- malformed JSON, field sets, or fingerprints fail closed before append
- no DB is used

No concurrency-safety claim is made.

## 9. Prior-Only Selection

`select_prior_pitcher_events` includes a revision only when:

- pitcher ID matches
- target game is excluded
- `game_start_utc < target_information_cutoff_utc`
- finalized time is known by the cutoff
- collection time is known by the cutoff
- latest known revision is `final` or `corrected`
- latest known revision is not `superseded`

Revisions are grouped by the stable logical identity `(game_pk, pitcher_id)`.
`appearance_sequence` is ordering metadata only and never partitions revision
history, so a corrected payload that reorders the pitcher list resolves to one
revision of the same pitcher-game rather than a second appearance. A later known
correction replaces the earlier row for selection without deleting history.
Differing latest revisions that share the latest collection timestamp fail
closed as `ambiguous_revision`. Because contract v1 stores one row per
`(game_pk, pitcher_id)`, two simultaneous logical rows for the same pitcher-game
are ambiguous and fail closed rather than both being returned.

#### Source lineage and cross-provider safety

The logical event identity is `(game_pk, pitcher_id)`. The source lineage is the
existing `(source_provider, source_endpoint_or_feed_id)` pair, exposed as
`PitcherGameEvent.source_lineage_key`. The complete source identity is the
lineage plus `source_record_id` (which is itself scoped by lineage; the same
`source_record_id` string may legitimately recur across lineages).

Revision resolution happens **only within one source lineage**. Different
providers, and different feed IDs from one provider, are **not** automatic
revisions of one another. The selector evaluates, per logical pitcher-game and
using only rows already known by the cutoff, how many distinct source lineages
are eligible:

- exactly one eligible lineage → normal within-lineage revision resolution
  (final/corrected, superseded exclusion, same-time `ambiguous_revision`);
- more than one eligible lineage → fail closed with the deterministic diagnostic
  `ambiguous_cross_source_lineage` (identifying `game_pk` and `pitcher_id`),
  excluding the event with no rows returned.

There is **no** latest-provider-wins, **no** provider precedence, **no** source
voting/consensus, **no** statistic averaging, and **no** silent cross-source
deduplication — even byte-identical content from two lineages stays ambiguous
until a separate explicit reconciliation contract is designed. The cross-source
check takes precedence over within-lineage `ambiguous_revision`. Because lineage
detection runs after the strict cutoff filter, a different-lineage row collected
after the cutoff is excluded first and cannot retroactively make earlier
single-lineage knowledge ambiguous.

The result reports diagnostics, the information cutoff, and the maximum
included game start. It does not calculate FIP or model features.

### Post-hoc backfill limitation

The collected-at gate is strict: a revision is eligible only when its
`collected_at_utc` is at or before the target cutoff. A finalized historical
game collected only later is therefore excluded at an earlier cutoff even though
it finalized earlier. This intentionally prevents a retrospective backfill from
masquerading as contemporaneously available evidence. Consequently this module
is observational storage, not leakage-free historical point-in-time evidence
before each row's actual collection time. `game_finalized_at_utc` alone does not
establish contemporaneous availability; trustworthy historical PIT eligibility
would require an additional verified publication/archive-availability timestamp,
which contract v1 does not assert.

## 10. Fixture Inventory

The fixture file contains 44 named synthetic scenarios and eight reusable
payload groups. All IDs, names, dates, and statistics are fictional; most use
2099 dates, while the post-hoc backfill scenarios use 2024/2025/2026 dates.
Several scenarios (including the cross-source lineage cases) are constructed
directly in tests from the reusable payloads rather than as standalone payload
objects, so the catalog count is not a count of full payloads.

Coverage includes:

- starter, reliever, opener, bulk pitcher, and zero-out appearance
- multiple home/away pitchers
- exact duplicate, correction, superseded selection, and ambiguity
- doubleheader games with distinct `gamePk`
- suspended-then-finalized, live, and cancelled games
- missing game/pitcher/team identity
- malformed innings and innings/outs disagreement
- negative and inconsistent statistics
- missing FIP components
- proxy and outcome-leakage rejection
- team aggregate rejection
- target/future/late-data exclusion
- corrected pitcher-list reorder resolving to one logical revision
- stable source_record_id across reorder
- same pitcher on both sides rejected
- post-hoc backfill excluded before its collection time
- cross-provider later row failing closed (no silent overwrite)
- cross-provider same-timestamp and identical-content failing closed
- cross-provider row after cutoff not creating historical ambiguity
- same provider with different feed IDs failing closed
- cross-source ambiguity blocking the whole selection (no partial escape)
- malformed JSONL
- stake independence

## 11. Test Results

- New direct suite: PASS, 119 passed
- P202E collector: PASS, 49 passed
- P202D snapshot intake: PASS, 89 passed
- Workflow guards: PASS, 157 passed
- Combined relevant suites: PASS, 414 passed
- Required `py_compile`: PASS
- `git diff --check`: PASS

The workflow guard group contains:

- `tests/test_p180_strategy_leaderboard.py`
- `tests/test_run_mlb_tsl_paper_recommendation_simulation_gate.py`
- `tests/test_mlb_paper_evaluator.py`
- `tests/test_mlb_paper_evaluation_runner.py`
- `tests/test_mlb_daily_scheduler.py`

## 12. Full Regression Status

Full repository regression: NOT RUN.

Reason: the prompt explicitly made it optional and the focused plus mandated
405-test regression set was proportional to this isolated four-file task.

## 13. Limitations

- No live or historical MLB payload was fetched.
- No real-season completeness or coverage claim is made.
- The existing real-boxscore parser branch remains unimplemented.
- The module requires decoded caller input with explicit role/provenance data.
- The JSONL store is not advertised as concurrency-safe.
- No point-in-time FIP, rolling feature, model, or betting output is produced.
- Post-hoc historical backfill is observational only; it is not leakage-free
  historical PIT evidence before each row's actual collection time, and
  `game_finalized_at_utc` alone does not establish contemporaneous availability.
- Production readiness remains false.
- P202F's live transport authorization blocker remains unresolved.

## 14. Explicit Non-Actions

This task did not:

- call StatsAPI or any network endpoint
- execute a live acquisition script
- backfill historical data
- write real MLB runtime data
- create a default runtime path
- write a DB or migrate a schema
- integrate with scheduler, probable starters, recommendations, evaluator, or
  models
- fit, refit, or run inference
- emit `learning_eligible=true`
- unlock a provider
- alter registry, strategy, champion, or controlled-apply state
- modify governance
- stage, commit, push, open a PR, or merge

## 15. Required Completion Check

- Actually complete: YES
- Test result: PASS
- New direct test count: 119
- P202E test count: 49
- P202D test count: 89
- Workflow test count: 157
- Combined relevant test count: 414
- Full regression: NOT RUN
- Source-shape evidence status: GROUNDED IN EXISTING PHASE62/63 FIXTURE/PARSER CONVENTIONS
- Pitcher-event schema status: COMPLETE, 34 EXACT FIELDS
- Innings validation status: PASS
- FIP-component completeness status: PASS, K/BB/HBP/HR REQUIRED
- Proxy rejection status: PASS
- Adapter diagnostics status: PASS
- Idempotency status: PASS
- Revision-history status: PASS, LOGICAL IDENTITY `(game_pk, pitcher_id)`, STABLE ACROSS PITCHER-LIST REORDER
- Source-lineage status: PASS, LINEAGE `(source_provider, source_endpoint_or_feed_id)`; MULTIPLE ELIGIBLE LINEAGES FAIL CLOSED `ambiguous_cross_source_lineage`; NO LATEST-WINS / PRECEDENCE / CONSENSUS / SILENT DEDUP
- Append-only status: PASS
- Prior-only selection status: PASS
- Target-game exclusion status: PASS
- No-network status: PASS
- Runtime-write status: NONE OUTSIDE PYTEST `tmp_path`
- Single blocker: NONE FOR P202G-B; LIVE TRANSPORT AUTHORIZATION REMAINS A SEPARATE HOLD
- P202G-B modified/untracked files: EXACTLY FOUR WHITELIST FILES
- Staged files: NONE
- Current branch: `main`
- Local HEAD / origin/main: BOTH `6de072b25dcdea722df7f4b6ebe5299cc4cd34b9`
- Open PR count: 0
- `active_task.md` status: STALE P199 PLAN-ONLY; NO COMPETING IMPLEMENTATION AUTHORIZATION
- DB/API/provider/production/registry/controlled_apply status: UNCHANGED / NOT USED
- Model/strategy/champion mutation status: NONE
- Commit/push status: NOT PERFORMED
- Whether next round is allowed: ONLY WITH A NEW EXPLICITLY AUTHORIZED SCOPE; LIVE P202G-A REMAINS HOLD
- Worker/thinking recommendation: OPUS-CLASS, MEDIUM-TO-STRONG
- Same/new conversation recommendation: NEW CONVERSATION FOR THE NEXT SCOPED TASK
- Final Classification: `P202G_B_PITCHER_EVENT_BACKFILL_SKELETON_COMPLETE`
