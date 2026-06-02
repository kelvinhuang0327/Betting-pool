# P129 Replay Drift Alert Contract (2026-06-01)

## Decision
- replay_drift_alert_contract_status: READY_WITH_BLOCKERS
- source_replay_gate_status: READY_WITH_BLOCKERS
- source_replay_run_count: 3
- source_fixture_count: 19
- source_drift_detected: False
- final_classification: P129_REPLAY_DRIFT_ALERT_CONTRACT_READY_WITH_BLOCKERS

## Alert Levels
- GREEN_NO_DRIFT: No drift across fingerprint/verdict/blocked reasons/rule matrix/unlock prevention
- YELLOW_METADATA_ONLY_DRIFT: Only reproducibility metadata changed; no verdict/rule/unlock impact
- ORANGE_BLOCKED_REASON_OR_RULE_DRIFT: Blocked reason matrix or rule matrix changed while verdict remains BLOCKED
- RED_VERDICT_OR_UNLOCK_DRIFT: Any verdict changes or any unlock prevention field becomes true
- CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT: Provider approval/authorization/production unlock indicators become true without legal evidence

## Blocking Conditions
- C001_PREVIOUSLY_BLOCKED_BECOMES_ALLOWED: Any previously BLOCKED verdict becomes ALLOWED (RED_VERDICT_OR_UNLOCK_DRIFT)
- C002_UNEXPECTED_ALLOWED_COUNT_GT_ZERO: unexpected_allowed_count > 0 (RED_VERDICT_OR_UNLOCK_DRIFT)
- C003_ACTUAL_BLOCKED_LT_EXPECTED_BLOCKED: actual_blocked_count < expected_blocked_count (RED_VERDICT_OR_UNLOCK_DRIFT)
- C004_RECOMMENDATION_UNLOCK_TRUE: recommendation_unlock_allowed becomes true (RED_VERDICT_OR_UNLOCK_DRIFT)
- C005_PRODUCTION_UNLOCK_TRUE: production_unlock_allowed becomes true (CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT)
- C006_EV_CLV_KELLY_STAKE_PROFIT_UNLOCK_TRUE: any EV/CLV/Kelly/stake/profit unlock becomes true (RED_VERDICT_OR_UNLOCK_DRIFT)
- C007_PROVIDER_APPROVED_WITHOUT_VERIFIED_LEGAL_EVIDENCE: provider_approved=true without verified legal evidence (CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT)
- C008_AUTH_EVIDENCE_PRESENT_WITHOUT_VERIFIED_LEGAL_EVIDENCE: authorization_evidence_present=true without verified legal evidence (CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT)
- C009_REAL_ODDS_INGESTED_WITHOUT_APPROVAL: real_legal_odds_ingested=true without explicit legal/provider approval (CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT)
- C010_LIVE_OR_PAID_API_CALLS_NON_ZERO: live_api_calls>0 or paid_api_called=true (CRITICAL_PROVIDER_OR_PRODUCTION_UNLOCK_DRIFT)
- C011_BASELINE_FINGERPRINT_CHANGED_WITHOUT_APPROVAL: baseline fingerprint changed and baseline change approval missing (ORANGE_BLOCKED_REASON_OR_RULE_DRIFT)
- C012_DRIFT_DETAILS_MISSING_WHEN_DRIFT_DETECTED: drift_detected=true but drift_details missing/empty (ORANGE_BLOCKED_REASON_OR_RULE_DRIFT)

## Baseline Hash Change Review Rules
- required_fields:
  - baseline_change_request_id
  - baseline_change_owner
  - baseline_change_reason
  - source_fixture_version_before
  - source_fixture_version_after
  - old_fingerprint
  - new_fingerprint
  - rule_change_summary
  - expected_verdict_delta
  - reviewer_approval_status
  - reviewer_identity
  - approval_timestamp
  - rollback_plan
  - non_unlock_attestation
- approval_policy: Any baseline fingerprint change requires completed request with reviewer approval before acceptance.
- non_unlock_attestation_required: Baseline change does not unlock provider/odds/recommendation/production.

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
- targeted_p118_p129_tests_status: PASS
- targeted_p118_p129_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p129_replay_drift_alert_contract.py tests/test_p128_deterministic_replay_consistency_gate.py tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Blockers
- APPROVAL_OWNER_MISSING_BLOCKER
- AUDIT_TRAIL_MISSING_BLOCKER
- AUTHORIZATION_EVIDENCE_MISSING_BLOCKER
- BASELINE_CHANGE_APPROVAL_REQUIRED_BLOCKER
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
- Do not activate providers or approve authorization from placeholders
- Do not unlock recommendation/production/EV/CLV/Kelly/stake/profit
- Do not bypass baseline hash change review workflow

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Use replay drift alert contract for governance diagnostics only
- Open baseline change request when fingerprint changes
- Keep full regression state explicit: PASS/FAIL/NOT_RUN
