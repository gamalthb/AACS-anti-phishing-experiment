import streamlit as st
import streamlit.components.v1 as components
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
    st.markdown("## Informasi Demografis")
    st.markdown("Mohon isi semua informasi berikut. Semua informasi bersifat anonim dan hanya digunakan untuk keperluan analisis penelitian.*")
    st.markdown("---")

    age = st.selectbox(
        "Rentang usia Anda:",
        ["", "18-24 tahun", "25–34 tahun", "34–44 tahun", "45-54 tahun", "55 tahun ke atas"],
    )

    gender = st.selectbox(
        "Jenis kelamin Anda:",
        ["", "Laki-laki", "Perempuan", "Memilih Tidak Menyebut"],
    )

    education = st.selectbox(
        "Pendidikan terakhir Anda:",
        ["", "SMA / Sederajat", "Diploma (D1–D3)", "Sarjana (S1)", "Pascasarjana (S2/S3)"],
    )

    job = st.selectbox(
        "Fungsi pekerjaan Anda saat ini:",
        ["", "Keuangan / Akuntansi", "HR / Personalia", "Layanan Pelanggan", "Manajemen / Eksekutif",
         "Administrasi / Sekretariat", "Pemasaran / Sales", "Akademik / Pengajaran",
         "Operasional / Logistik", "Lainnya"],
    )

    # Dynamic text input conditionally rendered
    job_other = ""
    if job == "Lainnya":
        job_other = st.text_input("Silakan sebutkan fungsi pekerjaan Anda:")

    exp = st.selectbox(
        "Lama pengalaman kerja Anda:",
        ["", "Kurang dari 1 tahun", "1–2 tahun", "3–5 tahun", "6-10 tahun", "Lebih dari 10 tahun"],
    )

    email_freq = st.selectbox(
        "Seberapa sering Anda menggunakan email dalam pekerjaan sehari-hari?",
        ["", "Jarang (kurang dari 5 email per hari)",
         "Sedang (5–20 email per hari)",
         "Sering (lebih dari 20 email per hari)"],
    )

    training = st.radio(
        "Pernahkah Anda mengikuti pelatihan keamanan siber di tempat kerja?",
        ["Ya", "Tidak"],
        index=None,
        horizontal=True,
    )

    device = st.radio(
        "Perangkat yang Anda gunakan saat ini:",
        ["Smartphone / HP", "Laptop", "Komputer Desktop", "Tablet"],
        index=None,
        horizontal=True,
    )

    st.markdown("---")

    # Determine the final job string to save and validate
    final_job = job_other.strip() if job == "Lainnya" else job

    # final_job evaluates to False if it's an empty string ""
    all_filled = all([age, gender, education, final_job, exp, email_freq, training, device])

    if st.button("Lanjut →", disabled=not all_filled,
                 type="primary", use_container_width=True):
        st.session_state.demographics = {
            "age_range": age,
            "gender": gender,
            "education": education,
            "job_function": final_job, # Save the specific job if 'Lainnya' was chosen
            "experience": exp,
            "email_frequency": email_freq,
            "prior_training": training,
            "device": device,
        }
        go_to("scenario")

    if not all_filled:
        st.caption("Mohon lengkapi semua pertanyaan untuk melanjutkan.")