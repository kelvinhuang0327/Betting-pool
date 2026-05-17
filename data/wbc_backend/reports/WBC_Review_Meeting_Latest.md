# WBC 檢討會議報告

日期: 2026-03-09
固定位置: `data/wbc_backend/reports/WBC_Review_Meeting_Latest.md`
歸檔位置: `archive/legacy_reports/wbc_backend_reports/review_archive/`

## 今日已完成回填賽果

- 墨西哥 16:0 巴西 (`B06`)
- 南韓 7:2 澳洲 (`C09`)

## 今日核心結論

1. 3/9 兩場勝負方向都抓對，但這不代表系統可直接信任。
2. **B06** 暴露出大比分崩盤鏈低估: 預測總分 6.65，實際總分 16。
3. **C09** 暴露出資料血緣問題: authoritative snapshot 已驗證 `Ju-Young Son / Lachlan Wells`，最終對外報告仍殘留 seed 版 `Koo Chang-Mo / Jack O'Loughlin`。
4. 今天之前 prediction registry 沒有賽後結果回寫，無法形成真正自動學習閉環。

## 三位虛擬評審團結論

### 方法理論專家

- 要先修補 uncertainty 與肥尾分布，再談增加模型複雜度。
- B06 類型需要 zero-inflated / hurdle / heavy-tail 得分模型；C09 類型需要把資料可信度變成模型與 gate 的一級訊號。

### 技術務實專家

- `VERIFIED_WITH_FALLBACK` 不應只是 warning，應升級成 deploy gate。
- 立即補上 `starter_identity_confidence`、`lineup_coverage_ratio`、`bullpen_cascade_fatigue`、`mismatch_blowout_propensity`。

### 程式架構專家

- 優先順序不是再加模型，而是補完整閉環。
- 已新增 [`postgame_learning.py`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/wbc_backend/reporting/postgame_learning.py) 並回填 [`postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl)，後續要排入 scheduler 自動化。

## 今日已落地

- 3/9 賽後回寫檔: [`postgame_results.jsonl`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/reports/postgame_results.jsonl)
- 線上學習狀態檔: [`retrainer_state.json`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/data/wbc_backend/artifacts/retrainer_state.json)
- 詳細賽後檢討: [`3_9_postmortem.md`](/Users/kelvin/Kelvin-WorkSpace/Betting-pool/docs/reports/postmortem/3_9_postmortem.md)

## 回填後觀察

- 目前 retrainer 僅有 **2 場**樣本，權重只可觀察不可部署。
- 暫時權重排序:
  - `real_gbm_stack` 23.84%
  - `neural_net` 21.38%
  - `bayesian` 17.77%
  - `poisson` 16.08%
  - `elo` 13.83%
  - `baseline` 7.10%

## 後續優先項

1. verified snapshot 強制覆蓋最終報告輸出
2. `VERIFIED_WITH_FALLBACK` 升級成 deploy gate
3. 大比分崩盤特徵與 mercy-rule hazard 納入建模
4. postgame result → retrainer → daily review 全自動化
