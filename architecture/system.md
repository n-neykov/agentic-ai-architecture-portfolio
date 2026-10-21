# Logical architecture

```mermaid
flowchart TD
  U[Customer / CLI demo] --> G[Trusted application boundary]
  G --> R[LangGraph policy router]
  R -->|Public FAQ| K[Approved keyword knowledge retrieval]
  K -->|Evidence available| L[Optional Azure OpenAI response generation]
  K -->|No evidence| H[Human escalation]
  L --> V[Grounding prompt and fallback]
  R -->|Account balance and authenticated| C[Read-only synthetic CRM adapter]
  R -->|Anonymous account request| D[Deny]
  R -->|High-risk request| H
  C --> O[Response]
  V --> O
  D --> O
  H --> O
```

## Trust boundaries
1. **Customer input is untrusted.** Customer identifiers in messages cannot choose the CRM record.
2. **Demo context is a simulation.** `TrustedContext` is not a verified identity token. In production it must be created from validated OIDC identity provider claims.
3. **CRM authorization remains outside the LLM.** The model cannot invoke a tool with an arbitrary account ID.
4. **Retrieved content is untrusted data.** Prompt instructions within documents must not be executed; current grounding prompt is insufficient alone for production assurance.
5. **No mutation tools.** Transfers and sensitive account changes are escalated.

## Failure handling
Missing FAQ evidence and model exceptions result in escalation. No autonomous retries of financial transactions exist because transactional tools are not exposed.

## Planned enterprise extensions
OIDC identity provider token validation; external tenant-aware CRM authorization; Azure AI Search; redacted distributed traces; deployment pipelines; evaluation and load testing.
