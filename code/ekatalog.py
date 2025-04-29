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

# URL Dataset SIRUP
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'ECAT': f"{base_url}/Ecat-PaketEPurchasing{tahun}.parquet",
    'ECAT_KD': f"{base_url}/ECATKomoditasDetail{tahun}.parquet", 
    'ECAT_IS': f"{base_url}/Ecat-InstansiSatker{tahun}.parquet",
    'ECAT_PD': f"{base_url}/ECATPenyediaDetail{tahun}.parquet",
}

try:
    st.title("TRANSAKSI E-KATALOG")

    # Baca dan gabungkan dataset E-Katalog
    dfECAT = read_df_duckdb(datasets['ECAT'])
    dfECAT_OK = (dfECAT
                 .merge(read_df_duckdb(datasets['ECAT_KD']), how='left', on='kd_komoditas')
                 .drop('nama_satker', axis=1)
                 .merge(read_df_duckdb(datasets['ECAT_IS']), left_on='satker_id', right_on='kd_satker', how='left')
                 .merge(read_df_duckdb(datasets['ECAT_PD']), how='left', on='kd_penyedia'))

    # Header dan tombol unduh
    col1, col2 = st.columns([8,2])
    col1.header(f"{pilih} TAHUN {tahun}")
    col2.download_button(
        label="📥 Unduh E-Katalog",
        data=download_excel(dfECAT_OK),
        file_name=f"Transaksi_E-Katalog_{pilih}_{tahun}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

except Exception as e:
    st.error(f"Error: {e}")


