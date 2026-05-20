# 🚀 WBC Betting Pool: GitHub Migration & Telegram Integration Plan

本報告參考 [OpenClaw](https://github.com/openclaw/openclaw) 的架構設計，為本系統規劃 GitHub 託管與 Telegram 整合方案。

---

## 1. GitHub 託管與建置方案

### 1.1 儲存庫結構優化 (OpenClaw Style)
OpenClaw 採用清晰的模組化結構。建議本系統轉向以下 GitHub 友善架構：
- **`.github/workflows/`**: 實作 GitHub Actions，用於自動化測試 (pytest) 與資料更新腳本。
- **`docs/`**: 存放系統設計與回測研究報告（已建立）。
- **`data/`**: 僅存放權威快照 (Authoritative Snapshots)，大型歷史資料透過連結或外部儲存下載。
- **`requirements.txt`**: 嚴格定義相依套件，確保環境一致性。

### 1.2 GitHub Actions 自動化 (CI/CD)
- **Daily Data Sync**: 每天定時執行 `scripts/legacy_entrypoints/fetch_wbc_all_players.py` 與 `data/live_updater.py` 並 commit 更新。
- **Model Validation**: 每次 PR 自動執行 `tests/` 中的回測驗證，確保模型穩定性。
- **Auto-Report**: 比賽結束後自動執行覆盤腳本並產出 Markdown 報告。

---

## 2. Telegram 溝通整合 (The "Gateway" Approach)

參考 OpenClaw 的 **Channel/Gateway** 模型，我們不直接將 Telegram 邏輯寫死在模型中，而是建立一個輕量級的 **Telegram Gateway**。

### 2.1 核心架構
- **Gateway**: 建立一個獨立的 Python 程序（或整合進 `wbc_backend/api`），處理 Telegram Bot API 的 Webhook 或 Polling。
- **Shared Envelope**: 將賠率預測、資金警報等格式化後推送至 Telegram。
- **Command Routing**: 支援 `/predict`, `/ev`, `/portfolio` 等自定義指令。

### 2.2 安全性 (借鏡 OpenClaw)
- **Pairing**: 只有通過配對的個人身分才能操作 Bot。
- **Allowlist**: 嚴格限制可存取的群組或個人 ID。

---

## 3. 分階段執行路線圖

### 第一階段：基礎建設 (Done ✅)
- [x] 初始化本地 Git 儲存庫
- [x] 配置 `.gitignore` (排除大型 .pkl 模型與敏感資料)
- [x] 撰寫 OpenClaw 風格的 `README.md`
- [x] 建立 `LICENSE` (MIT)

### 第二階段：GitHub 移轉
1. 在 GitHub 建立 Private Repository。
2. 配置 Secret (如 API Keys)。
3. 設定 GitHub Actions 自動化管線。

### 第三階段：Telegram 整合開發
1. 註冊 Telegram Bot (@BotFather)。
2. 實作通知推送 API。
3. 建立互動式指令集。
