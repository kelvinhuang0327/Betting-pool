# P202D — Post-Implementation Review & Commit-Readiness Audit

- **日期 (Date):** 2026-06-13 (Asia/Taipei)
- **任務類型:** Read-Only Review（Template 2，paper-only / offline）
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **Baseline HEAD:** `539bca205e420396962e4b32093dbe59030c7ef1`（= origin/main；P201 merge commit）
- **審查標的:** P202D 本地實作（未提交）4 檔，依 `report/p202d_…20260613.md` 與契約 `report/p202c_…20260612.md`。
- **性質:** 唯讀；**未修改** P202D 任何 source/test/fixture/report；未 stage/commit/push/PR；零網路；測試寫入僅 pytest `tmp_path`。唯一寫入＝本審查報告。

---

## 1. Governance Files Read Status

| 檔案 | 狀態 |
|------|------|
| `agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` / `TASK_TEMPLATES.md` / `CURRENT_STATE.md` | ✅ 已讀（Template 2 read-only review） |
| `00-Plan/roadmap/active_task.md` | ✅ 已讀（仍 P199 `AUTHORIZED_PLAN_ONLY`；**陳舊**；未授權其他 implementation → 不觸 STOP） |
| `00-Plan/roadmap/roadmap.md` / `CTO-Analysis.md` | ✅ 已讀（2026-06-11 `0L`/`0A`；phase 標籤落後 HEAD；未編輯） |
| `report/p202_* / p202b_* / p202c_* / p202d_*` | ✅ 已讀（契約與實作報告比對） |

**治理陳舊性（不修）：** `CURRENT_STATE.md` HEAD 記 `2a7aa13`（應 `539bca2`）；`active_task.md` 仍 P199。以實際 repo/產物/GitHub 為真相。無衝突觸發 STOP。

---

## 2. Phase 0 Result

| 檢查 | 觀察 | 結果 |
|------|------|------|
| repo / branch / git-dir / symbolic-ref | `…/Betting-pool` / `main` / `.git` / `main`（非 detached） | ✅ |
| HEAD / origin/main | `539bca2` / `539bca2` | ✅ |
| baseline ancestor | `BASELINE_ANCESTOR_OK` | ✅ |
| PR #19 | MERGED（`2026-06-12T05:18:18Z`） | ✅ |
| open PR / staged | 0 / 無 | ✅ |
| 4 個 P202D 檔 | 皆 EXISTS 且 untracked（未提交） | ✅ |
| dirty/untracked | tolerated runtime/data + 授權 governance + 未提交 P199/P202/P202B/P202C 報告 + 4 個 P202D 檔 | ✅（白名單內） |

**無 STOP 觸發。** P202D 檔為 untracked，已**直接完整閱讀**（不靠 git diff 推斷）。

---

## 3. Dirty / Untracked / Staged Status

- **Staged：** 無。
- **Modified（tracked）：** 僅 tolerated runtime/data（10 檔）+ 授權 CTO governance（3 檔）—— 皆既有 dirty，**非本審查或 P202D 所改**。
- **Untracked：** `00-Plan/roadmap/agent_bootstrap/`、未提交報告 P199/P202/P202B/P202C、**4 個 P202D 檔**（＋本審查報告）。
- **副作用驗證（Phase 10）：** 跑測試前後 `git status --short` **完全一致**（NO_STATUS_CHANGE）；HEAD 未變；`data/mlb_probable_starters` 不存在；無 stray jsonl。

---

## 4. P202D Implementation Review Summary（Full File Inspection）

四檔逐一完整閱讀；`py_compile` 通過。

- **`data/mlb_probable_starter_snapshots.py`（純 stdlib）：** imports 僅 `hashlib/json/logging/os/dataclasses/datetime/typing`。**無** `requests/httpx/socket/urllib/aiohttp/http.client/ssl`；**未** import/呼叫 `mlb_live_pipeline`/`fetch_probable_starters`/`fetch_schedule`/scheduler/evaluator/recommendation。grep 唯一命中 `statsapi` 之處為 **docstring 註解**（聲明「不呼叫」），非 import/call。無第三方相依。
- **寫入路徑：** `open()` 僅出現於 `load_snapshots(path)`（`"r"`）與 `append_snapshot(snapshot, path)`（`"a"`），路徑皆 `os.fspath(caller_path)`；**無 default 寫入路徑**；import 無 I/O 副作用；`CANONICAL_RUNTIME_OUTPUT_PATH_HINT` 為純文件常數（import 後該路徑確認不存在）。
- **`tests/…intake.py`：** 89 測試；全用 `tmp_path`/`monkeypatch.chdir`。
- **`tests/fixtures/…json`：** 18 個全合成 fixture。
- **報告 `report/p202d_…md`：** 宣稱（4 檔範圍、89+157=246、no-network、append-only、leakage 防護、source_freshness 調和為非負）與實作/測試**逐項相符**。

---

## 5. Schema / Timestamp Result

**Schema（Phase 2）：** `ProbableStarterSnapshot` 為 `@dataclass(frozen=True)`，**恰好 25 欄**＝P202C §4（測試 `test_normalized_record_has_exactly_contract_fields` 斷言精確集合，通過）。
- `diagnostic_only` 強制 True、`production_ready` 強制 False（`test_diagnostic_invariants_forced_and_claims_rejected`）。
- `learning_eligible` 出現即拒絕；actual-starter / score / result / winner / outcome / box_score 欄位拒絕（`_reject_forbidden`；`test_postgame_and_actual_fields_rejected` 8 參數）。
- enum 明確且 deterministic（`PITCHER_STATUS_VALUES`/`GAME_STATUS_VALUES`/`SNAPSHOT_STATUS_VALUES`；測試斷言集合）。
- **未知非禁用欄位被忽略（不入正規化），不靜默改變語意；** 故禁用集不過廣（合法 metadata 不誤殺，僅 outcome/actual 名稱被拒）。

**Timestamp / Identity（Phase 3）：** tz-aware UTC 強制；naive 拒絕；非零 offset 拒絕；`cutoff < scheduled_start`；`collected ≤ cutoff`；`source_freshness_seconds` 非負；`official_game_date` 與排定日 ≤1 日；`game_pk` 必填且為 canonical join 鍵；`home_team_id != away_team_id`；`doubleheader_game_number ∈ 0..2`（拒 bool/str/float）；date/team 組合永不替代 identity。
- **P202C→P202D 語意變更審查：** `source_freshness_seconds` 由 P202C 的「-1 表不可得」改為 **prompt 強制非負**。此 override **明確、內部一致**：缺/負值即 fail-closed，**不會**把「未知 freshness」偽裝成「可信新鮮度」——freshness 不參與 trust 判定（trust 僅看 cutoff/staleness/雙邊狀態），故非負化不造成誤信。**通過。**

---

## 6. Append-Only / Idempotency / Revision Result

- **Append-only：** 採**純物理 append（`open(path,"a")` 寫單行）**——既有行逐字不動（測試 `test_revision_appends_and_preserves_prior` 斷言 `content.startswith(first_line)`）。parent dir 必須先存在（`test_append_parent_dir_must_exist`）；malformed 既有檔 → `SnapshotStoreError` 且**檔案不變更**（`test_malformed_existing_store_fails_closed_without_alteration` 斷言前後 byte 相同）。
- **Idempotency：** dedup key `(provider, record_id, game_pk, dh, collected_at, fingerprint)`；exact duplicate no-op（`test_append_new_then_idempotent_duplicate`，檔案維持 1 行）。
- **Revision：** 變更 starter/status/time/collected → 不同 key → 追加（`test_dedup_key_distinguishes_revision_from_duplicate`）；歷史保留。
- **Fingerprint（Phase 4）：** `"sha256:"+sha256(canonical sort_keys JSON)`，**key-order 無關**（`test_fingerprint_is_key_order_independent`）、實質欄位變動即變（`test_fingerprint_changes_with_substantive_change`）、加密雜湊、有 `sha256:` 前綴；**不**遞迴納入 caller fingerprint（fingerprint 由正規化欄位重算，非沿用輸入）。決定性（不依賴 `hash()`）。

---

## 7. Selection / Fail-Closed Result（Phase 6）

- 比對 `game_pk` **且** `doubleheader_game_number`（dh 錯 → `no_matching_game`；`test_doubleheader_games_remain_independent`）。
- 排除 `collected_at > target_cutoff`（post-cutoff 永不入選；`test_post_cutoff_update_excluded_for_earlier_cutoff`、`test_postgame_collected_update_not_selected_for_pregame_cutoff`）。
- 排除 cancelled/postponed/source_unavailable/malformed/superseded；最新終態 surfaced（`test_cancelled_never_trusted`）。
- caller-supplied `stale_max_seconds`/`min_lead_seconds`（無隱藏生產門檻；負/非數 → fail-closed `test_selection_requires_caller_thresholds`）。
- fail-closed：`stale`/`one_side_missing`/`both_sides_tbd`/`insufficient_lead_time`/`cutoff_after_start` 皆顯式 reason。
- surfaced 而非隱藏：`changed`/`scratched`/`opener_bullpen`/`tbd`/`unavailable`（`test_changed_starter_surfaced`/`test_scratched_surfaced`/`test_opener_surfaced`）。
- **trusted** 僅當雙邊狀態 ∈ {announced/probable/confirmed} 且雙邊 pitcher_id 齊備。
- **改期/postponement 不混版本：** `test_postponement_history_surfaced_not_mixed` 驗證早 cutoff→原 schedule trusted、marker 期間→`postponed` surfaced、改期後→新 schedule trusted；每次只回**單一**快照（不混不同 scheduled_start）。
- **永不替換實際先發：** 選擇僅源自既存快照，而既存快照依建構不含 actual starter。

---

## 8. Leakage & No-Network Result（Phase 7）

- actual/as-played 欄位＋provider marker（`asplayed/as_played/actual/postgame`）拒絕（`test_actual_starter_substitution_rejected`/`test_asplayed_provider_rejected`）。
- score/winner/outcome/box_score 拒絕；`learning_eligible` 拒絕；正規化 schema 結構無 outcome/actual 欄位（`test_normalized_schema_has_no_outcome_or_actual_fields`）。
- postgame 更新無法影響較早 cutoff（已測）。
- fixture 明顯合成（年份 2099、team `90xx`、pitcher `8000xx`、provider `fixture_synthetic`）；**無** copied live payload、**無** secret/token（`test_fixture_file_is_synthetic_and_complete` 掃描 fixtures 資料）。
- **No-network：** 公開函式無網路路徑（`test_module_has_no_network_imports`）；import 零副作用、無 runtime 檔（`test_module_import_creates_no_runtime_file`）；normalize/select 不碰檔案系統（`test_normalize_and_select_touch_no_filesystem`）。
- **未碰** scheduler/recommendation/evaluator；**P200 fail-closed 與 P201 learning-eligibility 契約完整未動。**

---

## 9. Test-Quality Result（Phase 8）

- 89 測試含實質斷言（非湊行數）、正/負路徑兼具、決定性。
- 覆蓋 malformed JSONL 保存、exact-dup no-op、revision append、時間戳邊界、stale/min-lead 邊界、doubleheader 分離、改期/postponement、cancellation、單缺/雙 TBD、opener/bullpen、actual-starter 拒絕、no-network/import 副作用、no-default-path。
- 報告宣稱皆有對應測試覆蓋；無「條件式可空轉通過」之斷言；參數化（required-field、postgame-field、provider-marker、bad-threshold）擴大負路徑。
- **未見**冗餘充數測試或僅耦合實作細節之脆弱斷言（門檻測試以行為而非內部變數斷言）。

---

## 10. Test Results（Phase 9，獨立重跑）

| 指令 | 結果 |
|------|------|
| `pytest tests/test_mlb_probable_starter_snapshot_intake.py -q` | **89 passed** |
| 合併工作流護欄 5 檔 | **157 passed** |
| 合計觀測 | **246 passed** |
| 靜態：`py_compile`（module + test） | **COMPILE_OK** |
| 靜態：network/integration import 掃描 | 唯一命中＝docstring 註解；**無**真實 import/call |

**Test result：PASS。** 與 P202D 報告宣稱（89 / 157 / 246）**完全相符**。

---

## 11. Full Regression Status

**NOT RUN（全庫）。** 審查唯讀；新模組與產線完全解耦（純新增、零既有檔改動），跑直接套件＋成比例工作流護欄即足。

---

## 12. Side-Effect Verification（Phase 10）

- 測試前後 `git status --short` **完全一致**（NO_STATUS_CHANGE）。
- staged 無；HEAD 維持 `539bca2`。
- `data/mlb_probable_starters` **不存在**；無 stray jsonl；測試僅寫 `tmp_path`。
- 可歸因於 P202D 之檔案＝原 4 檔（＋本審查報告）；審查期間無任何 source/test/fixture 變更。

---

## 13. Risks & Limitations（誠實揭露；皆非 blocker）

1. **物理 in-place append（非 tmp→rename 原子替換）：** P202C §11 曾提議 `atomic-write: tmp→rename`，實作改採 `"a"` 模式。**邏輯 append-only** 且既有 byte 不動（較 rewrite 更不易損壞歷史），torn/partial write → 下次 `load_snapshots` fail-closed（不靜默使用）。**未宣稱**並發安全、無檔案鎖——符合 prompt Phase 5 對 fixture-only skeleton 的明確許可。**建議 P202E live collector 改用 tmp→rename + 鎖**。
2. **fingerprint / dedup key 排除 `source_freshness_seconds` 與 `parser_version`：** 兩列若僅 freshness 或 parser_version 不同會被視為重複（不追加）。freshness 為派生 metadata、parser 對相同輸入重跑刻意冪等——可接受並已隱含文件化；惟若日後需「parser 版本感知再吸收」，應將 `parser_version` 納入 dedup key。
3. **選擇排序依賴 canonical isoformat 字串字典序：** 因 normalize 強制 `+00:00` ISO，字典序＝時間序成立；正確但依賴該不變式（cutoff 比較另以 `_parse_utc` 重解析，較穩）。
4. **`snapshot_status` 僅顯式 honor `source_unavailable`：** 其他顯式值（如誤傳 `superseded`/`stale`/`malformed`）會被靜默改為 derived。因 stale/superseded 為選擇期概念、malformed 為拒絕期概念，永不入存，行為一致；惟「靜默忽略顯式值」可考慮改為拒絕以更明確。
5. **`test_module_import_creates_no_runtime_file` 用 CWD 相對路徑：** 於 repo 根目錄成立；若日後 P202E 真建該目錄，此測試需調整——屬輕微脆弱，現階段無誤。
6. **Skeleton 本質：** 不採集真實資料；賽前證據之實際累積仍待獨立授權之 live collector（P202E）；逐場投手事件 SSOT（P202C §5，候選 B）尚未實作。

以上 1–5 為設計/測試觀察，**均不影響正確性與安全邊界**，且多數已於 P202D 報告誠實揭露；6 為已知範圍限制。

---

## 14. Commit-Readiness Decision（Phase 11）

**`READY_FOR_COMMIT_PACKAGING`。**

達標項：
- ✅ 恰好 4 檔範圍（無溢出；審查未改任何 P202D 檔）。
- ✅ 直接（89）＋工作流（157）測試全綠；合計 246。
- ✅ 零持久測試副作用（git status 前後一致；無真實 runtime 檔）。
- ✅ 無網路路徑；無第三方相依；無 scheduler/recommendation/evaluator 整合。
- ✅ schema 與時間戳契約一致（freshness 非負 override 明確且不誤信）。
- ✅ append-only / idempotency / revision 正確。
- ✅ actual-starter 替換多重拒絕。
- ✅ 無 production-readiness 過度宣稱（diagnostic_only 強制；報告誠實揭露限制）。
- ✅ P200/P201 契約未動。

§13 之觀察為非阻斷之改進建議，**不要求**於本次 commit 前修正。

---

## 15. 是否允許 packaging：**允許**

- 可進入 commit packaging（須在**獨立授權**下執行 stage/commit/push/PR——本審查與 P202D 皆未獲此授權，故未執行）。
- 建議 commit 範圍恰為 4 檔（＋可選兩份報告 p202d 實作報告與本審查報告），**不得** stage 任何 tolerated runtime/data 或 governance 檔。
- 建議 conventional commit（繁中）：`feat(P202D): fixture-only pregame probable-starter snapshot intake skeleton`。

---

## 16. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — 12 階段審查完成；獨立重跑 246；副作用零；決策＝READY |
| Test result | **PASS** |
| P202D direct test count | **89** |
| Workflow test count | **157** |
| Full regression | **NOT RUN** |
| Commit readiness classification | **READY_FOR_COMMIT_PACKAGING** |
| Schema contract status | ✅ 25 欄 = P202C §4（test-proven） |
| Timestamp safety status | ✅（tz-aware UTC、cutoff<start、collected≤cutoff、freshness 非負 override 一致） |
| Append-only status | ✅（物理 append、既有行不動、malformed fail-closed；非原子替換，已揭露） |
| Idempotency status | ✅（exact-dup no-op） |
| Revision-history status | ✅（變更追加、歷史保留） |
| Selection/fail-closed status | ✅（caller 門檻、surfaced 特殊狀態、改期不混版本、永不替換實際先發） |
| Leakage-prevention status | ✅（actual/as-played/outcome/learning_eligible 拒絕，多測試覆蓋） |
| No-network status | ✅（無網路 import；import 零副作用；normalize/select 不碰檔案系統） |
| Persistent runtime-write status | 無（僅 tmp_path；`data/mlb_probable_starters` 不存在） |
| Single remaining blocker | **NONE** |
| Modified files | 無（僅 tolerated/governance dirty，非本任務所改） |
| Untracked files | `agent_bootstrap/`、P199/P202/P202B/P202C 報告、4 個 P202D 檔、本審查報告 |
| Staged files | 無 |
| Current branch / Local HEAD / origin/main HEAD | `main` / `539bca2` / `539bca2` |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199；未修改；陳舊） |
| DB write / network·API / provider unlock | 無 / 無 / 無 |
| production / registry / controlled_apply mutation | 無 / 無 / 無 |
| model / strategy / champion mutation | 無 / 無 / 無 |
| commit / push status | 無 / 無 |
| 下一輪是否允許 | ✅ 允許（commit packaging 需獨立授權；或 P202E live collector／候選 B skeleton） |
| Worker model 建議 | Opus 強 |
| Thinking level 建議 | 中到強 |
| 是否續用同一對話 | 建議新一輪對話（重跑 Phase 0） |

---

## Final Classification

**`P202D_POST_IMPLEMENTATION_REVIEW_READY_FOR_COMMIT_PACKAGING`**

> P202D 實作經獨立審查通過：恰好 4 檔範圍、89 直接 + 157 工作流 = 246 測試全綠、零持久副作用、零網路、schema/時間戳/identity 契約一致、append-only（物理 append、malformed fail-closed）、指紋冪等、revision 保留、canonical selection fail-closed 且 surfaced 特殊狀態、actual-starter 替換多重拒絕、P200/P201 契約未動、限制誠實揭露。單一 blocker＝NONE。§13 之觀察（append 非原子替換、freshness/parser 不入 dedup key 等）為非阻斷改進建議，多數已於實作報告揭露；建議於 P202E live collector 採 tmp→rename + 鎖。可進入 commit packaging（需獨立授權執行 stage/commit/push/PR）。

---

### CTO 結論（≤5 句）
P202D 以恰好 4 檔、純 stdlib、零網路、零真實寫入交付賽前 probable-starter 快照 intake skeleton，89+157=246 測試全綠且審查前後 git 狀態零變動，HEAD 維持 `539bca2`。schema（25 欄）、時間戳安全、identity（gamePk+dh）、指紋冪等、append-only revision、canonical fail-closed selection 與 actual-starter 多重拒絕皆經獨立測試證實，P200/P201 契約未動。唯一語意 override（`source_freshness_seconds` 非負）明確且不誤信。非阻斷觀察：物理 append 非 tmp→rename 原子替換、freshness/parser 不入 dedup key——適用於 fixture-only skeleton，建議於 live collector（P202E）強化。判定 **READY_FOR_COMMIT_PACKAGING，single blocker = NONE**；commit/push 須另行授權。

### CEO 結論（≤5 句）
這是一塊「打地基」的程式碼：它只在測試環境演練如何**正確、不可竄改地保存賽前先發投手公告**，完全不連網、不下注、不碰現有任何流程，風險為零。獨立複查確認它做到了關鍵承諾——賽後資料無法偽裝成賽前資訊、重複資料不會灌水、每次變更都留下完整歷史，且既有安全防線毫髮無傷。它已可被打包提交（需你另行授權正式 commit）。真正能開始累積「真資料」的下一步，是經授權的線上採集（P202E）——因為賽前公告錯過就補不回來，愈早上線愈好。建議照節奏推進，並維持 paper-only、不解鎖任何下注或外部供應商。
