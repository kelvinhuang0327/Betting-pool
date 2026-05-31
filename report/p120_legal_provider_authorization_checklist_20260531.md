# P120 Legal Provider Authorization Checklist (2026-05-31)

## 摘要
本文件為 P120 法定盤口來源授權檢查清單，僅用於診斷與治理驗證，無任何實際盤口、賠率、推薦、EV、CLV、Kelly 或生產邏輯。所有市場、來源、資料存取皆預設為「未授權」或「禁止」，僅允許未來合規審查後依規範逐步開放。

## 產出檔案
- data/mlb_2026/derived/p120_legal_provider_authorization_checklist_summary.json
- report/p120_legal_provider_authorization_checklist_20260531.md

## Checklist 主要區塊
- checklist_metadata
- source_p119_gate_violation_reference
- source_p118_gate_reference
- authorization_scope
- legal_provider_authorization_requirements
- provider_contract_requirements
- data_license_requirements
- market_coverage_requirements
- odds_access_method_requirements
- source_trace_requirements
- audit_log_requirements
- data_retention_requirements
- security_and_secret_handling_requirements
- compliance_review_requirements
- blocked_until_authorized_items
- future_integration_gates
- allowed_future_actions
- prohibited_actions
- market_authorization_matrix
- blocker_category_coverage

## 主要治理與禁止事項
- 所有盤口來源、API、資料存取皆需明確授權與合約
- 禁止任何形式的 scraping、未授權 API、未經審查的資料存取
- 禁止產生任何推薦、賠率、EV、CLV、Kelly 倉位等生產邏輯
- 僅允許 paper-only、diagnostic-only、合約驗證、治理審查
- 所有敏感資訊、憑證、密鑰、帳號必須嚴格隔離與審查
- 未來如需開放，須逐項通過合約、法遵、治理審查

## 測試與驗證
- tests/test_p120_legal_provider_authorization_checklist.py 全數通過
- tests/test_p119_recommendation_row_gate_violation_fixture.py 全數通過
- tests/test_p118_recommendation_row_validation_gate.py 全數通過

## 最終分類
- P120_LEGAL_PROVIDER_AUTHORIZATION_CHECKLIST_READY_DIAGNOSTIC_ONLY

---

本 checklist 僅供治理、法遵、合約審查參考，嚴禁用於任何生產、推薦、賠率、投注、或未經授權之用途。