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

# Perispan DuckDB
con = duckdb.connect(database=':memory:')
# con.sql("INSTALL httpfs")
# con.sql("LOAD httpfs")

# Dataset SIRUP (PARQUET)
DatasetRUPPP = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-PaketPenyedia-Terumumkan{tahun}.parquet"
DatasetRUPPS = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-PaketSwakelola-Terumumkan{tahun}.parquet"
DatasetRUPSA = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-StrukturAnggaranPD{tahun}.parquet"

# Dataset SIRUP (PARQUET) 31 Maret Tahun Berjalan
DatasetRUPPP31Mar = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-PaketPenyedia-Terumumkan-{tahun}-03-31.parquet"
DatasetRUPPS31Mar = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-PaketSwakelola-Terumumkan-{tahun}-03-31.parquet"
DatasetRUPSA31Mar = f"https://data.pbj.my.id/{kodeRUP}/sirup/RUP-StrukturAnggaranPD-{tahun}-03-31.parquet"

# Dataframe RUP
try:
    # Baca dataset RUP Paket Penyedia, Swakelola, dan Struktur Anggaran
    dfRUPPP = con.sql(f"SELECT * FROM read_parquet('{DatasetRUPPP}')").df()
    dfRUPPS = con.sql(f"SELECT * FROM read_parquet('{DatasetRUPPS}')").df()
    dfRUPSA = con.sql(f"SELECT * FROM read_parquet('{DatasetRUPSA}')").df()

    # Query RUP Paket Penyedia
    dfRUPPP_umumkan = con.execute("SELECT * FROM dfRUPPP WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
    dfRUPPP_umumkan_ukm = con.execute("SELECT * FROM dfRUPPP_umumkan WHERE status_ukm = 'UKM'").df()
    dfRUPPP_umumkan_pdn = con.execute("SELECT * FROM dfRUPPP_umumkan WHERE status_pdn = 'PDN'").df()

    # Query RUP Paket Swakelola
    sqlRUPPS = """
        SELECT nama_satker, kd_rup, nama_paket, pagu, tipe_swakelola, volume_pekerjaan, uraian_pekerjaan, 
        tgl_pengumuman_paket, tgl_awal_pelaksanaan_kontrak, nama_ppk, status_umumkan_rup
        FROM df_RUPPS
        WHERE status_umumkan_rup = 'Terumumkan'
    """
    dfRUPPS_umumkan = con.execute(sqlRUPPS).df()

    namaopd = dfRUPPP_umumkan['nama_satker'].unique()

except Exception as e:
    st.error(f"Error: {e}")