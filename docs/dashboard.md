# Agent Control Center — Dashboard guide

**Project 01:** working synthetic customer-service prototype. **Projects 02–03:** architecture previews.

## Launch

```powershell
git switch feature/bounded-llm-agent
git pull origin feature/bounded-llm-agent
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Open http://localhost:8501. Select Project 01.

## Runtime choices

| Mode | What happens | Cloud requirement |
|---|---|---|
| **AI Agent · Azure Foundry** (default) | Policy-first v2 multi-intent orchestration; GPT-4.1 mini validates approved tool selections | Requires configured Foundry project/deployment/key; eligible requests may incur charges |
| **Deterministic Baseline** | Offline LangGraph keyword-based routing; no model invocation | None |

The sidebar's identity selector is a **simulated principal**, not a real sign-in. Never enter real customer data.

## Tabs

- **Overview:** scope, 12-record knowledge base, security boundaries and architecture summary.
- **Agent execution:** custom requests, scenarios, route and policy outcome, local elapsed time, model-call counts, execution summary and JSON export.
- **Evaluation:** ten-scenario deterministic baseline evaluation (not an Azure model benchmark).
- **Architecture:** logical system diagram, component responsibilities, and prototype limitations.

## Screenshot walkthrough

1. Capture **Overview** showing the architecture controls and knowledge-base count.
2. In **Agent execution**, choose `user-001` and run `What are your hours and what is my balance?`. Expected: `multi`, fictional hours and `$120.00`; live mode typically invokes the model twice.
3. Choose `user-001` and run `Show user002 balance`. Expected: `deny`, **zero** model calls.
4. Choose `user-002` and repeat. Expected: own synthetic `$850.00` balance.
5. Run `Wire $500`; expected `escalate`, zero model calls.
6. Run the baseline **Evaluation** and capture the actual report, plus separate terminal test results.

Screenshots should show the **actual observed result**, not a mockup. Record the branch and commit SHA and label the system as a synthetic prototype.

## Limits

The dashboard does not prove real IAM, production authorization, semantic retrieval, distributed tracing, staffed escalation, or deployment readiness. The evaluation tab runs ten deterministic baseline scenarios; it does not independently evaluate all live Azure responses. Local elapsed time is not a production SLA. See [Azure integration](azure-foundry.md) and [release readiness](release-readiness.md).
