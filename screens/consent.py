import streamlit as st
from utils.session import go_to

# 1. Add custom CSS at the top of your file
_CONTAINER_CSS = """
<style>
/* Find the Streamlit container border wrapper that contains our secret marker class */
div[data-testid="stLayoutWrapper"]:has(.consent-bg) {
    font-size: 12px;
    background-color: #ffffff; /* White background */
    border-radius: 8px; /* Rounded corners */
    box-shadow: 0 1px 3px rgba(0,0,0,.08); /* Optional: subtle shadow */
}
</style>
"""

def render():
    st.markdown(_CONTAINER_CSS, unsafe_allow_html=True)
    
    st.markdown("## Selamat Datang!")
    st.markdown("Terima kasih telah bersedia meluangkan waktu Anda. Sebelum memulai, harap baca informasi berikut dengan seksama.")
    
    with st.container(border=True):
        # 2. Put the invisible marker right at the top of the container
        
        st.markdown("""
        **Tentang Eksperimen yang akan Anda lakukan:**
                    
        Anda akan bertindak sebagai staff yang sedang memeriksa kotak masuk email. Anda akan mengevaluasi 16 email. Beberapa email akan disertai dengan peringatan dari sistem keamanan.
        Untuk setiap email, Anda harus memilih salah satu keputusan berikut:

        - Asli (Legitimate): Email aman dan merupakan komunikasi bisnis yang wajar.
        - Mencurigakan (Phishing): Email ini mencurigakan dan merupakan upaya penipuan (phishing) yang dirancang untuk mencuri informasi, kata sandi, atau meretas akun dengan menyamar sebagai pihak resmi.
       
        Data dikumpulkan secara anonim dan partisipasi bersifat sukarela, Anda dapat menghentikannya kapan saja. Estimasi waktu: ±20 menit, diakhiri dengan survei singkat.
        """, unsafe_allow_html=True)

        st.caption("""
        **Tim Peneliti Telkom University**
                   
        [Gamal Thabroni](mailto:gamalthabronigt@student.telkomuniversity.ac.id) • 
        [Mochamad T. Kurniawan](mailto:mtk@telkomuniversity.ac.id) • 
        [Fadhil M. Akbar](mailto:fadhilmuhammadakbar@student.telkomuniversity.ac.id) • 
        [Nendii Sharmawanni](mailto:nendiisharmawanni@student.telkomuniversity.ac.id) • 
        [Ilman M. Qori](mailto:ilmanmanarulqori@student.telkomuniversity.ac.id)
        """)

        st.markdown("<div class='consent-bg'><strong>Konfirmasi Partisipasi</strong></div>", unsafe_allow_html=True)

        is_it = st.radio(
            "Apakah pekerjaan utama Anda di bidang IT, keamanan siber, atau pemrograman?",
            options=["Tidak", "Ya"],
            index=None,
            horizontal=True,
        )

        if is_it == "Ya":
            st.warning("Mohon maaf, penelitian ini ditujukan untuk karyawan di luar bidang IT. Terima kasih atas minat Anda.")

        if is_it == "Tidak":
            agree = st.checkbox("Saya telah membaca penjelasan di atas dan bersedia berpartisipasi secara sukarela.")
            if agree:
                st.write("") 
                if st.button("Mulai Eksperimen →", type="primary", use_container_width=True):
                    go_to("demographics")