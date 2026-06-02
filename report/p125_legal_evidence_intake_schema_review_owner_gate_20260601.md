# P125 Legal Evidence Intake Schema + Review Owner Gate (2026-06-01)

## Decision
- intake_schema_status: READY_WITH_BLOCKERS
- review_owner_gate_status: BLOCKED
- final_classification: P125_LEGAL_EVIDENCE_INTAKE_SCHEMA_REVIEW_OWNER_GATE_READY_WITH_BLOCKERS

## Core Validation Fields
- provider_approved: False
- authorization_evidence_present: False
- placeholder_detected: True
- placeholder_allowed_as_authorization: False
- real_legal_odds_ingested: False

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

## Intake/Review Contract Groups
- required_intake_fields:
  - intake_id
  - evidence_type
  - legal_document_reference_id
  - provider_legal_name
  - provider_identifier
  - submitted_by
  - submitted_at
  - review_owner
  - review_status
  - approval_owner
  - authorized_sports
  - authorized_leagues
  - authorized_markets
  - authorized_data_types
  - authorized_usage_scope
  - authorized_environment
  - effective_date
  - expiration_date
  - renewal_review_date
  - source_trace_reference
  - audit_trail_reference
  - restriction_notes
  - repository_storage_policy
  - secret_exclusion_attestation
  - private_contract_body_excluded
  - row_level_proprietary_odds_excluded
- required_review_owner_fields:
  - review_owner
  - review_owner_role
  - review_owner_identity_reference
  - review_owner_attested_at
  - review_status
- required_approval_workflow_fields:
  - approval_owner
  - approval_status
  - approval_decision_at
  - approval_decision_reference
  - approval_scope_attestation
- required_legal_document_reference_fields:
  - legal_document_reference_id
  - legal_document_external_reference
  - legal_document_type
  - legal_document_review_status
- required_scope_fields:
  - authorized_sports
  - authorized_leagues
  - authorized_markets
  - authorized_data_types
  - authorized_usage_scope
  - authorized_environment
- required_date_fields:
  - effective_date
  - expiration_date
  - renewal_review_date
- required_provider_identity_fields:
  - provider_legal_name
  - provider_identifier
  - provider_approval_status
- required_data_rights_fields:
  - row_level_proprietary_odds_excluded
  - separate_data_rights_decision_reference
  - repository_storage_policy
- required_repository_safety_fields:
  - paper_only_required
  - diagnostic_only_required
  - no_recommendation_unlock_without_approval
  - no_production_unlock_without_approval
- required_secret_exclusion_fields:
  - secret_exclusion_attestation
  - private_contract_body_excluded
  - no_api_key_in_repo
  - no_token_or_credentials_in_repo
  - no_auth_url_in_repo
- required_reviewer_attestation_fields:
  - review_owner_attestation
  - approval_owner_attestation
  - scope_completeness_attestation
  - repository_safety_attestation

## Rule Sets
- intake_validation_rules:
  - must_include_required_intake_fields: True
  - must_include_legal_document_reference: True
  - must_include_provider_identity: True
  - must_include_scope_fields: True
  - must_include_effective_and_expiration_or_renewal: True
  - must_include_source_trace_and_audit_reference: True
  - must_include_secret_exclusion_attestation: True
  - must_exclude_private_contract_body: True
  - must_exclude_row_level_proprietary_odds_without_data_rights_decision: True
- review_owner_validation_rules:
  - review_owner_required: True
  - approval_owner_required: True
  - review_status_must_be_explicit: True
  - approved_status_requires_authorized_reviewer: True
  - missing_owner_means_blocked: True
- blocked_state_rules:
  - missing_review_owner_blocked: True
  - missing_approval_owner_blocked: True
  - review_not_explicitly_approved_blocked: True
  - missing_legal_document_reference_blocked: True
  - missing_provider_identity_blocked: True
  - missing_scope_fields_blocked: True
  - missing_effective_date_blocked: True
  - missing_expiration_or_renewal_blocked: True
  - missing_source_trace_or_audit_blocked: True
  - missing_secret_exclusion_attestation_blocked: True
  - private_contract_body_present_blocked: True
  - secret_like_field_detected_blocked: True
  - placeholder_detected_blocked: True
  - unlock_requested_without_approval_blocked: True
- placeholder_rejection_rules:
  - placeholder_detected_means_blocked: True
  - placeholder_allowed_as_authorization_must_be_false: True
  - placeholder_cannot_set_provider_approved: True
  - placeholder_cannot_set_authorization_evidence_present: True

## Regression/Test Status
- targeted_p118_p124_tests_status: PASS
- targeted_p118_p125_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN
- full_regression_evidence: No full regression artifact found in P121 packet.

## Blockers
- REVIEW_OWNER_MISSING_BLOCKER
- APPROVAL_OWNER_MISSING_BLOCKER
- REVIEW_STATUS_NOT_EXPLICITLY_APPROVED_BLOCKER
- LEGAL_DOCUMENT_REFERENCE_MISSING_BLOCKER
- PROVIDER_IDENTITY_MISSING_BLOCKER
- SCOPE_FIELDS_MISSING_BLOCKER
- EFFECTIVE_DATE_MISSING_BLOCKER
- EXPIRATION_OR_RENEWAL_MISSING_BLOCKER
- SOURCE_TRACE_OR_AUDIT_MISSING_BLOCKER
- SECRET_EXCLUSION_ATTESTATION_MISSING_BLOCKER
- PRIVATE_CONTRACT_BODY_PRESENT_BLOCKER
- SECRET_OR_AUTH_URL_DETECTED_BLOCKER
- PLACEHOLDER_DETECTED_BLOCKER
- UNLOCK_REQUEST_WITHOUT_APPROVAL_BLOCKER
- FULL_REGRESSION_NOT_RUN_BLOCKER

## Prohibited Actions
- Do not treat placeholder evidence as approved legal authorization
- Do not unlock provider, recommendation, EV, CLV, Kelly, stake, profit, or production
- Do not store API keys, tokens, credentials, auth URLs, or private contract body in repo artifacts
- Do not ingest real legal odds or call live/paid APIs from this schema/gate task

## Allowed Next Actions
- Maintain paper_only=true and diagnostic_only=true
- Submit intake payload with complete legal reference metadata and review owner fields
- Keep review_status blocked until authorized reviewer and approval owner attestations are complete
- Keep full regression status explicit as PASS/FAIL/NOT_RUN
