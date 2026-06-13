# P202G-A — Source Policy Evidence Packet 獨立對抗性複審 (Independent Re-Review)

> 本報告為**獨立、對抗性、唯讀**複審，重新自官方來源驗證，不僅信任既有報告或上一個
> worker 摘要。所有法律性結論一律以**專案風險決策**陳述，非法律意見。每一核心主張附官方
> 引用或標 UNKNOWN；每來源引文 ≤ 25 英文字。本輪**未修改** evidence packet 或任何治理/原始碼。

## Report Metadata

| 欄位 | 值 |
|---|---|
| `generated_at_utc` | `2026-06-13T14:49:52Z` |
| 報告檔名日期 | `20260614`（依任務指定檔名） |
| `accessed_at` range（本複審輪） | 約 `2026-06-13T14:40Z` – `14:50Z`（Asia/Taipei 22:40–22:50） |
| `repository` | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` |
| `branch` | `main` |
| `HEAD` | `cac2a748dff5077dd3b947fbacdc01dbdeec5607` |
| `task ID` | `P202G-A-R` |
| Primary report under review | `report/p202g_a_source_policy_clarification_evidence_packet_20260614.md` |
| Official sources independently rechecked | 4（Terms of Use×3 targeted、`www.mlb.com/robots.txt`、`statsapi.mlb.com/robots.txt`、`docs.statsapi.mlb.com/openapi.json`） |
| Official domains | `www.mlb.com`、`statsapi.mlb.com`(robots only)、`docs.statsapi.mlb.com` |
| **Non-official evidence count** | **0** |
| **MLB data endpoint call count** | **0** |
| P202F classification | `P202F_SOURCE_POLICY_CLARIFICATION_REQUIRED` |
| live transport status | **HOLD（維持）** |

---

## 1. Executive Verdict（執行裁決）

**裁決：`NEEDS_REPORT_FIX`。** Evidence packet 的**最終決策全部正確且保守**（自動化存取受官方
明文限制、live one-shot 與 recurring 皆不可自我授權、live transport 維持 HOLD），且其引用的核心
條文**確為官方文件中之真實逐字文字**（非捏造、非非官方來源）。但本輪對抗性重驗發現**兩處
須窄修的引用／管道精確性瑕疵**，在納入治理更新與 commit packaging 前應先更正：

- **Blocker（單一最小）— 決定性範圍引文「誤標」**：packet 將
  > "...by MLB Advanced Media, L.P. ('MLB') are subject to this Agreement"（Terms §1 真實逐字）

  標示為「**"MLB Digital Properties" 的定義**」並截掉其操作性結尾 "are subject to this
  Agreement"。實際上這是 §1 的「**受本協議拘束**」範圍條款；正式定義是**另一句**（"...other
  MLB-controlled products or services or MLB-operated interactive media locations..."）。
  packet 據此將適用性寫成「決定性／直接適用」，而 `statsapi.mlb.com` 並未被條款**逐字點名**。
- **次要 — 聯絡管道誇大**：packet 將 `legaldepartment@mlb.com` 描述為「書面許可請求入口」，
  但官方文件中該地址明列於 **"Copyright Agent"（DMCA 著作權侵權通知）** 章節，非 data/API
  licensing 管道。

兩瑕疵**皆為報告層級文字精確性**，**不改變任何決策**，且方向保守（偏向更強限制，不會誤導向
live 授權）。本複審**不**修改 packet；僅列最小 blocker 與窄修 scope（見 §16）。

> 補強發現（對 packet 有利）：本輪自官方 `openapi.json` **直接**確認 `statsapi.mlb.com` 為
> *"Official API for Major League Baseball."* 之 Production server——這使「適用性」比 packet 原
> 引文更穩固，但應改以**正確歸屬**之 §1 範圍條款 + openapi 身分證據陳述，而非「定義點名」。

---

## 2. Scope and Non-Actions（範圍與未執行動作）

- ❌ 未呼叫任何 MLB 資料 endpoint（schedule/game/player/boxscore/stats/roster/probablePitcher/
  任何賽事或球員資料）。`statsapi.mlb.com` 僅取 `robots.txt`（404），未觸 `/api/...`。
- ❌ 未探索 undocumented API、未 enumeration、未 transport/collector、未 fixture、未 backfill。
- ❌ 未寫 runtime/DB/log payload；未改 source/test/config/fixture。
- ❌ **未修改 evidence packet**；未改四治理檔；未送 email/聯絡 MLB；未登入/取 token/接受契約。
- ❌ 未 branch/checkout/stage/commit/push/PR/merge/rebase/reset/stash/clean/delete；未 `git add`。
- ✅ 唯一寫檔：`report/p202g_a_source_policy_clarification_independent_review_20260614.md`（本檔）。
- ✅ 僅存取官方人類可讀政策/條款/robots/openapi 文件 + 一般網路搜尋找官方頁。

---

## 3. Governance and Phase 0

### Required Governance Read（本輪實讀）
- `SHARED_AGENT_BOOTSTRAP.md`：READ — Phase 0、STOP、whitelist、no-external-effects 規則適用。
- `TASK_TEMPLATES.md`：READ — 本任務符合 Template 2（Read-Only Execution）＋單一 report 白名單。
- `CURRENT_STATE.md`：READ — HEAD=`cac2a748`、tolerated dirty 清單、authorized uncommitted
  governance 清單與實測一致；line 99 明載「rate-limit/no-auth/public-accessibility 不得讀為
  automated-use permission」，與本複審立場一致。
- `active_task.md`：READ（前輪）— 仍為 P202G-A policy evidence 軸；本任務 P202G-A-R 為其複審，
  同軸不衝突。
- `roadmap.md` / `CTO-Analysis.md`：列既知 dirty；唯讀對待，未改。

### Phase 0 — Actual State Verification
| Check | Observed | Result |
|---|---|---|
| pwd / toplevel | `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` | PASS |
| branch / symbolic HEAD | `main` / `main`（非 detached） | PASS |
| git-dir | `.git` | PASS |
| local HEAD == origin/main == Expected | `cac2a748...` 三者相等 | PASS |
| staged files | 0 | PASS |
| open PR | 0 | PASS |
| Python | 3.13.8（≥3.11） | PASS |
| P202G-A evidence packet 存在 | 是（38,003 bytes） | PASS |
| P202F report 存在 | 是 | PASS |
| active_task 仍 P202G-A 軸 | 是 | PASS |
| no pitcher-event/probable-starter runtime data path | 僅 `.py` 模組，無資料目錄 | PASS |
| dirty tree = 既知 inventory（+ evidence packet untracked） | 與 prompt Known Dirty Inventory 一致 | PASS |

**Phase 0 = PASS。** dirty 清單＝3 治理 modified + 10 tolerated runtime + `agent_bootstrap/`（3 檔）
+ 5 既有排除報告 + P202G-A evidence packet（untracked）。無 STOP 觸發。

---

## 4. Evidence Packet Claim Inventory（claim 盤點與標記）

標記：`DIRECT_OFFICIAL_TEXT` / `SUPPORTED_INFERENCE` / `UNSUPPORTED_INFERENCE` / `UNKNOWN` / `CONFLICTING`

| # | Claim（packet） | 本輪重驗 | 標記 |
|---|---|---|---|
| 1 | automated-scripts 禁令 | 全句確認 "You must not use the MLB Digital Properties...to:...(xi) use automated scripts..." | **DIRECT_OFFICIAL_TEXT** ✅ |
| 2 | 「"MLB Digital Properties" **定義**含 MLBAM…」 | 引文為 §1「…by MLB Advanced Media, L.P. ('MLB') **are subject to this Agreement**」之真實逐字，但屬**範圍條款非定義**；正式定義為另一句 | **CONFLICTING（引文真實但誤標為定義；截斷操作性結尾）** |
| 3 | 適用於 `statsapi.mlb.com`（packet：直接適用） | §1「受本協議拘束」條款(DIRECT) + openapi「Official API for MLB」server=statsapi(DIRECT)；「statsapi 屬 MLBAM(而非泛 MLB)」為 micro-inference | **STRONGLY_SUPPORTED_INFERENCE**（packet 寫成「直接/決定性」略強） |
| 4 | 私人/非商業限定 | 與 §1/§4 一致（前輪逐字） | DIRECT_OFFICIAL_TEXT ✅ |
| 5 | 複製/衍生/散布/展示須書面許可 | §1 prohibitions（前輪逐字） | DIRECT_OFFICIAL_TEXT ✅ |
| 6 | retention 分類（raw/normalized/archive） | 源自複製條款之套用 | SUPPORTED_INFERENCE（packet 已標需許可/NOT_ADDRESSED，合理） |
| 7 | derived-use 分類 | 源自 derivative 條款 | SUPPORTED_INFERENCE（合理） |
| 8 | model-training 分類 | packet 標 NOT_ADDRESSED | **正確（誠實 UNKNOWN/NOT_ADDRESSED）** ✅ |
| 9 | redistribution | "distribute...without...written permission" | DIRECT_OFFICIAL_TEXT ✅ |
| 10 | commercial/user-facing | 私人非商業 + "display...without...permission" | DIRECT_OFFICIAL_TEXT ✅ |
| 11 | robots host distinction | www `/api/` disallow（重驗）；不同 host | DIRECT_OFFICIAL_TEXT ✅ |
| 12 | target-host robots 404 | `statsapi.mlb.com/robots.txt`=HTTP 404（重驗） | DIRECT_OFFICIAL_TEXT ✅ |
| 13 | 授權/聯絡管道（legaldepartment 為許可入口） | 官方標為 **Copyright Agent（DMCA）**；非 licensing office | **UNSUPPORTED_INFERENCE（誇大）** |
| 14 | one-shot 不可自我授權 | 與明文限制一致 | SUPPORTED ✅ |
| 15 | recurring 不可自我授權 | 同上 | SUPPORTED ✅ |

> 沒有把 SUPPORTED_INFERENCE 改寫為 DIRECT_OFFICIAL_TEXT。Claim 2、3、13 為本裁決依據。

---

## 5. Official Source Authenticity（官方來源真實性）

| 來源 | 最終 domain | 真實性 | 本輪結果 |
|---|---|---|---|
| Terms of Use `www.mlb.com/official-information/terms-of-use` | www.mlb.com（HTTPS） | 官方 MLB；標題 "Terms of Use Agreement"；Last Updated **2025-03-11**；§1/§2/§11 章節結構一致可重現 | **CURRENT、官方、可重現** |
| `www.mlb.com/robots.txt` | www.mlb.com | 官方 | 重驗：`User-agent: *`、含 `Disallow: /api/`（其餘 Disallow 子集隨擷取略異，`/api/` 恆在） |
| `statsapi.mlb.com/robots.txt` | statsapi.mlb.com | 官方 host | **HTTP 404**（重驗一致） |
| `docs.statsapi.mlb.com/openapi.json` | docs.statsapi.mlb.com | 官方 API spec | info.title="Stats API Documentation" v2.0.0；description=**"Official API for Major League Baseball."**；servers 含 `https://statsapi.mlb.com (Production)`；info.contact/license/termsOfService=absent |

- 非官方來源**未**作為政策證據（count=0）。搜尋引擎 snippet **未**作為證據。
- ⚠️ **WebFetch 抽取非決定性**：同一 Terms URL 不同 prompt 取得不同句子片段（見 §6），本輪以
  「字串存在性 + 章節歸屬」交叉確認真實性，未以單次抽取為準。

---

## 6. Automated-Access Restriction（自動化存取限制 — 重新定位核對）

**完整禁止句（本輪逐字確認）**：
> "You must not use the MLB Digital Properties...to:...(xi) use automated scripts to collect information from or otherwise interact..."

驗證：
1. 禁止句**完整存在**且為列舉式 "You must not use...to:" 之第 (xi) 項。✅
2. 該 (xi) 子句**未**附鄰近 "unless permitted/without consent" 等 carve-out——就引文所見，
   automated-scripts 禁令**無明文書面許可例外**（與複製/衍生/散布/展示之 "without first
   obtaining written permission" 不同）。此使 HOLD **更**穩固，非更弱。
3. 適用對象：**所有使用者**——"By using an MLB Digital Property, you agree to be bound by this
   Agreement."（無帳號區分）。✅
4. 不限特定頁/商業用途；為一般使用禁令。
5. 違反後果：§7 免責 + §10「may change, suspend or discontinue」（前輪確認）。

**packet 對此 claim 正確**（claim 1）。本輪未發現此禁令的反證或限縮。

---

## 7. StatsAPI Scope Applicability（適用性 — 獨立裁決）

可接受官方證據（本輪）：
- Terms §1 逐字：
  > "...all products and services provided and/or distributed (whether via this Website or elsewhere) by MLB Advanced Media, L.P. ('MLB') are subject to this Agreement"（**DIRECT**：MLBAM 提供/散布之產品服務「無論本站或他處」均**受本協議拘束**）
- Terms 正式定義（**另一句**，DIRECT）：
  > "...otherwise accessible via other MLB-controlled products or services or MLB-operated interactive media locations...referred to herein collectively as the 'MLB Digital Properties'"
- openapi.json（DIRECT）：`statsapi.mlb.com` = *"Official API for Major League Baseball."* 之 Production server。

**裁決分類：`STRONGLY_SUPPORTED_INFERENCE`**（接近 `DIRECTLY_ESTABLISHED`）。
- 「MLB 官方 API（statsapi）受 Terms 拘束」由 §1「受本協議拘束」條款 + 正式定義「MLB-controlled
  products or services」+ openapi「Official API for MLB」三條 DIRECT 證據共同支撐，**足以維持
  保守 HOLD**。
- 唯一 inferential micro-gap：條款**未逐字點名** "statsapi.mlb.com"；「Official API for MLB」
  與「MLB Advanced Media, L.P.」之等同為小幅推論（雖「MLB-controlled products or services」已
  涵蓋）。
- ⚠️ 因此 **packet §1/§6 將適用性寫成「直接適用／決定性」並把 §1 範圍條款誤標為「定義」**，
  屬「把 STRONGLY_SUPPORTED_INFERENCE 表述為官方明文直接點名」之邊界違反 → 須窄修（§16）。

---

## 8. Exceptions and Written Permission（例外與書面許可）

- 複製/衍生/散布/展示：明載 "without first obtaining written permission" → **書面許可例外存在
  （取得書面同意前禁止）**：`YES_EXPLICIT`（許可路徑理論上存在，但須事前書面同意）。
- automated-scripts (xi)：引文**無** carve-out → 該禁令是否可由書面許可解除 **NOT_ESTABLISHED**。
- 是否已取得適用書面許可：**NO**（無任何官方核准證據）。
- StatsAPI 自助註冊工具：為**帳號註冊**入口，**未**證明其本身構成 automated-collection /
  retention / derived-use 之 usage license → 註冊存在 ≠ 取得 API license。
- 無查得專責 data licensing 管道之官方頁。**不得**把「可聯絡」寫成「會核准」。

---

## 9. Contact Path Review（聯絡管道複審）

| 地址 | 出現章節（官方） | 原始用途 | 分類 |
|---|---|---|---|
| `legaldepartment@mlb.com` | Terms §2 **"Copyright Agent"**（DMCA 通知）；§2 "Service Provider: MLB Advanced Media, L.P." | 著作權侵權通知（DMCA） | **GENERAL_LEGAL_CONTACT**（DMCA Copyright Agent；**非** data licensing office） |
| MLBAM "Attn: General Counsel", 1271 Avenue of the Americas | Terms §11（Dispute Resolution 通知地址） | 法律爭議通知 | GENERAL_LEGAL_CONTACT（書面通知地址） |
| `registrationsupport@mlb.com` | StatsAPI 自助註冊頁（前輪） | 註冊技術支援 | **TECHNICAL_REGISTRATION_SUPPORT** |
| StatsAPI 自助註冊工具 `inside.mlb.com/...?GROUP=StatsAPI` | 前輪 | 帳號存取申請 | **NOT_ESTABLISHED**（非 usage-authorization；資格 NOT FOUND） |

- **Copyright Agent 不得自動視為 data licensing office；registration support 不得視為 usage
  authorization office。** → **packet §13/§20 將 `legaldepartment@mlb.com` 作「書面許可請求入口」
  屬誇大**（claim 13）。窄修：降為 DMCA/一般法律通知聯絡，明記**未**找到專責 data/API licensing
  管道。

---

## 10. Retention and Downstream Use（保存與下游使用 — 逐項複核）

| 項目 | packet 分類 | 本複審判定 | 標記 |
|---|---|---|---|
| A. Raw response retention | NOT_ADDRESSED/需許可 | NOT_ADDRESSED（個人單份例外不涵蓋研究用 API raw） | 一致 |
| B. Normalized internal storage | 需許可 | PERMISSION_REQUIRED（複製條款套用） | SUPPORTED ✅ |
| C. Historical archive | 需許可 | PERMISSION_REQUIRED | SUPPORTED ✅ |
| D. Derived statistics | 需許可 | PERMISSION_REQUIRED（derivative 條款） | SUPPORTED ✅ |
| E. Internal evaluation | NOT_ADDRESSED/需許可 | NOT_ADDRESSED | 一致 |
| F. Model features | 需許可（含 NOT_ADDRESSED 註） | PERMISSION_REQUIRED / NOT_ADDRESSED | SUPPORTED ✅ |
| G. Model training | NOT_ADDRESSED | NOT_ADDRESSED（ML 未明文） | **正確** ✅ |
| H. User-facing display | EXPLICITLY_RESTRICTED | EXPLICITLY_RESTRICTED（"display...without...permission"） | DIRECT ✅ |
| I. Redistribution | EXPLICITLY_RESTRICTED | EXPLICITLY_RESTRICTED | DIRECT ✅ |
| J. Commercial use | EXPLICITLY_RESTRICTED | EXPLICITLY_RESTRICTED（私人非商業） | DIRECT ✅ |

packet 對 §1 reproduction/derivative/distribution/display 限制之映射**忠實**；推論項皆已標
需許可或 NOT_ADDRESSED，**無**把推論寫成明文。此區**無瑕疵**。

---

## 11. Robots and Technical Accessibility（robots 與技術可達性）

| host | HTTP | accessed_at | directives | 解讀 |
|---|---|---|---|---|
| `www.mlb.com/robots.txt` | 200 | 2026-06-13(本輪) | `User-agent: *`；`Disallow: /api/`（+ /test//app//embed//en//mlb/ 等，子集隨擷取略異） | **不同 host**；治理 `www.mlb.com/api/`，非 `statsapi.mlb.com/api/...` |
| `statsapi.mlb.com/robots.txt` | **404** | 2026-06-13(本輪) | 無檔 | 目標 host **無 robots 政策**（沉默，非允許） |

確認 packet 解讀**正確**：
- www host 規則不自動適用 target host ✅
- target-host 404 = 無 robots file ≠ 允許 ✅
- robots ≠ contract、technical accessibility ≠ permission、no-auth ≠ permission、low frequency
  ≠ permission、rate limit ≠ permission ✅（與 CURRENT_STATE line 99 一致）
- 本輪未呼叫任何 data endpoint。

---

## 12. Decision Reassessment（決策重評）

| # | 問題 | 本複審答案 | 與 packet |
|---|---|---|---|
| 1 | Automated access explicitly restricted? | **YES_EXPLICIT** | 一致 |
| 2 | Automated access explicitly authorized? | **NO_EXPLICIT** | 一致 |
| 3 | Written permission exception exists? | **YES_EXPLICIT**（複製/衍生類）；automated-scripts 子句 **NOT_ESTABLISHED**（無 carve-out） | 補強 |
| 4 | Applicable written permission obtained? | **NO_EXPLICIT** | 一致 |
| 5 | Raw retention established? | **NOT_ESTABLISHED** | 一致 |
| 6 | Derived/internal analysis established? | **PERMISSION_REQUIRED** | 一致 |
| 7 | Model use established? | **NOT_ESTABLISHED** | 一致 |
| 8 | Redistribution established? | **NO_EXPLICIT**（未授權即禁） | 一致 |
| 9 | Commercial/user-facing established? | **NO_EXPLICIT** | 一致 |
| 10 | One-shot dry run authorized? | **NO_EXPLICIT** | 一致 |
| 11 | Recurring collector authorized? | **NO_EXPLICIT** | 一致 |
| 12 | Live transport HOLD required? | **YES_EXPLICIT** | 一致 |

「條款存在 / 條款適用性 / 已取得許可」三者分離：限制**存在**（YES）、**適用性**為強支撐推論
（足以 HOLD）、**許可未取得**（NO）。**packet 的所有決策與本複審一致。**

---

## 13. Quote and Citation Audit（引文與引用稽核）

| 檢查 | 結果 |
|---|---|
| 每核心 claim 有官方 citation | 是（或標 UNKNOWN） |
| citation 指向錯誤 host | **是（1 處概念性）**：packet 之 robots `/api/` 屬 www host，packet 已正確標註不同 host；惟「適用性」decisiveness 來自誤標之 §1 條款（見下） |
| 引用 inaccessible page 當內容證據 | 否（docs HTML/legal-notices/tac 已標 UNKNOWN） |
| quote ≤ 25 words/來源 | 是（packet 與本報告皆符合） |
| accessed_at 完整 | 是 |
| document version 標示 | 是（Terms 2025-03-11） |
| access failure 誤寫為政策證據 | 否 |
| robots 沉默誤寫為許可 | 否 |
| **contact path 誇大** | **是**：`legaldepartment@mlb.com`（Copyright Agent）被寫為許可入口 |
| **direct fact 與 inference 分離** | **部分未達**：§1「are subject to this Agreement」範圍條款被誤標為「定義」且截斷操作性結尾；適用性寫成「直接/決定性」而 statsapi 未被逐字點名 |
| legal conclusion 寫成法律意見 | 否（packet 已框為風險決策） |
| final classification 符合證據強度 | `EXPLICIT_AUTOMATED_ACCESS_RESTRICTION_FOUND` **成立**（限制確為明文且適用性足以 HOLD）；惟支撐引文需更正歸屬 |

**兩處須修**：(a) 範圍引文誤標為「定義」+ 截斷；(b) Copyright Agent 誤作 licensing 管道。

---

## 14. Side-Effect Verification（副作用驗證 — Phase 11）

本輪於寫入唯一 report 後執行 git 檢查（見 §17 完成檢查表）：
- 只新增唯一 review report；evidence packet **未修改**；四治理檔**未**被本輪修改；
  source/test/config/fixture **未**修改；staged=0；HEAD=origin/main=`cac2a748`；無 runtime data
  path；無 API payload/log；無 DB/production mutation。`git diff --check` PASS。

---

## 15. Risks and Limitations（風險與限制）

- **WebFetch 抽取非決定性**：同一官方 Terms URL 不同 prompt 回不同句片段；本輪以字串存在性 +
  章節歸屬交叉確認，但無法保證已窮舉全文每一條款。殘餘風險：低（核心句已逐字確認）。
- **docs.statsapi.mlb.com HTML 政策頁** 仍 JS-rendered 不可擷取；"public use 不受支援" 等本輪
  仍 UNKNOWN（不影響 HOLD：限制由 Terms 直接確立）。
- **legal-notices / tac** HTTP 406 仍不可擷取（商標/第二份條款 UNKNOWN）。
- openapi 顯示 statsapi 為「MLB 官方 API」但未逐字寫「MLBAM」；適用性最後一哩為小幅推論。
- 本複審為**證據與報告品質**裁決，非法律意見。

---

## 16. Governance/Packaging Readiness（治理/打包就緒）

**Commit-Readiness：`NEEDS_REPORT_FIX`。**

**Single minimal blocker：** Evidence packet 的「決定性」適用性引文誤標——把 Terms §1 範圍條款
「…by MLB Advanced Media, L.P. ('MLB') **are subject to this Agreement**」標示為「"MLB Digital
Properties" 的**定義**」並截斷操作性結尾，致適用性被表述為「直接/決定性」而非強支撐推論。

**Proposed narrow fix scope（僅改 evidence packet 單檔，不改決策、不碰 endpoint、HOLD 不變）：**
1. §1/§6 範圍引用更正為 §1「受本協議拘束」條款之**正確逐字**（"...by MLB Advanced Media,
   L.P. ('MLB') are subject to this Agreement"），並標明這是**範圍/適用條款**；另引正式定義句
   "...other MLB-controlled products or services or MLB-operated interactive media locations..."。
2. 新增 openapi.json 之 *"Official API for Major League Baseball."* + server `statsapi.mlb.com`
   作為 statsapi 官方身分錨點；適用性改標 **STRONGLY_SUPPORTED_INFERENCE（足以維持保守
   HOLD）**，移除「直接點名 statsapi」式措辭。
3. §13/§20 將 `legaldepartment@mlb.com` 降為 **DMCA Copyright Agent / 一般法律通知**，明記**未**
   找到專責 data/API licensing 管道；`registrationsupport@mlb.com` = 技術註冊支援；StatsAPI 註冊
   工具 = 帳號申請，非 usage license。

> 上述修正屬另一**獨立、受權**之窄修回合（Template 3 / 報告更正）。本複審輪**不**執行該修正。
> 修正後即達 READY_FOR_GOVERNANCE_AND_PACKAGING（其餘 READY 條件本輪已滿足：限制已驗、HOLD
> 維持、robots 正確、one-shot/recurring 皆 NO、retention/downstream 映射忠實、無端點呼叫）。

**Live implementation allowed next？ NO。** Governance update / packaging 須待窄修完成。

---

## 17. Required Completion Check

| Item | Result |
|---|---|
| 是否真的完成 | 是 |
| Phase 0 PASS / FAIL | **PASS** |
| Official sources independently rechecked count | 4 來源（Terms×3 targeted、www robots、statsapi robots、openapi.json） |
| Official domains | `www.mlb.com`、`statsapi.mlb.com`(robots)、`docs.statsapi.mlb.com` |
| Non-official evidence count | **0** |
| Automated restriction authenticity | **VERIFIED — DIRECT_OFFICIAL_TEXT**（"You must not use...to:...use automated scripts..."；binds all users） |
| MLB Digital Properties definition status | packet 引文**真實但誤標為定義**；正式定義為另一句（"MLB-controlled products or services..."） |
| StatsAPI applicability classification | **STRONGLY_SUPPORTED_INFERENCE**（§1「subject to this Agreement」+ openapi「Official API for MLB」；足以 HOLD） |
| Written-permission exception status | 複製/衍生類 YES_EXPLICIT；automated-scripts 子句無 carve-out（NOT_ESTABLISHED） |
| Applicable permission obtained status | **NO** |
| legaldepartment contact classification | **GENERAL_LEGAL_CONTACT（DMCA Copyright Agent）；非 licensing office** |
| registrationsupport contact classification | **TECHNICAL_REGISTRATION_SUPPORT** |
| Automated access decision | RESTRICTED（YES_EXPLICIT restricted；NO_EXPLICIT authorized） |
| Raw retention decision | NOT_ESTABLISHED / 需許可 |
| Derived/internal decision | PERMISSION_REQUIRED |
| Model-use decision | NOT_ESTABLISHED / NOT_ADDRESSED |
| Redistribution decision | NO_EXPLICIT（未授權即禁） |
| Commercial/user-facing decision | NO_EXPLICIT（限私人非商業） |
| One-shot decision | **NO_EXPLICIT（不可自我授權）** |
| Recurring collector decision | **NO_EXPLICIT** |
| Live transport HOLD | **維持 HOLD** |
| Robots interpretation | **正確**：www `/api/`（不同 host）；statsapi 404（沉默）；robots ≠ contract |
| Evidence conflicts | 1：packet「定義」引文 vs 實際 §1 範圍條款/正式定義（已釐清，非官方來源互相矛盾） |
| Evidence gaps | docs HTML/legal-notices/tac 不可擷取；statsapi=MLBAM 逐字未證；專責 licensing 管道未找到 |
| Evidence packet accuracy | 決策正確；**2 處引用/管道精確性瑕疵需窄修** |
| Quote-limit compliance | PASS（≤25 words/來源，packet 與本報告） |
| Citation completeness | 大致完整；適用性支撐引文需更正歸屬 |
| Tests PASS / FAIL / NOT RUN | **NOT RUN**（純政策複審，未改程式/治理） |
| git diff check | **PASS（DIFF_CHECK_CLEAN）** |
| Modified file count/list | 1 — `report/p202g_a_source_policy_clarification_independent_review_20260614.md`（新增） |
| Evidence packet unchanged | **是（未修改）** |
| Governance unchanged | 是 |
| Source/test/config unchanged | 是 |
| Staged files | 0 |
| Current branch | `main` |
| Local HEAD / origin/main | `cac2a748...` / `cac2a748...`（相等） |
| Open PR count | 0 |
| MLB policy-page requests | 官方政策/robots/openapi 頁；count=6 次擷取（含 access-fail） |
| MLB data endpoint call count | **0** |
| DB/runtime/production mutation | NONE |
| Single blocker or NONE | **Blocker：決定性適用性引文誤標（§1 範圍條款被當「定義」）；次要：Copyright Agent 誤作 licensing 管道** |
| Whether governance update is allowed next | **NO（須先窄修 evidence packet）** |
| Whether packaging is allowed next | **NO（同上）** |
| Whether live implementation is allowed next | **NO** |
| Recommended next task | 受權之**窄修回合**：依 §16 三點僅修 `report/p202g_a_..._evidence_packet_20260614.md` 引用/管道措辭（不改決策、不碰 endpoint、HOLD 不變），完成後再 governance + packaging |
| Worker model | Opus 強 |
| Thinking level | 強 |
| Same/new conversation | 新回合（窄修為獨立受權動作） |
| Final Classification | `P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX` |

---

## Final Classification

**`P202G_A_POLICY_REREVIEW_NEEDS_REPORT_FIX`**

Evidence packet 的核心結論**全部正確且保守**：官方 MLB.com Terms of Use（2025-03-11）**明文
禁止** "use automated scripts to collect information from or otherwise interact with the MLB
Digital Properties"，binds all users；該限制經 §1「MLBAM 提供/散布之產品服務…are subject to this
Agreement」條款、正式定義「MLB-controlled products or services」與 openapi「Official API for
Major League Baseball.」（server=`statsapi.mlb.com`）共同支撐，**足以維持 live transport HOLD**；
one-shot 與 recurring 皆**不可**由現有證據自我授權；robots 解讀正確；retention/derived 映射忠實。

惟本輪對抗性重驗發現**兩處須窄修的報告層級瑕疵**：(1) packet 把 §1「are subject to this
Agreement」**範圍條款**誤標為「"MLB Digital Properties" 的**定義**」並截斷操作性結尾，致適用性
被寫成「直接/決定性」而非強支撐推論（statsapi 未被條款逐字點名）；(2) `legaldepartment@mlb.com`
（官方 **DMCA Copyright Agent**）被誇大為書面許可請求入口。兩者**不改變任何決策**、方向保守，
但在納入治理更新與 commit packaging 前應由**獨立受權之窄修回合**更正（§16）。本複審**未**修改
evidence packet、治理檔或任何原始碼，HEAD 不變、0 staged、0 MLB data endpoint 呼叫。
