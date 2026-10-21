"""CLI demo. --azure performs paid Azure inference for approved public FAQ only."""
import argparse
import json
import sys
from .core import TrustedContext
from .workflow import run
from .evaluation import evaluate

def main():
    p=argparse.ArgumentParser(description='Synthetic enterprise support agent demo')
    p.add_argument('--azure',action='store_true',help='Enable live Azure OpenAI inference')
    p.add_argument('--agent',action='store_true',help='Use bounded LLM-selected tools (requires --azure)')
    p.add_argument('--evaluate',action='store_true',help='Run synthetic routing evaluation')
    p.add_argument('--message',default='What are your hours?')
    p.add_argument('--principal',default=None,help='SIMULATED identity, NOT authenticated')
    a=p.parse_args()
    if a.agent and not a.azure:
        p.error('--agent requires --azure; offline agent tests use a FakeModel')
    if a.evaluate:
        result = evaluate()
        print(json.dumps(result, indent=2))
        if result['passed'] != result['total']:
            sys.exit(1)
        return
    model=None
    if a.azure:
        from dotenv import load_dotenv
        load_dotenv()
        from .azure_model import make_azure_model
        model=make_azure_model()
    context=TrustedContext(a.principal, bool(a.principal))
    if a.agent:
        from .bounded_agent import run_agent
        result=run_agent(a.message,context,model)
    else:
        result=run(a.message,context,model)
    print(json.dumps(result,default=str,indent=2))
    print('WARNING: --principal is a synthetic demo assertion, not verified authentication.')

if __name__=='__main__': main()
