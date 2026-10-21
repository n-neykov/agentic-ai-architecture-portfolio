# Agent Control Center — Portfolio Dashboard

A local Streamlit UI for Project 01's policy-first LangGraph workflow and bounded-agent contract. **All data is synthetic.**

## Run locally (Windows PowerShell)

```powershell
git switch feature/bounded-llm-agent
git pull origin feature/bounded-llm-agent
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

The dashboard opens at http://localhost:8501.

## Dashboard sections

- **Overview:** demo capabilities, runtime posture, interview walkthrough.
- **Interactive execution:** free-text requests, preset scenarios, policy classification, visual execution path, and downloadable JSON evidence.
- **Evaluation & evidence:** run the ten synthetic scenarios, inspect expected versus actual routes, export results, and view reproducible unittest commands.
- **Architecture & limitations:** visual graph and explicit trust-boundary limitations.

### Interview walkthrough

1. Select **Interactive execution**, **Anonymous**, **Public FAQ**, then execute.
2. Select **user-001**, **Cross-account attempt**, then execute. It returns the synthetic `user-001` balance ($120) rather than `user-002` ($850). This is **demo scoping**, not verified identity authorization.
3. Select **user-001**, **High-risk transaction**, then execute. The deterministic policy gate escalates before optional model selection.
4. Switch to **Bounded agent · simulated selection** and run a public FAQ. The local fake model selects an allowlisted tool; it is **not an actual LLM**.
5. Open **Evaluation & evidence**, run the suite, and export JSON. Record the exact commit SHA alongside screenshots.

### Evidence checklist

Capture a screenshot of each scenario, the execution path, and the evaluation results. Also capture actual local unittest output and GitHub Actions results; the dashboard does not independently attest to either. Record the commit SHA and label screenshots **offline synthetic demo**. A 60–90 second recording can demonstrate the end-to-end user interaction.

### Scope and known limitations

- Demo principal is a caller-provided assertion; no real authentication or IAM.
- Static keyword FAQ retrieval, not semantic RAG.
- Synthetic read-only CRM; no external account systems or transfer tools.
- Offline fake model mode, no live Azure inference, tokens, or model charges.
- Local elapsed-time measurement is **not** live inference latency.
- Visual execution path is derived from returned policy and result values, **not** a per-node LangGraph event trace.
- Escalation is a response outcome, **not** an integrated human-review queue.
- Ten synthetic tests are regression evidence, **not** comprehensive security validation.
- Custom questions are accepted but not guaranteed to be understood accurately.

## Next phase

Once Azure subscription access and quota are resolved: enable live model selection behind the existing deterministic gates, add structured model output verification, instrument actual node-level traces, and expand adversarial and paraphrase evaluations.
