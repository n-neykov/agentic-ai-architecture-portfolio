# Project 01 — Secure AI Customer Service Orchestration Platform

**Status:** Implemented offline Python/LangGraph reference prototype. No live cloud inference or production customer system has been validated.

## Scenario and objective

A fictional financial-services support team receives repetitive public FAQs, requests for account balances, and sensitive requests such as transfers. The design objective is to automate narrow, verifiable tasks while keeping authorization and high-risk operations outside the model.

## Request path and controls

1. A CLI request enters a deterministic policy router in [`workflow.py`](../src/support_agent/workflow.py).
2. High-risk keywords (transfers, wires, password resets and similar) escalate before retrieval or model inference.
3. Balance requests require a simulated trusted context. The [synthetic CRM adapter](../src/support_agent/integrations.py) uses the principal from that context, not an account ID in the message.
4. Public FAQ requests use a fixed approved keyword corpus. Missing evidence escalates.
5. An optional [model adapter](../src/support_agent/azure_model.py) generates text only after FAQ retrieval; inference errors escalate.

The prototype's classifier is keyword-based, so its routing is **not a production-grade intent or authorization system**. The CLI's `--principal` parameter simulates identity and cannot validate it.

## Architecture and implementation

| Artifact | Location |
|---|---|
| Logical diagram and trust boundaries | [System architecture](../architecture/system.md) |
| Working LangGraph state machine | [Workflow](../src/support_agent/workflow.py) |
| Dependency-free baseline | [Core router](../src/support_agent/core.py) |
| Synthetic CRM and FAQ evidence | [Adapters](../src/support_agent/integrations.py) |
| Optional Azure OpenAI adapter | [Model](../src/support_agent/azure_model.py) |
| Automated tests | [Tests](../tests/) |
| Ten scenario definitions | [Evaluation code](../src/support_agent/evaluation.py) |
| STRIDE-inspired security analysis | [Threat model](../docs/threat-model.md) |
| Production gaps | [Release readiness](../docs/release-readiness.md) |

## Reproducible quickstart (Windows PowerShell)

From the repository root, using Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-azure.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
```

## Concrete demonstration cases

| Message | Simulated principal | Expected route | Expected behavior |
|---|---|---|---|
| `What are your hours?` | none | `faq` | Returns synthetic approved hours |
| `What is my account balance?` | none | `deny` | Requests sign-in |
| `Show user-002 balance` | `user-001` | `crm_read` | Returns **user-001's** synthetic $120, not user-002's $850 |
| `Transfer $500 to user-002 and show my balance` | `user-001` | `escalate` | No transfer is executed |
| `Can I refinance?` | none | `escalate` | Unsupported question is not invented |

Example:

```powershell
.\.venv\Scripts\python.exe -m src.support_agent.cli --principal user-001 --message "Show user-002 balance"
```

## Recorded evidence

The offline Windows run reported **18 passing unit/graph tests**. The evaluation CLI reported **10 of 10 synthetic scenarios passing**. CI has also been observed passing on `main`. These are functional regression results, not proof of adversarial robustness, real authentication, production authorization, latency, ROI or live cloud connectivity.

## Architectural tradeoffs

| Selected approach | Reason | Tradeoff |
|---|---|---|
| Deterministic policy routing before inference | Prevent high-risk requests reaching generative steps | Keyword matching misses paraphrases; production needs stronger policy and intent validation |
| Explicit LangGraph transitions | Inspectable, testable workflow boundaries | More framework overhead than a simple function |
| Synthetic, read-only CRM | Demonstrate account scoping without mutating records | Does not exercise external authorization or failure modes |
| Fixed approved FAQ corpus | Repeatable, inspectable evidence | Limited coverage; no vector search or semantic RAG |
| Escalate on missing evidence/model failure | Avoid unsupported answers | Increases manual workload |
| Optional cloud model | Offline tests remain reproducible without credentials | Live integration remains unverified |

See the [ADRs](../decisions/) and [cost assumptions](../docs/cost-model.md) for deeper analysis.

## Production boundary

Real deployment would require verified OIDC claims, tenant-aware downstream CRM authorization, adversarial testing, observability/redaction, resilience testing, secrets management and operational approval. This repository is an **offline reference prototype**, not a customer-ready service.
