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

def init_page():
    page_config()
    logo()

def get_dataset_urls(kode_rup, tahun):
    base_url = f"https://data.pbj.my.id/{kode_rup}/sirup"
    return {
        'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan{tahun}.parquet",
        'PS': f"{base_url}/RUP-PaketSwakelola-Terumumkan{tahun}.parquet", 
        'SA': f"{base_url}/RUP-StrukturAnggaranPD{tahun}.parquet",
        'PP31': f"{base_url}/RUP-PaketPenyedia-Terumumkan-{tahun}-03-31.parquet",
        'PS31': f"{base_url}/RUP-PaketSwakelola-Terumumkan-{tahun}-03-31.parquet",
        'SA31': f"{base_url}/RUP-StrukturAnggaranPD-{tahun}-03-31.parquet"
    }

def load_regular_data(con, datasets):
    """Load dan register data RUP reguler"""
    dfRUPPP = read_df_duckdb(datasets['PP'])
    dfRUPPS = read_df_duckdb(datasets['PS'])
    dfRUPSA = read_df_duckdb(datasets['SA'])
    
    con.register('dfRUPPP', dfRUPPP)
    con.register('dfRUPPS', dfRUPPS)
    con.register('dfRUPSA', dfRUPSA)
    
    return process_regular_data(con)

def process_regular_data(con):
    """Proses dan filter data RUP reguler"""
    dfRUPPP_umumkan = con.execute("""
        SELECT * FROM dfRUPPP 
        WHERE status_umumkan_rup = 'Terumumkan' 
        AND status_aktif_rup = 'TRUE' 
        AND metode_pengadaan <> '0'
    """).df()
    con.register('dfRUPPP_umumkan', dfRUPPP_umumkan)
    
    dfRUPPS_umumkan = con.execute("""
        SELECT nama_satker, kd_rup, nama_paket, pagu, tipe_swakelola, 
               volume_pekerjaan, uraian_pekerjaan, tgl_pengumuman_paket, 
               tgl_awal_pelaksanaan_kontrak, nama_ppk, status_umumkan_rup
        FROM dfRUPPS 
        WHERE status_umumkan_rup = 'Terumumkan'
    """).df()
    con.register('dfRUPPS_umumkan', dfRUPPS_umumkan)
    
    return dfRUPPP_umumkan, dfRUPPS_umumkan

def load_march_data(con, datasets, tahun):
    """Load dan register data RUP 31 Maret"""
    if tahun > datetime.now().year:
        return False
        
    try:
        dfRUPPP31 = read_df_duckdb(datasets['PP31'])
        dfRUPPS31 = read_df_duckdb(datasets['PS31'])
        dfRUPSA31 = read_df_duckdb(datasets['SA31'])
        
        con.register('dfRUPPP31', dfRUPPP31)
        con.register('dfRUPPS31', dfRUPPS31)
        con.register('dfRUPSA31', dfRUPSA31)
        
        process_march_data(con)
        return True
    except Exception:
        return False

def process_march_data(con):
    """Proses dan filter data RUP 31 Maret"""
    dfRUPPP31_umumkan = con.execute("""
        SELECT * FROM dfRUPPP31 
        WHERE status_umumkan_rup = 'Terumumkan' 
        AND status_aktif_rup = 'TRUE' 
        AND metode_pengadaan <> '0'
    """).df()
    dfRUPPS31_umumkan = con.execute("SELECT * FROM dfRUPPS31 WHERE status_umumkan_rup = 'Terumumkan'").df()
    
    con.register('dfRUPPP31_umumkan', dfRUPPP31_umumkan)
    con.register('dfRUPPS31_umumkan', dfRUPPS31_umumkan)

def display_tabs(pilih, tahun, con, data_31mar_tersedia):
    menu_tabs = st.tabs([
        "| PROFIL RUP |", "| STRUKTUR ANGGARAN |", "| RUP PAKET PENYEDIA |",
        "| RUP PAKET SWAKELOLA |", "| PERSENTASE INPUT RUP |", "| PERSENTASE INPUT RUP (31 MAR) |"
    ])
    
    with menu_tabs[0]:
        st.title("PROFIL RUP")
        st.write("Profil RUP")
    
    with menu_tabs[4]:  # Tab Persentase Input RUP
        display_percentage_tab(con, pilih, tahun)
    
    with menu_tabs[5]:  # Tab Persentase Input RUP 31 MAR
        display_march_percentage_tab(con, pilih, tahun, data_31mar_tersedia)

def display_percentage_tab(con, pilih, tahun):
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

def display_march_percentage_tab(con, pilih, tahun, data_31mar_tersedia):
    if not data_31mar_tersedia:
        st.info(f"Data 31 Maret {tahun} belum tersedia")
        return
        
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

def main():
    init_page()
    
    # Setup awal
    daerah = region_config()
    pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
    tahun = st.sidebar.selectbox("Pilih Tahun", range(datetime.now().year, datetime.now().year-3, -1))
    
    selected_daerah = daerah.get(pilih, {})
    datasets = get_dataset_urls(selected_daerah.get("RUP"), tahun)
    
    # Inisialisasi DuckDB
    con = duckdb.connect(database=':memory:')
    
    try:
        # Load dan proses data
        dfRUPPP_umumkan, dfRUPPS_umumkan = load_regular_data(con, datasets)
        data_31mar_tersedia = load_march_data(con, datasets, tahun)
        
        # Tampilkan UI
        display_tabs(pilih, tahun, con, data_31mar_tersedia)
        
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
    