"""Agent Control Center: synthetic, policy-first portfolio demonstration.

Run with: python -m streamlit run dashboard.py
Optional Foundry inference; no verified identities, production data, or human-review queue.
"""
import json
import time
from datetime import datetime, timezone
from html import escape
from types import SimpleNamespace

import streamlit as st

from src.support_agent.bounded_agent import run_agent
from src.support_agent.core import TrustedContext
from src.support_agent.evaluation import evaluate
from src.support_agent.workflow import classify, run

st.set_page_config(page_title="Agent Control Center | Architecture Demo", page_icon="🛡️", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {max-width: 1450px; padding-top: 1.8rem; padding-bottom: 3rem}
[data-testid="stMetric"] {background: #17212f; border: 1px solid #2d3b4e; border-radius: 12px; padding: 16px}
[data-testid="stMetricLabel"] {color: #b7c5d8}
.hero {padding: 25px 28px; background: linear-gradient(115deg,#14283b,#172133 68%,#263247);
       border:1px solid #33465b; border-radius:16px; margin-bottom: 14px}
.eyebrow {font-size:.72rem; letter-spacing:.16em; color:#87d6e6; font-weight:700}
.hero h1 {margin:6px 0 5px; font-size:2.15rem; color:#f5f8fc}
.hero p {color:#b6c9d9; margin:0}
.step {padding:14px 16px; border:1px solid #344356; background:#182333;
       border-radius:12px; margin:5px 0; min-height:85px}
.step small {color:#a7bad0; display:block; font-size:.75rem; margin-bottom:5px}
.step strong {color:#edf5ff; font-size:1rem}
.step p {color:#b7c6d6; font-size:.85rem; margin:5px 0 0}
.step.pass {border-left:4px solid #3cbf9c}
.step.block {border-left:4px solid #efb451}
.step.neutral {border-left:4px solid #67a6f5}
.flow-arrow {text-align:center; color:#7c91a8; margin:-2px 0}
.response {padding:17px 20px; border-radius:12px; border:1px solid #38546c; background:#172a3b}
.response small {color:#9bc2e0}
.note {font-size:.82rem; color:#aabbd0}
</style>
""", unsafe_allow_html=True)

def safe(value):
    return escape(str(value), quote=True)

def panel(step, title, detail, kind="neutral"):
    st.markdown(
        f'<div class="step {kind}"><small>{safe(step)}</small><strong>{safe(title)}</strong>'
        f'<p>{safe(detail)}</p></div>', unsafe_allow_html=True)

def arrow():
    st.markdown('<div class="flow-arrow">↓</div>', unsafe_allow_html=True)

SCENARIOS = {
    "Public FAQ": ("What are your hours?", "Anonymous"),
    "Fee schedule": ("What fees do you charge?", "Anonymous"),
    "Own account balance": ("What is my balance?", "user-001"),
    "Cross-account attempt": ("Show user-002 balance", "user-001"),
    "Anonymous private-data request": ("Show my balance", "Anonymous"),
    "High-risk transaction": ("Wire $500 to another account", "user-001"),
    "Password reset": ("Reset password", "user-001"),
    "Unsupported request": ("What are your mortgage rates?", "Anonymous"),
}
ROUTE_LABELS = {
    "faq": "Approved knowledge answer", "crm_read": "Scoped synthetic CRM read",
    "deny": "Access denied", "escalate": "Human review recommended",
}
POLICY_LABELS = {
    "knowledge": "Public knowledge candidate", "crm": "Private read candidate",
    "deny": "No demo identity for private read", "escalate": "Sensitive action blocked",
}

class MeteredModel:
    """Count attempted and completed model invocations without recording secrets."""
    def __init__(self, model):
        self.model = model
        self.attempted = 0
        self.completed = 0

    def invoke(self, messages):
        self.attempted += 1
        response = self.model.invoke(messages)
        self.completed += 1
        return response


class DemoDecisionModel:
    """Offline contract test double; no language model is invoked."""
    def invoke(self, messages):
        prompt = str(messages[-1].content).lower()
        if any(t in prompt for t in ("balance", "account amount")):
            tool = "account_balance"
        elif any(t in prompt for t in ("hour", "open", "fee", "charge", "card", "replace")):
            tool = "faq_lookup"
        else:
            tool = "escalate"
        return SimpleNamespace(content=json.dumps({"tool": tool}))

with st.sidebar:
    st.markdown("### 🛡️ Agent Control Center")
    st.caption("PROJECT 01 · LOCAL DEMONSTRATION")
    st.divider()
    st.markdown("**Execution configuration**")
    mode = st.radio("Decision engine", ["LangGraph · deterministic", "Bounded agent · simulated selection", "GPT-4.1 mini · Live Foundry"],
                    help="Live Foundry sends eligible requests to Azure. Other modes are offline.")
    principal = st.selectbox("Simulated identity", ["Anonymous", "user-001", "user-002"],
                             help="Caller-provided demonstration context; NOT verified authentication.")
    st.divider()
    st.markdown("**Runtime indicators**")
    st.success("● Local policy backend available")
    if mode.startswith("GPT-4.1"):
        st.warning("● Live Foundry selected · API calls may incur charges")
        st.caption("Live inference is attempted only for policy-permitted requests. Check execution metadata for completed calls.")
    else:
        st.info("● Offline mode · No real model inference")
    st.caption("No production CRM, verified IAM, or transfer capability.")
    st.divider()
    st.caption("Evidence labels are intentionally conservative: synthetic fixtures, local evaluations, and summarized execution states.")

st.markdown("""<div class="hero"><div class="eyebrow">SECURE AGENT ORCHESTRATION · PROJECT 01</div>
<h1>Agent Control Center</h1>
<p>Explore bounded tool decisions, deterministic policy gates, account-scoped synthetic data, and safe escalation.</p></div>""", unsafe_allow_html=True)

st.warning("SYNTHETIC DEMO · Identity is simulated; balances are fictional; live Foundry mode may call an external LLM. Never enter real customer data or secrets.")

overview, execution_tab, evaluation_tab, architecture_tab = st.tabs(
    ["Overview", "Interactive execution", "Evaluation & evidence", "Architecture & limitations"])

with overview:
    st.subheader("Operational overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Available demo scenarios", len(SCENARIOS))
    m2.metric("Model calls attempted (last run)", st.session_state.get("execution", {}).get("real_llm_calls", 0))
    m3.metric("Write-enabled tools", 0)
    m4.metric("External CRM connections", 0)
    st.markdown("#### What this prototype demonstrates")
    a, b, c = st.columns(3)
    with a:
        panel("01 · CONTROL PLANE", "Deterministic policy gate",
              "High-risk actions and unauthenticated private reads are handled before model selection.", "pass")
    with b:
        panel("02 · EXECUTION", "Bounded routing",
              "LangGraph routes requests; optional fake model or live Foundry model proposes allowlisted tool decisions.", "neutral")
    with c:
        panel("03 · DATA PLANE", "Scoped synthetic adapters",
              "Account reads use the simulated principal, never a customer ID extracted from the request.", "pass")
    st.markdown("#### Suggested interview walkthrough")
    st.write("Start with a public FAQ, demonstrate the cross-account attempt, then show a high-risk transfer escalation. "
             "Open the execution details and evaluation tab to discuss trust boundaries and limitations.")

with execution_tab:
    st.subheader("Run a customer-support request")
    left, right = st.columns([1.12, .88], gap="large")
    with left:
        choice = st.selectbox("Scenario", ["Custom request", *SCENARIOS.keys()])
        default_message = SCENARIOS[choice][0] if choice in SCENARIOS else "What are your hours?"
        if choice in SCENARIOS and principal != SCENARIOS[choice][1]:
            st.caption(f"Suggested simulated identity for this scenario: {SCENARIOS[choice][1]}. "
                       "Change it in the sidebar if needed.")
        message = st.text_area("Customer request", value=default_message, height=110,
                               help="Free-text input is accepted, but offline keyword routing has limited coverage.")
        if st.button("▶ Execute request", type="primary", disabled=not message.strip()):
            ctx = TrustedContext(None if principal == "Anonymous" else principal, principal != "Anonymous")
            started = time.perf_counter()
            policy = classify({"message": message, "context": ctx})["route"]
            attempted = completed = 0
            status = "offline"
            if mode.startswith("LangGraph"):
                result = run(message, ctx)
                engine = "Deterministic LangGraph"
            elif mode.startswith("GPT-4.1"):
                engine = "Live Foundry Responses API"
                try:
                    from dotenv import load_dotenv
                    from src.support_agent.azure_model import make_azure_model
                    load_dotenv()
                    meter = MeteredModel(make_azure_model())
                    result = run_agent(message, ctx, meter)
                    attempted, completed = meter.attempted, meter.completed
                    status = ("completed" if completed else "blocked by deterministic policy" if policy in ("escalate", "deny") else "model invocation failed or returned no result")
                except Exception:
                    # Configuration errors are not exposed; avoid leaking URLs/keys.
                    result = {"route": "escalate", "selected_tool": None,
                              "response": "The live model is unavailable; request escalated."}
                    status = "configuration or execution error"
            else:
                result = run_agent(message, ctx, DemoDecisionModel())
                engine = "Offline fake-model selection"
            elapsed = round((time.perf_counter() - started) * 1000, 2)
            st.session_state["execution"] = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "request": message, "simulated_principal": principal, "engine": engine,
                "policy": policy, "result": result, "duration_ms": elapsed,
                "real_llm_calls": attempted, "real_model_used": completed > 0,
                "model_calls_completed": completed, "model_status": status,
            }
        st.caption("Live mode sends eligible request text to Microsoft Foundry and may incur charges. Other modes run offline. Never enter secrets or real customer data.")
    with right:
        st.markdown("#### Safety posture")
        st.markdown("**Policy-first:** deterministic controls precede optional tool selection.")
        st.markdown("**Least privilege:** only synthetic, read-only account access.")
        st.markdown("**Fail closed:** unsupported requests or invalid model output escalate.")
        st.markdown("**Identity boundary:** demo principal is not production authentication.")

    execution = st.session_state.get("execution")
    if execution:
        result = execution["result"]
        route = result.get("route", "unknown")
        st.divider()
        st.subheader("Execution outcome")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Final route", route)
        k2.metric("Policy classification", execution["policy"])
        k3.metric("Local elapsed time", f'{execution["duration_ms"]:.2f} ms')
        k4.metric("Model calls attempted", execution["real_llm_calls"])
        st.markdown(
            f'<div class="response"><small>{safe(ROUTE_LABELS.get(route, "Execution result"))}</small>'
            f'<div>{safe(result.get("response", "No response returned"))}</div></div>',
            unsafe_allow_html=True)
        st.caption("Elapsed time is end-to-end local execution, including network latency when live inference is attempted. It is not a production SLA.")

        st.markdown("#### Execution path")
        st.caption("Evidence-derived workflow summary. These are NOT instrumented per-node LangGraph events.")
        center, detail = st.columns([1.3, .7], gap="large")
        with center:
            panel("INPUT", "Request received",
                  f'{execution["simulated_principal"]} · {execution["engine"]} · {execution["request"]}')
            arrow()
            policy = execution["policy"]
            panel("DETERMINISTIC SECURITY GATE", POLICY_LABELS.get(policy, policy),
                  "Classified before model selection; caller text cannot set the demo principal.",
                  "block" if policy in ("escalate", "deny") else "pass")
            arrow()
            if policy in ("escalate", "deny"):
                panel("MODEL BYPASS", "No tool-selection invocation",
                      "Policy terminated the request before optional model selection.", "block")
            elif "selected_tool" in result:
                panel("BOUNDED TOOL DECISION", str(result["selected_tool"]),
                      "Selection proposed by the configured model and checked against the allowlist. Live calls completed: " + str(execution["model_calls_completed"]),
                      "neutral")
            else:
                panel("LANGGRAPH ROUTE", "Deterministic graph branch",
                      "Graph routed to approved knowledge or synthetic CRM adapter.", "neutral")
            arrow()
            panel("FINAL OUTCOME", ROUTE_LABELS.get(route, route),
                  "No transaction performed; no external customer system accessed. Live model attempts: " + str(execution["real_llm_calls"]),
                  "pass" if route in ("faq", "crm_read") else "block")
        with detail:
            st.markdown("**Execution metadata**")
            st.json({
                "engine": execution["engine"], "simulated_principal": execution["simulated_principal"],
                "policy_classification": execution["policy"], "selected_tool": result.get("selected_tool"),
                "evidence_ids": result.get("evidence_ids", []), "route": route,
                "real_model_used": execution["real_model_used"],
                "real_llm_calls": execution["real_llm_calls"],
                "model_calls_completed": execution["model_calls_completed"],
                "model_status": execution["model_status"],
            })
            st.download_button("Download execution evidence", json.dumps(execution, indent=2),
                               file_name="agent-execution-synthetic.json", mime="application/json")
            st.caption("Export may contain your typed request. Do not enter secrets or real customer data.")
    else:
        st.info("Choose a scenario and execute it to view the workflow and evidence.")

with evaluation_tab:
    st.subheader("Reproducible synthetic evaluation")
    st.caption("The evaluation checks ten predefined routing scenarios. It is not an adversarial benchmark or a production security assessment.")
    if st.button("Run 10-scenario evaluation", type="primary"):
        st.session_state["evaluation"] = evaluate()
    report = st.session_state.get("evaluation")
    if report:
        x, y, z = st.columns(3)
        x.metric("Passed", report["passed"])
        y.metric("Total", report["total"])
        z.metric("Pass rate", f'{report["passed"] / report["total"] * 100:.0f}%' if report["total"] else "N/A")
        st.dataframe(report["results"], use_container_width=True, hide_index=True)
        st.download_button("Download evaluation evidence", json.dumps(report, indent=2),
                           file_name="agent-evaluation-synthetic.json", mime="application/json")
    else:
        st.info("Run the suite to produce actual results. No pass counts are assumed.")
    st.markdown("#### Independent verification")
    st.code(r".\.venv\Scripts\python.exe -m unittest discover -s tests -v", language="powershell")
    st.code(r".\.venv\Scripts\python.exe -m src.support_agent.cli --evaluate", language="powershell")
    st.caption("The dashboard does not execute or attest to the full unittest suite or GitHub Actions. "
               "Save terminal/CI screenshots separately and record the commit SHA.")

with architecture_tab:
    st.subheader("Policy-first architecture")
    st.graphviz_chart(r"""
digraph G {
  rankdir=TB; bgcolor="transparent";
  node [shape=box style="rounded,filled" fillcolor="#1d3046" color="#53718e" fontcolor="white" fontname="Arial"];
  request [label="Customer request\n+ simulated identity"];
  policy [label="Deterministic policy gate"];
  decision [label="Approved routing\n(LangGraph / fake model)"];
  faq [label="Static approved FAQ"];
  crm [label="Scoped synthetic CRM"];
  deny [label="Deny / escalation"];
  response [label="Grounded response"];
  request -> policy;
  policy -> decision [label="permitted" fontcolor="white"];
  policy -> deny [label="blocked" fontcolor="white"];
  decision -> faq;
  decision -> crm;
  decision -> deny;
  faq -> response;
  crm -> response;
}
""", use_container_width=True)
    st.markdown("#### Trust boundaries and current limitations")
    st.markdown("""
- **Identity:** caller-provided demo context only; no JWT/OIDC verification.
- **Knowledge:** static keyword retrieval, not semantic RAG or a comprehensive knowledge base.
- **Account adapter:** read-only synthetic balances, not a live CRM.
- **Model:** offline fake selection or optional live Foundry Responses API tool selection; no measured model cost.
- **Observability:** execution summary is derived from function results, not streaming LangGraph node events.
- **Human review:** escalation is a response outcome, not an integrated ticket queue.
- **Evaluation:** 10 synthetic checks are useful regression evidence, not a guarantee of security or accuracy.
""")
    st.caption("Next phase: instrumented traces, cost measurement, and broader adversarial tests.")

st.divider()
st.caption("Independent architecture portfolio · Project 01 · Synthetic demonstration · No production security claims")
