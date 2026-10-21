"""Bounded LLM-driven tool selection. Demo identity is NOT verified authentication.

The model selects from a small allowlist; server-side policy and adapters own authority.
No transaction tools exist. This module is a reference implementation, not production IAM.
"""
import json
from .core import TrustedContext
from .integrations import retrieve_approved, scoped_balance
from .workflow import classify

TOOLS = ("faq_lookup", "account_balance", "escalate")
ESCALATION = "A human specialist must review this request."

def choose_tool(model, message: str) -> str:
    """Request a structured tool decision; reject all unrecognized output."""
    from langchain_core.messages import SystemMessage, HumanMessage
    result = model.invoke([
        SystemMessage(content=(
            "Choose exactly one tool for the customer request: faq_lookup, account_balance, escalate. "
            "Return ONLY JSON of the form {\"tool\":\"faq_lookup\"}. "
            "Use account_balance for balance inquiries, faq_lookup for public support questions, "
            "and escalate for uncertain or sensitive requests. "
            "Never provide account IDs, arguments, credentials or executable instructions."
        )),
        HumanMessage(content=message),
    ])
    raw = result.content
    if not isinstance(raw, str) or len(raw) > 300:
        raise ValueError("Invalid tool decision")
    decision = json.loads(raw)
    if not isinstance(decision, dict) or set(decision) != {"tool"} or decision["tool"] not in TOOLS:
        raise ValueError("Tool decision not allowlisted")
    return decision["tool"]

def run_agent(message: str, context: TrustedContext, model) -> dict:
    """Model chooses a tool; deterministic policy always retains veto power."""
    if not message.strip():
        raise ValueError("Message must not be empty")
    if model is None:
        raise ValueError("Agent mode requires a model")
    # Policy is checked before model invocation. No LLM decision can authorize a write.
    policy = classify({"message": message, "context": context})["route"]
    if policy == "escalate":
        return {"route": "escalate", "selected_tool": None, "response": ESCALATION}
    if policy == "deny":
        return {"route": "deny", "selected_tool": None, "response": "Please sign in to view account information."}
    try:
        selected = choose_tool(model, message)
    except (Exception):
        return {"route": "escalate", "selected_tool": None, "response": ESCALATION}
    if selected == "escalate":
        return {"route": "escalate", "selected_tool": selected, "response": ESCALATION}
    # A model cannot redirect a balance request to a public tool or invoke private
    # data retrieval for an unrelated request. All private reads are scoped server-side.
    if selected == "account_balance":
        if policy != "crm" or not context.authenticated or not context.principal_id:
            return {"route": "deny", "selected_tool": selected, "response": "Account access is not authorized for this request."}
        balance = scoped_balance(principal_id=context.principal_id, authenticated=context.authenticated)
        if balance is None:
            return {"route": "escalate", "selected_tool": selected, "response": ESCALATION}
        return {"route": "crm_read", "selected_tool": selected, "response": f"Your balance is {balance}."}
    if selected == "faq_lookup":
        if policy != "knowledge":
            return {"route": "escalate", "selected_tool": selected, "response": ESCALATION}
        docs = retrieve_approved(message)
        if not docs:
            return {"route": "escalate", "selected_tool": selected, "response": ESCALATION}
        return {"route": "faq", "selected_tool": selected, "evidence_ids": [d.doc_id for d in docs],
                "response": " ".join(d.text for d in docs)}
    return {"route": "escalate", "selected_tool": selected, "response": ESCALATION}
