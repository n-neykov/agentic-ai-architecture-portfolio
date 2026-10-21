# ADR-003 — Server-authorized tools and safe fallback

**Status:** Accepted for prototype; production controls outstanding.

## Context
A customer-facing agent must not infer authority from user-supplied text or LLM-generated tool arguments. A missing/failed Azure model response must not result in fabricated account facts.

## Decision
1. Identity is represented by a trusted-context object supplied by the application boundary; the CLI simulates this boundary, **not** an identity provider.
2. CRM balance lookup accepts only the principal from trusted context. The LLM is not permitted to select account IDs.
3. High-risk actions are routed to human escalation before any model invocation.
4. Approved-document retrieval returns document identifiers and evidence; absent evidence or failed inference results in escalation.
5. No payment, account modification, or transactional tool is exposed.

## Alternatives
- LLM-selected account identifiers: rejected due to authorization risk.
- Vectorizing CRM balances: rejected due to stale and sensitive data exposure.
- Full autonomous multi-agent system: rejected for the bounded FAQ MVP due to cost, complexity and auditability.

## Consequences / residual risks
This prototype does not validate OIDC identity provider tokens, implement tenant isolation, enforce authorization in an external CRM, verify generated answer entailment, or persist audit traces. These are release blockers, not implied capabilities.
