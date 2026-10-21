# Threat model — STRIDE-inspired

**Assets:** customer identity, account data, approved documents, inference credentials, logs, tool permissions.

| Threat | Attack path | Prototype mitigation | Production gap |
|---|---|---|---|
| Spoofing | Forged customer identity | TrustedContext object separates message text from principal | Real Entra ID token validation absent |
| Information disclosure | User requests another account | CRM adapter uses principal, not message ID | Real CRM tenant authorization absent |
| Tampering / prompt injection | Malicious retrieved text | Fixed corpus, evidence-only grounding prompt | Robust adversarial tests and isolation absent |
| Elevation of privilege | Agent executes a transfer | No transactional tools; deterministic escalation | External authorization and approval workflow absent |
| Denial of service | Model outage or timeout | Error fallback to human escalation | Rate limits, circuit breaker, SLOs absent |
| Repudiation | User denies sensitive action | No sensitive action implemented | Tamper-evident audit trail absent |
| Credential disclosure | API key in repository | .gitignore and .env.example | Managed identity / Key Vault not integrated |

**Incident response exercise:** For a suspected cross-account exposure, disable account-read path, preserve logs/evidence, identify affected sessions, remediate authorization, run negative tests, review privacy obligations and obtain approval before restoring service.

**Residual risk:** This project must not process real customer records.
