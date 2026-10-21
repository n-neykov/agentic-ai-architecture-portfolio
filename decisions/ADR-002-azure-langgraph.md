# ADR-002 — Azure AI Foundry with replaceable orchestration

**Status: Accepted; live Foundry integration user-verified**

## Decision

Use a local Python adapter supporting Azure AI Foundry project's Responses API and legacy Azure OpenAI resource endpoints. The primary v2 mode uses GPT-4.1 mini for bounded tool selection. Keep an offline deterministic LangGraph baseline and fake-model unit tests for repeatability.

## Rationale

Foundry provides a managed model endpoint while the application retains authority for identity scoping, tool arguments and safety vetoes. Keeping the inference adapter separate enables local tests without Azure credentials.

## Implemented technical contract

The Foundry adapter normalizes a project endpoint to `/openai/v1/`, calls the OpenAI SDK Responses API with separate system instructions and user inputs, sets `store=False`, and limits output tokens/retries. The server parses a strict allowlisted JSON tool decision. No native provider-managed tool execution is claimed.

## Alternatives

Fully managed agent orchestration, custom multi-agent infrastructure, and deterministic templates only.

## Consequences

Live inference introduces cloud latency, charges, endpoint/credential management and model failure modes. No production cost/SLA measurement, Entra authentication, or deployed service is provided. See [Azure integration](../docs/azure-foundry.md).
