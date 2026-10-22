# Azure AI Foundry integration — Project 01

**Implementation:** [`src/support_agent/azure_model.py`](../src/support_agent/azure_model.py) · [`agent_v2.py`](../src/support_agent/agent_v2.py) · [`dashboard.py`](../dashboard.py)

## Verified behavior and scope

Live tests successfully invoked the **GPT-4.1 mini** deployment through a Microsoft/Azure AI Foundry **project Responses API** endpoint. Live dashboard testing covered approved FAQ answers, own-account synthetic reads, multi-intent responses, simulated session identity, pre-inference cross-account denials, and high-risk escalation. These are local live-Azure demonstrations, not provider-side certification or production benchmarks.

## Local configuration

Install `requirements-dashboard.txt`. Copy `.env.example` to `.env` and set:

| Variable | Purpose |
|---|---|
| `AZURE_OPENAI_ENDPOINT` | HTTPS Foundry project endpoint, `.../api/projects/PROJECT`, or its `/openai/v1/responses` route |
| `AZURE_OPENAI_API_KEY` | Local private API key; **never commit or screenshot** |
| `AZURE_OPENAI_DEPLOYMENT` | Deployment name; tested with `gpt-4.1-mini` |
| `AZURE_OPENAI_API_VERSION` | Used for legacy `.openai.azure.com` AzureChatOpenAI resource endpoints, not Foundry Responses |

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m src.support_agent.cli --agent --azure --message "What are your hours?"
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

The CLI command exercises the earlier bounded-agent path. Select **AI Agent · Azure Foundry** in Streamlit for the newer v2 multi-intent path.

## Request path

1. Deterministic policy screens the entire request and synthetic principal.
2. For approved FAQ/account intents, the application requests a strict JSON tool choice from GPT-4.1 mini.
3. The model cannot provide arbitrary account identifiers, write operations, or tool arguments.
4. The server validates the tool choice against the intended operation and executes read-only adapters.
5. The dashboard records attempted/completed model-call counts and a summarized execution outcome. No prompt text is intentionally logged to an external audit service by the application.

The Foundry SDK call uses `responses.create(model=deployment, instructions=..., input=..., max_output_tokens=160, store=False)` and a configured timeout/retry limit. This is **model-driven bounded tool selection**, not provider-native autonomous function calling or an open-ended planner.

## Security and operational limits

- `store=False` is an API request parameter, **not** a guarantee that no data is processed or retained by the provider under applicable service policies.
- API key authentication is used in the local prototype. Production should prefer approved identity/secrets infrastructure.
- No production CRM, verified customer identity, Azure AI Search, ticket queue, distributed trace backend, or deployed web service is connected.
- Cloud cost, token usage, latency distributions, rate limits and adversarial robustness have not been measured.
- Live calls can incur charges; use fictional prompts only.
