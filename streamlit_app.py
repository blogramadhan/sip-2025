# Import library yang diperlukan
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from fungsi import *

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Pelaporan Pengadaan Barang dan Jasa",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Tampilkan logo
logo()

# Struktur navigasi aplikasi
pages = {
    "RENCANA DAN PERSIPAN": [
        st.Page("./code/rencana/rup.py", title=" 📋  Rencana Pengadaan"),
        st.Page("./code/rencana/sipraja.py", title=" 🛠️  Persiapan Pengadaan"),
    ],
    "PROSES PENGADAAN": [
        st.Page("./code/proses/tender.py", title=" 🏆  Tender"),
        st.Page("./code/proses/nontender.py", title=" 📄  Non Tender"),
        st.Page("./code/proses/pencatatan.py", title=" ✏️  Pencatatan"),
        st.Page("./code/proses/ekatalog.py", title=" 🏪  E-Katalog Versi 5"),
        st.Page("./code/proses/ekatalogv6.py", title=" 🛍️  E-Katalog Versi 6"),
        st.Page("./code/proses/tokodaring.py", title=" 🏪  Toko Daring"),
        st.Page("./code/proses/pesertatender.py", title=" 👥  Peserta Tender"),
    ],
    "MONITORING": [
        st.Page("./code/monitoring/itkp.py", title=" 📈  ITKP"),
        st.Page("./code/monitoring/nilaisikap.py", title=" ⭐  NILAI SIKAP"),
    ]
}

# Jalankan navigasi
pg = st.navigation(pages)
pg.run()