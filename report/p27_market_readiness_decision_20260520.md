# P27 Market Readiness Decision Report
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 決策矩陣

| Market | N | Mean CLV% | CI (95%) | CI∋0 | Classification |
|--------|---|-----------|----------|------|----------------|
| MNL | 681 | +0.0449 | [-0.22, +0.30] | Yes | MARKET_CLEAN_INCONCLUSIVE |
| HDC | 402 | -0.0027 | [-0.32, +0.32] | Yes | MARKET_CLEAN_INCONCLUSIVE |
| OU | 418 | +0.0377 | [-0.25, +0.33] | Yes | MARKET_CLEAN_INCONCLUSIVE |
| OE | 460 | +0.0083 | [-0.07, +0.09] | Yes | MARKET_CLEAN_INCONCLUSIVE |
| TTO | 370 | +0.0815 | [-0.31, +0.47] | Yes | MARKET_CLEAN_INCONCLUSIVE |
| **Excl-OE** | **1,871** | **+0.0403** | **[-0.12, +0.20]** | **Yes** | **INCONCLUSIVE** |

---

## 最終分類

**`P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE`**  
**`P27_OE_EXCLUSION_NO_SIGNAL_RECOVERY`**

---

## 各市場 Readiness 評估

### MNL — 維持觀察
- 最大樣本（N=681），CI 最有收斂潛力
- 需注意 team alias 造成的 MISSING_OUTCOME（3 pairs）是否影響樣本質量
- **不建議進入 optimizer**；繼續累積資料

### HDC — 低優先度
- 唯一 mean 為負（-0.0027%），CI 最寬（±0.32pp）
- 盤口調整最頻繁（56 LINE_MOVED skips）
- **建議觀察 LINE_MOVED 比率是否隨賽季收斂**

### OU — 中性觀察
- trimmed mean (+0.05%) 比 raw mean (+0.04%) 高，顯示有輕微 outlier 雜訊
- **建議觀察 OU total 移動頻率**

### OE — 排除 aggregate
- 結構性無訊號，positive rate 只有 15.65%
- **建議從 aggregate CLV 統計中永久排除，作獨立結構研究**

### TTO — 最高 mean，最不穩定
- mean +0.08% 最高，但 CI 最寬（±0.39pp 寬度）
- LINE_MOVED skips 最多（64），說明 team total 調整非常頻繁
- **不建議作為訊號市場**

---

## 下一輪行動建議

### 根據 P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE：

| 優先度 | 行動 | 理由 |
|--------|------|------|
| P1 | 持續 TSL 資料積累（2026 regular season） | 目前 N=236 pairs，需至少 500+ 才有統計力 |
| P2 | Model quality repair（MLB Brier=0.2487→目標<0.24） | CLV 訊號依賴預測準確度；模型品質是前提條件 |
| P3 | OE 排除後的 aggregate CI 監控 | 建立 OE-excluded CI 作為主要 CLV 追蹤指標 |
| P4 | MNL team alias investigation | 確認 MISSING_OUTCOME 是否影響 MNL 樣本 |

### 嚴格禁止：
- 不得以 weak-stable 或 inconclusive 結果作為 optimizer promotion 依據
- 不得替換 fixed_edge_5pct champion
- 不得聲稱任何市場有可獲利的 CLV 訊號

---

## Champion 狀態

| 項目 | 狀態 |
|------|------|
| Champion | fixed_edge_5pct |
| Champion status | PRESERVED |
| Promotion | FROZEN |
| Next promotion gate | 需 Brier < 0.245 + CLV CI 不穿越 0 + CEO 批准 |
