# P27 Final Validation Report
**Date**: 2026-05-20  
**Phase**: P27_PER_MARKET_CLV_ISOLATION  
**paper_only**: true | **diagnostic_only**: true

---

## 本輪目標

以 P26 line-aware matching 為基礎，對每個市場做獨立 CLV isolation，特別評估 OE 是否造成 aggregate 稀釋，並輸出 market readiness decision。

---

## 驗證矩陣

| 驗證項目 | 結果 |
|----------|------|
| P26 tests（23個） | **23/23 PASS** |
| P17 standalone | **64/64 PASS** |
| P13-P17 regression | **296/296 PASS** |
| **合計** | **383/383 PASS** |
| JSON schema（4個 P27 artifacts） | **4/4 PASS** |
| Forbidden affirmative scan | **0 hits** |
| No index fallback | **PASS** |
| P23/P26 baseline 未被覆蓋 | **PASS** |
| Live API / TSL crawler 未修改 | **PASS** |
| Source drift 記錄完整 | **PASS** |

---

## Source Snapshot 狀態

| 項目 | P23/P26 Pinned | Current |
|------|---------------|---------|
| Lines | 2,788 | 2,808（+20） |
| Action | — | 僅記錄，P27 diagnostic 使用前 2,788 行 |

---

## Per-Market 結果彙總

| Market | N | Mean% | CI (95%) | CI∋0 | |CLV|>50 | 分類 |
|--------|---|-------|----------|------|---------|------|
| MNL | 681 | +0.0449 | [-0.22, +0.30] | **Yes** | 0 | INCONCLUSIVE |
| HDC | 402 | -0.0027 | [-0.32, +0.32] | **Yes** | 0 | INCONCLUSIVE |
| OU | 418 | +0.0377 | [-0.25, +0.33] | **Yes** | 0 | INCONCLUSIVE |
| OE | 460 | +0.0083 | [-0.07, +0.09] | **Yes** | 0 | INCONCLUSIVE |
| TTO | 370 | +0.0815 | [-0.31, +0.47] | **Yes** | 0 | INCONCLUSIVE |

---

## OE Exclusion 結果

| 測試 | 結果 |
|------|------|
| OE 是否稀釋 aggregate | YES（但影響極小：+0.006pp） |
| 排除 OE 後 CI 仍穿越 0 | **YES**，CI=[-0.12, +0.20] |
| 排除 OE 後 CI 是否收窄 | **NO**（反而略微變寬） |
| 信號恢復 | **NO_RECOVERY** |

---

## 嚴格禁止確認

| 禁止事項 | 狀態 |
|---------|------|
| 合併 PR #2 | 未執行 |
| 聲稱可獲利 | 未聲稱 |
| CLV 轉投注建議 | 未作 |
| 替換 fixed_edge_5pct champion | 未替換 |
| Strategy optimizer promotion | 未啟動 |
| 修改 TSL crawler / live odds API | 未修改 |
| 覆蓋 P23/P24/P25/P26 baseline | 未覆蓋 |
| Index fallback | 未使用 |
| Weak-stable 結果作 production 依據 | 未作 |

---

## 最終分類

- **`P27_ALL_MARKETS_CLEAN_CLV_INCONCLUSIVE`**
- **`P27_OE_EXCLUSION_NO_SIGNAL_RECOVERY`**

所有 5 個市場的 clean CLV（P26 line-aware matching）在 95% bootstrap CI 下均不顯著。  
OE 排除後 CI 仍穿越 0，無信號恢復。  
champion=fixed_edge_5pct 維持，promotion frozen。
