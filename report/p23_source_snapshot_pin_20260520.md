# P23-C Source Snapshot Pin Report
**日期：** 2026-05-20  
**Phase：** P23_SOURCE_SNAPSHOT_PIN  
**Task：** P23-C  
**paper_only：** true

---

## 1. 當前快照（P23 時間點）

| 欄位 | 值 |
|------|----|
| 檔案 | `data/tsl_odds_history.jsonl` |
| **行數** | **2,788** |
| **SHA256** | `ac1320de7efa23e645ffb81f27c9825634c3d63566ed8ccf5c62ee6cf7c94118` |
| 第一筆 fetched_at | `2026-03-13T03:30:16.039741Z` |
| 第一筆 game_time | `2026-03-13T12:00:00+08:00` |
| 最後筆 fetched_at | `2026-05-20T03:06:23.144632Z` |
| 最後筆 game_time | `2026-05-20T09:40:00+08:00` |

### 驗證指令
```bash
wc -l data/tsl_odds_history.jsonl
# → 2788 data/tsl_odds_history.jsonl

shasum -a 256 data/tsl_odds_history.jsonl
# → ac1320de7efa23e645ffb81f27c9825634c3d63566ed8ccf5c62ee6cf7c94118  data/tsl_odds_history.jsonl
```

## 2. P19 Source Baseline（回溯）

| 欄位 | 值 | 備注 |
|------|-----|------|
| 行數 | 2,747 | P19 artifact `total_records` 欄位 |
| SHA256 | 未 pin | P19 artifact 未記錄 |
| game_date_range | 2026-03-13 ~ 2026-05-20 | P19 artifact 記錄 |
| unique_match_ids | 859 | P19 artifact 記錄 |
| valid_clv_pairs | 233 | P19 artifact 記錄 |

> ⚠️ P19 未記錄 SHA256，無法重建 P19 時的精確檔案狀態。

## 3. P22 Source Baseline（回溯）

| 欄位 | 值 | 備注 |
|------|-----|------|
| 行數 | 2,772 | P22 pipeline log 輸出 |
| SHA256 | 未 pin | P22 artifact 未記錄 |
| valid_clv_pairs | 236 | P22-E artifact 記錄 |

> ⚠️ P22 未記錄 SHA256。由於檔案持續增長，P22 時的精確 hash 無法還原。

## 4. 成長時間線

```
P19 計算 → 2,747 records (hash: 未知)
  ↓ +25 records (+18 match_ids, 3 complete → new valid pairs)
P22 計算 → 2,772 records (hash: 未知)
  ↓ +16 records
P23 今日 → 2,788 records (hash: ac1320de7efa23e6...)
```

`tsl_odds_history.jsonl` 為 append-only 日誌，持續由 TSL crawler 寫入，本任務**不修改**此檔案。

## 5. 建議（未來 P1+）

未來各 Phase 在計算 valid pairs 時應同步記錄：
- `sha256`（`shasum -a 256`）
- `line_count`（`wc -l`）
- `last_record_fetched_at`

以確保完整可重現性。

## 6. Pin 狀態

| 快照 | 狀態 |
|------|------|
| Current (P23) | ✅ PINNED（行數 + SHA256 + 時間範圍） |
| P19 baseline | ⚠️ PARTIAL（行數 + 時間範圍，無 SHA256） |
| P22 baseline | ⚠️ PARTIAL（行數估算，無 SHA256） |
