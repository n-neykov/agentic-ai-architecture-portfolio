# Case Study 01 — Secure AI Customer Service Orchestration

**Independent engineering prototype · Fictional financial-services scenario**

## Business problem

A hypothetical support operation handling 50,000 monthly inquiries wants to automate repeatable informational requests while ensuring that an LLM cannot authorize transactions or reveal another customer's account data. The volume is a **planning assumption**, not observed traffic.

## Stakeholders

Support operations, enterprise architecture, security/IAM, compliance, product ownership, engineering and customer service.

## Implemented solution

- **Deterministic policy gate** screens known sensitive operations, cross-account references and anonymous balance inquiries before inference.
- **Azure AI Foundry GPT-4.1 mini** proposes validated, allowlisted tool selections for permitted requests.
- **V2 orchestration** handles a combination of public FAQ and synthetic own-account balance inquiries, plus simulated session information.
- **Twelve approved fictional FAQ records** use categorized keyword retrieval with stable evidence IDs.
- **Read-only synthetic account adapter** returns balances based on the simulated session identity rather than prompt-supplied account identifiers.
- **Streamlit dashboard** presents live and offline modes, execution metadata, a baseline evaluation, and an architecture diagram.

## Key design decision

The language model assists with bounded decisions but never becomes the source of authority for account access or sensitive operations. The model's JSON selection must match the server's permitted intent. The design accepts restricted flexibility and potential escalation in exchange for a clearer authorization boundary.

## Observed demonstration evidence

Screenshots supplied **2026-10-22** show **97/97 portfolio-wide tests passing** and **10/10 deterministic baseline scenarios passing** following malformed-bank regression fixes. Live Foundry demonstrations include approved multi-intent and pre-inference account-scope denial. Results are user-executed local evidence, not independently reproduced CI or production metrics.

## Hypothetical pilot targets — not achieved metrics

95% grounded FAQ accuracy on an agreed evaluation set; zero cross-account exposure in defined adversarial tests; 100% escalation for agreed high-risk cases; p95 latency below five seconds; and 60% routine-inquiry containment. These are illustrative acceptance criteria, not performance results.

## Production gaps

No verified identity, downstream CRM authorization, production data, semantic RAG, staffed escalation queue, real deployment, load testing, cost measurement, or complete security evaluation. Keyword risk screening is insufficient for production policy enforcement.

[Architecture](../architecture/system.md) · [Azure integration](azure-foundry.md) · [Threat model](threat-model.md) · [Release evidence](release-readiness.md)
