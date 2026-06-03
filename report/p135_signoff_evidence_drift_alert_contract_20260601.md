# P135 Sign-off Evidence Drift Alert Contract (2026-06-01)

## Decision
- signoff_drift_alert_contract_status: READY_WITH_BLOCKERS
- source_signoff_replay_gate_status: READY_WITH_BLOCKERS
- source_replay_run_count: 3
- source_signoff_packet_count: 22
- source_invalid_packet_count: 21
- source_drift_detected: False
- final_classification: P135_SIGNOFF_EVIDENCE_DRIFT_ALERT_CONTRACT_READY_WITH_BLOCKERS

## Alert Contract
- alert_level_definitions: {'GREEN_NO_SIGNOFF_DRIFT': 'No drift detected; consistency checks all pass.', 'YELLOW_SIGNOFF_METADATA_ONLY_DRIFT': 'Metadata-only replay deviations detected.', 'ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT': 'Blocker/evidence matrix drift detected.', 'RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT': 'Verdict matrix or escalation coverage drift detected.', 'CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT': 'Unlock/provider/governance invariant drift detected.'}
- drift_type_definitions: {'FINGERPRINT_DRIFT': 'Deterministic replay fingerprint mismatch.', 'SIGNOFF_VERDICT_MATRIX_DRIFT': 'Sign-off verdict matrix differs across runs.', 'BLOCKER_CLASSIFICATION_DRIFT': 'Blocker classification set differs across runs.', 'REQUIRED_EVIDENCE_MATRIX_DRIFT': 'Required evidence matrix differs across runs.', 'ESCALATION_LEVEL_COVERAGE_DRIFT': 'Escalation coverage mapping differs across runs.', 'GOVERNANCE_INVARIANT_DRIFT': 'Governance invariant values changed.', 'UNLOCK_PREVENTION_DRIFT': 'Unlock prevention matrix changed.', 'SIGNOFF_PACKET_COUNT_DRIFT': 'Sign-off packet count changed unexpectedly.', 'INVALID_PACKET_COUNT_DRIFT': 'Invalid packet count changed unexpectedly.', 'REPLAY_METADATA_DRIFT': 'Replay metadata changed unexpectedly.'}
- escalation_path_definitions: {'record_only': 'Record event in governance audit log only.', 'engineering_review': 'Route to engineering owner for review.', 'cto_review': 'Escalate to CTO governance owner.', 'legal_review': 'Escalate to legal owner.', 'compliance_review': 'Escalate to compliance owner.', 'security_review': 'Escalate to security owner.', 'ceo_review': 'Escalate to executive/CEO review.', 'immediate_stop': 'Immediate stop: no governance progression.'}
- sla_class_definitions: {'SLA_NONE_RECORD_ONLY': 'No response time requirement; archival record.', 'SLA_STANDARD_ENGINEERING_REVIEW': 'Standard engineering review window.', 'SLA_CTO_REVIEW': 'Expedited CTO review window.', 'SLA_LEGAL_COMPLIANCE_REVIEW': 'Legal/compliance review required.', 'SLA_SECURITY_REVIEW': 'Security review required.', 'SLA_EXECUTIVE_REVIEW': 'Executive review required.', 'SLA_IMMEDIATE_STOP': 'Immediate stop and incident-style escalation.'}
- required_signoff_owner_matrix: {'GREEN_NO_SIGNOFF_DRIFT': ['engineering_owner'], 'YELLOW_SIGNOFF_METADATA_ONLY_DRIFT': ['engineering_owner', 'compliance_owner'], 'ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT': ['engineering_owner', 'compliance_owner', 'cto_owner'], 'RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT': ['engineering_owner', 'cto_owner', 'legal_owner', 'compliance_owner'], 'CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT': ['engineering_owner', 'cto_owner', 'legal_owner', 'compliance_owner', 'ceo_owner', 'data_rights_owner', 'security_owner']}

## Blocking Conditions
- C001: any previously BLOCKED sign-off verdict becomes ALLOWED (RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT/SIGNOFF_VERDICT_MATRIX_DRIFT)
- C002: valid_signoff_packet_template becomes production-ready (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C003: source_signoff_packet_count changes without approved baseline update (ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT/SIGNOFF_PACKET_COUNT_DRIFT)
- C004: source_invalid_packet_count changes without approved baseline update (ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT/INVALID_PACKET_COUNT_DRIFT)
- C005: blocker classifications change without approved review (ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT/BLOCKER_CLASSIFICATION_DRIFT)
- C006: required evidence matrix changes without approved review (ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT/REQUIRED_EVIDENCE_MATRIX_DRIFT)
- C007: escalation coverage changes without approved review (RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT/ESCALATION_LEVEL_COVERAGE_DRIFT)
- C008: governance invariants become false (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/GOVERNANCE_INVARIANT_DRIFT)
- C009: provider_approved becomes true without verified legal evidence (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/GOVERNANCE_INVARIANT_DRIFT)
- C010: authorization_evidence_present becomes true without verified legal evidence (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/GOVERNANCE_INVARIANT_DRIFT)
- C011: recommendation_allowed becomes true (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C012: production_ready becomes true (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C013: EV/CLV/Kelly/stake/profit unlock becomes true (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C014: real_legal_odds_ingested becomes true without explicit legal/provider approval (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C015: live_api_calls or paid_api_called becomes non-zero (CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT/UNLOCK_PREVENTION_DRIFT)
- C016: drift_detected=true but drift_details is missing or incomplete (RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT/REPLAY_METADATA_DRIFT)
- C017: fingerprint consistency status changes from CONSISTENT (ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT/FINGERPRINT_DRIFT)

## Drift Rule Sets
- verdict_matrix_drift_rules: {'blocked_to_allowed_is_blocking': True, 'valid_template_status_must_remain_governance_only_pending_review': True, 'required_alert_level_for_verdict_drift': 'RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT', 'required_escalation_path': 'cto_review'}
- blocker_classification_drift_rules: {'blocker_set_change_without_review_is_blocking': True, 'required_alert_level': 'ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT', 'required_escalation_path': 'compliance_review'}
- required_evidence_matrix_drift_rules: {'evidence_matrix_change_without_review_is_blocking': True, 'required_alert_level': 'ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT', 'required_escalation_path': 'legal_review'}
- escalation_level_coverage_drift_rules: {'coverage_change_without_review_is_blocking': True, 'required_alert_level': 'RED_SIGNOFF_VERDICT_OR_ESCALATION_COVERAGE_DRIFT', 'required_escalation_path': 'cto_review'}
- governance_invariant_drift_rules: {'any_false_invariant_is_critical_blocking': True, 'required_alert_level': 'CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT', 'required_escalation_path': 'immediate_stop'}
- unlock_prevention_drift_rules: {'any_unlock_flag_true_is_critical_blocking': True, 'provider_or_authorization_true_without_legal_evidence_is_critical': True, 'live_or_paid_api_nonzero_is_critical': True, 'required_alert_level': 'CRITICAL_SIGNOFF_UNLOCK_OR_PROVIDER_DRIFT', 'required_escalation_path': 'immediate_stop'}
- fingerprint_drift_rules: {'fingerprint_mismatch_is_blocking': True, 'required_alert_level': 'ORANGE_SIGNOFF_BLOCKER_OR_EVIDENCE_MATRIX_DRIFT', 'required_escalation_path': 'engineering_review', 'hash_algorithm': 'sha256'}
- drift_details_required_fields: ['drift_event_id', 'drift_type', 'alert_level', 'source_packet_id_or_matrix', 'baseline_value', 'observed_value', 'affected_roles', 'affected_blocker_codes', 'affected_unlock_flags', 'escalation_path', 'sla_class', 'required_signoff_owners', 'reviewer_owner', 'remediation_required', 'rollback_required', 'non_unlock_attestation_required', 'created_at', 'final_blocked_status']

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
- targeted_p118_p135_tests_status: PASS
- targeted_p118_p135_tests_command: /Users/kelvin/Kelvin-WorkSpace/Betting-pool/.venv/bin/python -m pytest tests/test_p135_signoff_evidence_drift_alert_contract.py tests/test_p134_signoff_evidence_replay_consistency_gate.py tests/test_p133_escalation_signoff_evidence_packet_validator.py tests/test_p132_decision_card_escalation_router.py tests/test_p131_baseline_change_review_packet_runner_decision_card.py tests/test_p130_baseline_change_review_packet_validator.py tests/test_p129_replay_drift_alert_contract.py tests/test_p128_deterministic_replay_consistency_gate.py tests/test_p127_intake_payload_evaluation_runner_verdict_report.py tests/test_p126_legal_evidence_intake_payload_fixture_negative_cases.py tests/test_p125_legal_evidence_intake_schema_review_owner_gate.py tests/test_p124_legal_evidence_completeness_contract.py tests/test_p123_provider_evidence_validation_gate.py tests/test_p122_paper_only_recommendation_readiness_review.py tests/test_p121_provider_authorization_evidence_placeholder.py tests/test_p120_legal_provider_authorization_checklist.py tests/test_p119_recommendation_row_gate_violation_fixture.py tests/test_p118_recommendation_row_validation_gate.py
- full_regression_status: NOT_RUN

## Prohibited Actions
- Do not ingest real odds or call live/paid APIs
- Do not unlock provider/recommendation/production/EV/CLV/Kelly/stake/profit
- Do not treat drift alert review as legal provider approval or production readiness
- Do not bypass blocker resolution and sign-off owner requirements

## Allowed Next Actions
- Keep paper_only=true and diagnostic_only=true
- Use drift alert contract for governance diagnostics only
- Require approved baseline review before accepting structural drift
- Keep full regression state explicit: PASS/FAIL/NOT_RUN
