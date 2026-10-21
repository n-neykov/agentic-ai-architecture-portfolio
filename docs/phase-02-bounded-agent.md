# Phase 2 — Bounded model-driven tool selection

**Status:** Implemented reference code on a feature branch. Fake-model contract tests are supplied; a real Azure OpenAI agent call is **not yet validated**.

## What is new

The original workflow uses deterministic keyword-based classification. This optional mode asks an LLM to select one of three tools using a strictly validated JSON decision:

- `faq_lookup`: approved static keyword corpus; no arbitrary web or database access
- `account_balance`: read-only synthetic CRM, always scoped to server-supplied demo principal
- `escalate`: route to human review

The LLM selects a tool, **not its arguments or permissions**. A deterministic policy veto runs before the model and again before each adapter. Sensitive actions never reach the model; unknown or invalid model outputs fail closed.

## Why hybrid rather than unrestricted autonomy?

| Choice | Advantage | Tradeoff |
|---|---|---|
| Fully autonomous tool-calling agent | Flexible planning | Harder to bound authority and demonstrate safety |
| Fully deterministic router (baseline) | Simple, repeatable, inexpensive | No model-driven tool selection |
| **Bounded model tool selection (this phase)** | Demonstrates an LLM decision within enforceable constraints | Additional latency/cost; restricted tools and intent vocabulary; no autonomous planning |

## Run the offline tests

From repository root, with dependencies installed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m unittest tests.test_bounded_agent -v
```

The tests inject a `FakeModel` returning model-like JSON. They cover public FAQ, synthetic cross-account text, unauthenticated access, high-risk transfers, unexpected tools, extra arguments, malformed JSON, outages and unknown questions. **Fake-model tests do not prove live model compliance, adversarial robustness or production authorization.**

## Optional Azure demonstration

With your own Azure OpenAI configuration in `.env`, run:

```powershell
.\.venv\Scripts\python.exe -m src.support_agent.cli --agent --azure --message "What are your hours?"
.\.venv\Scripts\python.exe -m src.support_agent.cli --agent --azure --principal user-001 --message "Show user-002 balance"
```

`--principal` is simulated identity, **not verified authentication**. Do not connect this demo to customer data. Live Azure calls can incur charges.

## Production gaps

Validate OIDC/JWT identity and tenant permissions at an external gateway and each adapter; use strict provider-native structured tool calling where supported; add trace redaction, cost and latency budgets, adversarial and integration evaluations, rate limiting, prompt-injection defenses, and human-review operations. This prototype's keyword policy can miss paraphrases and must not be treated as comprehensive security enforcement.
