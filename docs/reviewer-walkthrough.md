# Reviewer walkthrough and evidence capture

This is a **synthetic architecture portfolio**. Use real application screenshots from the same commit as the test results. Do not generate mock execution screenshots or expose API keys.

## Recommended evidence set

| Artifact | Show | Architectural point |
|---|---|---|
| 01 — Multi-intent execution | Azure mode, simulated `user-001`, FAQ + own synthetic balance, execution metadata | Bounded model nominations with server-owned read-only data |
| 02 — Pre-inference denial | `user-001` requests `user-002` balance; denied with zero model calls | Known-pattern policy veto before inference |
| 03 — Invoice intake | Azure mode, staged invoice, extracted fields, source-line evidence | Extraction is checked against labeled source data |
| 04 — Agreement review | Azure mode, `needs_review`, bank-account issue, source-line evidence | Deterministic review gate overrides AI proposal |
| 05 — Authorized tool | Finance reader tenant A, finance report lookup, allowed with tenant-A record | Model tool nomination is not itself authorization |
| 06 — Cross-tenant denial | Finance reader tenant A, requested tenant B, `cross_tenant_access`, `model_called=false` | Tenant gate runs before optional inference |
| 07 — Tests and evaluation | Actual terminal results and/or GitHub Actions run from the same commit | Reproducible synthetic regression evidence |
| 08 — Decision diagrams | Project-specific Mermaid flows in each README | Clear control ownership and failure branches |

**Capture guidance:** Prefer full-width desktop screenshots with labels and outcome visible. Crop personal paths, tokens, and unrelated windows. Preserve enough UI context to identify the selected project, runtime mode, and result. Add a commit SHA in captions, not inside the application. Screenshots must match real observed behavior.

## Suggested five-minute narration

1. **Problem and scope (30 seconds):** Three fictional enterprise scenarios, one design principle: the model proposes, deterministic code authorizes.
2. **Project 01 (60 seconds):** Show successful bounded multi-intent execution, then a denied cross-account request before model invocation. Clarify simulated identity.
3. **Project 02 (60 seconds):** Show a staged invoice, then a bank-detail agreement held for review. Explain labeled source-line evidence and why this is not OCR.
4. **Project 03 (60 seconds):** Show authorized tenant-A lookup, then cross-tenant denial with no model call. Clarify static tools and simulated roles.
5. **Engineering evidence and tradeoffs (90 seconds):** Show the actual passing test run, offline baseline evaluation, branching diagrams, and top production gaps.

## Release evidence checklist

- [ ] Record final commit SHA and link to GitHub Actions run (if available).
- [ ] Verify `compileall` succeeds on that SHA.
- [ ] Verify all 97 discovered tests pass on that SHA (do not claim a pass without evidence).
- [ ] Reconfirm ten deterministic baseline scenarios on that SHA.
- [ ] Check all three Streamlit architecture tabs at normal browser zoom.
- [ ] Capture the six behavior screenshots above from the same revision.
- [ ] Confirm no secrets, real customer data or misleading production claims appear.
- [ ] If updating the README's numeric results, include the exact run date and commit.

## Architecture discussion prompts

- Why does a pre-inference policy gate still need real downstream authorization in production?
- What happens when GPT returns malformed JSON, an unsupported tool, or an ungrounded field?
- What is the tradeoff between exact labeled-line extraction and general document understanding?
- How would you replace the simulated principal with Entra ID and enforce tenant isolation at the data plane?
- What would you instrument to measure p95 latency, token cost, groundedness, denial rates and review volume?
- How would you evolve the in-memory approval and staging path into a durable, auditable workflow?

The projects intentionally **do not** establish production identity assurance, enterprise API integrations, security certification, or measured ROI.
