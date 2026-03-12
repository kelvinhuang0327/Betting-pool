---
name: analyze-wbc-betting
description: "分析數據 — 分析 WBC 2026 當天賽事並產出台灣運彩投注建議。Use when: 分析數據、分析比賽、投注建議、下注策略、今日賽事分析、分析賠率、預測比分、betting analysis、predict game、analyze matchup、today games。執行完整的 10 步分析管線，產出包含不讓分、讓分、大小分、單雙、前五局等所有台灣運彩玩法的 EV 分析與 Kelly 倉位建議。"
argument-hint: "指定 game_id (如 C01) 或日期 (如 03/10)，留空則分析今日所有賽事"
---

# 分析數據 (Analyze WBC Betting)

針對 WBC 2026 當天賽事執行完整量化分析，產出台灣運彩 (TSL) 投注策略報告。

## 適用時機
- 每日賽前分析當天所有比賽的投注價值
- 針對特定比賽 (game_id) 做深度分析
- 需要台灣運彩各玩法的 EV 計算與 Kelly 倉位
- 想了解兩隊戰力對比與比分預測

## 賽程查詢

首先確認今天有哪些比賽。參照 [wbc_2026_schedule_tpe.md](../../../docs/reference/wbc_2026_schedule_tpe.md) 找出今日賽事的 game_id。

Game ID 格式: `{Pool}{Number}`
- Pool A: A01–A10 (波多黎各聖胡安)
- Pool B: B01–B10 (美國休士頓)
- Pool C: C01–C10 (日本東京)
- Pool D: D01–D10 (美國邁阿密)

快速列出所有賽事：
```bash
python main.py --list
```

## 分析流程

### Step 1: 確認數據已更新

在分析前，先確保資料是最新的。若今天尚未更新，請先執行 `/update-wbc-data` skill。

關鍵檢查：
- `data/wbc_2026_authoritative_snapshot.json` 是否為最新
- 先發投手名單是否已確認

### Step 2: 抓取盤口賠率 (Fetch Odds from All Sources)

分析前抓取國際盤口與台灣運彩賠率，用於報告對照。

```python
from data.odds_api_client import OddsAPIClient
from data.tsl_crawler_v2 import TSLCrawlerV2

# 1) 國際盤口 (Pinnacle / The Odds API)
client = OddsAPIClient()
international_odds = client.fetch_baseball_odds(sport="baseball_wbc")
if international_odds:
    print(f"✅ 國際盤口: 取得 {len(international_odds)} 場賠率")
else:
    print("⚠️ 國際盤口: 無資料")

# 2) 台灣運彩 (TSL)
crawler = TSLCrawlerV2()
tsl_odds = crawler.fetch_baseball_games()
if tsl_odds:
    print(f"✅ 台灣運彩: 取得 {len(tsl_odds)} 場賠率")
else:
    print("⚠️ 台灣運彩: 無資料 (尚未開盤或 Cloudflare 阻擋)")
```

**盤口來源優先級**：
1. 台灣運彩 (TSL) → 實際下注用的賠率
2. 國際盤口 (Pinnacle) → TSL 未開盤時參考
3. Pool Seed Odds → 內建種子賠率，作為最終兜底

> 若全部無資料，模型會自動使用 pool data (`data/wbc_pool_*.py`) 中的 `odds_params` 進行分析。

### Step 3: 執行單場分析

```bash
# 分析特定比賽
python main.py --game=C01

# 分析特定比賽 + 輸出原始 JSON
python main.py --game=C01 --json
```

### Step 4: 執行批次分析（當天所有比賽）

```bash
# 分析所有 40 場預賽
python main.py --all

# 只分析特定組別
python main.py --all=C         # Pool C 所有比賽
python main.py --all=A,B       # Pool A + B
python main.py --all=ABCD      # 全部
```

### Step 5: 進階後端分析管線（如可用）

```bash
# 後端完整管線（含部署閘門、特徵工程、走前驗證）
python -m wbc_backend.run --game WBC26-TPE-AUS-001

# 含回測驗證
python -m wbc_backend.run --train --backtest --all
```

## 分析管線 10 步驟詳解

分析引擎（`main.py`）依序執行：

| 步驟 | 模組 | 說明 |
|------|------|------|
| 1 | `data/wbc_pool_*.py` | 載入比賽資料（兩隊陣容、先發投手、打線） |
| 2 | `wbc_backend/data/wbc_verification.py` | 驗證數據完整性，交叉比對權威快照 |
| 3 | `models/ensemble.py` | 6 模型集成預測（Elo 45% + Bayesian 25% + Poisson 15% + GB 10% + MC 5%） |
| 4 | `wbc/adjustments.py` | WBC 特殊規則修正（用球數限制、牛棚疲勞、短賽變異） |
| 5 | 機率計算 | 建立所有市場的真實機率 (true_probs) |
| 6 | `strategy/value_detector.py` | 比對賠率找出 +EV 投注機會 |
| 7 | `strategy/sharp_detector.py` | 偵測市場訊號（盤口異動、聰明錢方向） |
| 8 | `strategy/risk_control.py` | 風險評估（日損限制 15%、最大回撤 20%） |
| 9 | `strategy/kelly_criterion.py` | Kelly 倉位管理（1/6 Kelly，單注上限 1.5%） |
| 10 | `report/formatter.py` | 產出完整 Markdown 分析報告 |

## 報告包含的盤口對照與台灣運彩分析

每場比賽的報告應包含以下盤口資訊：

### 盤口對照表 (Odds Comparison)

列出各市場的三個盤口來源以便對照：

| 欄位 | 說明 |
|------|------|
| 台灣運彩 (TSL) | 實際可下注的賠率，無資料時顯示 「— 尚未開盤」 |
| 國際盤口 (Pinnacle) | 國際盤口參考值，無資料時顯示 「— 無資料」 |
| Seed Odds | pool data 中的內建賠率（永遠有值） |
| 盤口來源 | 標註模型實際使用的賠率來源 |

**顯示規則**：
- 若 TSL 有資料 → 盤口來源標註 `✅ TSL`
- 若 TSL 無資料但國際盤口有 → 標註 `✅ 國際`
- 若全部無資料 → 標註 `⚠️ Seed`，並在報告頂部加警語：`⚠️ 本場分析使用內建種子賠率，僅供參考`

### 台灣運彩玩法分析

| 台灣運彩玩法 | 代碼 | 分析內容 |
|-------------|------|---------|
| **不讓分（獨贏）** | ML | 真實勝率 vs 盤口賠率 → EV% |
| **讓分** | RL | 穿盤機率（依打線串連度 & 牛棚深度） |
| **大小分** | OU | 總分分佈 Over/Under 機率（Poisson + MC） |
| **單雙** | OE | 總分奇偶機率（Poisson 公式推導） |
| **前五局獨贏** | F5 | 先發投手主導的前半段勝負 |
| **隊伍總分** | TT | 各隊得分 Over/Under（Lambda 獨立計算） |

每個玩法都會計算：
- **真實機率** (True Probability)
- **盤口賠率** (Market Decimal Odds)
- **期望值 EV%** = `(true_prob × decimal_odds) - 1`
- **信心等級**: ★★★★★ (EV ≥ 7%) / ★★★☆☆ (3-7%) / ★☆☆☆☆ (1-3%) / SKIP (< 1%)
- **Kelly 倉位百分比** (Fractional Kelly sizing)

## 報告輸出範例

```
# WBC 2026: 中華台北 (TPE) vs 澳洲 (AUS) — Pool C, C01

## 盤口對照表 (Odds Comparison)

| 市場 | 台灣運彩 (TSL) | 國際盤口 (Pinnacle) | Seed Odds | 盤口來源 |
|------|----------------|---------------------|-----------|----------|
| ML TPE | 1.75 | 1.62 | 1.75 | ✅ TSL |
| ML AUS | 2.10 | 2.35 | 2.15 | ✅ TSL |
| RL TPE -1.5 | 2.10 | 2.10 | 2.20 | ✅ TSL |
| OU 8.0 Over | 1.90 | 1.95 | 1.85 | ✅ TSL |
| F5 TPE | 1.75 | — | 1.80 | ✅ TSL |

> ✅ = 實際使用的賠率來源。若 TSL 無資料，自動改用國際盤口；全部無資料則使用 Seed Odds。

## 推薦下注 (Taiwan Sports Lottery)

| 市場 | 選項 | 真實機率 | 盤口賠率 | EV% | Kelly % | 信心度 |
|------|------|---------|---------|-----|---------|--------|
| ML   | TPE  | 59.5%   | 1.750   | +6.8% | 1.5%  | ★★★★☆ |
| RL   | TPE -2.5 | 42.3% | 2.050 | +3.2% | 0.5% | ★★★☆☆ |
| OU   | Over 7.5 | 52.1% | 1.900 | -1.2% | ——   | SKIP   |
| F5   | TPE  | 60.8%   | 1.850   | +8.1% | 2.0%  | ★★★★★ |

## 最終投組 (Final Portfolio)
- 總下注額: 2.5% bankroll
- 預期報酬: +6.2%
```

## WBC 用球數限制提醒

分析時務必關注用球數限制對比賽的影響：

| 賽程階段 | 單場上限 | 先發投手預估局數 | 牛棚影響權重 |
|---------|---------|----------------|-------------|
| 預賽 Pool | 65 球 | ~3.5 局 | 60%+ |
| 複賽 | 80 球 | ~4.5 局 | 50%+ |
| 準決賽/決賽 | 95 球 | ~5.5 局 | 40%+ |

**關鍵因素**:
- 第二先發 (Piggyback Starter) 品質是隱藏關鍵
- 連續賽程下牛棚疲勞度累積（近 3 日用球數）
- 教練團提前換投策略影響後半段比分與大小分

## 風險控制參數

| 參數 | 值 | 說明 |
|------|---|------|
| Kelly 分數 | 1/6 | 保守 fractional Kelly |
| 單注上限 | 1.5% bankroll | 硬性上限 |
| 日曝險上限 | 4% bankroll | 每日最大投入 |
| 日損停損 | 15% | 當日虧損達此比例停止下注 |
| 連敗降注 | 連 3 敗減 50% | 自動降低倉位 |
| 最大回撤 | 20% | 從峰值回落達此比例進入保守模式 |

## 注意事項

- 分析前務必確認數據已更新（先跑 `/update-wbc-data`）
- 先發投手名單通常在比賽前 2-4 小時才確定，需即時更新
- EV < 1% 的投注建議跳過（SKIP），不要為了下注而下注
- 所有建議皆經過 Kelly Criterion 倉位管理，嚴禁全押
- 報告中的機率為模型預測值，實際結果受隨機性影響
