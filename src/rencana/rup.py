# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
from datetime import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards
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

# URL Dataset SIRUP
base_url = f"https://s3-sip.pbj.my.id/rup/{kodeRUP}"
datasets = {
    'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan/{tahun}/data.parquet",
    'PS': f"{base_url}/RUP-PaketSwakelola-Terumumkan/{tahun}/data.parquet", 
    'SA': f"{base_url}/RUP-StrukturAnggaranPD/{tahun}/data.parquet",
    'PP31': f"{base_url}/RUP-PaketPenyedia-Terumumkan/{tahun}/data31.parquet",
    'PS31': f"{base_url}/RUP-PaketSwakelola-Terumumkan/{tahun}/data31.parquet",
    'SA31': f"{base_url}/RUP-StrukturAnggaranPD/{tahun}/data31.parquet",
}

try:
    # Baca dataset RUP
    dfRUPPP = read_df_duckdb(datasets['PP'])
    dfRUPPS = read_df_duckdb(datasets['PS'])
    dfRUPSA = read_df_duckdb(datasets['SA'])
    # dfRUPPAP = read_df_duckdb(datasets['PAP'])

    # Filter data RUP Penyedia
    dfRUPPP_umumkan = con.execute("SELECT * FROM dfRUPPP WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'true' AND metode_pengadaan <> '0'").df()
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

    namaopd = con.execute("""
        SELECT DISTINCT nama_satker 
        FROM dfRUPPP_umumkan 
        ORDER BY nama_satker
    """).df()['nama_satker']

except Exception as e:
    st.error(f"Error: {e}")

#####
# Konten Data RUP
#####

st.title("RENCANA PENGADAAN")
st.header(f"{pilih} TAHUN {tahun}")

# Buat Tab Menu
menu_rup_1, menu_rup_2, menu_rup_3, menu_rup_4, menu_rup_5, menu_rup_6 = st.tabs([
    "📊 PROFIL RUP", "💰 STRUKTUR ANGGARAN", "📦 RUP PAKET PENYEDIA",
    "🏗️ RUP PAKET SWAKELOLA", "📈 PERSENTASE INPUT RUP", "📅 PERSENTASE INPUT RUP (31 MAR)"
])

with menu_rup_1:
    st.subheader("PROFIL RUP")

    try:
        # Tambahkan pilihan radio untuk memilih periode data
        periode_data = st.radio(
            "Pilih Periode Data:",
            ["Data Reguler", "31 Maret"],
            horizontal=True,
            key='periode_profil_rup'
        )
               
        # Load data berdasarkan pilihan periode
        if periode_data == "31 Maret":
            # Load data 31 Maret jika belum ada
            try:
                dfRUPPP31 = read_df_duckdb(datasets['PP31'])
                dfRUPPS31 = read_df_duckdb(datasets['PS31'])
                dfRUPSA31 = read_df_duckdb(datasets['SA31'])
                
                # Filter data 31 Maret
                dfRUPPP31_umumkan = con.execute("SELECT * FROM dfRUPPP31 WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'").df()
                dfRUPPS31_umumkan = con.execute("SELECT * FROM dfRUPPS31 WHERE status_umumkan_rup = 'Terumumkan'").df()
                
                # Set dataset yang akan digunakan
                dfRUPPP_source = dfRUPPP31_umumkan
                dfRUPPS_source = dfRUPPS31_umumkan
                dfRUPSA_source = dfRUPSA31
                
            except Exception as e:
                st.error(f"Error loading data 31 Maret: {e}")
                # Fallback ke data reguler
                dfRUPPP_source = dfRUPPP_umumkan
                dfRUPPS_source = dfRUPPS_umumkan
                dfRUPSA_source = dfRUPSA
        else:
            # Gunakan data reguler
            dfRUPPP_source = dfRUPPP_umumkan
            dfRUPPS_source = dfRUPPS_umumkan
            dfRUPSA_source = dfRUPSA
        
        # Tambahkan opsi "Semua Perangkat Daerah" di awal daftar
        opd_options = ["SEMUA PERANGKAT DAERAH"] + list(namaopd)
        opd = st.selectbox("Pilih Perangkat Daerah :", opd_options, key='rup_profil')

        if opd == "SEMUA PERANGKAT DAERAH":
            dfRUPPP_PD_Profil = dfRUPPP_source
            dfRUPPS_PD_Profil = dfRUPPS_source
            dfRUPSA_PD_Profil = dfRUPSA_source
        else:
            # Filter data berdasarkan perangkat daerah yang dipilih
            dfRUPPP_PD_Profil = dfRUPPP_source[dfRUPPP_source['nama_satker'] == opd]
            dfRUPPS_PD_Profil = dfRUPPS_source[dfRUPPS_source['nama_satker'] == opd]
            dfRUPSA_PD_Profil = dfRUPSA_source[dfRUPSA_source['nama_satker'] == opd]

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
        
        # Tentukan suffix file berdasarkan periode data
        file_suffix = "_31Mar" if periode_data == "31 Maret" else ""

        ProfilPD1, ProfilPD2, ProfilPD3 = st.columns((6,2,2))
        with ProfilPD1:
            st.subheader(f"{opd} - {periode_data}")
        with ProfilPD2:
            st.download_button(
                label="📥 Unduh RUP Paket Penyedia",
                data=unduh_RUPPP_PD_Profil,
                file_name=f"ProfilRUPPP_{opd}_{tahun}{file_suffix}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with ProfilPD3:
            st.download_button(
                label="📥 Unduh RUP Paket Swakelola",
                data=unduh_RUPPS_PD_Profil,
                file_name=f"ProfilRUPPS_{opd}_{tahun}{file_suffix}.xlsx",
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

        st.subheader(f"POSISI INPUT RUP - {periode_data}")

        jumlah_total_rup_pd = dfRUPPP_PD_Profil.shape[0] + dfRUPPS_PD_Profil.shape[0]
        nilai_total_rup_pd = dfRUPPP_PD_Profil['pagu'].sum() + dfRUPPS_PD_Profil['pagu'].sum()
        persen_capaian_rup_pd = nilai_total_rup_pd / belanja_pengadaan_pd

        colirpd11, colirpd12, colirpd13 = st.columns(3)
        colirpd11.subheader("Jumlah Total")
        colirpd12.metric(label="Jumlah Total Paket RUP", value="{:,}".format(jumlah_total_rup_pd))
        colirpd13.metric(label="Nilai Total Paket RUP", value="{:,.2f}".format(nilai_total_rup_pd))

        colirpd21, colirpd22, colirpd23 = st.columns(3)
        colirpd21.subheader("Paket Penyedia")
        colirpd22.metric(label="Jumlah Total Paket Penyedia", value="{:,}".format(dfRUPPP_PD_Profil.shape[0]))
        colirpd23.metric(label="Nilai Total Paket Penyedia", value="{:,.2f}".format(dfRUPPP_PD_Profil['pagu'].sum()))

        colirpd31, colirpd32, colirpd33 = st.columns(3)
        colirpd31.subheader("Paket Swakelola")
        colirpd32.metric(label="Jumlah Total Paket Swakelola", value="{:,}".format(dfRUPPS_PD_Profil.shape[0]))
        colirpd33.metric(label="Nilai Total Paket Swakelola", value="{:,.2f}".format(dfRUPPS_PD_Profil['pagu'].sum()))

        colirpd41, colirpd42, colirpd43 = st.columns(3)
        colirpd41.subheader("")
        colirpd42.subheader("")
        colirpd43.metric(label="Persentase Capaian RUP", value="{:.2%}".format(persen_capaian_rup_pd))

        st.divider()

        with st.container(border=True):

            st.subheader(f"STATUS UKM DAN PDN - {periode_data}")

            ### Tabel dan Grafik RUP Status UKM Perangkat Daerah
            grafik_rup_ukm_pd_tab_1, grafik_rup_ukm_pd_tab_2 = st.tabs(["📊 Jumlah Paket - UKM", "💰 Nilai Paket - UKM"])

            with grafik_rup_ukm_pd_tab_1:

                grafik_rup_ukm_pd_tab_1_1, grafik_rup_ukm_pd_tab_1_2 = st.columns((3,7))

                with grafik_rup_ukm_pd_tab_1_1:

                    gd_ukm_hitung = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_ukm_hitung)
                    gd_ukm_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(dfRUPPP_PD_ukm_hitung, 
                           gridOptions=gd_ukm_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(dfRUPPP_PD_ukm_hitung) + 1)))

                with grafik_rup_ukm_pd_tab_1_2:

                    # Membuat grafik pie yang lebih menarik dengan warna yang lebih cerah
                    figukmh = px.pie(
                        dfRUPPP_PD_ukm_hitung, 
                        values='JUMLAH_PAKET', 
                        names='STATUS_UKM', 
                        title='Grafik Status UKM - Jumlah Paket',
                        hole=.4,  # Memperbesar lubang di tengah untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih cerah
                        labels={'STATUS_UKM': 'Status UKM', 'JUMLAH_PAKET': 'Jumlah Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Menyesuaikan tampilan grafik
                    figukmh.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))  # Menambahkan garis putih di antara segmen
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figukmh, theme="streamlit", use_container_width=True)

            with grafik_rup_ukm_pd_tab_2:

                grafik_rup_ukm_pd_tab_2_1, grafik_rup_ukm_pd_tab_2_2 = st.columns((3,7))

                with grafik_rup_ukm_pd_tab_2_1:

                    gd_ukm_nilai = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_ukm_nilai)
                    gd_ukm_nilai.configure_default_column(autoSizeColumns=True)
                    gd_ukm_nilai.configure_column("NILAI_PAKET", 
                                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                              valueGetter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    AgGrid(dfRUPPP_PD_ukm_nilai, 
                           gridOptions=gd_ukm_nilai.build(),
                           enable_enterprise_modules=True,
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(dfRUPPP_PD_ukm_nilai) + 1)))

                with grafik_rup_ukm_pd_tab_2_2:

                    # Membuat grafik pie yang lebih menarik dengan warna yang lebih cerah
                    figukmn = px.pie(
                        dfRUPPP_PD_ukm_nilai, 
                        values='NILAI_PAKET', 
                        names='STATUS_UKM', 
                        title='Grafik Status UKM - Nilai Paket',
                        hole=.4,  # Memperbesar lubang di tengah untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih cerah
                        labels={'STATUS_UKM': 'Status UKM', 'NILAI_PAKET': 'Nilai Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Menyesuaikan tampilan grafik
                    figukmn.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))  # Menambahkan garis putih di antara segmen
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figukmn, theme="streamlit", use_container_width=True)

            st.divider()

            ### Tabel dan Grafik RUP Status PDN Perangkat Daerah
            grafik_rup_pdn_pd_tab_1, grafik_rup_pdn_pd_tab_2 = st.tabs(["📊 Jumlah Paket - PDN", "💰 Nilai Paket - PDN"])

            with grafik_rup_pdn_pd_tab_1:

                grafik_rup_pdn_pd_tab_1_1, grafik_rup_pdn_pd_tab_1_2 = st.columns((3,7))

                with grafik_rup_pdn_pd_tab_1_1:

                    gd_pdn_hitung = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_pdn_hitung)
                    gd_pdn_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(dfRUPPP_PD_pdn_hitung, 
                           gridOptions=gd_pdn_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(dfRUPPP_PD_pdn_hitung) + 1)))

                with grafik_rup_pdn_pd_tab_1_2:

                    # Membuat grafik pie yang lebih menarik dengan warna yang lebih cerah
                    figpdnh = px.pie(
                        dfRUPPP_PD_pdn_hitung, 
                        values='JUMLAH_PAKET', 
                        names='STATUS_PDN', 
                        title='Grafik Status PDN - Jumlah Paket',
                        hole=.4,  # Memperbesar lubang di tengah untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih cerah
                        labels={'STATUS_PDN': 'Status PDN', 'JUMLAH_PAKET': 'Jumlah Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Menyesuaikan tampilan grafik
                    figpdnh.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))  # Menambahkan garis putih di antara segmen
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figpdnh, theme="streamlit", use_container_width=True)

            with grafik_rup_pdn_pd_tab_2:

                grafik_rup_pdn_pd_tab_2_1, grafik_rup_pdn_pd_tab_2_2 = st.columns((3,7))

                with grafik_rup_pdn_pd_tab_2_1:

                    gd_pdn_nilai = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_pdn_nilai)
                    gd_pdn_nilai.configure_default_column(autoSizeColumns=True)
                    gd_pdn_nilai.configure_column("NILAI_PAKET", 
                                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                              valueGetter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    AgGrid(dfRUPPP_PD_pdn_nilai, 
                           gridOptions=gd_pdn_nilai.build(),
                           enable_enterprise_modules=True,
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(dfRUPPP_PD_pdn_nilai) + 1)))

                with grafik_rup_pdn_pd_tab_2_2:

                    # Membuat grafik pie yang lebih menarik dengan warna yang lebih cerah
                    figpdnn = px.pie(
                        dfRUPPP_PD_pdn_nilai, 
                        values='NILAI_PAKET', 
                        names='STATUS_PDN', 
                        title='Grafik Status PDN - Nilai Paket',
                        hole=.4,  # Memperbesar lubang di tengah untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih cerah
                        labels={'STATUS_PDN': 'Status PDN', 'NILAI_PAKET': 'Nilai Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Menyesuaikan tampilan grafik
                    figpdnn.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))  # Menambahkan garis putih di antara segmen
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figpdnn, theme="streamlit", use_container_width=True)
            
        with st.container(border=True):

            st.subheader(f"BERDASARKAN METODE PENGADAAN - {periode_data}")

            ### Tabel dan Grafik RUP Berdasarkan Metode Pengadaan Perangkat Daerah
            grafik_rup_mp_pd_tab_1, grafik_rup_mp_pd_tab_2 = st.tabs(["📊 Jumlah Paket - MP", "💰 Nilai Paket - MP"])

            with grafik_rup_mp_pd_tab_1:

                grafik_rup_mp_pd_tab_1_1, grafik_rup_mp_pd_tab_1_2 = st.columns((3,7))

                with grafik_rup_mp_pd_tab_1_1:

                    gd_mp_hitung = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_mp_hitung)
                    gd_mp_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(dfRUPPP_PD_mp_hitung, 
                           gridOptions=gd_mp_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=35 * (len(dfRUPPP_PD_mp_hitung) + 1))

                with grafik_rup_mp_pd_tab_1_2:

                    # Membuat grafik pie yang lebih menarik dengan warna yang lebih cerah
                    figmph = px.pie(
                        dfRUPPP_PD_mp_hitung, 
                        values='JUMLAH_PAKET', 
                        names='METODE_PENGADAAN', 
                        title='Grafik Metode Pengadaan - Jumlah Paket',
                        hole=.4,  # Memperbesar lubang di tengah untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih cerah
                        labels={'METODE_PENGADAAN': 'Metode Pengadaan', 'JUMLAH_PAKET': 'Jumlah Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Menyesuaikan tampilan grafik
                    figmph.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))  # Menambahkan garis putih di antara segmen
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figmph, theme="streamlit", use_container_width=True)

            with grafik_rup_mp_pd_tab_2:

                grafik_rup_mp_pd_tab_2_1, grafik_rup_mp_pd_tab_2_2 = st.columns((3,7))

                with grafik_rup_mp_pd_tab_2_1:

                    gd_mp_nilai = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_mp_nilai)
                    gd_mp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_mp_nilai.configure_column("NILAI_PAKET", 
                                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                              valueGetter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    AgGrid(dfRUPPP_PD_mp_nilai, 
                           gridOptions=gd_mp_nilai.build(),
                           enable_enterprise_modules=True,
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=35 * (len(dfRUPPP_PD_mp_nilai) + 1))
            
                with grafik_rup_mp_pd_tab_2_2:

                    # Membuat grafik pie yang lebih menarik dengan warna dan layout yang lebih baik
                    figmpn = px.pie(
                        dfRUPPP_PD_mp_nilai, 
                        values='NILAI_PAKET', 
                        names='METODE_PENGADAAN', 
                        title='Grafik Metode Pengadaan - Nilai Paket',
                        hole=.4,  # Memperbesar hole untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Vivid,  # Menggunakan palet warna yang lebih menarik
                        labels={'METODE_PENGADAAN': 'Metode Pengadaan', 'NILAI_PAKET': 'Nilai Paket (Rp.)'}  # Label yang lebih deskriptif
                    )
                    
                    # Memperbaiki tampilan grafik
                    figmpn.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figmpn, theme='streamlit', use_container_width=True)

        with st.container(border=True):
        
            st.subheader(f"BERDASARKAN JENIS PENGADAAN - {periode_data}")

            ### Tabel dan Grafik RUP Berdasarkan jenis pengadaan Perangkat Daerah
            grafik_rup_jp_pd_tab_1, grafik_rup_jp_pd_tab_2 = st.tabs(["📊 Jumlah Paket - JP", "💰 Nilai Paket - JP"])

            with grafik_rup_jp_pd_tab_1:

                grafik_rup_jp_pd_tab_1_1, grafik_rup_jp_pd_tab_1_2 = st.columns((3,7))

                with grafik_rup_jp_pd_tab_1_1:

                    gd_jp_hitung = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_jp_hitung)
                    gd_jp_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(dfRUPPP_PD_jp_hitung, 
                           gridOptions=gd_jp_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=35 * (len(dfRUPPP_PD_jp_hitung) + 1))

                with grafik_rup_jp_pd_tab_1_2:

                    # Membuat grafik pie yang lebih menarik dengan warna dan layout yang lebih baik
                    figjph = px.pie(
                        dfRUPPP_PD_jp_hitung, 
                        values='JUMLAH_PAKET', 
                        names='JENIS_PENGADAAN', 
                        title='Grafik Jenis Pengadaan - Jumlah Paket',
                        hole=.4,  # Memperbesar hole untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih menarik
                        labels={'JENIS_PENGADAAN': 'Jenis Pengadaan', 'JUMLAH_PAKET': 'Jumlah Paket'}  # Label yang lebih deskriptif
                    )
                    
                    # Memperbaiki tampilan grafik
                    figjph.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figjph, theme="streamlit", use_container_width=True)

            with grafik_rup_jp_pd_tab_2:

                grafik_rup_jp_pd_tab_2_1, grafik_rup_jp_pd_tab_2_2 = st.columns((3,7))

                with grafik_rup_jp_pd_tab_2_1:

                    gd_jp_nilai = GridOptionsBuilder.from_dataframe(dfRUPPP_PD_jp_nilai)
                    gd_jp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_jp_nilai.configure_column("NILAI_PAKET", 
                                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                              valueGetter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    AgGrid(dfRUPPP_PD_jp_nilai, 
                           gridOptions=gd_jp_nilai.build(),
                           enable_enterprise_modules=True,
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=35 * (len(dfRUPPP_PD_jp_nilai) + 1))

                with grafik_rup_jp_pd_tab_2_2:

                    # Membuat grafik pie yang lebih menarik dengan warna dan layout yang lebih baik
                    figjpn = px.pie(
                        dfRUPPP_PD_jp_nilai, 
                        values='NILAI_PAKET', 
                        names='JENIS_PENGADAAN', 
                        title='Grafik Jenis Pengadaan - Nilai Paket',
                        hole=.4,  # Memperbesar hole untuk tampilan donat yang lebih menarik
                        color_discrete_sequence=px.colors.qualitative.Bold,  # Menggunakan palet warna yang lebih menarik
                        labels={'JENIS_PENGADAAN': 'Jenis Pengadaan', 'NILAI_PAKET': 'Nilai Paket (Rp)'}  # Label yang lebih deskriptif
                    )
                    
                    # Memperbaiki tampilan grafik
                    figjpn.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        marker=dict(line=dict(color='#FFFFFF', width=2))
                    )
                    
                    # Menampilkan grafik dengan ukuran otomatis mengikuti lebar kolom
                    st.plotly_chart(figjpn, theme='streamlit', use_container_width=True)
        
    except Exception as e:
        st.error(f"Error: {e}")
   

with menu_rup_2:
    st.subheader("STRUKTUR ANGGARAN")

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
        gdsa.configure_default_column(autoSizeColumns=True)
        
        for col in ["BELANJA_OPERASI", "BELANJA_MODAL", "BELANJA_BTT", "BELANJA_NON_PENGADAAN", "BELANJA_PENGADAAN", "TOTAL_BELANJA"]:
            gdsa.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style:'currency',currency:'IDR',maximumFractionDigits:2}})")

        AgGrid(df_sa, 
               gridOptions=gdsa.build(), 
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               enable_enterprise_modules=True,
               width='100%',
               height=800,
               key='StrukturAnggaran')

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_3:
    st.subheader("RUP PAKET PENYEDIA")

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
        gdpp.configure_default_column(autoSizeColumns=True)
        gdpp.configure_column("PAGU", 
                          type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                          valueGetter="data.PAGU.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
        
        # Tampilkan grid
        AgGrid(df_pp,
               gridOptions=gdpp.build(),
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               enable_enterprise_modules=True,
               width='100%',
               height=800,
               key='RUPPP_PD')

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_4:
    st.subheader("RUP PAKET SWAKELOLA")

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
        gdps.configure_default_column(autoSizeColumns=True)
        gdps.configure_column("PAGU", 
                          type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                          valueGetter="data.PAGU.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
        
        # Tampilkan grid
        AgGrid(df_ps,
               gridOptions=gdps.build(),
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               enable_enterprise_modules=True,
               width='100%',
               height=800,
               key='RUPPS_PS')

    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_5:
    st.subheader("PERSENTASE INPUT RUP")

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
        gd.configure_default_column(autoSizeColumns=True)
        
        for col in ["STRUKTUR_ANGGARAN", "RUP_PENYEDIA", "RUP_SWAKELOLA", "TOTAL_RUP", "SELISIH"]:
            gd.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})")
           
        AgGrid(ir_gabung_final,
               gridOptions=gd.build(),
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               enable_enterprise_modules=True,
               width='100%',
               height=800,
               key='InputRUP')
 
    except Exception as e:
        st.error(f"Error: {e}")

with menu_rup_6:
    st.subheader("PERSENTASE INPUT RUP (31 MAR)")

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
        gd31.configure_default_column(autoSizeColumns=True)
        
        for col in ["STRUKTUR_ANGGARAN", "RUP_PENYEDIA", "RUP_SWAKELOLA", "TOTAL_RUP", "SELISIH"]:
            gd31.configure_column(col, 
                              type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                              valueGetter=f"data.{col}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})")
        
        AgGrid(ir_gabung_final31,
               gridOptions=gd31.build(),
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               enable_enterprise_modules=True,
               width='100%',
               height=800,
               key='InputRUP31Mar')

    except Exception as e:
        st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")