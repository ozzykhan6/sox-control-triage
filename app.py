import json
import os

import streamlit as st
from dotenv import load_dotenv

from triage_engine import analyze_control, mock_analyze
from samples.sample_controls import SAMPLE_CONTROLS, SAMPLE_LABELS

load_dotenv()

st.set_page_config(page_title="SOX Control Triage Tool", page_icon="🛡️", layout="wide")
st.markdown("""
<style>
    .main { padding-top: 1.5rem; }
    h1 { color: #1B3A6B; font-weight: 700; }
    h2 { color: #1B3A6B; }
    h3 { color: #1B3A6B; }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
        border-radius: 8px;
    }
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0E4EA;
        border-radius: 8px;
        padding: 1rem;
    }
    .stButton > button {
        font-weight: 600;
        letter-spacing: 0.5px;
        border-radius: 6px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #E0E4EA;
        border-radius: 8px;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
def _init_state():
    defaults = {
        "control_text": "",
        "selected_sample": "(none)",
        "result": None,
        "result_source": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


_init_state()
st.title("🛡️ SOX Control Triage Tool")
st.caption(
    "Paste a SOX internal control description and get a structured audit analysis. "
    "Powered by the Claude API."
)

ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1, 1, 1])

with ctrl_col1:
    mock_mode = st.toggle(
        "Mock Mode",
        value=True,
        help="When ON, returns hardcoded sample output without calling the API.",
    )

with ctrl_col2:
    prompt_version_label = st.selectbox(
        "Prompt version",
        options=["v2 (refined / production)", "v1 (generic / first attempt)"],
        index=0,
    )
    prompt_version = "v1" if prompt_version_label.startswith("v1") else "v2"

with ctrl_col3:
    st.write("")
    st.write("")
    run_clicked = st.button("▶ Run Analysis", type="primary", use_container_width=True)

if mock_mode:
    st.info("Mock Mode is ON. No API calls are made.", icon="🧪")

st.divider()
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Control Input")

    sample_choice = st.selectbox(
        "Load Sample",
        options=["(none)"] + SAMPLE_LABELS,
        index=0,
    )

    if sample_choice != "(none)" and sample_choice != st.session_state["selected_sample"]:
        st.session_state["control_text"] = SAMPLE_CONTROLS[sample_choice]
        st.session_state["selected_sample"] = sample_choice

    control_text = st.text_area(
        "SOX control description",
        key="control_text",
        height=320,
        placeholder="Paste a SOX internal control description here, or load a sample above...",
    )

    if not mock_mode:
        key_present = bool(os.getenv("ANTHROPIC_API_KEY"))
        if key_present:
            st.caption("API key detected. ✅")
        else:
            st.caption("No API key detected. Add ANTHROPIC_API_KEY to .env or use Mock Mode. ⚠️")
if run_clicked:
    text = st.session_state["control_text"]
    if not text or not text.strip():
        st.warning("Please enter or load a control description first.")
    else:
        try:
            if mock_mode:
                label = st.session_state["selected_sample"]
                label = label if label != "(none)" else None
                st.session_state["result"] = mock_analyze(text, label)
                st.session_state["result_source"] = "Mock Mode (no API call)"
            else:
                api_key = os.getenv("ANTHROPIC_API_KEY", "")
                with st.spinner("Analyzing control with Claude..."):
                    st.session_state["result"] = analyze_control(
                        text, api_key, prompt_version=prompt_version
                    )
                st.session_state["result_source"] = f"Claude API ({prompt_version} prompt)"
        except (ValueError, RuntimeError) as exc:
            st.session_state["result"] = None
            st.error(str(exc))
with right:
    st.subheader("Structured Analysis")
    result = st.session_state["result"]

    if result is None:
        st.markdown("_Run an analysis to see the structured output here._")
    else:
        if st.session_state["result_source"]:
            st.caption(f"Source: {st.session_state['result_source']}")

        with st.container(border=True):
            st.markdown("**1. Control Type**")
            st.markdown(f"### {result.get('control_type', '-')}")

        with st.container(border=True):
            st.markdown("**2. Framework Alignment**")
            st.write(result.get("framework_alignment", "-"))

        with st.container(border=True):
            st.markdown("**3. Risk Rating**")
            rating_text = str(result.get("risk_rating", "-"))
            level = rating_text.split(" ")[0].lower()
            if level.startswith("high"):
                st.error(rating_text, icon="🔴")
            elif level.startswith("medium"):
                st.warning(rating_text, icon="🟠")
            else:
                st.success(rating_text, icon="🟢")

        with st.container(border=True):
            st.markdown("**4. Plain-English Summary**")
            st.write(result.get("plain_english_summary", "-"))

        with st.container(border=True):
            st.markdown("**5. Recommended Test Procedures**")
            procs = result.get("recommended_test_procedures", [])
            for i, proc in enumerate(procs, start=1):
                st.markdown(f"{i}. {proc}")


st.divider()
if st.session_state["result"] is not None:
    with st.expander("📋 Copy output as JSON"):
        st.code(json.dumps(st.session_state["result"], indent=2), language="json")
else:
    st.caption("Run an analysis to enable JSON export.")

st.divider()
st.caption("Portfolio artifact demonstrating AI-assisted audit automation. Built with Streamlit + Claude API.")            