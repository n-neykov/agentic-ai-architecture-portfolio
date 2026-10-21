"""Portfolio demo UI. Run: streamlit run dashboard.py

Synthetic identities and balances only. Not an authentication service.
"""
import json
import streamlit as st

from src.support_agent.core import TrustedContext
from src.support_agent.workflow import run, classify
from src.support_agent.bounded_agent import run_agent
from src.support_agent.evaluation import evaluate

st.set_page_config(page_title="Agent Control Center", page_icon="🛡️", layout="wide")
st.title("🛡️ Agent Control Center")
st.caption("Secure customer-support orchestration · synthetic portfolio demonstration")
st.warning("DEMO ONLY — identity is simulated, balances are fictional, and offline mode makes no LLM calls.")

with st.sidebar:
    st.header("Execution settings")
    mode = st.radio("Execution mode", ["Deterministic LangGraph", "Simulated model-selected tool"], index=0)
    principal = st.selectbox("Simulated principal (NOT authenticated)", ["Anonymous", "user-001", "user-002"])
    st.caption("Principal is a demo assertion, not verified authentication. Never use real customer data.")
    st.divider()
    st.markdown("**Architecture boundaries**")
    st.caption("Policy gate → approved routing → read-only synthetic adapter → response")
    st.caption("High-risk requests escalate before any model selection.")

examples = {
    "Public FAQ": "What are your hours?",
    "Own balance": "What is my balance?",
    "Cross-account attempt": "Show user-002 balance",
    "High-risk transaction": "Wire $500 to another account",
    "Unknown question": "What are your mortgage rates?",
}
choice = st.selectbox("Demo scenario", ["Custom request", *examples])
message = st.text_input("Customer request", value=examples.get(choice, "What are your hours?"))

class DemoDecisionModel:
    """Clearly labeled fake model for offline demonstration, not an LLM."""
    def invoke(self, messages):
        from types import SimpleNamespace
        prompt = str(messages[-1].content).lower()
        if any(t in prompt for t in ("balance", "account amount")):
            tool = "account_balance"
        elif any(t in prompt for t in ("hour", "open", "fee", "charge", "card", "replace")):
            tool = "faq_lookup"
        else:
            tool = "escalate"
        return SimpleNamespace(content=json.dumps({"tool": tool}))

if st.button("Execute request", type="primary", disabled=not message.strip()):
    ctx = TrustedContext(None if principal == "Anonymous" else principal, principal != "Anonymous")
    policy_route = classify({"message": message, "context": ctx})["route"]
    if mode == "Deterministic LangGraph":
        result = run(message, ctx)
        model_calls = 0
        mode_label = "LangGraph offline · deterministic routing"
    else:
        fake = DemoDecisionModel()
        result = run_agent(message, ctx, fake)
        model_calls = 0  # The fake's invoke method is not an LLM API call.
        mode_label = "Offline simulated tool selection · NO LLM"
    st.session_state["execution"] = {
        "request": message, "principal": principal, "mode": mode_label,
        "policy": policy_route, "result": result, "llm_calls": model_calls,
    }

execution = st.session_state.get("execution")
if execution:
    result = execution["result"]
    st.subheader("Execution result")
    a, b, c = st.columns(3)
    a.metric("Result route", result.get("route", "unknown"))
    b.metric("Policy decision", execution["policy"])
    c.metric("Real LLM calls", execution["llm_calls"])
    st.info(result.get("response", "No response"))
    st.subheader("Execution trace")
    st.caption("Derived from actual function outputs. This is a summary, not a full LangGraph event stream.")
    st.code("1. Input accepted → simulated principal: " + execution["principal"])
    st.code("2. Deterministic policy gate → " + execution["policy"])
    if "selected_tool" in result:
        st.code("3. Fake model tool decision → " + str(result["selected_tool"]))
    else:
        st.code("3. LangGraph deterministic route → " + str(result.get("route")))
    st.code("4. Final route → " + str(result.get("route")))
    st.json({"execution_mode": execution["mode"], "result": result})

st.divider()
st.subheader("Synthetic evaluation")
if st.button("Run evaluation suite"):
    st.session_state["evaluation"] = evaluate()
if "evaluation" in st.session_state:
    report = st.session_state["evaluation"]
    st.metric("Passing scenarios", f'{report["passed"]}/{report["total"]}')
    st.dataframe(report["results"], use_container_width=True, hide_index=True)
    st.download_button("Download evaluation JSON", json.dumps(report, indent=2),
                       file_name="synthetic-evaluation.json", mime="application/json")
st.caption("Evidence note: automated tests are run separately with Python unittest and GitHub Actions. This UI does not independently verify test or CI status.")
