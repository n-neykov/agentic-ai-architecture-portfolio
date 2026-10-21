"""Azure-assisted natural-language tool selection, with deterministic authorization.

The model can only nominate an allowlisted tool name. No arbitrary arguments.
"""
from src.support_agent.structured_inference import structured_decision, ModelDecisionError
from .governance import TOOLS

INSTRUCTIONS = """You are a routing classifier for a synthetic enterprise agent platform.
Select ONE registered tool matching the user's request:
hr_policy_lookup (HR policy), finance_report_lookup (finance reports),
it_ticket_lookup (IT support), vendor_payment_update (vendor payment changes).
If unsupported or ambiguous, select none.
Return ONLY JSON with exactly one key: tool, with one of those names or "none".
You cannot grant access, change tenants, execute tools or approve payments."""


def select_tool(message: str, model) -> str | None:
    if not isinstance(message, str) or not message.strip() or len(message) > 2000:
        raise ValueError("Provide a short nonempty synthetic request")
    decision = structured_decision(model, INSTRUCTIONS, message, allowed_keys={"tool"})
    if set(decision) != {"tool"} or not isinstance(decision["tool"], str):
        raise ModelDecisionError("Invalid tool selection")
    selected = decision["tool"]
    if selected == "none":
        return None
    if selected not in TOOLS:
        raise ModelDecisionError("Model selected an unregistered tool")
    return selected
