# Architecture assurance and implementation boundaries

**Scope:** Three synthetic Python reference projects, shared Azure Foundry model adapter, Streamlit dashboard, architecture diagrams, tests, and evidence documentation.

This document records **implemented controls, design tradeoffs and known limitations**. It is not a penetration-test certificate, full-history credential attestation or production deployment approval.

## Implemented architecture

| Project | Control design | Deliberate limitation |
|---|---|---|
| 01 · Secure Customer Service | Deterministic high-risk/account-scope preflight, allowlisted model nominations, synthetic read-only balances, FAQ evidence IDs | No verified authentication, general-purpose intent coverage or production CRM |
| 02 · Intelligent Document Processing | Offline/AI-assisted extraction, exact labeled-line verification, validation, sensitive-field review, tenant-scoped in-memory staging | No OCR, arbitrary-document extraction, authenticated reviewer or durable queue |
| 03 · Governed Enterprise Agent Platform | Registered tool names, simulated role/tenant checks, pre-inference tenant denial, disconnected approval-gated write | No real IAM, external tool execution or durable audit service |
| Shared Azure adapter | Local Foundry Responses integration, bounded output, timeout/retry settings, `store=False` request parameter | No managed identity, provider retention guarantee or cloud performance certification |

## Architectural decisions and residual risks

1. **Pre-inference safety is deliberately narrow.** Known high-risk terms and explicit synthetic account IDs are screened before optional model calls. Regex/keyword matching can miss paraphrases or overblock benign terms; real authorization must be enforced by trusted downstream systems.
2. **The LLM does not authorize actions.** In Project 01, the server preplans supported intents and validates model-nominated tools. Multi-intent mode can use canonical per-intent prompts. This is bounded routing, not an autonomous multi-agent planner or provider-native function calling.
3. **Extraction requires exact source labels.** Project 02 validates model-proposed values against a deterministic labeled-line extractor. This is intentionally not OCR or a general document-understanding benchmark.
4. **Review is simulated.** A reviewer name is a string and approval/staging live in memory. Malformed bank-account labels remain blocked; only the explicitly reviewable bank-detail issue can be waived.
5. **Tenant/role controls use fictional principals.** Project 03 checks tenant and role in Python against synthetic records; it does not verify JWTs or delegate authorization to a data plane.
6. **Writes remain disconnected.** Payment update selection and approval are demonstrable but no external payment operation is implemented.
7. **Observability is local.** In-memory audit events and downloadable JSON illustrate decisions, not immutable audit logs or distributed tracing.
8. **Operational metrics are not measured.** No p95 latency, model accuracy, cloud spend, SLA, ROI or production availability is claimed.

## Recorded acceptance evidence

Local acceptance runs dated **2026-10-22** show **97/97 automated tests passing** and **10/10 deterministic baseline scenarios passing**. The [execution gallery](demonstration-evidence.md) includes live Azure demonstrations of approved multi-intent support, pre-inference cross-account denial, staged invoice extraction, sensitive-field review, authorized tenant-A lookup and pre-inference cross-tenant denial.

These results validate **known synthetic scenarios**, not comprehensive security or general model accuracy. The exact local code revision used for screenshot capture was not recorded. GitHub Actions status and full-history credential scanning must be checked independently.

## Final publication gates

- [x] Automated local suite: 97 tests, no failures/errors (2026-10-22)
- [x] Deterministic baseline: 10/10 scenarios (2026-10-22)
- [x] Six live Azure execution outcomes documented with screenshots
- [ ] Confirm GitHub Actions success for the published revision
- [ ] Run a credential scanner against **all Git history**
- [ ] Inspect all three architecture tabs and rendered Mermaid diagrams

**Release classification:** Demonstration-ready synthetic engineering portfolio. **Not production-certified or deployed.**

[Portfolio overview](../README.md) · [Threat model](threat-model.md) · [Test plan](portfolio-test-plan.md)
