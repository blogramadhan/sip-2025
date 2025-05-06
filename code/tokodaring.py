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

# URL Dataset Toko Daring
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'BELA': f"{base_url}/Bela-TokoDaringRealisasi{tahun}.parquet",
}

try:
    # Baca data dan siapkan unduhan
    dfBELA = read_df_duckdb(datasets['BELA'])

    # Tampilkan header dan tombol unduh
    col1, col2 = st.columns((7,3))
    col1.header(f"TRANSAKSI TOKO DARING - {pilih} - TAHUN {tahun}")
    col2.download_button(
        label="📥 Unduh Data Toko Daring",
        data=download_excel(dfBELA),
        file_name=f"TransaksiTokoDaring-{kodeFolder}-{tahun}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.divider()

    # Filter data
    col1, col2 = st.columns(2)
    with col1:
        status_verifikasi = st.radio("**Status Verifikasi**", ["Gabungan", "Verified", "Unverified"])
    with col2:
        status_ppmse = st.radio("**Status Konfirmasi PPMSE**", ["Gagal", "Selesai"])
    
    st.write(f"Filter aktif: **{status_verifikasi}** dan **{status_ppmse}**")

    # Query yang lebih ringkas
    query = "SELECT * FROM dfBELA WHERE LENGTH(nama_satker) > 1"
    
    if status_verifikasi != "Gabungan":
        query += f" AND status_verif = '{status_verifikasi.lower()}'"
    
    if status_ppmse.lower() == "selesai":
        query += " AND (status_konfirmasi_ppmse = 'selesai' OR status_konfirmasi_ppmse IS NULL)"
    else:
        query += f" AND status_konfirmasi_ppmse = '{status_ppmse.lower()}'"
    df_BELA_filter = con.execute(query).df()
    
    # Tampilkan metrik
    col1, col2 = st.columns(2)
    col1.metric(
        label="Jumlah Transaksi Toko Daring", 
        value="{:,}".format(df_BELA_filter['order_id'].nunique())
    )
    col2.metric(
        label="Nilai Transaksi Toko Daring", 
        value="{:,.2f}".format(df_BELA_filter['valuasi'].sum())
    )

    st.divider()

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
