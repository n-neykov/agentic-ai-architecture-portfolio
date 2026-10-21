# ADR-002 — Azure OpenAI with LangGraph

**Status:** Accepted for prototype

## Decision
Use LangGraph for explicit graph transitions and Azure OpenAI through a replaceable Python adapter for supported public FAQ generation.

## Rationale
LangGraph makes branching, state and error paths visible. Azure OpenAI aligns with Microsoft-centric enterprise architecture, but model inference remains an optional dependency so offline tests run without cloud resources.

## Alternatives
Azure-managed agent orchestration, a custom orchestration framework, and deterministic templates only.

## Consequences
Requires Python dependencies, Azure resource provisioning and cost monitoring for live use. The adapter does not constitute a verified Azure deployment.

## Validation
Run dependency-free tests locally; run full graph tests in CI; run optional live Azure smoke tests only after credentials and budget controls are configured.
