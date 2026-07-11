import random
import time
import uuid
import streamlit as st
from config import PHASE1_IDS, PHASE2_IDS

def init_session(mode: str):
    """Called once when a valid mode is first detected."""
    if "initialized" in st.session_state:
        return

    phase1 = PHASE1_IDS.copy()
    phase2 = PHASE2_IDS.copy()
    random.shuffle(phase1)
    random.shuffle(phase2)

    st.session_state.update({
        "initialized": True,
        "participant_id": str(uuid.uuid4())[:8],
        "mode": mode,
        "screen": "consent",
        "phase1_order": phase1,
        "phase2_order": phase2,
        "email_index": 0,
        "current_phase": 1,
        "responses": {},
        "demographics": {},
        "survey_responses": {},
        "timestamp_start": time.time(),
        "submitted": False,
    })

def go_to(screen: str):
    st.session_state.screen = screen
    st.rerun()

def save_email_response(email_id: str, answer: str,
                        confidence: int, cues: list,
                        response_time: float):
    st.session_state.responses[email_id] = {
        "answer": answer,
        "confidence": confidence,
        "cues_selected": cues,
        "response_time_seconds": round(response_time, 1)
    }