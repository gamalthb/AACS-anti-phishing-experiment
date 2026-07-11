import streamlit as st
import streamlit.components.v1 as components
from utils.session import go_to
from utils.loader import load_survey

def render():
    st.markdown("""
        <style>
        /* Menambah jarak vertikal antar pilihan radio button */
        div[role="radiogroup"] {
            gap: 12px; /* Sesuaikan angka ini (misal 16px atau 20px) untuk jarak yang pas */
        }
        </style>
    """, unsafe_allow_html=True)
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

    survey = load_survey()
    st.markdown("## Bagian 2 Selesai!")
    st.markdown("Terima kasih, Anda telah menyelesaikan seluruh tugas pemeriksaan email.")
    st.markdown("Sebagai langkah terakhir, silakan isi kuesioner singkat di bawah ini berdasarkan pengalaman Anda menggunakan sistem peringatan tadi.")
    st.markdown("*Catatan: Tidak ada jawaban yang benar atau salah—kami murni ingin mengetahui pendapat dan pengalaman Anda.*")
    st.markdown("---")
    responses = {}
    all_answered = True

    for item in survey["items"]:
        qid = item["id"]
        st.markdown(f"**{item['text']}**")

        if item["type"] == "likert_7":
            val = st.radio(
                label=f"survey_label_{qid}",
                options=[1, 2, 3, 4, 5, 6, 7],
                format_func=lambda x: {
                    1: "1 — Sangat Tidak Setuju",
                    2: "2 — Tidak Setuju", 
                    3: "3 — Agak Tidak Setuju",
                    4: "4 — Netral",
                    5: "5 — Agak Setuju", 
                    6: "6 — Setuju",
                    7: "7 — Sangat Setuju"
                }[x],
                index=None,
                horizontal=False,
                key=f"survey_{qid}",
                label_visibility="collapsed",
            )
            responses[qid] = val
            if val is None:
                all_answered = False

        elif item["type"] == "free_text":
            val = st.text_area(
                label=qid,
                placeholder="Tuliskan jawaban singkat Anda di sini...",
                key=f"survey_{qid}",
                label_visibility="collapsed",
            )
            responses[qid] = val

        st.markdown("")

    st.markdown("---")
    
    # Validation check
    all_answered = all(
        st.session_state.get(f"survey_{item['id']}") is not None
        for item in survey["items"]
        if item["type"] == "likert_7"
    )

    if st.button("Selesaikan Survei →",
                 type="primary",
                 use_container_width=True,
                 disabled=not all_answered):
        st.session_state.survey_responses = responses
        go_to("debrief")