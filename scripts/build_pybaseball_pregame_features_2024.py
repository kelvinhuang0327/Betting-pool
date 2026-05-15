"""
P39A — Pybaseball Pregame-Safe Feature Adapter
scripts/build_pybaseball_pregame_features_2024.py

Purpose:
    Research-only feature pipeline using pybaseball / Statcast.
    Builds rolling pregame-safe batting, pitching, workload, and team form
    features for P39 enrichment of P38A OOF predictions.

    ⚠️  pybaseball does NOT provide betting odds.
    ⚠️  This script does NOT produce moneyline / CLV / sportsbook data.
    ⚠️  All features use only data BEFORE game_date (no look-ahead).

SCRIPT_VERSION = p39a_pybaseball_skeleton_v1
PAPER_ONLY = True
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_VERSION = "p39a_pybaseball_skeleton_v1"
PAPER_ONLY = True

FORBIDDEN_ODDS_COLUMNS: frozenset[str] = frozenset(
    {
        "moneyline",
        "closing_line",
        "opening_line",
        "odds",
        "vig",
        "implied_prob",
        "home_ml",
        "away_ml",
        "home_odds",
        "away_odds",
        "clv",
        "closing_implied_prob",
        "no_vig_prob",
    }
)

OUTPUT_SCHEMA_COLUMNS: list[str] = [
    "game_date",
    "team",
    "opponent",
    "is_home",
    "feature_window_start",
    "feature_window_end",
    "source",
    "feature_name",
    "feature_value",
    "sample_size",
    "generated_at",
    "leakage_status",
]

logging.basicConfig(
    format="%(levelname)s | %(message)s",
    level=logging.INFO,
    stream=sys.stderr,
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pure functions — independently testable, no side effects, no external fetch
# ---------------------------------------------------------------------------


def validate_feature_window(game_date: date, feature_window_end: date) -> bool:
    """
    Return True iff feature_window_end is strictly before game_date.

    This is the core pregame-safe leakage guard.
    If False, the row must be rejected (leakage_detected).
    """
    return feature_window_end < game_date


def build_rolling_window_dates(
    game_date: date, window_days: int
) -> tuple[date, date]:
    """
    Return (window_start, window_end) for a rolling window.

    window_end = game_date - 1 day  (strictly pregame-safe)
    window_start = window_end - window_days + 1
    """
    window_end = game_date - timedelta(days=1)
    window_start = window_end - timedelta(days=window_days - 1)
    return window_start, window_end


def assert_no_odds_columns(columns: list[str]) -> None:
    """
    Raise ValueError if any forbidden odds column is present.

    Call this before saving any feature DataFrame.
    """
    found = set(columns) & FORBIDDEN_ODDS_COLUMNS
    if found:
        raise ValueError(
            f"LEAKAGE_DETECTED: Odds columns found in feature output: {found}\n"
            "pybaseball adapter must NOT produce odds data."
        )


def summarize_statcast_frame(df: pd.DataFrame) -> dict:
    """
    Return a summary dict for a raw Statcast DataFrame.

    Fields:
        rows                  — int
        columns               — int
        date_range_start      — str (YYYY-MM-DD) or None
        date_range_end        — str (YYYY-MM-DD) or None
        sample_columns        — list[str] (first 10)
        odds_boundary_status  — "CONFIRMED" | "VIOLATION"
        odds_columns_found    — list[str]
        leakage_rows          — 0 (statcast frame does not have leakage status)
    """
    if df is None or df.empty:
        return {
            "rows": 0,
            "columns": 0,
            "date_range_start": None,
            "date_range_end": None,
            "sample_columns": [],
            "odds_boundary_status": "CONFIRMED",
            "odds_columns_found": [],
            "leakage_rows": 0,
        }

    cols = list(df.columns)
    found_odds = list(set(cols) & FORBIDDEN_ODDS_COLUMNS)
    odds_status = "VIOLATION" if found_odds else "CONFIRMED"

    date_col = "game_date" if "game_date" in cols else None
    date_min = str(df[date_col].min()) if date_col else None
    date_max = str(df[date_col].max()) if date_col else None

    return {
        "rows": len(df),
        "columns": len(cols),
        "date_range_start": date_min,
        "date_range_end": date_max,
        "sample_columns": cols[:10],
        "odds_boundary_status": odds_status,
        "odds_columns_found": found_odds,
        "leakage_rows": 0,
    }


def assert_output_path_gitignored(path: str) -> None:
    """
    Raise ValueError if output path is not under data/pybaseball/local_only/.

    Prevents accidental commit of raw pybaseball data.
    """
    if "local_only" not in path:
        raise ValueError(
            f"Output path must be inside data/pybaseball/local_only/: {path}\n"
            "Raw pybaseball data must not be committed to git."
        )


def compute_summary_hash(summary: dict) -> str:
    """
    Return a deterministic SHA-256 hash of the summary dict.

    Used for smoke test determinism check (same inputs → same hash).
    """
    serialized = json.dumps(summary, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Runtime functions — may call pybaseball (only if --execute)
# ---------------------------------------------------------------------------


def fetch_statcast_range(
    start_date: str,
    end_date: str,
    cache_dir: Path | None = None,
) -> pd.DataFrame | None:
    """
    Fetch Statcast data via pybaseball.

    Imported inside function to avoid import cost in --summary-only mode.
    Fails softly: returns None on HTTPError / timeout.
    """
    try:
        import pybaseball  # noqa: PLC0415

        log.info(
            "[pybaseball] Fetching Statcast %s → %s ...", start_date, end_date
        )
        df = pybaseball.statcast(start_dt=start_date, end_dt=end_date)
        log.info("[pybaseball] Fetched %d rows, %d cols", len(df), len(df.columns))
        return df

    except Exception as exc:  # noqa: BLE001
        log.warning("[pybaseball] Statcast fetch FAILED: %s", exc)
        return None


def build_feature_summary_only(
    start_date: str,
    end_date: str,
    window_days: int,
) -> dict:
    """
    Dry-run: describe what features would be built without fetching.

    No external network call. Safe for CI.
    """
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    n_days = (end - start).days + 1

    # Validate window for first game date
    first_game = start
    ws, we = build_rolling_window_dates(first_game, window_days)
    window_safe = validate_feature_window(first_game, we)

    return {
        "mode": "summary-only",
        "script_version": SCRIPT_VERSION,
        "paper_only": PAPER_ONLY,
        "date_range": {"start": start_date, "end": end_date, "n_days": n_days},
        "rolling_window_days": window_days,
        "sample_window_check": {
            "game_date": str(first_game),
            "window_start": str(ws),
            "window_end": str(we),
            "pregame_safe": window_safe,
        },
        "feature_families": [
            "rolling_batting_proxies",
            "rolling_pitching_proxies",
            "starter_bullpen_workload",
            "team_form_proxies",
            "statcast_aggregate_proxies",
            "schedule_density_proxies",
        ],
        "estimated_feature_count": 28,
        "odds_boundary": "CONFIRMED (design: no odds columns)",
        "leakage_violations": 0,
        "note": (
            "This is a dry-run summary. "
            "Use --execute to fetch Statcast data and compute features."
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "P39A pybaseball pregame-safe feature adapter.\n"
            "PAPER_ONLY=True | pybaseball does NOT provide betting odds."
        )
    )
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--window-days", type=int, default=14, help="Rolling window days")
    p.add_argument(
        "--summary-only",
        action="store_true",
        default=True,
        help="Dry-run: describe output without fetching (default)",
    )
    p.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Actually fetch Statcast data and compute features",
    )
    p.add_argument("--out-file", default=None, help="Output CSV path (local_only only)")
    p.add_argument(
        "--cache-dir",
        default="data/pybaseball/local_only/cache",
        help="Directory for raw Statcast cache",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    run_ts = datetime.now(timezone.utc).isoformat()

    print("=" * 60)
    print("  P39A pybaseball Pregame-Safe Feature Adapter")
    print("=" * 60)
    print(f"  Script version : {SCRIPT_VERSION}")
    print(f"  PAPER_ONLY     : {PAPER_ONLY}")
    print(f"  Start date     : {args.start_date}")
    print(f"  End date       : {args.end_date}")
    print(f"  Window days    : {args.window_days}")
    print(f"  Mode           : {'EXECUTE' if args.execute else 'SUMMARY-ONLY'}")
    print(f"  Run timestamp  : {run_ts}")
    print()
    print("  BOUNDARY: pybaseball does NOT provide betting odds.")
    print("  This adapter produces baseball statistics only.")
    print()

    if not args.execute:
        # ── SUMMARY-ONLY MODE (default, safe) ──────────────────────────────
        print("=" * 60)
        print("  Summary-Only Mode (dry-run — no external fetch)")
        print("=" * 60)
        summary = build_feature_summary_only(
            args.start_date, args.end_date, args.window_days
        )

        for key, val in summary.items():
            print(f"  {key:30s} : {val}")

        # Deterministic hash for smoke repeatability check
        h = compute_summary_hash(summary)
        print()
        print(f"  Summary hash   : {h}")

        # Gate: verify window safety
        if not summary["sample_window_check"]["pregame_safe"]:
            print()
            print("  FAIL: pregame window safety check failed")
            sys.exit(1)

        print()
        print("  Pregame-safe  : CONFIRMED")
        print("  Odds boundary : CONFIRMED")
        print()
        print(
            "  Marker: P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515"
        )
        sys.exit(0)

    # ── EXECUTE MODE ────────────────────────────────────────────────────────
    print("=" * 60)
    print("  Execute Mode — fetching Statcast ...")
    print("=" * 60)

    df = fetch_statcast_range(
        args.start_date,
        args.end_date,
        cache_dir=Path(args.cache_dir) if args.cache_dir else None,
    )

    if df is None or df.empty:
        print("  [WARN] No Statcast data returned. Check date range or network.")
        print("  Overall: PARTIAL — no data to summarize")
        sys.exit(0)

    summary = summarize_statcast_frame(df)
    for key, val in summary.items():
        print(f"  {key:30s} : {val}")

    # Hard assert odds boundary
    try:
        assert_no_odds_columns(list(df.columns))
        print("  Odds boundary : CONFIRMED")
    except ValueError as exc:
        print(f"  FAIL: {exc}")
        sys.exit(2)

    # Optional write
    if args.out_file:
        assert_output_path_gitignored(args.out_file)
        out_path = Path(args.out_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # NOTE: In skeleton, we write summary JSON only (not feature rows).
        # Full feature computation is deferred to P39 implementation round.
        summary["generated_at"] = run_ts
        out_path.with_suffix(".summary.json").write_text(
            json.dumps(summary, indent=2, default=str)
        )
        print(f"  Summary written: {out_path.with_suffix('.summary.json')}")

    print()
    print("  Marker: P39A_PYBASEBALL_SKELETON_SCRIPT_READY_20260515")
    sys.exit(0)


if __name__ == "__main__":
    main()
