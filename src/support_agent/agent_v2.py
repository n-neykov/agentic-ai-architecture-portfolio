"""Project 01 v2: bounded, multi-intent synthetic customer support.

This is a deterministic orchestration baseline with optional LLM tool-selection
for supported public/private intents. It is NOT production authentication.
"""
import re
from .core import TrustedContext
from .integrations import retrieve_approved, scoped_balance
from .workflow import HIGH_RISK, cross_account_reference
from .bounded_agent import choose_tool, ESCALATION

IDENTITY = re.compile(r"\b(who am i|what user am i|my (?:user|account) id|which user am i)\b", re.I)
BALANCE = re.compile(r"\b(balance|account amount)\b", re.I)
PUBLIC = re.compile(r"\b(hours?|open|fees?|charges?|cards?|replace(?:ment)?)\b", re.I)


def plan(message: str, context: TrustedContext) -> dict:
    """Validate request-level safety before allowing any model invocation."""
    if not message or not message.strip():
        raise ValueError("Message must not be empty")
    normalized = message.lower()
    if any(term in normalized for term in HIGH_RISK):
        return {"policy": "escalate", "intents": [], "reason": "high-risk operation"}
    if cross_account_reference(message, context.principal_id):
        return {"policy": "deny", "intents": [], "reason": "cross-account reference"}
    intents = []
    if IDENTITY.search(message):
        intents.append("session_info")
    if BALANCE.search(message):
        if not context.authenticated or not context.principal_id:
            return {"policy": "deny", "intents": [], "reason": "private read without demo identity"}
        intents.append("account_balance")
    if PUBLIC.search(message):
        intents.append("faq_lookup")
    if not intents:
        return {"policy": "escalate", "intents": [], "reason": "unsupported intent"}
    return {"policy": "allow", "intents": intents, "reason": "supported request"}


def run_v2(message: str, context: TrustedContext, model=None) -> dict:
    """Return structured steps and a safe composite response.

    If model is supplied, each public/private intent requires a matching
    allowlisted model decision; session_info is deterministic. Any mismatch,
    outage, or missing evidence fails closed without partial private disclosure.
    """
    decision = plan(message, context)
    trace = [{"stage": "policy", **decision}]
    if decision["policy"] != "allow":
        return {"route": decision["policy"], "selected_tool": None,
                "response": ("Account access is not authorized for this request."
                             if decision["policy"] == "deny" else ESCALATION),
                "evidence_ids": [], "steps": trace}
    answers, evidence, selected = [], [], []
    for intent in decision["intents"]:
        if intent != "session_info" and model is not None:
            try:
                # Model chooses from existing bounded allowlist, but it cannot
                # override the policy's intended tool or choose tool arguments.
                tool = choose_tool(model, message if len(decision["intents"]) == 1 else
                                   ("What are your hours or fees?" if intent == "faq_lookup"
                                    else "What is my balance?"))
            except Exception:
                return {"route": "escalate", "selected_tool": None, "response": ESCALATION,
                        "evidence_ids": [], "steps": trace + [{"stage": "model", "status": "failed"}]}
            if tool != intent:
                return {"route": "escalate", "selected_tool": tool, "response": ESCALATION,
                        "evidence_ids": [], "steps": trace + [{"stage": "model", "status": "tool mismatch"}]}
        if intent == "session_info":
            answer = ("Demo identity: " + context.principal_id + " (simulated; not verified authentication)."
                      if context.authenticated and context.principal_id
                      else "Demo identity: Anonymous (not signed in).")
        elif intent == "account_balance":
            balance = scoped_balance(principal_id=context.principal_id,
                                     authenticated=context.authenticated)
            if balance is None:
                return {"route": "escalate", "selected_tool": intent,
                        "response": ESCALATION, "evidence_ids": [], "steps": trace}
            answer = "Your synthetic account balance is " + balance + "."
        else:
            docs = retrieve_approved(message)
            if not docs:
                return {"route": "escalate", "selected_tool": intent,
                        "response": ESCALATION, "evidence_ids": [], "steps": trace}
            answer = " ".join(d.text for d in docs)
            evidence.extend(d.doc_id for d in docs)
        answers.append(answer)
        selected.append(intent)
        trace.append({"stage": "tool", "tool": intent, "status": "completed"})
    return {"route": "multi" if len(selected) > 1 else
            {"session_info": "session_info", "account_balance": "crm_read", "faq_lookup": "faq"}[selected[0]],
            "selected_tool": selected[0] if len(selected) == 1 else selected,
            "response": "\n\n".join(answers), "evidence_ids": evidence, "steps": trace}
