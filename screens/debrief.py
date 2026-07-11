import streamlit as st
import streamlit.components.v1 as components
from utils.sheets import write_response
from utils.scoring import compute_scores
from utils.loader import load_emails
from utils.session import go_to

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

    # Write data on first render of debrief
    if not st.session_state.get("submitted"):
        write_response()

    st.markdown("## Terima Kasih!")
    st.markdown("Eksperimen selesai. Berikut hasil penilaian Anda:")

    scores = compute_scores(st.session_state.responses)
    emails = load_emails()

    p1 = scores["phase1"]
    p2 = scores["phase2"]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Akurasi Bagian 1", f"{int(p1['accuracy']*100)}%",
                  help="8 email pertama (dengan peringatan)")
    with col2:
        st.metric("Akurasi Bagian 2", f"{int(p2['accuracy']*100)}%",
                  help="8 email terakhir (tanpa peringatan)")

    st.markdown("---")
    st.markdown("### Detail Per Email")

    all_order = (
        st.session_state.phase1_order +
        st.session_state.phase2_order
    )

    for eid in all_order:
        email = emails.get(eid, {})
        resp = st.session_state.responses.get(eid, {})
        if not resp:
            continue
        correct = resp["answer"] == email["correct_answer"]
        icon = "✅" if correct else "❌"
        label = "Phishing" if email["correct_answer"] == "phishing" else "Legitimate"
        your_ans = "Mencurigakan" if resp["answer"] == "phishing" else "Legitimate"
        st.markdown(
            f"{icon} **{email['display']['subject'][:50]}...** "
            f"| Seharusnya: *{label}* | Jawaban Anda: *{your_ans}*"
        )

    st.markdown("---")
    st.markdown("""
    **Tentang Penelitian Ini:**
    Seluruh email phishing yang Anda lihat adalah contoh yang direkonstruksi dari serangan siber nyata. Penelitian ini bertujuan untuk mengukur efektivitas berbagai jenis peringatan keamanan dalam membantu karyawan mengidentifikasi ancaman, meskipun saat peringatan tersebut sudah tidak ada lagi (seperti di Bagian 2).

    **Keamanan Data Anda:**
    Harap diingat bahwa seluruh aktivitas ini hanyalah simulasi. Tidak ada data pribadi, kata sandi, atau akun nyata Anda yang diretas atau berada dalam bahaya. Jika Anda melakukan kesalahan dalam mengenali email phishing tadi, hal tersebut sangat wajar—serangan phishing modern memang dirancang agar sangat meyakinkan. Partisipasi Anda sangat membantu kami dalam merancang sistem keamanan yang lebih baik.

    **Kontak Peneliti:**
    Jika Anda memiliki pertanyaan mengenai eksperimen ini atau hasil Anda, silakan hubungi tim peneliti di bawah.

    **Sekali lagi, terima kasih banyak atas waktu dan partisipasi Anda! 🙏 Anda dapat menutup tab ini sekarang.**
    """)
    st.caption("""
    **Tim Peneliti Telkom University**
                
    [Gamal Thabroni](mailto:gamalthabronigt@student.telkomuniversity.ac.id) • 
    [Mochamad T. Kurniawan](mailto:mtk@telkomuniversity.ac.id) • 
    [Fadhil M. Akbar](mailto:fadhilmuhammadakbar@student.telkomuniversity.ac.id) • 
    [Nendii Sharmawanni](mailto:nendiisharmawanni@student.telkomuniversity.ac.id) • 
    [Ilman M. Qori](mailto:ilmanmanarulqori@student.telkomuniversity.ac.id)
    """)