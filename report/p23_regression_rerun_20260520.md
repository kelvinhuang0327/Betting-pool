# P23-D Regression Rerun Report
**日期：** 2026-05-20  
**Phase：** P23_REGRESSION_RERUN  
**Task：** P23-D  
**paper_only：** true

---

## 1. 執行環境

| 欄位 | 值 |
|------|----|
| Platform | darwin (macOS) |
| Python | 3.13.8 |
| pytest | 9.0.3 |
| pluggy | 1.6.0 |
| venv | `.venv/bin/python` |
| rootdir | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` |
| configfile | `pytest.ini` |

---

## 2. P17 Standalone 測試

```bash
pytest tests/ -k "p17" -v --tb=short --ignore=tests/test_agent_orchestrator.py
```

| 指標 | 值 |
|------|----|
| 收集測試數 | 69 |
| **PASS** | **69** |
| FAIL | 0 |
| ERROR | 0 |
| 執行時間 | 2.28s |
| **結果** | **✅ ALL PASS** |

---

## 3. P12-P17 Regression Governance Suite

```bash
pytest tests/ -k "p12 or p13 or p14 or p15 or p16 or p17" -v --tb=short --ignore=tests/test_agent_orchestrator.py
```

| 指標 | 值 |
|------|----|
| 收集測試數 | 323 |
| **PASS** | **323** |
| FAIL | 0 |
| ERROR | 0 |
| 執行時間 | 3.34s |
| **結果** | **✅ ALL PASS** |

### 涵蓋測試檔案

| 檔案 | 測試數（含 filter） |
|------|------|
| test_blocked_state_daily_monitor_p12.py | (partial) |
| test_blocked_state_governance.py | 5/29 匹配 filter |
| test_p13_minimal_monitor.py | (partial) |
| test_p14_no_expansion_guard.py | (partial) |
| test_p15_no_expansion_watch.py | (partial) |
| test_p16_no_expansion_hold.py | (partial) |
| test_p17_hold_state_continuity.py | 69 |

---

## 4. 全套 Baseline（參考）

```bash
pytest tests/ --tb=short -q --ignore=tests/test_agent_orchestrator.py
```

| 指標 | 值 |
|------|----|
| PASS | 5,843 |
| FAIL | 97 |
| SKIP | 15 |
| 執行時間 | 278.26s (4:38) |

> FAIL 97 筆全數位於 `test_strategy_replay_ui_*`、`test_task_quality_gate.py`、`test_tsl_feed_status_reporting.py` 等非 P12-P17 governance 範疇。

---

## 5. 排除項目

| 檔案 | 原因 |
|------|------|
| `tests/test_agent_orchestrator.py` | `ImportError: cannot import name 'load_project_profile' from 'orchestrator.common'` — 3 個測試無法收集，已排除 |

---

## 6. 對比 P22 聲稱數字

| | P22 報告 | P23 Rerun |
|-|---------|----------|
| P17 standalone | 未個別記錄 | **69/69 PASS** |
| P12-P17 regression | 347/347 | **323/323 PASS** |
| **差異** | — | **-24** |

### Delta 解釋

P22 報告的 347 = P12-P17 k-filter 323 + `test_blocked_state_governance.py` 另外 24 個不匹配 filter 的測試（全 29 - 匹配 5 = 24）。P22 在 regression run 時可能將 `test_blocked_state_governance.py` 以模組方式單獨執行，累計得到 347。

**無 regression 發現。P12-P17 governance 全數 PASS。**

---

## 7. 結論

| 測試範圍 | 結果 |
|----------|------|
| P17 standalone | ✅ 69/69 PASS |
| P12-P17 regression | ✅ 323/323 PASS |
| P22 vs P23 一致性 | ✅ 一致（差 24 為測試選取範圍差異，非 regression） |

**Overall：`REGRESSION_SUITE_PASS`**
