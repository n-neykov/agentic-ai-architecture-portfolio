# ADR-001 — Hybrid deterministic and agentic orchestration

**Status:** Accepted

## Decision
Use deterministic policy routing for authentication gates, account requests and high-risk operations. Use LangGraph to express the workflow and optional Azure OpenAI only for synthesis over approved public FAQs.

## Why
A fictional financial-services client has cost and deadline constraints. A fully autonomous agent increases complexity, token usage, and the surface area for prompt injection without demonstrable business value for routine requests.

## Alternatives
- Fully managed vendor agent: faster deployment, but unknown licensing and integration constraints.
- Fully custom autonomous multi-agent platform: maximum flexibility but disproportionate MVP complexity.
- Purely deterministic chatbot: cheap and auditable but limited language flexibility.

## Tradeoff
Hybrid routing reduces freedom and increases explicit workflow code; it improves testability, cost predictability and access-control separation.

## Revisit when
Real task complexity, operational benchmarks, and vendor constraints justify adding more autonomous behavior.
