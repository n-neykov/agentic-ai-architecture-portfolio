# Three-project portfolio — Final acceptance plan

Run from the repository root on branch `main`:

```powershell
git switch main
git pull origin main
.\.venv\Scripts\python.exe -m pip install -r requirements-dashboard.txt
.\.venv\Scripts\python.exe -m compileall -q src tests dashboard.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

## Project 01

Run a public FAQ, multi-intent FAQ + own balance, cross-account denial and high-risk escalation in **AI Agent · Azure Foundry** mode. Verify live call counts, evidence IDs and no private data in denied responses. The ten-scenario baseline evaluation should pass.

## Project 02

| Fixture | Expected |
|---|---|
| Valid invoice | Staged with field/line evidence |
| Valid invoice submitted twice | Same workflow ID, duplicate=true, one staged record |
| Missing invoice amount | Needs review; approval rejected |
| Agreement requiring review | Bank-account issue; named reviewer may approve to in-memory staging |
| Unknown vendor | Needs review; no staging |

Verify tenant-specific workflow IDs and downloadable JSON.

## Project 03

| Principal / tool / tenant | Expected |
|---|---|
| HR reader A / HR lookup / A | Allowed; HR record only |
| HR reader A / finance lookup / A | Denied: role |
| Finance reader A / finance lookup / B | Denied: tenant |
| Unverified caller / finance lookup / A | Denied: verification |
| Finance admin A / vendor payment update / A | Approval required |
| Approver A records approval; finance admin retries same ID | Denied: live write disconnected |

Verify audit events and JSON export. These are simulated identity claims, not real IAM tests.

## Sign-off

The integrated three-project PR has been merged; rerun the regression suite after presentation changes and verify dashboard smoke tests. Capture screenshots later from the same final commit. Never enter real customer/supplier records or commit credentials.

## Optional live Azure Foundry acceptance tests (Projects 02 and 03)

Requires the same private local `.env` as Project 01. No keys are stored in GitHub.
Select the Azure execution mode inside each project's dashboard tab.

**Project 02:** Process the valid invoice in AI-assisted mode. Expected: `mode=azure`, staged, verified source-line evidence. Process the agreement with bank details; expected: needs_review with `sensitive_bank_details_require_review` and extracted bank-account source evidence, **not** `model_inference_failed`. The user subsequently verified Azure agreement extraction with source-line evidence and the expected `sensitive_bank_details_require_review` decision. Repeat only if reconfirming the final code revision. Submit an unsupported or unlabeled synthetic text; expected: needs_review, not fabricated fields. Offline and Azure document fingerprints are independent. The Azure model is a structured extraction proposer, not an OCR engine.

**Project 03:** Choose Finance reader tenant A, requested tenant A, and ask "Find the finance reporting procedure." Expected: model selects `finance_report_lookup`, gateway allows tenant-A record only. Repeat with requested tenant B; expected: cross_tenant_access and model_called=false. Choose HR reader tenant A and ask for finance reporting; expected: role_not_permitted even if GPT selects the finance tool. Choose Finance admin and ask to update vendor payment details; expected: approval_required and no actual write.

Model failures and malformed output must fail closed. Azure calls may incur charges. Automated tests use fake models and do not attest to live inference.
