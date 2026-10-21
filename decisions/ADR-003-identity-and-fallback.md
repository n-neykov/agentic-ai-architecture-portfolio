# ADR-003 — Identity-scoped read-only tools and fail-closed outcomes

**Status: Accepted for prototype; production authorization not implemented**

## Decision

1. Simulated session identity is supplied outside customer text. It is **not** verified IAM.
2. Explicit references to another synthetic user are denied before model invocation; matching own-account references can proceed.
3. The read-only balance adapter accepts only the simulated session principal; the LLM cannot supply account IDs.
4. Known high-risk requests escalate before model invocation.
5. Model failures, mismatched/invalid tool decisions and missing evidence escalate.
6. No write, money transfer or account modification tools exist.

## Tradeoffs

The explicit synthetic-ID matching and keyword policy are intentionally narrow. This is not tenant-aware production authorization, comprehensive prompt-injection protection or an integrated human queue. Real deployment requires validated Entra/OIDC identity, CRM-side authorization, redacted audit trails and incident procedures.

## Evidence

Offline tests and user-observed live Foundry scenarios demonstrate the bounded fixture behavior, not real customer security.
