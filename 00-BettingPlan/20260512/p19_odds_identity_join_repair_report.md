# P19 Odds Identity Join Repair — 完成報告

**日期**: 2026-05-12  
**狀態**: ✅ P19_ODDS_IDENTITY_JOIN_REPAIR_READY  
**前驅**: P17 (paper ledger settlement)  
**目標**: 修復 `game_id` 身份識別 join 缺口，使 P17 結算能夠以 game_id 為 key 完整進行

---

## 問題背景

P17 settlement audit 發現 `simulation_ledger.csv` 缺少 `game_id` 欄位，無法進行 game-id-based join。原始 P15 管線只保留了 `row_idx` 作為索引，未將 `game_id` 寫入 ledger。

P19 任務：透過「位置對齊驗證 (positional alignment verification)」安全地將 `game_id` 從 `joined_oof_with_odds.csv` 反向注入 `simulation_ledger.csv`。

---

## 身份對齊方法

**核心洞察**：P15 的 `_prepare_rows_with_odds` 函數在建立 simulation_ledger 之前，會將 `joined_oof_with_odds` 按 `p_oof` **降序**排序，再指定 `row_idx = 0..N-1`。

只要確認 simulation_ledger 中的 `y_true`、`fold_id`、`p_model`（= p_oof）、`p_market` 在排序後完全對齊，即可安全以 row_idx 做 join。

**對齊安全條件**（需全部通過）：
- `y_true` 完全吻合
- `fold_id` 完全吻合
- `p_model` (= p_oof) max_diff < 1e-8
- `p_market` max_diff < 1e-6

---

## 執行結果

### P19 Identity Field Audit

| 項目 | 結果 |
|------|------|
| `simulation_ledger` game_id | 0 (缺失) |
| `joined_oof_with_odds` game_id | 1577 (全覆蓋) |
| 位置對齊驗證 | ✅ SAFE |
| 富集方法 | IDENTITY_ENRICHED_BY_VERIFIED_POSITIONAL_ALIGNMENT |
| 富集後 game_id 覆蓋率 | 6308/6308 = **100.0%** |
| 合約驗證 | ✅ PASS |

### P19 Settlement Join Repair Audit

| 項目 | 結果 |
|------|------|
| Join 方法 | JOIN_BY_GAME_ID |
| Join 覆蓋率 | **100.0%** |
| Join 品質 | **HIGH** |
| 整體 gate | **P19_IDENTITY_JOIN_REPAIR_READY** |

### P17 Replay (with P19 enriched ledger)

| 項目 | 結果 |
|------|------|
| 活躍下注數 | 324 |
| 已結算 WIN | 171 |
| 已結算 LOSS | 153 |
| 未結算 | **0** |
| ROI | **+10.7783%** |
| 整體 gate | **P17_PAPER_LEDGER_READY** |

### 決定論驗證

兩次獨立執行的 `enriched_simulation_ledger.csv` MD5 完全相同：

```
c2d8602f39f977caa5f9cd0c92af1280
```

---

## 輸出文件

### P19 輸出 (`outputs/predictions/PAPER/2026-05-12/p19_odds_identity_join_repair/`)

| 文件 | 說明 |
|------|------|
| `identity_field_audit.json` | 各文件 game_id 覆蓋率與對齊審計 |
| `identity_field_audit.md` | 人類可讀版本 |
| `enriched_simulation_ledger.csv` | 已注入 game_id 的 simulation_ledger (6308 rows) |
| `identity_enrichment_summary.json` | 富集方法、覆蓋率統計 |
| `identity_enrichment_summary.md` | 人類可讀版本 |
| `settlement_join_repair_audit.json` | settlement join 修復審計 |
| `settlement_join_repair_audit.md` | 人類可讀版本 |
| `p19_gate_result.json` | 最終 gate 結果 |

### P17 Replay 輸出 (`outputs/predictions/PAPER/2026-05-12/p17_replay_with_p19_identity/`)

| 文件 | 說明 |
|------|------|
| `paper_recommendation_ledger.csv` | 完整結算 ledger (1577 rows) |
| `paper_recommendation_ledger_summary.json` | 摘要統計 (含 source_p19_enrichment=true) |
| `settlement_join_audit.json` | settlement join 審計記錄 |
| `ledger_gate_result.json` | gate 決策 |

---

## 測試覆蓋

| 測試文件 | 測試數 | 狀態 |
|----------|--------|------|
| `test_p19_identity_field_audit.py` | 10 | ✅ 全通過 |
| `test_p19_p15_ledger_identity_enricher.py` | 15 | ✅ 全通過 |
| `test_run_p19_odds_identity_join_repair.py` | 6 | ✅ 全通過 |
| `test_run_p17_replay_with_p19_enriched_ledger.py` | 5 | ✅ 全通過 |
| **合計** | **39** | **✅ 39/39** |

---

## 關鍵技術洞察

1. **p_model = p_oof in simulation_ledger**: P15 在寫入 simulation_ledger 時，`p_model` 欄位儲存的是 OOF 機率值（`p_oof`），而非獨立的 model 預測值。對齊驗證必須比較 `sim["p_model"]` vs `jof["p_oof"]`。

2. **位置對齊後 join 是安全的**: P15 排序是確定性的（`p_oof` 降序），且 simulation_ledger 的 `row_idx` 直接對應排序後的位置索引。只要對齊 4 個欄位均通過，game_id 的傳遞是 100% 安全的。

3. **無 look-ahead leakage**: game_id 是比賽識別符，不是未來資訊。將其從 `joined_oof_with_odds` 反向填入 `simulation_ledger` 不引入任何資料滲透風險。

---

## 安全守則

- `PAPER_ONLY = True` — 本報告所有分析均為 paper trading 模式
- `PRODUCTION_READY = False` — 未授權任何真實資金操作
- 無 TSL 爬取、無真實下注、無 push 至遠端

---

## 終端標記

```
P19_ODDS_IDENTITY_JOIN_REPAIR_READY
```
