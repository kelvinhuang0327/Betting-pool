# P202G-A — MLB 來源政策澄清證據包 (Source Policy Clarification Evidence Packet)

> 本報告為 **evidence collection，不是法律意見 (not legal advice)**。所有法律性結論一律以
> 「專案風險決策 (project risk decision)」的形式陳述，而非法律建議。每一條非顯而易見的政策
> 主張都附官方引用，或明確標記 `UNKNOWN`。

## Report Metadata

| 欄位 | 值 |
|---|---|
| `generated_at_utc` | `2026-06-13T14:31:52Z` |
| 報告檔名日期 | `20260614`（依任務指定檔名；實際產製為 2026-06-13 Asia/Taipei / UTC 同日） |
| `accessed_at` range | 約 `2026-06-13T14:24Z` – `2026-06-13T14:32Z`（Asia/Taipei 22:24–22:32） |
| `repository` | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` |
| `branch` | `main` |
| `HEAD` | `cac2a748dff5077dd3b947fbacdc01dbdeec5607` |
| `task ID` | `P202G-A` |
| Task Type | `READ_ONLY_POLICY_EVIDENCE` |
| P202F classification | `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED` |
| live transport status | **HOLD** |
| official source URLs accessed | 9 個不同 URL，橫跨 4 個官方網域（新增 `docs.statsapi.mlb.com/openapi.json` identity 文件） |
| official sources with usable content (evidence) | 4（O1 Terms、O2 www robots、O3 registration、O8 openapi identity；O5 statsapi robots 為 404 存取結果） |
| official sources access-failed (記為存取結果，非證據內容) | 5（O4 docs HTML×2、O6 legal-notices、O7 tac、O5 robots 404） |
| **non-official source count used as evidence** | **0** |
| MLB data endpoint call count | **0** |
| `corrected_at_utc` | `2026-06-13T14:58:57Z`（P202G-A-FIX 窄修） |
| `correction_reason` | 依獨立複審修正 2 處報告層級瑕疵：① §1「are subject to this Agreement」**範圍條款**原被誤標為「MLB Digital Properties 的定義」並截斷操作性結尾；② `legaldepartment@mlb.com`（官方 **DMCA Copyright Agent**）原被誇大為 licensing/permission 管道。**決策、限制分類與 HOLD 均不變。** |
| `independent_review_reference` | `report/p202g_a_source_policy_clarification_independent_review_20260614.md`（`P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`） |
| `applicability evidence level` | **`STRONGLY_SUPPORTED_INFERENCE`**（Terms 未逐字點名 `statsapi.mlb.com`） |
| `contact-path evidence level` | 無用途相符之正式 data/API licensing 管道（**`NOT_ESTABLISHED`**）；僅帳號註冊入口 + DMCA/一般法律 fallback |

---

## 1. Executive Summary（執行摘要）

本輪僅依官方且官方控制的人類可讀政策／條款／robots 與註冊頁面，重新獨立蒐證，回答
「目前是否存在足以授權本 Betting 專案對 MLB 資料進行自動化存取、保存與衍生使用的明確
書面證據」。

> **📝 修正註記（P202G-A-FIX，2026-06-13）**：本檔依獨立複審
> （`..._independent_review_20260614.md`）作 2 處報告層級窄修——更正 §1 範圍條款的歸屬
> （原誤標為「MLB Digital Properties 定義」）與聯絡管道分類（`legaldepartment@mlb.com` 實為
> DMCA Copyright Agent）。**最終限制分類、所有決策與 live HOLD 均維持不變。** 下文凡標
> 「（prior incorrect wording）」者為原措辭之更正說明。

**核心結論：找到一條官方明文的自動化存取限制（explicit）；其適用於本專案擬使用之 `statsapi.mlb.com` 屬「強支撐的保守推論 (STRONGLY_SUPPORTED_INFERENCE)」，足以維持 HOLD（Terms 未逐字點名該 host）。**

1. 本輪自官方 **MLB.com Terms of Use**（標題 "Terms of Use Agreement"，Last Updated
   **2025-03-11**）獨立查得明文禁止：
   > "use automated scripts to collect information from or otherwise interact with the MLB Digital Properties"

2. 同一份 Terms 亦明文要求「複製、製作衍生著作、散布、展示」須先取得書面許可：
   > "reproduce, prepare derivative works based upon, distribute, perform or display the MLB Digital Properties without first obtaining written permission"

3. **範圍適用性（強支撐推論；更新 P202F 第 1 個未決問題）**：Terms §1 之下列文字為
   **範圍/受拘束條款**（**非** "MLB Digital Properties" 的正式定義；prior incorrect wording
   曾誤標為「定義」並截掉操作性結尾）：
   > "...by MLB Advanced Media, L.P. ('MLB') are subject to this Agreement"

   正式定義為**另一句**（涵蓋 "...other MLB-controlled products or services or MLB-operated
   interactive media locations..."）。官方 OpenAPI 文件（`docs.statsapi.mlb.com/openapi.json`）
   直接載明 `statsapi.mlb.com` 為 *"Official API for Major League Baseball."* 之 Production
   server。據此，把 automated-scripts 限制套用於 StatsAPI 屬**強支撐的保守專案風險推論
   (STRONGLY_SUPPORTED_INFERENCE)**，**足以維持 HOLD**；但 **Terms 並未逐字點名
   `statsapi.mlb.com`**，故不主張「直接明文點名」。官方 API 身分**不**等於已取得自動化使用授權。

4. 找到一條**具體、官方的存取申請／聯絡管道**（StatsAPI 自助註冊工具 + MLBAM Copyright
   Agent `legaldepartment@mlb.com` + 註冊支援 `registrationsupport@mlb.com`），但該管道
   **未陳述任何公開資格 (eligibility NOT FOUND)**，且在頁面上**重申**無書面許可不得複製／
   衍生／散布。因此這是「可申請的管道」，**不代表本專案用途已獲授權**。

5. 因此，依現有官方書面證據，**無法自我授權**任何 live 呼叫——即使是「單次 (one-shot)
   診斷 GET」亦不可。Live transport（P202G）**維持 HOLD**。最保守且符合證據的技術邊界仍是
   **fixture-only**。

**Final Classification：`P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`**

---

## 2. Scope and Explicit Non-Actions（範圍與明確未執行動作）

本任務為唯讀政策證據蒐集。以下動作**全數未執行**：

- ❌ 未呼叫任何 MLB 資料 endpoint：schedule / game / player / boxscore / stats / roster /
  probablePitcher / 任何 live data。`statsapi.mlb.com/api/...` 一次都未觸及。
- ❌ 未試探 undocumented API、未做 endpoint enumeration。
- ❌ 未實作 transport / collector / acquisition script；未產生 fixture；未做 real historical backfill。
- ❌ 未寫入任何 runtime data / DB / log payload / production / registry。
- ❌ 未修改任何 source / test / config / fixture。
- ❌ 未修改、stage 或提交四個治理檔；未做任何 git add / branch / checkout / commit / push /
  PR / merge / rebase / reset / stash / clean / delete。
- ❌ 未送出任何 email、contact form 或註冊申請（僅閱讀註冊頁 HTML）。
- ❌ 未登入、未取得 token / API key、未接受任何新契約。
- ❌ 未繞過任何網站存取限制；未使用 rotating UA / proxy / 低頻規避手法。

**唯一寫入檔案**：`report/p202g_a_source_policy_clarification_evidence_packet_20260614.md`（本檔）。

存取範圍僅限官方或官方控制之政策／條款／法律／developer／contact／robots 頁面，以及
官方網路搜尋以尋找上述官方來源。

---

## 3. Governance and Phase 0（治理與 Phase 0）

### 3.1 Governance Priority 與讀取狀態

依任務 Governance Priority：本 prompt 的唯讀政策證據任務與單一報告 whitelist 為最高優先，
其次 `active_task.md` → `CURRENT_STATE.md` → `SHARED_AGENT_BOOTSTRAP.md` → `TASK_TEMPLATES.md`。

- `00-Plan/roadmap/active_task.md`：**READ**。確認 Active Task = **P202G-A Source Policy
  Clarification Evidence Packet**，Status `AUTHORIZED_READ_ONLY_AUDIT`，Task Type
  `READ_ONLY_POLICY_EVIDENCE`，背景載明 P202F 分類與 live transport HOLD。與本 prompt 一致，
  **無治理衝突**。
- `agent_bootstrap/`（SHARED_AGENT_BOOTSTRAP.md / TASK_TEMPLATES.md / CURRENT_STATE.md）與
  `roadmap.md` / `CTO-Analysis.md`：列於 Phase 0 dirty/untracked 既知清單；本輪以唯讀對待，
  **未修改**。其陳舊性不構成衝突（本 prompt 優先）。

> 註：`active_task.md` 內列的 Final Classification 候選集（`..._EVIDENCE_COMPLETE/PARTIAL/...`）
> 與本 prompt 的候選集不同。依 Governance Priority #1，本報告採用 **本 prompt 指定的**
> Final Classification 候選集。此差異已記錄，非阻斷。

### 3.2 Phase 0 — Actual State Verification 結果

| Check | Observed | Result |
|---|---|---|
| `pwd` / git toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | PASS |
| `git branch --show-current` | `main` | PASS |
| `git symbolic-ref -q --short HEAD` | `main`（非 detached） | PASS |
| `git rev-parse --git-dir` | `.git` | PASS |
| local HEAD | `cac2a748dff5077dd3b947fbacdc01dbdeec5607` | PASS |
| `origin/main` | `cac2a748dff5077dd3b947fbacdc01dbdeec5607` | PASS |
| local HEAD == origin/main == Expected HEAD | 三者相等 | PASS |
| `gh pr list --state open` | 空（0） | PASS |
| staged files (`git diff --cached --name-only`) | 空（0） | PASS |
| `.venv/bin/python --version` | `Python 3.13.8`（≥ 3.11） | PASS |
| P202F 報告存在 | `report/p202f_..._20260613.md` 在 untracked 清單 | PASS |
| P202G-B 七檔 tracked | source+test+fixture+4 reports 皆 `git ls-files` 命中 | PASS |
| active_task = P202G-A read-only policy | 是 | PASS |
| no pitcher-event runtime data path | `data/mlb_pitcher_game_events/`（資料目錄）不存在；僅 `.py` 模組 | PASS |
| no probable-starter runtime data path | `data/mlb_probable_starters/` 等資料目錄不存在 | PASS |
| dirty tree = 既知治理/bootstrap/tolerated runtime/既有排除報告 | 與上一輪回報完全一致 | PASS |

**Phase 0 = PASS。** 無 STOP condition 觸發。

#### Dirty Inventory（Phase 0 實測完整清單）

Tracked-modified（13）：
- 治理（3）：`00-Plan/roadmap/CTO-Analysis.md`、`00-Plan/roadmap/active_task.md`、`00-Plan/roadmap/roadmap.md`
- tolerated runtime/data（10）：`data/.live_cache/tsl_dedup_state.json`、`data/derived/tsl_market_availability_state.json`、`data/mlb_context/external_closing_state.json`、`data/mlb_context/odds_capture_schedule.json`、`data/mlb_context/odds_timeline.jsonl`、`data/tsl_fetch_status.json`、`data/tsl_odds_history.jsonl`、`data/tsl_odds_snapshot.json`、`logs/daemon_heartbeat.jsonl`、`runtime/agent_orchestrator/training_memory.json`

Untracked：
- bootstrap（治理第 4 檔含於此）：`00-Plan/roadmap/agent_bootstrap/`（`CURRENT_STATE.md`、`SHARED_AGENT_BOOTSTRAP.md`、`TASK_TEMPLATES.md`）
- 既有排除報告（5）：`report/p199_..._20260611.md`、`report/p202_..._20260612.md`、`report/p202b_..._20260612.md`、`report/p202c_..._20260612.md`、`report/p202f_..._20260613.md`

四個治理檔（`roadmap.md`、`CTO-Analysis.md`、`active_task.md`、`agent_bootstrap/CURRENT_STATE.md`）為上一輪已授權修改，本輪保持原狀、未觸碰。狀態與上一輪回報一致，**不因此 STOP**。

---

## 4. Prior P202F Unresolved Questions（P202F 未決問題的對賬）

依任務要求，分開記錄 P202F 的事實／推論／未取得證據，並標明本輪重新驗證結果。
**未直接複製 P202F 結論作為新證據**；本輪每一關鍵結論皆有本輪官方來源或標 `UNKNOWN`。

### 4.1 P202F 已證實的事實（其報告層級）
- 技術 endpoint 身分：`statsapi.mlb.com` / `GET /api/v1/schedule` / `hydrate=probablePitcher`。
- 來源所有權：MLB / MLBAM 官方網域與文件。
- （P202F 由 docs 頁取得）public schedules 無需憑證、25 req/s rate limit、"public use 尚未受支援"。
- （P202F 由 Terms 取得）一般 Terms 禁 automated scripts；複製／衍生／散布須書面許可。
- `www.mlb.com` robots disallow `/api/`；`docs.statsapi.mlb.com/robots.txt` 為 404。

### 4.2 P202F 的合理推論（本輪不採為新證據）
- 「technical design 已足以設計 one-shot」屬實作就緒判斷，非授權證據。
- 「是否可主張單次非商業診斷 GET 為允許」P202F 列為未決——本輪**明確不採此推論為許可**。

### 4.3 P202F 未取得的證據（仍待官方書面澄清）
- 一般 Terms 是否原封不動適用於 `statsapi.mlb.com`（P202F 列為 Unknown #1）。
- 單次非商業診斷 GET 是否被允許（#2）。
- 本專案是否符合 club/vendor/developer 帳號類別（#3）。
- attribution 文字（#4）、normalized 保存（#5）、fingerprint 保存（#6）、衍生資料
  redistribution／betting 研究使用（#7）、`hydrate=probablePitcher` 是否官方支援（#8）。

### 4.4 本輪重新從官方來源驗證之結果
| P202F 項目 | 本輪獨立驗證 | 結果 |
|---|---|---|
| Terms 禁 automated scripts | 重新擷取 Terms（2025-03-11）取得 verbatim | **RE-VERIFIED（O1）** |
| 複製/衍生/散布須書面許可 | 同上 verbatim | **RE-VERIFIED（O1）** |
| 私人非商業使用例外 | 同上 verbatim | **RE-VERIFIED（O1）** |
| 一般 Terms 是否適用 statsapi（#1） | §1「are subject to this Agreement」**範圍條款（非定義）** ＋正式定義（"MLB-controlled products or services..."）＋ O8 openapi「Official API for MLB」server=statsapi | **STRONGLY_SUPPORTED_INFERENCE（足以 HOLD；Terms 未逐字點名 statsapi）** |
| 官方聯絡管道身分 | `legaldepartment@mlb.com` 經查為 §2 **DMCA Copyright Agent**（非 data/API licensing office） | **RE-VERIFIED（O1）；用途相符 licensing 管道 NOT_ESTABLISHED** |
| StatsAPI 申請管道 | 取得 StatsAPI 自助註冊工具 + `registrationsupport@mlb.com`（技術註冊支援） | **新證據（O3）；非 usage authorization** |
| `www.mlb.com` robots disallow `/api/` | 重新擷取 robots.txt verbatim | **RE-VERIFIED（O2）** |
| target host robots | 擷取 `statsapi.mlb.com/robots.txt` → 404 | **新證據（O5）：目標 host 無 robots 政策** |
| `statsapi` 官方身分 | 擷取 `openapi.json`：描述 "Official API for Major League Baseball."、server=`statsapi.mlb.com` | **新證據（O8）：官方 MLB API 身分確立** |
| docs「public use 不受支援」 | docs HTML 子網域 JS-rendered，body 空 | **本輪 UNKNOWN（未能獨立擷取）** |
| docs「no-auth public schedules」 | 同上 | **本輪 UNKNOWN** |
| docs 25 req/s rate limit | 同上 | **本輪 UNKNOWN** |
| legal-notices 商標聲明 | HTTP 406（兩次） | **本輪 UNKNOWN** |
| `hydrate=probablePitcher` 是否官方支援 | O8 openapi 僅取 info/servers identity，未列舉 path token | **本輪 NOT ADDRESSED（屬 P202F 技術問題）** |

---

## 5. Official Source Inventory（官方來源清單）

僅列官方或官方控制之來源。非官方來源（部落格、Stack Overflow、Reddit、非官方 StatsAPI
文件、套件 README）一律**不**列入，亦**未**作為政策證據（evidence count = 0）。

### O1 — MLB.com Terms of Use ✅（核心政策，本輪可擷取）
- **URL**：`https://www.mlb.com/official-information/terms-of-use`
- **Domain**：`www.mlb.com`
- **Title**：Terms of Use Agreement
- **Issuing entity**：Major League Baseball / MLB Advanced Media, L.P.
- **Last Updated**：2025-03-11
- **Accessed**：2026-06-13（約 14:24Z 與 14:30Z 兩次擷取，內容一致）
- **Document type**：人類可讀條款（Terms of Use）
- **Evidence strength**：**EXPLICIT** ｜ **Confidence**：**HIGH**

### O2 — www.mlb.com robots.txt ✅
- **URL**：`https://www.mlb.com/robots.txt`
- **Domain**：`www.mlb.com`
- **Title**：robots.txt
- **Issuing entity**：MLB / MLBAM
- **Accessed**：2026-06-13（約 14:26Z）
- **Document type**：robots 指令檔
- **Evidence strength**：**EXPLICIT（僅就 www.mlb.com host）** ｜ **Confidence**：**HIGH**
- ⚠️ robots ALLOW/DISALLOW **不等於** contractual authorization（詳 §7）。

### O3 — MLB Self Registration Utility（StatsAPI group）✅
- **URL**：`https://inside.mlb.com/UserRegistrationForm/?GROUP=StatsAPI`
- **Domain**：`inside.mlb.com`（MLB 營運之註冊基礎設施）
- **Title**：Major League Baseball Self Registration Utility
- **Issuing entity**：Major League Baseball
- **Accessed**：2026-06-13（約 14:29Z）
- **Document type**：存取申請（self-registration）頁面
- **Evidence strength**：**EXPLICIT（管道存在）／SILENT（資格／用途）** ｜ **Confidence**：**MEDIUM**

### O4 — docs.statsapi.mlb.com（getting-started: authentication-authorization、rate-limiting）⚠️ 本輪不可擷取
- **URL**：`https://docs.statsapi.mlb.com/getting-started/authentication-authorization`、`.../rate-limiting`
- **Domain**：`docs.statsapi.mlb.com`
- **Accessed result**：`PAGE_BODY_EMPTY`（子網域為 JS-rendered，無 JS 執行環境下 body 為空）
- **本輪判定**：無法獨立取得內容 → 相關發現標 **UNKNOWN**（不沿用 P202F 引文作為本輪證據）。

### O5 — statsapi.mlb.com robots.txt ✅（存取結果）
- **URL**：`https://statsapi.mlb.com/robots.txt`
- **Accessed result**：**HTTP 404**（目標 host 未發布 robots 政策）
- **Evidence strength**：**EXPLICIT（存取結果）** ｜ **Confidence**：**HIGH**

### O6 — www.mlb.com Legal Notices ⚠️ 本輪不可擷取
- **URL**：`https://www.mlb.com/official-information/legal-notices`
- **Accessed result**：**HTTP 406 Not Acceptable**（兩次；邊緣內容協商）→ 商標／著作權專頁本輪 **UNKNOWN**。

### O7 — www.mlb.com/tac（Terms & Conditions）⚠️ 本輪不可擷取
- **URL**：`https://www.mlb.com/tac`
- **Accessed result**：**HTTP 406 Not Acceptable** → 本輪 **UNKNOWN**。

### O8 — docs.statsapi.mlb.com OpenAPI document ✅（官方 API 身分，P202G-A-FIX 新增）
- **URL**：`https://docs.statsapi.mlb.com/openapi.json`
- **Domain**：`docs.statsapi.mlb.com`（官方文件子網域之靜態 JSON spec，非資料 endpoint）
- **Title / 類型**：OpenAPI/Swagger spec — `info.title` "Stats API Documentation" v2.0.0
- **Issuing entity**：Major League Baseball
- **Accessed**：2026-06-13（約 14:45Z；P202G-A-FIX 複審輪擷取）
- **關鍵內容**：`info.description` = *"Official API for Major League Baseball."*；`servers[]` 含
  `https://statsapi.mlb.com (Production)`；`info.contact/license/termsOfService` = absent。
- **用途**：確立 `statsapi.mlb.com` 之**官方 MLB API 身分**（支撐範圍適用性之強推論）。
  ⚠️ 官方身分**不**等於自動化使用授權。
- **Evidence strength**：**EXPLICIT（身分）** ｜ **Confidence**：**HIGH**

> 來源探查過程中，網路搜尋另列出若干官方 URL（如 `support.mlb.com/s/contact-us`、
> footage/photo licensing 信箱、copy/photo license 電話）。這些僅來自**搜尋摘要**而非實際
> 擷取之官方頁面，依任務規則**不列為證據**，僅作為未來尋找官方頁面的線索。

---

## 6. Automated Access Evidence（自動化存取證據）

針對 automated access / automated means / scraping / crawling / spider / robot / bot /
data mining / bulk access / systematic download / API / developer / license / commercial use /
derivative / reproduce / redistribute / archive / retain / store / cache 等詞，於官方主站 Terms、
robots、註冊頁進行檢查（docs 子網域與 legal-notices 本輪不可擷取）。

| 項目 | 官方明文（verbatim，≤25 words） | 來源 | 判定 |
|---|---|---|---|
| automated scripts | "use automated scripts to collect information from or otherwise interact with the MLB Digital Properties" | O1 | **EXPLICITLY PROHIBITED** |
| 複製／衍生／散布／展示 | "reproduce, prepare derivative works based upon, distribute, perform or display the MLB Digital Properties without first obtaining written permission" | O1 | **須書面許可** |
| 私人非商業使用例外 | "downloading one copy of the MLB Digital Properties on any single device for your personal, non-commercial home use" | O1 | 例外狹窄（單份／個人／非商業／home use） |
| 非商業限定 + 禁衍生 | "...are provided for your private, non-commercial use, and you may not distribute, modify, translate, rebroadcast, transmit, stream, perform or create derivative works" | O1 | **EXPLICIT 限制** |
| API / StatsAPI / developer 字樣 | （Terms 文內）**NOT FOUND** | O1 | Terms 未列 API 專屬例外 |
| robots `/api/`（www host） | `Disallow: /api/`（User-agent: `*`） | O2 | 僅就 `www.mlb.com`；非契約授權 |
| 註冊頁重申限制 | "Materials must not be reproduced, prepare derivative works based upon, distribute, perform or display without written permission" | O3 | 申請管道亦帶相同限制 |

**範圍適用性（`STRONGLY_SUPPORTED_INFERENCE`；prior incorrect wording 曾標「決定性／直接適用」並把下列範圍條款誤標為「定義」）**：

- Terms §1 **範圍/受拘束條款**（verbatim；**非**正式定義）：
  > "...by MLB Advanced Media, L.P. ('MLB') are subject to this Agreement"
- Terms **正式定義**（另一句，verbatim）：
  > "...other MLB-controlled products or services or MLB-operated interactive media locations...referred to herein collectively as the 'MLB Digital Properties'"
- 拘束力（verbatim）：
  > "By using an MLB Digital Property, you agree to be bound by this Agreement."
- 官方身分（O8 openapi，verbatim）：
  > "Official API for Major League Baseball."（server = `statsapi.mlb.com`）

**推論鏈（direct fact 與 inference 清楚分離）**：(1) 官方 Terms §1 將 MLBAM 提供/散布之產品
服務（"whether via this Website or elsewhere"）納入「受本協議拘束」，正式定義另涵蓋
"MLB-controlled products or services"（皆 DIRECT_OFFICIAL_TEXT）；(2) 官方 OpenAPI 證明
`statsapi.mlb.com` 為 official MLB API（DIRECT_OFFICIAL_TEXT）；(3) 故把 automated-scripts
限制套用於 StatsAPI 屬**強支撐之保守專案風險推論**；(4) 此**足以維持 HOLD**；(5) 但 **Terms
並未逐字點名該 hostname**（非 DIRECTLY_NAMED）。官方 API 身分**不得**推論為已取得自動化
使用授權；技術公開／no-auth／robots 沉默亦**不得**改寫為許可。

> Terms 另載：`"In some instances, this Agreement and separate terms (e.g., an end user license agreement) will apply to the MLB Digital Properties."`
> 即縱有 StatsAPI 專屬條款，一般 Agreement 仍同時適用；而本輪查得之 StatsAPI 註冊頁
> （O3）亦重申相同的無書面許可即禁複製／衍生／散布限制。兩條路徑皆指向「須書面許可」。

**沉默處理**：docs 子網域所述「public use 不受支援」「public schedules 無需 auth」「25 req/s」
本輪不可擷取 → 標 **SILENT/UNKNOWN（本輪）**，且即便存在，亦**不得**將「技術上公開、無需
憑證、rate limit 存在、robots 未禁」任一者改寫為授權。

---

## 7. Robots.txt Evidence and Limitations（robots 證據與限制）

| host | robots 結果 | 與目標來源關係 |
|---|---|---|
| `www.mlb.com` | `User-agent: *`；`Disallow: /api/`（另含 `/test/`、`/app/`、`/embed/`、`/en/`、`/mlb/`、`/search` 及球隊 search 路徑）；無 Crawl-delay；列數個 Sitemap | **不同 host**：此 `/api/` 規則治理 `www.mlb.com/api/`，**非** `statsapi.mlb.com/api/...` |
| `statsapi.mlb.com` | **HTTP 404**（無 robots.txt） | **目標 host 未發布任何 robots 政策**（既無 ALLOW 亦無 DISALLOW） |
| `docs.statsapi.mlb.com` | （P202F 曾記 404；本輪未重取） | 文件子網域 |

**限制與明確註記**：
- robots.txt **不等於**授權合約。即使某路徑為 robots ALLOW，亦**不得**據此主張取得自動化
  使用之契約授權。
- 目標 host `statsapi.mlb.com` 無 robots 政策（404）→ robots 對目標來源**沉默**；沉默
  **不得**解讀為許可。
- `www.mlb.com` 的 `Disallow: /api/` 是針對另一 host，雖在態度上對自動化抓取 `/api/` 路徑
  顯示不歡迎，但其法律拘束力仍以 Terms 為準，非以 robots 為準。

---

## 8. Authentication and Rate-Limit Evidence（驗證與速率限制證據）

| 項目 | 本輪官方證據 | 判定 |
|---|---|---|
| Authentication / API key | docs 子網域不可擷取；Terms 未述 API 驗證細節 | **本輪 UNKNOWN**（不沿用 P202F docs 引文為本輪證據） |
| 受保護資料憑證類別 | O3 StatsAPI 自助註冊工具存在（Okta 類登入路徑於搜尋中出現） | 存在憑證式存取，但資格／用途未明 |
| Rate limit（25 req/s 等） | docs `rate-limiting` 頁 `PAGE_BODY_EMPTY` | **本輪 NOT_ESTABLISHED** |
| Burst / 429 | 同上 | **本輪 NOT_ESTABLISHED** |
| User-Agent 要求 | 官方無明文要求格式（本輪未見） | **NOT_STATED** |

**重要原則**：
- **no-auth endpoint 不得寫成 permission**。技術上無需憑證 ≠ 取得自動化使用授權。
- **rate limit 技術存在不得寫成合法授權**。速率上限是技術防護，不構成存取契約。
- 本輪無法獨立確證 25 req/s，故 Decision Framework Q7（explicit rate-limit contract）判
  `NOT_ESTABLISHED`；縱使可確證，rate limit 本身亦非「契約」。

---

## 9. Retention and Historical Storage（保存與歷史儲存）

官方明文（O1）：私人使用例外限於
> "downloading one copy of the MLB Digital Properties on any single device for your personal, non-commercial home use"

且
> "...are provided for your private, non-commercial use..."

- **Raw response 保存**：Terms 未對 API raw bytes 之保存給予明文許可；超出「單份／個人／
  非商業／home use」之保存即落入需書面許可之複製範疇。判定 **NOT_ADDRESSED / 需許可**。
- **Normalized 內部儲存**：屬「reproduce / prepare derivative works」→ 依 O1 **須書面許可**。
- **Long-term / 歷史 archive**：官方無 API 專屬保存期限或刪除義務之明文 → **NOT_ADDRESSED**；
  在無許可下之歷史 backfill 與長期保存皆**須書面許可**。
- **Fingerprint / checksum 保存**：官方未述 → **NOT_ADDRESSED**；保守視為衍生內容之一部分，
  須許可。
- **刪除義務**：本輪未見 API 資料之刪除義務明文 → **NOT_ADDRESSED**（隱私政策本輪未擷取，
  且擬用 payload 為公開職業賽程／球員身分，非個資）。

---

## 10. Derived / Internal / Model Use（衍生／內部／模型使用）

- **Derived statistics**：O1 明文「prepare derivative works ... without first obtaining
  written permission」屬禁止 → **須書面許可**。
- **Model features**：屬上述衍生著作之套用 → **須書面許可**（ML-specific 字樣官方未列，屬
  NOT_ADDRESSED，但衍生條款為治理預設）。
- **Model training**：官方文本**未直接述及** ML 訓練 → **NOT_ADDRESSED**；惟複製／衍生條款
  為治理預設，實務上仍須許可。
- **Internal evaluation / analysis**：私人非商業 home-use 例外狹窄，betting 研究專案是否屬之
  並無明文 → **NOT_ADDRESSED / 需許可**。

---

## 11. Redistribution and Commercial Use（再散布與商業使用）

- **Redistribution**：O1
  > "reproduce, prepare derivative works based upon, distribute, perform or display ... without first obtaining written permission"
  及
  > "Third Party Materials shall not be published, broadcast, rewritten for broadcast or publication or redistributed directly or indirectly in any medium"
  → **EXPLICITLY RESTRICTED（須書面許可）**。
- **Commercial use**：服務「provided for your private, non-commercial use」→ 商業使用
  **EXPLICITLY RESTRICTED（須許可）**。betting 研究／可能商業化之情境**不**落入個人非商業
  例外。
- **User-facing display**：O1 將 "display" 列入須書面許可之列 → 對外顯示來自未授權 MLB 資料
  之內容 **EXPLICITLY RESTRICTED**。

---

## 12. Attribution, Copyright and Trademark（標示、著作權與商標）

- **著作權聯絡（§2 DMCA Copyright Agent；非 licensing/permission office）**（O1）：Terms 指定
  - MLB Advanced Media, L.P., **Copyright Agent**（DMCA 侵權通知用途；§2 "Service Provider: MLB Advanced Media, L.P."）, 1271 Avenue of the Americas, New York, NY 10020
  - 電子郵件：`legaldepartment@mlb.com`（DMCA / 一般法律通知；**非**確認之 data/API licensing 管道。prior incorrect wording 曾稱「許可聯絡」）
- **Attribution 文字**：官方無明文要求之確切 attribution 格式（本輪未見）→ **NOT_STATED**。
- **Trademark / 商標**：`legal-notices` 專頁本輪 HTTP 406 不可擷取 → 商標使用須許可之專屬
  條款本輪 **UNKNOWN**（不沿用 P202F 引文為本輪證據）。惟 O1 之「未經書面許可不得複製／
  展示」已涵蓋大部分內容使用面向。
- **資料所有權**：搜尋摘要曾出現 BOC/MLBAM/Clubs 為 Event Information 權利人之語句，但該語句
  來自**搜尋摘要非擷取頁面**，依規則**不列為證據** → 本項以 O1 之著作權／許可條款為準，
  其餘標 **UNKNOWN**。

---

## 13. Authorization and Contact Paths（授權與聯絡管道）

| 管道 | 官方 URL / 位址 | 類型 | 是否專責 data/API 授權 | 是否需帳號 | 公開申請表 | 是否合理涵蓋本專案用途 | 下一步所需資訊 |
|---|---|---|---|---|---|---|---|
| StatsAPI 自助註冊工具 | `https://inside.mlb.com/UserRegistrationForm/?GROUP=StatsAPI` | 帳號 self-registration（**非 usage license**） | 否（僅帳號申請，非用途授權） | 是（User ID/email/T&C 接受） | 是（線上表單） | **NOT_ESTABLISHED**（資格 NOT FOUND；頁面重申禁複製/衍生/散布） | 用途說明、是否屬 club/vendor/partner 類別、是否覆蓋外部 betting 研究衍生使用 |
| 註冊支援 | `registrationsupport@mlb.com` | **TECHNICAL_REGISTRATION_SUPPORT** | 否（僅帳號/技術支援） | — | — | 否（非授權管道） | 帳號/註冊技術問題 |
| 著作權/法律（DMCA） | `legaldepartment@mlb.com`；§2 **Copyright Agent**（DMCA）, 1271 Avenue of the Americas, NY；§11 MLBAM "Attn: General Counsel" | **GENERAL_LEGAL_OR_DMCA_CONTACT / FALLBACK_CONTACT_ONLY** | 否（DMCA/法律通知；**非** data/API licensing office） | — | 否 | 否（fallback；非用途相符 licensing 管道） | 僅 fallback；本專案用途之正式 licensing 管道未建立 |

**判定（更正；prior incorrect wording 曾寫「YES_EXPLICIT, path found」並把 `legaldepartment@mlb.com` 當「書面許可請求入口」）**：

- **用途相符之正式 data/API licensing / authorization 管道：`NOT_ESTABLISHED`。** 本輪未查得
  任何官方明列、適用於本專案（外部、自動化、衍生、betting 研究）用途之 data licensing 申請管道。
- 已查得者僅為：(a) **帳號 self-registration 入口**（StatsAPI 自助註冊；資格 NOT FOUND、非
  usage license）；(b) **DMCA Copyright Agent / 一般法律通知** `legaldepartment@mlb.com`
  （§2 DMCA 用途，fallback，非 licensing office）；(c) **技術註冊支援**
  `registrationsupport@mlb.com`。
- 「可聯絡之 fallback」**不等於**「找到用途相符之授權管道」，更**不等於**已取得授權。本報告
  **不**主張授權不可取得，僅陳述**尚未找到用途相符之官方 licensing 管道**。

---

## 14. Evidence Matrix（證據矩陣）

| Src | URL | Domain | Title / 類型 | Issuer | Date | Accessed | 支持的 policy question | Strength | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| O1 | `www.mlb.com/official-information/terms-of-use` | www.mlb.com | Terms of Use Agreement | MLB / MLBAM | Updated 2025-03-11 | 2026-06-13 | Q1 自動化、Q2 保存、Q3 衍生、Q4 模型、Q5 散布、Q6 商業、Q7 attribution；範圍=§1「subject to this Agreement」**條款（非定義）** | **EXPLICIT** | HIGH |
| O2 | `www.mlb.com/robots.txt` | www.mlb.com | robots.txt | MLB / MLBAM | n/a | 2026-06-13 | Q8 robots（www host） | **EXPLICIT** | HIGH |
| O3 | `inside.mlb.com/UserRegistrationForm/?GROUP=StatsAPI` | inside.mlb.com | MLB Self Registration Utility | MLB | n/a | 2026-06-13 | Q9 授權/聯絡管道 | **EXPLICIT(管道)/SILENT(資格)** | MEDIUM |
| O5 | `statsapi.mlb.com/robots.txt` | statsapi.mlb.com | robots.txt → 404 | MLB / MLBAM | n/a | 2026-06-13 | Q8 robots（目標 host 沉默） | **EXPLICIT(存取結果)** | HIGH |
| O4 | `docs.statsapi.mlb.com/getting-started/*` | docs.statsapi.mlb.com | auth / rate-limiting | MLB / MLBAM | — | 2026-06-13（body 空） | Q1/Q3 速率/驗證 | **SILENT(本輪不可擷取)** | n/a |
| O6 | `www.mlb.com/official-information/legal-notices` | www.mlb.com | Legal Notices → 406 | MLB / MLBAM | — | 2026-06-13（406） | Q7 商標/著作權 | **SILENT(本輪不可擷取)** | n/a |
| O7 | `www.mlb.com/tac` | www.mlb.com | Terms & Conditions → 406 | MLB / MLBAM | — | 2026-06-13（406） | Q1/Q3 條款 | **SILENT(本輪不可擷取)** | n/a |
| O8 | `docs.statsapi.mlb.com/openapi.json` | docs.statsapi.mlb.com | OpenAPI spec v2.0.0；"Official API for Major League Baseball." | MLB | — | 2026-06-13 | statsapi 官方身分（範圍適用強推論之錨點） | **EXPLICIT(身分)** | HIGH |

**Conflicting evidence**：未發現官方來源之間互相矛盾。`www.mlb.com` robots 不歡迎 `/api/`
抓取，與目標 host 無 robots（沉默）並不矛盾（不同 host）。robots（態度）與 Terms（契約）層級
不同，亦非矛盾。**non-official source used as evidence = 0。**

---

## 15. Threat and Compliance Assessment（威脅與合規評估，皆為專案風險決策）

| 風險 | 證據 | 可能性 | 衝擊 | 現有緩解 | 殘餘風險 | go/no-go 意涵 |
|---|---|---|---|---|---|---|
| Terms-of-use 違約 | O1 明文禁 automated scripts；範圍涵蓋 MLBAM 服務 | 高（若 live 抓取） | 高 | 維持 fixture-only、未呼叫 endpoint | 高（一旦 live） | **NO-GO（live）** |
| 著作權／資料庫內容 | O1 複製/衍生須書面許可 | 高（保存/衍生） | 高 | 不保存 raw/normalized；僅 metadata | 高 | **NO-GO（保存/衍生）** |
| 自動化存取遭封鎖 | O2 www `/api/` Disallow；O5 目標 host 無 robots | 中 | 中 | 不抓取 | 低（不抓取時） | NO-GO 強化 |
| 帳號／IP 限制 | O3 註冊/憑證體系存在 | 中 | 中 | 不登入、不申請帳號 | 低 | 須先合法管道 |
| 保存／刪除義務 | O1 無 API 保存權；衍生須許可 | 中 | 中 | 不保存資料 | 中（未明） | NO-GO（保存） |
| Redistribution | O1 明文禁未授權散布 | 高（若公開/commit） | 高 | 不 commit 任何 payload | 高 | **NO-GO** |
| 模型訓練／衍生不確定 | O1 衍生須許可；ML 字樣 NOT_ADDRESSED | 中 | 中–高 | 不以未授權資料建特徵 | 中 | NO-GO（未授權資料） |
| Attribution 風險 | attribution NOT_STATED | 低–中 | 低 | 不對外顯示 | 中（未明） | 需許可後確認 |
| 政策變更 | O1 可隨時變更/停止服務 | 中 | 中 | 不依賴 | 中 | 不建立 production 依賴 |
| 無法證明歷史可得性 | post-hoc backfill 無法重建賽前時點 | 高 | 中–高 | 僅 fixture | 高 | 與 live HOLD 一致 |
| 依賴未文件化行為 | docs 本輪不可擷取；token 未列舉 | 中 | 中 | 不依賴 | 中 | 不建立 runtime 依賴 |

---

## 16. One-Shot Dry-Run Decision（單次 live dry-run 裁定）

**裁定：NO — 無法僅憑現有官方證據授權任何 one-shot live 呼叫。**

- O1 明文禁止 "use automated scripts to collect information from or otherwise interact with"
  MLB Digital Properties；其適用於 `statsapi.mlb.com` 屬**強支撐推論**（O8 openapi 確認該 host
  為官方 MLB API；Terms 未逐字點名）——對 one-shot 決策已足夠保守。
- 官方**無**任何「單次／低頻／非商業診斷」之公開例外被查得。
- 依任務規則，**不得**將「公開、no-auth、rate limit 存在、robots 沉默」改寫為許可，亦**不得**
  把低頻 one-shot 描述成自然合法。
- 故 one-shot live dry-run **不**可由現有證據自我授權；須另有用途相符之**書面**許可。

---

## 17. Recurring Collector Decision（週期性 collector 裁定）

**裁定：NO — 比 one-shot 更明確不被允許。**

- 週期性自動化採集直接落入 automated-scripts 禁令核心，且涉及保存／衍生／（潛在）散布，
  全部須書面許可。
- 無任何官方明文支持外部週期性 collector。**NO-GO**，維持 HOLD。

---

## 18. Conservative Technical Boundary（最保守技術邊界）

在無用途相符之書面授權前，最保守且符合證據之邊界為：

- ✅ **fixture-only development**（沿用 P202D/P202E/P202G-B 之 fixture-only、no-network、
  fail-closed 模式）。
- ✅ 僅使用**人工提供之已授權 fixture**。
- ❌ **no live transport**、❌ **no recurring collection**、❌ **no historical backfill**。
- ❌ **no production dependency**、❌ **no provider unlock**、❌ **no learning eligibility**。
- ❌ **no user-facing claim sourced from unlicensed data**。
- 🚫 **不**建議以 rotating user agent、proxy、低頻請求或任何規避手法降低風險；**不**將低頻
  one-shot 描述成自然合法。
- 任何 P202G live 之實作與執行，須在取得並另行審查**用途相符之官方書面授權**後，由**獨立**的
  授權回合處理。

---

## 19. Evidence Gaps（證據缺口）

1. docs 子網域（auth-authorization、rate-limiting）本輪 JS-rendered 不可擷取 → 「public use
   不受支援／no-auth public schedules／25 req/s」本輪未獨立確證。
2. `legal-notices`、`/tac` 本輪 HTTP 406 → 商標／第二份條款本輪不可擷取。
3. `hydrate=probablePitcher` 是否官方支援：本輪未擷取 openapi.json（聚焦政策、避免資料 host
   疑義）→ NOT ADDRESSED（屬 P202F 技術問題）。
4. StatsAPI 註冊工具之**資格與許可用途**未公開陳述 → 無法確認本專案外部 betting 研究用途
   是否被涵蓋。
5. attribution 確切文字、API 資料保存期限／刪除義務、衍生資料 betting 研究與商業化之專屬
   裁定：官方文本**未明文** → 須書面澄清。

---

## 20. Recommended Next Action（建議下一步）

1. **維持 live transport HOLD**；維持 fixture-only。不得新增 live/transport/collector/backfill。
2. 若確有 live 取數需求，**唯一**合規路徑為先取得**用途相符之官方書面授權**：
   - **先確認用途相符之官方 data/API licensing 管道**（本輪 `NOT_ESTABLISHED`）：
     `legaldepartment@mlb.com` 僅為 §2 **DMCA Copyright Agent / 一般法律通知**（fallback，非
     licensing office），不宜當作 licensing 入口；應循官方法律／商務管道查詢正式 data
     licensing／permission 窗口。請求內容應涵蓋：自動化存取、raw 與 normalized 保存（與期限）、
     fingerprint、衍生統計／模型特徵、betting 研究／（潛在）商業使用、redistribution、
     attribution、撤銷／到期條件；並／或
   - 評估 `inside.mlb.com` StatsAPI 自助註冊工具之資格與用途適配（帳號註冊 ≠ usage license；
     需確認是否屬可申請類別）。
   - 上述為**人類發起**之外部聯絡，非本任務範圍；本任務未送出任何申請。
3. 取得任何書面回覆後，於**新的授權回合**重新審查；即使回覆有利，亦僅使後續 P202G live 任務
   **有資格**接受**另行明確之使用者授權**，不等於可直接執行。
4. 可選的純離線後續：補強 docs/legal-notices 之官方擷取（改用可執行 JS 之擷取方式）以填補
   §19 缺口，但此不改變 live HOLD。

---

## 21. Required Completion Check（必填完成檢查）

| Item | Result |
|---|---|
| 是否真的完成 | 是 |
| Phase 0 PASS / FAIL | **PASS** |
| Official sources reviewed count | 9 URL（4 可擷取為證據，含 O8 openapi；5 access-failed） |
| Official domains reviewed | `www.mlb.com`、`inside.mlb.com`、`docs.statsapi.mlb.com`、`statsapi.mlb.com`（僅 robots） |
| Non-official evidence count | **0** |
| Automated access classification | **EXPLICITLY PROHIBITED**（O1；restriction 為 explicit official text） |
| StatsAPI applicability level | **STRONGLY_SUPPORTED_INFERENCE**（足以 HOLD；§1 範圍條款＋正式定義＋O8 openapi） |
| Direct hostname naming status | **NOT_ESTABLISHED**（Terms 未逐字點名 `statsapi.mlb.com`） |
| legaldepartment classification | **GENERAL_LEGAL_OR_DMCA_CONTACT / FALLBACK_CONTACT_ONLY** |
| registrationsupport classification | **TECHNICAL_REGISTRATION_SUPPORT** |
| Raw retention classification | NOT_ADDRESSED / 須書面許可 |
| Derived/internal use classification | REQUIRES_LICENSE_OR_PERMISSION |
| Model training classification | NOT_ADDRESSED（衍生條款為預設，須許可） |
| Redistribution classification | EXPLICITLY_RESTRICTED |
| Commercial/user-facing classification | EXPLICITLY_RESTRICTED |
| Explicit rate-limit evidence status | NOT_ESTABLISHED（本輪 docs 不可擷取；且 rate limit ≠ 契約） |
| Formal authorization path status | **NOT_ESTABLISHED**（用途相符 data/API licensing 管道未建立；僅帳號註冊入口 + DMCA/一般法律 fallback） |
| One-shot dry-run decision | **NO**（不可由現有證據自我授權） |
| Recurring collector decision | **NO** |
| Robots.txt interpretation | www host disallow `/api/`（不同 host）；目標 host 無 robots（404，沉默）；robots ≠ 授權 |
| Evidence conflicts | 無官方來源互相矛盾 |
| Evidence gaps | docs/legal-notices/tac 本輪不可擷取；註冊資格未公開；attribution/保存期限未明文 |
| Live transport HOLD status | **HOLD（維持）** |
| Report path | `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md` |
| Report completeness | 21 sections + metadata + completion check 齊備 |
| Citation completeness | 每核心主張均有官方引用或標 UNKNOWN |
| Quote-limit compliance | 所有 verbatim 引文 ≤ 25 words |
| Tests PASS / FAIL / NOT RUN | **NOT RUN**（純政策報告，未改程式；治理/source/test 未動） |
| git diff check | 預計 PASS（見 Phase 11） |
| Modified file count | 1（僅本報告，新增） |
| Modified file list | `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md` |
| Governance files unchanged | 是（四治理檔未動） |
| Source/test/config unchanged | 是 |
| Staged files | 0 |
| Current branch | `main` |
| Local HEAD / origin/main | `cac2a748...` / `cac2a748...`（相等） |
| Open PR count | 0 |
| Network use limited to official policy pages | 是（僅官方政策/robots/註冊頁；0 data endpoint） |
| MLB data endpoint call count | **0** |
| DB/runtime/production mutation status | NONE |
| Single blocker or NONE | **Blocker：缺乏用途相符之官方書面授權；且 O1 明文禁自動化存取** |
| Whether live one-shot implementation is authorized next | **NO** |
| Whether recurring collector implementation is authorized next | **NO** |
| Recommended next task | 維持 fixture-only；若需 live，人類先確認用途相符之官方 data/API licensing 管道（本輪 NOT_ESTABLISHED；`legaldepartment@mlb.com` 僅 DMCA/法律 fallback）並取得書面許可後，於新回合重審 |
| Worker model recommendation | Opus 強 |
| Thinking level recommendation | 強 |
| Same/new conversation recommendation | 新回合（live 實作須獨立授權；本回合僅證據） |
| Final Classification | `P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND` |

---

## Final Classification

**`P202G_A_EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND`**

本輪自官方 MLB.com Terms of Use（2025-03-11）獨立查得**明文 (explicit)** 之自動化存取限制：
禁止 "use automated scripts to collect information from or otherwise interact with" MLB Digital
Properties（binds all users），且複製／衍生／散布／展示須先取得書面許可。該限制**適用於**本
專案擬使用之 `statsapi.mlb.com` 屬 **STRONGLY_SUPPORTED_INFERENCE**——以 §1「…are subject to
this Agreement」**範圍條款**、正式定義（"MLB-controlled products or services..."）與官方 OpenAPI
（`statsapi.mlb.com` = *"Official API for Major League Baseball."*）共同支撐，**足以維持 HOLD**；
但 **Terms 未逐字點名該 hostname**，故不主張直接明文點名（prior incorrect wording 曾稱「直接
適用／決定性」）。**用途相符之官方 data/API licensing 管道 `NOT_ESTABLISHED`**：
`legaldepartment@mlb.com` 經查為 §2 DMCA Copyright Agent（fallback，非 licensing office），
StatsAPI 自助註冊為帳號入口（非 usage license）。依任務規則，公開性／no-auth／robots 沉默／
rate limit 技術存在皆**不得**改寫為授權。因此 live transport（P202G）**維持 HOLD**，最保守
邊界為 **fixture-only**；任何 live 一次性或週期性實作均**不**得由現有證據自我授權，須另取得
用途相符之官方書面授權並由獨立回合審查。
