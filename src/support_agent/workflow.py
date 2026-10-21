"""LangGraph implementation of a policy-first support workflow.

IMPORTANT: Authentication is trusted only as a caller-supplied server-side assertion.
The demo does not verify JWTs or implement production IAM.
"""
from typing import TypedDict
from .core import TrustedContext
from .integrations import retrieve_approved, scoped_balance

HIGH_RISK=('transfer','wire','send money','close account','refund','change address','reset password')
ACCOUNT=('balance','account amount')

class State(TypedDict, total=False):
    message: str
    context: TrustedContext
    route: str
    response: str
    evidence_ids: list[str]

def classify(state: State) -> State:
    m=state['message'].lower()
    ctx=state['context']
    if any(x in m for x in HIGH_RISK): route='escalate'
    elif any(x in m for x in ACCOUNT): route='crm' if ctx.authenticated and ctx.principal_id else 'deny'
    else: route='knowledge'
    return {'route':route}

def crm(state: State) -> State:
    ctx=state['context']
    result=scoped_balance(principal_id=ctx.principal_id, authenticated=ctx.authenticated)
    return {'route':'crm_read','response':f'Your balance is {result}.'} if result is not None else {'route':'escalate','response':'A human specialist must review this request.'}

def knowledge(state: State, model=None) -> State:
    docs=retrieve_approved(state['message'])
    if not docs: return {'route':'escalate','response':'A human specialist can help with that request.','evidence_ids':[]}
    evidence='\n'.join(f'[{d.doc_id}] {d.text}' for d in docs)
    if model is None:
        answer=' '.join(d.text for d in docs)
    else:
        try:
            from .azure_model import grounded_answer
            answer=grounded_answer(model,state['message'],evidence)
        except Exception:
            return {'route':'escalate','response':'Automated assistance is temporarily unavailable. A human specialist can help.','evidence_ids':[d.doc_id for d in docs]}
        if not answer or answer.strip().upper()=='ESCALATE':
            return {'route':'escalate','response':'A human specialist can help with that request.','evidence_ids':[d.doc_id for d in docs]}
    return {'route':'faq','response':answer,'evidence_ids':[d.doc_id for d in docs]}

def finish(state: State) -> State:
    if state['route']=='deny': return {'response':'Please sign in to view account information.'}
    return {'response':'A human specialist must review this request.'}

def build_graph(model=None):
    from langgraph.graph import StateGraph, START, END
    graph=StateGraph(State)
    graph.add_node('classify',classify)
    graph.add_node('crm',crm)
    graph.add_node('knowledge',lambda state: knowledge(state,model))
    graph.add_node('finish',finish)
    graph.add_edge(START,'classify')
    graph.add_conditional_edges('classify',lambda state:state['route'],{
        'crm':'crm','knowledge':'knowledge','escalate':'finish','deny':'finish'
    })
    for node in ('crm','knowledge','finish'): graph.add_edge(node,END)
    return graph.compile()

def run(message: str, context: TrustedContext, model=None) -> State:
    if not message.strip(): raise ValueError('Message must not be empty')
    return build_graph(model).invoke({'message':message,'context':context})
