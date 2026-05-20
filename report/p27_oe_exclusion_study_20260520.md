# P27 OE Exclusion Study Report
**Date**: 2026-05-20  
**paper_only**: true | **diagnostic_only**: true

---

## 研究問題

P25 確認 OE（Odd/Even）為「PASS_BUT_NON_INFORMATIVE」市場：  
odds 幾乎不動，CLV ≈ 0，positive rate 僅 15.65%。  
本研究確認：**OE 是否只是稀釋 aggregate CLV？排除 OE 後是否能恢復統計顯著性？**

---

## Aggregate CLV 比較

| Aggregate | N | Mean% | CI_lo | CI_hi | CI∋0 | 說明 |
|-----------|---|-------|-------|-------|------|------|
| all_markets | 2,331 | +0.0340 | -0.0915 | +0.1614 | **Yes** | 全部 5 市場 |
| exclude_oe | 1,871 | +0.0403 | -0.1171 | +0.1966 | **Yes** | MNL+HDC+OU+TTO |
| hdc_ou_tto | 1,190 | +0.0377 | -0.1497 | +0.2323 | **Yes** | 不含 MNL、OE |
| mnl_only | 681 | +0.0449 | -0.2180 | +0.3083 | **Yes** | — |
| hdc_only | 402 | -0.0027 | -0.3240 | +0.3039 | **Yes** | — |
| ou_only | 418 | +0.0377 | -0.2607 | +0.3401 | **Yes** | — |
| tto_only | 370 | +0.0815 | -0.2974 | +0.4723 | **Yes** | 最高 mean，但 CI 最寬 |
| oe_only | 460 | +0.0083 | -0.0670 | +0.0826 | **Yes** | 結構性接近 0 |

---

## 三個核心問題解答

### Q1：OE 是否只是稀釋 aggregate CLV？

**答：YES（輕微稀釋）**

- All markets mean = +0.034%
- Exclude OE mean = +0.040%
- OE mean = +0.008%（顯著低於其他市場）
- OE positive rate = 15.65%（其他市場 30-38%）

OE 確實是稀釋因子，但影響極小（mean 差距只有 +0.006pp）。  
OE 的 CI 最窄（[-0.07, +0.09]），因其 odds 幾乎不動，實際上是在 aggregate 中增加「無訊號」雜訊。

---

### Q2：排除 OE 後 CI 是否仍穿越 0？

**答：YES，CI 仍穿越 0**

- Exclude OE CI = **[-0.1171, +0.1966]**（仍然穿越 0）
- All markets CI = [-0.0915, +0.1614]

矛盾地，排除 OE 後 CI **變寬**（因為 OE 本身貢獻了大量 N=460 筆接近 0 的穩定觀測，移除反而增加剩餘樣本的不穩定性）。

---

### Q3：是否存在任何 clean market 方向值得進入 model-quality repair？

**答：NO_INCONCLUSIVE**

- 最高 mean：TTO = +0.0815%，CI = [-0.31, +0.47]（CI 寬度 0.78pp，完全無法作為訊號）
- 最穩定：OE（CI 窄，但結構性無訊號）
- 沒有任何市場的 CI 下界 > 0

無任何市場達到即使是「weak-stable」程度的訊號強度。

---

### Q4：是否存在任何 market 應暫停評估？

| Market | 建議 |
|--------|------|
| OE | 建議從 aggregate CLV 分析中移除，作為獨立市場結構研究 |
| HDC | mean = -0.003%（唯一負值），CI 最寬，說明盤口線頻繁調整造成大量 skip，sample 較不穩定 |
| 所有市場 | 需要更多季度資料積累方能取得統計顯著 CLV 訊號 |

---

## OE 排除效果視覺化

```
All markets  : ████░░░░░░░░░░░░░░░░  CI=[-0.09, +0.16]  mean=+0.034%
Exclude OE   : ████░░░░░░░░░░░░░░░░  CI=[-0.12, +0.20]  mean=+0.040%  ← CI 變寬
HDC+OU+TTO   : ████░░░░░░░░░░░░░░░░  CI=[-0.15, +0.23]  mean=+0.038%
TTO only     : ████░░░░░░░░░░░░░░░░  CI=[-0.30, +0.47]  mean=+0.082%  ← 最高 mean，最不穩定
OE only      : ██░░░░░░░░░            CI=[-0.07, +0.08]  mean=+0.008%  ← 結構性 ≈ 0
```

---

## 結論

**OE Exclusion Sub-Classification**: `P27_OE_EXCLUSION_NO_SIGNAL_RECOVERY`

- OE 輕微稀釋 aggregate CLV（mean 差 +0.006pp）
- 排除 OE 後 CI **仍穿越 0**，且 CI 反而變寬
- 沒有任何 aggregate 組合能讓 CI 站上 0
- 目前樣本量（N=236 valid pairs）不足以支撐統計顯著的 CLV 訊號

**不作 profitability claim。不作 production proposal。**
