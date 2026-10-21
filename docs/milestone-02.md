# Milestone 02 — Azure AI + LangGraph

## Setup
Requires Python 3.11+ and an isolated environment.

```bash
python -m venv .venv
# activate .venv for your shell
python -m pip install -r requirements-azure.txt
python -m unittest discover -s tests -v
python -m src.support_agent.cli --evaluate
python -m src.support_agent.cli --message "What are your hours?"
python -m src.support_agent.cli --principal user-001 --message "Show user-002 balance"
```

## Optional Azure integration
Create a deployed Azure OpenAI chat model. Copy `.env.example` to `.env`, set endpoint, key, deployment and API version, then run:

```bash
python -m src.support_agent.cli --azure --message "What are your hours?"
```

The Azure call is billable. No Azure resource is provisioned by this project. Never commit `.env`.

## Scope and limitations
The CLI's `--principal` simulates a trusted upstream identity, and is **not authentication**. The FAQ corpus is static keyword retrieval, not semantic RAG. Model grounding is prompt-based and not a proof of correctness. See `docs/release-readiness.md`.
