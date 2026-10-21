"""Offline contract tests with a fake LLM; no Azure calls or credentials."""
import unittest
from types import SimpleNamespace
from src.support_agent.core import TrustedContext
from src.support_agent.bounded_agent import run_agent

class FakeModel:
    def __init__(self, content, fails=False):
        self.content, self.fails, self.calls = content, fails, 0
    def invoke(self, messages):
        self.calls += 1
        if self.fails:
            raise RuntimeError("model unavailable")
        return SimpleNamespace(content=self.content)

class BoundedAgentTests(unittest.TestCase):
    def setUp(self):
        self.anon = TrustedContext(None, False)
        self.user = TrustedContext("user-001", True)

    def test_model_selects_faq_tool(self):
        model = FakeModel('{"tool":"faq_lookup"}')
        result = run_agent("What are your hours?", self.anon, model)
        self.assertEqual(result["route"], "faq")
        self.assertEqual(result["selected_tool"], "faq_lookup")
        self.assertIn("faq-hours", result["evidence_ids"])
        self.assertEqual(model.calls, 1)

    def test_model_selects_scoped_balance(self):
        model = FakeModel('{"tool":"account_balance"}')
        result = run_agent("Show user-002 balance", self.user, model)
        self.assertEqual(result["route"], "deny")
        self.assertEqual(model.calls, 0)
        self.assertNotIn("$120.00", result["response"])
        self.assertNotIn("$850.00", result["response"])

    def test_own_balance_still_works(self):
        model = FakeModel('{"tool":"account_balance"}')
        result = run_agent("Show user-001 balance", self.user, model)
        self.assertEqual(result["route"], "crm_read")
        self.assertEqual(model.calls, 1)

    def test_anonymous_balance_blocked_before_model(self):
        model = FakeModel('{"tool":"account_balance"}')
        result = run_agent("Show my balance", self.anon, model)
        self.assertEqual(result["route"], "deny")
        self.assertEqual(model.calls, 0)

    def test_transfer_blocked_before_model(self):
        model = FakeModel('{"tool":"faq_lookup"}')
        result = run_agent("Transfer $500 and show my balance", self.user, model)
        self.assertEqual(result["route"], "escalate")
        self.assertEqual(model.calls, 0)

    def test_unrelated_private_tool_denied(self):
        result = run_agent("What are your hours?", self.user, FakeModel('{"tool":"account_balance"}'))
        self.assertEqual(result["route"], "deny")

    def test_model_cannot_relabel_private_request_as_public(self):
        result = run_agent("Show my balance", self.user, FakeModel('{"tool":"faq_lookup"}'))
        self.assertEqual(result["route"], "escalate")

    def test_unknown_tool_escalates(self):
        result = run_agent("What are your hours?", self.anon, FakeModel('{"tool":"send_money"}'))
        self.assertEqual(result["route"], "escalate")

    def test_extra_arguments_rejected(self):
        result = run_agent("Show my balance", self.user, FakeModel('{"tool":"account_balance","account_id":"user-002"}'))
        self.assertEqual(result["route"], "escalate")

    def test_malformed_json_escalates(self):
        result = run_agent("What are your hours?", self.anon, FakeModel("faq_lookup"))
        self.assertEqual(result["route"], "escalate")

    def test_model_outage_escalates(self):
        result = run_agent("What are your hours?", self.anon, FakeModel("", fails=True))
        self.assertEqual(result["route"], "escalate")

    def test_unknown_faq_escalates(self):
        result = run_agent("Can I refinance?", self.anon, FakeModel('{"tool":"faq_lookup"}'))
        self.assertEqual(result["route"], "escalate")

    def test_empty_message_rejected(self):
        with self.assertRaises(ValueError):
            run_agent(" ", self.anon, FakeModel('{"tool":"faq_lookup"}'))

if __name__ == "__main__":
    unittest.main()
