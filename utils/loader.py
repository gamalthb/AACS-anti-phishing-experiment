import json
import streamlit as st
from pathlib import Path

@st.cache_data
def load_emails():
    path = Path(__file__).parent.parent / "data" / "emails.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    emails = {}
    for email in data["phase1"] + data["phase2"]:
        emails[email["id"]] = email
    return emails

@st.cache_data
def load_survey():
    path = Path(__file__).parent.parent / "data" / "survey.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)