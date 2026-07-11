import time
import streamlit as st

_FORM_CSS = """
<style>
/* 1. Darken the app background to isolate the email showcase */
[data-testid="stAppViewContainer"] {
    background-color: #e8eaed !important; 
}

.st-emotion-cache-1svz3dh{
    background-color: #ffffff !important;
    border-radius: 0px !important;
    border: none !important;
    border-top: 1px solid #dadce0 !important;
    box-shadow: 0px -8px 24px rgba(0, 0, 0, 0.12) !important; /* Upward docked shadow */
}

/* Remove the default inner padding Streamlit forces inside borders */
div[data-testid="stElementContainer"] > div:has(> div[data-testid="stVerticalBlock"]:has(#form-dock-marker)) > div[data-testid="stVerticalBlock"] {
    padding: 0 !important;
}

/* Hide our secret marker */
#form-dock-marker {
    display: none !important;
}

/* 3. Tap targets for the radios */
div[data-testid="stRadio"] > div { gap: 8px; }
div[data-testid="stRadio"] label {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: 12px 14px !important;
    font-size: 14px !important;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s ease;
}
div[data-testid="stRadio"] label:hover {
    background: #f8f9fa;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: #e8f0fe !important;
    border-color: #1a73e8 !important;
    box-shadow: 0 0 0 1px #1a73e8 !important;
}

.form-label {
    font-size: 15px;
    font-weight: 600;
    color: #202124;
    margin-bottom: 12px;
}

.st-emotion-cache-zh2fnc {
    width: 100%;
}
</style>
"""

def render_response_form(email: dict, mode: str, phase: int) -> dict | None:
    # Inject the CSS globally
    st.markdown(_FORM_CSS, unsafe_allow_html=True)

    # 🚨 PUT BORDER=TRUE BACK IN! 
    # We MUST have this so Streamlit creates a physical wrapper box for our CSS to hijack.
    with st.container(border=True):
        
        # Inject the exact marker our CSS is looking for
        st.markdown("<span id='form-dock-marker'></span>", unsafe_allow_html=True)
        
        st.markdown('<div class="form-label">📋 Keputusan Anda</div>', unsafe_allow_html=True)

        email_id = email["id"]
        start_key = f"start_{email_id}"
        if start_key not in st.session_state:
            st.session_state[start_key] = time.time()

        answer = st.radio(
            "Email ini menurut Anda:",
            options=["legitimate", "phishing"],
            format_func=lambda x: (
                "✅  Email Asli (Legitimate)" if x == "legitimate"
                else "⚠️  Email Mencurigakan (Phishing)"
            ),
            index=None,
            horizontal=True,
            key=f"answer_{email_id}",
            label_visibility="collapsed",
        )

        st.write("") # Spacing

        # Cue checkboxes — Phase 1 phishing only
        cues_selected = []
        show_cues = (
            phase == 1
            and mode != "pilot"
            and email["type"] == "phishing"
            and bool(email.get("cue_options"))
        )

        if show_cues:
            st.markdown("**🔍 Sinyal yang mempengaruhi keputusan Anda:**")
            st.caption("Pilih semua yang relevan")
            for opt in email["cue_options"]:
                if st.checkbox(opt["text"], key=f"cue_{email_id}_{opt['id']}"):
                    cues_selected.append(opt["id"])
            st.write("") # Spacing

        st.markdown(
            '<div class="form-label" style="margin-top:8px;">🎯 Tingkat keyakinan Anda:</div>',
            unsafe_allow_html=True,
        )
        confidence = st.radio(
            "Keyakinan:",
            options=[1, 2, 3, 4, 5, 6, 7],
            format_func=lambda x: {
                1: "1 — Sangat tidak yakin", 
                2: "2 — Tidak yakin", 
                3: "3 — Agak tidak yakin",
                4: "4 — Netral",
                5: "5 — Agak yakin", 
                6: "6 — Yakin", 
                7: "7 — Sangat yakin",
            }[x],
            index=None,
            horizontal=True,
            key=f"conf_{email_id}",
            label_visibility="collapsed",
        )

        st.write("") # Spacing
        
        disabled = answer is None or confidence is None
        
        if st.button(
            "Lanjut →",
            disabled=disabled,
            key=f"next_{email_id}",
            type="primary",
            use_container_width=True,
        ):
            elapsed = time.time() - st.session_state[start_key]
            return {
                "answer": answer,
                "confidence": confidence,
                "cues_selected": cues_selected,
                "response_time_seconds": round(elapsed, 1),
            }

        if disabled:
            st.caption("Pilih opsi email dan tingkat keyakinan untuk melanjutkan.")

    return None