import time
import streamlit as st
import streamlit.components.v1 as components
from utils.session import go_to, save_email_response
from utils.loader import load_emails
from components.email_display import render_email_card
from components.response_form import render_response_form

def render(phase: int):
    emails = load_emails()
    mode = st.session_state.mode
    order = st.session_state[f"phase{phase}_order"]
    index = st.session_state.email_index

    if index >= len(order):
        st.session_state.email_index = 0
        go_to("transition" if phase == 1 else "survey")
        return

    email_id = order[index]
    email = emails[email_id]

    # 1. Inject the current index into the JS so Streamlit treats it as a NEW component every time.
    # 2. Target stAppViewContainer and stMain to ensure we hit the right scrollable element.
    components.html(f"""
        <script>
            // This comment forces a re-render when index changes: {index}
            const parent = window.parent.document;
            const scrollContainers = [
                parent.querySelector('[data-testid="stAppViewContainer"]'),
                parent.querySelector('section[data-testid="stMain"]')
            ];
            
            scrollContainers.forEach(container => {{
                if (container) container.scrollTop = 0;
            }});
        </script>
    """, height=0, scrolling=False)

    phase1_len = len(st.session_state.phase1_order)
    current_num = (index + 1) if phase == 1 else (phase1_len + index + 1)

    render_email_card(email, mode, current_num)

    result = render_response_form(email, mode, phase)
    if result is not None:
        save_email_response(
            email_id,
            result["answer"],
            result["confidence"],
            result["cues_selected"],
            result["response_time_seconds"],
        )
        st.session_state.email_index += 1
        st.rerun()