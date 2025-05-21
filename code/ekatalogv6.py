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

# URL Dataset Katalog
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'ECATV6': f"{base_url}/Ecat-PaketEPurchasingV6{tahun}.parquet",
}

st.title("TRANSAKSI E-KATALOG VERSI 6")
st.header(f"{pilih} - TAHUN {tahun}")

st.divider()

try:
    # Baca dataset E-Katalog V6
    dfECATV6 = read_df_duckdb(datasets['ECATV6'])

    # Header dan tombol unduh
    col1, col2 = st.columns([8,2])
    col1.subheader("TRANSAKSI E-KATALOG V6")
    col2.download_button(
        label="📥 Unduh Transaksi E-Katalog V6",
        data=download_excel(dfECATV6),
        file_name=f"Transaksi_E-Katalog_V6_{pilih}_{tahun}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    KATALOGV6_radio_1, KATALOGV6_radio_2, KATALOGV6_radio_3, KATALOGV6_radio_4 = st.columns((1,1,1,7))  
    with KATALOGV6_radio_1:
        nama_sumber_dana = np.insert(dfECATV6['sumber_dana'].unique(), 0, "Gabungan")
        nama_sumber_dana = st.radio("**Sumber Dana**", nama_sumber_dana)
    with KATALOGV6_radio_2:
        status_paket = np.insert(dfECATV6['status_pkt'].unique(), 0, "Gabungan")
        status_paket = st.radio("**Status Paket**", status_paket)
    with KATALOGV6_radio_3:
        status_kirim = np.insert(dfECATV6['status_pengiriman'].unique(), 0, "Gabungan")
        status_kirim = st.radio("**Status Pengiriman**", status_kirim)
    st.write(f"Anda memilih : **{nama_sumber_dana}** dan **{status_paket}** dan **{status_kirim}**")

    # Build filter query
    df_ECATV6_filter_Query = "SELECT * FROM dfECATV6 WHERE 1=1"
    if nama_sumber_dana != "Gabungan":
        if "APBD" in nama_sumber_dana:
            df_ECATV6_filter_Query += f" AND sumber_dana LIKE '%APBD%'"
        else:
            df_ECATV6_filter_Query += f" AND sumber_dana = '{nama_sumber_dana}'"
    if status_paket != "Gabungan":
        df_ECATV6_filter_Query += f" AND status_pkt = '{status_paket}'"
    if status_kirim != "Gabungan":
        df_ECATV6_filter_Query += f" AND status_pengiriman = '{status_kirim}'"

    df_ECATV6_filter = con.execute(df_ECATV6_filter_Query).df()

    # Metrics   
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Jumlah Produk Katalog", value="{:,}".format(df_ECATV6_filter['jml_jenis_produk'].sum()))
    col2.metric(label="Jumlah Transaksi Katalog", value="{:,}".format(df_ECATV6_filter['kd_paket'].nunique()))
    col3.metric(label="Nilai Transaksi Katalog", value="{:,.2f}".format(df_ECATV6_filter['total_harga'].sum()))

    st.divider()

    # Berdasarkan Kualifikasi Usaha
    

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
