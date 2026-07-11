import streamlit as st
from utils.session import go_to

def render():
    st.markdown("## Bagian 1 selesai!")
    st.markdown("""
    <div style="background:white; border-radius:8px; padding:20px;border:1px solid #e0e0e0; font-size:15px; line-height:1.7;">
    Anda telah berhasil mengevaluasi 8 email pertama. Selanjutnya, Anda akan memasuki Bagian 2 untuk memeriksa 8 email terakhir.
    <br /><br />     
    <strong>Perhatian:</strong><br />
    Pada bagian ini, sistem peringatan telah dinonaktifkan. Anda tidak akan melihat peringatan keamanan atau sinyal apa pun. Anda hanya akan melihat tampilan email saja.
    <br /><br />
    <strong>Tugas Anda tetap sama:</strong><br />
    Lanjutkan seperti sebelumnya — baca setiap email dengan saksama dan nilai apakah email tersebut Asli (Legitimate) atau Mencurigakan (Phishing) berdasarkan penilaian Anda sendiri.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("Lanjutkan →", type="primary", use_container_width=True):
        go_to("email_phase2")