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

# URL Dataset Pencatatan
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'CatatNonTender': f"{base_url}/SPSE-PencatatanNonTender{tahun}.parquet",
    'CatatNonTenderRealisasi': f"{base_url}/SPSE-PencatatanNonTenderRealisasi{tahun}.parquet",
    'CatatSwakelola': f"{base_url}/SPSE-PencatatanSwakelola{tahun}.parquet",
    'CatatSwakelolaRealisasi': f"{base_url}/SPSE-PencatatanSwakelolaRealisasi{tahun}.parquet",
}

st.title(f"TRANSAKSI PENCATATAN")
st.header(f"{pilih} - TAHUN {tahun}")

menu_pencatatan_1, menu_pencatatan_2 = st.tabs(["| PENCATATAN NON TENDER |", "| PENCATATAN SWAKELOLA |"])

with menu_pencatatan_1:
    try:
        # Baca dan gabungkan dataset pencatatan non tender
        dfCatatNonTender = read_df_duckdb(datasets['CatatNonTender'])
        dfCatatNonTenderRealisasi = read_df_duckdb(datasets['CatatNonTenderRealisasi'])[[
            "kd_nontender_pct", "jenis_realisasi", "no_realisasi", 
            "tgl_realisasi", "nilai_realisasi", "nama_penyedia", "npwp_penyedia"
        ]]
        dfGabung = dfCatatNonTender.merge(dfCatatNonTenderRealisasi, how='left', on='kd_nontender_pct')

        # Tampilkan header dan tombol unduh
        col1, col2 = st.columns((7,3))
        with col1:
            st.subheader(f"PENCATATAN NON TENDER TAHUN {tahun}")
        with col2:
            st.download_button(
                label = "📥 Download Data Pencatatan Non Tender",
                data = download_excel(dfGabung),
                file_name = f"SPSEPencatatanNonTender-{kodeFolder}-{tahun}.xlsx",
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        st.divider()

    except Exception as e:
        st.error(f"Error: {e}")

with menu_pencatatan_2:
    st.subheader("PENCATATAN SWAKELOLA")


