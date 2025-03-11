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

# Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Membuat Logo
add_logo()

# Membuat Judul Halaman
st.title("Sistem Informasi Pelaporan - Biro Pengadaan Barang dan Jasa")

# Membuat Social Media Links
social_media = SocialMediaIcons(
    "https://www.facebook.com/biropbjkalbar",
    "https://youtube.com/@biropengadaanbarangdanjasa8573?si=jHg5uFTfMQjbF_a3",
    "https://www.instagram.com/barjaskalbar",
)
social_media.render()