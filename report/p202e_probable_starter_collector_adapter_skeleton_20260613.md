# P202E — Pregame Probable-Starter Collector Adapter Skeleton (FIXTURE-ONLY)

- **日期 (Date):** 2026-06-13 (Asia/Taipei)
- **任務類型:** Implementation（Template 3）— fixture-only / no-network adapter skeleton
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **Baseline HEAD:** `49b0991a388e286d48facb2081af23e543388d1b`（= origin/main；P202D PR#20 merge commit）
- **依據:** P202D 已合併之快照契約 `data/mlb_probable_starter_snapshots.py`（read-only 重用）；契約 `report/p202c_…20260612.md`。
- **性質:** 純標準函式庫；零網路、零外部相依；**注入式** transport / clock（無 default 實作）；不接 scheduler / recommendation / evaluator / model；不寫真實 runtime 資料（測試用 `tmp_path`）；P202D 模組**未修改**；永不 `learning_eligible`。

---

## 1. Governance Files Read Status

| 檔案 | 狀態 |
|------|------|
| `agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` / `TASK_TEMPLATES.md` / `CURRENT_STATE.md` | ✅ 已讀（Template 3） |
| `00-Plan/roadmap/active_task.md` | ✅ 已讀（仍 P199 `AUTHORIZED_PLAN_ONLY`；**陳舊**；不觸 STOP） |
| `00-Plan/roadmap/roadmap.md` / `CTO-Analysis.md` | ✅ 已讀（2026-06-11 `0L`/`0A`；phase 標籤落後實際 HEAD；未編輯） |
| `report/p202c_*` / `p202d_*`（intake skeleton + post-impl review） | ✅ 已讀（契約與 P202D 公開 API） |

**治理陳舊性（不修）：** `CURRENT_STATE.md` HEAD 基線記 `2a7aa13`（實際 `49b0991`）；`active_task.md` 仍 P199。以實際 repo/產物/GitHub 為真相。無衝突觸發 STOP。

---

## 2. Phase 0 Result

| 檢查 | 觀察 | 結果 |
|------|------|------|
| repo / branch / git-dir / symbolic-ref | `…/Betting-pool` / `main` / `.git` / `main`（非 detached） | ✅ |
| HEAD / origin/main | `49b0991` / `49b0991` | ✅ |
| P202D merge baseline `49b0991` ancestor | `P202D_MERGE_BASELINE_OK` | ✅ |
| P202D impl commit `b288b22` ancestor | `P202D_COMMIT_IN_MAIN_OK` | ✅ |
| PR #20 | MERGED · open PR 0 | ✅ |
| staged | 無 | ✅ |
| merged P202D 檔 | 皆 EXISTS | ✅ |
| 4 個 P202E 白名單檔 | 起始皆 MISSING（無既有檔衝突） | ✅ |
| dirty/untracked | tolerated runtime/data + 授權 governance + 未提交 P199/P202/P202B/P202C 報告 | ✅（白名單內） |

**無 STOP 觸發。**

---

## 3. Source-Boundary Inspection（Phase 1，read-only）

- `data/mlb_probable_starter_snapshots.py`（P202D）公開 API 足夠重用：`normalize_snapshot(raw, *, parser_version)`、`append_snapshot(snapshot, path)`、`SnapshotValidationError`、`SnapshotStoreError`、`ProbableStarterSnapshot`。**無需修改 P202D。**
- `data/mlb_player_stats.py::fetch_probable_starters`（`:502-530`，**未呼叫**）確立來源形狀：`schedule?hydrate=probablePitcher` → `data["dates"][].games[]`，每局含 `teams["home"/"away"]["team"]` 與 `["probablePitcher"]`。據此推得完整賽前形狀（`gamePk`/`gameDate`/`officialDate`/`doubleHeader`/`gameNumber`/`status.{abstractGameState,detailedState}`/`teams.{home,away}.{team.id, probablePitcher.{id,fullName}}}`）。
- 確認：標準函式庫足夠；新模組可與所有 production path 解耦；來源形狀**可由 repo source 確定**（無需 live API）。

---

## 4. Adapter Architecture（Phase 2）

新增 `data/mlb_probable_starter_collector.py`（純 stdlib：`logging/dataclasses/typing`；import P202D 公開符號）。

- **`adapt_schedule_payload(payload, *, collected_at_utc, information_cutoff_utc, source_provider, source_endpoint_or_feed_id, parser_version=COLLECTOR_PARSER_VERSION) -> CollectorResult`** — **純函式、零 I/O**：驗證頂層形狀 → 確定性逐 `dates[].games[]` 抽取 → 每局映射為 P202D raw → `normalize_snapshot` → 收集 accepted（normalized 快照）+ rejected（含 `source_ref` + `reason`）。per-game 問題→rejection（不丟失、不靜默）；僅 programmer error 上拋。
- Result：`CollectorResult{status(ok|source_unavailable|malformed_payload), accepted, rejected, accepted_count, rejected_count, partial_count, appended_count, duplicate_count}`；`RejectedRecord{source_ref, reason}`（皆 frozen dataclass）。

---

## 5. Injected Transport & Clock Contract（Phase 3）

**`collect_probable_starters(*, transport, request, source_provider, source_endpoint_or_feed_id, information_cutoff_utc, collected_at_utc=None, clock=None, parser_version=…, output_path=None) -> CollectorResult`**

- `transport` **必填、無 default、無網路庫**；只收 `request`，回 payload（或 `None` 表 source-unavailable）。
- collection 時刻：顯式 `collected_at_utc` 或注入 `clock()`；**無 default clock**（不隱式讀牆鐘）；兩者皆缺 → `ValueError`。
- transport 例外或回 `None` → 顯式 `source_unavailable` 診斷（非靜默）。
- 僅 `output_path` 顯式提供時才持久化（P202D append-only）；無 default 輸出路徑；不建 runtime 目錄；**無 retry/sleep/scheduling/daemon**。

---

## 6. Source-to-P202D Field Mapping（Phase 4）

| P202D 欄位 | 來源 / 規則 |
|------|------|
| `game_pk` | `game["gamePk"]`（必填 int，否則 reject `missing_game_pk`） |
| `scheduled_start_utc` | `game["gameDate"]`（必填；支援 `…Z`，P202D 正規化為 `+00:00`） |
| `official_game_date` | `game["officialDate"]`；缺則以 `gameDate[:10]` 確定性回退 |
| `doubleheader_game_number` | `doubleHeader∈{S,Y}` → `gameNumber`，否則 `0` |
| `home/away_team_id` | `teams[side]["team"]["id"]`（必填，否則 reject） |
| `home/away_probable_pitcher_id/name` | `teams[side]["probablePitcher"].{id,fullName}`（缺→None） |
| `home/away_pitcher_status` | 顯式 `probableStatus` hint；否則 id 有→`probable`，無→`tbd` |
| `game_status` | 由 `status.{detailedState,abstractGameState}` 映射（見 §9） |
| `collected_at_utc` / `information_cutoff_utc` | **caller context**（非 payload 賽後戳） |
| `source_record_id` | 確定性 `f"{game_pk}:{dh_no}"`（穩定 → exact-dup 冪等、revision 靠 collected/fingerprint） |
| `source_freshness_seconds` | `game["sourceFreshnessSeconds"]`（非負 int）否則 `0`（文件化語意） |
| `snapshot_status` | 由 P202D 依 game_status + pids 派生 |
| `diagnostic_only` / `production_ready` | P202D 強制 `True` / `False` |

---

## 7. Accepted & Rejected Diagnostics

- **Accepted**：通過 P202D 正規化之快照（順序＝來源順序，確定性）。`partial_count`＝`snapshot_status=="partial"` 數。
- **Rejected**（顯式 reason，永不靜默丟失）：`malformed_game_record` / `missing_game_pk` / `missing_scheduled_start` / `missing_{side}_team_id` / `missing_teams` / `missing_or_malformed_status` / `unknown_game_status` / `final_or_live_not_pregame` / `leakage_field_present: <key>` / `normalize_rejected: <P202D error>` / `malformed_date_entry`。
- **頂層**：非 dict → `malformed_payload`；缺 `dates` list → `malformed_payload`；`{"source_unavailable": true}` → `source_unavailable`。

---

## 8. Time & Identity Safety

- `collected_at_utc` / `information_cutoff_utc` 一律取自 **caller**，非 payload 賽後時間（測試 `test_caller_cutoff_used`）。
- P202D 強制 tz-aware UTC、`cutoff < scheduled_start`、`collected ≤ cutoff`；違反 → `normalize_rejected`（`test_cutoff_after_start_rejected` / `test_collected_after_cutoff_rejected`）。
- freshness 確定性（預設 0 或顯式整數；`test_freshness_default_zero_and_explicit`）。
- `game_pk` 必填且為 canonical 鍵；team id 缺/相同 → reject；date/team 組合**永不**替代 identity（`test_missing_team_id_rejected`、doubleheader 測試）。

---

## 9. Probable-Starter & Game-Status Behavior

- **Game-status 映射：** `Scheduled/Pre-Game/Preview/Warmup`→`scheduled`；`Postponed`→`postponed`；`Cancelled/Canceled`→`cancelled`；`Suspended`→`suspended`；含 `delayed`→`delayed`；`Final/Game Over/Completed Early/In Progress/Live` 或 `abstractGameState∈{Final,Live}` → **reject**（`final_or_live_not_pregame`）；未知 → **reject**（`unknown_game_status`）。
- **Pitcher-status：** `announced/probable/confirmed/changed/scratched/opener/bullpen_game/tbd/unavailable`（由 P202D enum 驗證）；changed/scratched/opener 經 `probableStatus` hint **surfaced**（`test_changed_and_scratched_statuses_surfaced`、`test_opener_status_surfaced_inline`）。
- **Partial：** 單缺→partial（`one_side_missing`）、雙缺→partial（`both_sides_tbd`），皆**接受並保存**（append-only 歷史），於 P202D 選擇期 fail-closed。
- **Postponed/Cancelled：** 接受並保存（snapshot_status 對應），選擇期永不 trusted。

---

## 10. Duplicate / Revision Handling

- adapt **不去重**（保留來源順序，含 payload 內重複局 → 兩筆相同指紋；`test_duplicate_in_payload_normalizes_twice`）。
- 去重/revision 由 P202D `append_snapshot` 決定：exact-dup（同 dedup key）→ no-op（`duplicate_count++`）；變更（starter/status/time/collected）→ revision append（`appended_count++`）。
- `test_exact_duplicate_in_payload_not_appended_twice`（accepted 2 → appended 1 / duplicate 1，檔案 1 行）；`test_revision_appends`（同 game 兩 revision → 2 行）。

---

## 11. Optional Persistence Behavior（Phase 6）

- 無 `output_path` → **零檔案寫入**（`test_no_output_path_means_no_write`，tmp 目錄空）。
- 顯式 `output_path`（tmp_path）→ 透過 P202D append；無 default 路徑、不建 runtime 目錄（`test_no_runtime_directory_created_during_persistence`）。
- malformed 既有 JSONL → **fail-closed**（`SnapshotStoreError` 上拋，檔案不變更；`test_malformed_existing_store_fails_closed`）。
- 部分成功不謊報全成功（`appended_count`/`duplicate_count` 分別計）。

---

## 12. No-Network Proof

- 模組 import 僅 `logging/dataclasses/typing` + P202D 公開符號——**無** `requests/httpx/socket/urllib/aiohttp/http.client/ssl`（`test_module_imports_and_is_stdlib_only`）。
- **無** `fetch_probable_starters` / `statsapi.mlb.com` / scheduler / recommendation / evaluator / `learning_eligible` / `time.sleep` / `while True` / `threading` 之**程式碼**引用（`test_no_fetch_probable_starters_or_integration_imports`、`test_no_scheduler_recommendation_evaluator_imports`；以去除 docstring/註解後的 code-only 掃描——唯一出現處為 docstring 之「不使用」聲明）。
- import 零副作用、不建 runtime 路徑（`test_import_creates_no_runtime_path`）；adapt 純函式不碰檔案系統；唯一 I/O＝顯式 `output_path` 之 P202D append。
- 傳輸為**注入式**：真實 HTTP transport 與採集授權為**獨立未來任務**（本任務未含）。

---

## 13. Fixture Inventory（`tests/fixtures/mlb_probable_starter_source_payload_fixtures.json`）

`schema_version=p202e_source_payload_fixture_v1`；全合成（team `90xx`、pitcher `8000xx`/`8001xx`/`8002xx`、gamePk `99xxxx`、年份 2099、provider `fixture_synthetic_schedule`）；無 copied live payload、無 secret/token、無官方授權聲明。19 情境：`valid_scheduled_both`、`starter_change`、`scratched_starter`、`one_side_missing`、`both_sides_tbd`、`doubleheader_game_1`/`_2`、`delayed_game`、`postponed_game`、`cancelled_game`、`source_unavailable`、`malformed_top_level`、`malformed_game_record`、`missing_game_pk`、`missing_scheduled_start`、`duplicate_game_record`、`completed_final_game`、`actual_starter_markers`、`multi_game_mixed`。transport-exception 情境由測試之 fake transport 表示（非 payload 資料）。

---

## 14. Tests Run（Phase 8）

| 指令 | 結果 |
|------|------|
| `pytest tests/test_mlb_probable_starter_collector.py -q` | **49 passed** |
| `pytest tests/test_mlb_probable_starter_snapshot_intake.py -q`（P202D 回歸） | **89 passed** |
| 合併工作流護欄 5 檔 | **157 passed** |
| 合併相關 7 套件（collector + intake + 5 workflow） | **295 passed** |
| `py_compile`（collector + snapshots） | **COMPILE_OK** |
| 邊界掃描（network/integration） | code-level 無；唯一命中為 docstring「不使用」聲明 |

涵蓋 A.import/boundary、B.parsing、C.probable-mapping、D.game-status、E.time-safety、F.doubleheader/revision、G.injected-transport、H.persistence、I.integration-guards 全部 9 組。
> 本輪未遇 `test_*_active_task_updated` 治理陳舊失敗（不在驗證集／不在 scope）。

**Test result：PASS。**

---

## 15. Full Regression Status

**NOT RUN（全庫）。** 新模組純新增、與產線解耦、P202D 未改；跑直接套件（49）+ P202D 回歸（89）+ 工作流護欄（157）對風險成比例。

---

## 16. Known Limitations

1. **Fixture-only / 無真實採集：** 不含真實 HTTP transport；真實採集與網路授權為**獨立未來任務**（仍 UNKNOWN）。
2. **Pitcher-status 粒度：** 基本 schedule 僅給 probable/缺；`changed/scratched/opener/bullpen_game` 經合成 `probableStatus` hint 模擬——真實來源需更豐富 feed 或事件。
3. **Freshness：** 預設 0 或顯式整數；真實 collector 應由 provider 更新時戳計算。
4. **`official_game_date` 回退：** 缺漏時以 UTC 日回退，可能與聯盟 local 日差一日（在 P202D ±1 日容忍內）。
5. **未接產線：** 選擇/採集輸出皆 diagnostic-only，未接 scheduler/recommendation/evaluator。
6. **逐場投手事件契約（P202C §5，候選 B）仍未實作。**

---

## 17. Explicit Non-Actions

未呼叫任何網路/live MLB API/付費 API；未實作真實 HTTP transport；未呼叫 `fetch_probable_starters`；未接 scheduler/recommendation/evaluator/model；未寫真實 runtime 資料（`data/mlb_probable_starters` 未建立）；測試全用 `tmp_path`；無 model fit/feature/learning_eligible；無 DB/provider unlock/production/registry/controlled_apply/strategy·champion mutation；未新增第三方相依；未改 package/config/CI；**未修改 P202D 模組**或 `data/mlb_player_stats.py`、`data/mlb_sp_data_loader.py`、scheduler、recommendation、evaluator 或任何既有測試；未編輯 governance；未 branch/checkout/commit/push/PR/merge/rebase/reset/stash/clean/delete；未 stage/`git add`；未碰 tolerated dirty 檔。**僅建立 4 個白名單檔。**

---

## 18. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — adapter + injected transport/clock + 映射 + 診斷 + optional persistence 完成；49 + 89 + 157 全綠 |
| Test result | **PASS** |
| P202E direct test count | **49** |
| P202D regression test count | **89** |
| Workflow test count | **157** |
| Combined relevant test count | **295** |
| Full regression | **NOT RUN** |
| Source payload contract status | ✅（依 repo source 確定的 schedule 形狀；全合成） |
| Adapter mapping status | ✅（22 contract 欄位映射 + 確定性抽取） |
| Injected transport status | ✅（必填、無 default、無網路庫；例外→source_unavailable） |
| Injected clock/cutoff status | ✅（顯式或注入 clock；無 default clock；cutoff 取自 caller） |
| Probable-starter status mapping | ✅（probable/tbd 派生 + changed/scratched/opener surfaced） |
| Game-status mapping | ✅（scheduled/delayed/postponed/cancelled/suspended；final/live + unknown → reject） |
| Duplicate/idempotency status | ✅（P202D dedup；exact-dup no-op） |
| Revision-history status | ✅（變更→append；歷史保留） |
| Optional persistence status | ✅（無 path→不寫；tmp_path→append；malformed→fail-closed） |
| Actual-starter substitution prevention status | ✅（遞迴 leakage 掃描 + final/live 拒絕 + provider-marker 繼承 P202D） |
| No-network status | ✅（無網路 import；import 零副作用；adapt 不碰 FS） |
| Real runtime data write status | 無（僅 tmp_path；`data/mlb_probable_starters` 不存在） |
| Single remaining blocker | live transport + 網路採集授權（獨立未來任務，UNKNOWN） |
| Selected next task recommendation | **P202F**：真實 HTTP transport + 採集授權（需網路授權）／或候選 B 逐場投手事件 backfill skeleton |
| Modified files | 無（僅 tolerated/governance dirty，非本任務所改） |
| Untracked files（本任務新增） | `data/mlb_probable_starter_collector.py`、`tests/test_mlb_probable_starter_collector.py`、`tests/fixtures/mlb_probable_starter_source_payload_fixtures.json`、`report/p202e_probable_starter_collector_adapter_skeleton_20260613.md`（另有既有未提交 `agent_bootstrap/`、P199/P202/P202B/P202C 報告） |
| Staged files | 無 |
| Current branch / Local HEAD / origin/main HEAD | `main` / `49b0991` / `49b0991` |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199；未修改；陳舊） |
| DB / network·API / provider unlock | 無 / 無 / 無 |
| production / registry / controlled_apply mutation | 無 / 無 / 無 |
| model / strategy / champion mutation | 無 / 無 / 無 |
| commit / push status | 無 / 無 |
| 下一輪是否允許 | ✅ 允許（P202E commit packaging 需獨立授權；或 P202F／候選 B） |
| Worker model 建議 | Opus 強 |
| Thinking level 建議 | 中到強 |
| 是否續用同一對話 | 建議新一輪對話（重跑 Phase 0） |

---

## Final Classification

**`P202E_COLLECTOR_ADAPTER_SKELETON_COMPLETE`**

> 已在 P202D 可信快照契約之上實作 fixture-only、no-network 的 probable-starter collector adapter（`data/mlb_probable_starter_collector.py`）：純函式 `adapt_schedule_payload` 將合成 schedule payload 確定性映射為 P202D 正規化快照並回報 accepted/rejected 診斷；`collect_probable_starters` 以**注入式 transport/clock**（無 default、無網路庫）編排，transport 例外/None→source_unavailable，並僅在顯式 `output_path` 下透過 P202D append-only 持久化（exact-dup 冪等、revision 追加、malformed fail-closed）。賽後/完賽局與 actual/as-played 欄位一律拒絕；caller 提供 cutoff/collected；`game_pk` 為 canonical 鍵。49 直接 + 89 P202D 回歸 + 157 工作流 = 295 測試全綠；恰好 4 個白名單檔；P202D 模組未修改；零真實 runtime 寫入；P200/P201 與 P202D 契約完整保留（永不 learning_eligible）。唯一剩餘 blocker＝真實 transport + 網路採集授權（獨立未來任務）。
