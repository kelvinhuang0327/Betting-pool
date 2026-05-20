# 2026 WBC 3/9 賽事檢討報告 (Post-Mortem Meeting)

## 賽事結果摘要

| 場次 | 對戰組合 | 預測勝率 (模型) | 預測比分 | 實際比分 | 預測結果 | 核心誤差 |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **B06** | 巴西 vs 墨西哥 | MEX 97.0% | 4.9-1.8 | **16-0** | ✅ 勝負正確 | 極端大比分與崩盤鏈低估 |
| **C09** | 南韓 vs 澳洲 | KOR 73.7% | 6.7-2.4 | **7-2** | ✅ 勝負正確 | 勝負抓對，但賽前報告資料來源失真 |

## 今日真正暴露的問題

### 1. C09 不是「模型猜錯」，而是「資料血緣斷裂」

- authoritative snapshot 在賽前已驗證 **Ju-Young Son vs Lachlan Wells**。
- 但 [`last_report.txt`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/latest/last_report.txt) 最終對外報告仍使用 **Koo Chang-Mo vs Jack O'Loughlin** 的 seed 組合。
- 這代表系統雖然有驗證層，卻沒有把 verified snapshot 強制覆蓋到最終報告輸出。
- 結論: 這次勝負方向抓對，不代表流程可信；同樣的管線失誤下次會直接造成錯單。

### 2. B06 暴露出「大比分崩盤鏈」仍嚴重低估

- [`data/wbc_backend/reports/postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl) 顯示，B06 的預測總分只有 **6.65**，實際總分 **16**，絕對誤差 **9.35**。
- 目前模型能抓住超強弱分布下的勝負方向，但仍把爆發型賽局壓回常態區。
- 這種錯誤在 WBC 很危險，因為國際賽牛棚深度差、守備失誤鏈、提早崩盤與 mercy-rule 邊界都比職業聯盟更常見。

### 3. `VERIFIED_WITH_FALLBACK` 仍然過於寬鬆

- B06 / C09 兩場都使用 previous-game lineup fallback。
- C09 還同時缺少 verified live odds，代表 market calibration 其實是跳過的。
- 目前系統把這種狀態當作「可預測但降 confidence」，實務上更合理的是:
  - 若先發或打序仍 fallback，禁止對外生成最終版下注報告。
  - 若 source 仍殘留 `MOCK/SEED`，直接標記 unsafe，不得產出公開推薦。

### 4. 今天之前系統沒有真正的賽後閉環

- 原本 repo 只有 [`prediction_registry.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/prediction_registry.jsonl) 記賽前快照。
- 今日已補上 [`postgame_learning.py`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/wbc_backend/reporting/postgame_learning.py)，並回填 B06 / C09 到 [`postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl)。
- 同步建立 [`retrainer_state.json`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/artifacts/retrainer_state.json)，開始累積 sub-model 的真實 Brier / logloss。

## 沒抓到的跡象與特徵

### A. 資料品質 / 來源一致性特徵

- `starter_identity_confidence`: seed 先發與 verified snapshot 是否一致
- `lineup_coverage_ratio`: 先發打序已確認比例
- `source_integrity_score`: authoritative / verified / fallback / mock 分級
- `odds_availability_flag`: 是否存在可驗證 live odds

### B. WBC 特有崩盤特徵

- `bullpen_cascade_fatigue`: 第一層中繼用完後的第二層實力斷崖
- `mismatch_blowout_propensity`: 強弱差 + 防守深度差 + 牛棚斷層的乘數效應
- `mercy_rule_hazard`: 7 局提前結束或大比分提前失控機率
- `defensive_collapse_threshold`: 分差擴大後的守備與保送放大機制

### C. 球員與打序層級特徵

- 真實打序左右打交互
- 當日先發捕手與配球穩定度
- 近兩場打序連續性與換位幅度
- bench depth / 代打品質差

### D. 非結構化與賽會脈絡特徵

- must-win / elimination pressure
- 前一戰牛棚高槓桿用量
- 當日新聞中的身體狀態、出賽限制、旅途疲勞
- 社群與媒體對先發異動的早期訊號

## 三位虛擬設計評審團結論

### 方法理論專家

「今天的主要問題不是分類器勝負率，而是 **資料可信度與分布尾端**。B06 再次證明標準 Poisson 對 WBC 大分差太保守；建議導入 **zero-inflated negative binomial / hurdle** 得分模型，並把 `VERIFIED_WITH_FALLBACK` 視為不確定性來源，直接反映到區間預測與 abstention。C09 則說明任何 calibration 都不能修補錯誤輸入，資料品質本身必須進入模型與 decision gate。」

### 技術務實專家

「最實際的改善順序很清楚:
1. verified snapshot 必須覆蓋 seed 輸出，不可只停在 warning。
2. 增加 `starter_identity_confidence`、`lineup_coverage_ratio`、`source_integrity_score` 三個硬特徵。
3. 對 B06 這類賽局加上 `bullpen_cascade_fatigue` 和 `mismatch_blowout_propensity`。
4. 自動學習只允許吃 authoritative result，不能吃人工猜測或 mock odds。」

### 程式架構專家

「今天最值得做的不是再加一個模型，而是補完整閉環。已落地的 [`postgame_learning.py`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/wbc_backend/reporting/postgame_learning.py) 是正確方向，但下一步要把它變成 scheduler job：
1. 賽後自動回寫結果。
2. 自動更新 retrainer state。
3. 自動生成 review report。
4. 只有當樣本數與健康度達標時，才允許調整 live ensemble 權重。」

## 自動學習機制的可行性判斷

### 立即可做

- 每場賽後回寫實際比分、Brier、logloss、score error
- 對 sub-model 做 online weight tracking
- 把 `winner_correct` 與 `score_error_total_abs` 作為兩條獨立監控線
- 對 `VERIFIED_WITH_FALLBACK` 樣本做單獨分桶評估

### 一週內可做

- 將 postgame registry 串入 scheduler
- 自動產出 `data_quality_bucket` 報表
- 針對 WBC / Premier12 / 奧運代理樣本做 feature ablation
- 用 auto feature lab 搜 2-way / 3-way interaction

### 暫時不要做

- 直接把今天 2 場結果拿去大幅改權重
- 在沒有更多真實樣本前，重押深度神經網路
- 用 mock/fallback 樣本驅動自動重訓

## 今日回填後的觀察值

- retrainer 目前只累積 **2 場**，樣本太少，**只可觀察不可部署**。
- 當前追蹤權重傾向:
  - `real_gbm_stack`: 23.84%
  - `neural_net`: 21.38%
  - `bayesian`: 17.77%
  - `poisson`: 16.08%
  - `elo`: 13.83%
  - `baseline`: 7.10%

## 後續優先順序

1. 把 verified snapshot 強制寫進最終報告，不再容忍 seed 漏出。
2. 把 `VERIFIED_WITH_FALLBACK` 從 soft warning 升級成 deploy gate。
3. 補 `bullpen_cascade_fatigue`、`mismatch_blowout_propensity`、`mercy_rule_hazard`。
4. 將 postgame result → retrainer → daily review 自動化。
5. 只在 authoritative sample 累積達門檻後，才開放自動調權。

## 外部驗證來源

- [MLB WBC 預告: Korea vs Australia](https://www.mlb.com/world-baseball-classic/news/korea-vs-australia-in-2026-world-baseball-classic)
- [MLB WBC 預告: Brazil vs Mexico](https://www.mlb.com/world-baseball-classic/news/brazil-vs-mexico-in-2026-world-baseball-classic)
- [Yonhap 韓媒賽果: 韓國 7 比 2 澳洲](https://www.yonhapnewstv.co.kr/news/MYH20260309208700641)
