"""Synthetic supplier-document intake, validation, review and idempotent staging.

No OCR, real ERP, persistent queue, external files or Azure services are used.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
import re

TYPES = ("invoice", "tax_form", "supplier_agreement")
REQUIRED = {
    "invoice": ("vendor_id", "invoice_number", "amount", "currency"),
    "tax_form": ("vendor_id", "tax_id"),
    "supplier_agreement": ("vendor_id", "effective_date"),
}
PATTERNS = {
    "vendor_id": r"(?im)^Vendor ID:\s*([A-Z0-9-]+)\s*$",
    "invoice_number": r"(?im)^Invoice Number:\s*([A-Z0-9-]+)\s*$",
    "amount": r"(?im)^Amount:\s*([0-9]+(?:\.[0-9]{1,2})?)\s*$",
    "currency": r"(?im)^Currency:\s*([A-Z]{3})\s*$",
    "tax_id": r"(?im)^Tax ID:\s*([0-9-]+)\s*$",
    "effective_date": r"(?im)^Effective Date:\s*(\d{4}-\d{2}-\d{2})\s*$",
    "bank_account": r"(?im)^Bank Account:\s*([A-Z0-9-]+)\s*$",
}
VENDORS = {"VEN-001": "Northstar Office Supplies", "VEN-002": "Atlas Components"}
MAX_BYTES = 20_000


@dataclass(frozen=True)
class IntakeResult:
    workflow_id: str
    document_type: str
    status: str
    fields: dict
    evidence: dict
    issues: list[str]
    audit: list[dict]
    staged: bool


def classify(text: str) -> str:
    first = text.splitlines()[0].strip().lower() if text.splitlines() else ""
    return {"invoice": "invoice", "tax form": "tax_form",
            "supplier agreement": "supplier_agreement"}.get(first, "unknown")


def extract(text: str) -> tuple[dict, dict]:
    fields, evidence = {}, {}
    lines = text.splitlines()
    for name, pattern in PATTERNS.items():
        matches = list(re.finditer(pattern, text))
        if matches:
            match = matches[0]
            fields[name] = match.group(1)
            line = text[:match.start()].count("\n") + 1
            evidence[name] = {"line": line, "source": lines[line - 1].split(":")[0]}
    return fields, evidence


def validate(doc_type: str, fields: dict) -> list[str]:
    if doc_type not in REQUIRED:
        return ["unsupported_document_type"]
    issues = [f"missing_{name}" for name in REQUIRED[doc_type] if not fields.get(name)]
    if fields.get("vendor_id") and fields["vendor_id"] not in VENDORS:
        issues.append("unknown_vendor")
    if doc_type == "invoice" and "amount" in fields:
        try:
            if float(fields["amount"]) <= 0:
                issues.append("invalid_amount")
        except ValueError:
            issues.append("invalid_amount")
    if doc_type == "invoice" and fields.get("currency") not in (None, "USD", "EUR"):
        issues.append("unsupported_currency")
    if doc_type == "supplier_agreement" and "effective_date" in fields:
        from datetime import date
        try:
            date.fromisoformat(fields["effective_date"])
        except ValueError:
            issues.append("invalid_effective_date")
    if "bank_account" in fields:
        issues.append("sensitive_bank_details_require_review")
    return issues


class IntakeEngine:
    """In-memory idempotency and staging; deliberately not durable across restarts."""

    def __init__(self):
        self._results = {}
        self._staging = {}

    def process(self, text: str, tenant_id: str = "demo-tenant", model=None) -> dict:
        if not isinstance(text, str) or not text.strip():
            raise ValueError("A nonempty synthetic document is required")
        if len(text.encode("utf-8")) > MAX_BYTES:
            raise ValueError("Document exceeds demo size limit")
        if not re.fullmatch(r"[a-z][a-z0-9-]{1,63}", tenant_id):
            raise ValueError("Invalid tenant identifier")
        workflow_id = sha256((tenant_id + "\0" + ("azure" if model is not None else "offline") + "\0" + text).encode()).hexdigest()[:16]
        if workflow_id in self._results:
            result = dict(self._results[workflow_id])
            result["duplicate"] = True
            return result
        if model is None:
            kind = classify(text)
            fields, evidence = extract(text)
        else:
            from .azure_extraction import infer_document
            try:
                kind, fields, evidence = infer_document(text, model)
            except (ValueError, RuntimeError, TimeoutError) as exc:
                result = asdict(IntakeResult(workflow_id, "unknown", "needs_review", {}, {},
                            ["model_inference_failed"], [
                                {"event": "received", "workflow_id": workflow_id, "tenant": tenant_id},
                                {"event": "model_failed_closed", "error_type": type(exc).__name__}
                            ], False))
                result["duplicate"] = False
                result["mode"] = "azure"
                return dict(result)
        issues = validate(kind, fields)
        status = "needs_review" if issues else "staged"
        audit = [
            {"event": "received", "workflow_id": workflow_id, "tenant": tenant_id},
            {"event": "classified", "type": kind},
            {"event": "validated", "status": status, "issue_codes": issues},
        ]
        if status == "staged":
            self._staging[workflow_id] = {"tenant": tenant_id, "type": kind, "fields": fields.copy()}
            audit.append({"event": "staged", "target": "synthetic_in_memory_outbox"})
        result = asdict(IntakeResult(workflow_id, kind, status, fields, evidence, issues, audit, status == "staged"))
        result["duplicate"] = False
        result["mode"] = "azure" if model is not None else "offline"
        self._results[workflow_id] = result
        return dict(result)

    def approve(self, workflow_id: str, reviewer: str, tenant_id: str = "demo-tenant") -> dict:
        """Explicit simulated reviewer approval; never automatic for sensitive records."""
        if not reviewer or not reviewer.strip():
            raise ValueError("Named reviewer required")
        if workflow_id not in self._results:
            raise KeyError("Unknown workflow")
        result = self._results[workflow_id]
        if result["audit"][0]["tenant"] != tenant_id:
            raise PermissionError("Cross-tenant approval denied")
        if result["status"] == "staged":
            return dict(result)
        if any(x.startswith("missing_") or x in ("unknown_vendor", "invalid_amount", "invalid_effective_date", "unsupported_currency", "unsupported_document_type") for x in result["issues"]):
            raise ValueError("Invalid records require correction before approval")
        result["status"] = "staged"
        result["staged"] = True
        result["audit"].append({"event": "approved_and_staged", "reviewer": reviewer, "target": "synthetic_in_memory_outbox"})
        self._staging[workflow_id] = {"tenant": tenant_id, "type": result["document_type"], "fields": result["fields"].copy()}
        return dict(result)

    def staged_count(self) -> int:
        return len(self._staging)


SAMPLES = {
    "Valid invoice": "Invoice\nVendor ID: VEN-001\nInvoice Number: INV-1007\nAmount: 1450.00\nCurrency: USD",
    "Missing invoice amount": "Invoice\nVendor ID: VEN-001\nInvoice Number: INV-1008\nCurrency: USD",
    "Tax form": "Tax Form\nVendor ID: VEN-002\nTax ID: 12-3456789",
    "Agreement requiring review": "Supplier Agreement\nVendor ID: VEN-002\nEffective Date: 2026-11-01\nBank Account: DEMO-12345",
    "Unknown vendor": "Invoice\nVendor ID: VEN-999\nInvoice Number: INV-999\nAmount: 99.00\nCurrency: USD",
}
