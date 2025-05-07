# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
import openpyxl
from datetime import datetime
# Library Currency
from babel.numbers import format_currency
# Library Aggrid
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
# Library Social Media Links
from st_social_media_links import SocialMediaIcons
# Library Tambahan
from fungsi import *

# Membuat UKPBJ
daerah = region_config()
pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
tahun = st.sidebar.selectbox("Pilih Tahun", range(datetime.now().year, datetime.now().year-3, -1))
selected_daerah = daerah.get(pilih, {})
kodeFolder = selected_daerah.get("folder")
kodeRUP = selected_daerah.get("RUP")
kodeLPSE = selected_daerah.get("LPSE")

# Koneksi DuckDB
con = duckdb.connect(database=':memory:')

# URL Dataset NonTender
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'NonTenderPengumuman': f"{base_url}/SPSE-NonTenderPengumuman{tahun}.parquet",
    'NonTenderSelesai': f"{base_url}/SPSE-NonTenderSelesai{tahun}.parquet",
    'NonTenderSPPBJ': f"{base_url}/SPSE-NonTenderEkontrak-SPPBJ{tahun}.parquet",
    'NonTenderKontrak': f"{base_url}/SPSE-NonTenderEkontrak-Kontrak{tahun}.parquet",
    'NonTenderSPMK': f"{base_url}/SPSE-NonTenderEkontrak-SPMKSPP{tahun}.parquet",
    'NonTenderBAST': f"{base_url}/SPSE-NonTenderEkontrak-BAPBAST{tahun}.parquet",
}

st.title(f"TRANSAKSINON TENDER - {pilih} - {tahun}")

menu_nontender_1, menu_nontender_2, menu_nontender_3, menu_nontender_4, menu_nontender_5 = st.tabs(["| PENGUMUMAN |", "| SPPBJ |", "| KONTRAK |", "| SPMK |", "| BAPBAST |"])

with menu_nontender_1:
    st.header("PENGUMUMAN NON TENDER")

with menu_nontender_2:
    st.header("SPPBJ NON TENDER")

with menu_nontender_3:
    st.header("KONTRAK NON TENDER")

with menu_nontender_4:
    st.header("SPMK NON TENDER")
    
with menu_nontender_5:
    st.header("BAPBAST NON TENDER")