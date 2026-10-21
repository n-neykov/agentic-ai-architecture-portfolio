# ADR-001 — Hybrid policy-first agent orchestration

**Status: Accepted and implemented for synthetic Project 01**

## Decision

Keep recognized high-risk actions, cross-account references and anonymous private-data requests under deterministic application policy. Use LangGraph for an offline baseline and a bounded v2 orchestrator for multi-intent requests. GPT-4.1 mini through Azure AI Foundry can propose strict JSON tool choices, but cannot grant account access or execute writes.

## Why

An unrestricted autonomous agent adds cost, complexity and security exposure without a compelling requirement for this narrow support workload. Read-only tools, explicit fallback and a reproducible offline suite offer clearer assurance boundaries.

## Alternatives considered

- Fully managed vendor agent: faster possible deployment, but unknown commercial/integration constraints.
- Autonomous multi-agent orchestration: greater flexibility, harder permissioning and audit.
- Deterministic-only workflow: simple and cheap, but no live model-driven selection.
- **Chosen hybrid:** deterministic authority with bounded model assistance.

## Accepted limitations

Keyword policy misses paraphrases, v2 intent planning remains deterministic, JSON selection is not native provider tool calling, and production IAM/CRM authorization are absent. Escalation may increase containment cost.

## Evidence

User-verified live GPT-4.1 mini scenarios, 53 passing tests and 10/10 baseline evaluation **before** the 12-FAQ expansion. New tests require rerun.
