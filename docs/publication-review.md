# Publication review — independent reference portfolio

## Evidence classification

- **Implemented and locally tested:** Project 01 offline LangGraph workflow, static FAQ retrieval, synthetic read-only CRM, deterministic routing and CLI.
- **Recorded local results:** 18/18 unit and graph tests passed; 10/10 synthetic routing scenarios passed (Windows, Python 3.11).
- **Configured CI:** GitHub Actions installs dependencies, compiles Python, runs tests, evaluates routing and performs an offline FAQ smoke test.
- **Architecture-only:** Project 02 document intake/review and Project 03 governed enterprise platform.
- **Not validated:** Live cloud model inference, real OIDC authentication, tenant-scoped external CRM, semantic search, security certification, throughput/latency, and business ROI.

## Public-review checklist

| Area | Review outcome |
|---|---|
| Landing page | Case studies, compact workflow, commands, scenario examples and evidence links included |
| Technical traceability | Project 01 links to source, tests, threat model and architecture decisions |
| Claims | Prototype results separated from hypothetical designs and targets |
| Risk disclosure | Identity is simulated; synthetic data only; no production security claim |
| Credential hygiene | `.env.example` and `.gitignore` exist; repository history and all branches require a separate secret scan before visibility change |
| Dependency security | No package vulnerability audit or SBOM recorded |
| Cloud integration | Not tested with live credentials |
| License | MIT license included |

## Interpretation

**Suitable to publish as an independent educational/reference architecture portfolio**, provided no secrets or private material remain in any branch or Git history. It is **not** suitable to deploy to production or represent as a completed enterprise implementation.

The recorded 18-test and 10-scenario runs are functional evidence for a small synthetic suite. They do not measure false negatives for paraphrased high-risk requests, adversarial prompt robustness, authorization with a real identity provider, or reliability under load.

## Reproduction

Run the commands in the root [README](../README.md). Check GitHub Actions for the most recent successful commit before sharing the link. Verify the entire repository history and other branches contain no credentials or private material before changing visibility.
