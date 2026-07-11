import time
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from utils.scoring import compute_scores
from utils.loader import load_emails
from config import PHASE1_IDS, PHASE2_IDS

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=SCOPES
    )
    client = gspread.authorize(creds)
    return client.open(st.secrets["sheets"]["spreadsheet_name"]).sheet1

def build_row(session) -> list:
    emails = load_emails()
    scores = compute_scores(session["responses"])
    all_ids = PHASE1_IDS + PHASE2_IDS

    base = [
        session["participant_id"],
        session["mode"],
        session.get("timestamp_start", ""),
        round(time.time() - session.get("timestamp_start", time.time()), 0),
        session["demographics"].get("age_range", ""),
        session["demographics"].get("education", ""),
        session["demographics"].get("job_function", ""),
        session["demographics"].get("experience", ""),
        session["demographics"].get("email_frequency", ""),
        session["demographics"].get("prior_training", ""),
        session["demographics"].get("device", ""),
    ]

    email_cols = []
    for eid in all_ids:
        r = session["responses"].get(eid, {})
        email_cols += [
            r.get("answer", ""),
            int(r.get("answer", "") == emails.get(eid, {}).get("correct_answer", "")),
            r.get("confidence", ""),
            "|".join(r.get("cues_selected", [])),
            r.get("response_time_seconds", ""),
        ]

    survey_cols = [
        session["survey_responses"].get(f"Q{i}", "") for i in range(1, 9)
    ]

    score_cols = [
        scores["phase1"]["accuracy"],
        scores["phase1"]["phishing_accuracy"],
        scores["phase1"]["legit_accuracy"],
        scores["phase2"]["accuracy"],           # ← was after avg_confidence, move here
        scores["phase2"]["phishing_accuracy"],  # ← same
        scores["phase2"]["legit_accuracy"],     # ← same
        scores["phase1"]["avg_confidence"],     # ← now after phase2 accuracies
        scores["phase2"]["avg_confidence"],
        scores["phase1"].get("cue_accuracy", ""),
        "No",
        "Yes",
    ]

    return base + email_cols + survey_cols + score_cols

def write_response():
    if st.session_state.get("submitted"):
        return
    try:
        sheet = get_sheet()
        row = build_row(st.session_state)
        sheet.append_row(row, value_input_option="RAW")
        st.session_state.submitted = True
    except Exception as e:
        st.error(f"Gagal menyimpan data: {e}")