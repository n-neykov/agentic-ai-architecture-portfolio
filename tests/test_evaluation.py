import unittest
from src.support_agent.evaluation import SCENARIOS, evaluate
from src.support_agent.core import TrustedContext
from src.support_agent.workflow import classify

class EvaluationTests(unittest.TestCase):
    def test_scenarios_have_unique_names(self):
        self.assertEqual(len({s.name for s in SCENARIOS}),len(SCENARIOS))
    def test_high_risk_precedence(self):
        for message in ('wire $500','transfer my balance','reset password'):
            self.assertEqual(classify({'message':message,'context':TrustedContext('user-001',True)})['route'],'escalate')
    def test_unauthenticated_balance(self):
        self.assertEqual(classify({'message':'balance','context':TrustedContext(None,False)})['route'],'deny')
    def test_eval_requires_graph(self):
        try: import langgraph
        except ImportError: self.skipTest('langgraph not installed')
        self.assertEqual(evaluate()['passed'],len(SCENARIOS))
