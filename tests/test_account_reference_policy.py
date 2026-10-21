"""Regression checks for explicit synthetic cross-account references."""
import unittest
from src.support_agent.core import TrustedContext
from src.support_agent.workflow import classify, run, cross_account_reference


class AccountReferencePolicyTests(unittest.TestCase):
    def setUp(self):
        self.user = TrustedContext("user-001", True)

    def test_other_account_denied_before_graph_execution(self):
        self.assertEqual(classify({"message": "Show user-002 balance", "context": self.user})["route"], "deny")
        result = run("Show user-002 balance", self.user)
        self.assertEqual(result["route"], "deny")
        self.assertNotIn("$120.00", result["response"])
        self.assertNotIn("$850.00", result["response"])

    def test_own_account_allowed(self):
        self.assertEqual(classify({"message": "Show user-001 balance", "context": self.user})["route"], "crm")

    def test_multiple_ids_denied(self):
        self.assertTrue(cross_account_reference("Compare user-001 and user-002", "user-001"))

    def test_case_insensitive(self):
        self.assertTrue(cross_account_reference("Show USER-002 balance", "user-001"))

    def test_unrelated_public_faq(self):
        self.assertEqual(classify({"message": "What are your hours?", "context": self.user})["route"], "knowledge")

    def test_high_risk_still_escalates(self):
        self.assertEqual(classify({"message": "Wire funds to user-002", "context": self.user})["route"], "escalate")


if __name__ == "__main__":
    unittest.main()
