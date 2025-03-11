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
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
# Library Social Media Links
from st_social_media_links import SocialMediaIcons
# Library Tambahan
from fungsi import *

# Konfigurasi Page Conf
page_config()

# Membuat Logo
logo()

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
base_url = f"https://data.pbj.my.id/{kodeRUP}/sirup"
datasets = {
    'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan{tahun}.parquet",
    'PS': f"{base_url}/RUP-PaketSwakelola-Terumumkan{tahun}.parquet", 
    'SA': f"{base_url}/RUP-StrukturAnggaranPD{tahun}.parquet"
}

try:
    # Baca dataset RUP
    dfRUPPP = read_df_duckdb(datasets['PP'])
    dfRUPPS = read_df_duckdb(datasets['PS'])
    dfRUPSA = read_df_duckdb(datasets['SA'])

    # Filter data RUP Penyedia
    dfRUPPP_umumkan = con.execute("SELECT * FROM dfRUPPP WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
    dfRUPPP_umumkan_ukm = con.execute("SELECT * FROM dfRUPPP_umumkan WHERE status_ukm = 'UKM'").df()
    dfRUPPP_umumkan_pdn = con.execute("SELECT * FROM dfRUPPP_umumkan WHERE status_pdn = 'PDN'").df()

    # Filter data RUP Swakelola
    dfRUPPS_umumkan = con.execute("""
        SELECT nama_satker, kd_rup, nama_paket, pagu, tipe_swakelola, volume_pekerjaan, 
               uraian_pekerjaan, tgl_pengumuman_paket, tgl_awal_pelaksanaan_kontrak, 
               nama_ppk, status_umumkan_rup
        FROM dfRUPPS 
        WHERE status_umumkan_rup = 'Terumumkan'
    """).df()

    namaopd = dfRUPPP_umumkan['nama_satker'].unique()

except Exception as e:
    st.error(f"Error: {e}")

#####
# Konten Data RUP
#####

# Buat Tab Menu
menu_rup_1, menu_rup_2, menu_rup_3, menu_rup_4, menu_rup_5, menu_rup_6 = st.tabs([
    "| PROFIL RUP |", "| STRUKTUR ANGGARAN |", "| RUP PAKET PENYEDIA |", 
    "| RUP PAKET SWAKELOLA |", "| PERSENTASE INPUT RUP |", "| PERSENTASE INPUT RUP (31 MAR) |"
])

with menu_rup_1:
    st.title("PROFIL RUP")
    st.write("Profil RUP")

with menu_rup_2:
    st.title("STRUKTUR ANGGARAN")
    st.write("Struktur Anggaran")

with menu_rup_3:
    st.title("RUP PAKET PENYEDIA")
    st.write("RUP Paket Penyedia")

with menu_rup_4:
    st.title("RUP PAKET SWAKELOLA")
    st.write("RUP Paket Swakelola")

with menu_rup_5:
    st.title("PERSENTASE INPUT RUP")
    st.write("Persentase Input RUP")

with menu_rup_6:
    st.title("PERSENTASE INPUT RUP (31 MAR)")
    st.write("Persentase Input RUP (31 Mar)")

