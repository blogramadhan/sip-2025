# Import library yang diperlukan
import streamlit as st
from streamlit_extras.app_logo import add_logo
from fungsi import *

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Pelaporan Pengadaan Barang dan Jasa",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
load_css()

# Tampilkan logo
logo()

# Struktur navigasi aplikasi
pages = {
    "RENCANA PENGADAAN": [
        st.Page("./src/rencana/rup.py", title="Profil RUP"),
    ],
    "PROSES PENGADAAN": [
        st.Page("./src/proses/tender.py", title="Tender"),
        st.Page("./src/proses/nontender.py", title="Non Tender"),
        st.Page("./src/proses/pencatatan.py", title="Pencatatan"),
        st.Page("./src/proses/ekatalog.py", title="E-Katalog Versi 5"),
        st.Page("./src/proses/ekatalogv6.py", title="E-Katalog Versi 6"),
        st.Page("./src/proses/tokodaring.py", title="Toko Daring"),
        st.Page("./src/proses/pesertatender.py", title="Peserta Tender"),
    ],
    "MONITORING": [
        st.Page("./src/monitoring/itkp.py", title="ITKP"),
        st.Page("./src/monitoring/nilaisikap.py", title="Nilai SIKAP"),
        st.Page("./src/monitoring/jenisbelanja.py", title="Jenis Belanja"),
    ]
}

# Jalankan navigasi
pg = st.navigation(pages)
pg.run()
