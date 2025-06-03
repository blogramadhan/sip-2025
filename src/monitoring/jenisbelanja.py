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
con = duckdb.connect(database=':memory:');

# URL Dataset Jenis Belanja
base_url = f"https://data.pbj.my.id/{kodeRUP}/sirup"
datasets = {
    'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan{tahun}.parquet",
    'PAP': f"{base_url}/RUP-PaketAnggaranPenyedia{tahun}.parquet"
}

try:
    # Baca dataset RUP
    dfRUPPP = read_df(datasets['PP'])
    dfRUPPAP = read_df(datasets['PAP'])

    # Gabungkan dataframe RUP
    dfRUPPP_mak = dfRUPPP.merge(
        dfRUPPAP,
        how='left',
        on='kd_rup'
    )

    st.dataframe(dfRUPPP_mak)

except Exception as e:
    st.error(f"Error: {e}")
    
st.title("JENIS BELANJA")
