# P132 Decision Card Escalation Router (2026-06-01)

## Decision
- escalation_router_status: READY_WITH_BLOCKERS
- source_decision_card_runner_status: READY_WITH_BLOCKERS
- source_evaluated_packet_count: 22
- source_blocked_packet_count: 21
- source_unexpected_approved_count: 0
- final_classification: P132_DECISION_CARD_ESCALATION_ROUTER_READY_WITH_BLOCKERS

## Escalation Summary
- sla_summary: {'SLA_EXPEDITED_REVIEW': 16, 'SLA_IMMEDIATE_STOP': 5, 'SLA_STANDARD_REVIEW': 1}
- blocker_escalation_summary: {'APPROVAL_TIMESTAMP_MISSING_BLOCKER': 1, 'BASELINE_CHANGE_OWNER_MISSING_BLOCKER': 1, 'BASELINE_CHANGE_REASON_MISSING_BLOCKER': 1, 'BASELINE_CHANGE_REQUEST_ID_MISSING_BLOCKER': 1, 'EXPECTED_VERDICT_DELTA_MISSING_BLOCKER': 1, 'LIVE_OR_PAID_API_REQUESTED_BLOCKER': 1, 'NEW_FINGERPRINT_MISSING_BLOCKER': 1, 'NON_UNLOCK_ATTESTATION_MISSING_BLOCKER': 1, 'OLD_AND_NEW_FINGERPRINT_IDENTICAL_BLOCKER': 1, 'OLD_FINGERPRINT_MISSING_BLOCKER': 1, 'PRODUCTION_UNLOCK_REQUESTED_BLOCKER': 1, 'PROVIDER_UNLOCK_REQUESTED_BLOCKER': 1, 'REAL_ODDS_INGESTION_REQUESTED_BLOCKER': 1, 'RECOMMENDATION_UNLOCK_REQUESTED_BLOCKER': 1, 'REVIEWER_APPROVAL_NOT_APPROVED_BLOCKER': 1, 'REVIEWER_IDENTITY_MISSING_BLOCKER': 1, 'ROLLBACK_PLAN_MISSING_BLOCKER': 1, 'RULE_CHANGE_SUMMARY_EMPTY_WITH_FINGERPRINT_CHANGE_BLOCKER': 2, 'RULE_CHANGE_SUMMARY_MISSING_BLOCKER': 2, 'SOURCE_FIXTURE_VERSION_AFTER_MISSING_BLOCKER': 1, 'SOURCE_FIXTURE_VERSION_BEFORE_MISSING_BLOCKER': 1}
- signoff_requirement_summary: {'ceo_owner': 5, 'compliance_owner': 22, 'cto_owner': 5, 'data_rights_owner': 5, 'engineering_owner': 22, 'legal_owner': 5, 'security_owner': 21}
- blocked_action_summary: {'baseline_change_apply': 21, 'ev_clv_kelly_unlock': 22, 'live_api_call': 5, 'odds_unlock': 22, 'paid_api_call': 5, 'production_unlock': 22, 'provider_unlock': 22, 'real_odds_ingestion': 5, 'recommendation_unlock': 22}

## Escalation Cards
- P130_INVALID_EMPTY_RULE_CHANGE_WITH_FINGERPRINT_CHANGE_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_LIVE_OR_PAID_API_REQUESTED_BLOCKED: source_verdict=BLOCKED escalation_level=CRITICAL_STOP sla=SLA_IMMEDIATE_STOP
- P130_INVALID_MISSING_APPROVAL_TIMESTAMP_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_BASELINE_CHANGE_OWNER_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_BASELINE_CHANGE_REASON_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_BASELINE_CHANGE_REQUEST_ID_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_EXPECTED_VERDICT_DELTA_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_NEW_FINGERPRINT_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_NON_UNLOCK_ATTESTATION_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_OLD_FINGERPRINT_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_REVIEWER_IDENTITY_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_ROLLBACK_PLAN_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_RULE_CHANGE_SUMMARY_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_SOURCE_FIXTURE_VERSION_AFTER_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_MISSING_SOURCE_FIXTURE_VERSION_BEFORE_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_PRODUCTION_UNLOCK_REQUESTED_BLOCKED: source_verdict=BLOCKED escalation_level=CRITICAL_STOP sla=SLA_IMMEDIATE_STOP
- P130_INVALID_PROVIDER_UNLOCK_REQUESTED_BLOCKED: source_verdict=BLOCKED escalation_level=CRITICAL_STOP sla=SLA_IMMEDIATE_STOP
- P130_INVALID_REAL_ODDS_INGESTION_REQUESTED_BLOCKED: source_verdict=BLOCKED escalation_level=CRITICAL_STOP sla=SLA_IMMEDIATE_STOP
- P130_INVALID_RECOMMENDATION_UNLOCK_REQUESTED_BLOCKED: source_verdict=BLOCKED escalation_level=CRITICAL_STOP sla=SLA_IMMEDIATE_STOP
- P130_INVALID_REVIEWER_APPROVAL_NOT_APPROVED_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_INVALID_SAME_OLD_AND_NEW_FINGERPRINT_BLOCKED: source_verdict=BLOCKED escalation_level=BLOCKED_NO_UNLOCK_ALLOWED sla=SLA_EXPEDITED_REVIEW
- P130_VALID_TEMPLATE: source_verdict=GOVERNANCE_ONLY_PENDING escalation_level=REVIEW_REQUIRED sla=SLA_STANDARD_REVIEW

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
- targeted_p118_p132_tests_status: PASS
- targeted_p118_p132_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p132_decision_card_escalation_router.py tests/test_p131_baseline_change_review_packet_runner_decision_card.py tests/test_p130_baseline_change_review_packet_validator.py tests/test_p129_replay_drift_alert_contract.py tests/test_p128_deterministic_replay_consistency_gate.py tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Prohibited Actions
- Do not ingest real odds or call live/paid APIs
- Do not unlock provider/recommendation/production/EV/CLV/Kelly/stake/profit
- Do not treat escalation routing as legal provider approval or production readiness
- Do not bypass blocker resolution and required sign-off

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Route decision cards through governance-only escalation path
- Collect required sign-off evidence before any baseline change
- Keep full regression state explicit: PASS/FAIL/NOT_RUN
