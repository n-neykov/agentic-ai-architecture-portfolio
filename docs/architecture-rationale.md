# Architecture rationale

## Context
A fictional financial services support operation handles 50,000 monthly requests. The design prioritizes FAQ containment and data isolation.

## Architectural choice
Hybrid policy-first orchestration uses deterministic routing for authorization and high-risk requests, with LangGraph for explicit workflow transitions and optional language generation for approved FAQ content.

## Request paths
- Public FAQ: keyword retrieval and optional grounded response.
- Account inquiry: application-supplied principal and read-only synthetic CRM lookup.
- High-risk operation: escalation without transactional tools.

## Security boundaries
Message content never determines account identity. CLI principal assertions are simulated and do not constitute authentication. Production deployment requires independent identity validation and CRM-side authorization.

## Evidence and limitations
Synthetic tests cover selected routing and privacy scenarios. Live cloud inference, production security, operational latency, and financial outcomes are not verified.
