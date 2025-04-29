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
    "📝 RENCANA DAN PERSIPAN": [
        st.Page("./code/rup.py", title=" 📅  Rencana Pengadaan"),
        st.Page("./code/sipraja.py", title=" ⚙️  Persiapan Pengadaan"),
    ],
    "🔄 PROSES PENGADAAN": [
        st.Page("./code/tender.py", title=" 🔨  Tender"),
        st.Page("./code/nontender.py", title=" 📄  Non Tender"),
        st.Page("./code/ekatalog.py", title=" 🛒  E-Katalog"),
        st.Page("./code/tokodaring.py", title=" 🏪  Toko Daring"),
        st.Page("./code/pesertatender.py", title=" 👥  Peserta Tender"),
    ],
    "📊 MONITORING": [
        st.Page("./code/itkp.py", title=" 📈  ITKP"),
        st.Page("./code/nilaisikap.py", title=" ⭐  NILAI SIKAP"),
    ]
}

# Jalankan navigasi
pg = st.navigation(pages)
pg.run()