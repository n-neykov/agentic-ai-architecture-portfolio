# Three-project portfolio — Final acceptance plan

Run from the repository root on branch `feature/bounded-llm-agent`:

```powershell
git pull origin feature/bounded-llm-agent
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

Do not merge until the final regression suite and dashboard smoke tests pass. Capture screenshots later from the same final commit. Never enter real customer/supplier records or commit credentials.
