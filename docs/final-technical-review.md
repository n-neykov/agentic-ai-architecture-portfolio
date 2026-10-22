# Portfolio technical review — updated 2026-10-22

**Scope:** Three synthetic Python/Streamlit reference projects, shared Azure Foundry adapter, architecture READMEs, threat model, dashboard, and automated regression tests. Reviewed source files through the connected GitHub repository. This is a targeted code and documentation review, **not** a complete line-by-line attestation of every file, a credential-history scan, a production penetration test, or a local execution of the latest commit.

## Corrections made in this review

- Project 02: Rebuilt the Mermaid decision diagram; removed the reused node identifier and distinguished offline/AI extraction, provenance verification, validation, review, and staging.
- Project 03: Rebuilt the Mermaid routing/authorization diagram; documented pre-inference identity/tenant checks and post-inference tool/role/approval gates.
- Project 02: Added explicit review for malformed bank-account labels that would otherwise evade the narrow extractor. Simulated approval now accepts **only** the known `sensitive_bank_details_require_review` issue; unrecognized or malformed issues cannot be waived.
- Added offline and mocked-Azure regression tests for malformed sensitive banking fields.
- Updated outdated Project 02 Azure agreement test evidence, Project 03 inference claims, portfolio status, test plan, and release-readiness wording.

## Confirmed architectural boundaries

| Area | Implemented | Not claimed |
|---|---|---|
| P1 | Known-pattern pre-inference veto, bounded JSON tool selection, synthetic scoped read-only data, FAQ evidence | Verified authentication, complete intent safety, production CRM |
| P2 | Offline or Azure-proposed extraction, exact label/value provenance checks, deterministic business validation, in-memory staging/review | OCR, model-quality benchmark, production document handling, authenticated reviewers |
| P3 | Offline or Azure tool nomination, simulated tenant/role policy, allowlisted tools, approval simulation, read-only synthetic records | Verified IAM, live enterprise APIs, durable audit, actual payment writes |
| Azure | Local key-based Foundry inference, timeout/retry settings, `store=False` request option | Provider zero-retention guarantee, managed identity, deployed service |

## Residual technical risks and production-boundary assessment

1. **P1 policy coverage:** Keyword/regex screening can miss paraphrases. The account-scope check recognizes only explicit synthetic user IDs. Never characterize it as complete authorization or comprehensive prompt-injection defense.
2. **P1 multi-intent:** The model nominates a bounded tool for each preplanned intent, sometimes using a canonical prompt. This is **bounded model-assisted routing**, not autonomous multi-agent planning or provider-native function calling.
3. **P2 extraction:** The AI-assisted mode requires fields to match regex-extracted labeled source lines. It does not demonstrate generalized extraction from arbitrary unstructured PDFs. Provenance is source-line evidence, not OCR/page citations.
4. **P2 review:** A named reviewer is a simulated string. In-memory state and approvals are not durable or authenticated.
5. **P3 identity:** `verified=True` is a synthetic flag. Tenant and role enforcement is implemented in Python against synthetic data, not at an external data store or API gateway.
6. **P3 model role:** GPT selects one registered tool; the model cannot execute the tool or grant permission. A payment-write example is approval-gated but never connected to a write API.
7. **Tests:** Automated tests exercise local fixtures and mocked model decisions. observed in local live-Azure demonstrations live Azure acceptance is separate. A subsequent captured terminal screenshot dated 2026-10-22 shows **97/97 tests passing** after the malformed-bank fixture and regex corrections. GitHub Actions and full UI rendering were not independently verified.
8. **Security:** `.gitignore` excludes `.env` and credential-like files. This review did not independently scan all Git history or certify absence of secrets in prior commits.
9. **Observability:** Local audit arrays and downloadable JSON are demonstration artifacts, not immutable centralized audit trails or end-to-end distributed traces.
10. **Performance:** No measured accuracy, cost, SLA, latency percentile, or production availability should be presented as achieved.

## Final verification

```powershell
git switch main
git pull origin main
.\.venv\Scripts\python.exe -m compileall -q src tests dashboard.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

Verify the Project 02 malformed bank-account fixture cannot stage or be approved, and confirm the three project architecture tabs render at normal browser zoom. Check GitHub Actions for the exact final SHA. Screenshots should identify the prototype as synthetic and avoid showing `.env` or secrets.

**Verification update (2026-10-22):** The recorded evidence includes screenshots showing **97/97 local automated tests passing**, **10/10 offline baseline scenarios passing**, and six live Azure demonstrations across the three projects. Evidence includes Project 01 two-model-call approved multi-intent and zero-call cross-account denial; Project 02 staged invoice and bank-detail review; Project 03 allowed tenant-A finance lookup and pre-inference tenant-B denial. CI and history-wide secret scanning remain unverified.

**Disposition:** Suitable as a synthetic enterprise architecture reference portfolio **subject to CI, full-history credential scanning and architecture visual verification**. Not production ready.
