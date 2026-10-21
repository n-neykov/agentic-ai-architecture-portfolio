"""Shared, bounded Azure Foundry inference helpers for synthetic portfolio demos.

Only explicit user-triggered calls use Azure. No credentials or source data logged.
"""
import json
from langchain_core.messages import SystemMessage, HumanMessage


class ModelDecisionError(ValueError):
    pass


def structured_decision(model, instructions: str, user_text: str, *, allowed_keys: set[str]) -> dict:
    """Parse one JSON object with a strict key allowlist; fail closed."""
    response = model.invoke([SystemMessage(content=instructions), HumanMessage(content=user_text)])
    raw = response.content
    if not isinstance(raw, str) or len(raw) > 12_000:
        raise ModelDecisionError("Invalid model output")
    try:
        value = json.loads(raw.strip())
    except (ValueError, TypeError) as exc:
        raise ModelDecisionError("Model did not return valid JSON") from exc
    if not isinstance(value, dict) or set(value) - allowed_keys:
        raise ModelDecisionError("Unexpected model response shape")
    return value


def configured_model():
    from src.support_agent.azure_model import make_azure_model
    return make_azure_model()
