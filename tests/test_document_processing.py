import unittest
from src.document_processing.pipeline import IntakeEngine, SAMPLES, validate

class DocumentPipelineTests(unittest.TestCase):
    def setUp(self):
        self.engine = IntakeEngine()

    def test_invoice_staged_with_evidence(self):
        r = self.engine.process(SAMPLES["Valid invoice"])
        self.assertEqual(r["status"], "staged")
        self.assertEqual(r["evidence"]["amount"]["line"], 4)

    def test_duplicate_idempotency(self):
        a = self.engine.process(SAMPLES["Valid invoice"])
        b = self.engine.process(SAMPLES["Valid invoice"])
        self.assertEqual(a["workflow_id"], b["workflow_id"])
        self.assertTrue(b["duplicate"])
        self.assertEqual(self.engine.staged_count(), 1)

    def test_missing_field_review(self):
        r = self.engine.process(SAMPLES["Missing invoice amount"])
        self.assertIn("missing_amount", r["issues"])
        with self.assertRaises(ValueError):
            self.engine.approve(r["workflow_id"], "reviewer")

    def test_tax_form(self):
        self.assertEqual(self.engine.process(SAMPLES["Tax form"])["status"], "staged")

    def test_bank_details_require_review(self):
        r = self.engine.process(SAMPLES["Agreement requiring review"])
        self.assertEqual(r["status"], "needs_review")
        self.assertEqual(self.engine.staged_count(), 0)
        self.assertEqual(self.engine.approve(r["workflow_id"], "reviewer")["status"], "staged")

    def test_malformed_bank_details_cannot_bypass_review(self):
        text = "Supplier Agreement\nVendor ID: VEN-002\nEffective Date: 2026-11-01\nBank Account: invalid value!"
        result = self.engine.process(text)
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("invalid_bank_account_format", result["issues"])
        with self.assertRaises(ValueError):
            self.engine.approve(result["workflow_id"], "reviewer")
        self.assertEqual(self.engine.staged_count(), 0)

    def test_cross_tenant_approval_denied(self):
        r = self.engine.process(SAMPLES["Agreement requiring review"], "tenant-a")
        with self.assertRaises(PermissionError):
            self.engine.approve(r["workflow_id"], "reviewer", "tenant-b")

    def test_unknown_vendor(self):
        self.assertIn("unknown_vendor", self.engine.process(SAMPLES["Unknown vendor"])["issues"])

    def test_unsupported_type(self):
        self.assertEqual(self.engine.process("Unknown\nVendor ID: VEN-001")["status"], "needs_review")

    def test_empty_or_oversize(self):
        for value in (" ", "X" * 20001):
            with self.assertRaises(ValueError):
                self.engine.process(value)

    def test_tenant_specific_hash(self):
        a = self.engine.process(SAMPLES["Valid invoice"], "tenant-a")
        b = self.engine.process(SAMPLES["Valid invoice"], "tenant-b")
        self.assertNotEqual(a["workflow_id"], b["workflow_id"])

    def test_bad_date(self):
        issues = validate("supplier_agreement", {"vendor_id": "VEN-001", "effective_date": "2026-02-30"})
        self.assertIn("invalid_effective_date", issues)

if __name__ == "__main__":
    unittest.main()
