"""Agent Control Center: synthetic, policy-first portfolio demonstration.

Run with: python -m streamlit run dashboard.py
Optional Foundry inference; no verified identities, production data, or human-review queue.
"""
import json
import time
from datetime import datetime, timezone
from html import escape

import streamlit as st

from src.support_agent.agent_v2 import run_v2, plan
from src.support_agent.core import TrustedContext
from src.support_agent.integrations import DOCUMENTS
from src.support_agent.evaluation import evaluate
from src.support_agent.workflow import classify, run

st.set_page_config(page_title="Agent Control Center | Enterprise AI Portfolio", page_icon="◈", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
.block-container {max-width: 1320px; padding-top: 2.3rem; padding-bottom: 3rem}
[data-testid="stSidebar"] {background: #111923}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {line-height: 1.45}
[data-testid="stTabs"] [data-baseweb="tab"] {font-weight: 600; padding: 13px 18px}
[data-testid="stTabs"] [aria-selected="true"] {color: #7dd3fc}
h2, h3 {letter-spacing: -.025em}
div[data-testid="stAlert"] {border-radius: 10px}
.portfolio-meta {display:flex; gap:9px; flex-wrap:wrap; margin-top:18px}
.portfolio-chip {border:1px solid #36526b; border-radius:6px; padding:6px 10px; color:#bcd3e6; font-size:.77rem; font-weight:600}
.portfolio-section {font-size:.72rem; font-weight:700; letter-spacing:.14em; color:#86a8c5; margin:8px 0 15px}
.portfolio-note {font-size:.82rem; color:#91a6ba; margin-top:12px}
.portfolio-divider {border-top:1px solid #27394b; margin:22px 0}
[data-testid="stMetric"] {background: #17212f; border: 1px solid #2d3b4e; border-radius: 12px; padding: 16px}
[data-testid="stMetricLabel"] {color: #b7c5d8}
.hero {padding: 34px 38px; background: linear-gradient(115deg,#12263a,#15283b 68%,#20354b);
       border:1px solid #33465b; border-radius:16px; margin-bottom: 14px}
.eyebrow {font-size:.72rem; letter-spacing:.16em; color:#87d6e6; font-weight:700}
.hero h1 {margin:6px 0 5px; font-size:2.5rem; letter-spacing:-.04em; color:#f5f8fc}
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
.arch-heading {margin:18px 0 26px; max-width:850px}
.arch-kicker {color:#70c9ed; font-size:.73rem; letter-spacing:.14em; font-weight:800; margin-bottom:9px}
.arch-heading h3 {font-size:1.55rem; color:#f4f8ff; margin:0 0 8px}
.arch-heading p {color:#b8cce0; font-size:.93rem; line-height:1.65; margin:0}
.arch-node {display:flex; align-items:flex-start; gap:18px; padding:20px 23px; background:#17283a;
 border:1px solid #42617c; border-left:4px solid #5aa9e2; border-radius:12px; min-height:105px}
.arch-node.arch-warning {border-left-color:#e6ac63; background:#30271f}
.arch-node.arch-success {border-left-color:#54c9aa}
.arch-index {font-size:.76rem; font-weight:800; color:#9ddaff; background:#254059; border-radius:7px;
 padding:8px 11px; white-space:nowrap}
.arch-title {font-size:1.03rem; font-weight:750; color:#f1f7ff; margin-bottom:6px}
.arch-detail {font-size:.88rem; color:#b7ccdf; line-height:1.6}
.arch-connector {height:54px; display:flex; align-items:center; justify-content:center; flex-direction:column;
 color:#a8bfd3; font-size:.73rem; font-weight:650; letter-spacing:.03em}
.arch-line {height:14px; width:2px; background:#5d8bad}
.arch-chevron {font-size:.8rem; color:#82b5db; line-height:1.1}
.arch-outcome {padding:19px 21px; border:1px solid #3c766a; border-left:4px solid #57c9a5;
 background:#152d2b; border-radius:11px; min-height:110px}
.arch-outcome.arch-warning {border-color:#896749; border-left-color:#e6ad68; background:#302720}
.arch-outcome strong {font-size:.99rem; color:#f1f7ff}
.arch-outcome p {font-size:.84rem; color:#c2d2df; line-height:1.6; margin:7px 0 0}
.arch-section-label {font-size:.76rem; color:#91b6d1; letter-spacing:.1em; font-weight:800; margin:22px 0 11px}
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

def architecture_stage(number, heading, detail, tone="neutral"):
    """Readable, responsive architecture component with explicit trust-boundary cues."""
    st.markdown(
        f'<div class="arch-node arch-{safe(tone)}">'
        f'<span class="arch-index">{safe(number)}</span>'
        f'<div><div class="arch-title">{safe(heading)}</div>'
        f'<div class="arch-detail">{safe(detail)}</div></div></div>',
        unsafe_allow_html=True,
    )


def architecture_connector(label=""):
    caption = f'<span>{safe(label)}</span>' if label else ""
    st.markdown(f'<div class="arch-connector"><div class="arch-line"></div>{caption}'
                '<div class="arch-chevron">▼</div></div>', unsafe_allow_html=True)


def architecture_outcome(title, detail, tone="success"):
    st.markdown(f'<div class="arch-outcome arch-{safe(tone)}">'
                f'<strong>{safe(title)}</strong><p>{safe(detail)}</p></div>',
                unsafe_allow_html=True)


def architecture_heading(kicker, title, description):
    st.markdown(f'<div class="arch-heading"><div class="arch-kicker">{safe(kicker)}</div>'
                f'<h3>{safe(title)}</h3><p>{safe(description)}</p></div>',
                unsafe_allow_html=True)


SCENARIOS = {
    "Public FAQ": ("What are your hours?", "Anonymous"),
    "Fee schedule": ("What fees do you charge?", "Anonymous"),
    "Lost card guidance": ("I lost my card. What should I do?", "Anonymous"),
    "Account statements": ("How can I view my statements?", "Anonymous"),
    "Direct deposit": ("How does direct deposit work?", "Anonymous"),
    "Payment timing": ("What are payment processing times?", "Anonymous"),
    "Opening an account": ("How can I open an account?", "Anonymous"),
    "Support contact": ("How do I contact support?", "Anonymous"),
    "Online access": ("I have an online login issue", "Anonymous"),
    "ATM limits": ("What are the ATM withdrawal limits?", "Anonymous"),
    "Transaction disputes": ("How do I dispute a transaction?", "Anonymous"),
    "Card replacement": ("How do I replace a damaged card?", "Anonymous"),
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
    "multi": "Multiple approved tools", "session_info": "Simulated session identity",
}
POLICY_LABELS = {
    "knowledge": "Public knowledge candidate", "crm": "Private read candidate",
    "deny": "Private data access blocked", "escalate": "Sensitive action blocked",
    "allow": "Approved bounded intents",
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


with st.sidebar:
    st.markdown("### ◈ Agent Architecture Lab")
    project = st.selectbox("Project workspace", [
        "01 · Secure Customer Service",
        "02 · Intelligent Document Processing",
        "03 · Enterprise Agent Platform",
    ], key="portfolio_project")
    st.caption("Enterprise AI engineering portfolio")
    st.divider()
    if project.startswith("01"):
        st.markdown("**Runtime configuration**")
        mode = st.radio("Execution mode", ["AI Agent · Azure Foundry", "Deterministic Baseline"],
                        help="AI Agent uses GPT-4.1 mini for approved requests. Baseline runs without an LLM.")
        st.caption("**AI Agent:** multi-intent tool execution with GPT-4.1 mini." if mode.startswith("AI Agent")
                   else "**Baseline:** deterministic LangGraph routing without model inference.")
        principal = st.selectbox("Simulated identity", ["Anonymous", "user-001", "user-002"],
                                 help="Caller-provided demonstration context; NOT verified authentication.")
        st.divider()
        st.markdown("**Environment**")
        st.caption("● Policy engine · Local")
        st.caption("● Inference · " + ("Azure Foundry · on demand" if mode.startswith("AI Agent") else "Offline · no model calls"))
        st.caption("● Data · Synthetic, read-only")
        st.divider()
        st.caption("Independent portfolio · No production data")

if project.startswith("01"):
    st.markdown("""<div class="hero">
    <div class="eyebrow">PROJECT 01 / SECURE AGENT ORCHESTRATION</div>
    <h1>Customer Service Agent</h1>
    <p>Policy-governed AI orchestration with Azure AI Foundry, LangGraph, and scoped tool execution.</p>
    <div class="portfolio-meta">
      <span class="portfolio-chip">FUNCTIONAL PROTOTYPE</span>
      <span class="portfolio-chip">GPT-4.1 mini</span>
      <span class="portfolio-chip">READ-ONLY TOOLS</span>
      <span class="portfolio-chip">SYNTHETIC DATA</span>
    </div></div>""", unsafe_allow_html=True)

    st.caption("Demonstration environment · Simulated identity and fictional account data · Do not enter real customer information.")

    overview, execution_tab, evaluation_tab, architecture_tab = st.tabs(
        ["Overview", "Agent execution", "Evaluation", "Architecture"])

    with overview:
        st.markdown('<div class="portfolio-section">SYSTEM AT A GLANCE</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("AI model", "GPT-4.1 mini")
        m2.metric("Tool permissions", "Read-only")
        m3.metric("Knowledge base", f"{len(DOCUMENTS)} FAQs")
        m4.metric("Evaluation suite", "10 checks")
        st.caption("Knowledge records are fictional. The AI model is called only when a permitted request is executed in live mode.")
        st.markdown('<div class="portfolio-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="portfolio-section">ARCHITECTURAL CONTROLS</div>', unsafe_allow_html=True)
        a, b, c = st.columns(3, gap="medium")
        with a:
            panel("01 / POLICY ENFORCEMENT", "Deterministic authorization",
                  "Risk screening and account-scope checks run before any LLM call.", "pass")
        with b:
            panel("02 / AGENT EXECUTION", "Bounded orchestration",
                  "Approved FAQ, balance, and session tools; multi-intent execution in v2.", "neutral")
        with c:
            panel("03 / SAFE OUTCOMES", "Fail-closed behavior",
                  "Unauthorized, unsupported, or high-risk requests are denied or escalated.", "pass")
        st.markdown('<div class="portfolio-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="portfolio-section">VALIDATED CAPABILITIES</div>', unsafe_allow_html=True)
        left_cap, right_cap = st.columns(2, gap="large")
        with left_cap:
            st.markdown("**Customer assistance**")
            st.markdown("✓ Approved knowledge retrieval · Scoped synthetic balance lookup · Multi-intent requests")
        with right_cap:
            st.markdown("**Governance & assurance**")
            st.markdown("✓ Cross-account blocking · Pre-inference risk screening · Execution metadata and reproducible tests")
        st.caption("Scope: working synthetic prototype. Identity is not externally verified; no production CRM, transactions, or staffed escalation integration.")

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
            if not message.strip():
                st.info("Enter a request before executing. Blank requests do not call the model.")
            if st.button("▶ Execute request", type="primary", disabled=not message.strip()):
                ctx = TrustedContext(None if principal == "Anonymous" else principal, principal != "Anonymous")
                started = time.perf_counter()
                policy = (plan(message, ctx)["policy"] if mode.startswith("AI Agent")
                          else classify({"message": message, "context": ctx})["route"])
                attempted = completed = 0
                status = "offline"
                if mode.startswith("Deterministic"):
                    result = run(message, ctx)
                    engine = "Deterministic LangGraph"
                elif mode.startswith("AI Agent"):
                    engine = "Azure Foundry · GPT-4.1 mini · Agent v2"
                    try:
                        from dotenv import load_dotenv
                        from src.support_agent.azure_model import make_azure_model
                        load_dotenv()
                        meter = MeteredModel(make_azure_model())
                        result = run_v2(message, ctx, meter)
                        attempted, completed = meter.attempted, meter.completed
                        status = ("completed" if completed else "blocked by deterministic policy" if policy in ("escalate", "deny") or (mode.startswith("AI Agent") and result.get("route") == "session_info") else "model invocation failed or returned no result")
                    except Exception:
                        # Configuration errors are not exposed; avoid leaking URLs/keys.
                        result = {"route": "escalate", "selected_tool": None,
                                  "response": "The live model is unavailable; request escalated."}
                        status = "configuration or execution error"
                elapsed = round((time.perf_counter() - started) * 1000, 2)
                st.session_state["execution"] = {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "request": message, "simulated_principal": principal, "engine": engine,
                    "policy": policy, "result": result, "duration_ms": elapsed,
                    "real_llm_calls": attempted, "real_model_used": completed > 0,
                    "model_calls_completed": completed, "model_status": status,
                }
            st.caption("AI Agent mode sends approved request text to Azure Foundry and may incur charges. Baseline mode is offline. Use synthetic data only.")
        with right:
            st.markdown("#### Execution safeguards")
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
            st.caption("Application-derived policy and tool decisions; not distributed tracing or per-node LangGraph telemetry.")
            if result.get("steps"):
                with st.expander("View recorded agent decisions", expanded=False):
                    st.dataframe(result["steps"], use_container_width=True, hide_index=True)
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
                      "pass" if route in ("faq", "crm_read", "multi", "session_info") else "block")
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
        st.caption("Ten deterministic baseline routing checks. This does not benchmark GPT-4.1 mini or certify production security.")
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
        st.subheader("System architecture")
        st.caption("Policy-controlled tool access. Model output cannot grant account permissions or execute financial transactions.")
        architecture_heading("TRUST BOUNDARIES / PROJECT 01", "Policy-first agent orchestration",
                             "The application enforces request policy before optional model inference. Model decisions are constrained to allowlisted, read-only tools.")
        architecture_stage("01", "Customer request + simulated session", "Untrusted message text and caller-selected demo principal. No verified sign-in.")
        architecture_connector("request enters deterministic boundary")
        architecture_stage("02", "Pre-inference policy gate", "High-risk operation screening, cross-account pattern checks and anonymous private-data denial.", "warning")
        architecture_connector("only approved requests proceed")
        architecture_stage("03", "Bounded agent execution", "GPT-4.1 mini chooses approved tools in live mode; the offline LangGraph baseline routes deterministically.")
        architecture_connector("read-only capability boundary")
        st.markdown('<div class="arch-section-label">AUTHORIZED DATA SOURCES</div>', unsafe_allow_html=True)
        col_faq, col_balance, col_session = st.columns(3, gap="medium")
        with col_faq:
            architecture_outcome("Approved FAQ retrieval", f"{len(DOCUMENTS)} synthetic knowledge records with evidence IDs.")
        with col_balance:
            architecture_outcome("Scoped account read", "Synthetic balance adapter always uses the session principal.")
        with col_session:
            architecture_outcome("Session information", "Returns simulated caller identity without private account lookup.")
        st.markdown('<div class="arch-section-label">SAFE TERMINATION</div>', unsafe_allow_html=True)
        architecture_outcome("Deny / escalate", "Rejected policy decisions never reach the model; invalid tool decisions and outages fail closed.", "warning")
        st.markdown("#### Component responsibilities")
        st.table({
            "Component": ["Policy gate", "AI orchestration", "Knowledge source",
                          "Account data", "Session identity", "Safe fallback"],
            "Responsibility": [
                "Screens high-risk requests and enforces account scope before inference.",
                "Selects bounded tools and handles approved multi-intent requests.",
                f"Retrieves answers from {len(DOCUMENTS)} fictional, approved FAQ records.",
                "Returns read-only synthetic balances for the simulated caller.",
                "Displays caller-provided demo identity; no real sign-in or IAM.",
                "Denies unauthorized access or recommends human review.",
            ],
        })
        with st.expander("Prototype boundaries and production considerations"):
            st.markdown("""
            - **Identity:** simulated session only; production requires verified authentication and authorization.
            - **Knowledge:** keyword-matched static FAQs; not semantic retrieval.
            - **Account data:** fictional balances; no external CRM or banking integration.
            - **Human review:** escalation is a response outcome, not a staffed ticket queue.
            - **Observability:** execution summaries are not instrumented distributed traces.
            - **Evaluation:** ten predefined scenarios; not a production security certification.
            """)

    st.divider()
    st.caption("Independent architecture portfolio · Project 01 · Synthetic demonstration · No production security claims")

else:
    if project.startswith("02"):
        from src.document_processing.pipeline import IntakeEngine, SAMPLES, TYPES
        st.markdown("""<div class="hero"><div class="eyebrow">PROJECT 02 / DOCUMENT INTELLIGENCE</div>
        <h1>Intelligent Document Processing</h1>
        <p>Deterministic supplier intake, field-level evidence, validation, human-review gates and idempotent staging.</p>
        <div class="portfolio-meta"><span class="portfolio-chip">FUNCTIONAL OFFLINE PROTOTYPE</span>
        <span class="portfolio-chip">SYNTHETIC DOCUMENTS</span>
        <span class="portfolio-chip">REVIEW GATES</span></div></div>""", unsafe_allow_html=True)
        st.caption("Local text-only fixtures. No OCR, Azure Document Intelligence, live ERP, external queue or real supplier records.")
        if "doc_engine" not in st.session_state:
            st.session_state["doc_engine"] = IntakeEngine()
        engine = st.session_state["doc_engine"]
        overview, execute, architecture = st.tabs(["Overview", "Document execution", "Architecture"])
        with overview:
            a,b,c = st.columns(3)
            a.metric("Supported document types", len(TYPES))
            b.metric("Synthetic fixtures", len(SAMPLES))
            c.metric("Staged in this session", engine.staged_count())
            st.markdown("**Processing contract:** classify → extract labeled fields with line evidence → validate vendor/schema → stage or request review.")
            st.markdown("**Approval control:** bank-account details require explicit simulated reviewer approval; invalid records cannot be approved.")
            st.markdown("**Idempotency:** tenant + document content hash identifies repeat submissions within the current process.")
        with execute:
            doc_mode = st.radio("Extraction mode", ["Deterministic offline", "AI-assisted · Azure Foundry"], horizontal=True, key="p2_mode")
            choice = st.selectbox("Document fixture", ["Custom document", *SAMPLES.keys()])
            sample = SAMPLES.get(choice, SAMPLES["Valid invoice"])
            tenant = st.selectbox("Simulated tenant", ["demo-tenant", "tenant-a", "tenant-b"])
            content = st.text_area("Synthetic text document", value=sample, height=200)
            if st.button("Process document", type="primary"):
                try:
                    if doc_mode.startswith("AI-assisted"):
                        from dotenv import load_dotenv
                        from src.support_agent.structured_inference import configured_model
                        load_dotenv()
                        st.session_state["doc_result"] = engine.process(content, tenant, model=configured_model())
                    else:
                        st.session_state["doc_result"] = engine.process(content, tenant)
                except (ValueError, RuntimeError, TimeoutError) as exc:
                    st.error("Processing failed safely: " + str(exc))
            result = st.session_state.get("doc_result")
            if result:
                st.subheader("Processing outcome")
                st.metric("Status", result["status"].replace("_", " ").title())
                st.caption("Execution mode: " + result.get("mode", "offline"))
                st.caption("Workflow ID: " + result["workflow_id"] + (" · duplicate submission" if result["duplicate"] else ""))
                left, right = st.columns(2)
                with left:
                    st.markdown("**Extracted fields**")
                    st.json(result["fields"])
                with right:
                    st.markdown("**Source-line evidence**")
                    st.json(result["evidence"])
                if result["issues"]:
                    st.warning("Review/validation issues: " + ", ".join(result["issues"]))
                if result["status"] == "needs_review":
                    reviewer = st.text_input("Simulated reviewer", value="reviewer-01")
                    if st.button("Approve reviewable record"):
                        try:
                            st.session_state["doc_result"] = engine.approve(result["workflow_id"], reviewer, tenant)
                            st.success("Approved for synthetic in-memory staging; no ERP write occurred.")
                        except (ValueError, KeyError, PermissionError) as exc:
                            st.error(str(exc))
                st.markdown("**Audit trail**")
                st.dataframe([{key: (value if value is not None else "—") for key, value in event.items()} for event in result["audit"]], use_container_width=True, hide_index=True)
                st.download_button("Download synthetic processing evidence", json.dumps(result, indent=2),
                                   file_name="document-intake-evidence.json", mime="application/json")
        with architecture:
            architecture_heading("EXECUTION FLOW / PROJECT 02", "Evidence-driven document intake",
                                 "A staged document must pass explicit field and vendor rules. Sensitive bank details require simulated review.")
            architecture_stage("01", "Synthetic text intake", "Select a sample or provide plain text; tenant ID and content hash establish in-memory idempotency.")
            architecture_connector()
            architecture_stage("02", "Classification + field extraction", "Recognize invoice, tax form or supplier agreement and record source-line provenance for each extracted field.")
            architecture_connector()
            architecture_stage("03", "Deterministic validation", "Check required fields, synthetic vendor registry, amounts, currency and dates. Bank-account details trigger review.", "warning")
            st.markdown('<div class="arch-section-label">POLICY DECISION / TWO DISTINCT OUTCOMES</div>', unsafe_allow_html=True)
            left_path, right_path = st.columns(2, gap="medium")
            with left_path:
                architecture_outcome("Validated → staged", "Valid, nonsensitive records enter the synthetic in-memory outbox. Replays return the existing workflow.")
            with right_path:
                architecture_outcome("Exception → review", "Invalid records need correction. Sensitive bank details require explicit named simulated approval before staging.", "warning")
            st.markdown('<div class="arch-section-label">AUDITABILITY</div>', unsafe_allow_html=True)
            architecture_stage("04", "Evidence + audit export", "Field-level line references, decision reasons, workflow ID and structured events can be exported as JSON.", "success")
            st.markdown("**Production gaps:** file upload validation, OCR, malware scanning, durable queue/state, real ERP integration, reviewer authentication, telemetry and cloud evaluation.")
    else:
        from src.enterprise_platform.governance import GovernedGateway, DEMO_PRINCIPALS, TOOLS
        st.markdown("""<div class="hero"><div class="eyebrow">PROJECT 03 / ENTERPRISE GOVERNANCE</div>
        <h1>Enterprise Agent Platform</h1>
        <p>Tool registry, simulated identity, tenant/role enforcement, approval gates and inspectable audit decisions.</p>
        <div class="portfolio-meta"><span class="portfolio-chip">FUNCTIONAL OFFLINE PROTOTYPE</span>
        <span class="portfolio-chip">TENANT ISOLATION</span>
        <span class="portfolio-chip">NO LIVE WRITES</span></div></div>""", unsafe_allow_html=True)
        st.caption("Simulated identity claims only; no OIDC verification, production APIs, Azure infrastructure or persistent audit backend.")
        if "governed_gateway" not in st.session_state:
            st.session_state["governed_gateway"] = GovernedGateway()
        gateway = st.session_state["governed_gateway"]
        overview, execute, architecture = st.tabs(["Overview", "Governed tool execution", "Architecture"])
        with overview:
            a,b,c = st.columns(3)
            a.metric("Registered tools", len(TOOLS))
            b.metric("Demo principals", len(DEMO_PRINCIPALS))
            c.metric("Audit events this session", len(gateway.audit))
            st.markdown("**Control sequence:** simulated verification → registered tool → tenant boundary → role permission → approval gate → scoped read-only data.")
            st.dataframe([{"tool": t.name, "department": t.department,
                           "required_role": t.required_role, "approval_required": t.requires_approval}
                          for t in TOOLS.values()], use_container_width=True, hide_index=True)
        with execute:
            gov_mode = st.radio("Execution mode", ["Deterministic offline", "AI tool selection · Azure Foundry"], horizontal=True, key="p3_mode")
            principal_label = st.selectbox("Simulated principal", list(DEMO_PRINCIPALS))
            selected_principal = DEMO_PRINCIPALS[principal_label]
            if gov_mode.startswith("Deterministic"):
                tool_name = st.selectbox("Requested tool", list(TOOLS))
            else:
                request_text = st.text_area("Natural-language tool request", value="Find the finance reporting procedure for my department.", height=100)
            requested_tenant = st.selectbox("Requested tenant", ["tenant-a", "tenant-b"])
            request_id = st.text_input("Request correlation ID", value="demo-request-001")
            if st.button("Execute governed tool request", type="primary"):
                if gov_mode.startswith("Deterministic"):
                    st.session_state["gov_result"] = gateway.execute(selected_principal, tool_name, requested_tenant, request_id)
                else:
                    try:
                        if not selected_principal.verified or requested_tenant != selected_principal.tenant:
                            st.session_state["gov_result"] = gateway.execute_request(
                                selected_principal, request_text, requested_tenant, request_id)
                        else:
                            from dotenv import load_dotenv
                            from src.support_agent.structured_inference import configured_model
                            load_dotenv()
                            st.session_state["gov_result"] = gateway.execute_request(
                                selected_principal, request_text, requested_tenant, request_id,
                                model=configured_model())
                    except (ValueError, RuntimeError, TimeoutError) as exc:
                        st.error("Azure routing unavailable; no tool executed: " + str(exc))
            if st.button("Record simulated reviewer approval"):
                ok = gateway.approve(request_id, selected_principal)
                if ok:
                    st.success("Simulated approval recorded. Payment updates remain disconnected.")
                else:
                    st.warning("Only a verified simulated principal with the approver role can approve.")
            result = st.session_state.get("gov_result")
            if result:
                st.subheader("Policy decision")
                st.metric("Outcome", result["status"].replace("_", " ").title())
                st.write("**Reason:** " + result["reason"])
                if "model_called" in result:
                    st.caption("Model called: " + str(result["model_called"]))
                st.json(result["records"])
                st.download_button("Download decision evidence", json.dumps(result, indent=2),
                                   file_name="governance-decision.json", mime="application/json")
            st.markdown("**Session audit events**")
            if gateway.audit:
                st.dataframe(gateway.audit, use_container_width=True, hide_index=True)
                st.download_button("Download audit events", json.dumps(gateway.audit, indent=2),
                                   file_name="synthetic-governance-audit.json", mime="application/json")
        with architecture:
            architecture_heading("CONTROL PLANE / PROJECT 03", "Governed enterprise tool access",
                                 "A default-deny policy checks identity assertions, tenant boundaries, tool registration and role permissions before returning synthetic data.")
            architecture_stage("01", "Simulated principal + tool request", "The demo provides a subject, tenant, roles and verification flag; real OIDC/JWT validation is not implemented.")
            architecture_connector("default-deny enforcement")
            architecture_stage("02", "Tenant + role policy", "Reject unverified callers, cross-tenant requests and missing role permissions before data access.", "warning")
            architecture_connector()
            architecture_stage("03", "Allowlisted tool registry", f"{len(TOOLS)} registered capabilities spanning HR, finance and IT, including a payment-write approval example.")
            architecture_connector("approval and action boundary")
            st.markdown('<div class="arch-section-label">POLICY DECISION / CONTROLLED OUTCOMES</div>', unsafe_allow_html=True)
            allowed, denied = st.columns(2, gap="medium")
            with allowed:
                architecture_outcome("Authorized read", "Only matching-tenant, matching-department synthetic records are returned.")
            with denied:
                architecture_outcome("Deny / approval required", "Unapproved requests stop. Even approved payment updates remain disconnected.", "warning")
            st.markdown('<div class="arch-section-label">ACCOUNTABILITY</div>', unsafe_allow_html=True)
            architecture_stage("04", "Auditable policy decisions", "In-memory events record request ID, subject, tenant, tool, decision and reason; exportable as JSON.", "success")
            st.markdown("**Production gaps:** verified OIDC/JWT, managed identities, centralized policy service, real agent runtime, durable approvals, redacted telemetry and deployed Azure services.")
    st.divider()
    st.caption("Independent enterprise AI portfolio · Functional synthetic offline prototype · Not production deployed")
