# Phase 6B — Odds Snapshot Adapter Report

**Date:** 2026-04-29
**Adapter script:** `data/derived/odds_snapshots_2026-04-29.jsonl`
**Input:** `data/tsl_odds_history.jsonl`
**Output:** `data/derived/odds_snapshots_2026-04-29.jsonl`
**Predecessor commit:** 806f2a5 (Phase 6A CLV data contract)

---

## 1. Executive Summary

Phase 6B adapter successfully processed 1,205 TSL odds history rows into 28,941 canonical odds snapshot records across 383 canonical matches (411 raw TSL match IDs).

Snapshot type classification was applied to every output record. Records with only one pre-match snapshot were marked `AMBIGUOUS_SINGLE_PREMATCH` (1,821 records) — these are not sufficient for formal CLV validation.

**Phase 6B target blocker resolved:** `snapshot_type` is now populated for all derived odds snapshot records.

**Remaining CLV blocker:** The derived file cannot yet be joined to model predictions because TSL `match_id` (numeric, e.g. `3452364.1`) and model `game_id` (WBC pool code, e.g. `A05`) overlap = 0. This requires Phase 6C (canonical match ID bridge).

---

## 2. Input Evidence

| Field | Value |
|---|---|
| Input file | `data/tsl_odds_history.jsonl` |
| Input rows | 1,205 |
| Unique TSL match IDs | 411 |
| Source values | `TSL_BLOB3RD`, `tsl_crawler_v2` |
| Fetch date range | 2026-03-13 to 2026-04-29 |
| Game time date range | 2026-03-13 to 2026-04-30 |
| Market codes present | MNL, HDC, OU, OE, TTO |
| `snapshot_type` in source | MISSING (all 1,205 rows) |
| `home_code` / `away_code` in source | Empty string for all rows |

**DOMAIN_DESIGN_REQUIRED: League normalization table**
TSL records include Chinese team names (e.g. `羅德海洋`, `西武獅`, `起亞老虎`). No mapping from Chinese team names to league (CPBL/KBO/NPB/WBC) or 3-letter codes exists. All output records are assigned `league = unknown_league` with quality flag `LEAGUE_INFERRED` until this table is built.

---

## 3. Adapter Logic

### 3.1 Expansion

Each TSL row represents one match snapshot with multiple markets and outcomes. The adapter expands each row into one record per market × outcome, producing a flat canonical JSONL where each record is a single price observation for one selection.

### 3.2 Market Normalization

| TSL `marketCode` | Contract `market_type` | Notes |
|---|---|---|
| `MNL` | `ML` | Moneyline |
| `HDC` | `RL` | Handicap / run-line |
| `OU` | `OU` | Over-under total |
| `OE` | `OE` | Odd-even |
| `TTO` | `OU` | Alternative total — mapped to OU |

### 3.3 Selection Inference

| Pattern | Mapped Selection |
|---|---|
| `大` prefix in outcomeName | `over` |
| `小` prefix in outcomeName | `under` |
| `單` | `odd` |
| `雙` | `even` |
| outcomeName matches home team name | `home` |
| outcomeName matches away team name | `away` |
| No match | `UNKNOWN_SELECTION` + `SELECTION_MISSING` flag |

### 3.4 Canonical Match ID Construction

```
canonical_match_id = "baseball:{league}:{match_date_utc}:{home_team_norm}:{away_team_norm}"
```

League is set to `unknown_league` for all TSL records pending team name normalization table (DOMAIN_DESIGN_REQUIRED). Team names are Unicode-NFC normalized, lowercased, spaces replaced with underscores.

### 3.5 Snapshot Type Classification

Records are grouped by `selection_key` (= canonical_match_id:market_type:line:selection). Within each group, pre-match snapshots (fetched_at < game_time) are sorted by time.

| Condition | snapshot_type |
|---|---|
| Only one pre-match snapshot for this selection | `AMBIGUOUS_SINGLE_PREMATCH` |
| First pre-match snapshot (N>1 total) | `OPENING` |
| Last pre-match snapshot (N>1 total) | `CLOSING` |
| Any other pre-match snapshot | `INTERMEDIATE` |
| fetched_at >= game_time | `POST_MATCH` |

### 3.6 Odds Normalization

- `odds` field (string) cast to float.
- Records with `decimal_odds <= 1.0` or non-numeric odds excluded with `INVALID_ODDS` flag.
- `implied_probability = round(1 / decimal_odds, 6)`.

---

## 4. Output Summary

| Metric | Value |
|---|---|
| Output file | `data/derived/odds_snapshots_2026-04-29.jsonl` |
| Output records | 28,941 |
| Unique canonical match IDs | 383 |
| Unique raw TSL match IDs | 411 |
| Invalid odds excluded | 0 |

**Market type distribution:**

| market_type | Records |
|---|---|
| `ML` | 8,335 |
| `OE` | 2,148 |
| `OU` | 14,572 |
| `RL` | 3,886 |

**Snapshot type distribution:**

| snapshot_type | Records |
|---|---|
| `AMBIGUOUS_SINGLE_PREMATCH` | 1,821 |
| `CLOSING` | 4,796 |
| `INTERMEDIATE` | 15,215 |
| `OPENING` | 4,796 |
| `POST_MATCH` | 2,313 |

**Quality flag distribution (top flags):**

| Flag | Count |
|---|---|
| `LEAGUE_INFERRED` | 28,941 |
| `POST_MATCH_EXCLUDED` | 2,313 |
| `SELECTION_MISSING` | 1,975 |
| `OPENING_CLOSING_AMBIGUOUS` | 1,821 |

---

## 5. Data Quality Findings

### 5.1 AMBIGUOUS_SINGLE_PREMATCH

1,821 records are classified `AMBIGUOUS_SINGLE_PREMATCH`. These are matches where only one pre-match odds fetch exists for a given market × selection. Without a distinct opening AND closing snapshot, CLV probability delta (predicted_probability - implied_probability_close) cannot be reliably computed. These records are retained in the derived file for data coverage analysis only.

### 5.2 POST_MATCH

2,313 records are classified `POST_MATCH` (fetched_at >= game_time). These snapshots are tagged with `POST_MATCH_EXCLUDED` and must be excluded from any CLV or leakage-sensitive computation. They may be used for settlement validation (confirming final odds before settlement).

### 5.3 OPENING / CLOSING Pairs

OPENING records: 4,796. CLOSING records: 4,796. INTERMEDIATE records: 15,215.

Matches with true temporal separation (>1h between first and last fetch) number approximately 237 out of 411 raw TSL match IDs. For these matches, OPENING and CLOSING pairs exist at the market × selection level.

**However**, because the canonical_match_id for TSL records uses `unknown_league` and Chinese team names (not 3-letter codes), these canonical IDs cannot yet be joined to model prediction canonical IDs (which use WBC pool codes like `A05`). Formal CLV validation is NOT YET possible.

### 5.4 LEAGUE_INFERRED Flag

All output records carry `LEAGUE_INFERRED` because no team name → league normalization table exists. This flag indicates the `unknown_league` value in the canonical_match_id is provisional.

### 5.5 SELECTION_MISSING Records

Records with `SELECTION_MISSING` flag: 1,975. These occur where the outcomeName could not be matched to home/away or to a known Chinese prefix pattern. Excluded from CLV analysis.

---

## 6. Leakage / CLV Readiness

| Check | Status |
|---|---|
| `snapshot_type` populated for all derived records | YES ✅ |
| `POST_MATCH` records excluded from CLV | YES — tagged `POST_MATCH_EXCLUDED` ✅ |
| `AMBIGUOUS_SINGLE_PREMATCH` excluded from formal CLV | YES — per Phase 6A rules ✅ |
| Both OPENING and CLOSING snapshots exist (some matches) | YES — for ~237 matches ✅ |
| CLV probability delta computable | NOT YET — model prediction join blocked 🔴 |
| canonical_match_id bridge to prediction_registry | ABSENT — Phase 6C required 🔴 |
| Leakage guard: all OPENING/CLOSING are pre-match | YES — enforced in classification ✅ |

**Formal CLV validation is NOT ready.** The derived odds snapshot file is structurally correct per Phase 6A contract, but cannot be joined to model predictions until Phase 6C (match ID bridge + team name normalization) is completed.

---

## 7. Backward Compatibility

- Original `data/tsl_odds_history.jsonl` was NOT modified. ✅
- Derived file `data/derived/odds_snapshots_2026-04-29.jsonl` is additive. ✅
- Crawler (`data/tsl_crawler_v2.py`, `data/tsl_crawler.py`) was NOT changed. ✅
- No DB schema changed. ✅
- No model changed. ✅

---

## 8. Next Steps

### If Phase 6C proceeds (recommended):

Phase 6C must build the canonical match ID bridge:
1. Build team name normalization table: Chinese team name → 3-letter code + league.
2. Map TSL numeric match_id → canonical_match_id using game_time + normalized teams.
3. Map WBC pool code game_id → canonical_match_id using `wbc_2026_authoritative_snapshot.json`.
4. Join derived `odds_snapshots_2026-04-29.jsonl` with `prediction_registry.jsonl`    on canonical_match_id.
5. Compute CLV probability delta per Phase 6A §2.7 formula.

### If Phase 6B-2 is needed instead:

If the existing snapshot coverage is insufficient (too many AMBIGUOUS_SINGLE_PREMATCH), update the crawler to fetch odds at multiple time points:
- T-24h (opening proxy)
- T-1h (closing proxy)
- T+1h (post-match confirmation)

This would generate true OPENING and CLOSING tags without requiring historical backfill.

---

## 9. Scope Confirmation

- ✅ Original `data/tsl_odds_history.jsonl` not modified
- ✅ Crawler not changed
- ✅ DB not changed
- ✅ Model not changed
- ✅ No external API called
- ✅ No orchestrator task created
- ✅ No git commit made

---

## 10. Contamination Check

This document and the adapter script were reviewed for disallowed lottery-domain patterns.
All disallowed patterns were searched. Result: 0 occurrences.
This document contains only Betting-pool-native market, odds, and CLV terminology.