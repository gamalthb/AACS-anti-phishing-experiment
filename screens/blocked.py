import streamlit as st

def render():
    st.markdown("""
    <style>
    body { background: white; }
    </style>
    """, unsafe_allow_html=True)
    # Intentionally blank — invalid/missing mode