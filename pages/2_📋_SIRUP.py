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
    'SA': f"{base_url}/RUP-StrukturAnggaranPD{tahun}.parquet",
    'PP31': f"{base_url}/RUP-PaketPenyedia-Terumumkan-{tahun}-03-31.parquet",
    'PS31': f"{base_url}/RUP-PaketSwakelola-Terumumkan-{tahun}-03-31.parquet",
    'SA31': f"{base_url}/RUP-StrukturAnggaranPD-{tahun}-03-31.parquet"
}

try:
    # Baca dataset RUP
    dfRUPPP = read_df_duckdb(datasets['PP'])
    dfRUPPS = read_df_duckdb(datasets['PS'])
    dfRUPSA = read_df_duckdb(datasets['SA'])

    # Register DataFrame ke DuckDB
    con.register('dfRUPPP', dfRUPPP)
    con.register('dfRUPPS', dfRUPPS)
    con.register('dfRUPSA', dfRUPSA)

    # Baca dataset RUP 31 Mar jika tahun <= tahun sekarang
    if tahun <= datetime.now().year:
        try:
            dfRUPPP31 = read_df_duckdb(datasets['PP31'])
            dfRUPPS31 = read_df_duckdb(datasets['PS31'])
            dfRUPSA31 = read_df_duckdb(datasets['SA31'])
            # Register DataFrame 31 Mar ke DuckDB
            con.register('dfRUPPP31', dfRUPPP31)
            con.register('dfRUPPS31', dfRUPPS31)
            con.register('dfRUPSA31', dfRUPSA31)
            data_31mar_tersedia = True
        except Exception as e:
            data_31mar_tersedia = False
            # st.warning(f"Data 31 Maret {tahun} belum tersedia")
    else:
        data_31mar_tersedia = False
        st.info(f"Data 31 Maret {tahun} belum tersedia karena tahun yang dipilih adalah tahun yang akan datang")

    # Filter data RUP Penyedia
    dfRUPPP_umumkan = con.execute("SELECT * FROM dfRUPPP WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
    con.register('dfRUPPP_umumkan', dfRUPPP_umumkan)
    
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
    con.register('dfRUPPS_umumkan', dfRUPPS_umumkan)

    # Filter data RUP Penyedia 31 Mar jika tersedia
    if data_31mar_tersedia:
        dfRUPPP31_umumkan = con.execute("SELECT * FROM dfRUPPP31 WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
        dfRUPPS31_umumkan = con.execute("SELECT * FROM dfRUPPS31 WHERE status_umumkan_rup = 'Terumumkan'").df()
        con.register('dfRUPPP31_umumkan', dfRUPPP31_umumkan)
        con.register('dfRUPPS31_umumkan', dfRUPPS31_umumkan)

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
    queries = {
        'strukturanggaran': "SELECT nama_satker AS NAMA_SATKER, belanja_pengadaan AS STRUKTUR_ANGGARAN FROM dfRUPSA WHERE belanja_pengadaan > 0",
        'paketpenyedia': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_PENYEDIA FROM dfRUPPP_umumkan GROUP BY NAMA_SATKER",
        'paketswakelola': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_SWAKELOLA FROM dfRUPPS_umumkan GROUP BY NAMA_SATKER"
    }
    data = get_rup_data(queries, con)
    if not data.empty:
        display_rup_data(data, "PERSENTASE INPUT RUP", pilih, tahun)
    else:
        st.warning("Tidak ada data yang tersedia untuk ditampilkan")
    

with menu_rup_6:
    if tahun <= datetime.now().year:
        try:
            # Cek apakah data 31 Maret tersedia
            dfRUPPP31 = read_df_duckdb(datasets['PP31'])
            dfRUPPS31 = read_df_duckdb(datasets['PS31'])
            dfRUPSA31 = read_df_duckdb(datasets['SA31'])
            
            # Register DataFrame ke DuckDB
            con.register('dfRUPPP31', dfRUPPP31)
            con.register('dfRUPPS31', dfRUPPS31)
            con.register('dfRUPSA31', dfRUPSA31)
            
            # Filter data
            dfRUPPP31_umumkan = con.execute("SELECT * FROM dfRUPPP31 WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
            dfRUPPS31_umumkan = con.execute("SELECT * FROM dfRUPPS31 WHERE status_umumkan_rup = 'Terumumkan'").df()
            con.register('dfRUPPP31_umumkan', dfRUPPP31_umumkan)
            con.register('dfRUPPS31_umumkan', dfRUPPS31_umumkan)
            
            # Query dan tampilkan data
            queries31 = {
                'strukturanggaran31': "SELECT nama_satker AS NAMA_SATKER, belanja_pengadaan AS STRUKTUR_ANGGARAN FROM dfRUPSA31 WHERE belanja_pengadaan > 0",
                'paketpenyedia31': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_PENYEDIA FROM dfRUPPP31_umumkan GROUP BY NAMA_SATKER",
                'paketswakelola31': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_SWAKELOLA FROM dfRUPPS31_umumkan GROUP BY NAMA_SATKER"
            }
            data31 = get_rup_data(queries31, con)
            if not data31.empty:
                display_rup_data(data31, "PERSENTASE INPUT RUP (31 MAR)", pilih, tahun, " 31 Mar")
            else:
                st.warning("Data 31 Maret tidak memiliki entri yang dapat ditampilkan")
        except Exception as e:
            st.error("Data 31 Maret belum tersedia")
    else:
        st.info(f"Data 31 Maret {tahun} belum tersedia karena tahun yang dipilih adalah tahun yang akan datang")
    