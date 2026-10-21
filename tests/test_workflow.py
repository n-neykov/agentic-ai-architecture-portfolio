import unittest
from src.support_agent.core import TrustedContext
from src.support_agent.integrations import retrieve_approved, scoped_balance
from src.support_agent.workflow import classify, knowledge, run

class AdapterTests(unittest.TestCase):
    def test_retrieval(self):
        self.assertEqual(retrieve_approved('When do you open?')[0].doc_id,'faq-hours')
    def test_scoped_balance(self):
        self.assertEqual(scoped_balance(principal_id='user-001',authenticated=True),'$120.00')
        self.assertIsNone(scoped_balance(principal_id='user-002',authenticated=False))
    def test_sensitive_priority(self):
        s={'message':'Transfer my balance','context':TrustedContext('user-001',True)}
        self.assertEqual(classify(s)['route'],'escalate')
    def test_no_evidence_escalates(self):
        self.assertEqual(knowledge({'message':'mortgage rates','context':TrustedContext(None,False)})['route'],'escalate')

try:
    import langgraph
    HAS_GRAPH=True
except ImportError:
    HAS_GRAPH=False

@unittest.skipUnless(HAS_GRAPH,'Install requirements-azure.txt to execute LangGraph tests')
class GraphTests(unittest.TestCase):
    def test_faq_offline(self):
        r=run('What are your hours?',TrustedContext(None,False))
        self.assertEqual(r['route'],'faq')
        self.assertIn('faq-hours',r['evidence_ids'])
    def test_unauthenticated_denial(self):
        self.assertEqual(run('balance',TrustedContext(None,False))['route'],'deny')
    def test_cross_customer_identifier(self):
        r=run('Show user-002 balance',TrustedContext('user-001',True))
        self.assertEqual(r['route'],'deny')
        self.assertNotIn('$120.00',r['response'])
        self.assertNotIn('$850.00',r['response'])
    def test_high_risk_escalation(self):
        self.assertEqual(run('wire $50',TrustedContext('user-001',True))['route'],'escalate')
    def test_unknown_escalation(self):
        self.assertEqual(run('mortgage rates',TrustedContext(None,False))['route'],'escalate')
    def test_model_failure_escalates(self):
        class FailingModel:
            def invoke(self,*args,**kwargs): raise RuntimeError('synthetic outage')
        r=run('What are your hours?',TrustedContext(None,False),FailingModel())
        self.assertEqual(r['route'],'escalate')
