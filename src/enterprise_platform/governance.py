"""Synthetic enterprise tool gateway with tenant, role and approval boundaries.

Identity verification is simulated; no real JWTs, services or write APIs.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    subject: str
    tenant: str
    roles: tuple[str, ...]
    verified: bool = False

@dataclass(frozen=True)
class Tool:
    name: str
    department: str
    required_role: str
    requires_approval: bool = False

TOOLS = {
    "hr_policy_lookup": Tool("hr_policy_lookup", "hr", "hr_reader"),
    "finance_report_lookup": Tool("finance_report_lookup", "finance", "finance_reader"),
    "it_ticket_lookup": Tool("it_ticket_lookup", "it", "it_reader"),
    "vendor_payment_update": Tool("vendor_payment_update", "finance", "finance_admin", True),
}
RECORDS = (
    {"id": "hr-01", "tenant": "tenant-a", "department": "hr", "text": "Synthetic HR leave policy overview."},
    {"id": "fin-01", "tenant": "tenant-a", "department": "finance", "text": "Synthetic finance reporting procedure."},
    {"id": "it-01", "tenant": "tenant-a", "department": "it", "text": "Synthetic IT support procedure."},
    {"id": "fin-02", "tenant": "tenant-b", "department": "finance", "text": "Synthetic tenant B finance procedure."},
)

class GovernedGateway:
    def __init__(self):
        self.audit = []
        self._approvals = set()

    def approve(self, request_id: str, approver: Principal) -> bool:
        if not approver.verified or "approver" not in approver.roles:
            return False
        self._approvals.add((approver.tenant, request_id))
        self.audit.append({"event": "approved", "request_id": request_id,
                           "tenant": approver.tenant, "approver": approver.subject})
        return True

    def execute(self, principal: Principal, tool_name: str,
                requested_tenant: str, request_id: str = "demo-request") -> dict:
        tool = TOOLS.get(tool_name)
        reason = None
        if not principal.verified:
            reason = "identity_not_verified"
        elif tool is None:
            reason = "tool_not_registered"
        elif requested_tenant != principal.tenant:
            reason = "cross_tenant_access"
        elif tool.required_role not in principal.roles:
            reason = "role_not_permitted"
        elif tool.requires_approval and (principal.tenant, request_id) not in self._approvals:
            reason = "human_approval_required"
        elif tool.requires_approval:
            reason = "write_execution_not_connected"
        if reason:
            outcome = {"status": "approval_required" if reason == "human_approval_required" else "denied",
                       "reason": reason, "tool": tool_name, "records": []}
        else:
            records = [{"id": row["id"], "text": row["text"]} for row in RECORDS
                       if row["tenant"] == principal.tenant and row["department"] == tool.department]
            outcome = {"status": "allowed", "reason": "tenant_role_and_tool_authorized",
                       "tool": tool_name, "records": records}
        self.audit.append({"event": "tool_decision", "request_id": request_id,
                           "subject": principal.subject, "tenant": principal.tenant,
                           "tool": tool_name, "status": outcome["status"], "reason": outcome["reason"]})
        return outcome


    def execute_request(self, principal: Principal, message: str, requested_tenant: str,
                        request_id: str = "demo-request", model=None) -> dict:
        """Optional model routing, never model authorization or arbitrary arguments."""
        # Reject unverified and cross-tenant requests before any model inference.
        if not principal.verified or requested_tenant != principal.tenant:
            result = self.execute(principal, "preflight_request", requested_tenant, request_id)
            result["model_called"] = False
            return result
        if model is None:
            raise ValueError("Natural-language routing requires a model")
        from .azure_routing import select_tool
        try:
            selected = select_tool(message, model)
        except (ValueError, RuntimeError, TimeoutError) as exc:
            result = {"status": "denied", "reason": "model_routing_failed",
                      "tool": None, "records": [], "model_called": True}
            self.audit.append({"event": "tool_decision", "request_id": request_id,
                               "subject": principal.subject, "tenant": principal.tenant,
                               "tool": None, "status": "denied", "reason": result["reason"],
                               "error_type": type(exc).__name__})
            return result
        if selected is None:
            result = {"status": "denied", "reason": "unsupported_request",
                      "tool": None, "records": [], "model_called": True}
            self.audit.append({"event": "tool_decision", "request_id": request_id,
                               "subject": principal.subject, "tenant": principal.tenant,
                               "tool": None, "status": "denied", "reason": result["reason"]})
            return result
        result = self.execute(principal, selected, requested_tenant, request_id)
        result["model_called"] = True
        return result


DEMO_PRINCIPALS = {
    "Unverified caller": Principal("guest", "tenant-a", ("finance_reader",), False),
    "HR reader · tenant A": Principal("hr-analyst", "tenant-a", ("hr_reader",), True),
    "Finance reader · tenant A": Principal("fin-analyst", "tenant-a", ("finance_reader",), True),
    "Finance reader · tenant B": Principal("fin-analyst-b", "tenant-b", ("finance_reader",), True),
    "Finance admin · tenant A": Principal("fin-admin", "tenant-a", ("finance_admin",), True),
    "Approver · tenant A": Principal("reviewer", "tenant-a", ("approver",), True),
}
