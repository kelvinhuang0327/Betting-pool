# P1 Metrics SSOT — Phase67–72 Metrics Schema 統一研究報告

**日期**: 2026-05-07  
**報告路徑**: `00-BettingPlan/20260507/metrics_ssot_phase67_72_inventory_report_20260507.md`  
**JSON 清單**: `reports/metrics_ssot_phase67_72_inventory_20260507.json`  
**Gate**: `METRICS_SSOT_FOUNDATION_READY`

> ⚠️ **NO EDGE CLAIM** — 本報告僅為量化研究 / 統計診斷用途。  
> 不構成任何投注邊際聲明、預期價值保證或盈利主張。  
> 所有分析均使用歷史回測數據，過去表現不代表未來結果。  
> `PRODUCTION_MODIFIED = False` | `CANDIDATE_PATCH_CREATED = False` | `ALPHA_MODIFIED = False`

---

## 一、任務背景 (P1 任務說明)

**P1 任務目標**: 建立 Metrics SSOT（Single Source of Truth）foundation，讓 Phase67–72 以及後續 phase 的 audit/report 可以共用一致的 metrics schema、計算函式、報告格式與 safety flag。

**核心問題**: Phase67–72 各自在 orchestrator 中定義了 private 版本的 `_brier`、`_ece`、`_bss`、`BootstrapCI`、`NegativeControl`、`SegmentMetrics` dataclass，但命名與欄位不一致，導致：
- 跨 phase 的 schema 比較困難
- Future phases 需要自行決定要 copy 哪個版本
- Safety flag 覆蓋率不一致

**本輪不做的事** (防止 regression risk):
- ❌ 不修改 Phase67–71 現有 orchestrator
- ❌ 不替換任何生產預測數據
- ❌ 不 patch 任何 model_home_prob / ALPHA

---

## 二、SSOT 模組設計 (`orchestrator/metrics_ssot.py`)

### 2.1 架構原則

```
orchestrator/metrics_ssot.py
├── Safety constants (module-level, read-only)
├── 7 Gate constants + VALID_GATES (frozenset)
├── 9 Canonical dataclasses
├── 13 Pure math functions (zero I/O)
├── Validation: validate_metrics_payload()
├── Serialisation: ssot_to_dict()
└── Inventory helpers: CANONICAL_* fields + PHASE_SCHEMA_INVENTORY
```

### 2.2 Safety Constants

| Constant | Value | 說明 |
|---|---|---|
| `PRODUCTION_MODIFIED` | `False` | 不改生產預測 |
| `CANDIDATE_PATCH_CREATED` | `False` | 不建立 patch |
| `ALPHA_MODIFIED` | `False` | ALPHA=0.40 不動 |
| `PREDICTION_JSONL_OVERWRITTEN` | `False` | JSONL 不覆寫 |
| `NO_EDGE_CLAIM` | `True` | 無投注邊際聲明 |
| `NO_PROFIT_CLAIM` | `True` | 無盈利聲明 |
| `DIAGNOSTIC_ONLY` | `True` | 純診斷模式 |

### 2.3 Canonical Dataclasses

| Dataclass | 主要欄位 | 對應前身 |
|---|---|---|
| `BrierResult` | n, brier, baseline_brier, bss_vs_baseline | 無統一前身 |
| `ECEBucket` | bin_index, bin_lo, bin_hi, n, mean_predicted, mean_observed, abs_calibration_error, weight | 無統一前身 |
| `ECEResult` | n, ece, n_bins, buckets | 無統一前身 |
| `ResidualSummary` | n, residual_mean, residual_std, residual_min, residual_max, overconfident_bands, underconfident_bands | Phase70/71 residual stats |
| `SegmentMetricsSSO` | 18 fields (see below) | Phase71 `SegmentMetrics` (最完整) |
| `BootstrapCISSO` | 13 fields (see below) | Phase70/71 `BootstrapCI` + Phase69 `method` |
| `NegativeControlSSO` | 11 fields (see below) | Phase70/71 `NegativeControlResult` (最完整) |
| `GateSummarySSO` | phase_id, gate, gate_candidates, rationale, safety flags, report_paths, completion_marker | Phase72 gate summary |
| `MetricsPayload` | phase_id, n_samples, brier, ece, segments, negative_controls, gate_summary | 統一 container |

### 2.4 SegmentMetricsSSO 完整欄位

```python
@dataclass
class SegmentMetricsSSO:
    segment_name: str
    segment_definition: str
    n: int
    # Model metrics
    model_brier: float
    model_ece: float
    model_residual_mean: float
    model_residual_std: float
    model_mean_prob: float
    # Market metrics
    market_brier: float
    market_ece: float
    market_residual_mean: float
    market_mean_prob: float
    # Delta
    brier_delta: float           # model_brier - market_brier
    bss_vs_market: float         # 1 - model_brier / market_brier
    model_minus_market_mean: float
    # Targets
    observed_win_rate: float
    # Flags
    market_superiority: bool
    data_limited: bool
    notes: str = ""
```

### 2.5 Public Functions (13 個)

| 函式 | 說明 |
|---|---|
| `calculate_brier_score(probs, labels, baseline_probs)` | Brier score + BSS vs baseline |
| `calculate_bss(model_brier, ref_brier)` | BSS = 1 - model/ref |
| `calculate_ece(probs, labels, n_bins)` | ECE with bucket decomposition |
| `calculate_bucket_ece(probs, labels, n_bins)` | 只回傳 bucket list |
| `calculate_residual_summary(probs, labels, ...)` | Residual stats |
| `calculate_segment_metrics(...)` | 完整 SegmentMetricsSSO |
| `calculate_model_market_delta(...)` | Plain dict of delta metrics |
| `bootstrap_ci(values, stat_fn, ...)` | Generic bootstrap CI |
| `bootstrap_brier_delta_ci(model, market, labels, ...)` | Brier delta bootstrap |
| `build_negative_control_summary(...)` | NegativeControlSSO builder |
| `build_gate_summary(...)` | GateSummarySSO builder (validates gate) |
| `validate_metrics_payload(payload)` | Schema validator → list[str] |
| `ssot_to_dict(obj)` | Recursive dataclass → dict serialiser |

---

## 三、Phase67–72 Metrics Schema 清單

### 3.1 Brier / BSS / ECE 重複計算

Phase67–71 各自定義了 private 版本的計算函式。以下為重複實作清單：

| Function Pattern | 出現 Phases | SSOT 對應函式 |
|---|---|---|
| `_brier_score` (Phase67) / `_brier` (Phase68–71) | Phase67, 68, 69, 70, 71 | `calculate_brier_score()` |
| `_bss_direct` | Phase67, 68, 69, 70, 71 | `calculate_bss()` |
| `_compute_ece` (Phase67) / `_ece` (Phase68–71) | Phase67, 68, 69, 70, 71 | `calculate_ece()` |
| `_bootstrap_ci` / `_bootstrap_brier_delta` 等 | Phase67, 69, 70, 71 | `bootstrap_ci()` / `bootstrap_brier_delta_ci()` |

**合計**: 19 個重複函式實例分散在 5 個 phases（Phase72 是 paper-only，無計算函式）。

### 3.2 SegmentMetrics 欄位演進

| 欄位 | P67 | P68 | P69* | P70 | P71 | SSOT |
|---|---|---|---|---|---|---|
| `n` | ✅ | ✅ | N/A | ✅ | ✅ | ✅ |
| `model_brier` | ✅ | ✅ | N/A | `brier` ⚠️ | ✅ | `model_brier` |
| `market_brier` | ✅ | ✅ | N/A | ✅ | ✅ | ✅ |
| `blend_brier` | ✅ | ✅ | N/A | ❌ | ❌ | ❌ (移除) |
| `model_ece` | `ece_blend`⚠️ | `ece_model`⚠️ | N/A | `ece`⚠️ | ✅ | `model_ece` |
| `market_ece` | ❌ | `ece_market`⚠️ | N/A | ❌ | ✅ | `market_ece` |
| `model_residual_mean` | ❌ | ❌ | N/A | `residual_mean`⚠️ | ✅ | `model_residual_mean` |
| `market_residual_mean` | ❌ | ❌ | N/A | ✅ | ✅ | ✅ |
| `observed_win_rate` | ❌ | ❌ | N/A | ✅ | ✅ | ✅ |
| `bss_vs_market` | `blend_bss_vs_market`⚠️ | ✅ | N/A | ✅ | ✅ | ✅ |
| `model_mean_prob` | ❌ | `mean_model_fav_prob`⚠️ | N/A | `predicted_mean_prob`⚠️ | ✅ | `model_mean_prob` |
| `data_limited` | ❌ | ✅ | N/A | ✅ | ✅ | ✅ |
| `market_superiority` | ❌ | ❌ | N/A | `market_beats_model_brier`⚠️ | ✅ | `market_superiority` |
| `brier_delta` | ❌ | ❌ | N/A | ❌ | ✅ | ✅ |

*Phase69 使用 `CounterfactualMetrics`（結構完全不同，不在此表中比較）

### 3.3 BootstrapCI / BootstrapResult 欄位演進

| 欄位 | P67 (`BootstrapResult`) | P69 (`BootstrapCI`) | P70 (`BootstrapCI`) | P71 (`BootstrapCI`) | SSOT (`BootstrapCISSO`) |
|---|---|---|---|---|---|
| `metric` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `segment` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `n` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `n_boot` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `seed` | ❌ | ❌ | ❌ | ❌ | ✅ (新增) |
| `observed` | `observed_delta`⚠️ | ✅ | ✅ | ✅ | `observed` |
| `ci_lower` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ci_upper` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `ci_excludes_zero` | `significant`⚠️ | ✅ | ✅ | ✅ | `ci_excludes_zero` |
| `ci_stable` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `ci_width` | ❌ | ❌ | ❌ | ❌ | ✅ (新增) |
| `data_limited` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `method` | ❌ | ✅ (P69新增) | ❌ | ❌ | ✅ (optional, 預設"") |
| `prob_positive` | ✅ (P67特有) | ❌ | ❌ | ❌ | ❌ (移除) |

### 3.4 NegativeControl 欄位演進

| 欄位 | P67 | P68 | P69 | P70 | P71 | SSOT |
|---|---|---|---|---|---|---|
| `control_name` | ❌ (`dim`⚠️) | ✅ | ✅ | ✅ | ✅ | ✅ |
| `control_type` | ❌ (`segment`⚠️) | ❌ | ❌ | ❌ | ❌ | ✅ (新增) |
| `description` | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `n_permutations` | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| `seed` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (新增) |
| `observed_gap` | `real_blend_bss_delta`⚠️ | `real_bss`⚠️ | `real_improvement`⚠️ | ✅ | ✅ | `observed_gap` |
| `permuted_gap_mean` | `shuffled_mean_delta`⚠️ | `null_bss_mean`⚠️ | `null_improvement_mean`⚠️ | ✅ | ✅ | `permuted_gap_mean` |
| `permuted_gap_std` | `shuffled_std_delta`⚠️ | `null_bss_std`⚠️ | `null_improvement_std`⚠️ | ✅ | ✅ | `permuted_gap_std` |
| `signal_gap` | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `overfit_risk` | `null_rejected`⚠️ | ✅ | ✅ | ✅ | ✅ | `overfit_risk` |
| `interpretation` | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |

### 3.5 Safety Flag 覆蓋率

| Phase | CANDIDATE_PATCH_CREATED | PRODUCTION_MODIFIED | ALPHA_MODIFIED | DIAGNOSTIC_ONLY | PREDICTION_JSONL_OVERWRITTEN | PIT_SAFE_VALIDATION |
|---|---|---|---|---|---|---|
| Phase67 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Phase68 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Phase69 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Phase70 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Phase71 | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Phase72 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **SSOT Module** | ✅ | ✅ | ✅ | ✅ | ✅ | — |

Phase67–71 只有 3 個核心 safety flags；Phase72 引入了完整的 6 flag 模式。SSOT module 採用 Phase72 的完整模式。

---

## 四、Schema Gap 彙整

| Gap 類型 | 影響 Phases | SSOT 解決方案 |
|---|---|---|
| Brier fn 命名 (`_brier_score` vs `_brier`) | P67 vs P68–71 | `calculate_brier_score()` |
| ECE fn 命名 (`_compute_ece` vs `_ece`) | P67 vs P68–71 | `calculate_ece()` |
| BootstrapResult vs BootstrapCI schema | P67 (獨特) | `BootstrapCISSO` |
| NegativeControl field names | 各 phase 不同 | `NegativeControlSSO` |
| SegmentMetrics field names | P67/68/70 各異 | `SegmentMetricsSSO` |
| 缺少 `seed` in BootstrapCI | P67–71 全部 | SSOT 新增 `seed` 欄位 |
| 缺少 `ci_width` in BootstrapCI | P67–71 全部 | SSOT 新增 `ci_width` |
| 缺少 `control_type` in NegativeControl | P67–71 全部 | SSOT 新增 `control_type` |
| 缺少 `interpretation` in NegativeControl | P67–69 | SSOT 新增 `interpretation` |
| Safety flags 不完整 | P67–71 只有 3 flags | SSOT validate 會檢查 |

---

## 五、Future Phases 使用指引

### 5.1 如何在 Phase73+ 使用 SSOT

```python
# ✅ Future phases 應這樣使用
from orchestrator.metrics_ssot import (
    calculate_brier_score,
    calculate_ece,
    calculate_segment_metrics,
    bootstrap_brier_delta_ci,
    build_negative_control_summary,
    build_gate_summary,
    validate_metrics_payload,
    ssot_to_dict,
    SegmentMetricsSSO,
    BootstrapCISSO,
    NegativeControlSSO,
    METRICS_SSOT_FOUNDATION_READY,
    VALID_GATES,
)

# ❌ 不要再 copy-paste 這些 private 函式
# def _brier(probs, labels): ...
# def _ece(probs, labels, n_bins): ...
```

### 5.2 使用 validate_metrics_payload 防止 Schema Regression

```python
# 在 report 產出前驗證
errors = validate_metrics_payload(report_dict)
if errors:
    raise MetricsValidationError(f"Schema validation failed: {errors}")
```

### 5.3 使用 ssot_to_dict 序列化 Dataclass

```python
import json
report_dict = ssot_to_dict(metrics_payload_dataclass)
json.dump(report_dict, f, indent=2, ensure_ascii=False)
```

---

## 六、為什麼不重寫 Phase67–71 的歷史報告

本輪刻意不修改 Phase67–71 orchestrator，原因：

1. **Regression risk**: 現有 752 tests 全部通過，修改 private 函式會需要全面重測
2. **Data integrity**: 歷史 JSON 報告已存盤，修改 orchestrator 不會改變存盤的數字
3. **Scope control**: P1 任務目標是「建立 SSOT foundation」，不是「重構歷史」
4. **Audit trail**: 保留 Phase67–71 的原始實作有助於日後對照 SSOT 是否計算一致

**如需 Phase67–71 refactor**：建立一個獨立的 Phase73-governance 任務，逐步遷移，並附帶完整的數字等值驗證（old_brier == new_brier 對每一筆數據）。

---

## 七、風險評估

| 風險 | 等級 | 說明 | 緩解措施 |
|---|---|---|---|
| SSOT math 與 Phase70/71 不一致 | 低 | SSOT math 直接參照 Phase71 作為 reference | 93 個 unit tests 覆蓋所有計算函式 |
| Future phase 不使用 SSOT | 中 | 無強制機制 | CLAUDE.md 加入 SOP 規範；validate_metrics_payload 作為軟性約束 |
| SSOT module 引入 I/O 副作用 | 低 | 模組無 import data 模組，無 open() | test_no_live_pipeline_import 測試覆蓋 |
| SSOT 欄位設計不夠完整 | 低 | 參照 Phase67–72 全部 schema | PHASE_SCHEMA_INVENTORY 記錄完整來源 |

---

## 八、測試覆蓋摘要

| 測試類別 | 測試數 | 結果 |
|---|---|---|
| Safety constants | 10 | ✅ Pass |
| Gate constants (7 members check) | 4 | ✅ Pass |
| Brier / BSS math | 13 | ✅ Pass |
| ECE math + bucket schema | 12 | ✅ Pass |
| Residual summary | 3 | ✅ Pass |
| Segment metrics schema | 7 | ✅ Pass |
| Model-market delta | 3 | ✅ Pass |
| Bootstrap CI (determinism + schema) | 9 | ✅ Pass |
| Negative control schema | 6 | ✅ Pass |
| Gate summary schema | 4 | ✅ Pass |
| validate_metrics_payload | 10 | ✅ Pass |
| ssot_to_dict serialisation | 4 | ✅ Pass |
| Inventory constants | 11 | ✅ Pass |
| No production mutation | 2 | ✅ Pass |
| **合計** | **93** | **93/93 ✅** |

---

## 九、Gate 結論

**Gate: `METRICS_SSOT_FOUNDATION_READY`**

依據如下：

| 判斷條件 | 狀態 |
|---|---|
| SSOT 模組建立完成 | ✅ |
| 93 個 unit tests 全部通過 | ✅ |
| Phase67–72 schema inventory 完成 | ✅ |
| 命名不一致清單記錄完整 | ✅ |
| 重複計算函式清單完整 | ✅ (19 個實例) |
| Safety flag 覆蓋率分析完成 | ✅ |
| 生產程式碼未被修改 | ✅ |
| 無投注邊際聲明 | ✅ |
| JSON 報告已產出 | ✅ |
| Phase67–72 regression 全部通過 | 待下一步驗證 |

**本 gate 不主張 Phase67–71 已完成 SSOT 遷移**。  
Phase67–71 保留各自 private 實作是刻意設計（防止 regression），非缺陷。  
SSOT 模組是面向未來 phases 的 foundation，現有 phases 的歷史數字不受影響。

### 後續建議優先序

1. **Budget Guard 強化** (優先級最高) — 已由 Phase72 spec 確認
2. **LeagueAdapter** — 待後續排定
3. **Phase67–71 SSOT Refactor** — 低優先級，可作為治理任務獨立進行

---

## 十、相關檔案

| 檔案 | 說明 |
|---|---|
| `orchestrator/metrics_ssot.py` | SSOT 模組主體 (~620 lines) |
| `scripts/run_metrics_ssot_phase67_72_inventory.py` | Inventory 執行腳本 |
| `tests/test_metrics_ssot.py` | 93 個 unit tests |
| `reports/metrics_ssot_phase67_72_inventory_20260507.json` | 完整 JSON 清單報告 |
| `orchestrator/phase67_context_failure_attribution.py` | Phase67 (gate: OVERFIT_RISK) |
| `orchestrator/phase68_model_architecture_ensemble_failure_audit.py` | Phase68 |
| `orchestrator/phase69_calibration_objective_redesign_counterfactual.py` | Phase69 (gate: CALIBRATION_OBJECTIVE_NOT_PROMISING) |
| `orchestrator/phase70_strong_home_favorite_underconfidence_audit.py` | Phase70 (gate: MARKET_ONLY_SUPERIOR) |
| `orchestrator/phase71_market_dominance_model_derisk_audit.py` | Phase71 (gate: MARKET_DE_RISK_GUARD_PROMISING) |
| `orchestrator/phase72_market_derisk_guard_proposal.py` | Phase72 (gate: MARKET_DERISK_GUARD_SPEC_READY) |

---

`METRICS_SSOT_PHASE67_72_INVENTORY_VERIFIED`
