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
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        opd = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='rup_profil')

        dfRUPPP_PD_Profil = con.execute(f"SELECT * FROM dfRUPPP_umumkan WHERE nama_satker = '{opd}'").df()
        dfRUPPS_PD_Profil = con.execute(f"SELECT * FROM dfRUPPS_umumkan WHERE nama_satker = '{opd}'").df()
        dfRUPSA_PD_Profil = con.execute(f"SELECT * FROM dfRUPSA WHERE nama_satker = '{opd}'").df()

        dfRUPPP_PD_mp_hitung = con.execute("SELECT metode_pengadaan AS METODE_PENGADAAN, COUNT(metode_pengadaan) AS JUMLAH_PAKET FROM dfRUPPP_PD_Profil WHERE metode_pengadaan IS NOT NULL GROUP BY metode_pengadaan").df()
        dfRUPPP_PD_mp_nilai = con.execute("SELECT metode_pengadaan AS METODE_PENGADAAN, SUM(pagu) AS NILAI_PAKET FROM dfRUPPP_PD_Profil WHERE metode_pengadaan IS NOT NULL GROUP BY metode_pengadaan").df()
        dfRUPPP_PD_jp_hitung = con.execute("SELECT jenis_pengadaan AS JENIS_PENGADAAN, COUNT(jenis_pengadaan) AS JUMLAH_PAKET FROM dfRUPPP_PD_Profil WHERE jenis_pengadaan IS NOT NULL GROUP BY jenis_pengadaan").df()
        dfRUPPP_PD_jp_nilai = con.execute("SELECT jenis_pengadaan AS JENIS_PENGADAAN, SUM(pagu) AS NILAI_PAKET FROM dfRUPPP_PD_Profil WHERE jenis_pengadaan IS NOT NULL GROUP BY Jenis_pengadaan").df()
        dfRUPPP_PD_ukm_hitung = con.execute("SELECT status_ukm AS STATUS_UKM, COUNT(status_ukm) AS JUMLAH_PAKET FROM dfRUPPP_PD_Profil WHERE status_ukm IS NOT NULL GROUP BY status_ukm").df()
        dfRUPPP_PD_ukm_nilai = con.execute("SELECT status_ukm AS STATUS_UKM, SUM(pagu) AS NILAI_PAKET FROM dfRUPPP_PD_Profil WHERE status_ukm IS NOT NULL GROUP BY status_ukm").df()
        dfRUPPP_PD_pdn_hitung = con.execute("SELECT status_pdn AS STATUS_PDN, COUNT(status_pdn) AS JUMLAH_PAKET FROM dfRUPPP_PD_Profil WHERE status_pdn IS NOT NULL GROUP BY status_pdn").df()
        dfRUPPP_PD_pdn_nilai = con.execute("SELECT status_pdn AS STATUS_PDN, SUM(pagu) AS NILAI_PAKET FROM dfRUPPP_PD_Profil WHERE status_pdn IS NOT NULL GROUP BY status_pdn").df()

        ### Unduh Dataframe Analisa Profil RUP Daerah Perangkat Daerah
        unduh_RUPPP_PD_Profil = download_excel(dfRUPPP_PD_Profil)
        unduh_RUPPS_PD_Profil = download_excel(dfRUPPS_PD_Profil)       

        ProfilPD1, ProfilPD2, ProfilPD3 = st.columns((6,2,2))
        with ProfilPD1:
            st.subheader(f"{opd}")
        with ProfilPD2:
            st.download_button(
                label="📥 Unduh RUP Paket Penyedia",
                data=unduh_RUPPP_PD_Profil,
                file_name=f"ProfilRUPPP_{opd}_{tahun}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with ProfilPD3:
            st.download_button(
                label="📥 Unduh RUP Paket Swakelola",
                data=unduh_RUPPS_PD_Profil,
                file_name=f"ProfilRUPPS_{opd}_{tahun}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.divider()

        st.subheader("STRUKTUR ANGGARAN")

        belanja_pengadaan_pd = dfRUPSA_PD_Profil['belanja_pengadaan'].sum()
        belanja_operasional_pd = dfRUPSA_PD_Profil['belanja_operasi'].sum()
        belanja_modal_pd = dfRUPSA_PD_Profil['belanja_modal'].sum()
        belanja_total_pd = belanja_operasional_pd + belanja_modal_pd

        colsapd11, colsapd12, colsapd13 = st.columns(3)
        colsapd11.metric(label="Belanja Operasional", value="{:,.2f}".format(belanja_operasional_pd))
        colsapd12.metric(label="Belanja Modal", value="{:,.2f}".format(belanja_modal_pd))
        colsapd13.metric(label="Belanja Pengadaan", value="{:,.2f}".format(belanja_total_pd))  

        st.divider() 
            
        
    except Exception as e:
        st.error(f"Error: {e}")
   

with menu_rup_2:
    st.title("STRUKTUR ANGGARAN")
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        # Query dan tampilkan data
        df_sa = con.execute("""
            SELECT nama_satker AS NAMA_SATKER,
                   SUM(belanja_operasi) AS BELANJA_OPERASI,
                   SUM(belanja_modal) AS BELANJA_MODAL, 
                   SUM(belanja_btt) AS BELANJA_BTT,
                   SUM(belanja_non_pengadaan) AS BELANJA_NON_PENGADAAN,
                   SUM(belanja_pengadaan) AS BELANJA_PENGADAAN,
                   SUM(total_belanja) AS TOTAL_BELANJA
            FROM dfRUPSA WHERE BELANJA_PENGADAAN > 0
            GROUP BY nama_satker ORDER BY total_belanja DESC""").df()

        # Setup grid
        gdsa = GridOptionsBuilder.from_dataframe(df_sa)
        gdsa.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                  aggFunc="sum", editable=True, autoSizeColumns=True)
        
        for col in ["BELANJA_OPERASI", "BELANJA_MODAL", "BELANJA_BTT", "BELANJA_NON_PENGADAAN", "BELANJA_PENGADAAN", "TOTAL_BELANJA"]:
            gdsa.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style:'currency',currency:'IDR',maximumFractionDigits:2}})")
        
        gdsa.configure_pagination(paginationAutoPageSize=False)  # Set lebih banyak baris per halaman

        AgGrid(df_sa, 
               gridOptions=gdsa.build(), 
               enable_enterprise_modules=True,
               update_mode=GridUpdateMode.MODEL_CHANGED, 
               fit_columns_on_grid_load=True,
               height=800,
               key='StrukturAnggaran')

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_3:
    st.title("RUP PAKET PENYEDIA")
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        # Pilih Perangkat Daerah
        rup_pp = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='rup_pp')
        st.divider()
        st.subheader(rup_pp)
        
        # Ambil data RUP Paket Penyedia untuk PD yang dipilih
        dfRUPPP_PD = con.execute(f"SELECT * FROM dfRUPPP_umumkan WHERE nama_satker = '{rup_pp}'").df()
        
        # Tombol unduh data
        unduhRUPPP_PD = download_excel(dfRUPPP_PD)
        st.download_button(
            label="📥 Unduh RUP PAKET PENYEDIA",
            data=unduhRUPPP_PD,
            file_name=f"RUP_PAKET_PENYEDIA_{rup_pp}_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Query dan tampilkan data dalam grid
        df_pp = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, kd_rup AS ID_RUP, metode_pengadaan AS METODE_PEMILIHAN, 
                   jenis_pengadaan AS JENIS_PENGADAAN, status_pradipa AS STATUS_PRADIPA, 
                   status_pdn AS STATUS_PDN, status_ukm AS STATUS_UKM, 
                   tgl_pengumuman_paket AS TANGGAL_PENGUMUMAN, 
                   tgl_awal_pemilihan AS TANGGAL_RENCANA_PEMILIHAN, pagu AS PAGU 
            FROM dfRUPPP_PD
        """).df()
        
        # Konfigurasi grid
        gdpp = GridOptionsBuilder.from_dataframe(df_pp)
        gdpp.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                  aggFunc="sum", editable=True, autoSizeColumns=True)
        gdpp.configure_column("PAGU", 
                          type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                          valueGetter="data.PAGU.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
        gdpp.configure_pagination(paginationAutoPageSize=False)
        
        # Tampilkan grid
        AgGrid(df_pp,
               gridOptions=gdpp.build(),
               enable_enterprise_modules=True,
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               height=800,
               key='RUPPP_PD')

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_4:
    st.title("RUP PAKET SWAKELOLA")
    st.header(f"{pilih} TAHUN {tahun}")

    try:
        # Pilih Perangkat Daerah
        rup_ps = st.selectbox("Pilih Perangkat Daerah :", namaopd, key='rup_ps')
        st.divider()
        st.subheader(rup_ps)
        
        # Ambil data RUP Paket Penyedia untuk PD yang dipilih
        dfRUPPS_PD = con.execute(f"SELECT * FROM dfRUPPS_umumkan WHERE nama_satker = '{rup_ps}'").df()
        
        # Tombol unduh data
        unduhRUPPS_PD = download_excel(dfRUPPS_PD)
        st.download_button(
            label="📥 Unduh RUP PAKET SWAKELOLA",
            data=unduhRUPPS_PD,
            file_name=f"RUP_PAKET_SWAKELOLA_{rup_ps}_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Query dan tampilkan data dalam grid
        df_ps = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, kd_rup AS ID_RUP, tipe_swakelola AS TIPE_SWAKELOLA, 
                   tgl_pengumuman_paket AS TANGGAL_PENGUMUMAN, tgl_awal_pelaksanaan_kontrak AS TANGGAL_PELAKSANAAN,
                   pagu AS PAGU 
            FROM dfRUPPS_PD
        """).df()
        
        # Konfigurasi grid
        gdps = GridOptionsBuilder.from_dataframe(df_ps)
        gdps.configure_default_column(groupable=True, value=True, enableRowGroup=True,
                                  aggFunc="sum", editable=True, autoSizeColumns=True)
        gdps.configure_column("PAGU", 
                          type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                          valueGetter="data.PAGU.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
        gdps.configure_pagination(paginationAutoPageSize=False)
        
        # Tampilkan grid
        AgGrid(df_ps,
               gridOptions=gdps.build(),
               enable_enterprise_modules=True,
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               height=800,
               key='RUPPS_PS')

    except Exception as e:
        st.error(f"Error: {e}")

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
            label="📥 Unduh  % Input RUP",
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
        
        gd.configure_pagination(paginationAutoPageSize=False)
           
        AgGrid(ir_gabung_final,
               gridOptions=gd.build(),
               enable_enterprise_modules=True, 
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               height=800,
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
            label="📥 Unduh  % Input RUP (31 Mar)",
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
            
        gd31.configure_pagination(paginationAutoPageSize=False)
        
        AgGrid(ir_gabung_final31,
               gridOptions=gd31.build(),
               enable_enterprise_modules=True, 
               update_mode=GridUpdateMode.MODEL_CHANGED,
               fit_columns_on_grid_load=True,
               height=800,
               key='InputRUP31Mar')

    except Exception as e:
        st.error(f"Error: {e}")