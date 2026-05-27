# P84A — 2026 Upstream Data Collector Contract
**Date:** 2026-05-26
**Classification:** `P84A_UPSTREAM_COLLECTOR_CONTRACT_READY`
**Mode:** paper_only=True | diagnostic_only=True | NO_REAL_BET=True

---

## Summary

P84A defines the upstream data collector contract for the three files required by P83E.

**P83E State:** `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA`
**Missing upstream files:** ['schedule', 'pitchers', 'model_outputs']

---

## P83E State Verification

| Check | Result |
|---|---|
| P83E classification | `P83E_BLOCKED_BY_MISSING_UPSTREAM_DATA` |
| rows_written | False |
| live_api_calls | 0 |
| odds_used | False |
| production_ready | False |

---

## Upstream Target File Status

| File | Status |
|---|---|
| data/mlb_2026/schedule/mlb_2026_schedule.jsonl | ❌ Missing |
| data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl | ❌ Missing |
| data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl | ❌ Missing |

---

## Allowed Source Classes

| Source Class | Description |
|---|---|
| MLB_STATS_API_PUBLIC_SCHEDULE | statsapi.mlb.com/api/v1/schedule — free, public |
| MLB_STATS_API_PUBLIC_PLAYER_STATS | statsapi.mlb.com/api/v1/people — pitcher stats |
| LOCAL_PUBLIC_STATS_EXPORT | Manually exported CSV/JSON from public MLB sites |
| MANUAL_PUBLIC_STATS_FIXTURE | Hand-keyed records with source trace |
| MOCK_SCHEMA_ONLY_FIXTURE | In-memory only, noncanonical, testing only |

## Forbidden Source Classes

| Source Class | Reason |
|---|---|
| ODDS_API | No odds allowed |
| PAID_ODDS_DATA | No paid data |
| SPORTSBOOK_SOURCE | No sportsbook scrape |
| RUNTIME_PAPER_OUTPUT | Noncanonical; cannot be model source |
| FABRICATED_NON_MOCK | Data integrity violation |

---

## Schedule Collector Contract (P84A_SCHEDULE_COLLECTOR_CONTRACT_V1)

- **Output:** `data/mlb_2026/schedule/mlb_2026_schedule.jsonl`
- **Required fields:** game_id, game_date, season=2026, home_team, away_team, source_trace, collected_at_utc
- **Recommended source:** `MLB_STATS_API_PUBLIC_SCHEDULE`
- **Endpoint:** `statsapi.mlb.com/api/v1/schedule?sportId=1&season=2026`
- **Activation gate:** SCHEDULE_GATE

---

## Pitcher FIP Feature Builder Contract (P84A_PITCHER_FIP_CONTRACT_V1)

- **Output:** `data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl`
- **Required fields:** game_id, home_sp_fip, away_sp_fip, source_trace, feature_version
- **Row status values:** FEATURE_READY | FEATURE_PENDING
- **Blocking behavior:** FEATURE_PENDING row blocks PITCHER_FEATURE_GATE
- **FIP formula:** `((13*HR + 3*(BB+HBP) - 2*K) / IP) + FIP_constant`
- **Recommended source:** `MLB_STATS_API_PUBLIC_PLAYER_STATS`

---

## Model Output Builder Contract (P84A_MODEL_OUTPUT_CONTRACT_V1)

- **Output:** `data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl`
- **Required fields:** game_id, model_probability, source_prediction_version, model_input_trace, predicted_side_derivation_status
- **Row status values:** DERIVABLE | MODEL_PENDING
- **Blocking behavior:** MODEL_PENDING row blocks MODEL_OUTPUT_GATE
- **Model source:** 2025-trained ensemble (P7A / PredictionOrchestrator) applied to 2026 feature rows
- **Runtime PAPER output is noncanonical** — cannot be used as model source

---

## Mock Schema-Only Fixture Validation

| Check | Result |
|---|---|
| Source class | MOCK_SCHEMA_ONLY_FIXTURE |
| Canonical | False |
| N games | 3 |
| Schedule schema valid | ✅ |
| Pitcher schema valid | ✅ |
| Model output schema valid | ✅ |
| All valid | ✅ |

---

## Governance Invariants

| Invariant | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| live_api_calls | 0 |
| odds_used | False |
| ev_calculated | False |
| clv_calculated | False |
| kelly_calculated | False |
| production_ready | False |
| canonical_rows_written | False |
| forbidden_scan_pass | True |

---

## Next Steps (P84B / P83E Retry)

```
[P84B — 2026 Public Stats Collector Implementation]

P84A has defined the upstream data collector contract. Re-run P83E once all three files exist locally.

To unblock P83E, implement P84B or manually provide:

1. data/mlb_2026/schedule/mlb_2026_schedule.jsonl
   Contract: P84A_SCHEDULE_COLLECTOR_CONTRACT_V1
   Source:   MLB_STATS_API_PUBLIC_SCHEDULE
   Endpoint: statsapi.mlb.com/api/v1/schedule?sportId=1&season=2026
   Fields:   game_id, game_date, season=2026, home_team, away_team, source_trace, collected_at_utc

2. data/mlb_2026/pitchers/mlb_2026_sp_fip_features.jsonl
   Contract: P84A_PITCHER_FIP_CONTRACT_V1
   Source:   MLB_STATS_API_PUBLIC_PLAYER_STATS
   Endpoint: statsapi.mlb.com/api/v1/people/{pitcher_id}/stats?stats=season&season=2026
   Fields:   game_id, home_sp_fip, away_sp_fip, source_trace, feature_version
   Note:     row_status=FEATURE_PENDING if FIP unavailable → blocks PITCHER_FEATURE_GATE

3. data/mlb_2026/model_outputs/mlb_2026_model_outputs.jsonl
   Contract: P84A_MODEL_OUTPUT_CONTRACT_V1
   Source:   LOCAL (2025-trained ensemble applied to 2026 feature rows)
   Fields:   game_id, model_probability, source_prediction_version, model_input_trace, predicted_side_derivation_status
   Note:     Runtime PAPER output is noncanonical and cannot be used here

Rules: paper_only=True | no odds API | no EV/CLV/Kelly | no canonical rows in P84B until activation gates pass

```

---

## Final Classification

**`P84A_UPSTREAM_COLLECTOR_CONTRACT_READY`**

P84A defines the upstream data collector contract for 2026 MLB schedule, pitcher FIP features, and model outputs. No external API calls are made. No market edge is computed. No canonical prediction rows are written. paper_only=True, diagnostic_only=True.
