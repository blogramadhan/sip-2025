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


# Jalankan navigasi
pg = st.navigation(get_pages())
pg.run()
