# P128 Deterministic Replay Consistency Gate (2026-06-01)

## Decision
- replay_consistency_gate_status: READY_WITH_BLOCKERS
- final_classification: P128_DETERMINISTIC_REPLAY_CONSISTENCY_GATE_READY_WITH_BLOCKERS

## Replay Counts
- replay_run_count: 3
- source_fixture_count: 19

## Consistency Status
- fingerprint_consistency_status: CONSISTENT
- verdict_consistency_status: CONSISTENT
- blocked_reason_consistency_status: CONSISTENT
- rule_matrix_consistency_status: CONSISTENT
- unlock_prevention_consistency_status: CONSISTENT
- drift_detected: False

## Fingerprints
- baseline_fingerprint: d29fcde955c321e384caf65f5add03e8a719ecbb1c6e8fb57177aee04dab5b40
- run_1: d29fcde955c321e384caf65f5add03e8a719ecbb1c6e8fb57177aee04dab5b40 | evaluated=19 | expected_blocked=19 | actual_blocked=19 | unexpected_allowed=0
- run_2: d29fcde955c321e384caf65f5add03e8a719ecbb1c6e8fb57177aee04dab5b40 | evaluated=19 | expected_blocked=19 | actual_blocked=19 | unexpected_allowed=0
- run_3: d29fcde955c321e384caf65f5add03e8a719ecbb1c6e8fb57177aee04dab5b40 | evaluated=19 | expected_blocked=19 | actual_blocked=19 | unexpected_allowed=0

## Governance Invariants
- paper_only: True
- diagnostic_only: True
- production_ready: False
- real_bet_allowed: False
- recommendation_allowed: False
- provider_approved: False
- authorization_evidence_present: False
- placeholder_allowed_as_authorization: False
- real_legal_odds_ingested: False
- live_api_calls: 0
- paid_api_called: False
- ev_computed: False
- clv_computed: False
- kelly_computed: False
- stake_sizing: False
- profit_computed: False
- recommendation_generated: False

## Regression/Test Status
- targeted_p118_p128_tests_status: PASS
- targeted_p118_p128_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p128_deterministic_replay_consistency_gate.py tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Blockers
- APPROVAL_OWNER_MISSING_BLOCKER
- AUDIT_TRAIL_MISSING_BLOCKER
- AUTHORIZATION_EVIDENCE_MISSING_BLOCKER
- DATA_USAGE_SCOPE_MISSING_BLOCKER
- EFFECTIVE_DATE_MISSING_BLOCKER
- EV_CLV_KELLY_UNLOCK_REQUEST_BLOCKER
- EXPIRATION_OR_RENEWAL_MISSING_BLOCKER
- FULL_REGRESSION_NOT_RUN_BLOCKER
- LEGAL_DOCUMENT_REFERENCE_MISSING_BLOCKER
- MARKET_SCOPE_MISSING_BLOCKER
- PLACEHOLDER_DETECTED_BLOCKER
- PRIVATE_CONTRACT_BODY_PRESENT_BLOCKER
- PRODUCTION_UNLOCK_REQUEST_BLOCKER
- PROVIDER_IDENTITY_MISSING_BLOCKER
- PROVIDER_NOT_APPROVED_BLOCKER
- RECOMMENDATION_UNLOCK_REQUEST_BLOCKER
- REVIEW_OWNER_MISSING_BLOCKER
- REVIEW_STATUS_NOT_APPROVED_BLOCKER
- ROW_LEVEL_PROPRIETARY_ODDS_PRESENT_BLOCKER
- SECRET_OR_AUTH_URL_DETECTED_BLOCKER
- SOURCE_TRACE_MISSING_BLOCKER

## Prohibited Actions
- Do not ingest real odds or call live/paid APIs
- Do not activate providers or approve authorization from placeholder data
- Do not unlock recommendation/production/EV/CLV/Kelly/stake/profit
- Do not store secrets, auth URLs, private contract body, or row-level proprietary odds

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Use replay consistency outputs for governance diagnostics only
- Collect real legal evidence via legal/compliance workflow before approval consideration
- Keep full regression status explicit: PASS/FAIL/NOT_RUN
