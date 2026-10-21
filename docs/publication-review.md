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
| Credential hygiene | `.env.example` and `.gitignore` exist; Six reachable commits (initial 34-file import plus five updates) reviewed with credential-pattern checks; no recognizable keys found. This is not a full entropy/secret-scanner audit |
| Dependency security | No package vulnerability audit or SBOM recorded; dependencies are version-ranged |
| Cloud integration | Not tested with live credentials |
| License | MIT license included |

## Interpretation

**Conditionally suitable to publish as an independent educational/reference architecture portfolio.** Recognizable credential-pattern checks across six commits found no matches, but a dedicated secrets scan, manual privacy review, and latest CI confirmation remain outstanding. It is **not** suitable to deploy to production or represent as a completed enterprise implementation.

The recorded 18-test and 10-scenario runs are functional evidence for a small synthetic suite. They do not measure false negatives for paraphrased high-risk requests, adversarial prompt robustness, authorization with a real identity provider, or reliability under load.

## Reproduction

Run the commands in the root [README](../README.md). **Latest CI is not verified:** the connector's combined-status response was empty, and its workflow-run endpoint only lists pull-request runs (none returned). Inspect the Actions page directly and verify the latest commit before publication. The two branches are `main` and `develop`; `develop` points to the initial release commit, with `main` five commits ahead. Review any non-pattern private material manually; pattern checks are not a substitute for a dedicated scanner such as Gitleaks.
