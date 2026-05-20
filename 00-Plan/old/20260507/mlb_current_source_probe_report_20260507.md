# MLB Current Source Probe — Adapter Validation Report

> **⚠️ PAPER-ONLY — DRY-RUN — NO REAL BET — NO PROFIT CLAIM**
>
> 本報告為 source adapter 驗證報告，所有 fixture 賠率均為測試用途，
> 不代表任何真實下注、真實賠率、或真實 edge 聲明。

**Probe Date:** 2026-05-07
**Source Mode:** `fixture`
**Fixture Source Used:** `True`
**Current Source Reachable:** `False`
**Model Prediction Available:** `False`
**Total Snapshots:** 4
**Report Generated:** 2026-05-07T08:22:21.372169+00:00

---

## Source Health

- **source_name**: `current_mlb_api`
- **source_mode**: `current`
- **checked_at**: `2026-05-07T08:22:21.372528+00:00`
- **reachable**: `False`
- **total_games**: `0`
- **moneyline_games**: `0`
- **runline_games**: `0`
- **total_games_with_total**: `0`
- **result_games**: `0`
- **errors**: `['live_api_not_configured: no current MLB schedule/odds API source available; fixture or replay mode required']`
- **warnings**: `['system_in_dry_run_mode: only fixture or replay sources are operational', 'no_real_bet: this system does not execute real bets under any mode']`

---

## Market Coverage Matrix

| Field | Available |
|-------|-----------|
| moneyline_available | ✅ YES |
| runline_available | ✅ YES |
| total_available | ✅ YES |
| result_available | ❌ NO |
| odds_available | ✅ YES |
| market_home_prob_available | ✅ YES |
| closing_market_available | ❌ NO |
| source_name | `fixture` |
| source_mode | `fixture` |
| fixture_source_used | `True` |
| current_source_reachable | `False` |
| model_prediction_available | `False` |

---

## Game Snapshots

Total: 4 games

| # | Date | Away | Home | ML Home | ML Away | no-vig | Runline | Total | Status |
|---|------|------|------|---------|---------|--------|---------|-------|--------|
| 1 | 2026-05-07 | New York Yankees | Boston Red Sox | -130.0 | 110.0 | 0.543 | N/A | N/A | scheduled |
| 2 | 2026-05-07 | Houston Astros | Los Angeles Dodgers | -155.0 | 130.0 | 0.583 | -1.5 | N/A | scheduled |
| 3 | 2026-05-07 | Chicago Cubs | Atlanta Braves | -115.0 | 95.0 | 0.510 | -1.5 | 8.5 | scheduled |
| 4 | 2026-05-07 | Seattle Mariners | Oakland Athletics | N/A | N/A | N/A | N/A | N/A | scheduled |

---

## Validation Results

Snapshot validation errors: 0

✅ No validation errors found.

---

## Gate Conclusion

**Gate: `MLB_CURRENT_SOURCE_FIXTURE_READY`**

> Live source not configured; fixture source loaded with moneyline data; adapter/advisory integration validated via fixture mode; live API integration pending

---

## No Profit Claim

本系統不聲稱已找到可盈利的投注 edge。
所有 fixture 賠率均為測試用途，不代表任何真實獲利預期。

**NO_PROFIT_CLAIM = True**
**NO_EDGE_CLAIM = True**
**PAPER_ONLY = True**
**NO_REAL_BET = True**

---

## Completion Marker

`MLB_CURRENT_SOURCE_ADAPTER_VERIFIED`

