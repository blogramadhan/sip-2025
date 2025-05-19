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

# URL Dataset Tender
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'TenderPengumuman': f"{base_url}/SPSE-TenderPengumuman{tahun}.parquet",
    'TenderSelesai': f"{base_url}/SPSE-TenderSelesai{tahun}.parquet",
    'TenderSelesaiNilai': f"{base_url}/SPSE-TenderSelesaiNilai{tahun}.parquet",
    'TenderSPPBJ': f"{base_url}/SPSE-TenderEkontrak-SPPBJ{tahun}.parquet",
    'TenderKontrak': f"{base_url}/SPSE-TenderEkontrak-Kontrak{tahun}.parquet",
    'TenderSPMK': f"{base_url}/SPSE-TenderEkontrak-SPMKSPP{tahun}.parquet",
    'TenderBAST': f"{base_url}/SPSE-TenderEkontrak-BAPBAST{tahun}.parquet",
}

st.title("TRANSAKSI TENDER")
st.header(f"{pilih} - TAHUN {tahun}")

menu_tender_1, menu_tender_2, menu_tender_3, menu_tender_4, menu_tender_5 = st.tabs(["| PENGUMUMAN |", "| SPPBJ |", "| KONTRAK |", "| SPMK |", "| BAPBAST |"])

with menu_tender_1:
    try:
        # Baca dataset pengumuman Tender Selesai
        dfSPSETenderPengumuman = read_df_duckdb(datasets['TenderPengumuman']).drop(columns=['nama_pokja'])

        # Tampilkan header dan tombol unduh
        col1, col2 = st.columns([7,3])
        col1.subheader("PENGUMUMAN TENDER")
        col2.download_button(
            label="📥 Unduh Data Pengumuman Tender",
            data=download_excel(dfSPSETenderPengumuman),
            file_name=f"Tender-Pengumuman-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.divider()

    except Exception as e:
        st.error(f"Error: {e}")

with menu_tender_2:
    st.subheader("SPPBJ TENDER")

with menu_tender_3:
    st.subheader("KONTRAK TENDER")

with menu_tender_4:
    st.subheader("SPMK TENDER")

with menu_tender_5:
    st.subheader("BAPBAST TENDER")