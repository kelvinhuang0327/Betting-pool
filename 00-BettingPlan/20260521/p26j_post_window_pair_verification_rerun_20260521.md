# P26J Post-Window Verification — BettingPlan 2026-05-21

**Generated:** 2026-05-21T09:12:47Z  
**Final Classification:** `P26J_TSL_SOURCE_UNAVAILABLE_AT_CLOSING_CONFIRMED`

---

## Summary

| Item | Result |
|------|--------|
| Timing guard | ✅ PASS (UTC 09:12:47 ≥ 09:10:00) |
| 3469930.1 pair status | `PREGAME_ONLY_NO_CLOSING` |
| 3469931.1 pair status | `PREGAME_ONLY_NO_CLOSING` |
| target_pair_delta | 0 |
| COMPLETE_PAIR before/after | 220 → 219 (delta = –1) |
| Daemon continuity | `DAEMON_RAN_BUT_SOURCE_DID_NOT_RETURN_TARGETS` |
| P25C bootstrap eligible | ❌ No (219 < 300) |

---

## Root Cause

- **markets=[]** on ALL rows for both targets — TSL source never provided market data
- `force_closing` captures (02:09–03:24Z) were labeled closing but occurred at gap 5.6–6.9h (not within 0–2h window)
- During the actual closing window (07:00–09:00Z): `fetched=false` in all 8 daemon cycles
- `api_calls_today=2` stable — external API not called in closing window
- True closing rows (gap 0–2h) never captured for either target

## No Action Taken

This is a verification-only report. No code changes, no API calls, no bootstrap execution.

Full reports:
- [report/p26j_post_window_pair_verification_rerun_20260521.md](../../report/p26j_post_window_pair_verification_rerun_20260521.md)
- [report/p26j_daemon_continuity_verification_rerun_20260521.md](../../report/p26j_daemon_continuity_verification_rerun_20260521.md)
