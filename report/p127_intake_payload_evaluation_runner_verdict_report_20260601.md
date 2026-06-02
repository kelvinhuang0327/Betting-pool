# P127 Intake Payload Evaluation Runner + Deterministic Gate Verdict Report (2026-06-01)

## Decision
- evaluation_runner_status: READY_WITH_BLOCKERS
- deterministic_verdict_status: READY_WITH_BLOCKERS
- final_classification: P127_INTAKE_PAYLOAD_EVALUATION_RUNNER_VERDICT_REPORT_READY_WITH_BLOCKERS

## Evaluation Counts
- evaluated_fixture_count: 19
- expected_blocked_count: 19
- actual_blocked_count: 19
- unexpected_allowed_count: 0

## Deterministic Reproducibility
- runner_version: P127.20260601
- deterministic_hash_sha256: a6191e0b0f8b27ef9d539872421b901f36f3c105b705123e764a717b397afe64
- source_p126_final_classification: P126_LEGAL_EVIDENCE_INTAKE_PAYLOAD_FIXTURE_NEGATIVE_CASES_READY_WITH_BLOCKERS

## Verdicts
- AUDIT_TRAIL_MISSING_BLOCKED: BLOCKED | rules=R014_AUDIT_TRAIL_REQUIRED | blockers=AUDIT_TRAIL_MISSING_BLOCKER
- DATA_USAGE_SCOPE_MISSING_BLOCKED: BLOCKED | rules=R010_DATA_USAGE_SCOPE_REQUIRED | blockers=DATA_USAGE_SCOPE_MISSING_BLOCKER
- EFFECTIVE_DATE_MISSING_BLOCKED: BLOCKED | rules=R011_EFFECTIVE_DATE_REQUIRED | blockers=EFFECTIVE_DATE_MISSING_BLOCKER
- EV_CLV_KELLY_UNLOCK_REQUEST_BLOCKED: BLOCKED | rules=R020_EV_CLV_KELLY_UNLOCK_FORBIDDEN | blockers=EV_CLV_KELLY_UNLOCK_REQUEST_BLOCKER
- EXPIRATION_OR_RENEWAL_MISSING_BLOCKED: BLOCKED | rules=R012_EXPIRATION_AND_RENEWAL_REQUIRED | blockers=EXPIRATION_OR_RENEWAL_MISSING_BLOCKER
- MARKET_SCOPE_MISSING_BLOCKED: BLOCKED | rules=R009_MARKET_SCOPE_REQUIRED | blockers=MARKET_SCOPE_MISSING_BLOCKER
- MISSING_APPROVAL_OWNER_BLOCKED: BLOCKED | rules=R005_APPROVAL_OWNER_REQUIRED | blockers=APPROVAL_OWNER_MISSING_BLOCKER
- MISSING_LEGAL_DOCUMENT_REFERENCE_BLOCKED: BLOCKED | rules=R003_LEGAL_DOC_REFERENCE_REQUIRED | blockers=LEGAL_DOCUMENT_REFERENCE_MISSING_BLOCKER
- MISSING_REVIEW_OWNER_BLOCKED: BLOCKED | rules=R004_REVIEW_OWNER_REQUIRED | blockers=REVIEW_OWNER_MISSING_BLOCKER
- PLACEHOLDER_AS_EVIDENCE_BLOCKED: BLOCKED | rules=R007_NO_PLACEHOLDER_AS_EVIDENCE | blockers=PLACEHOLDER_DETECTED_BLOCKER
- PRIVATE_CONTRACT_BODY_PRESENT_BLOCKED: BLOCKED | rules=R016_PRIVATE_CONTRACT_BODY_FORBIDDEN | blockers=PRIVATE_CONTRACT_BODY_PRESENT_BLOCKER
- PRODUCTION_UNLOCK_REQUEST_BLOCKED: BLOCKED | rules=R019_PRODUCTION_UNLOCK_FORBIDDEN | blockers=PRODUCTION_UNLOCK_REQUEST_BLOCKER
- PROVIDER_IDENTITY_MISSING_BLOCKED: BLOCKED | rules=R008_PROVIDER_IDENTITY_REQUIRED | blockers=PROVIDER_IDENTITY_MISSING_BLOCKER
- RECOMMENDATION_UNLOCK_REQUEST_BLOCKED: BLOCKED | rules=R018_RECOMMENDATION_UNLOCK_FORBIDDEN | blockers=RECOMMENDATION_UNLOCK_REQUEST_BLOCKER
- REVIEW_STATUS_NOT_APPROVED_BLOCKED: BLOCKED | rules=R006_REVIEW_STATUS_APPROVED_REQUIRED | blockers=REVIEW_STATUS_NOT_APPROVED_BLOCKER
- ROW_LEVEL_PROPRIETARY_ODDS_PRESENT_BLOCKED: BLOCKED | rules=R017_ROW_LEVEL_PROPRIETARY_ODDS_FORBIDDEN | blockers=ROW_LEVEL_PROPRIETARY_ODDS_PRESENT_BLOCKER
- SECRET_OR_AUTH_URL_PRESENT_BLOCKED: BLOCKED | rules=R015_SECRET_OR_AUTH_URL_FORBIDDEN | blockers=SECRET_OR_AUTH_URL_DETECTED_BLOCKER
- SOURCE_TRACE_MISSING_BLOCKED: BLOCKED | rules=R013_SOURCE_TRACE_REQUIRED | blockers=SOURCE_TRACE_MISSING_BLOCKER
- VALID_SCHEMA_BUT_NOT_APPROVED_BLOCKED: BLOCKED | rules=R001_PROVIDER_APPROVAL_REQUIRED,R002_AUTH_EVIDENCE_REQUIRED | blockers=PROVIDER_NOT_APPROVED_BLOCKER,AUTHORIZATION_EVIDENCE_MISSING_BLOCKER

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
- targeted_p118_p127_tests_status: PASS
- targeted_p118_p127_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Blockers
- APPROVAL_OWNER_MISSING_BLOCKER
- AUDIT_TRAIL_MISSING_BLOCKER
- AUTHORIZATION_EVIDENCE_MISSING_BLOCKER
- DATA_USAGE_SCOPE_MISSING_BLOCKER
- EFFECTIVE_DATE_MISSING_BLOCKER
- EV_CLV_KELLY_UNLOCK_REQUEST_BLOCKER
- EXPIRATION_OR_RENEWAL_MISSING_BLOCKER
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
- FULL_REGRESSION_NOT_RUN_BLOCKER

## Prohibited Actions
- Do not approve provider from fixture-only payloads
- Do not unlock recommendation/EV/CLV/Kelly/stake/profit/production
- Do not ingest real legal odds or activate providers
- Do not call live/paid APIs
- Do not store secret-like values, auth URLs, or private contract body in repo artifacts

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Use deterministic verdicts for governance review only
- Collect real legal evidence via legal/compliance workflow before any approval consideration
- Keep full regression status explicit: PASS/FAIL/NOT_RUN
