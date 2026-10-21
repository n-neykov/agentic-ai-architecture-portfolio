# Project 01 — Evaluation methodology

## Automated checks

The repository provides an offline Python unit/graph regression suite and a **ten-scenario deterministic LangGraph baseline evaluation**. The baseline checks public FAQ routes, unsupported inquiries, anonymous balance denial, scoped own-account access, cross-account denial, high-risk escalation and basic malicious-instruction strings.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
```

A separate `tests/test_knowledge_base.py` covers the 12 synthetic FAQ topics, evidence IDs, retrieval specificity, and high-risk precedence. The ten-scenario dashboard evaluation is **not** a benchmark of the Azure model.

## Recorded evidence

The user confirmed 53 passing tests and 10/10 baseline scenarios **before the knowledge-base expansion**. They also confirmed live GPT-4.1 mini scenarios including multi-intent, session identity, own-account reads and cross-account denials. The expanded suite requires rerunning; no updated pass count is claimed.

## Proposed enterprise release gates — not achieved

- Verified identity, tenant-aware CRM authorization and privacy review.
- Adversarial and paraphrase testing across the full policy/intent surface.
- Human-reviewed groundedness and factual accuracy scoring.
- Measured p50/p95 latency, cloud cost per request and failure rates.
- Redacted distributed traces, credential scanning and incident-response drills.
- Operational owner approval before real customer deployment.

## Interpretation

Passing synthetic tests demonstrates behavior on known fixtures, **not** arbitrary prompt-injection resistance, verified access control, cloud reliability, security certification, or business ROI.
