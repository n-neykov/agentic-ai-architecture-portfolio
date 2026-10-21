# Agent Control Center

Streamlit UI for synthetic offline demonstrations. Run from repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

The deterministic mode executes the existing LangGraph graph. The simulated model-selected mode uses a local rule-based fake model, **not a real LLM**. Both modes use fictional balances and simulated identity, not production authentication.

Demo: public FAQ, cross-account balance request using demo principal user-001, wire transfer escalation, unknown-question escalation, and the 10-scenario synthetic evaluation.

The trace panel summarizes actual function outputs; it is not a full node-by-node LangGraph event stream. Capture screenshots of each demo and the evaluation, and record the commit SHA. Never upload keys, real customer data, or Azure billing details.
