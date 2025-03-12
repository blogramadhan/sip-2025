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
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        # Query data dari database
        queries = {
            'strukturanggaran': "SELECT nama_satker AS NAMA_SATKER, belanja_pengadaan AS STRUKTUR_ANGGARAN FROM dfRUPSA WHERE STRUKTUR_ANGGARAN > 0",
            'paketpenyedia': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_PENYEDIA FROM dfRUPPP_umumkan GROUP BY NAMA_SATKER",
            'paketswakelola': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_SWAKELOLA FROM dfRUPPS_umumkan GROUP BY NAMA_SATKER"
        }
        
        # Eksekusi query dan merge dataframe
        dfs = {k: con.execute(v).df() for k,v in queries.items()}
        ir_gabung = pd.merge(pd.merge(dfs['strukturanggaran'], dfs['paketpenyedia'], how='left', on='NAMA_SATKER'), 
                            dfs['paketswakelola'], how='left', on='NAMA_SATKER')
        
        # Kalkulasi kolom tambahan
        ir_gabung_final = (ir_gabung
            .assign(TOTAL_RUP = lambda x: x.RUP_PENYEDIA + x.RUP_SWAKELOLA)
            .assign(SELISIH = lambda x: x.STRUKTUR_ANGGARAN - x.TOTAL_RUP)
            .assign(PERSEN = lambda x: round((x.TOTAL_RUP / x.STRUKTUR_ANGGARAN * 100), 2))
            .fillna(0))

        # Download button
        st.download_button(
            label="📥 Download  % Input RUP",
            data=download_excel(ir_gabung_final),
            file_name=f"TabelPersenInputRUP_{pilih}_{tahun}.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Tampilkan dataframe
        st.dataframe(
            ir_gabung_final,
            column_config={
                "STRUKTUR_ANGGARAN": "STRUKTUR ANGGARAN",
                "RUP_PENYEDIA": "RUP PAKET PENYEDIA", 
                "RUP_SWAKELOLA": "RUP PAKET SWAKELOLA",
                "TOTAL_RUP": "TOTAL RUP",
                "SELISIH": "SELISIH",
                "PERSEN": "PERSENTASE"
            },
            hide_index=True,
            use_container_width=True,
            height=1000
        )

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_6:
    st.title("PERSENTASE INPUT RUP (31 MAR)")
    st.write("Persentase Input RUP (31 Mar)")

