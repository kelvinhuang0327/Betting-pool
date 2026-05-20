# P24 Market-Level CLV Robustness Report

**Phase**: P24 — Per-Market CLV Robustness  
**Date**: 2026-05-20  
**Tags**: `paper_only=true` | `diagnostic_only=true` | `no_production_proposal`

---

## 五市場診斷摘要

| Market | N | Mean CLV | Median | Std | Pos Rate | CI 95% Lo | CI 95% Hi | 穿越零 | 分類 |
|--------|---|----------|--------|-----|----------|-----------|-----------|--------|------|
| HDC | 458 | +1.4704% | 0.0% | 19.35% | 40.17% | −0.20% | +3.30% | **是** | INCONCLUSIVE |
| TTO | 434 | +0.2546% | 0.0% | 6.87% | 40.78% | −0.38% | +0.91% | **是** | INCONCLUSIVE |
| OU | 460 | +0.1180% | 0.0% | 5.07% | 38.91% | −0.36% | +0.59% | **是** | INCONCLUSIVE |
| OE | 460 | +0.0083% | 0.0% | 0.84% | 15.65% | −0.07% | +0.09% | **是** | INCONCLUSIVE |
| MNL | 472 | −0.0314% | 0.0% | 3.77% | 45.34% | −0.37% | +0.30% | **是** | INCONCLUSIVE |

**全體 5 市場均為 INCONCLUSIVE**

---

## 個別市場分析

### HDC (讓分)
- **Mean**: +1.47% — 名義上最高，但標準差高達 19.35%
- **極端值**: max = +158.33%, min = −62.15%（單一極端觀測可能主導均值）
- **Top-5 outlier dominance**: 17.31% — 前 5 個絕對值觀測佔總 CLV 變異的 17%
- **判定**: INCONCLUSIVE — outlier-dominated，廣 CI 確認無穩健正邊緣

### MNL (獨贏)
- **Mean**: −0.03% — 唯一負均值市場
- **對稱性**: pos=neg=214，完美對稱
- **標準差**: 3.77% — 最窄（排除 OE）
- **判定**: INCONCLUSIVE — 近零均值，pos/neg 完全平衡，無訊號

### OU (大小分)
- **Mean**: +0.12%
- **對稱性**: pos=179 vs neg=178 — 幾乎完全對稱
- **CI**: [−0.36%, +0.59%] 穿越零
- **判定**: INCONCLUSIVE

### OE (單雙)
- **Mean**: +0.008% — 幾乎為零
- **中性率**: 68.7% (316/460) — 賠率幾乎不動
- **標準差**: 0.84% — 極低；OE 市場基本沒有流動性
- **判定**: INCONCLUSIVE — 無資訊內容，非有效市場

### TTO (前五局)
- **Mean**: +0.25%
- **對稱性**: pos=neg=177 — 完全對稱
- **CI**: [−0.38%, +0.91%] 穿越零
- **Positive rate**: 40.78% — 略高於 HDC，值得長期追蹤
- **判定**: INCONCLUSIVE（可觀察，但不可行動）

---

## 市場排名 (by 名義均值)

```
1. HDC:  +1.4704%  →  INCONCLUSIVE (outlier-dominated)
2. TTO:  +0.2546%  →  INCONCLUSIVE
3. OU:   +0.1180%  →  INCONCLUSIVE
4. OE:   +0.0083%  →  INCONCLUSIVE
5. MNL:  −0.0314%  →  INCONCLUSIVE
```

---

## 跨市場一致性

所有市場的中位數均為 0.0%。這表明在大多數賽事中，賠率從 pregame 到 closing 並無實質移動。CLV 訊號（無論正負）主要由少數賽事的大幅賠率變動產生，這與 WBC 賽事的有限流動性一致。

---

> 本報告為純學術診斷，不構成任何市場參與建議。`fixed_edge_5pct` champion 維持不變。
