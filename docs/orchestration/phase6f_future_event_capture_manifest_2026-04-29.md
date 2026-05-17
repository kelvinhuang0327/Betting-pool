# Phase 6F — Future-Event Capture Manifest for MLB/KBO/NPB CLV Pipeline

**Date:** 2026-04-29
**Type:** Manifest design document — NOT an implementation
**Predecessor:** Phase 6E (`0cbfdec`) — `docs/orchestration/phase6e_domain_commitment_decision_2026-04-29.md`
**Domain commitment:** `DOMAIN_COMMITMENT_MLB_KBO_NPB`
**Author:** Betting-pool Orchestrator Research Agent

---

## 1. Executive Summary

Phase 6E committed Betting-pool's CLV validation target to the
**MLB/KBO/NPB regular-season domain** (`DOMAIN_COMMITMENT_MLB_KBO_NPB`). Existing TSL odds
infrastructure already covers this domain: 28,941 rows, 383 canonical matches, 4,796
CLV-eligible OPENING+CLOSING selection pairs are already in
`data/derived/odds_snapshots_2026-04-29.jsonl`.

**This document is the Phase 6F future-event capture manifest.** It defines:

- which leagues, markets, and match types to capture going forward
- the full capture lifecycle for each match (discovery → opening → intermediate →
  prediction → closing → decision → settlement → CLV record)
- snapshot schedule with explicit timing windows
- prediction registry alignment requirements
- settlement alignment requirements
- quality gates before formal CLV validation is permitted
- a proposed manifest schema (documentation-only; not loaded by production at this stage)
- failure mode handling
- next implementation roadmap and Phase 6G prompt

**No runtime changes are made by this document.**
No crawler, DB, model, orchestrator, or existing data files are modified.

---

## 2. Evidence Recap

### 2.1 Files Read

| File | Status | Key Finding |
|---|---|---|
| `docs/orchestration/phase6e_domain_commitment_decision_2026-04-29.md` | ✅ Read | `DOMAIN_COMMITMENT_MLB_KBO_NPB`; MLB/KBO/NPB wins 7/9 decision criteria; Phase 6G prompt provided |
| `docs/orchestration/phase6d_clv_readiness_decision_2026-04-29.md` | ✅ Read | CLV readiness=0.0%; Option C (future-event) primary; domain commitment required |
| `docs/orchestration/phase6a_clv_data_contract_2026-04-29.md` | ✅ Read | Full canonical schema for MatchIdentity, OddsSnapshot, ModelPrediction, BettingDecision, SettlementResult, CLVValidationRecord |
| `docs/orchestration/phase6b_odds_snapshot_adapter_report_2026-04-29.md` | ✅ Read | 28,941 rows; 383 matches; OPENING/CLOSING classification logic; league=unknown_league blocker |
| `docs/orchestration/phase6c_match_identity_bridge_report_2026-04-29.md` | ✅ Read | Team alias: MLB=30, KBO=10, NPB=12 RESOLVED; UNMATCHED=6 (league code gaps) |
| `scripts/build_odds_snapshots.py` | ✅ Read | 34KB Phase 6B adapter; market normalization map; canonical_match_id construction logic; CLOSING_WINDOW_MINUTES default=30 |
| `scripts/build_match_identity_bridge.py` | ✅ Read | 34KB Phase 6C adapter; UUID5-based canonical IDs; team alias resolution logic |
| `data/derived/odds_snapshots_2026-04-29.jsonl` | ✅ Sampled | OPENING=4,796; CLOSING=4,796; INTERMEDIATE=15,215; POST_MATCH=2,313; AMBIGUOUS=1,821 |
| `data/derived/team_alias_map_2026-04-29.csv` | ✅ Referenced | 66 entries; 59 RESOLVED; 6 TEAM_CODE_MISSING |
| `config/settings.py` | ✅ Read | EV_STRONG=0.07, EV_MEDIUM=0.03, KELLY_FRACTION=0.15, DRAWDOWN_MAX=0.20 |

### 2.2 Current Blockers the Manifest Must Address

| Blocker | Source | Required Manifest Section |
|---|---|---|
| `league=unknown_league` in all current snapshots | Phase 6B: no league normalization table at capture time | §3 Capture Domain — define league codes at ingestion |
| No per-match MLB/KBO/NPB prediction outputs | Phase 6D: walk-forward not persisted | §6 Prediction Registry Alignment |
| No settlement data for MLB/KBO/NPB | Phase 6D: source undefined | §7 Settlement Alignment |
| Closing window is "last pre-match snapshot" not a fixed window | Phase 6B: CLOSING_WINDOW_MINUTES=30 but actual gap varies 27min–18h | §5 Snapshot Schedule — define explicit closing window |
| `canonical_match_id` uses `unknown_league` as league component | Phase 6B: league not resolved at capture time | §3 + §9 — normalize at capture, not post-hoc |
| 6 team codes UNMATCHED (TEAM_CODE_MISSING) | Phase 6C: gaps in KBO/NPB alias table | §11 Failure Modes |
| CLV_high sample = 38 (need ≥200) | Phase 5.5 | §8 Quality Gates — sample gate before aggregate validation |

### 2.3 Timing Evidence from Current Dataset

From observed OPENING/CLOSING pairs in `odds_snapshots_2026-04-29.jsonl`:

| Metric | Observed Range |
|---|---|
| Opening lead (before match_time_utc) | 1.0h – 23.7h |
| Closing lead (before match_time_utc) | 27.6 min – 17.9h |
| Median closing lead | ~3–5h (estimated; varies widely by league timezone) |

> **Note:** The current "CLOSING" classification assigns the label to the last
> pre-match snapshot regardless of timing. This is not a true closing line.
> Phase 6F mandates a **defined closing window** (see §5) for future captures.

---

## 3. Capture Domain

### 3.1 Sport

- `sport = "baseball"` (only sport in scope for Phase 6F–6I)

### 3.2 Leagues In Scope

| League | Code | Teams | Season | Priority |
|---|---|---|---|---|
| Major League Baseball | `MLB` | 30 | April–October (UTC) | 1 (primary) |
| Korea Baseball Organization | `KBO` | 10 | March–October (KST = UTC+9) | 2 |
| Nippon Professional Baseball | `NPB` | 12 | March–October (JST = UTC+9) | 3 |

**WBC is explicitly out of scope** for Phase 6F capture. WBC 2026 is complete;
WBC 2029 can be revisited as a separate future phase.

### 3.3 Market Types — Initial Scope

| Market | TSL Code | Contract Code | Priority | CLV Usage |
|---|---|---|---|---|
| Moneyline | `MNL` | `ML` | 1 — Primary | YES |
| Run-line / Handicap | `HDC` | `RL` | 2 — Secondary | YES |
| Over-Under Total | `OU` | `OU` | 3 — Tertiary | YES |

### 3.4 Market Types — Excluded Initially

| Market | TSL Code | Reason |
|---|---|---|
| Odd-Even | `OE` | Low edge relevance; model not calibrated |
| Alternative Total | `TTO` | Mapped to OU in Phase 6B; expand only after ML validated |
| Exotic / Prop | varies | Out of scope until base markets validated |

Excluded markets may be added after Phase 6J CLV validation confirms ML performance.

### 3.5 Bookmaker / Source Expectations

| Field | Expected Value |
|---|---|
| Current source | `TSL_BLOB3RD` (via `data/tsl_odds_history.jsonl`) |
| `bookmaker` field | `"TSL_BLOB3RD"` (retain for traceability) |
| Future sources | To be defined in Phase 6G; do not expand bookmaker list in this manifest |

### 3.6 Timezone Requirements

- All timestamps stored in **UTC** (`snapshot_time_utc`, `match_time_utc`, `prediction_time_utc`, `settled_at_utc`)
- Local timezone conversion (KST/JST → UTC) applied at ingestion time
- `match_time_utc` is the canonical first-pitch time; no local-time fields stored in CLV records
- Daylight Saving Time changes (MLB: US timezones observe DST) must be handled at fetch time

---

## 4. Capture Lifecycle

Each future MLB/KBO/NPB match must progress through the following lifecycle stages.
A match is CLV-eligible only if all required steps are satisfied.

### Step 1 — Match Discovery

| Item | Requirement |
|---|---|
| **Input** | TSL or alternative schedule feed listing future match with teams, time, league |
| **Output** | `MatchIdentity` record with `canonical_match_id`, `match_time_utc`, `home_team`, `away_team`, `league` |
| **Timestamp** | Discovery must occur before opening odds are fetched |
| **Leakage guard** | Match must be in `SCHEDULED` status; no result data present |
| **Failure** | If league cannot be inferred: set `league=UNKNOWN`, flag `LEAGUE_INFERRED`, escalate to §11 failure mode |

**canonical_match_id format for MLB/KBO/NPB:**
```
baseball:{league}:{YYYYMMDD_UTC}:{home_team_code}:{away_team_code}
```
Example: `baseball:MLB:20260501:NYY:BOS`

> **Critical:** The `unknown_league` placeholder used in Phase 6B output must NOT appear
> in future captures. League must be resolved at discovery time.

### Step 2 — Opening Odds Snapshot

| Item | Requirement |
|---|---|
| **Input** | Scheduled match + available odds from bookmaker |
| **Output** | `OddsSnapshot` rows with `snapshot_type=OPENING` for all in-scope market/selection pairs |
| **Timing** | First available odds fetch after match is discovered; at least 6h before `match_time_utc` |
| **Leakage guard** | `snapshot_time_utc < match_time_utc` — hard fail if violated |
| **Required fields** | All Phase 6A `OddsSnapshot` fields; `league` must not be `unknown_league` |
| **Failure** | If odds not available: record `OPENING_MISSING` flag; match is not CLV-eligible |

### Step 3 — Intermediate Odds Snapshots

| Item | Requirement |
|---|---|
| **Input** | Scheduled match with OPENING already captured |
| **Output** | `OddsSnapshot` rows with `snapshot_type=INTERMEDIATE` |
| **Timing** | Periodic fetches between OPENING and CLOSING window (see §5) |
| **Leakage guard** | All `snapshot_time_utc < match_time_utc` |
| **Failure** | Missing intermediate snapshots do not block CLV eligibility; only OPENING and CLOSING are required |

### Step 4 — Prediction Generation

| Item | Requirement |
|---|---|
| **Input** | Match discovery record + opening odds + feature data for team/pitcher/weather/regime |
| **Output** | `ModelPrediction` row with `canonical_match_id`, `prediction_time_utc`, `predicted_probability`, `model_version`, `feature_version` |
| **Timing** | `prediction_time_utc` must be: (a) after OPENING snapshot availability, (b) before CLOSING window start, (c) before `match_time_utc` |
| **Leakage guard** | Model must not use any data with `event_time >= prediction_time_utc` |
| **Required fields** | All Phase 6A `ModelPrediction` fields; `model_version` and `feature_version` must not be empty |
| **Failure** | If prediction is missing: match is not CLV-eligible for that market |

### Step 5 — Pre-Match Closing Odds Snapshot

| Item | Requirement |
|---|---|
| **Input** | Scheduled match with OPENING + prediction already captured |
| **Output** | `OddsSnapshot` rows with `snapshot_type=CLOSING` |
| **Timing** | Last snapshot within the defined closing window before `match_time_utc` (see §5) |
| **Leakage guard** | `snapshot_time_utc < match_time_utc` — hard fail if violated; `prediction_time_utc < snapshot_time_utc` for CLOSING |
| **Failure** | If CLOSING missing: match not CLV-eligible; flag `CLOSING_MISSING` |

### Step 6 — Betting Decision Record

| Item | Requirement |
|---|---|
| **Input** | Prediction + CLOSING odds |
| **Output** | `BettingDecision` row: `bet_decision = BET or NO_BET`, `expected_value`, `stake_fraction` |
| **Timing** | `decision_time_utc` must be after CLOSING snapshot and before `match_time_utc` |
| **Leakage guard** | Decision must not use post-match data |
| **Required fields** | Phase 6A `BettingDecision` fields; `model_version` must match prediction |
| **Note** | `NO_BET` decisions are retained in the validation set for CLV distribution analysis |

### Step 7 — Settlement Result Capture

| Item | Requirement |
|---|---|
| **Input** | Confirmed final score from result source |
| **Output** | `SettlementResult` row with `hit`, `realized_roi`, `closing_line_value`, `settlement_quality_flags` |
| **Timing** | `settled_at_utc > match_time_utc`; typically within 4 hours of final out |
| **Leakage guard** | Settlement must not be captured before `match_time_utc` |
| **Required fields** | Phase 6A `SettlementResult` fields; `result_source` must be in approved list (see §7) |
| **Failure** | If settlement missing: CLVValidationRecord has `settlement_ref=null`; excluded from realized ROI computation but retained for CLV signal analysis |

### Step 8 — CLV Validation Record Generation

| Item | Requirement |
|---|---|
| **Input** | All prior lifecycle records: MatchIdentity + OPENING snapshot + CLOSING snapshot + ModelPrediction + BettingDecision + SettlementResult |
| **Output** | `CLVValidationRecord` row: `clv_proxy`, `implied_prob_open`, `implied_prob_close`, `predicted_probability`, `hit`, `realized_roi` |
| **CLV_proxy formula** | `clv_proxy = predicted_probability - implied_probability_close` |
| **Timing** | Generated after settlement; input of aggregate CLV analysis (Phase 6J+) |
| **Leakage guard** | All component timestamps must satisfy the full causal chain: `prediction_time_utc < closing_snapshot_time_utc < match_time_utc < settled_at_utc` |
| **Failure** | Any hard-fail leakage rule failure excludes the record from CLV aggregate |

---

## 5. Snapshot Schedule

> **PROVISIONAL_CAPTURE_SCHEDULE_REQUIRES_RECALIBRATION**
>
> The schedule below is a conservative starting proposal. Actual feasibility depends
> on TSL crawl frequency, bookmaker suspension windows, and network reliability.
> Phase 6G dry-run will validate against current observed patterns.

### 5.1 Proposed Schedule

| Window | Snapshot Type | Timing Relative to `match_time_utc` | Required for CLV? | CLV Usage |
|---|---|---|---|---|
| Match discovery | (identity only) | ≥6h before match | YES | Not a snapshot |
| First fetch after discovery | `OPENING` | ≥6h before match (earliest available) | YES | CLV opening line |
| Periodic refresh | `INTERMEDIATE` | Every 3h between OPENING and closing window | NO | Price movement analysis (not CLV compute) |
| Pre-close fetch | `INTERMEDIATE` | ~2h before match | NO | Safety buffer before closing window |
| Closing window start | `CLOSING` candidate | 90 min before `match_time_utc` | YES | CLV closing line |
| Final pre-match fetch | `CLOSING` (confirmed) | Within 30–90 min before `match_time_utc` | YES | Last available odds used for CLV |
| Post-match | `POST_MATCH` | After `match_time_utc` | NO | Audit only — excluded from CLV |

### 5.2 Closing Window Definition

For Phase 6F forward, the closing window is defined as:

```
CLOSING_WINDOW_START_MINUTES = 90   # start of closing capture zone before match
CLOSING_WINDOW_END_MINUTES   = 10   # hard stop before match (avoid in-play contamination)
```

A snapshot is classified `CLOSING` if:
```
10 ≤ (match_time_utc - snapshot_time_utc).total_minutes ≤ 90
```

If no snapshot falls within this window, the latest pre-match snapshot is used
with quality flag `CLOSING_WINDOW_MISS` added.

**Rationale:** Current Phase 6B data shows closing lead times ranging from 27 min
to 17.9 hours — the 30-minute default CLOSING_WINDOW_MINUTES in Phase 6B does not
describe when the snapshot was fetched, only the theoretical threshold. Phase 6F
standardizes the definition for prospective captures.

### 5.3 League-Specific Schedule Notes

| League | Typical First Pitch (Local) | UTC Equivalent | Notes |
|---|---|---|---|
| MLB | 13:00–22:00 ET (UTC-4/5) | 17:00–03:00 UTC | Double-headers common in summer |
| KBO | 17:00–18:00 KST (UTC+9) | 08:00–09:00 UTC | Evening games Mon–Fri; 14:00 KST on weekends |
| NPB | 17:00–18:00 JST (UTC+9) | 08:00–09:00 UTC | Similar to KBO; Friday night games shift to 18:30 |

> Double-headers and postponements require deduplication logic at the `canonical_match_id`
> construction step.

---

## 6. Prediction Registry Alignment

### 6.1 Required Prediction Timing Rules

For a `ModelPrediction` to be CLV-eligible:

| Rule | Constraint |
|---|---|
| **T1** | `prediction_time_utc < match_time_utc` |
| **T2** | `prediction_time_utc < closing_snapshot_time_utc` |
| **T3** | `prediction_time_utc > opening_snapshot_time_utc` (if market features are used) |

Rule T2 is the strongest leakage guard: prediction must not see closing line before
making a probability estimate.

### 6.2 Required New Fields in prediction_registry Schema

The current `prediction_registry.jsonl` (WBC-only, 66 rows, all NO_BET) requires the
following schema extensions for MLB/KBO/NPB CLV validation:

| Field | Type | Description | Gap? |
|---|---|---|---|
| `canonical_match_id` | string | FK → MatchIdentity; replaces WBC `game_id` for MLB/KBO/NPB | **MISSING** — must be added |
| `prediction_time_utc` | ISO8601 | Exact inference timestamp in UTC | **MISSING** — currently approximated by `recorded_at_utc` |
| `model_version` | string | e.g. `"gbm_stack_v2.1"` | **MISSING** — not stored |
| `feature_version` | string | e.g. `"features_32_v1"` | **MISSING** — not stored |
| `training_window_id` | string | Walk-forward fold identifier | **MISSING** — not stored |
| `leakage_guard_version` | string | Version of leakage rules applied at inference | **MISSING** — not stored |
| `market_type` | string | `ML` / `RL` / `OU` per Phase 6A | Partially present |
| `market_line` | string | RL line or OU total; null for ML | Partially present |
| `selection` | string | `home` / `away` / `over` / `under` | Partially present |
| `predicted_probability` | float | Model win probability for the selection | Present (as `home_prob` / `away_prob`) |
| `league` | string | `MLB` / `KBO` / `NPB` | **MISSING** for MLB/KBO/NPB rows |

**Implementation note:** These schema extensions are **design-only** in Phase 6F.
The actual prediction pipeline changes belong to Phase 6G and Phase 6H.

### 6.3 Backward Compatibility

WBC `game_id` format (`A05`, `B06`, etc.) must remain valid in the prediction_registry.
New MLB/KBO/NPB rows will use `canonical_match_id` as the primary key; `game_id` will
be null or omitted for non-WBC rows.

---

## 7. Settlement Alignment

### 7.1 Settlement Data Sources

| League | Proposed Source | Source Type | Latency |
|---|---|---|---|
| MLB | To be confirmed in Phase 6H | Authoritative external API or scrape | Typically ≤4h post-game |
| KBO | To be confirmed in Phase 6H | KBO official or third-party aggregator | Typically ≤6h post-game |
| NPB | To be confirmed in Phase 6H | NPB official or third-party aggregator | Typically ≤6h post-game |

> **Note:** No settlement data source for MLB/KBO/NPB is confirmed in the current repo.
> `data/wbc_backend/reports/postgame_results.jsonl` covers WBC only (B06, C09 WBC codes).
> Settlement source selection belongs to Phase 6H and is out of scope for Phase 6F.

### 7.2 Required Settlement Record Fields

Per Phase 6A `SettlementResult` entity:

| Field | Required | Notes |
|---|---|---|
| `settlement_id` | YES | UUID |
| `canonical_match_id` | YES | FK → MatchIdentity |
| `decision_ref` | YES | FK → BettingDecision |
| `settled_at_utc` | YES | Must satisfy `settled_at_utc > match_time_utc` |
| `result_source` | YES | Must be in approved source list (defined in Phase 6H) |
| `final_score` | YES | `{home_score: int, away_score: int}` |
| `market_type` | YES | Matches prediction market_type |
| `outcome` | YES | `home_win` / `away_win` / `over` / `under` / `push` |
| `hit` | YES | Boolean: did the bet selection win? |
| `realized_roi` | CONDITIONAL | Required if `bet_decision = BET`; null if `NO_BET` |
| `closing_line_value` | YES | `predicted_probability - implied_probability_close` |
| `settlement_quality_flags` | YES | e.g. `[]` or `["UNVERIFIED_SOURCE", "RAIN_DELAY"]` |

### 7.3 Settlement Quality Flags

| Flag | Meaning |
|---|---|
| `UNVERIFIED_SOURCE` | Result source not in primary approved list |
| `SUSPENDED_MARKET` | Bookmaker suspended market before match; odds not comparable |
| `POSTPONED_GAME` | Match was postponed; settlement deferred |
| `RAIN_DELAY_OFFICIAL` | Game ended due to rain; outcome may be official or unofficial |
| `PUSH_OUTCOME` | RL market resulted in push; no winner |
| `SCORE_DISCREPANCY` | Two sources disagree on final score by ≥1 run |

---

## 8. Quality Gates

The following gates must all pass before a record contributes to formal aggregate
CLV validation. Records failing any hard gate are excluded from the CLV aggregate
but retained in the raw dataset for audit.

### 8.1 Per-Record Hard Gates

| Gate | Check | Failure Action |
|---|---|---|
| `G1` | `OPENING` snapshot exists for `selection_key` | Exclude record; flag `OPENING_MISSING` |
| `G2` | `CLOSING` snapshot exists for `selection_key` | Exclude record; flag `CLOSING_MISSING` |
| `G3` | `prediction_time_utc < closing_snapshot_time_utc` | Hard leakage fail; exclude record; flag `LEAKAGE_PREDICTION_AFTER_CLOSING` |
| `G4` | `prediction_time_utc < match_time_utc` | Hard leakage fail; flag `LEAKAGE_PREDICTION_POST_MATCH` |
| `G5` | `closing_snapshot_time_utc < match_time_utc` | Hard leakage fail; flag `LEAKAGE_CLOSING_POST_MATCH` |
| `G6` | `bridge_confidence >= 0.90` (canonical_match_id resolution) | Exclude; flag `BRIDGE_LOW_CONFIDENCE` |
| `G7` | `market_type` is `ML`, `RL`, or `OU` | Exclude; flag `UNSUPPORTED_MARKET_TYPE` |
| `G8` | `league` is `MLB`, `KBO`, or `NPB` | Exclude; flag `OUT_OF_SCOPE_LEAGUE` |

### 8.2 Aggregate Validation Gate

| Gate | Check | Notes |
|---|---|---|
| `A1` | Matched + settled records ≥ 200 per CLV bucket per market regime | Minimum required before computing CLV_high vs benchmark ROI |
| `A2` | At least 3 distinct calendar months represented in sample | Prevents seasonal overfitting |
| `A3` | At least 2 of 3 leagues (MLB, KBO, NPB) represented | Avoids single-league bias |

> **Current status:** `A1` is not satisfied for any bucket or league. CLV_high sample = 38
> (from Phase 5.5 WBC data). Aggregate validation is blocked until sample accumulation
> is demonstrated by the Phase 6G dry-run quality checker.

---

## 9. Manifest Schema

The proposed manifest schema below is **documentation-only**. It is not loaded by
any production runtime at this stage. Phase 6G will produce a dry-run quality checker
that reads this schema as configuration input.

### 9.1 Schema Definition

```
manifest_version:     string    — semver e.g. "1.0.0"
target_domain:        string    — "MLB/KBO/NPB regular season baseball"
domain_token:         string    — "DOMAIN_COMMITMENT_MLB_KBO_NPB"
sport:                string    — "baseball"
leagues:              list[str] — ["MLB", "KBO", "NPB"]
market_types:         list[str] — ["ML", "RL", "OU"]
excluded_market_types: list[str] — ["OE", "TTO", "EXOTIC"]

snapshot_schedule:
  opening_min_lead_hours:    int     — minimum hours before match for OPENING fetch
  closing_window_start_min:  int     — minutes before match to begin CLOSING window
  closing_window_end_min:    int     — minutes before match hard stop
  intermediate_interval_h:   int     — hours between INTERMEDIATE fetches

prediction_requirements:
  must_precede_closing:      bool    — true
  must_precede_match:        bool    — true
  required_fields:           list[str]
  forbidden_features:        list[str] — features that carry future information

settlement_requirements:
  approved_sources:          list[str]
  max_latency_hours:         int     — max hours post-match before settlement required
  required_fields:           list[str]

leakage_guards:
  hard_fail_rules:           list[str] — G3, G4, G5 from §8
  soft_warn_rules:           list[str]

quality_gates:
  per_record:                list[str] — G1–G8
  aggregate:                 list[str] — A1–A3

sample_targets:
  min_clv_high_bets:         int     — 200
  min_calendar_months:       int     — 3
  min_leagues:               int     — 2

output_paths:
  odds_snapshots:            string
  model_predictions:         string
  betting_decisions:         string
  settlement_results:        string
  clv_validation_records:    string
  quality_report:            string

owner_notes:           string    — freeform notes
```

### 9.2 JSON Example Block

```json
{
  "manifest_version": "1.0.0",
  "target_domain": "MLB/KBO/NPB regular season baseball",
  "domain_token": "DOMAIN_COMMITMENT_MLB_KBO_NPB",
  "sport": "baseball",
  "leagues": ["MLB", "KBO", "NPB"],
  "market_types": ["ML", "RL", "OU"],
  "excluded_market_types": ["OE", "TTO", "EXOTIC"],
  "snapshot_schedule": {
    "opening_min_lead_hours": 6,
    "closing_window_start_min": 90,
    "closing_window_end_min": 10,
    "intermediate_interval_h": 3,
    "note": "PROVISIONAL_CAPTURE_SCHEDULE_REQUIRES_RECALIBRATION"
  },
  "prediction_requirements": {
    "must_precede_closing": true,
    "must_precede_match": true,
    "required_fields": [
      "canonical_match_id", "prediction_time_utc", "predicted_probability",
      "model_version", "feature_version", "market_type", "selection"
    ],
    "forbidden_features": ["post_game_result", "final_score", "live_score"]
  },
  "settlement_requirements": {
    "approved_sources": ["TBD_IN_PHASE_6H"],
    "max_latency_hours": 6,
    "required_fields": [
      "canonical_match_id", "settled_at_utc", "result_source",
      "final_score", "outcome", "hit", "closing_line_value"
    ]
  },
  "leakage_guards": {
    "hard_fail_rules": ["G3", "G4", "G5"],
    "soft_warn_rules": ["G1", "G2"]
  },
  "quality_gates": {
    "per_record": ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8"],
    "aggregate": ["A1", "A2", "A3"]
  },
  "sample_targets": {
    "min_clv_high_bets": 200,
    "min_calendar_months": 3,
    "min_leagues": 2
  },
  "output_paths": {
    "odds_snapshots": "data/derived/future_odds_snapshots_{date}.jsonl",
    "model_predictions": "data/derived/future_model_predictions_{date}.jsonl",
    "betting_decisions": "data/derived/future_betting_decisions_{date}.jsonl",
    "settlement_results": "data/derived/future_settlement_results_{date}.jsonl",
    "clv_validation_records": "data/derived/future_clv_validation_records_{date}.jsonl",
    "quality_report": "docs/orchestration/phase6f_capture_quality_report_{date}.md"
  },
  "owner_notes": "Phase 6F manifest — proposed only. Not loaded by production runtime. Phase 6G dry-run will validate this schema against current derived outputs."
}
```

> **This JSON block is documentation only.** It is not committed as a config file.
> If a machine-readable manifest is needed, it will be created under
> `docs/orchestration/phase6f_capture_manifest_2026-04-29.json` and will carry
> the same `owner_notes` disclaimer.

---

## 10. Output Path Plan

Proposed future output files for the MLB/KBO/NPB CLV pipeline:

| File | Purpose | Phase Introduced |
|---|---|---|
| `data/derived/future_odds_snapshots_{date}.jsonl` | Daily odds snapshots with resolved `league` field (not `unknown_league`) | Phase 6G |
| `data/derived/future_model_predictions_{date}.jsonl` | Per-match MLB/KBO/NPB predictions with `canonical_match_id` and full metadata | Phase 6H |
| `data/derived/future_betting_decisions_{date}.jsonl` | Decision records (BET/NO_BET) with EV and Kelly stake | Phase 6H |
| `data/derived/future_settlement_results_{date}.jsonl` | Settlement results with `hit`, `realized_roi`, `closing_line_value` | Phase 6I |
| `data/derived/future_clv_validation_records_{date}.jsonl` | Joined CLV records for aggregate validation | Phase 6J |
| `docs/orchestration/phase6f_capture_quality_report_{date}.md` | Daily quality gate pass/fail report | Phase 6G |

**Existing files are not modified.** The `future_` prefix distinguishes new
prospective captures from historical Phase 6B/6C derived outputs.

---

## 11. Failure Modes

| Failure Mode | Severity | Detection Point | Handling |
|---|---|---|---|
| Missing OPENING snapshot | HIGH | Step 2 / Gate G1 | Exclude from CLV; flag `OPENING_MISSING`; log match_id |
| Missing CLOSING snapshot | HIGH | Step 5 / Gate G2 | Exclude from CLV; flag `CLOSING_MISSING`; attempt one retry within closing window |
| Prediction after CLOSING | CRITICAL (hard fail) | Gate G3 | Exclude record; flag `LEAKAGE_PREDICTION_AFTER_CLOSING`; alert immediately |
| Prediction missing for match | HIGH | Step 4 | Match not CLV-eligible for that market; flag `PREDICTION_MISSING` |
| Settlement missing | MEDIUM | Step 7 | Retain in raw dataset; `settlement_ref=null`; retry after 24h |
| Ambiguous team identity (UNMATCHED) | HIGH | Step 1 | Set `canonical_match_id=UNRESOLVED`; flag `BRIDGE_UNRESOLVED`; exclude from CLV |
| Source odds format change | HIGH | Ingestion parse | Fail batch with `SCHEMA_PARSE_ERROR`; do not write partial rows; alert |
| Market suspended / no odds | MEDIUM | Step 2 or 5 | Skip that market for the match; do not synthesize odds |
| Bookmaker / source mismatch | MEDIUM | Deduplication | Retain primary source; discard secondary; flag `BOOKMAKER_MISMATCH` |
| Duplicate match records | HIGH | canonical_match_id deduplication | Keep earliest discovered record; log duplicates; flag `DUPLICATE_MATCH` |
| Timezone parse error | HIGH | Step 1 (match discovery) | Reject match record; do not infer timezone; flag `TIMEZONE_PARSE_ERROR` |
| Double-header same-day same-teams | MEDIUM | Step 1 | Append game sequence suffix to canonical_match_id: `baseball:MLB:20260501:NYY:BOS:G2`; document convention |
| Postponed game re-scheduled | MEDIUM | Step 1 / settlement | Update `match_status=POSTPONED`; reassign canonical_match_id with new date; retire old record |

---

## 12. Next Implementation Roadmap

All phases below follow the pattern: **design document first → dry-run validation → implementation**.
No phase skips the design step.

| Phase | Title | Goal | Key Deliverable |
|---|---|---|---|
| **6G** | Manifest Dry-Run Quality Checker | Read current `odds_snapshots_2026-04-29.jsonl` through manifest gates; report pass/fail per record; measure current CLV eligibility rate without modifying any file | `docs/orchestration/phase6g_dry_run_quality_report_YYYY-MM-DD.md` |
| **6H** | Prediction Registry Extension for MLB/KBO/NPB | Extend `build_odds_snapshots.py` and/or prediction pipeline to emit `canonical_match_id`-keyed predictions for MLB/KBO/NPB | `data/derived/future_model_predictions_YYYY-MM-DD.jsonl` + schema migration doc |
| **6I** | Settlement Join for MLB/KBO/NPB | Confirm settlement source; build settlement join from postgame results to predictions via `canonical_match_id` | `data/derived/future_settlement_results_YYYY-MM-DD.jsonl` |
| **6J** | CLV Validation Record Generation | Join predictions + odds + settlements into `CLVValidationRecord` format; apply leakage guards G1–G8 | `data/derived/future_clv_validation_records_YYYY-MM-DD.jsonl` |
| **6K** | CLV Aggregate Validation and Readiness Report | When sample ≥200 CLV_high bets per bucket: compute CLV_high ROI vs benchmark; test hypothesis from Phase 5.5 | `research/clv_validation_report_YYYY-MM-DD.md` |

---

## 13. Next Prompt

The following prompt is ready to be used as the Phase 6G task specification:

---

```text
# TASK: BETTING-POOL ORCHESTRATION PHASE 6G — MANIFEST DRY-RUN QUALITY CHECKER

Follow AI system rules.

GOAL:
Implement a manifest dry-run quality checker that reads the current
`data/derived/odds_snapshots_2026-04-29.jsonl` output through the Phase 6F
capture manifest quality gates and produces a readiness report.

This task reads existing derived outputs only. Do not modify crawler, DB, model,
prediction pipeline, or any existing data file. Do not call external APIs.
Do not create orchestrator tasks. Do not commit.

CONTEXT:
- Phase 6E domain commitment: DOMAIN_COMMITMENT_MLB_KBO_NPB
- Phase 6F capture manifest: docs/orchestration/phase6f_future_event_capture_manifest_2026-04-29.md
- Current odds snapshot file: data/derived/odds_snapshots_2026-04-29.jsonl (28,941 rows)
- Current match bridge: data/derived/match_identity_bridge_2026-04-29.jsonl (383 records)
- CLV-eligible pairs observed: 4,796 (OPENING+CLOSING selection pairs)
- CLV_high sample needed: ≥200 (current: 38)

REQUIRED INPUTS:
- docs/orchestration/phase6f_future_event_capture_manifest_2026-04-29.md
- docs/orchestration/phase6a_clv_data_contract_2026-04-29.md
- data/derived/odds_snapshots_2026-04-29.jsonl
- data/derived/match_identity_bridge_2026-04-29.jsonl
- data/wbc_backend/reports/prediction_registry.jsonl

SCOPE:
The dry-run checker must:
1. Apply quality gates G1–G8 from Phase 6F §8 to current derived outputs.
2. Count how many existing records pass each gate.
3. Count how many match/selection pairs are CLV-eligible (G1+G2 both pass).
4. Identify the blocking reasons for ineligible records (OPENING_MISSING,
   CLOSING_MISSING, LEAGUE_INFERRED, BRIDGE_UNRESOLVED, etc.).
5. Report current `unknown_league` coverage and what would need to change for
   full league resolution.
6. Report sample accumulation status: current CLV-eligible count vs ≥200 target.
7. Do NOT compute CLV values — prediction and settlement records are not yet
   available for MLB/KBO/NPB matches.

REQUIRED OUTPUT:
1. Script (read-only): scripts/run_manifest_dry_run.py
   - Reads existing derived files only
   - No writes to any existing file
   - Writes only to: docs/orchestration/phase6g_dry_run_quality_report_YYYY-MM-DD.md
2. Report: docs/orchestration/phase6g_dry_run_quality_report_YYYY-MM-DD.md
   Required sections:
   - Gate-by-gate pass/fail counts
   - CLV eligibility rate for current dataset
   - Blocking reason distribution
   - Unknown league coverage analysis
   - Sample accumulation status
   - Manifest gaps identified by dry-run
   - Phase 6H readiness assessment

FORBIDDEN:
- Do not modify crawler, DB, model, or existing data files.
- Do not call external APIs.
- Do not run CLV validation.
- Do not modify prediction_registry.
- Do not commit.

ACCEPTANCE:
Dry-run script created; quality report created; contamination = 0;
scope constraints confirmed; no existing file modified.
```

---

## 14. Scope Confirmation

This document is a manifest design and documentation file only.
No implementation actions were taken.

| Constraint | Status |
|---|---|
| Code modified | NO |
| Data files modified | NO |
| DB modified | NO |
| Crawler modified | NO |
| Model modified | NO |
| External API called | NO |
| Orchestrator task created | NO |
| Git commit made | NO |
| CLV validation run | NO |
| Phase 6G implementation started | NO |

All Phase 6 predecessor outputs remain unchanged:
- `data/derived/odds_snapshots_2026-04-29.jsonl` — 28,941 rows, unchanged ✅
- `data/derived/team_alias_map_2026-04-29.csv` — 66 entries, unchanged ✅
- `data/derived/match_identity_bridge_2026-04-29.jsonl` — 383 records, unchanged ✅
- `data/wbc_backend/reports/prediction_registry.jsonl` — 66 rows, unchanged ✅

---

**PHASE_6F_MANIFEST_VERIFIED**

*Target domain: DOMAIN_COMMITMENT_MLB_KBO_NPB.*
*Next action: Execute Phase 6G using the prompt in §13 above.*
