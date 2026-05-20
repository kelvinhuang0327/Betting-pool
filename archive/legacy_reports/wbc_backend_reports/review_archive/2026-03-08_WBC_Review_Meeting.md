# WBC 檢討會議報告

日期: 2026-03-08
固定位置: `data/wbc_backend/reports/WBC_Review_Meeting_Latest.md`
歸檔位置: `data/wbc_backend/reports/review_archive/`

## 今日白天賽果

- 加拿大 8:2 哥倫比亞
- 荷蘭 4:3 尼加拉瓜
- 義大利 8:0 巴西
- 波多黎各 4:3 巴拿馬
- 委內瑞拉 11:3 以色列
- 美國 9:1 英國
- 台灣 5:4 南韓
- 澳洲 vs 日本: 夜場，另行補充

## 核心結論

1. 問題主因不是單一模型錯誤，而是資料驗證、模型部署、回測校準沒有形成強制閉環。
2. 先發投手驗證門檻已補上，但 live inference 直到今日仍暴露出 artifact schema 與 feature count 不一致風險。
3. 現有系統能做方向判讀，但不等於已具備穩定可下注能力；校準、過擬合抑制、賽後自動學習仍需補強。

## 三位虛擬評審團結論

### 方法理論專家

- 先補 uncertainty 與 calibration，再談增加模型複雜度。
- WBC 小樣本要靠跨屆 shrinkage、walk-forward、conformal/區間信心控風險。

### 技術務實專家

- 最優先是版本一致性: feature schema、artifact、walk-forward、calibration 必須同版。
- 沒有通過 deployment gate，一律不准 live 預測。

### 程式架構專家

- 必須建立 prediction registry，逐場落地賽前快照、預測、決策、賽後結果。
- 優先順序: deployment gate > prediction registry > calibration loop > feature expansion。

## 已啟動優化項目

- 新增 deployment gate
- 新增 prediction registry
- 模型 artifact schema 驗證
- 重訓 32-feature artifact

## 後續優先項

1. prediction registry 串上賽後結果回寫
2. walk-forward / calibration 作為 deploy gate
3. lineup-level / leverage bullpen / elimination pressure 特徵
4. meta-learning 僅在校準合格時允許更新權重
