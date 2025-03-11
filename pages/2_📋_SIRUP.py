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
page_config()

# Membuat Logo
logo()

# Membuat UKPBJ
region_config()

daerah = list(region_config().keys())
tahuns = list(range(2023, 2025))

pilih = st.sidebar.selectbox("Pilih Daerah", daerah)
tahun = st.sidebar.selectbox("Pilih Tahun", tahuns)

# Membuat Judul Halaman
st.title("SIRUP")