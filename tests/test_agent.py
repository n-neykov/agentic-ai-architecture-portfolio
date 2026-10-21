import unittest
from src.support_agent.core import TrustedContext, handle

class RoutingTests(unittest.TestCase):
    def test_public_faq(self):
        self.assertEqual(handle('What are your hours?',TrustedContext(None,False))['route'],'faq')
    def test_unauthenticated_balance_denied(self):
        self.assertEqual(handle('balance',TrustedContext(None,False))['route'],'deny')
    def test_scoped_account_lookup(self):
        result=handle('Show user-002 balance',TrustedContext('user-001',True))
        self.assertIn('$120.00',result['response'])
        self.assertNotIn('$850.00',result['response'])
    def test_high_risk_escalation(self):
        self.assertEqual(handle('wire $500',TrustedContext('user-001',True))['route'],'escalate')
