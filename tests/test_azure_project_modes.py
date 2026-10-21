"""Offline mocked-Azure tests: no network or secrets required."""
import json
import unittest
from types import SimpleNamespace

from src.document_processing.pipeline import IntakeEngine, SAMPLES
from src.enterprise_platform.governance import GovernedGateway, DEMO_PRINCIPALS


class FakeModel:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error
        self.calls = 0

    def invoke(self, messages):
        self.calls += 1
        if self.error:
            raise self.error
        return SimpleNamespace(content=json.dumps(self.value))


class AzureDocumentTests(unittest.TestCase):
    def test_valid_invoice_model_staged(self):
        model = FakeModel({"document_type": "invoice", "fields": {
            "vendor_id": "VEN-001", "invoice_number": "INV-1007",
            "amount": "1450.00", "currency": "USD"}})
        result = IntakeEngine().process(SAMPLES["Valid invoice"], model=model)
        self.assertEqual(result["status"], "staged")
        self.assertEqual(result["mode"], "azure")
        self.assertEqual(result["evidence"]["amount"]["line"], 4)
        self.assertEqual(model.calls, 1)

    def test_hallucinated_value_fails_closed(self):
        model = FakeModel({"document_type": "invoice", "fields": {"amount": "999999"}})
        engine = IntakeEngine()
        result = engine.process(SAMPLES["Valid invoice"], model=model)
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("model_inference_failed", result["issues"])
        self.assertEqual(engine.staged_count(), 0)

    def test_sensitive_bank_account_cannot_be_omitted(self):
        model = FakeModel({"document_type": "supplier_agreement", "fields": {
            "vendor_id": "VEN-002", "effective_date": "2026-11-01"}})
        result = IntakeEngine().process(SAMPLES["Agreement requiring review"], model=model)
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("sensitive_bank_details_require_review", result["issues"])

    def test_model_failure_does_not_poison_retry(self):
        engine = IntakeEngine()
        fail = FakeModel(error=RuntimeError("test outage"))
        self.assertEqual(engine.process(SAMPLES["Valid invoice"], model=fail)["status"], "needs_review")
        success = FakeModel({"document_type": "invoice", "fields": {
            "vendor_id": "VEN-001", "invoice_number": "INV-1007",
            "amount": "1450.00", "currency": "USD"}})
        self.assertEqual(engine.process(SAMPLES["Valid invoice"], model=success)["status"], "staged")

    def test_duplicate_avoids_second_model_call(self):
        model = FakeModel({"document_type": "invoice", "fields": {
            "vendor_id": "VEN-001", "invoice_number": "INV-1007",
            "amount": "1450.00", "currency": "USD"}})
        engine = IntakeEngine()
        engine.process(SAMPLES["Valid invoice"], model=model)
        self.assertTrue(engine.process(SAMPLES["Valid invoice"], model=model)["duplicate"])
        self.assertEqual(model.calls, 1)


class AzureGovernanceTests(unittest.TestCase):
    def test_authorized_natural_language_lookup(self):
        model = FakeModel({"tool": "finance_report_lookup"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Finance reader · tenant A"], "Find finance reports",
            "tenant-a", model=model)
        self.assertEqual(result["status"], "allowed")
        self.assertEqual([r["id"] for r in result["records"]], ["fin-01"])

    def test_cross_tenant_denied_without_inference(self):
        model = FakeModel({"tool": "finance_report_lookup"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Finance reader · tenant A"], "Find finance reports",
            "tenant-b", model=model)
        self.assertEqual(result["reason"], "cross_tenant_access")
        self.assertEqual(model.calls, 0)

    def test_unverified_denied_without_inference(self):
        model = FakeModel({"tool": "finance_report_lookup"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Unverified caller"], "Find finance reports",
            "tenant-a", model=model)
        self.assertEqual(result["reason"], "identity_not_verified")
        self.assertEqual(model.calls, 0)

    def test_model_cannot_grant_hr_finance_access(self):
        model = FakeModel({"tool": "finance_report_lookup"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["HR reader · tenant A"], "Find finance reports",
            "tenant-a", model=model)
        self.assertEqual(result["reason"], "role_not_permitted")
        self.assertEqual(result["records"], [])

    def test_unregistered_model_tool_fails_closed(self):
        model = FakeModel({"tool": "delete_records"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Finance reader · tenant A"], "Delete everything",
            "tenant-a", model=model)
        self.assertEqual(result["reason"], "model_routing_failed")

    def test_model_outage_fails_closed(self):
        model = FakeModel(error=RuntimeError("test outage"))
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Finance reader · tenant A"], "Find finance reports",
            "tenant-a", model=model)
        self.assertEqual(result["reason"], "model_routing_failed")

    def test_model_write_cannot_execute(self):
        model = FakeModel({"tool": "vendor_payment_update"})
        result = GovernedGateway().execute_request(
            DEMO_PRINCIPALS["Finance admin · tenant A"], "Update vendor payment",
            "tenant-a", model=model)
        self.assertEqual(result["status"], "approval_required")


if __name__ == "__main__":
    unittest.main()
