import streamlit as st
from config import VALID_MODES

st.set_page_config(
    page_title="Penelitian Keamanan Email",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* ── Hide Streamlit chrome ───────────────────── */
header[data-testid="stHeader"]   { display: none !important; }
[data-testid="stToolbar"]        { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
#MainMenu                        { display: none !important; }
footer                           { display: none !important; }

/* ── Page shell ──────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: #f1f3f4 !important;
}
.block-container {
    padding: 0rem 1rem 10rem 1rem !important;
    # max-width: 680px !important;
}

/* ── Response-form panel (top white card) ────── */
div[data-testid="stVerticalBlock"] > div:first-child {
    background: #ffffff;
}

/* ── Radio tap cards (shared) ───────────────── */
# div[data-testid="stRadio"] > div { gap: 6px; }
# div[data-testid="stRadio"] label {
#     background: #f8f9fa;
#     border: 1px solid #dadce0;
#     border-radius: 8px;
#     padding: 10px 14px !important;
#     font-size: 14px !important;
#     cursor: pointer;
#     width: 100%;
#     display: block;
# }
# div[data-testid="stRadio"] label:has(input:checked) {
#     background: #e8f0fe;
#     border-color: #1a73e8;
#     font-weight: 600;
# }

/* ── Checkbox items ──────────────────────────── */
div[data-testid="stCheckbox"] label {
    font-size: 13px;
    padding: 4px 0;
}

/* ── Primary button full width ───────────────── */
div[data-testid="stButton"] > button[kind="primary"] {
    width: 100%;
    min-height: 48px;
    font-size: 16px;
    border-radius: 0;
    margin: 0;
}

/* ── Mobile tweaks ───────────────────────────── */
@media (max-width: 480px) {
    h2 { font-size: 1.2rem !important; }
    h3 { font-size: 1rem !important;  }
}
</style>
""", unsafe_allow_html=True)

# ── Mode detection ─────────────────────────────────────────────────────────
params = st.query_params
mode = params.get("mode", "").lower()

if mode not in VALID_MODES:
    from screens.blocked import render as render_blocked
    render_blocked()
    st.stop()

from utils.session import init_session
init_session(mode)

# ── Router ─────────────────────────────────────────────────────────────────
screen = st.session_state.get("screen", "consent")

if screen == "consent":
    from screens.consent import render; render()
elif screen == "demographics":
    from screens.demographics import render; render()
elif screen == "scenario":
    from screens.scenario import render; render()
elif screen == "email_phase1":
    from screens.email_screen import render; render(phase=1)
elif screen == "transition":
    from screens.transition import render; render()
elif screen == "email_phase2":
    from screens.email_screen import render; render(phase=2)
elif screen == "survey":
    from screens.survey_screen import render; render()
elif screen == "debrief":
    from screens.debrief import render; render()
else:
    st.markdown("### Selesai. Terima kasih! 🙏")