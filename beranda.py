import streamlit as st

st.title("🏠 Selamat Datang di Sistem Informasi Pelaporan")
st.header("Pengadaan Barang dan Jasa")

st.markdown("""
### Tentang Aplikasi

Aplikasi ini menyediakan informasi terkait pengadaan barang dan jasa dengan fitur-fitur berikut:

#### 📋 Rencana
- **RUP**: Rencana Umum Pengadaan

#### ⚖️ Proses
- **Tender**: Informasi tender pengadaan
- **Non Tender**: Informasi non tender
- **Pencatatan**: Data pencatatan pengadaan
- **E-Katalog**: Transaksi e-katalog versi 5
- **E-Katalog v6**: Transaksi e-katalog versi 6
- **Toko Daring**: Transaksi toko daring
- **Peserta Tender**: Data peserta tender

#### 📊 Monitoring
- **ITKP**: Indikator Kinerja Pengadaan
- **Jenis Belanja**: Analisis jenis belanja
- **Nilai SIKAP**: Penilaian kinerja penyedia

---

Silakan pilih menu di sidebar untuk mengakses fitur yang tersedia.
""")

st.info("💡 Gunakan menu navigasi di sidebar untuk memulai eksplorasi data.")
