# Evolution of Project 01 — Bounded model selection and v2 orchestration

**Status:** implemented and user-verified with Azure AI Foundry GPT-4.1 mini. This is an engineering evolution within Project 01, not Project 02 of the portfolio.

## Development progression

1. **Deterministic LangGraph baseline:** policy-first routing, public FAQ lookup, simulated account reads and safe fallback.
2. **Bounded model selection:** JSON allowlist `faq_lookup`, `account_balance`, `escalate`; server-side veto and scoped tool arguments.
3. **V2 agent:** deterministic multi-intent planning, `session_info`, composite FAQ/balance responses, policy/tool execution steps, optional live Foundry tool-selection validation.
4. **Knowledge expansion:** 12 categorized synthetic FAQ records with stable evidence IDs and offline regression tests.

## Why not an unrestricted agent?

The architecture deliberately limits authority. The model may propose an approved operation but cannot select an arbitrary account record, perform writes, or override policy. This is not autonomous planning or provider-native tool execution. The policy vocabulary remains narrow, and unknown requests may escalate.

## Azure implementation

[`azure_model.py`](../src/support_agent/azure_model.py) supports Foundry project Responses API endpoints using the OpenAI SDK and legacy Azure OpenAI resource endpoints via LangChain. The user verified GPT-4.1 mini live calls in the local dashboard. See [Azure setup](azure-foundry.md).

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Before the FAQ expansion, 53 automated tests and all ten baseline evaluation scenarios passed in the user's environment. Additional FAQ tests now require a fresh run.

## Production gaps

Verified identity and downstream authorization, robust natural-language policy handling, rate limits, observability/redaction, cloud cost tracking, staffed escalation, adversarial evaluation and managed secrets remain unimplemented.
