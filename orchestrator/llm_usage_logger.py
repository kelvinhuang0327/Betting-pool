"""
orchestrator/llm_usage_logger.py

Phase 0 — 結構化 LLM 使用量 JSONL 記錄器。

每次 LLM 呼叫（允許或封鎖）都寫入一行 JSON 到：
    runtime/agent_orchestrator/llm_usage.jsonl

設計原則：
- 非同步安全（append-mode 寫入，不鎖檔）
- 不引入外部套件
- 所有例外皆為非致命（寫入失敗不中斷執行流程）
- 超過 _MAX_FILE_BYTES（50 MB）時自動輪轉為 .1
"""
from __future__ import annotations

import json
import os
import traceback
import uuid
from datetime import datetime, timezone
from typing import Optional

_LOG_PATH: str = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "runtime",
    "agent_orchestrator",
    "llm_usage.jsonl",
)
_MAX_FILE_BYTES: int = 50 * 1024 * 1024  # 50 MB


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_caller_stack(skip_frames: int = 3) -> list[str]:
    """取得精簡的呼叫堆疊（略去此函式本身及 skip_frames 個框架）。"""
    frames = traceback.extract_stack()
    # 排除 log_llm_event → _get_caller_stack 本身的 frames，再排 skip_frames
    cutoff = max(0, len(frames) - skip_frames)
    return [
        f"{f.filename}:{f.lineno} in {f.name}"
        for f in frames[:cutoff]
    ]


def _rotate_if_needed(path: str) -> None:
    """若 JSONL 超過 _MAX_FILE_BYTES 則輪轉（舊檔改名為 .1）。"""
    try:
        if os.path.exists(path) and os.path.getsize(path) > _MAX_FILE_BYTES:
            rotated = path + ".1"
            if os.path.exists(rotated):
                os.remove(rotated)
            os.rename(path, rotated)
    except OSError:
        pass


def log_llm_event(
    *,
    runner: str,
    provider: str,
    blocked: bool,
    block_reason: Optional[str] = None,
    task_id: Optional[int] = None,
    correlation_id: Optional[str] = None,
    entrypoint: Optional[str] = None,
    model: Optional[str] = None,
    command: Optional[str] = None,
    requires_llm: bool = True,
    allowed_by_policy: bool = True,
    success: Optional[bool] = None,
    error: Optional[str] = None,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    caller_skip_frames: int = 3,
) -> None:
    """
    寫入一筆 LLM 使用量記錄至 llm_usage.jsonl。

    Args:
        runner:           呼叫者身份，例如 "planner", "worker", "cto", "copilot_daemon"
        provider:         LLM 提供者，例如 "codex", "claude", "copilot"
        blocked:          True = 此次呼叫被封鎖
        block_reason:     封鎖原因代碼（blocked=True 時必填）
        task_id:          關聯的任務 ID（可選）
        correlation_id:   跨系統追蹤 ID，未提供時自動生成
        entrypoint:       呼叫進入點描述
        model:            實際使用的模型名稱
        command:          執行的指令（可選，敏感資訊應省略）
        requires_llm:     此任務是否需要 LLM
        allowed_by_policy: 政策層面是否允許
        success:          執行結果（None = 尚未知道）
        error:            錯誤訊息（執行失敗時）
        input_tokens:     輸入 tokens 數量
        output_tokens:    輸出 tokens 數量
        caller_skip_frames: 堆疊追蹤時要跳過的框架數
    """
    record: dict = {
        "timestamp": _utc_now_iso(),
        "correlation_id": correlation_id or str(uuid.uuid4()),
        "task_id": task_id,
        "runner": runner,
        "entrypoint": entrypoint,
        "provider": provider,
        "model": model,
        "command": command,
        "caller_stack": _get_caller_stack(skip_frames=caller_skip_frames),
        "requires_llm": requires_llm,
        "allowed_by_policy": allowed_by_policy,
        "blocked": blocked,
        "block_reason": block_reason,
        "success": success,
        "error": error,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }
    try:
        os.makedirs(os.path.dirname(_LOG_PATH), exist_ok=True)
        _rotate_if_needed(_LOG_PATH)
        with open(_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError:
        pass  # 寫入失敗為非致命錯誤，不中斷執行流程
