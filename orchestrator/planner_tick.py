"""
Betting-pool Orchestrator Planner Tick
複製 LotteryNew 的 Planner 邏輯
"""
from __future__ import annotations

import os
import re
import uuid
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from orchestrator import db
from orchestrator import common as _common
from orchestrator import execution_policy
from orchestrator import insight_extractor, patch_task_generator, patch_validator
from orchestrator.task_quality_gate import build_task_dedupe_key, evaluate_task_quality

logger = logging.getLogger(__name__)

# ── 根目錄（用於 wiki / evidence 挖掘）──
_REPO_ROOT = Path(__file__).resolve().parents[1]
WIKI_MINING_SOURCES = [
    # Wiki knowledge sources
    "wiki/RESEARCH_LAYER.md",
    "wiki/DATA_SOURCES.md",
    "wiki/KNOWN_ISSUES.md",
    "wiki/CLEANUP_PLAN.md",
    "wiki/INVENTORY.md",
    "wiki/ARCHITECTURE.md",
    "wiki/PIPELINES.md",
]
# MLB evidence files mined for additional task candidates
MLB_EVIDENCE_SOURCES = [
    "data/wbc_backend/reports/mlb_regime_paper_report.json",
    "data/wbc_backend/reports/mlb_decision_quality_report.json",
    "data/wbc_backend/reports/mlb_paper_tracking_report.json",
    "data/mlb_context/odds_timeline.jsonl",
    "data/mlb_context/external_closing_state.json",
    "data/wbc_backend/reports/prediction_registry.jsonl",
    "research/trade_ledger.jsonl",
    "research/roi_tracking.json",
]
# 限制每次 mining 候選數量
MINING_MAX_CANDIDATES = 5
# REPLAN_REQUIRED 連續超過此數量才啟動批量歸檔
REPLAN_ARCHIVE_THRESHOLD = 3

# ── Planner 封鎖守衛常數 ─────────────────────────────────────────────────────
# 這些狀態代表任務已終止，Planner 可以繼續建立新任務
_TERMINAL_TASK_STATUSES = frozenset({
    "COMPLETED", "FAILED", "FAILED_RATE_LIMIT", "FAILED_STUB",
    "CANCELLED", "REPLAN_REQUIRED", "ARCHIVED",
})

# Rate limit 關鍵字：用於 BLOCKED_ENV 自動解除時判斷新狀態
_RATE_LIMIT_MARKERS = (
    "rate limit", "weekly rate limit", "you've hit your rate limit",
    "premium request limit", "429", "quota exceeded",
)


REQUIRED_OUTPUT_FIELDS = [
    "violations",
    "metrics",
    "regime_counts",
    "leakage_detected",
    "candidate_fix",
]


def _make_atomic_blueprint(
    *,
    focus_area: str,
    market_scope: str,
    analysis_family: str,
    title: str,
    objective: str,
    focus_keys: str,
    signal_state_type: str,
    task_kind: str,
    deliverable_kind: str,
    dataset_paths: list[str],
    steps: list[str],
    validation_checks: list[str],
    expected_duration_hours: int = 2,
    optional_follow_up: Optional[str] = None,
) -> dict:
    return {
        "focus_area": focus_area,
        "market_scope": market_scope,
        "analysis_family": analysis_family,
        "title": title,
        "focus_keys": focus_keys,
        "signal_state_type": signal_state_type,
        "expected_duration_hours": expected_duration_hours,
        "objective": objective,
        "major_objectives": [objective],
        "task_kind": task_kind,
        "deliverable_kind": deliverable_kind,
        "dataset_paths": dataset_paths,
        "steps": steps,
        "validation_checks": validation_checks,
        "optional_follow_up": optional_follow_up,
    }


# ── Atomic Planner Profile ───────────────────────────────────────────────────
# Rule set:
# - single objective per task
# - <= 2 小時真實計算預算
# - 結果必須輸出結構化 JSON，可直接餵給 insight / patch loop
# - Monte Carlo 一律拆成獨立 follow-up task
TASK_BLUEPRINTS = (
    _make_atomic_blueprint(
        focus_area="mlb-calibration-baseline-snapshot",
        market_scope="MLB moneyline pregame",
        analysis_family="calibration-atomic",
        title="MLB 校準基線快照：Regime Brier / LogLoss 差異盤點",
        objective="量化各 regime 的校準基線差異，輸出可追蹤的 Brier / LogLoss / ECE 指標快照。",
        focus_keys="mlb_calibration,brier,logloss,ece,regime",
        signal_state_type="deep_research_calibration",
        task_kind="audit",
        deliverable_kind="metric_delta",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
        ],
        steps=[
            "按 regime 切分現有預測樣本，計算 Brier、LogLoss、ECE 與樣本數。",
            "標記指標最差的 3 個 regime，確認是否集中於特定信心區間。",
            "輸出可供後續 patch 使用的 regime 指標落差 JSON。",
        ],
        validation_checks=[
            "每個 regime 都要有 metrics 與 regime_counts。",
            "若樣本不足，violations 需列出不足門檻與實際數量。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-calibration-drift-audit",
        market_scope="MLB moneyline pregame",
        analysis_family="calibration-atomic",
        title="MLB 校準漂移審計：高誤差 Regime 的特徵漂移盤查",
        objective="找出高校準誤差 regime 的漂移特徵與違規樣本數，產出可修補候選。",
        focus_keys="mlb_calibration,feature_drift,violation_count,regime",
        signal_state_type="deep_research_calibration",
        task_kind="audit",
        deliverable_kind="candidate_patch",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
            "wbc_backend/research/mlb_regime_feature_redesign.py",
        ],
        steps=[
            "鎖定基線快照中誤差最高的 regime。",
            "對照特徵來源，統計漂移最嚴重的特徵與違規樣本數。",
            "輸出 candidate_fix 清單，限定為可直接修補的特徵處理策略。",
        ],
        validation_checks=[
            "candidate_fix 至少包含 target_file、patch_hint、expected_metric。",
            "不可同時加入 Monte Carlo 或最終推薦段落。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-calibration-monte-carlo-sensitivity",
        market_scope="MLB moneyline pregame",
        analysis_family="calibration-atomic",
        title="MLB 校準敏感度模擬：Monte Carlo 對資金曲線尾風險的單獨驗證",
        objective="單獨量化校準誤差對 bankroll tail risk 的影響，不混入審計或修正提案。",
        focus_keys="mlb_calibration,monte_carlo,tail_risk,drawdown",
        signal_state_type="deep_research_calibration",
        task_kind="simulation",
        deliverable_kind="metric_delta",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
            "research/roi_tracking.json",
        ],
        steps=[
            "使用既有 regime 校準誤差分布建立 Monte Carlo 輸入。",
            "模擬不同校準誤差情境下的 tail loss 與 drawdown。",
            "輸出 metrics.delta 與 leakage_detected=false 的模擬 JSON。",
        ],
        validation_checks=[
            "此任務只能做 simulation，不得同時包含 audit 或 proposal。",
            "candidate_fix 可為空陣列，但 metrics 必須完整。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-feature-window-leakage-audit",
        market_scope="MLB moneyline / totals pregame",
        analysis_family="feature-atomic",
        title="MLB 特徵視窗洩漏審計：Starter / Bullpen 時間窗違規盤點",
        objective="驗證 starter 與 bullpen 特徵是否跨越賽前時間窗，產出 violation count 與修補候選。",
        focus_keys="mlb_features,starter,bullpen,window_leakage",
        signal_state_type="deep_research_feature",
        task_kind="audit",
        deliverable_kind="violation_count",
        dataset_paths=[
            "wbc_backend/research/mlb_regime_feature_redesign.py",
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
        ],
        steps=[
            "盤點 starter / bullpen 特徵的時間窗與資料來源。",
            "統計跨越開賽前 cut-off 的特徵與違規次數。",
            "輸出 leakage_detected、violations 與 candidate_fix。",
        ],
        validation_checks=[
            "若無洩漏也要輸出 leakage_detected=false 與空 violations。",
            "不可在同任務要求 SHAP、Monte Carlo 與最終推薦。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-feature-predictive-delta",
        market_scope="MLB moneyline / totals pregame",
        analysis_family="feature-atomic",
        title="MLB 特徵邊際貢獻快照：Contact / Weather 指標增量驗證",
        objective="量化 contact quality 與 weather 特徵的邊際貢獻，只輸出 metric delta 與 regime_counts。",
        focus_keys="mlb_features,contact_quality,weather,metric_delta",
        signal_state_type="deep_research_feature",
        task_kind="audit",
        deliverable_kind="metric_delta",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
        ],
        steps=[
            "比較有無 contact / weather 特徵時的核心 metrics。",
            "依 regime 彙整 metric delta 與樣本數。",
            "輸出是否值得進一步 patch 的 candidate_fix 建議。",
        ],
        validation_checks=[
            "metrics 至少包含 baseline、candidate、delta 三組欄位。",
            "不可同時要求最終推薦與模擬。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-regime-boundary-validation",
        market_scope="MLB moneyline pregame by regime",
        analysis_family="regime-atomic",
        title="MLB Regime 邊界驗證：分界條件誤分類盤點",
        objective="驗證現有 regime 邊界是否造成誤分類，輸出違規區間與樣本數。",
        focus_keys="mlb_regime,boundary_validation,misclassification",
        signal_state_type="deep_research_regime",
        task_kind="audit",
        deliverable_kind="violation_count",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
            "data/wbc_backend/reports/mlb_decision_quality_report.json",
        ],
        steps=[
            "載入 regime 標籤與預測結果，統計邊界附近樣本。",
            "識別誤分類最集中的邊界區間。",
            "輸出 violations 與後續修補建議。",
        ],
        validation_checks=[
            "violations 須標示 regime、boundary_range、count。",
            "不可混入 proposal 與 Monte Carlo。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-regime-sample-sufficiency",
        market_scope="MLB moneyline pregame by regime",
        analysis_family="regime-atomic",
        title="MLB Regime 樣本充分性分析：各分層統計顯著性檢查",
        objective="檢查各 regime 是否達到最低樣本門檻，輸出 regime_counts 與不足警示。",
        focus_keys="mlb_regime,sample_sufficiency,regime_counts",
        signal_state_type="deep_research_regime",
        task_kind="audit",
        deliverable_kind="insight",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
        ],
        steps=[
            "統計各 regime 的有效測試樣本數。",
            "標記低於門檻的 regime 並列入 violations。",
            "輸出可讓 planner 後續補樣本或調整切分的 JSON。",
        ],
        validation_checks=[
            "regime_counts 不可缺欄。",
            "candidate_fix 可為補樣本建議，但不得是最終推薦書面報告。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-odds-staleness-audit",
        market_scope="MLB pregame odds timeline",
        analysis_family="odds-atomic",
        title="MLB 決策時刻賠率陳舊度審計：Pregame Timeline Staleness 盤點",
        objective="量化開賽前賠率 staleness 與缺口，輸出 violation count 與 CLV 風險指標。",
        focus_keys="mlb_odds,staleness,clv,timeline",
        signal_state_type="deep_research_odds_quality",
        task_kind="audit",
        deliverable_kind="violation_count",
        dataset_paths=[
            "data/mlb_context/odds_timeline.jsonl",
            "data/mlb_context/external_closing_state.json",
        ],
        steps=[
            "按 30 / 60 / 120 分鐘決策時刻計算 staleness rate。",
            "標記超過閾值的賽事與 league。",
            "輸出 violations、metrics 與 candidate_fix。",
        ],
        validation_checks=[
            "需列出 staleness rate 與缺口計數。",
            "不可把 closing proxy 推薦和 Monte Carlo 混在同任務。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-feedback-bad-bet-patterns",
        market_scope="MLB paper-only trade ledger",
        analysis_family="feedback-atomic",
        title="MLB Bad Bet 模式提取：Regime 關聯虧損序列盤點",
        objective="從 trade ledger 提取可重複 bad bet 模式，輸出可追蹤的 insight 與候選預警規則。",
        focus_keys="mlb_feedback,bad_bet,regime_loss,warning_rule",
        signal_state_type="deep_research_feedback",
        task_kind="audit",
        deliverable_kind="insight",
        dataset_paths=[
            "research/trade_ledger.jsonl",
            "research/roi_tracking.json",
        ],
        steps=[
            "按 regime 與連續虧損序列聚類 bad bet。",
            "找出重複出現的特徵組合與次數。",
            "輸出可供後續規則 patch 的 candidate_fix。",
        ],
        validation_checks=[
            "violations 應記錄高風險 pattern 與出現次數。",
            "不可同時要求最終推薦報告。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-walkforward-split-boundary",
        market_scope="MLB paper-only backtest",
        analysis_family="backtest-validity-atomic",
        title="MLB Walk-Forward Split Boundary Validation",
        objective="驗證 walk-forward split 邊界是否正確隔離訓練與測試集，輸出 split 違規數。",
        focus_keys="mlb_walkforward,split_boundary,violation_count",
        signal_state_type="deep_research_backtest_validity",
        task_kind="audit",
        deliverable_kind="violation_count",
        dataset_paths=[
            "wbc_backend/evaluation/real_backtest.py",
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
        ],
        steps=[
            "檢查 split 定義與時間序排列是否一致。",
            "列出 train/test overlap 或 lookahead 的違規樣本數。",
            "輸出 violations、regime_counts 與 candidate_fix。",
        ],
        validation_checks=[
            "只做 split boundary validation，不可混入 Monte Carlo。",
            "leakage_detected 必須明確 true / false。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-walkforward-feature-window",
        market_scope="MLB paper-only backtest",
        analysis_family="backtest-validity-atomic",
        title="MLB Feature Window Leakage Audit",
        objective="檢查滑動窗口特徵是否跨越 split 邊界，輸出 feature-level leakage 統計。",
        focus_keys="mlb_walkforward,feature_window,leakage",
        signal_state_type="deep_research_backtest_validity",
        task_kind="audit",
        deliverable_kind="violation_count",
        dataset_paths=[
            "wbc_backend/research/mlb_model_rebuild.py",
            "data/mlb_context/odds_timeline.jsonl",
        ],
        steps=[
            "盤點回測中使用的滑動窗口特徵。",
            "檢查每個特徵的時間窗是否跨越 split。",
            "輸出 feature 級 violations 與 candidate_fix。",
        ],
        validation_checks=[
            "每條 violation 需帶 feature_name 與 window_range。",
            "不可混入 sample sufficiency 或 proposal。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-walkforward-regime-samples",
        market_scope="MLB paper-only backtest",
        analysis_family="backtest-validity-atomic",
        title="MLB Regime Sample Sufficiency Analysis",
        objective="確認各 regime 測試樣本是否達標，輸出不足門檻的 regime_counts 與違規列表。",
        focus_keys="mlb_walkforward,regime_counts,sample_sufficiency",
        signal_state_type="deep_research_backtest_validity",
        task_kind="audit",
        deliverable_kind="insight",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
        ],
        steps=[
            "依 regime 統計有效測試樣本數。",
            "標記低於門檻的 regime 並量化缺口。",
            "輸出可供後續補樣本或降權的 JSON。",
        ],
        validation_checks=[
            "regime_counts 必須完整。",
            "不能同時要求 Monte Carlo 或最終推薦。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-walkforward-leakage-monte-carlo",
        market_scope="MLB paper-only backtest",
        analysis_family="backtest-validity-atomic",
        title="Monte Carlo Leakage Sensitivity",
        objective="單獨模擬不同 leakage 率對 edge 與 drawdown 的影響，不混入審計與修補提案。",
        focus_keys="mlb_walkforward,monte_carlo,leakage_sensitivity",
        signal_state_type="deep_research_backtest_validity",
        task_kind="simulation",
        deliverable_kind="metric_delta",
        dataset_paths=[
            "data/wbc_backend/reports/mlb_regime_paper_report.json",
            "research/roi_tracking.json",
        ],
        steps=[
            "建立 leakage rate 2% / 10% / 25% 三組模擬情境。",
            "計算 edge 虛增與 drawdown 變化。",
            "輸出 metrics.delta 與 regime_counts，不附最終建議。",
        ],
        validation_checks=[
            "simulation 任務不得包含 audit / proposal 關鍵字。",
            "candidate_fix 預設空陣列。",
        ],
    ),
    _make_atomic_blueprint(
        focus_area="mlb-walkforward-leakage-fix-proposal",
        market_scope="MLB paper-only backtest",
        analysis_family="backtest-validity-atomic",
        title="Leakage Fix Proposal",
        objective="基於已知 split / feature leakage 證據，輸出可實作的 candidate patch，不做額外審計或模擬。",
        focus_keys="mlb_walkforward,candidate_patch,leakage_fix",
        signal_state_type="deep_research_backtest_validity",
        task_kind="proposal",
        deliverable_kind="candidate_patch",
        dataset_paths=[
            "wbc_backend/research/mlb_model_rebuild.py",
            "wbc_backend/evaluation/mlb_decision_quality.py",
        ],
        steps=[
            "彙整既有 leakage 證據與違規熱點。",
            "為每個熱點提出最小 patch 設計。",
            "輸出 candidate_fix JSON，包含 target_file、change_type、expected_metric。",
        ],
        validation_checks=[
            "proposal 任務不得再跑 Monte Carlo 或重新做 audit。",
            "至少輸出一個 candidate_fix，否則列入 violations。",
        ],
        optional_follow_up="如需驗證 patch 成效，另開 validation task。",
    ),
)


def generate_task_slot_key() -> str:
    """產生任務 slot key"""
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S%f")
    return f"{date_str}{time_str}-task"


def _attempt_maintenance_task(request_id: str, start_time: datetime) -> dict:
    """嘗試建立 maintenance_health_check light task（每日一次，daily cap 守衛）。

    Called by run_planner_tick() in STEP 3 when no research task is eligible.

    Returns dict:
      {"status": "CREATED", "task_id": int, "dedupe_key": str}
      {"status": "SKIP_DAILY_CAP", "task_id": int, "dedupe_key": str}
    """
    today = _common.dedupe_day_utc()
    dedupe_key = f"maintenance_health_check:{today}"

    existing = db.get_nonfailed_task_by_dedupe_key(dedupe_key)
    if existing:
        msg = (
            f"PLANNER_SKIP_DAILY_CAP: 今日維護任務已建立或完成，避免重複建立。 "
            f"existing_task_id={existing['id']} "
            f"existing_status={existing['status']} "
            f"dedupe_key={dedupe_key!r}"
        )
        logger.info("[PlannerTick] %s", msg)
        db.record_run(
            runner="planner_tick",
            outcome="SKIPPED",
            request_id=request_id,
            task_id=existing["id"],
            message=msg,
            tick_at=start_time.isoformat(),
        )
        return {"status": "SKIP_DAILY_CAP", "task_id": existing["id"], "dedupe_key": dedupe_key}

    # Create the maintenance task (no LLM, light worker only)
    slot_key = generate_task_slot_key()
    date_folder = today
    task_dir = os.path.join(db.ORCH_ROOT, "tasks", date_folder)
    os.makedirs(task_dir, exist_ok=True)
    prompt_path = os.path.join(task_dir, f"{slot_key}-prompt.md")
    prompt_text = (
        "# [MAINTENANCE] Orchestration health check\n\n"
        "## Objective\n"
        "Check current orchestrator state without touching betting strategy or external APIs.\n\n"
        "## Constraints\n"
        "- No betting strategy changes\n"
        "- No external API calls\n"
        "- No production betting data writes\n"
        "- No LLM required — light worker executes this directly\n\n"
        f"## Task Type\nmaintenance_health_check\n\n"
        f"## Created At\n{datetime.now(timezone.utc).isoformat()}\n"
    )
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt_text)

    task_id = db.create_task(
        slot_key=slot_key,
        date_folder=date_folder,
        title="[MAINTENANCE] Orchestration health check",
        slug=slot_key,
        status="QUEUED",
        prompt_file_path=prompt_path,
        prompt_text=prompt_text,
        dedupe_key=dedupe_key,
        task_type="maintenance_health_check",
        worker_type="light",
        regime_state="maintenance",
        epoch_id=0,
    )
    msg = (
        f"Planner created maintenance task #{task_id}: [MAINTENANCE] Orchestration health check "
        f"(dedupe_key={dedupe_key!r})"
    )
    logger.info("[PlannerTick] %s", msg)
    db.record_run(
        runner="planner_tick",
        outcome="SUCCESS",
        request_id=request_id,
        task_id=task_id,
        message=msg,
        tick_at=start_time.isoformat(),
    )
    return {"status": "CREATED", "task_id": task_id, "dedupe_key": dedupe_key}


# ── Phase 4: Forced Exploration Lane Definitions ──────────────────────────

_FORCED_EXPLORATION_LANES: list[dict] = [
    {
        "name": "market_signal",
        "task_type": "forced_exploration_market_signal",
        "title": "[EXPLORE] Market Signal Research: Odds Movement & CLV Proxy",
        "purpose": (
            "Research whether market-derived signals may improve betting decision quality."
        ),
        "examples": [
            "odds movement",
            "opening line vs closing line",
            "line drift",
            "implied probability change",
            "market consensus",
            "CLV proxy",
        ],
        "output_prefix": "market_signal_hypothesis",
    },
    {
        "name": "risk_rule",
        "task_type": "forced_exploration_risk_rule",
        "title": "[EXPLORE] Risk / Bankroll Rule Research: No-Bet & Drawdown Guards",
        "purpose": (
            "Research no-bet / risk-cap rules that may reduce bad bets or drawdown."
        ),
        "examples": [
            "max drawdown guard",
            "Kelly cap",
            "exposure concentration",
            "low-liquidity no-bet rule",
            "high-uncertainty no-bet rule",
        ],
        "output_prefix": "risk_rule_hypothesis",
    },
    {
        "name": "walk_forward",
        "task_type": "forced_exploration_walk_forward",
        "title": "[EXPLORE] Walk-Forward Robustness Research: Backtest & Leakage Checks",
        "purpose": (
            "Research whether current backtest / model logic survives walk-forward, "
            "sample sufficiency, and leakage checks."
        ),
        "examples": [
            "train/test split integrity",
            "sample sufficiency by market regime",
            "rolling window stability",
            "leakage risk",
            "OOS degradation",
        ],
        "output_prefix": "walk_forward_hypothesis",
    },
    {
        "name": "calibration",
        "task_type": "forced_exploration_calibration",
        "title": "[EXPLORE] Model Calibration / CLV Research: Brier Score & Reliability",
        "purpose": "Research calibration quality and CLV alignment.",
        "examples": [
            "predicted probability calibration",
            "Brier score",
            "reliability curve",
            "CLV vs model confidence",
            "overconfident market regimes",
        ],
        "output_prefix": "calibration_hypothesis",
    },
    {
        "name": "no_bet",
        "task_type": "forced_exploration_no_bet",
        "title": "[EXPLORE] Anti-Strategy / No-Bet Rule Research: Fake Edge & Market Shock",
        "purpose": "Research conditions where the system should avoid betting.",
        "examples": [
            "fake edge",
            "market shock",
            "stale odds",
            "conflicting model / market signals",
            "high variance regime",
            "low sample confidence",
        ],
        "output_prefix": "no_bet_rule_hypothesis",
    },
    {
        "name": "ux_decision",
        "task_type": "forced_exploration_ux_decision",
        "title": "[EXPLORE] UX / Decision Quality Research: Decision Card & CLV Display",
        "purpose": (
            "Research UI / decision improvements that reduce operator error."
        ),
        "examples": [
            "decision card clarity",
            "bet/no-bet explanation",
            "confidence badge",
            "CLV tracking display",
            "risk warning visibility",
            "manual override audit trail",
        ],
        "output_prefix": "ux_decision_quality_hypothesis",
    },
]

# Lane rotation order (deterministic, by index)
# market_signal → risk_rule → walk_forward → calibration → no_bet → ux_decision → repeat


def _build_forced_exploration_prompt(lane_def: dict, today: str, output_filename: str) -> str:
    """Build the research prompt markdown for a forced exploration lane task."""
    lane_name = lane_def["name"]
    task_type = lane_def["task_type"]
    title = lane_def["title"]
    purpose = lane_def["purpose"]
    examples_list = "\n".join(f"- {ex}" for ex in lane_def["examples"])

    return (
        f"# {title}\n\n"
        f"## Lane\n{lane_name}\n\n"
        f"## Task Type\n{task_type}\n\n"
        f"## Worker Type\nresearch\n\n"
        f"## Purpose\n{purpose}\n\n"
        f"## Exploration Examples\n{examples_list}\n\n"
        f"## Constraints\n"
        f"- No betting strategy changes\n"
        f"- No model weight modifications\n"
        f"- No external betting API calls\n"
        f"- No production betting data writes\n"
        f"- Research only; do not place bets\n\n"
        f"## Required Report Sections\n\n"
        f"### 1. New Hypothesis\n"
        f"State one clear, falsifiable hypothesis relevant to: {purpose}\n\n"
        f"### 2. Why It May Improve Betting Decision Quality\n"
        f"Explain the mechanism: how this hypothesis, if validated, would improve "
        f"match odds assessment, CLV, ROI, hit rate, or drawdown.\n"
        f"Use only Betting-pool domain terms: market, match, odds, line movement, CLV, "
        f"ROI, hit rate, drawdown, active betting strategy, benchmark model, shadow model, "
        f"walk-forward, backtest, leakage audit, bankroll / risk-cap, no-bet rule, "
        f"market regime, sample sufficiency.\n\n"
        f"### 3. Required Data\n"
        f"List the data sources, time windows, and minimum sample requirements.\n\n"
        f"### 4. Minimal Validation Plan\n"
        f"Describe the smallest meaningful experiment:\n"
        f"- Metric to measure\n"
        f"- Baseline to compare against\n"
        f"- Acceptance threshold\n\n"
        f"### 5. Risk / Leakage Check\n"
        f"Identify:\n"
        f"- Any look-ahead leakage risks\n"
        f"- Data availability risks\n"
        f"- Market regime sensitivity\n\n"
        f"### 6. Decision\n"
        f"State exactly one of:\n"
        f"- WORTH_VALIDATION\n"
        f"- WATCH_ONLY\n"
        f"- REJECT_FOR_NOW\n"
        f"- INCONCLUSIVE_NEED_DATA\n\n"
        f"### 7. Next Task If Worth Validation\n"
        f"If decision is WORTH_VALIDATION, include a complete validation task prompt with:\n"
        f"- Title\n"
        f"- Objective\n"
        f"- Dataset paths\n"
        f"- Steps\n"
        f"- Validation checks\n"
        f"- Expected output\n\n"
        f"---\n\n"
        f"## Output File\n{output_filename}\n\n"
        f"## Created\n{today}\n\n"
        f"## Source\nforced_exploration\n"
    )


def _attempt_forced_exploration(request_id: str, start_time: datetime) -> dict:
    """Attempt to create exactly one forced exploration research task (daily cap per lane).

    Lane rotation order (deterministic):
      market_signal → risk_rule → walk_forward → calibration → no_bet → ux_decision → repeat

    Skips any lane whose dedupe_key already has a non-failed task today.
    Creates the first eligible lane only.

    Returns:
      {"status": "CREATED", "task_id": int, "dedupe_key": str, "lane": str}
      {"status": "SKIP_ALL_LANES_CAPPED", "capped_lanes": list[str]}
    """
    today = _common.dedupe_day_utc()
    capped_lanes: list[str] = []

    for lane_def in _FORCED_EXPLORATION_LANES:
        lane_name = lane_def["name"]
        task_type = lane_def["task_type"]
        dedupe_key = f"forced_exploration:{lane_name}:{today}"

        existing = db.get_nonfailed_task_by_dedupe_key(dedupe_key)
        if existing:
            capped_lanes.append(lane_name)
            logger.info(
                "[PlannerTick] PLANNER_SKIP_DAILY_CAP lane=%r existing_task_id=%s existing_status=%s",
                lane_name, existing["id"], existing["status"],
            )
            continue

        # First eligible lane — create task
        slot_key = generate_task_slot_key()
        date_folder = today
        task_dir = os.path.join(db.ORCH_ROOT, "tasks", date_folder)
        os.makedirs(task_dir, exist_ok=True)
        prompt_path = os.path.join(task_dir, f"{slot_key}-prompt.md")

        output_filename = f"{lane_def['output_prefix']}_{today}.md"
        prompt_text = _build_forced_exploration_prompt(lane_def, today, output_filename)

        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt_text)

        task_id = db.create_task(
            slot_key=slot_key,
            date_folder=date_folder,
            title=lane_def["title"],
            slug=slot_key,
            status="QUEUED",
            prompt_file_path=prompt_path,
            prompt_text=prompt_text,
            dedupe_key=dedupe_key,
            task_type=task_type,
            worker_type="research",
            regime_state="exploration",
            epoch_id=0,
            focus_keys=f"forced_exploration,{lane_name}",
            signal_state_type=f"forced_exploration_{lane_name}",
        )

        msg = (
            f"Planner created forced exploration task #{task_id} "
            f"lane={lane_name!r} task_type={task_type!r} "
            f"dedupe_key={dedupe_key!r}"
        )
        logger.info("[PlannerTick] %s", msg)
        db.record_run(
            runner="planner_tick",
            outcome="SUCCESS",
            request_id=request_id,
            task_id=task_id,
            message=msg,
            tick_at=start_time.isoformat(),
        )
        return {
            "status": "CREATED",
            "task_id": task_id,
            "dedupe_key": dedupe_key,
            "lane": lane_name,
        }

    # All lanes have non-failed tasks today
    msg = (
        f"PLANNER_SKIP_FORCED_EXPLORATION_DAILY_CAP: 今日所有 forced exploration lanes 已建立。 "
        f"capped_lanes={capped_lanes}"
    )
    logger.info("[PlannerTick] %s", msg)
    db.record_run(
        runner="planner_tick",
        outcome="SKIPPED",
        request_id=request_id,
        message=msg,
        tick_at=start_time.isoformat(),
    )
    return {"status": "SKIP_ALL_LANES_CAPPED", "capped_lanes": capped_lanes}


# ── Phase 5: Exploration Result Router ───────────────────────────────────

_DECISION_ENUMS = frozenset([
    "WORTH_VALIDATION",
    "WATCH_ONLY",
    "REJECT_FOR_NOW",
    "INCONCLUSIVE_NEED_DATA",
])

_LANE_OUTPUT_PREFIX: dict[str, str] = {
    lane["name"]: lane["output_prefix"] for lane in _FORCED_EXPLORATION_LANES
}


def _find_research_report_path(source_task: dict, source_lane: str) -> str | None:
    """Attempt to locate the hypothesis report for a completed forced exploration task.

    Strategy (in order):
    1. Search completed_text / completed_file content for a 'research/...' path.
    2. Convention-based path: research/{output_prefix}_{YYYY-MM-DD}.md
    """
    import re

    dedupe_key = source_task.get("dedupe_key", "")
    # Extract YYYYMMDD from dedupe_key: forced_exploration:{lane}:{YYYYMMDD}
    parts = dedupe_key.split(":")
    date_ymd = parts[-1] if len(parts) >= 3 else ""
    date_dashed = (
        f"{date_ymd[:4]}-{date_ymd[4:6]}-{date_ymd[6:8]}"
        if len(date_ymd) == 8 else ""
    )

    # 1. Search completed_text or completed_file content for a research/ path
    for content_src in (source_task.get("completed_text"), _read_file_safe(source_task.get("completed_file_path"))):
        if not content_src:
            continue
        m = re.search(r'research/[\w/_-]+\.md', content_src)
        if m:
            candidate = os.path.join(db.ORCH_ROOT.replace("runtime/agent_orchestrator/", "").rstrip("/"), m.group(0))
            # ORCH_ROOT is relative; use REPO_ROOT
            candidate_abs = os.path.join(_REPO_ROOT, m.group(0))
            if os.path.exists(candidate_abs):
                return candidate_abs

    # 2. Convention-based
    output_prefix = _LANE_OUTPUT_PREFIX.get(source_lane, f"{source_lane}_hypothesis")
    if date_dashed:
        convention_path = os.path.join(_REPO_ROOT, "research", f"{output_prefix}_{date_dashed}.md")
        if os.path.exists(convention_path):
            return convention_path

    return None


def _read_file_safe(path: str | None) -> str | None:
    """Read file content safely; return None on any error."""
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def _parse_decision_from_report(report_content: str) -> str | None:
    """Extract the decision enum from a research hypothesis report.

    Looks for a '### 6. Decision' section and returns the first matching enum on the
    lines that follow it. Returns None if not found.
    """
    import re

    # Find the Decision section
    decision_section_match = re.search(
        r"###\s+6\.\s+Decision\s*\n(.*?)(?=\n###|\Z)",
        report_content,
        re.DOTALL | re.IGNORECASE,
    )
    if not decision_section_match:
        return None

    section_text = decision_section_match.group(1)
    for enum_val in ("WORTH_VALIDATION", "WATCH_ONLY", "REJECT_FOR_NOW", "INCONCLUSIVE_NEED_DATA"):
        if enum_val in section_text:
            return enum_val
    return None


def _build_validation_prompt(
    source_task: dict,
    source_lane: str,
    source_report_path: str,
    today: str,
) -> str:
    """Build a structured validation task prompt for a WORTH_VALIDATION exploration result."""
    report_rel = os.path.relpath(source_report_path, _REPO_ROOT) if source_report_path else "unknown"
    created_at = datetime.now(timezone.utc).isoformat()
    return (
        f"# [VALIDATION] Exploration Follow-up: {source_lane}\n\n"
        f"**Source Task ID:** {source_task['id']}\n"
        f"**Source Lane:** {source_lane}\n"
        f"**Source Decision:** WORTH_VALIDATION\n"
        f"**Source Report:** `{report_rel}`\n"
        f"**Created At:** {created_at}\n\n"
        f"---\n\n"
        f"## Objective\n\n"
        f"Formally validate the hypothesis documented in the source exploration report.\n"
        f"The exploration identified a potential edge in the **{source_lane}** domain "
        f"and recommended statistical validation before integration.\n\n"
        f"Read the source report at `{report_rel}` to understand the hypothesis, "
        f"required data, and minimal validation plan.\n\n"
        f"---\n\n"
        f"## Task\n\n"
        f"1. Re-read the source exploration report (Section 3: Required Data, "
        f"Section 4: Minimal Validation Plan, Section 5: Risk / Leakage Check).\n"
        f"2. Implement the Minimal Validation Plan as a reproducible script "
        f"or analysis notebook — no production changes.\n"
        f"3. Run the validation on historical data within the repository.\n"
        f"4. Report the primary metric (e.g., ROI delta, CLV proxy lift, hit rate improvement) "
        f"against the acceptance threshold defined in the exploration report.\n"
        f"5. Perform walk-forward isolation: training data must not overlap with validation data.\n"
        f"6. Confirm zero look-ahead leakage (no future data accessible at decision time).\n\n"
        f"---\n\n"
        f"## Constraints (Read-Only)\n\n"
        f"- **Read-only**: Do not modify any betting strategy, model weights, or active parameters.\n"
        f"- **No production deployment**: Do not push changes to any live betting system.\n"
        f"- **No betting strategy promotion**: Do not activate any new strategy or model.\n"
        f"- **No external betting API**: Do not call any sportsbook, exchange, or odds feed API "
        f"unless the source report explicitly lists it as a required read-only data source.\n"
        f"- **No live bets**: Do not place any bets or simulate live bet placement.\n"
        f"- **No bankroll changes**: Do not modify bankroll state, risk-cap, or Kelly fractions.\n"
        f"- **No LotteryNew**: Do not touch any LotteryNew draw logic, lottery number "
        f"generators, or lottery-domain files.\n\n"
        f"---\n\n"
        f"## Domain Vocabulary\n\n"
        f"Use only Betting-pool terms in your analysis and report:\n"
        f"market, match, odds, CLV, ROI, hit rate, drawdown, active betting strategy, "
        f"benchmark model, shadow model, walk-forward, backtest, leakage audit, "
        f"bankroll, risk-cap, no-bet rule, market regime, sample sufficiency.\n\n"
        f"---\n\n"
        f"## Required Outputs\n\n"
        f"1. **Validation Script / Notebook** (if applicable):\n"
        f"   - Reproducible, standalone script in `research/` or `scripts/`\n"
        f"   - Input: historical match data from `data/`\n"
        f"   - Output: metric table + statistical test result\n\n"
        f"2. **Validation Report** at:\n"
        f"   `research/{source_lane}_validation_{today}.md`\n\n"
        f"   Must contain:\n"
        f"   - Hypothesis restated\n"
        f"   - Dataset used (path, row count, date range)\n"
        f"   - Primary metric value vs. acceptance threshold\n"
        f"   - Statistical test result (p-value or confidence interval)\n"
        f"   - Walk-forward isolation confirmation\n"
        f"   - Leakage audit result\n"
        f"   - **Validation Decision**: one of:\n"
        f"     VALIDATED / REJECTED / INCONCLUSIVE_NEED_MORE_DATA / DEFERRED\n"
        f"   - Recommended next step (if VALIDATED)\n\n"
        f"---\n\n"
        f"## Fail Conditions\n\n"
        f"- Report does not include a Validation Decision enum\n"
        f"- Primary metric value not reported\n"
        f"- No statistical test conducted\n"
        f"- Walk-forward isolation not confirmed\n"
        f"- Look-ahead leakage detected\n"
        f"- Any production deployment or strategy activation performed\n"
        f"- LotteryNew terms appear in the output\n"
    )


_REPO_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def process_completed_exploration_tasks(
    request_id: str | None = None,
    start_time: datetime | None = None,
) -> dict:
    """Phase 5: Scan completed forced exploration tasks and route decisions.

    For each COMPLETED forced_exploration task that has not yet been routed:
      - Parse the Decision enum from the research report
      - WORTH_VALIDATION → create validation task (with dedupe) + record routing state
      - Other decisions → record routing state with appropriate route_status

    Returns a summary dict:
      {
        "processed": int,       # tasks newly routed
        "validation_created": int,
        "watch_recorded": int,
        "reject_recorded": int,
        "inconclusive_recorded": int,
        "parse_failed": int,
        "already_routed": int,
        "validation_task_ids": list[int],
      }
    """
    if request_id is None:
        import uuid
        request_id = str(uuid.uuid4())
    if start_time is None:
        start_time = datetime.now(timezone.utc)

    today = _common.dedupe_day_utc()
    summary: dict = {
        "processed": 0,
        "validation_created": 0,
        "watch_recorded": 0,
        "reject_recorded": 0,
        "inconclusive_recorded": 0,
        "parse_failed": 0,
        "already_routed": 0,
        "validation_task_ids": [],
    }

    # Fetch all completed forced_exploration tasks
    conn = db.get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM agent_tasks "
            "WHERE dedupe_key LIKE 'forced_exploration:%' AND status='COMPLETED' "
            "ORDER BY id ASC"
        ).fetchall()
        source_tasks = [dict(r) for r in rows]
    finally:
        conn.close()

    for source_task in source_tasks:
        source_task_id = source_task["id"]
        dedupe_key = source_task.get("dedupe_key", "")

        # Extract lane name from dedupe_key: forced_exploration:{lane}:{date}
        parts = dedupe_key.split(":")
        source_lane = parts[1] if len(parts) >= 2 else "unknown"

        # Skip if already routed
        existing_route = db.get_exploration_routing_state_by_source_task_id(source_task_id)
        if existing_route:
            logger.info(
                "[PlannerTick] PLANNER_SKIP_EXPLORATION_ALREADY_ROUTED "
                "source_task_id=%s route_status=%s",
                source_task_id, existing_route["route_status"],
            )
            summary["already_routed"] += 1
            continue

        # Locate research report
        report_path = _find_research_report_path(source_task, source_lane)
        report_content = _read_file_safe(report_path)

        # Parse decision
        decision = None
        if report_content:
            decision = _parse_decision_from_report(report_content)

        if not decision:
            logger.warning(
                "[PlannerTick] PARSE_FAILED: cannot parse decision from source_task_id=%s "
                "report_path=%r",
                source_task_id, report_path,
            )
            db.create_exploration_routing_state(
                source_task_id=source_task_id,
                source_lane=source_lane,
                source_dedupe_key=dedupe_key,
                source_report_path=report_path,
                decision=None,
                route_status="PARSE_FAILED",
            )
            summary["parse_failed"] += 1
            summary["processed"] += 1
            continue

        # Route by decision
        if decision == "WORTH_VALIDATION":
            # Check dedupe for validation task
            validation_dedupe_key = f"validation:{source_lane}:{today}"
            existing_validation = db.get_nonfailed_task_by_dedupe_key(validation_dedupe_key)
            if existing_validation:
                msg = (
                    f"PLANNER_SKIP_EXPLORATION_VALIDATION_DEDUPE: validation task already exists "
                    f"for dedupe_key={validation_dedupe_key!r} "
                    f"existing_task_id={existing_validation['id']}"
                )
                logger.info("[PlannerTick] %s", msg)
                db.create_exploration_routing_state(
                    source_task_id=source_task_id,
                    source_lane=source_lane,
                    source_dedupe_key=dedupe_key,
                    source_report_path=report_path,
                    decision=decision,
                    route_status="VALIDATION_CREATED",
                    validation_task_id=existing_validation["id"],
                )
                summary["validation_created"] += 1
                summary["validation_task_ids"].append(existing_validation["id"])
                summary["processed"] += 1
                continue

            # Create validation task
            slot_key = generate_task_slot_key()
            date_folder = today
            task_dir = os.path.join(db.ORCH_ROOT, "tasks", date_folder)
            os.makedirs(task_dir, exist_ok=True)
            prompt_path = os.path.join(task_dir, f"{slot_key}-prompt.md")
            prompt_text = _build_validation_prompt(source_task, source_lane, report_path or "", today)

            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(prompt_text)

            validation_task_id = db.create_task(
                slot_key=slot_key,
                date_folder=date_folder,
                title=f"[VALIDATION] Exploration follow-up ({source_lane}) — {today}",
                slug=slot_key,
                status="QUEUED",
                prompt_file_path=prompt_path,
                prompt_text=prompt_text,
                dedupe_key=validation_dedupe_key,
                task_type=f"validation_{source_lane}",
                worker_type="research",
                regime_state="validation",
                epoch_id=0,
                focus_keys=f"validation,{source_lane}",
                signal_state_type=f"validation_{source_lane}",
                previous_task_id=source_task_id,
            )

            db.create_exploration_routing_state(
                source_task_id=source_task_id,
                source_lane=source_lane,
                source_dedupe_key=dedupe_key,
                source_report_path=report_path,
                decision=decision,
                route_status="VALIDATION_CREATED",
                validation_task_id=validation_task_id,
            )

            msg = (
                f"PLANNER_CREATE_EXPLORATION_VALIDATION: "
                f"source_task_id={source_task_id} source_lane={source_lane!r} "
                f"decision=WORTH_VALIDATION → validation_task_id={validation_task_id} "
                f"dedupe_key={validation_dedupe_key!r}"
            )
            logger.info("[PlannerTick] %s", msg)
            db.record_run(
                runner="planner_tick",
                outcome="SUCCESS",
                request_id=request_id,
                task_id=validation_task_id,
                message=msg,
                tick_at=start_time.isoformat(),
            )
            summary["validation_created"] += 1
            summary["validation_task_ids"].append(validation_task_id)

        elif decision == "WATCH_ONLY":
            db.create_exploration_routing_state(
                source_task_id=source_task_id,
                source_lane=source_lane,
                source_dedupe_key=dedupe_key,
                source_report_path=report_path,
                decision=decision,
                route_status="WATCH_RECORDED",
            )
            summary["watch_recorded"] += 1

        elif decision == "REJECT_FOR_NOW":
            db.create_exploration_routing_state(
                source_task_id=source_task_id,
                source_lane=source_lane,
                source_dedupe_key=dedupe_key,
                source_report_path=report_path,
                decision=decision,
                route_status="REJECT_RECORDED",
            )
            summary["reject_recorded"] += 1

        elif decision == "INCONCLUSIVE_NEED_DATA":
            db.create_exploration_routing_state(
                source_task_id=source_task_id,
                source_lane=source_lane,
                source_dedupe_key=dedupe_key,
                source_report_path=report_path,
                decision=decision,
                route_status="INCONCLUSIVE_RECORDED",
            )
            summary["inconclusive_recorded"] += 1

        summary["processed"] += 1

    return summary


def _load_system_state_snapshot() -> dict:
    """從 DB 讀取目前系統狀態，安全降級為空 dict。"""
    try:
        return db.get_system_state_snapshot()
    except Exception:
        return {}


def _load_strategy_snapshot() -> str:
    """掃描 strategy_states_*.json，產出各遊戲策略表現快照。"""
    import glob
    lines: list[str] = []
    for path in sorted(glob.glob("lottery_api/data/strategy_states_*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            game = os.path.basename(path).replace("strategy_states_", "").replace(".json", "")
            count = len(data) if isinstance(data, dict) else 0
            edges = [
                v.get("short_term_edge", v.get("edge"))
                for v in data.values()
                if isinstance(v, dict)
            ]
            valid_edges = [e for e in edges if isinstance(e, (int, float))]
            best_edge = max(valid_edges) if valid_edges else None
            edge_str = f"+{best_edge:.3f}" if best_edge is not None else "N/A"
            lines.append(f"- **{game}**: {count} 策略, 短期最佳 edge={edge_str}")
        except Exception:
            continue
    return "\n".join(lines) if lines else "（無策略快照資料）"


def _build_task_contract(blueprint: dict) -> dict:
    """根據 blueprint 建立 per-task 驗收合約。"""
    return {
        "max_compute_hours": min(int(blueprint.get("expected_duration_hours", 2) or 2), 2),
        "max_major_objectives": 2,
        "max_dataset_count": 2,
        "task_kind": blueprint.get("task_kind", "audit"),
        "deliverable_kind": blueprint.get("deliverable_kind", "insight"),
        "required_output_fields": REQUIRED_OUTPUT_FIELDS,
        "forbidden_terms": ["NO_SIGNAL", "SIGNAL_EXHAUSTED", "signal_exhausted", "no_signal"],
        "focus_keys": blueprint.get("focus_keys", ""),
        "signal_state_type": blueprint.get("signal_state_type", ""),
        "expected_duration_hours": blueprint.get("expected_duration_hours", 2),
        "major_objectives": blueprint.get("major_objectives", [blueprint.get("objective", "")]),
        "dataset_paths": blueprint.get("dataset_paths", []),
    }


def _render_blueprint_prompt(blueprint: dict, generated_at: str, sys_state: Optional[dict] = None) -> str:
    sys_state = sys_state or {}
    regime = sys_state.get("regime_state") or "UNKNOWN"
    confidence = sys_state.get("confidence_snapshot")
    merge_rate = sys_state.get("recent_merge_rate")
    confidence_str = f"{confidence:.2f}" if confidence is not None else "N/A"
    merge_rate_str = f"{merge_rate:.1%}" if merge_rate is not None else "N/A"
    strategy_snapshot = _load_strategy_snapshot()
    datasets = blueprint.get("dataset_paths", [])
    steps = blueprint.get("steps", [])
    validation_checks = blueprint.get("validation_checks", [])
    output_template = {
        "violations": [
            {
                "code": "example_violation",
                "message": "說明違規或風險",
                "count": 0,
            }
        ],
        "metrics": {
            "baseline": {},
            "candidate": {},
            "delta": {},
        },
        "regime_counts": {},
        "leakage_detected": False,
        "candidate_fix": [
            {
                "target_file": "",
                "change_type": "",
                "expected_metric": "",
            }
        ],
    }
    rendered_steps = "\n".join(
        f"{index + 1}. {step}" for index, step in enumerate(steps)
    ) or "1. 盤點資料\n2. 執行分析\n3. 輸出 JSON 結果"
    rendered_checks = "\n".join(
        f"- {item}" for item in validation_checks
    ) or "- 需輸出結構化 JSON"
    dataset_lines = "\n".join(f"- {path}" for path in datasets) or "- （未指定）"
    optional_follow_up_section = ""
    if blueprint.get("optional_follow_up"):
        optional_follow_up_section = f"## 可選後續任務\n{blueprint['optional_follow_up']}\n\n"
    return f"""# 任務：{blueprint['title']}

## 背景
這是由 Betting-pool Orchestrator 自動產生的原子研究任務。任務必須可在 2 小時內完成，且能直接餵回 insight / patch loop。

## 當前系統狀態
| 項目 | 値 |
|------|-----|
| Regime | `{regime}` |
| 信心度 | {confidence_str} |
| 近期 merge rate | {merge_rate_str} |
| Signal State | `{blueprint.get('signal_state_type', 'N/A')}` |
| 任務型別 | `{blueprint.get('task_kind', 'audit')}` |
| 交付型別 | `{blueprint.get('deliverable_kind', 'insight')}` |
| 預期時長 | {blueprint.get('expected_duration_hours', 2)}h |

## 策略表現快照
{strategy_snapshot}

## 單一目標
{blueprint['objective']}

## 允許資料集（最多 2 個）
{dataset_lines}

## 執行步驟
{rendered_steps}

## 必要輸出
最終結果必須先輸出一個可解析的 JSON 物件，欄位固定如下；JSON 後面可以補充簡短說明，但不允許只有 Markdown 報告。

```json
{json.dumps(output_template, ensure_ascii=False, indent=2)}
```

## Loop Compatibility
1. `signal_state_type` 不可留空，必須可供 `insight_extractor -> patch_task_generator` 使用。
2. `candidate_fix` 若非空，必須可對應到實際檔案與可驗證的 metric。
3. 若沒有發現問題，也必須輸出空陣列 / 空物件，而不是純敘述結論。

## 驗證方法
{rendered_checks}

{optional_follow_up_section}

## 產生時間
{generated_at}
"""


def create_sample_task() -> dict:
    """建立可通過 atomic quality gate 的任務草稿。"""
    now = datetime.now(timezone.utc)
    date_folder = now.strftime("%Y%m%d")
    slot_key = generate_task_slot_key()
    recent_tasks = db.list_tasks(limit=len(TASK_BLUEPRINTS))
    recent_dedupe_keys = {str(task.get("dedupe_key") or "") for task in recent_tasks}
    blueprint = None
    for candidate in TASK_BLUEPRINTS:
        candidate_key = build_task_dedupe_key(candidate)
        if candidate_key not in recent_dedupe_keys:
            blueprint = candidate
            break
    if blueprint is None:
        blueprint = TASK_BLUEPRINTS[int(now.timestamp()) % len(TASK_BLUEPRINTS)]

    sys_state = _load_system_state_snapshot()
    prompt_text = _render_blueprint_prompt(blueprint, now.isoformat(), sys_state)
    dedupe_key = build_task_dedupe_key({**blueprint, "prompt_text": prompt_text})
    contract = _build_task_contract(blueprint)

    return {
        "slot_key": slot_key,
        "date_folder": date_folder,
        "title": blueprint["title"],
        "objective": blueprint["title"],
        "slug": slot_key,
        "prompt_file_path": "",
        "prompt_text": prompt_text,
        "focus_area": blueprint["focus_area"],
        "market_scope": blueprint["market_scope"],
        "analysis_family": blueprint["analysis_family"],
        "dedupe_key": dedupe_key,
        "regime_state": sys_state.get("regime_state"),
        "confidence_snapshot": sys_state.get("confidence_snapshot"),
        "contract_json": json.dumps(contract, ensure_ascii=False),
        "focus_keys": blueprint.get("focus_keys"),
        "signal_state_type": blueprint.get("signal_state_type"),
        "expected_duration_hours": blueprint.get("expected_duration_hours"),
    }


def persist_task_prompt(task_data: dict) -> dict:
    """通過 quality gate 後才把 prompt 寫入檔案系統。"""
    task_dir = os.path.join(db.ORCH_ROOT, "tasks", task_data["date_folder"])
    os.makedirs(task_dir, exist_ok=True)

    prompt_path = os.path.join(task_dir, f"{task_data['slot_key']}-prompt.md")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(task_data["prompt_text"])

    persisted = dict(task_data)
    persisted["prompt_file_path"] = prompt_path
    return persisted


def normalize_task_draft(task_data: dict) -> dict:
    normalized = dict(task_data)
    normalized.setdefault("objective", normalized.get("title") or normalized.get("objective"))
    normalized.setdefault("dedupe_key", build_task_dedupe_key(normalized))
    return normalized


def _build_task_from_candidate(candidate: dict) -> dict:
    """從候選 dict（blueprint 或 wiki-mined）建立任務草稿，邏輯同 create_sample_task。"""
    now = datetime.now(timezone.utc)
    date_folder = now.strftime("%Y%m%d")
    slot_key = generate_task_slot_key()
    sys_state = _load_system_state_snapshot()
    # If candidate already has a rendered prompt_text, use it; otherwise render from blueprint fields
    if candidate.get("prompt_text"):
        prompt_text = candidate["prompt_text"]
    else:
        prompt_text = _render_blueprint_prompt(candidate, now.isoformat(), sys_state)
    dedupe_key = build_task_dedupe_key({**candidate, "prompt_text": prompt_text})
    contract = _build_task_contract(candidate)
    return {
        "slot_key": slot_key,
        "date_folder": date_folder,
        "title": candidate["title"],
        "objective": candidate.get("objective", candidate["title"]),
        "slug": slot_key,
        "prompt_file_path": "",
        "prompt_text": prompt_text,
        "focus_area": candidate.get("focus_area", "general"),
        "market_scope": candidate.get("market_scope", "general"),
        "analysis_family": candidate.get("analysis_family", "inventory-research"),
        "dedupe_key": dedupe_key,
        "regime_state": sys_state.get("regime_state"),
        "confidence_snapshot": sys_state.get("confidence_snapshot"),
        "contract_json": json.dumps(contract, ensure_ascii=False),
        "focus_keys": candidate.get("focus_keys"),
        "signal_state_type": candidate.get("signal_state_type"),
        "expected_duration_hours": candidate.get("expected_duration_hours"),
    }


def _recover_replan_required() -> dict:
    """
    REPLAN recovery policy:
    - 若 REPLAN_REQUIRED 任務超過閾值，將最舊的批量設為 ARCHIVED（跳過，不再干擾 planner）
    - 回傳: {"archived_count": int, "kept_count": int}
    """
    replan_tasks = db.list_tasks(status="REPLAN_REQUIRED", limit=50)
    if len(replan_tasks) <= REPLAN_ARCHIVE_THRESHOLD:
        return {"archived_count": 0, "kept_count": len(replan_tasks)}

    # 按建立時間排序，保留最新 1 個，其餘歸檔
    sorted_tasks = sorted(replan_tasks, key=lambda t: t.get("created_at") or "", reverse=True)
    to_keep = sorted_tasks[:1]
    to_archive = sorted_tasks[1:]

    archived_count = 0
    for task in to_archive:
        try:
            db.update_task(task["id"], status="ARCHIVED",
                           log_snippet=f"[REPLAN_RECOVERY] Archived: exceeded threshold ({len(replan_tasks)} REPLAN_REQUIRED tasks)")
            archived_count += 1
            logger.info("[PlannerTick] REPLAN_RECOVERY: archived task #%s", task["id"])
        except Exception as exc:
            logger.warning("[PlannerTick] REPLAN_RECOVERY: failed to archive task #%s: %s", task["id"], exc)

    return {"archived_count": archived_count, "kept_count": len(to_keep)}


def _mine_tasks_from_wiki() -> list[dict]:
    """
    從 wiki/ 文件與 MLB evidence 文件挖掘候選任務草案。
    Profile: atomic loop-compatible MLB task generation
    每個候選需包含: title, objective, focus_area, analysis_family, expected_duration_hours
    最多回傳 MINING_MAX_CANDIDATES 個。
    """
    static_candidates = [
        _make_atomic_blueprint(
            focus_area="mlb-clv-external-coverage",
            market_scope="MLB pregame odds timeline",
            analysis_family="odds-atomic",
            title="MLB 外部收盤覆蓋率快照",
            objective="量化外部收盤資料覆蓋率，輸出缺口 league / month 與違規樣本數。",
            focus_keys="mlb_clv,external_closing,coverage",
            signal_state_type="deep_research_odds_quality",
            task_kind="audit",
            deliverable_kind="violation_count",
            dataset_paths=[
                "data/mlb_context/external_closing_state.json",
                "data/mlb_context/odds_timeline.jsonl",
            ],
            steps=[
                "計算外部收盤覆蓋率。",
                "列出缺口最大的 league / month。",
                "輸出 violations 與 candidate_fix。",
            ],
            validation_checks=["不得混入 Monte Carlo 或 proxy proposal。"],
        ),
        _make_atomic_blueprint(
            focus_area="mlb-feedback-settlement-completeness",
            market_scope="MLB paper settlement",
            analysis_family="feedback-atomic",
            title="MLB 結算完整性審計",
            objective="量化已結算與未結算比例，輸出可供 feedback loop 修補的違規清單。",
            focus_keys="mlb_feedback,settlement,completeness",
            signal_state_type="deep_research_feedback",
            task_kind="audit",
            deliverable_kind="violation_count",
            dataset_paths=[
                "research/trade_ledger.jsonl",
                "research/roi_tracking.json",
            ],
            steps=[
                "統計已結算 / 未結算比例。",
                "列出缺失欄位與違規樣本數。",
                "輸出 JSON 結果。",
            ],
            validation_checks=["若無缺口也要輸出空 violations。"],
        ),
        _make_atomic_blueprint(
            focus_area="mlb-feature-missingness-simulation",
            market_scope="MLB moneyline / totals pregame",
            analysis_family="feature-atomic",
            title="MLB Feature Missingness Monte Carlo Sensitivity",
            objective="單獨模擬特徵缺失率對 metrics 的影響，不混入審計與 patch proposal。",
            focus_keys="mlb_features,monte_carlo,missingness",
            signal_state_type="deep_research_feature",
            task_kind="simulation",
            deliverable_kind="metric_delta",
            dataset_paths=[
                "data/wbc_backend/reports/mlb_decision_quality_report.json",
                "research/roi_tracking.json",
            ],
            steps=[
                "建立 10% / 30% / 50% 缺失率模擬情境。",
                "計算 metrics.delta 與 regime_counts。",
                "輸出 machine-readable JSON。",
            ],
            validation_checks=["simulation 任務不得要求最終推薦。"],
        ),
    ]

    # 讀取 wiki 文件，確認候選仍然相關（MLB evidence 文件存在才補充動態提示）
    relevant_keys: dict[str, bool] = {}
    for src_path in WIKI_MINING_SOURCES:
        full_path = _REPO_ROOT / src_path
        relevant_keys[src_path] = full_path.exists()

    # 確認 MLB evidence 文件存在，記錄可用性
    available_evidence: list[str] = []
    for src_path in MLB_EVIDENCE_SOURCES:
        full_path = _REPO_ROOT / src_path
        if full_path.exists():
            available_evidence.append(src_path)
    if available_evidence:
        logger.debug("[PlannerTick] Available MLB evidence files: %s", available_evidence)

    # 動態補充：掃描 wiki 文件中的 TODO / Remediation 行，提取額外 MLB 相關線索
    extra_hints: list[str] = []
    for src_path in WIKI_MINING_SOURCES:
        full_path = _REPO_ROOT / src_path
        if not full_path.exists():
            continue
        try:
            text = full_path.read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                stripped = line.strip()
                if re.search(r"(?i)\b(TODO|Remediation|FIXME|MIGRATE|CLEANUP|AUDIT)\b", stripped):
                    extra_hints.append(f"{src_path}: {stripped[:120]}")
        except OSError:
            pass

    if extra_hints:
        logger.debug("[PlannerTick] wiki mining found %d hint lines: %s", len(extra_hints), extra_hints[:5])

    return static_candidates[:MINING_MAX_CANDIDATES]


def _resolve_previous_task_blocker(latest: dict) -> Optional[str]:
    """
    前置封鎖守衛：檢查最新任務是否阻止 Planner 繼續。
    回傳 blocker 描述字串；None 表示允許繼續。

    封鎖規則（對齊 LotteryNew，適配本系統）：
    - RUNNING / QUEUED → 封鎖（不堆疊任務）
    - BLOCKED_ENV + 年齡 < 600s → 封鎖（給環境時間自我恢復）
    - BLOCKED_ENV + 年齡 ≥ 600s → 自動解除：
        · error_message 含 rate limit 關鍵字 → FAILED_RATE_LIMIT
        · 否則 → FAILED
        → 解除後允許 Planner 繼續
    - _TERMINAL_TASK_STATUSES 或 None → 允許
    """
    if not latest:
        return None

    status = latest.get("status", "")
    if status in _TERMINAL_TASK_STATUSES:
        return None

    if status in ("RUNNING", "QUEUED"):
        # ── 殭屍任務偵測：RUNNING 但超過容許時間未完成 ──────────────────────
        # 原因：Worker 行程崩潰或從未正確啟動，任務永久卡在 RUNNING。
        # 條件：age ≥ max(expected_duration × 3600 + 3600, 7200)（預期時長 + 1h 緩衝，最少 2h）
        if status == "RUNNING":
            ts_str = (
                latest.get("started_at")
                or latest.get("updated_at")
                or latest.get("created_at")
                or ""
            )
            age_seconds = 0.0
            if ts_str:
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                    age_seconds = (datetime.now(timezone.utc) - ts).total_seconds()
                except ValueError:
                    pass

            expected_hours = float(latest.get("expected_duration_hours") or 2.0)
            zombie_timeout = max(expected_hours * 3600 + 3600, 7200)

            if age_seconds >= zombie_timeout:
                db.update_task(
                    latest["id"],
                    status="FAILED",
                    error_message=(
                        f"[PLANNER_AUTO_RESOLVE] RUNNING → FAILED (zombie): "
                        f"no completion after {int(age_seconds)}s "
                        f"(timeout={int(zombie_timeout)}s, expected={expected_hours}h). "
                        + (latest.get("error_message") or "")
                    )[:500],
                )
                logger.warning(
                    "[PlannerTick] PLANNER_RESOLVED_ZOMBIE_RUNNING: task #%s "
                    "RUNNING → FAILED (age=%ds, timeout=%ds)",
                    latest["id"], int(age_seconds), int(zombie_timeout),
                )
                return None  # 允許 Planner 繼續
        # ──────────────────────────────────────────────────────────────────────
        return (
            f"PLANNER_SKIP_PREV_RUNNING: task #{latest['id']} is {status}"
        )

    if status == "BLOCKED_ENV":
        # 計算任務年齡（依優先序取時間戳）
        ts_str = (
            latest.get("updated_at")
            or latest.get("completed_at")
            or latest.get("started_at")
            or latest.get("created_at")
            or ""
        )
        age_seconds = 0.0
        if ts_str:
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                age_seconds = (datetime.now(timezone.utc) - ts).total_seconds()
            except ValueError:
                pass

        if age_seconds < 600:
            return (
                f"PLANNER_SKIP_PREV_RUNNING: task #{latest['id']} is BLOCKED_ENV "
                f"(age={int(age_seconds)}s < 600s)"
            )

        # 自動解除：判斷是否為 rate limit 類型
        err = (latest.get("error_message") or "").lower()
        new_status = (
            "FAILED_RATE_LIMIT"
            if any(m in err for m in _RATE_LIMIT_MARKERS)
            else "FAILED"
        )
        db.update_task(
            latest["id"],
            status=new_status,
            error_message=(
                f"[PLANNER_AUTO_RESOLVE] BLOCKED_ENV → {new_status} "
                f"after {int(age_seconds)}s. "
                + (latest.get("error_message") or "")
            )[:500],
        )
        logger.info(
            "[PlannerTick] PLANNER_RESOLVED_STALE_BLOCKED_ENV: task #%s "
            "BLOCKED_ENV → %s (age=%ds)",
            latest["id"], new_status, int(age_seconds),
        )
        return None  # 允許 Planner 繼續

    # 其他未知狀態：保守放行（安全降級）
    return None


def run_planner_tick() -> dict:
    """執行 Planner Tick"""
    start_time = datetime.now(timezone.utc)
    request_id = os.environ.get("ORCHESTRATOR_REQUEST_ID") or str(uuid.uuid4())
    
    logger.info(f"[PlannerTick] Starting planner tick, request_id={request_id}")
    
    try:
        decision = execution_policy.evaluate_execution(
            runner="planner_tick",
            background=True,
            manual_override=execution_policy.is_manual_run(os.environ),
        )
        if not decision["allowed"]:
            message = decision["message"]
            db.record_run(
                runner="planner_tick",
                outcome="SKIPPED",
                request_id=request_id,
                message=message,
                tick_at=start_time.isoformat()
            )
            logger.info(f"[PlannerTick] {message}")
            return {"status": "SKIPPED", "message": message}

        # ── STEP 0: REPLAN recovery ──
        recovery = _recover_replan_required()
        if recovery["archived_count"] > 0:
            logger.info("[PlannerTick] REPLAN_RECOVERY: archived %d stale tasks", recovery["archived_count"])

        # ── STEP 0.5: MLB 閉迴圈 — 提取洞見，生成 patch / validation 候選 ──
        try:
            new_insights = insight_extractor.extract_insights_from_completed_tasks()
            if new_insights:
                logger.info("[PlannerTick] Extracted %d new MLB insights", len(new_insights))
        except Exception as _ie_exc:
            logger.warning("[PlannerTick] Insight extraction failed (non-fatal): %s", _ie_exc)
            new_insights = []

        _patch_candidates: list[dict] = []
        _validation_candidates: list[dict] = []  # now empty: validation runs directly in STEP 0.6
        try:
            _pending = insight_extractor.get_pending_insights()
            _patch_candidates = patch_task_generator.generate_patch_tasks(_pending)
        except Exception as _pg_exc:
            logger.warning("[PlannerTick] Patch candidate gen failed (non-fatal): %s", _pg_exc)

        # ── STEP 0.6: Auto-validate PATCH_QUEUED insights whose patch task is COMPLETED ──
        # Runs patch_validator.run_patch_validation() synchronously — no new DB task required.
        # Idempotent: get_patch_queued_insights() only returns status=PATCH_QUEUED entries;
        # once validation transitions the insight to VALIDATED/PARTIAL/FAILED it never re-runs.
        _auto_validated: list[str] = []
        try:
            for _ins in insight_extractor.get_patch_queued_insights():
                # Extra guard: skip if insight already has a validation timestamp
                if _ins.get("validated_at") or _ins.get("partial_at"):
                    logger.debug(
                        "[PlannerTick] Insight %s already has validation timestamp, skipping",
                        _ins.get("id"),
                    )
                    continue
                _patch_task_id = _ins.get("patch_task_id")
                if not _patch_task_id:
                    continue
                _pt = db.get_task(int(_patch_task_id))
                if not _pt or _pt.get("status") != "COMPLETED":
                    continue
                logger.info(
                    "[PlannerTick] Auto-validating insight %s (patch task #%s)",
                    _ins.get("id"), _patch_task_id,
                )
                _vr = patch_validator.run_patch_validation(_pt, _ins)
                _auto_validated.append(str(_ins.get("id")))
                logger.info(
                    "[PlannerTick] Validation done: insight %s → decision=%s  "
                    "Brier_before=%.4f  Brier_after=%.4f",
                    _ins.get("id"),
                    _vr.get("decision"),
                    _vr.get("before_metrics", {}).get("brier_score", float("nan")),
                    _vr.get("after_metrics", {}).get("brier_score", float("nan")),
                )
        except Exception as _av_exc:
            logger.warning("[PlannerTick] Auto-validation failed (non-fatal): %s", _av_exc)
        if _auto_validated:
            logger.info("[PlannerTick] Auto-validated %d insights: %s", len(_auto_validated), _auto_validated)

        # ── STEP 1: 前置封鎖守衛（RUNNING / QUEUED / BLOCKED_ENV 自動解除）──
        latest_task = db.get_latest_task()
        blocker = _resolve_previous_task_blocker(latest_task)
        if blocker:
            message = f"Planner skipped: {blocker}"
            db.record_run(
                runner="planner_tick",
                outcome="SKIPPED",
                request_id=request_id,
                task_id=latest_task["id"] if latest_task else None,
                message=message,
                tick_at=start_time.isoformat(),
            )
            logger.info("[PlannerTick] %s", message)
            return {
                "status": "SKIPPED",
                "outcome": "PLANNER_SKIP_PREV_RUNNING",
                "message": message,
                "blocking_task_id": latest_task["id"] if latest_task else None,
            }

        # ── STEP 2: 建立候選列表（blueprints 優先，再試 wiki-mined tasks）──
        # 包含 cooldown 時間內已完成的任務（防止 stub 執行時任務被立即重建）
        cooldown_hours = int(db.get_setting("task_recycle_cooldown_hours", "4"))
        from datetime import timedelta
        cutoff_iso = (datetime.now(timezone.utc) - timedelta(hours=cooldown_hours)).isoformat()
        all_recent = db.list_tasks(limit=100)
        recent_tasks = [
            t for t in all_recent
            if t.get("status") not in ("ARCHIVED", "CANCELLED")
            and not (
                t.get("status") == "COMPLETED"
                and (t.get("completed_at") or "") < cutoff_iso
            )
        ]

        # 先嘗試 blueprints（隨機輪換，避免永遠試同一個）
        import random
        blueprints = list(TASK_BLUEPRINTS)
        random.shuffle(blueprints)
        wiki_candidates = _mine_tasks_from_wiki()
        # 優先順序：validation > patch > audit blueprints > wiki candidates
        all_candidates = _validation_candidates + _patch_candidates + blueprints + wiki_candidates

        last_verdict = None
        blocked_by_recent_count = 0
        duplicate_rejection_count = 0
        non_duplicate_rejection_count = 0
        for candidate in all_candidates:
            _insight_id = candidate.get("insight_id")  # only set for patch/validation tasks
            task_data = normalize_task_draft(_build_task_from_candidate(candidate))

            # ── 前置去重：依 focus_area + analysis_family 快速排除 ──────────
            # （quality_gate 的 text-similarity 無法解析 current task 的 family，
            #   故在此用 dict 欄位直接比對）
            task_focus = task_data.get("focus_area", "")
            task_family = task_data.get("analysis_family", "")
            task_title = task_data.get("title", "")
            if task_focus and task_family:
                already_recent = any(
                    t.get("focus_area") == task_focus
                    and t.get("analysis_family") == task_family
                    for t in recent_tasks
                )
            else:
                already_recent = any(t.get("title") == task_title for t in recent_tasks)
            if already_recent:
                blocked_by_recent_count += 1
                logger.info(
                    "[PlannerTick] Candidate '%s' skipped: already in recent_tasks (focus=%s, family=%s)",
                    task_title, task_focus, task_family,
                )
                continue

            quality_verdict = evaluate_task_quality(task_data, recent_tasks=recent_tasks)
            last_verdict = quality_verdict

            if quality_verdict.passed:
                # 通過品質驗收
                task_data = persist_task_prompt(task_data)
                task_id = db.create_task(**task_data)

                # 更新洞見生命週期
                _family = task_data.get("analysis_family", "")
                if _insight_id:
                    try:
                        if _family.startswith("model-patch-"):
                            insight_extractor.mark_insight_patch_queued(_insight_id, task_id)
                        elif _family.startswith("model-validation-"):
                            insight_extractor.mark_insight_validated(_insight_id, task_id)
                    except Exception as _lc_exc:
                        logger.warning("[PlannerTick] Insight lifecycle update failed (non-fatal): %s", _lc_exc)

                end_time = datetime.now(timezone.utc)
                duration = int((end_time - start_time).total_seconds())

                message = f"Planner created new task #{task_id}: {task_data['title']}"
                db.record_run(
                    runner="planner_tick",
                    outcome="SUCCESS",
                    request_id=request_id,
                    task_id=task_id,
                    message=message,
                    tick_at=start_time.isoformat(),
                    duration_seconds=duration,
                )
                logger.info("[PlannerTick] Created task #%s: %s", task_id, task_data["title"])
                return {
                    "status": "SUCCESS",
                    "quality_status": quality_verdict.quality_status,
                    "message": message,
                    "task_id": task_id,
                    "objective": task_data["title"],
                    "duration_seconds": duration,
                    "replan_recovered": recovery["archived_count"],
                }
            else:
                duplicate_only_rejection = (
                    quality_verdict.rejection_reasons
                    and all(reason.startswith("重複性檢查") for reason in quality_verdict.rejection_reasons)
                )
                if duplicate_only_rejection:
                    duplicate_rejection_count += 1
                else:
                    non_duplicate_rejection_count += 1
                logger.info(
                    "[PlannerTick] Candidate '%s' rejected: %s",
                    candidate.get("title", "?"),
                    quality_verdict.rejection_reasons,
                )

        # ── STEP 3: 所有候選都失敗 ──
        # Phase 4: 先嘗試 forced exploration（daily cap per lane，rotation）
        _explore = _attempt_forced_exploration(request_id, start_time)
        if _explore["status"] == "CREATED":
            end_time = datetime.now(timezone.utc)
            duration = int((end_time - start_time).total_seconds())
            return {
                "status": "SUCCESS",
                "quality_status": "FORCED_EXPLORATION",
                "message": (
                    f"Planner created forced exploration task #{_explore['task_id']} "
                    f"lane={_explore['lane']!r}"
                ),
                "task_id": _explore["task_id"],
                "lane": _explore["lane"],
                "objective": _explore.get("dedupe_key", ""),
                "duration_seconds": duration,
            }

        # Phase 3: 所有 exploration lanes 已滿 → fallback 到 maintenance_health_check
        _maint = _attempt_maintenance_task(request_id, start_time)
        if _maint["status"] == "CREATED":
            end_time = datetime.now(timezone.utc)
            duration = int((end_time - start_time).total_seconds())
            return {
                "status": "SUCCESS",
                "quality_status": "MAINTENANCE",
                "message": f"Planner created maintenance task #{_maint['task_id']}: [MAINTENANCE] Orchestration health check",
                "task_id": _maint["task_id"],
                "objective": "[MAINTENANCE] Orchestration health check",
                "duration_seconds": duration,
            }
        elif _maint["status"] == "SKIP_DAILY_CAP":
            # Phase 5: forced exploration capped + maintenance capped
            # → process completed exploration results → create validation task if needed
            _routing = process_completed_exploration_tasks(request_id, start_time)
            if _routing["validation_created"] > 0:
                end_time = datetime.now(timezone.utc)
                duration = int((end_time - start_time).total_seconds())
                vt_ids = _routing["validation_task_ids"]
                return {
                    "status": "SUCCESS",
                    "quality_status": "EXPLORATION_ROUTING",
                    "message": (
                        f"Planner created {_routing['validation_created']} validation task(s) "
                        f"from completed exploration results: {vt_ids}"
                    ),
                    "validation_task_ids": vt_ids,
                    "routing_summary": _routing,
                    "duration_seconds": duration,
                }
            # All lanes capped, maintenance capped, no new validation tasks → idle
            end_time = datetime.now(timezone.utc)
            duration = int((end_time - start_time).total_seconds())
            idle_msg = "PLANNER_IDLE_NO_ELIGIBLE_TASK: 目前沒有合格任務，排程正常待命。"
            logger.info("[PlannerTick] %s", idle_msg)
            db.record_run(
                runner="planner_tick",
                outcome="SKIPPED",
                request_id=request_id,
                message=idle_msg,
                tick_at=start_time.isoformat(),
                duration_seconds=duration,
            )
            return {
                "status": "SKIPPED",
                "outcome": "PLANNER_IDLE_NO_ELIGIBLE_TASK",
                "message": idle_msg,
                "skip_daily_cap_task_id": _maint["task_id"],
                "routing_summary": _routing,
                "duration_seconds": duration,
            }

        end_time = datetime.now(timezone.utc)
        duration = int((end_time - start_time).total_seconds())

        duplicate_blocked_total = blocked_by_recent_count + duplicate_rejection_count
        if all_candidates and duplicate_blocked_total == len(all_candidates) and non_duplicate_rejection_count == 0:
            message = (
                f"Planner skipped: all {len(all_candidates)} candidates blocked by recent-task "
                f"cooldown / duplicate gate ({cooldown_hours}h window)"
            )
            log_snippet = (
                f"blocked_by_recent={blocked_by_recent_count}\n"
                f"blocked_by_duplicate={duplicate_rejection_count}\n"
                f"cooldown_hours={cooldown_hours}"
            )
            db.record_run(
                runner="planner_tick",
                outcome="SKIPPED",
                request_id=request_id,
                message=message,
                log_snippet=log_snippet,
                tick_at=start_time.isoformat(),
                duration_seconds=duration,
            )
            logger.info("[PlannerTick] %s", message)
            return {
                "status": "SKIPPED",
                "quality_status": "SKIP",
                "message": message,
                "blocked_by_recent": blocked_by_recent_count,
                "blocked_by_duplicate": duplicate_rejection_count,
                "cooldown_hours": cooldown_hours,
                "duration_seconds": duration,
            }

        rejection_reasons = last_verdict.rejection_reasons if last_verdict else ["no candidates"]
        message = f"Planner rejected all {len(all_candidates)} candidates by quality gate"
        db.record_run(
            runner="planner_tick",
            outcome="REJECTED",
            request_id=request_id,
            message=message,
            log_snippet="\n".join(rejection_reasons),
            tick_at=start_time.isoformat(),
            duration_seconds=duration,
        )
        logger.info("[PlannerTick] %s: %s", message, rejection_reasons)
        return {
            "status": "REJECTED",
            "quality_status": last_verdict.quality_status if last_verdict else "UNKNOWN",
            "message": message,
            "rejection_reasons": rejection_reasons,
            "criteria_results": last_verdict.criteria_results if last_verdict else {},
            "candidates_tried": len(all_candidates),
            "duration_seconds": duration,
        }
        
    except Exception as e:
        end_time = datetime.now(timezone.utc)
        duration = int((end_time - start_time).total_seconds())
        
        error_message = f"Planner failed: {str(e)}"
        db.record_run(
            runner="planner_tick",
            outcome="FAILED",
            request_id=request_id,
            message=error_message,
            tick_at=start_time.isoformat(),
            duration_seconds=duration
        )
        
        logger.error(f"[PlannerTick] Failed: {e}")
        
        return {
            "status": "FAILED",
            "message": error_message,
            "duration_seconds": duration
        }


if __name__ == "__main__":
    # 直接測試執行
    logging.basicConfig(level=logging.INFO)
    db.init_db()
    result = run_planner_tick()
    print(f"Planner tick result: {result}")
