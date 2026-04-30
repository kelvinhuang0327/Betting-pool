#!/usr/bin/env python3
"""
scripts/llm_usage_recent.py

Phase 0 — LLM 使用量近期記錄查詢 CLI。

用法：
    python3 scripts/llm_usage_recent.py --hours 24
    python3 scripts/llm_usage_recent.py --runner planner
    python3 scripts/llm_usage_recent.py --runner worker --provider codex --hours 1
    python3 scripts/llm_usage_recent.py --blocked-only
    python3 scripts/llm_usage_recent.py --json

選項：
    --hours N       查詢最近 N 小時（預設：24）
    --runner NAME   篩選 runner（planner / worker / cto / copilot_daemon）
    --provider NAME 篩選 provider（codex / claude / copilot 等）
    --blocked-only  只顯示被封鎖的記錄
    --json          以 JSON 格式輸出原始記錄（不輸出摘要）
    --tail N        顯示最新 N 筆記錄（搭配 --json）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional

_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "runtime",
    "agent_orchestrator",
    "llm_usage.jsonl",
)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="查詢 llm_usage.jsonl 近期 LLM 使用量記錄",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--hours", type=float, default=24.0, help="查詢最近 N 小時（預設 24）")
    p.add_argument("--runner", type=str, default=None, help="篩選 runner")
    p.add_argument("--provider", type=str, default=None, help="篩選 provider")
    p.add_argument("--blocked-only", action="store_true", help="只顯示被封鎖的記錄")
    p.add_argument("--json", action="store_true", dest="json_out", help="輸出 JSON 格式")
    p.add_argument("--tail", type=int, default=None, help="僅顯示最新 N 筆（搭配 --json）")
    return p.parse_args()


def _load_records(
    cutoff: datetime,
    runner_filter: Optional[str],
    provider_filter: Optional[str],
    blocked_only: bool,
) -> list[dict]:
    if not os.path.exists(_LOG_PATH):
        return []

    records: list[dict] = []
    with open(_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            ts_str = rec.get("timestamp", "")
            try:
                ts = datetime.fromisoformat(ts_str)
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
            except (ValueError, AttributeError):
                continue

            if ts < cutoff:
                continue
            if runner_filter and rec.get("runner", "").lower() != runner_filter.lower():
                continue
            if provider_filter and rec.get("provider", "").lower() != provider_filter.lower():
                continue
            if blocked_only and not rec.get("blocked", False):
                continue

            records.append(rec)

    return records


def _summarize(records: list[dict]) -> None:
    total = len(records)
    allowed = sum(1 for r in records if not r.get("blocked"))
    blocked = sum(1 for r in records if r.get("blocked"))

    # 按 runner 統計
    by_runner: dict[str, dict[str, int]] = {}
    for r in records:
        runner = r.get("runner") or "unknown"
        if runner not in by_runner:
            by_runner[runner] = {"allowed": 0, "blocked": 0}
        if r.get("blocked"):
            by_runner[runner]["blocked"] += 1
        else:
            by_runner[runner]["allowed"] += 1

    # 按 provider 統計
    by_provider: dict[str, int] = {}
    for r in records:
        prov = r.get("provider") or "unknown"
        by_provider[prov] = by_provider.get(prov, 0) + 1

    # 封鎖原因統計
    block_reasons: dict[str, int] = {}
    for r in records:
        if r.get("blocked"):
            reason = r.get("block_reason") or "unknown"
            block_reasons[reason] = block_reasons.get(reason, 0) + 1

    print(f"\n{'='*60}")
    print(f"  LLM 使用量摘要 — 最近 {args.hours:.0f} 小時")
    print(f"{'='*60}")
    print(f"  總記錄數：{total}")
    print(f"  允許：{allowed}  |  封鎖：{blocked}")

    print(f"\n  ── 按角色 (runner) ──")
    for runner, counts in sorted(by_runner.items()):
        print(f"    {runner:20s}  允許={counts['allowed']}  封鎖={counts['blocked']}")

    print(f"\n  ── 按 Provider ──")
    for prov, count in sorted(by_provider.items(), key=lambda x: -x[1]):
        print(f"    {prov:20s}  {count}")

    if block_reasons:
        print(f"\n  ── 封鎖原因 ──")
        for reason, count in sorted(block_reasons.items(), key=lambda x: -x[1]):
            print(f"    {reason:40s}  {count}")

    # 最近 5 筆記錄
    if records:
        print(f"\n  ── 最近 5 筆記錄 ──")
        for r in records[-5:]:
            ts = r.get("timestamp", "?")[:19]
            runner = r.get("runner") or "?"
            prov = r.get("provider") or "?"
            status = "BLOCKED" if r.get("blocked") else "ALLOWED"
            reason = r.get("block_reason") or ""
            reason_str = f"  ({reason})" if reason else ""
            print(f"    [{ts}] {runner:15s} / {prov:15s} → {status}{reason_str}")

    print(f"{'='*60}\n")


if __name__ == "__main__":
    args = _parse_args()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    records = _load_records(
        cutoff=cutoff,
        runner_filter=args.runner,
        provider_filter=args.provider,
        blocked_only=args.blocked_only,
    )

    if args.json_out:
        output = records[-args.tail:] if args.tail else records
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        _summarize(records)
