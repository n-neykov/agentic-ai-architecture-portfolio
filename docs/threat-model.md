# Project 01 — STRIDE-inspired threat model

**Assets:** synthetic identity context, fictional account records, approved FAQ documents, Azure inference credentials, tool permissions, and execution evidence.

| Threat | Example attack | Implemented mitigation | Production gap |
|---|---|---|---|
| Spoofing | Caller chooses another user | Demo `TrustedContext` separates identity from message text; account IDs in text cannot override it | Identity selector itself is unverified; require OIDC/Entra ID and downstream checks |
| Information disclosure | `user-001` requests `user-002` balance | Explicit synthetic account references are compared against session principal before inference | Pattern matching is narrow; real tenant-aware authorization and robust entity parsing needed |
| Prompt injection | Customer text instructs model to bypass policy | Deterministic veto and JSON tool allowlist; no write tools | Adversarial and paraphrase testing incomplete |
| Elevation of privilege | Agent sends funds or changes credentials | No write or transaction tools; recognized sensitive requests escalate | Real approval workflow and transaction authorization absent |
| Denial of service | Azure outage, timeout or malformed output | Model exceptions and mismatches escalate; limited retries and timeout | Rate limiting, quotas, circuit breaker and SLO monitoring absent |
| Repudiation | User disputes an agent action | Execution metadata and optional local JSON export | No tamper-evident audit store or trace correlation |
| Credential disclosure | API key exposed in source or screenshot | Local `.env` and example placeholders; no intentional key logging | Managed identity/Key Vault and credential scanning not integrated |

## Incident-response exercise

If cross-account information is suspected to have leaked, disable the account-read capability, preserve relevant evidence securely, assess the exposure and affected users, notify the appropriate security/privacy stakeholders, fix the authorization boundary, rerun negative tests, and require release approval before restoration.

**Residual risk:** the synthetic identity selector and keyword policy are **not** production authentication or comprehensive security controls. Do not process real customer data.
