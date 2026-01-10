# Import library yang diperlukan
import streamlit as st
from streamlit_extras.app_logo import add_logo
from fungsi import *

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Informasi Pelaporan Pengadaan Barang dan Jasa",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="auto",
)

# Load custom CSS
load_css()

# Tampilkan logo
logo()


# Jalankan navigasi (disembunyikan, gunakan sidebar kustom)
pg = st.navigation(get_pages(), position="hidden", expanded=True)
with st.sidebar:
    st.markdown("---")

    st.page_link("beranda.py", label="HOME", icon="🏠")

    st.markdown("**RENCANA PENGADAAN**")
    st.page_link("src/rencana/rup.py", label="RUP", icon="📋")

    
    st.markdown("**PROSES PENGADAAN**")
    st.page_link("src/proses/tender.py", label="Tender", icon="⚖️")
    st.page_link("src/proses/nontender.py", label="Non Tender", icon="📝")
    st.page_link("src/proses/pencatatan.py", label="Pencatatan", icon="✍️")
    st.page_link("src/proses/ekatalog.py", label="E-Katalog", icon="📚")
    st.page_link("src/proses/ekatalogv6.py", label="E-Katalog v6", icon="📖")
    st.page_link("src/proses/tokodaring.py", label="Toko Daring", icon="🛒")
    st.page_link("src/proses/pesertatender.py", label="Peserta Tender", icon="👥")
        
    st.markdown("**MONITORING**")
    st.page_link("src/monitoring/itkp.py", label="ITKP", icon="📊")
    st.page_link("src/monitoring/jenisbelanja.py", label="Jenis Belanja", icon="💰")
    st.page_link("src/monitoring/nilaisikap.py", label="Nilai SIKAP", icon="📈")
    
    st.markdown("---")

pg.run()
