import streamlit as st
from utils.session import go_to
import streamlit.components.v1 as components

def render():
    # Inject JavaScript to force scroll to top on load
    components.html("""
        <script>
            const parent = window.parent.document;
            const scrollContainers = [
                parent.querySelector('[data-testid="stAppViewContainer"]'),
                parent.querySelector('section[data-testid="stMain"]')
            ];
            
            scrollContainers.forEach(container => {
                if (container) container.scrollTop = 0;
            });
        </script>
    """, height=0, scrolling=False)
    
    st.markdown("## Skenario Eksperimen")
    st.markdown("""
    <div style="background:white; border-radius:8px; padding:20px; border:1px solid #e0e0e0; font-size:15px; line-height:1.7;">
    <strong>Bayangkan situasi berikut:</strong><br><br>
    Anda sedang memeriksa <strong>kotak masuk (inbox)</strong> email kerja Anda hari ini.
    Anda akan melihat beberapa email yang masuk dari berbagai pengirim dengan berbagai topik yang berbeda.<br><br>
    <strong>Untuk setiap email, tugas Anda adalah:</strong><br />
                
    - Membaca email dan peringatan dari sistem keamanan dengan seksama
    - Menilai apakah email tersebut <strong>asli (legitimate)</strong> atau <strong>mencurigakan (phishing)</strong>
    - Menentukan tingkat keyakinan Anda pada keputusan tersebut<br>

    <strong>Panduan Antarmuka Layar:</strong>
    - Bagian Atas: Menampilkan email yang harus Anda evaluasi.
    - Bagian Bawah: Menampilkan formulir untuk mengisi jawaban dan tingkat keyakinan.
    - Gunakan tombol "Lanjut" untuk menyimpan jawaban dan berpindah ke email berikutnya.
        
    <em><small><strong>*Catatan:</strong> Pada tampilan e-mail, tidak ada link atau tautan yang akan terbuka jika diklik, fokus pada isi dan tampilan email.</small></em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("Saya Siap — Mulai Periksa Email →",
                 type="primary", use_container_width=True):
        go_to("email_phase1")