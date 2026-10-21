# Evaluation plan

## Reproducible synthetic checks
Run `python -m src.support_agent.cli --evaluate` after installing `requirements-azure.txt`.

Ten scenarios check FAQ routing, unsupported inquiries, anonymous access, identity scoping, high-risk escalation, and basic malicious-instruction handling. The evaluator reports route accuracy and a simple forbidden-string check, **not** a complete privacy or hallucination assessment.

## Release gates (proposed, not achieved)
- All unit and workflow tests passing in CI
- Security threat-model review and negative tenant tests
- Groundedness evaluation with human-labeled answer set
- Measured p50/p95 latency and cost per request
- Credential scanning, structured audit logs and incident playbook
- Validated Entra ID authentication and CRM-side authorization
- Operational owner approval before any live customer deployment

## Known evaluation limitations
Small synthetic corpus, no real production traffic, no model-level adversarial suite, no measured quality/latency/cost, and no live Azure inference results. Do not advertise proposed KPI targets as outcomes.
