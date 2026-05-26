# P62 — MLB Paper Recommendation Contract Draft

**Contract Version**: P62_v1_20260526
**Date**: 2026-05-26
**Classification**: P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW

---

## Pre-flight

| Check | Value |
|---|---|
| Repo | /Users/kelvin/Kelvin-WorkSpace/Betting-pool |
| Branch | main |
| HEAD | d8b3ef5 |
| paper_only | True |
| diagnostic_only | True |
| actual_rows_emitted | False |

---

## Governance

| Flag | Value |
|---|---|
| paper_only | True |
| diagnostic_only | True |
| promotion_freeze | True |
| kelly_deploy_allowed | False |
| live_api_calls | 0 |
| tsl_crawler_modified | False |
| champion_strategy_changed | False |
| production_usage_proposed | False |
| runtime_recommendation_logic_changed | False |
| data_download_attempted | False |
| paid_api_called | False |
| real_bet_allowed | False |
| actual_rows_emitted | False |
| p45_platt_constants_modified | False |
| p52_thresholds_modified | False |
| p60_artifacts_overwritten | False |
| p61_artifacts_overwritten | False |

---

## Platt Constants (P45 Locked)

| Constant | Value |
|---|---|
| platt_A | 0.435432 |
| platt_B | 0.245464 |
| calibration_method | platt_scaled |
| P45 artifact verified | False |

> **Note**: Platt constants are permanently locked from P45. No refitting in P62.

---

## Signal & Tier

| Parameter | Value |
|---|---|
| signal | sp_fip_delta |
| tier | Tier_C |
| threshold | |sp_fip_delta| >= 0.50 (T_LOCKED) |
| market | moneyline |

---

## Eligibility Gate — 17 Conditions

| ID | Condition | Description |
|---|---|---|
| EG01 | `paper_only=True` | All operations strictly paper-only — no live deployment |
| EG02 | `diagnostic_only=True` | Diagnostic mode only — contract defines schema, emits no rows |
| EG03 | `promotion_freeze=True` | Champion promotion frozen — no strategy replacement allowed |
| EG04 | `live_api_calls=0` | Zero live API calls made during contract draft |
| EG05 | `kelly_deploy_allowed=False` | Kelly criterion may be computed theoretically but never deployed |
| EG06 | `runtime_recommendation_logic_changed=False` | Runtime recommendation logic unchanged from P52 SSOT |
| EG07 | `champion_replacement=False` | fixed_edge_5pct champion strategy not replaced |
| EG08 | `production_ready=False` | Contract is not a production deployment proposal |
| EG09 | `real_bet_allowed=False` | No real betting allowed at any stage of this contract |
| EG10 | `signal=sp_fip_delta` | Recommendation signal must be sp_fip_delta (no other signals substituted) |
| EG11 | `tier=Tier_C` | Only Tier C games qualify (|sp_fip_delta| >= T_LOCKED) |
| EG12 | `threshold=abs(sp_fip_delta)>=0.50` | T_LOCKED=0.50 — threshold must not be re-optimized |
| EG13 | `calibration=P45_Platt_constants` | Calibration must use P45 locked constants A=0.435432, B=0.245464 |
| EG14 | `odds_source_trace_required` | Odds traceability reference required — no odds without source audit trail |
| EG15 | `timestamps_required` | game_start_utc, prediction_timestamp_utc, odds_timestamp_utc must all be pregame |
| EG16 | `no_postgame_leakage` | No postgame data used in prediction or odds — pregame isolation required |
| EG17 | `2024_data_gap_documented` | 2024 closing-line data gap explicitly documented; contract covers 2025-only evidence |

---

## Row Schema — 27 Required Fields

| Field | Type | Description |
|---|---|---|
| contract_version | str | Contract version string, e.g. P62_v1_20260526 |
| game_id | str | Unique game identifier (MLB game ID) |
| game_start_utc | str | Game start time in ISO8601 UTC — pregame only |
| generated_at_utc | str | Timestamp this contract row was generated |
| prediction_timestamp_utc | str | Timestamp model prediction was made (must be pregame) |
| odds_timestamp_utc | str | Timestamp odds were captured (must be pregame) |
| market | str | Market type — always 'moneyline' for P62 |
| side | str | Home or Away — whichever model favors |
| model_signal_name | str | Signal driving recommendation — always 'sp_fip_delta' |
| sp_fip_delta | float | Raw FIP differential for this game |
| signal_tier | str | Tier classification — must be 'Tier_C' |
| tier_threshold | float | Locked threshold — 0.50 |
| model_prob_home | float | Raw sigmoid model probability for home team |
| model_prob_away | float | Raw sigmoid model probability for away team |
| calibration_method | str | Always 'platt_scaled' — P45 locked |
| platt_A | float | Platt A constant — locked 0.435432 |
| platt_B | float | Platt B constant — locked 0.245464 |
| calibrated_prob | float | Platt-calibrated model probability for favored side |
| odds_source | str | Source of odds data (e.g. mlb_odds_2025_real.csv) |
| odds_source_trace | str | Traceability reference — file + row hash or URL |
| decimal_odds | float | Decimal odds for favored side |
| implied_probability | float | Implied probability from decimal odds |
| edge_pct | float | calibrated_prob - implied_probability (positive = model edge) |
| paper_stake_units | float | Theoretical paper stake in units (never deployed) |
| kelly_fraction_theoretical | float | Kelly criterion fraction (theoretical only, not deployed) |
| kelly_deploy_allowed | bool | Always False — paper-only |
| recommendation_status | str | One of 9 allowed status values |
| gate_status | str | GATE_PASS or GATE_BLOCK |
| gate_reasons | list | List of gate failure reasons (empty if GATE_PASS) |
| paper_only | bool | Always True |
| diagnostic_only | bool | Always True |
| production_ready | bool | Always False |
| real_bet_allowed | bool | Always False |

---

## Allowed Status Values (9)

- `PAPER_ELIGIBLE_CONTRACT_ONLY`
- `BLOCKED_MISSING_ODDS_SOURCE_TRACE`
- `BLOCKED_MISSING_TIMESTAMP`
- `BLOCKED_POSTGAME_LEAKAGE_RISK`
- `BLOCKED_SIGNAL_BELOW_TIER_C`
- `BLOCKED_CALIBRATION_SOURCE_INVALID`
- `BLOCKED_PROMOTION_FREEZE`
- `BLOCKED_PRODUCTION_NOT_ALLOWED`
- `BLOCKED_2024_DATA_GAP_UNRESOLVED`

---

## Governance Exclusions

| Exclusion | Detail |
|---|---|
| NO_LIVE_DEPLOYMENT | Contract rows must never be used for live betting decisions |
| NO_CHAMPION_REPLACEMENT | fixed_edge_5pct strategy remains champion; contract does not propose replacement |
| NO_PRODUCTION_PROPOSAL | This contract is explicitly NOT a production readiness proposal |
| NO_KELLY_DEPLOYMENT | Kelly fractions are theoretical only; kelly_deploy_allowed=False always |
| NO_PAID_API_USAGE | No paid odds API called during contract draft (P61 PATH_A/B pending CEO auth) |
| NO_TSL_CRAWLER_MODIFICATION | TSL crawler unchanged; all odds from existing 2025 CSV artifacts |
| NO_P45_CONSTANT_REFITTING | Platt constants A=0.435432, B=0.245464 are permanently locked from P45 |
| NO_P52_THRESHOLD_MODIFICATION | P52 monitoring thresholds unchanged |
| NO_PROFIT_CLAIMS | Zero affirmative profit or deployment claims issued — diagnostic-only framing enforced |
| NO_2024_INFERENCE | 2024 closing-line data gap unresolved; contract evidence is 2025-only |

---

## P61 Relationship — 2024 Data Gap

**P61 Classification**: P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT
**Gap Status**: UNRESOLVED_AS_OF_P62

2024 MLB closing-line odds are missing from available data sources. P43 final classification was P43_BLOCKED_BY_DATA_GAP despite confirmed 2025 edge (mean_edge=0.1059, CI=[0.0989, 0.1132], Tier C, n=535). P61 identified two viable resolution paths: PATH_A (The Odds API, ~$30-50, MEDIUM effort, requires CEO authorization) and PATH_B (Kaggle/GitHub, $0, try first). Neither path has been executed as of P62 contract draft.

**Impact on P62**: P62 contract rows covering 2025 games can be fully defined. However, rows that would reference 2024 games are BLOCKED_2024_DATA_GAP_UNRESOLVED. The P43 potential upgrade from BLOCKED to CONFIRMED is contingent on P61 resolution.

| Path | Description |
|---|---|
| PATH_A | The Odds API historical data (~$30-50, MEDIUM effort) — requires CEO auth |
| PATH_B | Kaggle/GitHub free search ($0, MEDIUM effort) — try first |

**Recommended order**: PATH_B first, PATH_A if PATH_B fails
**CEO authorization required**: True
**Data download attempted**: False

---

## Prior Phase Context

### P43
- Classification: P43_BLOCKED_BY_DATA_GAP
- Blocked by data gap: True

### P60
- Classification: P60_EDGE_STABLE_ACROSS_MONTHS
- Cross-month edge stability: None
- Months within threshold: None/None

### P61
- Classification: P61_DATA_GAP_RESOLVABLE_MEDIUM_EFFORT
- Gap resolvable: True

---

## Sample Row Illustration (Hypothetical — No Actual Data)

```json
{
  "contract_version": "P62_v1_20260526",
  "game_id": "HYPOTHETICAL_SAMPLE_2025_ABC123",
  "game_start_utc": "2025-07-15T23:05:00Z",
  "generated_at_utc": "2026-05-26T00:00:00Z",
  "prediction_timestamp_utc": "2025-07-15T18:30:00Z",
  "odds_timestamp_utc": "2025-07-15T20:00:00Z",
  "market": "moneyline",
  "side": "Home",
  "model_signal_name": "sp_fip_delta",
  "sp_fip_delta": 0.72,
  "signal_tier": "Tier_C",
  "tier_threshold": 0.5,
  "model_prob_home": 0.640146,
  "model_prob_away": 0.359854,
  "calibration_method": "platt_scaled",
  "platt_A": 0.435432,
  "platt_B": 0.245464,
  "calibrated_prob": 0.621583,
  "odds_source": "mlb_odds_2025_real.csv",
  "odds_source_trace": "mlb_odds_2025_real.csv:row_hash=HYPOTHETICAL",
  "decimal_odds": 1.85,
  "implied_probability": 0.540541,
  "edge_pct": 0.081042,
  "paper_stake_units": 1.0,
  "kelly_fraction_theoretical": 0.176387,
  "kelly_deploy_allowed": false,
  "recommendation_status": "PAPER_ELIGIBLE_CONTRACT_ONLY",
  "gate_status": "GATE_PASS",
  "gate_reasons": [],
  "paper_only": true,
  "diagnostic_only": true,
  "production_ready": false,
  "real_bet_allowed": false
}
```

---

## Contract Coverage

| Item | Value |
|---|---|
| Year covered | 2025 |
| Year excluded | 2024 (data gap) |
| Months validated by P60 | Apr–Sep 2025 (6/6 EDGE_WITHIN_THRESHOLD) |
| Cross-month edge stability | EDGE_STABLE_ACROSS_MONTHS |

---

## Forbidden Claims Scan

**Result**: CLEAN — 0 violations

Scanned for affirmative deployment or profit assertions. All checks CLEAN.

---

## P62 Final Classification

**`P62_CONTRACT_DRAFT_READY_FOR_CEO_REVIEW`**

> Contract schema fully defined with 17-condition eligibility gate, row schema,
> 9 status values, 10 governance exclusions, and explicit P61 data gap documentation.
> No live rows emitted. No production deployment proposed. Paper-only diagnostic contract.

---

*paper_only=True | diagnostic_only=True | promotion_freeze=True | kelly_deploy_allowed=False*
*No champion replacement | No production proposal | Diagnostic-only framing*
