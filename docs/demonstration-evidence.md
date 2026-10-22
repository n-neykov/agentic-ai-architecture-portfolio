# Demonstration evidence

**Synthetic reference implementations · User-executed acceptance evidence, 2026-10-22**

The screenshots in the evidence set were captured from local Streamlit runs and show real observed outcomes, not generated mockups. They demonstrate selected success, denial and review paths; they do **not** establish production security, performance, or availability.

| Project | Evidence | Observed result |
|---|---|---|
| 01 · Secure Customer Service | Azure multi-intent request from simulated `user-001` | `multi`, `allow`, two model calls, fictional $120 balance and hours FAQ evidence |
| 01 · Secure Customer Service | Cross-account balance request from `user-001` for `user-002` | `deny`, zero model calls, no private account data |
| 02 · Intelligent Document Processing | Valid synthetic invoice in Azure mode | `staged`; vendor, invoice, amount, currency and source-line evidence |
| 02 · Intelligent Document Processing | Synthetic supplier agreement with bank account | `needs_review`; `sensitive_bank_details_require_review`; source-line evidence |
| 03 · Governed Enterprise Agent Platform | Finance reader, tenant A, finance procedure request | `allowed`; model called; synthetic tenant-A finance record |
| 03 · Governed Enterprise Agent Platform | Finance reader, tenant A, requested tenant B | `denied`; `cross_tenant_access`; `model_called=false` |
| Engineering | Local unit test terminal output | `Ran 97 tests ... OK` |
| Engineering | Deterministic baseline CLI evaluation | `passed: 10`, `total: 10` |

## Screenshot publication guidance

Approved screenshot assets have been reviewed in the conversation but **have not yet been uploaded to this GitHub repository**. This page intentionally does not embed nonexistent image links.

Recommended paths for the selected images, after uploading:

```text
docs/assets/
  p01-azure-multi-intent.png
  p01-cross-account-denied.png
  p02-azure-invoice-staged.png
  p02-bank-details-review.png
  p03-tenant-a-finance-allowed.png
  p03-cross-tenant-denied.png
  verification-97-tests.png
  verification-10-baseline-scenarios.png
```

Before publishing, crop extraneous desktop chrome and check screenshots for secrets, real identities, tokens, customer data and accidental personal paths. Include only synthetic fixtures. Avoid representing a local screenshot as GitHub CI evidence.

## Verification still outstanding

- Confirm the exact GitHub Actions workflow run is green for the final commit.
- Scan Git history for credentials; `.gitignore` does not prove historical absence.
- Visually inspect all three architecture tabs and Mermaid diagrams at normal browser zoom.
- Record the exact commit used for local screenshot capture if available; do not infer it from later documentation commits.

[Portfolio overview](../README.md) · [Technical review](final-technical-review.md) · [Acceptance plan](portfolio-test-plan.md)
