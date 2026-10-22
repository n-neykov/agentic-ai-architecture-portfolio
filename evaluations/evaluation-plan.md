# Project 01 — Evaluation methodology

## Automated checks

The repository provides an offline Python unit/graph regression suite and a **ten-scenario deterministic LangGraph baseline evaluation**. The baseline checks public FAQ routes, unsupported inquiries, anonymous balance denial, scoped own-account access, cross-account denial, high-risk escalation and basic malicious-instruction strings.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
```

A separate `tests/test_knowledge_base.py` covers the 12 synthetic FAQ topics, evidence IDs, retrieval specificity, and high-risk precedence. The ten-scenario dashboard evaluation is **not** a benchmark of the Azure model.

## Recorded evidence

The user previously confirmed **10/10 baseline scenarios**, and live GPT-4.1 mini multi-intent, session identity, own-account and cross-account demonstrations. The latest reported repository-wide test run discovered 97 tests and had two failures in Project 02 malformed-bank tests. Those fixture/regex escaping errors were corrected afterward, but the final suite result is not yet confirmed. This is not a live-model accuracy evaluation.

## Proposed enterprise release gates — not achieved

- Verified identity, tenant-aware CRM authorization and privacy review.
- Adversarial and paraphrase testing across the full policy/intent surface.
- Human-reviewed groundedness and factual accuracy scoring.
- Measured p50/p95 latency, cloud cost per request and failure rates.
- Redacted distributed traces, credential scanning and incident-response drills.
- Operational owner approval before real customer deployment.

## Interpretation

Passing synthetic tests demonstrates behavior on known fixtures, **not** arbitrary prompt-injection resistance, verified access control, cloud reliability, security certification, or business ROI.
