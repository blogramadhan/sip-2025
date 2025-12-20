import streamlit as st

st.title("🏠 Sistem Informasi Pelaporan Pengadaan")
st.caption("Ringkasan modul, data, dan panduan cepat untuk memulai analisis.")

col_hero_1, col_hero_2 = st.columns((7, 3))
with col_hero_1:
    st.markdown(
        """
        Aplikasi ini menyajikan informasi pengadaan barang dan jasa secara terstruktur
        dari tahap perencanaan, pelaksanaan, hingga monitoring kinerja. Anda dapat
        menelusuri data RUP, status paket, kontrak, realisasi, serta penilaian kinerja
        penyedia secara terpusat. Setiap modul dilengkapi filter daerah dan tahun,
        ringkasan metrik, serta opsi unduh data agar analisis lebih cepat dan konsisten.
        Gunakan menu di sidebar untuk masuk ke modul yang dibutuhkan.
        """
    )
with col_hero_2:
    st.metric("Modul Rencana", "1")
    st.metric("Modul Proses", "7")
    st.metric("Modul Monitoring", "3")

st.divider()

with st.container(border=True):
    st.subheader("🚀 Panduan Cepat")
    col_q_1, col_q_2, col_q_3 = st.columns(3)
    with col_q_1:
        st.page_link("src/rencana/rup.py", label="Buka RUP", icon="📋")
        st.caption("Lihat ringkasan RUP dan struktur anggaran.")
    with col_q_2:
        st.page_link("src/proses/tender.py", label="Buka Tender", icon="⚖️")
        st.caption("Pantau pengumuman, kontrak, dan SPMK.")
    with col_q_3:
        st.page_link("src/monitoring/itkp.py", label="Buka ITKP", icon="📊")
        st.caption("Prediksi indikator kinerja pengadaan.")

st.divider()

with st.container(border=True):
    st.subheader("🧭 Modul Utama")
    col_m_1, col_m_2, col_m_3 = st.columns(3)
    with col_m_1:
        st.markdown(
            """
            **📋 Rencana**
            - RUP
            """
        )
    with col_m_2:
        st.markdown(
            """
            **⚖️ Proses**
            - Tender
            - Non Tender
            - Pencatatan
            - E-Katalog
            - E-Katalog v6
            - Toko Daring
            - Peserta Tender
            """
        )
    with col_m_3:
        st.markdown(
            """
            **📊 Monitoring**
            - ITKP
            - Jenis Belanja
            - Nilai SIKAP
            """
        )

st.divider()

col_i_1, col_i_2 = st.columns(2)
with col_i_1:
    with st.container(border=True):
        st.subheader("📌 Sorotan")
        st.markdown(
            """
            - Ringkas data per perangkat daerah dengan filter cepat.
            - Unduh data Excel langsung dari tiap modul.
            - Visualisasi interaktif untuk tren dan perbandingan.
            """
        )
with col_i_2:
    with st.container(border=True):
        st.subheader("🧩 Sumber Data")
        st.markdown(
            """
            - RUP (SIRUP)
            - SPSE (Tender & Non Tender)
            - SIKAP (Penilaian Kinerja Penyedia)
            - E-Katalog & Toko Daring
            """
        )

st.info("💡 Gunakan sidebar untuk berpindah modul. Pilih daerah dan tahun di setiap halaman.")
