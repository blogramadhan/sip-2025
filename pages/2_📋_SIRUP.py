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
    st.write(f"{pilih} TAHUN {tahun}")

with menu_rup_3:
    st.title("RUP PAKET PENYEDIA")
    st.write(f"{pilih} TAHUN {tahun}")

with menu_rup_4:
    st.title("RUP PAKET SWAKELOLA")
    st.header(f"{pilih} TAHUN {tahun}")

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

        ir_gabung_final = (dfs['strukturanggaran']
            .merge(dfs['paketpenyedia'], how='left', on='NAMA_SATKER')
            .merge(dfs['paketswakelola'], how='left', on='NAMA_SATKER')
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
        # Konfigurasi dan tampilkan grid
        gd = GridOptionsBuilder.from_dataframe(ir_gabung_final)
        
        # Set konfigurasi default dan kolom numerik
        gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, 
                                  aggFunc="sum", editable=True, autoSizeColumns=True)
        
        for col in ["STRUKTUR_ANGGARAN", "RUP_PENYEDIA", "RUP_SWAKELOLA", "TOTAL_RUP", "SELISIH"]:
            gd.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})")
        
        gd.configure_pagination()
        gd.configure_side_bar()
        gd.configure_selection('multiple')
        
        AgGrid(ir_gabung_final,
               gridOptions=gd.build(),
               enable_enterprise_modules=True, 
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               key='InputRUP')
 
    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_6:
    st.title("PERSENTASE INPUT RUP (31 MAR)")
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        # Baca dataset RUP 31 Mar
        dfRUPPP31 = read_df_duckdb(datasets['PP31'])
        dfRUPPS31 = read_df_duckdb(datasets['PS31'])
        dfRUPSA31 = read_df_duckdb(datasets['SA31'])

        dfRUPPP31_umumkan = con.execute("SELECT * FROM dfRUPPP31 WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
        dfRUPPS31_umumkan = con.execute("SELECT * FROM dfRUPPS31 WHERE status_umumkan_rup = 'Terumumkan'").df()

        # Query data dari database
        queries31 = {
            'strukturanggaran31': "SELECT nama_satker AS NAMA_SATKER, belanja_pengadaan AS STRUKTUR_ANGGARAN FROM dfRUPSA31 WHERE STRUKTUR_ANGGARAN > 0",
            'paketpenyedia31': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_PENYEDIA FROM dfRUPPP31_umumkan GROUP BY NAMA_SATKER",
            'paketswakelola31': "SELECT nama_satker AS NAMA_SATKER, SUM(pagu) AS RUP_SWAKELOLA FROM dfRUPPS31_umumkan GROUP BY NAMA_SATKER"
        }
        
        # Eksekusi query dan merge dataframe
        dfs31 = {k: con.execute(v).df() for k,v in queries31.items()}

        ir_gabung_final31 = (dfs31['strukturanggaran31']
            .merge(dfs31['paketpenyedia31'], how='left', on='NAMA_SATKER')
            .merge(dfs31['paketswakelola31'], how='left', on='NAMA_SATKER')
            .assign(TOTAL_RUP = lambda x: x.RUP_PENYEDIA + x.RUP_SWAKELOLA)
            .assign(SELISIH = lambda x: x.STRUKTUR_ANGGARAN - x.TOTAL_RUP)
            .assign(PERSEN = lambda x: round((x.TOTAL_RUP / x.STRUKTUR_ANGGARAN * 100), 2))
            .fillna(0))
        
        # Download button
        st.download_button(
            label="📥 Download  % Input RUP (31 Mar)",
            data=download_excel(ir_gabung_final31),
            file_name=f"TabelPersenInputRUP31Mar_{pilih}_{tahun}.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Tampilkan dataframe
        # Konfigurasi dan tampilkan grid
        gd31 = GridOptionsBuilder.from_dataframe(ir_gabung_final31)

        # Set konfigurasi default dan kolom numerik
        gd31.configure_default_column(groupable=True, value=True, enableRowGroup=True, 
                                  aggFunc="sum", editable=True, autoSizeColumns=True)
        
        for col in ["STRUKTUR_ANGGARAN", "RUP_PENYEDIA", "RUP_SWAKELOLA", "TOTAL_RUP", "SELISIH"]:
            gd31.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})")
            
        gd31.configure_pagination()
        gd31.configure_side_bar()
        gd31.configure_selection('multiple')

        AgGrid(ir_gabung_final31,
               gridOptions=gd31.build(),
               enable_enterprise_modules=True, 
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               key='InputRUP31Mar')

    except Exception as e:
        st.error(f"Error: {e}")