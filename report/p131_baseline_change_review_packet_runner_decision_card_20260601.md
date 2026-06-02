# P131 Baseline Change Review Packet Runner + Decision Card (2026-06-01)

## Decision
- packet_runner_status: READY_WITH_BLOCKERS
- source_baseline_change_validator_status: READY_WITH_BLOCKERS
- evaluated_packet_count: 22
- approved_packet_count: 0
- blocked_packet_count: 21
- unexpected_approved_count: 0
- final_classification: P131_BASELINE_CHANGE_REVIEW_PACKET_RUNNER_DECISION_CARD_READY_WITH_BLOCKERS

## Decision Cards
- VALID_PACKET_TEMPLATE: verdict=GOVERNANCE_ONLY_PENDING level=YELLOW_GOVERNANCE_ONLY blockers=
- MISSING_BASELINE_CHANGE_REQUEST_ID_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=BASELINE_CHANGE_REQUEST_ID_MISSING_BLOCKER
- MISSING_BASELINE_CHANGE_OWNER_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=BASELINE_CHANGE_OWNER_MISSING_BLOCKER
- MISSING_BASELINE_CHANGE_REASON_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=BASELINE_CHANGE_REASON_MISSING_BLOCKER
- MISSING_SOURCE_FIXTURE_VERSION_BEFORE_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=SOURCE_FIXTURE_VERSION_BEFORE_MISSING_BLOCKER
- MISSING_SOURCE_FIXTURE_VERSION_AFTER_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=SOURCE_FIXTURE_VERSION_AFTER_MISSING_BLOCKER
- MISSING_OLD_FINGERPRINT_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=OLD_FINGERPRINT_MISSING_BLOCKER
- MISSING_NEW_FINGERPRINT_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=NEW_FINGERPRINT_MISSING_BLOCKER
- MISSING_RULE_CHANGE_SUMMARY_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=RULE_CHANGE_SUMMARY_EMPTY_WITH_FINGERPRINT_CHANGE_BLOCKER,RULE_CHANGE_SUMMARY_MISSING_BLOCKER
- MISSING_EXPECTED_VERDICT_DELTA_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=EXPECTED_VERDICT_DELTA_MISSING_BLOCKER
- REVIEWER_APPROVAL_NOT_APPROVED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=REVIEWER_APPROVAL_NOT_APPROVED_BLOCKER
- MISSING_REVIEWER_IDENTITY_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=REVIEWER_IDENTITY_MISSING_BLOCKER
- MISSING_APPROVAL_TIMESTAMP_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=APPROVAL_TIMESTAMP_MISSING_BLOCKER
- MISSING_ROLLBACK_PLAN_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=ROLLBACK_PLAN_MISSING_BLOCKER
- MISSING_NON_UNLOCK_ATTESTATION_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=NON_UNLOCK_ATTESTATION_MISSING_BLOCKER
- PRODUCTION_UNLOCK_REQUESTED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=PRODUCTION_UNLOCK_REQUESTED_BLOCKER
- RECOMMENDATION_UNLOCK_REQUESTED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=RECOMMENDATION_UNLOCK_REQUESTED_BLOCKER
- PROVIDER_UNLOCK_REQUESTED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=PROVIDER_UNLOCK_REQUESTED_BLOCKER
- REAL_ODDS_INGESTION_REQUESTED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=REAL_ODDS_INGESTION_REQUESTED_BLOCKER
- LIVE_OR_PAID_API_REQUESTED_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=LIVE_OR_PAID_API_REQUESTED_BLOCKER
- SAME_OLD_AND_NEW_FINGERPRINT_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=OLD_AND_NEW_FINGERPRINT_IDENTICAL_BLOCKER
- EMPTY_RULE_CHANGE_WITH_FINGERPRINT_CHANGE_BLOCKED: verdict=BLOCKED level=RED_BLOCKED blockers=RULE_CHANGE_SUMMARY_EMPTY_WITH_FINGERPRINT_CHANGE_BLOCKER,RULE_CHANGE_SUMMARY_MISSING_BLOCKER

## Reviewer/Rollback/Attestation Summary
- reviewer_status_summary: {'APPROVED': 21, 'NOT_APPROVED': 1}
- rollback_readiness_summary: {'MISSING': 1, 'PRESENT': 21}
- non_unlock_attestation_summary: {'MISSING': 1, 'VALID': 21}

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
- targeted_p118_p131_tests_status: PASS
- targeted_p118_p131_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p131_baseline_change_review_packet_runner_decision_card.py tests/test_p130_baseline_change_review_packet_validator.py tests/test_p129_replay_drift_alert_contract.py tests/test_p128_deterministic_replay_consistency_gate.py tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Blockers
- APPROVAL_OWNER_MISSING_BLOCKER
- AUDIT_TRAIL_MISSING_BLOCKER
- AUTHORIZATION_EVIDENCE_MISSING_BLOCKER
- BASELINE_CHANGE_APPROVAL_REQUIRED_BLOCKER
- BASELINE_PACKET_REVIEW_REQUIRED_BLOCKER
- DATA_USAGE_SCOPE_MISSING_BLOCKER
- DECISION_CARD_GOVERNANCE_ONLY_BLOCKER
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
- Do not unlock provider/recommendation/production/EV/CLV/Kelly/stake/profit
- Do not treat packet review as legal provider approval or production readiness
- Do not bypass blocker resolution before any baseline change

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Use decision cards for governance review workflow only
- Require reviewer approval, rollback plan, and valid non-unlock attestation before baseline change
- Keep full regression status explicit: PASS/FAIL/NOT_RUN
