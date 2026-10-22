# Project 01 — Release and evidence register

**Classification:** functional synthetic portfolio prototype. **Not production-ready.**

| Capability | Status | Evidence / boundary |
|---|---|---|
| Policy-first LangGraph baseline | Implemented | Offline workflow and baseline evaluation |
| Bounded v2 multi-intent agent | Implemented | Offline tests and locally recorded Azure dashboard executions |
| Azure Foundry GPT-4.1 mini Responses API | **Validated in local Azure demonstrations** | Working local project endpoint/deployment; no performance certification |
| Synthetic read-only account adapter | Implemented | Session-scoped fixture balances; demo identity is unverified |
| Cross-account and high-risk screening | Implemented for known patterns | Recorded zero-model-call denials; not comprehensive security assurance |
| Approved FAQ knowledge base | **12 records implemented** | 12 synthetic FAQ records; local 97-test suite passed 2026-10-22 |
| Baseline evaluation | **10 scenarios** | 2026-10-22 screenshot shows passed=10, total=10; deterministic baseline only |
| Unit and workflow tests | **97/97 passing in local acceptance run** | Terminal screenshot dated 2026-10-22 shows Ran 97 tests / OK; CI status independently unverified |
| Dashboard and architecture visualization | Implemented | Two Project 01 modes; final visual smoke check not independently verified |
| CI | Configured | Workflow defined for pushes/PRs; inspect the latest GitHub Actions run before claiming success |
| Verified OIDC/Entra identity | Not implemented | Production blocker |
| Real CRM/tenant-level authorization | Not implemented | Production blocker |
| Semantic RAG / Azure AI Search | Not implemented | Potential future enhancement |
| Human escalation queue | Not implemented | Escalation is an outcome string |
| Redacted distributed traces | Not implemented | Execution summary is not an audit system |
| Measured cloud cost, p95 latency, throughput | Not measured | No production KPI claims |
| Comprehensive red-team assessment | Not completed | Production blocker |

## Release checklist for portfolio handoff

- [x] Run complete test suite after regression corrections (captured terminal screenshot: 97/97, 2026-10-22). Compilation separately not evidenced.
- [x] Confirm 10/10 baseline evaluation after changes (captured terminal screenshot, 2026-10-22).
- [ ] Verify representative new FAQ topics in live Foundry mode.
- [x] Capture execution, denial, review and evaluation screenshots for all three projects. Architecture-tab captures remain optional pending visual inspection.
- [ ] Confirm no secrets or real customer information in commits or screenshots.
- [ ] Record final commit SHA and CI status.
- [x] Review README and architecture labels against observed behavior in the supplied execution screenshots. Architecture-tab rendering still requires separate visual confirmation.

**Never describe this as a production banking application or a certified security control.**
