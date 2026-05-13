# P38A Retrosheet OOF Rebuild Plan — 2026-05-13

**Status:** PLANNING PACKAGE (not runtime)  
**Author:** CEO/CTO Agent  
**Date:** 2026-05-13  
**Acceptance Marker:** P38A_RETROSHEET_OOF_REBUILD_PLAN_20260513_READY

---

## ⚠️ Non-Goals Declaration (Read First)

Before reading this plan, be clear about what this plan does NOT do:

- ❌ 不做 production bet
- ❌ 不做 live TSL integration
- ❌ 不做 edge claim（不聲稱模型具備穩定正期望值）
- ❌ 不跳過 odds approval（P37.5 路徑繼續進行）
- ❌ 不在 runtime 實作，此為 planning package 僅止於文件規格

---

## 1. Objective

Resolve the 2024 OOF (Out-of-favor / closing line outperformance) prediction
source gap by rebuilding the pregame-safe feature pipeline using Retrosheet 2024
public game logs.

| Goal                              | Detail                                                       |
|-----------------------------------|--------------------------------------------------------------|
| 解決 2024 OOF prediction source 缺口 | 現有 OOF artifacts 缺少 2024 完整 game log 支撐           |
| 放大 recommendation sample size    | 2024 season adds ~2430 MLB games to replay corpus           |
| 支援 multi-season true-date replay  | Enable date-ordered replay without look-ahead leakage       |

---

## 2. Scope

### 2.1 In-Scope

| Component                         | Description                                                  |
|-----------------------------------|--------------------------------------------------------------|
| Retrosheet 2024 schedule file     | `2024SKED.TXT` — game dates, teams, park codes              |
| Retrosheet 2024 game logs         | `GL2024.TXT` — Gamelogs: final scores, starters, attendance  |
| Retrosheet team mapping           | `TEAMABR.csv` — 3-letter code ↔ full team name              |
| Pregame-safe feature subset       | See Section 4 — only pre-first-pitch state features         |
| OOF prediction artifact           | Output JSONL/CSV — one row per game, pregame-safe            |
| Leakage audit report              | Formal certification that no postgame data enters features   |
| Replay join certification         | Prove artifact can join with odds proxy on game_date + teams |

### 2.2 Out-of-Scope (Confirmed Non-Goals)

| Item                              | Reason                                                       |
|-----------------------------------|--------------------------------------------------------------|
| Live TSL odds                     | Not available; P37.5 handles this path                       |
| 2024 closing odds (licensed)      | Blocked by P37.5; feasibility spike handles proxy research   |
| Run line / totals models          | P8 (later phase); moneyline only for this rebuild            |
| Model edge claims                 | Prohibited per governance rules                              |
| Production deployment             | P10 gate required before any production use                  |

---

## 3. Dependency Chain

```
Retrosheet 2024 game logs (public, free)
    │
    ▼
Team code normalization (TEAMABR.csv → canonical team_id)
    │
    ▼
Pregame-safe feature extraction
  [LEAKAGE SENTINEL REQUIRED at this step]
    │
    ▼
OOF prediction artifact (JSONL/CSV)
  [is_research=true flag required]
    │
    ▼
Replay join certification
  (artifact game_key ↔ odds proxy game_key)
    │
    ▼
[BLOCKED until P1: Free-source odds feasibility passes]
    │
    ▼
Multi-season true-date replay (P5)
```

**Critical path note:** Steps 1-4 (feature extraction through artifact production)
can begin without odds. Steps 5+ require either P37.5 approved odds or a
join-certified research proxy from the feasibility spike.

---

## 4. Pregame-Safe Feature Subset

All features in this subset must satisfy the leakage rule:
> A feature is pregame-safe if and only if its value is knowable
> from publicly available information **before** the first pitch of that game.

| Feature Name               | Source             | Pregame-Safe? | Notes                              |
|----------------------------|--------------------|---------------|------------------------------------|
| `home_team_id`             | Schedule           | ✅ YES         | From SKED file                     |
| `away_team_id`             | Schedule           | ✅ YES         | From SKED file                     |
| `game_date`                | Schedule           | ✅ YES         | ISO 8601 date                      |
| `home_starter_hand`        | Game log + roster  | ✅ YES         | Announced before game              |
| `away_starter_hand`        | Game log + roster  | ✅ YES         | Announced before game              |
| `home_win_pct_last_30`     | Derived from history | ✅ YES       | Rolling window using prior games only |
| `away_win_pct_last_30`     | Derived from history | ✅ YES       | Rolling window using prior games only |
| `home_runs_scored_avg_10`  | Derived from history | ✅ YES       | Rolling 10-game avg, prior games   |
| `away_runs_scored_avg_10`  | Derived from history | ✅ YES       | Rolling 10-game avg, prior games   |
| `park_factor`              | Historical park data | ✅ YES       | Season-level, pre-published        |
| `home_team_era_last_10`    | Derived from history | ✅ YES       | Rolling ERA, prior games only      |
| `is_doubleheader`          | Schedule           | ✅ YES         | Known before game                  |

**Banned features (postgame leakage risk):**

| Feature                    | Reason Banned                                                |
|----------------------------|--------------------------------------------------------------|
| `final_score_home`         | Postgame result                                              |
| `final_score_away`         | Postgame result                                              |
| `game_result`              | Postgame result                                              |
| `starter_innings_pitched`  | Only known after game                                        |
| `live_attendance`          | Can be corrupted by postgame data                            |

---

## 5. Artifact Contract

### 5.1 Input Manifest

```yaml
input_manifest:
  retrosheet_schedule:
    path: data/mlb_2024/raw/2024SKED.TXT
    format: fixed-width
    required: true
  retrosheet_gamelogs:
    path: data/mlb_2024/raw/GL2024.TXT
    format: CSV (Retrosheet gamelog format)
    required: true
  team_mapping:
    path: data/mlb_2024/raw/TEAMABR.csv
    format: CSV
    required: true
  historical_rolling_stats:
    path: data/mlb_2024/processed/rolling_stats_2024.csv
    format: CSV
    derived_from: [GL2024.TXT, prior seasons]
    required: true
```

### 5.2 Feature Manifest

```yaml
feature_manifest:
  version: "1.0"
  created: "2026-05-13"
  leakage_audit_status: PENDING
  features:
    - name: home_team_id
      source: schedule
      pregame_safe: true
    - name: away_team_id
      source: schedule
      pregame_safe: true
    - name: game_date
      source: schedule
      pregame_safe: true
    - name: home_starter_hand
      source: gamelog
      pregame_safe: true
      note: "Use announced starter, not actual if pinch-started"
    - name: away_starter_hand
      source: gamelog
      pregame_safe: true
    - name: home_win_pct_last_30
      source: derived
      pregame_safe: true
      window: "30 prior games (strict date filter)"
    - name: away_win_pct_last_30
      source: derived
      pregame_safe: true
      window: "30 prior games (strict date filter)"
    - name: home_runs_scored_avg_10
      source: derived
      pregame_safe: true
      window: "10 prior games"
    - name: away_runs_scored_avg_10
      source: derived
      pregame_safe: true
      window: "10 prior games"
    - name: park_factor
      source: historical
      pregame_safe: true
    - name: home_team_era_last_10
      source: derived
      pregame_safe: true
      window: "10 prior games"
    - name: is_doubleheader
      source: schedule
      pregame_safe: true
```

### 5.3 Prediction JSONL Schema

Each line in the output JSONL file must conform to:

```json
{
  "game_key": "2024-04-01_NYA_BOS",
  "game_date": "2024-04-01",
  "home_team_id": "BOS",
  "away_team_id": "NYA",
  "predicted_home_win_prob": 0.523,
  "predicted_total_runs": 8.7,
  "model_version": "oof_v1_retrosheet2024",
  "feature_set_version": "pregame_safe_v1",
  "is_research": true,
  "is_synthetic": false,
  "leakage_audit_passed": false,
  "generated_at": "2026-05-13T00:00:00Z"
}
```

**Required flags:**
- `is_research: true` — mandatory; prevents production use
- `leakage_audit_passed: false` — must stay false until formal audit completed
- `is_synthetic: false` — true only for fixture-based smoke tests

### 5.4 Leakage Audit Report

Output: `reports/leakage_audit_p38a_YYYYMMDD.md`

Must contain:
- Feature-by-feature leakage analysis
- Date filter verification (rolling windows use strict `< game_date` filter)
- Sentinel test results (see Section 6)
- Sign-off status: PENDING / PASSED / FAILED

### 5.5 Replay Join Certification

Output: `reports/replay_join_cert_p38a_YYYYMMDD.md`

Must contain:
- Join rate: (games joined / total games) — target ≥ 90%
- Unjoined games: list with reason codes
- Odds proxy source used for join test
- Join key used: `game_date + home_team_id + away_team_id`
- Certification status: PENDING / CERTIFIED / FAILED

---

## 6. Minimum Smoke Test Specifications

### 6.1 Fixture-Only Smoke

```
smoke_id: FIXTURE_SMOKE_P38A
purpose: Validate pipeline end-to-end with known fixture data
input: data/fixtures/p38a_fixture_2024_games.csv (10 games, hardcoded)
expected:
  - 10 rows in output JSONL
  - All rows have is_synthetic=true
  - All rows have is_research=true
  - No NaN in feature columns
  - predicted_home_win_prob in (0.0, 1.0)
  - predicted_total_runs > 0
pass_criteria: All 6 assertions pass
```

### 6.2 Small Date-Range Replay Smoke

```
smoke_id: DATERANGE_SMOKE_P38A
purpose: Validate date-ordered replay with real Retrosheet data
input: Retrosheet 2024, April 1–7 (7 days, ~40 games)
expected:
  - Output contains expected game count for that range
  - No game_date > 2024-04-07 in features derived before 2024-04-07
  - game_key format: YYYY-MM-DD_AAA_HHH
pass_criteria: Date integrity + game count check pass
```

### 6.3 Leakage Sentinel Test

```
smoke_id: LEAKAGE_SENTINEL_P38A
purpose: Confirm no postgame data enters pregame features
method:
  1. For 20 games in 2024, manually verify home_win_pct_last_30
     only uses games strictly before game_date.
  2. Randomly inject a future-date game into rolling window source.
  3. Assert prediction output changes (leakage detected).
  4. Remove injection, assert prediction returns to baseline.
pass_criteria: No leakage detected in step 1; leakage correctly detected in step 3
```

### 6.4 Deterministic Output Check

```
smoke_id: DETERMINISM_P38A
purpose: Confirm pipeline produces identical output on re-run
method:
  1. Run pipeline twice on same input
  2. diff output JSONL files
  3. Assert diff is empty
pass_criteria: diff is empty (hash match)
```

---

## 7. Execution Prerequisites

Before starting P38A runtime work:

- [ ] P1 (Free-Source Odds Feasibility Spike) must have at least one ACCEPTABLE_FOR_RESEARCH source identified
- [ ] Retrosheet 2024 game logs must be present at `data/mlb_2024/raw/GL2024.TXT`
- [ ] Retrosheet 2024 schedule must be present at `data/mlb_2024/raw/2024SKED.TXT`
- [ ] Team mapping file must be present and normalized
- [ ] Feature manifest v1.0 approved (this document serves as draft)
- [ ] Leakage audit framework in place (scripts/leakage_audit.py or equivalent)

---

## 8. Open Questions

| Question                                   | Owner       | Due           |
|--------------------------------------------|-------------|---------------|
| Does GL2024.TXT already exist in repo?     | Agent       | Next session  |
| What model architecture for OOF rebuild?   | CTO         | P38A planning |
| Join key format: use Retrosheet game_id?   | CTO         | P38A planning |
| Rolling window: 30d or 30 games?           | CTO         | P38A planning |

---

**Acceptance Marker:** P38A_RETROSHEET_OOF_REBUILD_PLAN_20260513_READY
