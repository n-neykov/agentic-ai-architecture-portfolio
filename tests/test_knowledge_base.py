"""Offline regression coverage for the 12 approved fictional FAQ records."""
import unittest
from src.support_agent.core import TrustedContext
from src.support_agent.integrations import DOCUMENTS, retrieve_approved
from src.support_agent.agent_v2 import run_v2


class KnowledgeBaseTests(unittest.TestCase):
    CASES = (
        ("What are your hours?", "faq-hours"),
        ("What fees do you charge?", "faq-fees"),
        ("How do I replace a damaged card?", "faq-cards"),
        ("I lost my card", "faq-lost-card"),
        ("Where can I see my statements?", "faq-statements"),
        ("How does direct deposit work?", "faq-deposits"),
        ("What are payment processing times?", "faq-payment-times"),
        ("How can I open an account?", "faq-opening"),
        ("How do I contact support?", "faq-contact"),
        ("I have an online login issue", "faq-online-access"),
        ("What are ATM withdrawal limits?", "faq-atm"),
        ("How do I dispute a transaction?", "faq-disputes"),
    )

    def test_catalog_is_twelve_unique_records(self):
        self.assertEqual(len(DOCUMENTS), 12)
        self.assertEqual(len({d.doc_id for d in DOCUMENTS}), 12)
        self.assertTrue(all(d.title and d.text and d.category for d in DOCUMENTS))

    def test_each_topic_has_correct_evidence(self):
        for question, expected in self.CASES:
            with self.subTest(question=question):
                matches = retrieve_approved(question)
                self.assertIn(expected, [d.doc_id for d in matches])
                result = run_v2(question, TrustedContext(None, False))
                self.assertEqual(result["route"], "faq")
                self.assertIn(expected, result["evidence_ids"])

    def test_open_account_not_mistaken_for_business_hours(self):
        matches = retrieve_approved("How can I open an account?")
        self.assertEqual([d.doc_id for d in matches], ["faq-opening"])

    def test_lost_card_not_mistaken_for_replacement(self):
        matches = retrieve_approved("I lost my card")
        self.assertEqual([d.doc_id for d in matches], ["faq-lost-card"])

    def test_unsupported_request_does_not_get_evidence(self):
        self.assertEqual(retrieve_approved("What are your mortgage rates?"), [])
        self.assertEqual(run_v2("What are your mortgage rates?", TrustedContext(None, False))["route"], "escalate")

    def test_high_risk_still_preempts_public_retrieval(self):
        result = run_v2("What are your hours and transfer money?", TrustedContext(None, False))
        self.assertEqual(result["route"], "escalate")
        self.assertEqual(result["evidence_ids"], [])


if __name__ == "__main__":
    unittest.main()
