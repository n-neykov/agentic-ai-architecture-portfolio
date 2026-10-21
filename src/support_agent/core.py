"""Dependency-free synthetic vertical slice; not an LLM or LangGraph deployment."""
from dataclasses import dataclass

FAQ = {
    "hours": "Support is available Monday through Friday, 9:00–17:00 (fictional).",
    "fees": "Please consult the published fee schedule (fictional).",
}
BALANCES = {"user-001": "$120.00", "user-002": "$850.00"}  # Synthetic only

@dataclass(frozen=True)
class TrustedContext:
    principal_id: str | None
    authenticated: bool

def handle(message: str, context: TrustedContext) -> dict:
    """Route requests; never accept customer identity from message text."""
    m = message.lower()
    if any(term in m for term in ("transfer", "wire", "send money", "close account", "refund")):
        return {"route": "escalate", "response": "A human specialist must review this request."}
    if any(term in m for term in ("balance", "account amount")):
        if not context.authenticated or not context.principal_id:
            return {"route": "deny", "response": "Please sign in to view account information."}
        balance = BALANCES.get(context.principal_id)
        if balance is None:
            return {"route": "escalate", "response": "Account information is unavailable; please contact support."}
        return {"route": "crm_read", "response": f"Your balance is {balance}."}
    if "hours" in m or "open" in m:
        return {"route": "faq", "response": FAQ["hours"]}
    if "fee" in m:
        return {"route": "faq", "response": FAQ["fees"]}
    return {"route": "escalate", "response": "A human specialist can help with that request."}
