---
name: update-wbc-data
description: "更新數據 — 更新 WBC 2026 賽事資料。Use when: 更新數據、更新賽事結果、抓取最新比分、更新球員名單、更新投手數據、更新打擊數據、fetch WBC scores、update game results、update rosters、update stats。適用於每日賽前更新所有已完成賽事的成績與最新球員數據。"
argument-hint: "可指定日期 (YYYY-MM-DD) 或留空使用今天日期"
---

# 更新數據 (Update WBC Data)

更新 2026 WBC 經典賽所有已完成賽事的比分、球員數據、以及台灣運彩賠率。

## 適用時機
- 每日賽前，更新所有已完成比賽的結果
- 需要抓取最新球員名單或統計數據
- 需要更新台灣運彩 (TSL) 最新賠率
- 需要重建權威數據快照 (authoritative snapshot)

## 完整更新流程

依照以下順序執行，每步驟完成後確認無錯誤再進行下一步。

### Step 1: 抓取即時比分 (Fetch Live/Final Scores)

從 MLB Stats API (sportId=51) 抓取已完成賽事比分。

```python
# 使用 data/live_updater.py
from data.live_updater import LiveDataEngine

engine = LiveDataEngine()

# 抓取指定日期（或今日）的比分
results = engine.fetch_live_scores("YYYY-MM-DD")  # 留空 = 今天
for game in results:
    print(f"{game['away']} {game['away_score']} - {game['home_score']} {game['home']}")
    print(f"  Status: {game['status']}")
```

若需要抓取多天的歷史成績，依照 [wbc_2026_schedule_tpe.md](../../../docs/reference/wbc_2026_schedule_tpe.md) 中的賽程逐日查詢：
- Pool C (東京): 03/05 ~ 03/10
- Pool A (聖胡安): 03/07 ~ 03/12
- Pool B (休士頓): 03/07 ~ 03/12
- Pool D (邁阿密): 03/07 ~ 03/11

### Step 2: 更新球隊名單 (Update Rosters)

從 MLB Stats API 抓取最新 WBC 各隊 30 人名單。

```bash
python scripts/legacy_entrypoints/fetch_wbc_all_players.py
```

**輸出檔案**: `data/wbc_all_players_realtime.json`
- 內容：各隊球員 ID、姓名、守備位置

### Step 3: 更新球員賽季統計 (Update Player Stats)

抓取各球員 2025/2026 賽季的投打數據。

```bash
python scripts/legacy_entrypoints/fetch_wbc_2025_stats_full.py
```

**輸出檔案**: `data/wbc_players_2025_stats.json`

### Step 4: 重建權威數據快照 (Rebuild Authoritative Snapshot)

合併賽程、名單、先發投手等資訊為單一權威數據源。

```bash
python scripts/build_wbc_authoritative_snapshot.py
```

**輸出檔案**: `data/wbc_2026_authoritative_snapshot.json`
- 包含所有 40 場預賽的完整比賽資料
- 用於模型分析前的數據驗證

### Step 5: 抓取國際盤口賠率 (Fetch International Odds)

從 The Odds API 或 Pinnacle 等國際盤口抓取最新賠率。

```python
from data.odds_api_client import OddsAPIClient

client = OddsAPIClient()  # 若有 API Key 可傳入: OddsAPIClient(api_key="YOUR_KEY")
games = client.fetch_baseball_odds(sport="baseball_wbc")

if games:
    for g in games:
        home = g["home_team"]
        away = g["away_team"]
        print(f"\n{away} @ {home}")
        for bm in g.get("bookmakers", []):
            for mkt in bm.get("markets", []):
                outcomes = ", ".join([f"{o['name']} {o['price']}" for o in mkt["outcomes"]])
                print(f"  [{bm['key']}] {mkt['key']}: {outcomes}")
else:
    print("⚠️ 國際盤口：無資料 (API 未回傳或尚未開盤)")
```

也可以查詢特定比賽的 Pinnacle 賠率：
```python
odds = client.get_match_odds("Japan", "Czech Republic")
if odds:
    print(f"ML: {odds.away_ml} / {odds.home_ml}")
    print(f"Spread: {odds.spread_line} ({odds.spread_away} / {odds.spread_home})")
    print(f"Total: {odds.total_line} (O {odds.over_price} / U {odds.under_price})")
else:
    print("⚠️ 該場比賽國際盤口尚無資料")
```

**注意**：
- 免費 API Key 每月有請求額度限制，`DEMO` 模式使用內建模擬數據
- 國際盤口通常比台灣運彩更早開盤，可作為台灣運彩盤口的預估參考
- 若 API 無回傳，顯示「無資料」即可，模型會回退使用 pool data 中的 seed odds

### Step 6: 抓取台灣運彩賠率 (Fetch TSL Odds)

抓取台灣運彩當前開盤的所有棒球賠率。

```python
from data.tsl_crawler_v2 import TSLCrawlerV2

crawler = TSLCrawlerV2()
games = crawler.fetch_baseball_games()

if games:
    for game in games:
        print(f"{game}")
else:
    print("⚠️ 台灣運彩：無資料 (尚未開盤或 API 被 Cloudflare 阻擋)")
```

**注意**：
- 台灣運彩 API 可能受 Cloudflare 保護，回傳非 JSON 格式
- 若抓取失敗，顯示「無資料」，分析時可參考國際盤口或使用 pool data 中的 seed odds
- 通常台灣運彩會在賽前 1-2 天開盤，若比賽當天仍無資料屬於正常情況

### Step 7: 更新驗證覆寫檔 (Update Verified Overrides — 如需要)

若有球員傷病、陣容異動等手動修正，更新 `data/wbc_verified_overrides.json`：

```json
{
  "games": {
    "C01": {
      "home_sp_override": "新投手姓名",
      "notes": "原先發投手因傷退出"
    }
  }
}
```

## 快速更新指令 (一鍵全更新)

```bash
# 完整更新流程（不含盤口）
python scripts/legacy_entrypoints/fetch_wbc_all_players.py && \
python scripts/legacy_entrypoints/fetch_wbc_2025_stats_full.py && \
python scripts/build_wbc_authoritative_snapshot.py
```

## 資料檔案清單

| 檔案路徑 | 說明 | 更新方式 |
|----------|------|---------|
| `data/wbc_all_players_realtime.json` | 各隊名單 | `scripts/legacy_entrypoints/fetch_wbc_all_players.py` |
| `data/wbc_players_2025_stats.json` | 球員統計 | `scripts/legacy_entrypoints/fetch_wbc_2025_stats_full.py` |
| `data/wbc_2026_authoritative_snapshot.json` | 權威快照 | `scripts/build_wbc_authoritative_snapshot.py` |
| `data/wbc_hitting_stats_2026.json` | 打擊特徵向量 | 模型內部產生 |
| `data/wbc_pitching_stats_2026.json` | 投手特徵向量 | 模型內部產生 |
| `data/wbc_verified_overrides.json` | 手動修正 | 手動編輯 |
| `docs/reference/wbc_2026_schedule_tpe.md` | 完整賽程表 | 參考用 |

### 盤口資料來源優先級

| 優先級 | 來源 | 說明 |
|--------|------|------|
| 1 | 台灣運彩 (TSL) | 實際下注用的賠率，最重要 |
| 2 | 國際盤口 (Pinnacle) | TSL 未開盤時作為參考 |
| 3 | Pool Seed Odds | 內建種子賠率，作為最終兜底 |

> 若 TSL 與國際盤口皆無資料，模型會自動使用 pool data 中的 seed odds 進行分析。

## 驗證更新是否成功

更新完成後，執行以下確認：

1. 確認 JSON 檔案的更新時間為今日
2. 確認各隊球員數量合理（25-30 人/隊）
3. 確認已完成賽事的比分已記錄
4. 如有異常，檢查 API 回傳狀態碼與錯誤訊息

## 注意事項
- MLB Stats API 是免費公開的，無需 API Key
- 台灣運彩 API 可能受 Cloudflare 保護，`TSLCrawlerV2` 已有模擬瀏覽器 headers
- 建議在台灣時間早上 8:00 前完成更新（趕在第一場比賽前）
- 連續大量 API 請求時加入適當延遲 (`time.sleep(0.1)`) 避免被封鎖
