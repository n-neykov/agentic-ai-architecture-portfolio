# Release readiness and evidence register

| Capability | State | Evidence / limitation |
|---|---|---|
| Synthetic CRM read and identity scoping | Implemented | Unit tests; identity supplied by demo, not independently verified |
| Policy-first LangGraph routing | Implemented, environment-dependent | Requires LangGraph installation and passing graph tests |
| Approved-document keyword retrieval | Implemented | Static synthetic corpus; not Azure AI Search or semantic RAG |
| Azure OpenAI inference adapter | Implemented, not live-validated | Requires user-managed deployment and credentials |
| Adversarial routing suite | Implemented | Small synthetic scenarios, not comprehensive security assurance |
| CI tests | Configured | GitHub Actions Python workflow passed on main (unit tests, evaluation, offline smoke test) |
| OIDC identity provider validation | Not implemented | Production release blocker |
| External CRM and tenant authorization | Not implemented | Production release blocker |
| Azure AI Search | Not implemented | Future enhancement |
| Distributed tracing and redaction | Not implemented | Future enhancement |
| Load testing, cost and latency benchmarks | Not measured | Do not claim performance KPIs |

**Release classification:** independent demonstration / reference prototype. Not suitable for real customer data or production traffic.
