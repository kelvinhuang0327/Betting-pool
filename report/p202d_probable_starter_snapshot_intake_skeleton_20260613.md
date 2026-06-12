# P202D — Pregame Probable-Starter Snapshot Intake Skeleton (FIXTURE-ONLY)

- **日期 (Date):** 2026-06-13 (Asia/Taipei)
- **任務類型:** Implementation（Template 3）— fixture-only / no-network / append-only skeleton
- **Repo:** `/Users/kelvin/Kelvin-WorkSpace/Betting-pool` · **Branch:** `main`
- **Baseline HEAD:** `539bca205e420396962e4b32093dbe59030c7ef1`（= origin/main；P201 merge commit）
- **依據契約:** `report/p202c_point_in_time_pitcher_data_gap_evidence_contract_20260612.md`（§4 schema／§8 規則／§9 leakage）
- **性質:** 純標準函式庫；零網路、零外部相依、零真實 runtime 資料寫入；所有寫入測試用 `tmp_path`。未連接 scheduler / recommendation / evaluator；未標任何 `learning_eligible`；P200/P201 fail-closed 邊界完整保留。

---

## 1. Governance Files Read Status

| 檔案 | 狀態 |
|------|------|
| `agent_bootstrap/SHARED_AGENT_BOOTSTRAP.md` / `TASK_TEMPLATES.md` / `CURRENT_STATE.md` | ✅ 已讀（套用 Template 3 Implementation） |
| `00-Plan/roadmap/active_task.md` | ✅ 已讀（仍 P199 `AUTHORIZED_PLAN_ONLY`；**陳舊**；非 implementation 授權 → 不觸 STOP） |
| `00-Plan/roadmap/roadmap.md` / `CTO-Analysis.md` | ✅ 已讀（2026-06-11 `0L`/`0A`；phase 標籤落後實際 HEAD；未編輯） |
| `report/p199_* / p200_* / p201_* / p202_* / p202b_* / p202c_*` | ✅ 已讀／背景掌握 |

**治理陳舊性（不修）：** `CURRENT_STATE.md` HEAD 記 `2a7aa13`（應 `539bca2`）；`active_task.md` 仍 P199。以實際 repo/產物/GitHub 為真相。無衝突觸發 STOP。

---

## 2. Phase 0 Result

| 檢查 | 觀察 | 結果 |
|------|------|------|
| repo / branch / git-dir / symbolic-ref | `…/Betting-pool` / `main` / `.git` / `main`（非 detached） | ✅ |
| HEAD / origin/main | `539bca2` / `539bca2` | ✅ |
| P201 ancestor | `P201_BASELINE_ANCESTOR_OK` | ✅ |
| PR #19 | MERGED（`2026-06-12T05:18:18Z`） | ✅ |
| open PR / staged | 0 / 無 | ✅ |
| P202 / P202B / P202C 報告 | 皆 EXISTS | ✅ |
| 4 個 P202D 白名單檔 | 起始皆 MISSING（無既有檔衝突） | ✅ |
| dirty/untracked | tolerated runtime/data + 授權 CTO governance + 未提交 P199/P202/P202B/P202C 報告 | ✅（白名單內） |

**無 STOP 觸發。**

---

## 3. Files Inspected（read-only）

- `report/p202c_…20260612.md`（契約 §4/§8/§9）。
- `data/mlb_player_stats.py`（確認 `fetch_probable_starters` live helper **未**被本模組引用；本模組零網路）。
- `data/mlb_sp_data_loader.py`（as-played relabel 反面教材 → 本模組明禁）。
- Repo 慣例：atomic write `os.replace`（`wbc_backend/mlb_data/tsl_market_availability_monitor.py:136`、`orchestrator/copilot_daemon.py`）、fingerprint `"sha256:"+hashlib.sha256().hexdigest()`（`data/mlb_sp_data_loader.py:74`、`data/mlb_bullpen_usage_loader.py:118`）、canonical JSON `sort_keys=True`（`wbc_backend/reporting/strategy_replay_backfill_apply.py:224`）、模組風格 hard-constants + dataclass + forbidden-field frozenset（`wbc_backend/features/mlb_relief_appearance_parser.py`）。
- 既有 tmp_path 測試慣例（pytest）。
- 確認標準函式庫足夠；**未新增任何第三方相依**。

---

## 4. Implementation Summary

新增模組 `data/mlb_probable_starter_snapshots.py`（純 stdlib：`json/hashlib/os/datetime/dataclasses/logging/typing`）。公開 API：

| 函式 | 角色 |
|------|------|
| `normalize_snapshot(raw, *, parser_version=PARSER_VERSION) -> ProbableStarterSnapshot` | 驗證 + 正規化（fail-closed），強制 `diagnostic_only=True`、`production_ready=False` |
| `compute_payload_fingerprint(canonical_fields) -> str` | canonical（sort_keys）JSON 之 `sha256:` 指紋 |
| `snapshot_dedup_key(record) -> tuple` | 冪等去重鍵（含 provider/record/game_pk/dh/collected/fingerprint） |
| `load_snapshots(path) -> list[dict]` | 讀 JSONL，malformed → fail-closed（不更動檔案） |
| `append_snapshot(snapshot, path) -> AppendResult` | append-only、冪等；`path` 無預設 |
| `select_canonical_snapshot(...) -> SelectionResult` | 純函式選擇；diagnostic-only；fail-closed + 顯式 reason |

Hard constants：`DIAGNOSTIC_ONLY=True`、`PRODUCTION_READY=False`、`CONTRACT_VERSION="p202c_probable_starter_snapshot_v1"`、`PARSER_VERSION="p202d_probable_snapshot_parser_v1"`。`CANONICAL_RUNTIME_OUTPUT_PATH_HINT`（`data/mlb_probable_starters/probable_starter_snapshots.jsonl`）為**純文件用途常數**，模組與測試**絕不寫入**；`append_snapshot` **無 default path**。

---

## 5. Exact Normalized Snapshot Schema（25 欄；P202C §4）

`ProbableStarterSnapshot`（`@dataclass(frozen=True)`）：
`contract_version`(str), `source_provider`(str), `source_endpoint_or_feed_id`(str), `source_record_id`(str), `payload_fingerprint`(str), `collected_at_utc`(ISO UTC), `information_cutoff_utc`(ISO UTC), `game_pk`(int), `scheduled_start_utc`(ISO UTC), `official_game_date`(YYYY-MM-DD), `doubleheader_game_number`(int 0..2), `home_team_id`(int), `away_team_id`(int), `home_probable_pitcher_id`(int|None), `home_probable_pitcher_name`(str|None), `away_probable_pitcher_id`(int|None), `away_probable_pitcher_name`(str|None), `home_pitcher_status`(enum), `away_pitcher_status`(enum), `game_status`(enum), `snapshot_status`(enum), `source_freshness_seconds`(int≥0), `parser_version`(str), `diagnostic_only`(=True), `production_ready`(=False)。

- **pitcher_status enum:** `announced/probable/confirmed/changed/scratched/opener/bullpen_game/tbd/unavailable`
- **game_status enum:** `scheduled/postponed/cancelled/delayed/suspended`
- **snapshot_status enum:** `valid/partial/stale/superseded/postponed/cancelled/malformed/source_unavailable`
- 正規化記錄**僅** 25 欄；**無任何 actual-starter / postgame outcome / learning_eligible 欄位**。
- **與 P202C §4 之契約調和（已記錄）：** P202C 曾允許 `source_freshness_seconds=-1` 表「不可得」；P202D prompt Phase 3 明令「必非負」，依**優先序（本 prompt 第一）**採非負（`≥0`），缺/負值即 fail-closed。

---

## 6. Timestamp & Identity Validation Rules

**Timestamp（`_parse_utc`，皆 fail-closed）：**
- 必為 timezone-aware UTC；**naive datetime 拒絕**；非零 offset（如 `+08:00`）拒絕；非 ISO-8601 拒絕。
- `information_cutoff_utc` 必**嚴格早於** `scheduled_start_utc`。
- `collected_at_utc` 必**不晚於** `information_cutoff_utc`。
- `source_freshness_seconds` 必為非負 int。
- `official_game_date` 必為 `YYYY-MM-DD` 且與 `scheduled_start_utc`（UTC 日）相差 ≤ 1 日（聯盟 local 日差）。
- 正規化後時間戳一律輸出為 `…+00:00` ISO 字串。

**Identity：**
- `game_pk` 必存在且為 int（非 bool）。
- `home_team_id != away_team_id`（相同即拒絕）。
- `doubleheader_game_number` 必為 int 且 ∈ 0..2（含拒絕 `bool`/`"1"`/`1.0`）。
- **`game_pk`（＋`doubleheader_game_number`）為唯一 game identity；date/team 組合永不充當 join 鍵。**
- 缺任一必填 identity/timestamp → fail-closed（不靜默強制）。

---

## 7. Canonical Fingerprint & Idempotency Key

- **Fingerprint：** `"sha256:" + sha256(json.dumps(canonical_fields, sort_keys=True, ensure_ascii=False, separators=(",",":")))`，其中 `canonical_fields` 為 18 個正規化後實質欄位（含 source provider/endpoint/record、collected/cutoff/scheduled（ISO）、game_pk、official_date、dh、team ids、雙邊 pitcher id/name、雙邊 pitcher_status、game_status）。→ **key-order 無關**（已測），且 starter/status/time/source/collected 任一變動即變指紋（已測）。
- **Idempotency / dedup key（tuple）：** `(source_provider, source_record_id, game_pk, doubleheader_game_number, collected_at_utc, payload_fingerprint)`。
  - 完全相同的 raw → 相同 tuple → **冪等（不追加第二行）**。
  - 變更先發/狀態/時間/採集時刻 → 不同 tuple → **revision（追加）**。

---

## 8. Append-Only & Revision Behavior

- `append_snapshot(snapshot, path)`：`path` **必填、無預設**；parent dir **必須先存在**（不靜默自建 → fail-closed `SnapshotStoreError`）。
- 採**純 append 模式**（`open(path, "a")` 寫單行）——既有行**逐字不動**（最強 append-only 保證）。
- 追加前以 `load_snapshots` 讀全檔做去重；**malformed 既有檔 → fail-closed（raise；檔案不變更）**。
- 結果 `AppendResult{appended, status∈{appended_new, appended_revision, idempotent_duplicate}, reason, dedup_key, total_records, path}`。
- 邏輯 append-only：歷史記錄不得改寫，revision 以新行表示（已測 `test_revision_appends_and_preserves_prior` 原行保留）。
- 決定性：相同輸入序列 → byte-identical 輸出檔（已測 `test_append_deterministic_repeat`）。

---

## 9. Snapshot-Selection Behavior（`select_canonical_snapshot`，純函式、diagnostic-only）

呼叫端**必須**提供 `stale_max_seconds` 與 `min_lead_seconds`（無未核准之生產預設；負/非數值 → fail-closed）。流程：
1. 比對 `game_pk` **且** `doubleheader_game_number`；無 → `no_matching_game`。
2. 排除 `collected_at_utc > target_information_cutoff_utc`（**post-cutoff 更新永不可用於較早 cutoff**）；全排除 → `no_pre_cutoff_snapshot`。
3. 取 pre-cutoff 中 `collected_at` 最新者；若其 `snapshot_status ∈ {cancelled, postponed, source_unavailable}` → 顯式回該狀態（非 trusted、surfaced）。
4. **Min lead：** `scheduled_start − target_cutoff < min_lead_seconds`（含 cutoff 在開賽後 → 負）→ `insufficient_lead_time`。
5. 排除終態（`cancelled/postponed/source_unavailable/malformed/superseded`）後取最新 selectable；無 → `no_selectable_snapshot`。
6. **Stale：** `target_cutoff − collected_at > stale_max_seconds` → `stale`。
7. `partial` → 區分 `both_sides_tbd`（雙缺）/`one_side_missing`（單缺）。
8. 雙邊任一狀態 ∈ {`scratched/changed/opener/bullpen_game/tbd/unavailable`} → 以代表狀態 **surfaced**（非 trusted）。
9. 雙邊狀態皆 ∈ {`announced/probable/confirmed`} 且雙邊 pitcher_id 齊備 → **`trusted`（diagnostic-only）**；否則 `not_trusted`。
- **永不替換實際先發**：選擇僅來自既存快照，而既存快照依建構即不含 actual starter。

---

## 10. Doubleheader / Postponement / Cancellation / Stale / Missing / TBD / Opener / Scratch

| 情境 | 行為 | 測試 |
|------|------|------|
| Doubleheader | 不同 `game_pk` + `dh∈{1,2}` 完全獨立；同 game_pk 錯 dh → `no_matching_game` | `test_doubleheader_games_remain_independent` |
| Postponement/reschedule | 三快照（原/postponed marker/改期）全保留；早 cutoff→原 trusted；marker 期間→`postponed` surfaced；改期後→新 `scheduled_start` trusted；**不靜默混用 stale 版本** | `test_postponement_history_surfaced_not_mixed` |
| Cancellation | `snapshot_status=cancelled`，**永不 trusted** | `test_cancelled_never_trusted` |
| Stale | 依呼叫端門檻判定 → `stale` fail-closed | `test_stale_fails_closed` |
| One-side missing | `partial` → `one_side_missing` | `test_one_side_missing_fails_closed` |
| Both TBD | `partial` → `both_sides_tbd` | `test_both_sides_tbd_fails_closed` |
| Opener/bullpen | surfaced `opener_bullpen` | `test_opener_surfaced` |
| Scratch | surfaced `scratched` | `test_scratched_surfaced` |
| Starter change | revision 追加；surfaced `changed` | `test_changed_starter_surfaced` |
| Min lead / cutoff 後 | `insufficient_lead_time` | `test_insufficient_lead_time` / `test_cutoff_after_start_rejected` |

---

## 11. Actual-Starter Substitution Prevention

- `_reject_forbidden(raw)`：任一禁用欄位（`home_win/final_score/home_score/away_score/result/box_score/post_game_stats/actual_winner/winning_team/...` 及 `home_actual_starter_id/away_actual_starter_id/as_played/asplayed/actual_starter/...`）出現（非 None）即 `SnapshotValidationError`。亦拒絕 `production_ready=True`、`diagnostic_only=False`、任何 `learning_eligible`。
- `_reject_provider_markers(provider, endpoint)`：含 `asplayed/as_played/actual/postgame/post_game` 即拒絕（杜絕來源自稱 as-played）。
- 正規化 schema 結構上**不含**任何 actual/outcome 欄位（已測 `test_normalized_schema_has_no_outcome_or_actual_fields`）。
- 選擇器只回既存快照，**永不**以賽後資料替換。
- 測試：`test_actual_starter_substitution_rejected`、`test_postgame_and_actual_fields_rejected`（8 參數）、`test_asplayed_provider_rejected`、`test_postgame_collected_update_not_selected_for_pregame_cutoff`。

---

## 12. No-Network Proof

- 模組 import 僅 `json/hashlib/os/datetime/dataclasses/typing/logging`——**無** `requests/httpx/socket/urllib/aiohttp/http.client/ssl`（已測 `test_module_has_no_network_imports` 掃描原始碼）。
- import **零副作用**：不寫檔、不連網；`CANONICAL_RUNTIME_OUTPUT_PATH_HINT` 僅文件常數，import 後該路徑不存在（已測 `test_module_import_creates_no_runtime_file`）。
- `normalize_snapshot` / `select_canonical_snapshot` **不碰檔案系統**（已測 `test_normalize_and_select_touch_no_filesystem`：chdir 至空 tmp_path 後無檔案生成）。
- 唯一 I/O＝`append_snapshot`/`load_snapshots`，路徑由呼叫端顯式提供；測試一律 `tmp_path`。

---

## 13. Fixture Inventory（`tests/fixtures/probable_starter_snapshot_fixtures.json`）

`schema_version=p202d_probable_snapshot_fixture_v1`；全合成（team `90xx`、pitcher `8000xx`、game_pk `99xxxx`、年份 2099、provider `fixture_synthetic`、endpoint `fixture://…`）；無 live payload、無 secret/token、無官方授權聲明；皆 `diagnostic_only`（正規化強制）。

| Fixture | expect | 涵蓋 |
|---------|--------|------|
| `valid_both_side` | valid | 雙邊 probable → trusted |
| `exact_duplicate` | valid | 冪等 |
| `starter_change` | valid | revision / changed |
| `post_cutoff_update` | valid | post-cutoff 排除 |
| `scratched_starter` | valid | scratched surfaced |
| `one_side_missing` | valid | partial 單缺 |
| `both_sides_tbd` | valid | partial 雙缺 |
| `doubleheader_game_1` / `_2` | valid | dh 獨立 |
| `postponed_reschedule_original` / `postponed_marker` / `postponed_reschedule_new` | valid | 改期歷史 |
| `cancelled_game` | valid | cancelled |
| `stale_snapshot` | valid | staleness |
| `opener_bullpen_game` | valid | opener surfaced |
| `malformed_timestamp` | reject | naive ts |
| `malformed_identity` | reject | 同隊 id |
| `actual_starter_substitution` | reject | as-played 欄位 |

---

## 14. Tests Run

| 指令 | 結果 |
|------|------|
| `pytest tests/test_mlb_probable_starter_snapshot_intake.py -q` | **89 passed** |
| 合併工作流 5 檔（`test_p180_strategy_leaderboard` + `test_run_mlb_tsl_paper_recommendation_simulation_gate` + `test_mlb_paper_evaluator` + `test_mlb_paper_evaluation_runner` + `test_mlb_daily_scheduler`） | **157 passed**（＝既有基線，無回歸） |

涵蓋 A.schema/normalization、B.timestamp、C.identity/join、D.fingerprint/idempotency、E.append-only、F.selection、G.leakage、H.no-network 全部 9 組。
> 註：5 檔個別指令所執行之測試由上述合併指令完整涵蓋，總數一致（157）。
> 本輪**未遇** `test_*_active_task_updated` 類治理陳舊失敗（不在驗證集；不在本任務 scope；不得編輯 `active_task.md` 修正）。

**Test result：PASS。**

---

## 15. Full Regression Status

**NOT RUN（全庫）。** 新模組與既有產線完全解耦（純新增、零既有檔修改），僅跑新直接套件（89）＋成比例之工作流護欄（157），對風險成比例。

---

## 16. Known Limitations

1. **Fixture-only / 無真實覆蓋：** 不採集任何真實資料；賽前 probable 證據之實際累積須待**獨立授權**之 live collector（P202E）。
2. **賽前史不可重建：** 本 skeleton 只「就緒」捕捉格式；在 live 採集開啟前，賽前證據仍持續不可逆流失。
3. **未接產線：** 選擇器輸出為 diagnostic-only，**未**接 recommendation/scheduler/evaluator；不影響任何推薦或 `learning_eligible`。
4. **門檻為 caller-supplied：** `stale_max_seconds`/`min_lead_seconds` 由呼叫端提供（P202C 中為 PROPOSED 值，尚待核准）；模組不內建生產門檻。
5. **`changed` 保守視為非 trusted：** 即使附新 probable id，`changed` 一律 surfaced 非 trusted（fail-closed 偏向）；日後可依政策放寬。
6. **無逐場投手事件契約之實作：** P202C §5 的 pitcher-event SSOT 仍未實作（候選 B，可日後回填）。

---

## 17. Explicit Non-Actions

未呼叫任何網路/live MLB API/付費 API；未實作 collector/producer/model/feature/scheduler；未連接 recommendation/scheduler/evaluator；未寫任何真實 runtime 資料集（`data/mlb_probable_starters/` 未建立）；測試全用 `tmp_path`；未 regenerate artifact；無 model fit/refit/calibration；無 DB write / provider unlock / production / real recommendation / observed-odds / EV·CLV·Kelly / registry / controlled_apply / strategy·champion mutation；未新增第三方相依；未改 package/config/CI；未改 `data/mlb_player_stats.py`、`data/mlb_sp_data_loader.py`、`scripts/run_mlb_tsl_paper_recommendation.py`、`orchestrator/mlb_daily_scheduler.py`、`orchestrator/mlb_paper_evaluator.py` 或任何 P83/P84/Phase52/58–64 實作；未改 recommendation row schema；未編輯 governance 檔；未 branch/checkout/commit/push/PR/merge/rebase/reset/stash/clean/delete；未 stage/`git add`；未碰 tolerated dirty 檔。**僅建立 4 個白名單檔。**

---

## 18. Required Completion Check

| 項目 | 結果 |
|------|------|
| 是否真的完成 | ✅ 是 — module + fixtures + tests + report 完成；89 直接測試 + 157 工作流全綠 |
| Test result | **PASS** |
| New P202D direct test count | **89 passed** |
| Existing workflow result | **157 passed**（無回歸） |
| Full regression | **NOT RUN** |
| Schema contract status | ✅ 25 欄 = P202C §4（freshness 非負，已調和並記錄） |
| Timestamp safety status | ✅（tz-aware UTC、cutoff<start、collected≤cutoff、naive/offset 拒絕） |
| Append-only status | ✅（純 append、既有行不動、parent 須存在、malformed fail-closed） |
| Idempotency status | ✅（exact duplicate no-op） |
| Revision-history status | ✅（同 game 變更追加；歷史保留） |
| Doubleheader handling status | ✅（game_pk+dh 獨立；date/team 不替代） |
| Postponement/cancellation status | ✅（歷史保留；surfaced；不混用 stale 版本） |
| Staleness/fail-closed status | ✅（caller 門檻；stale/partial/missing/tbd/insufficient_lead → fail-closed + 顯式 reason） |
| Actual-starter substitution prevention status | ✅（forbidden 欄位 + provider marker + 結構無 actual 欄位 + 不替換） |
| No-network status | ✅（無網路 import；import 零副作用；normalize/select 不碰檔案系統） |
| Real runtime data write status | 無（僅 tmp_path） |
| Selected next task recommendation | **P202E**（獨立授權之 live probable-starter snapshot collector，將真實寫入 append-only store）；或 **P202F** 逐場投手事件契約之 backfill skeleton（候選 B） |
| Single remaining blocker | live 採集授權（賽前證據只能從今起前向擷取） |
| Modified files | 無（僅 tolerated/governance dirty，非本任務所改） |
| Untracked files（本任務新增） | `data/mlb_probable_starter_snapshots.py`、`tests/test_mlb_probable_starter_snapshot_intake.py`、`tests/fixtures/probable_starter_snapshot_fixtures.json`、`report/p202d_probable_starter_snapshot_intake_skeleton_20260613.md`（另有既有未提交 `agent_bootstrap/`、P199/P202/P202B/P202C 報告） |
| Staged files | 無 |
| Current branch / Local HEAD / origin/main HEAD | `main` / `539bca2` / `539bca2` |
| Open PR count | 0 |
| active_task.md status | `AUTHORIZED_PLAN_ONLY`（P199；未修改；陳舊） |
| DB write / network·API / provider unlock | 無 / 無 / 無 |
| production / registry / controlled_apply mutation | 無 / 無 / 無 |
| model / strategy / champion mutation | 無 / 無 / 無 |
| commit / push status | 無 / 無 |
| 下一輪是否允許 | ✅ 允許（P202E live collector 需獨立授權白名單；或候選 B skeleton） |
| Worker model 建議 | Opus 強 |
| Thinking level 建議 | 中到強 |
| 是否續用同一對話 | 建議新一輪對話（重跑 Phase 0） |

---

## Final Classification

**`P202D_PROBABLE_STARTER_SNAPSHOT_SKELETON_COMPLETE`**

> 已實作 fixture-only、no-network、append-only、fail-closed 之賽前 probable-starter 快照 intake skeleton（`data/mlb_probable_starter_snapshots.py`），完整落實 P202C §4 schema 與 §8/§9 規則：時間戳安全、`game_pk`+dh identity、canonical 指紋冪等、append-only revision（歷史保留）、純函式 canonical selection、賽後/實際先發替換之多重 leakage 防護、零網路證明。89 直接測試 + 157 工作流護欄全綠；恰好 4 個白名單檔；零真實資料寫入；P200 provenance fail-closed 與 P201 learning-eligibility 完整保留（本模組與推薦產線解耦，永不標 learning_eligible）。唯一剩餘 blocker＝live 採集授權（P202E，獨立授權），因賽前證據只能從今起前向擷取。
