# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
import openpyxl
# Library Currency
from babel.numbers import format_currency
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
# Library Social Media Links
from st_social_media_links import SocialMediaIcons
# Library Tambahan
from fungsi import *

# Konfigurasi Page Conf
st.set_page_config(
    page_title="Sistem Informasi Pelaporan Pengadaan Barang dan Jasa",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Membuat Logo
logo()

# Membuat Navigation Bar
pages = {
    "RENCANA DAN PERSIPAN": [
        st.Page("./code/rup.py", title="📋 Rencana Umum Pengadaan"),
        st.Page("./code/sipraja.py", title="🔧 Persiapan Pengadaan"),
    ],
    "PROSES PENGADAAN": [
        st.Page("./code/tender.py", title="🏛️ Tender"),
        st.Page("./code/nontender.py", title="📝 Non Tender"),
        st.Page("./code/epurchasing.py", title="🛒 E-Purchasing"),
        st.Page("./code/pesertatender.py", title="👥 Peserta Tender"),
    ],
    "MONITORING": [
        st.Page("./code/itkp.py", title="🎯 ITKP"),
        st.Page("./code/sikap.py", title="🔍 SIKAP"),
    ]
}

pg = st.navigation(pages)
pg.run()