# Project 01 — Release and evidence register

**Classification:** functional synthetic portfolio prototype. **Not production-ready.**

| Capability | Status | Evidence / boundary |
|---|---|---|
| Policy-first LangGraph baseline | Implemented | Offline workflow and baseline evaluation |
| Bounded v2 multi-intent agent | Implemented | Offline tests and user-observed live dashboard runs |
| Azure Foundry GPT-4.1 mini Responses API | **Live validated by user** | Working local project endpoint/deployment; no performance certification |
| Synthetic read-only account adapter | Implemented | Session-scoped fixture balances; demo identity is unverified |
| Cross-account and high-risk screening | Implemented for known patterns | User-tested zero-model-call denials; not comprehensive security assurance |
| Approved FAQ knowledge base | **12 records implemented** | New topic tests committed; updated suite still needs verification |
| Baseline evaluation | **10 scenarios** | User confirmed 10/10 before FAQ expansion; deterministic baseline only |
| Unit and workflow tests | **53 passed before FAQ expansion** | New test cases need rerun; do not claim a new count yet |
| Dashboard and architecture visualization | Implemented | Two modes; screenshots still to be captured from final version |
| CI | Configured | Workflow runs compile, tests and baseline evaluation; new branch run not independently confirmed |
| Verified OIDC/Entra identity | Not implemented | Production blocker |
| Real CRM/tenant-level authorization | Not implemented | Production blocker |
| Semantic RAG / Azure AI Search | Not implemented | Potential future enhancement |
| Human escalation queue | Not implemented | Escalation is an outcome string |
| Redacted distributed traces | Not implemented | Execution summary is not an audit system |
| Measured cloud cost, p95 latency, throughput | Not measured | No production KPI claims |
| Comprehensive red-team assessment | Not completed | Production blocker |

## Release checklist for portfolio handoff

- [ ] Run updated Python compilation and complete test suite on the final commit.
- [ ] Confirm 10/10 baseline evaluation after changes.
- [ ] Verify representative new FAQ topics in live Foundry mode.
- [ ] Capture screenshots: overview, multi-intent, cross-account denial, evaluation, architecture.
- [ ] Confirm no secrets or real customer information in commits or screenshots.
- [ ] Record final commit SHA and CI status.
- [ ] Review README and architecture labels against actual execution behavior.

**Never describe this as a production banking application or a certified security control.**
