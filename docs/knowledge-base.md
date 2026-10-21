# Project 01 — Approved synthetic knowledge catalog

The working prototype has **12 fictional FAQ records** in [`src/support_agent/integrations.py`](../src/support_agent/integrations.py). Each record has a stable `doc_id`, title, category and approved answer. Retrieval uses deterministic regex/keyword matching; this is **not** Azure AI Search, embeddings or semantic RAG.

| Evidence ID | Topic | Category |
|---|---|---|
| `faq-hours` | Support hours | Support |
| `faq-fees` | Account fees | Accounts |
| `faq-cards` | Card replacement | Cards |
| `faq-lost-card` | Lost or stolen cards | Cards |
| `faq-statements` | Account statements | Accounts |
| `faq-deposits` | Direct deposit | Payments |
| `faq-payment-times` | Payment processing times | Payments |
| `faq-opening` | Opening an account | Accounts |
| `faq-contact` | Contacting support | Support |
| `faq-online-access` | Online account access | Digital |
| `faq-atm` | ATM withdrawals | Cards |
| `faq-disputes` | Transaction disputes | Payments |

## Retrieval and authority

- Matching evidence is returned only from this approved, local fixture corpus.
- A question may match multiple documents. Responses concatenate approved fictional answers and retain evidence IDs.
- No answer contains real provider phone numbers, policies, fee amounts or actual financial guidance.
- High-risk actions such as transfers, password resets and account changes remain blocked or escalated before model selection.
- A statement about how to contact support is **not** an implemented ticket submission or live human handoff.

## Testing

[`tests/test_knowledge_base.py`](../tests/test_knowledge_base.py) checks all 12 topics, uniqueness, evidence IDs, collision avoidance for account opening vs business hours and lost card vs replacement, unsupported inquiries and high-risk precedence.

```powershell
.\.venv\Scripts\python.exe -m unittest tests.test_knowledge_base -v
```

**Limitations:** keyword retrieval can miss paraphrases or select unintended matches. Production use would require curated knowledge governance, semantic evaluation, access controls, content freshness and approved ingestion.
