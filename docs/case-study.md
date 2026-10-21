# Case Study 01 — Secure Customer Service Orchestration

**Type:** Independent architecture and prototype; fictional financial-services scenario.

## Business problem
A hypothetical mid-market financial services organization receives 50,000 monthly support inquiries. Its operations team wants to reduce repetitive FAQ work without allowing AI systems to perform unauthorized transactions or expose account data.

## Stakeholders
Customer support operations, security/IAM, engineering, compliance, product owner, customer representatives.

## Functional scope
- Answer public FAQs from approved synthetic documents.
- Return synthetic account balances through a read-only CRM adapter scoped to the caller's asserted identity.
- Deny anonymous account access.
- Escalate sensitive and unsupported requests.
- Provide evidence IDs for FAQ answers.

## Out of scope
Real customer data, real CRM access, money transfers, account changes, production authentication, and regulated financial advice.

## Hypothetical pilot acceptance targets (NOT measured)
- 95% grounded FAQ accuracy on an agreed evaluation corpus
- 100% high-risk escalation on a defined test suite
- 0 cross-account exposures on defined adversarial tests
- FAQ p95 latency under 5 seconds
- 60% routine inquiry containment, subject to a validated baseline

## Design approach
A policy-first hybrid architecture with deterministic authorization/routing and LangGraph orchestration. The Azure OpenAI adapter is optional and is used only for supported public FAQ synthesis; it never determines account authorization.

## Status
Working source and synthetic tests are provided. The Azure adapter has not been validated against a live deployment, and the project has no production deployment or measured ROI.
