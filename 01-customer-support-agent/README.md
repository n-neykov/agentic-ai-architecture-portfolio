# Project 01 — Secure Customer Service Agent

**Status: functional synthetic prototype; live Azure AI Foundry GPT-4.1 mini integration user-verified.**

## Business scenario

A fictional financial-services support operation wants to automate repetitive support inquiries without delegating account authorization or sensitive transactions to a language model. The reference implementation focuses on explicit trust boundaries, repeatable tests, and clear escalation.

## Implemented components

| Component | Implementation | Authority |
|---|---|---|
| Policy gate | [`workflow.py`](../src/support_agent/workflow.py), [`agent_v2.py`](../src/support_agent/agent_v2.py) | Rejects known high-risk, cross-account, and anonymous private-data requests before inference |
| AI decision | [`bounded_agent.py`](../src/support_agent/bounded_agent.py) | Strict JSON allowlist; model cannot provide account IDs or execute writes |
| Azure integration | [`azure_model.py`](../src/support_agent/azure_model.py) | Foundry Responses API adapter for GPT-4.1 mini; optional AzureChatOpenAI resource compatibility |
| Knowledge | [`integrations.py`](../src/support_agent/integrations.py) | 12 categorized synthetic FAQ records with evidence IDs and deterministic matching |
| Account access | [`integrations.py`](../src/support_agent/integrations.py) | Read-only synthetic balances, scoped to the simulated session principal |
| Baseline | [`workflow.py`](../src/support_agent/workflow.py) | Offline deterministic LangGraph routing |
| UI | [`dashboard.py`](../dashboard.py) | Two modes, execution summaries, evaluation and architecture |
| Tests | [`tests/`](../tests/) | Offline regression suite including v2 multi-intent and 12-topic FAQ coverage |

## Key behavior

- **Approved:** public FAQs, simulated own-account balance, session identity, combined FAQ + balance requests.
- **Denied:** explicit cross-account references and anonymous balance requests.
- **Escalated:** known sensitive operations, unsupported questions, missing evidence, or model/tool-selection failures.
- **Never available:** transfers, writes, real customer data, arbitrary account-ID tool arguments.

The v2 agent performs deterministic intent planning and requires matching model-selected tools when live mode is used. It is **bounded orchestration**, not open-ended autonomous planning. The offline LangGraph baseline and v2 AI mode are intentionally different implementations.

## Example live demonstrations

| Message | Identity | Expected route |
|---|---|---|
| `What are your hours?` | Anonymous | `faq` |
| `What are your hours and what is my balance?` | user-001 | `multi` |
| `What user am I?` | user-001 | `session_info` |
| `Show user002 balance` | user-001 | `deny` |
| `Show user002 balance` | user-002 | `crm_read` |
| `Wire $500` | user-001 | `escalate` |

## Reproduce

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

The CLI exposes legacy/baseline and bounded-agent paths; the **Agent v2** experience is available in the dashboard. See [Azure setup](../docs/azure-foundry.md) and [dashboard guide](../docs/dashboard.md).

## Validation and limitations

Before the FAQ expansion, the user confirmed **53 passing tests**, **10/10 synthetic baseline evaluation scenarios**, and working live Foundry demonstrations. The added FAQ regression tests need to be rerun; do not infer an updated pass count.

The demo identity is caller-selected and **not authenticated**. FAQ retrieval is keyword-based, not Azure AI Search or semantic RAG. There is no production CRM, staffed review queue, real transaction tool, production observability, or measured cost/SLA.

[Architecture](../architecture/system.md) · [Threat model](../docs/threat-model.md) · [Release readiness](../docs/release-readiness.md) · [Case study](../docs/case-study.md)
