# Project 01 — Secure AI Customer Service Orchestration Platform

**Status:** Implemented offline reference prototype; live cloud inference not verified.

## Overview

This case study explores a policy-first, hybrid agent workflow for a fictional financial-services support operation. LangGraph coordinates deterministic routing, read-only account access, approved FAQ retrieval, and bounded optional language generation.

## Technical deliverables

| Component | Repository path |
|---|---|
| Architecture and trust boundaries | [Logical architecture](../architecture/system.md) |
| Solution rationale | [Case study](../docs/case-study.md) |
| Workflow implementation | [LangGraph workflow](../src/support_agent/workflow.py) |
| Security and request policy | [Core router](../src/support_agent/core.py) |
| Data adapters | [Synthetic CRM and FAQ retrieval](../src/support_agent/integrations.py) |
| Cloud adapter | [Optional Azure OpenAI](../src/support_agent/azure_model.py) |
| Automated tests | [Test suite](../tests/) |
| Scenario evaluation | [Evaluation design](../evaluations/evaluation-plan.md) |
| Architecture decisions | [ADR index](../decisions/) |
| Operational limitations | [Release readiness](../docs/release-readiness.md) |

## Reproducibility

From the repository root, with Python 3.11 and dependencies installed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
```

The offline suite has been run on Windows with 18 tests passing and the synthetic evaluation passing 10 of 10 scenarios. These results do not validate production identity, external CRM authorization, or live cloud inference.
