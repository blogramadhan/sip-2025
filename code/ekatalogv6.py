# Impor Library yang Dibutuhkan
# Library Utama untuk Manipulasi Data dan Visualisasi
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
import openpyxl
from datetime import datetime
# Library untuk Tabel Interaktif
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Library untuk Tampilan Metrik
from streamlit_extras.metric_cards import style_metric_cards
# Library Fungsi Tambahan
from fungsi import *

# Konfigurasi UKPBJ dan Tahun
daerah = region_config()
pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
tahun = st.sidebar.selectbox("Pilih Tahun", range(datetime.now().year, datetime.now().year-3, -1))
selected_daerah = daerah.get(pilih, {})
kodeFolder = selected_daerah.get("folder")
kodeRUP = selected_daerah.get("RUP")
kodeLPSE = selected_daerah.get("LPSE")

# Inisialisasi Koneksi Database
con = duckdb.connect(database=':memory:')

# Menyiapkan URL untuk Dataset
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'ECATV6': f"{base_url}/Ecat-PaketEPurchasingV6{tahun}.parquet",
}

# Tampilan Judul Halaman
st.title("TRANSAKSI E-KATALOG VERSI 6")
st.header(f"{pilih} - TAHUN {tahun}")

st.divider()

try:
    # Membaca Data E-Katalog V6
    dfECATV6 = read_df_duckdb(datasets['ECATV6'])

    # Menampilkan Header dan Tombol Unduh
    col1, col2 = st.columns([8,2])
    col1.subheader("TRANSAKSI E-KATALOG V6")
    col2.download_button(
        label="📥 Unduh Transaksi E-Katalog V6",
        data=download_excel(dfECATV6),
        file_name=f"Transaksi_E-Katalog_V6_{pilih}_{tahun}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    # Filter Data dengan Radio Button
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

    # Membangun Query Filter
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

    # Menampilkan Metrik Utama   
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Jumlah Produk Katalog", value="{:,}".format(df_ECATV6_filter['jml_jenis_produk'].sum()))
    col2.metric(label="Jumlah Transaksi Katalog", value="{:,}".format(df_ECATV6_filter['kd_paket'].nunique()))
    col3.metric(label="Nilai Transaksi Katalog", value="{:,.2f}".format(df_ECATV6_filter['total_harga'].sum()))

    st.divider()

    # Analisis Berdasarkan Perangkat Daerah
    with st.container(border=True):
        st.subheader("Berdasarkan Perangkat Daerah (10 Besar)")

        tab1, tab2 = st.tabs(["| Jumlah Transaksi Perangkat Daerah |", "| Nilai Transaksi Perangkat Daerah |"])

        # Query untuk Data Perangkat Daerah
        tabel_jumlah_pd = con.execute("""
            SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(kd_paket)) AS JUMLAH_TRANSAKSI
            FROM df_ECATV6_filter
            WHERE nama_satker IS NOT NULL
            GROUP BY nama_satker
            ORDER BY JUMLAH_TRANSAKSI DESC
            LIMIT 10
        """).df()

        tabel_nilai_pd = con.execute("""
            SELECT nama_satker AS NAMA_SATKER, SUM(total_harga) AS NILAI_TRANSAKSI
            FROM df_ECATV6_filter
            WHERE nama_satker IS NOT NULL
            GROUP BY nama_satker
            ORDER BY NILAI_TRANSAKSI DESC
            LIMIT 10
        """).df()

        # Tab untuk Jumlah Transaksi
        with tab1:
            col1, col2 = st.columns((4,6))
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_jumlah_pd)
                gb.configure_default_column(autoSizeColumns=True)
                AgGrid(tabel_jumlah_pd, 
                    gridOptions=gb.build(),
                    fit_columns_on_grid_load=True,
                    enable_enterprise_modules=True,
                    width='100%',
                    height=min(350, 35 * (len(tabel_jumlah_pd) + 1)))
            
            with col2:
                fig = px.bar(tabel_jumlah_pd, 
                    x='NAMA_SATKER', 
                    y='JUMLAH_TRANSAKSI',
                    text='JUMLAH_TRANSAKSI',
                    title='Jumlah Transaksi per Perangkat Daerah',
                    color_discrete_sequence=['#00B4D8']*10)
                fig.update_layout(
                    xaxis_title='Perangkat Daerah',
                    yaxis_title='Jumlah Transaksi',
                    xaxis={'categoryorder':'total descending'},
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        # Tab untuk Nilai Transaksi  
        with tab2:
            col1, col2 = st.columns((4,6))
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_nilai_pd)
                gb.configure_column("NILAI_TRANSAKSI", 
                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                AgGrid(tabel_nilai_pd,
                    gridOptions=gb.build(),
                    fit_columns_on_grid_load=True,
                    enable_enterprise_modules=True,
                    width='100%',
                    height=min(350, 35 * (len(tabel_nilai_pd) + 1)))

            with col2:
                fig = px.bar(tabel_nilai_pd,
                    x='NAMA_SATKER',
                    y='NILAI_TRANSAKSI', 
                    text='NILAI_TRANSAKSI',
                    title='Nilai Transaksi per Perangkat Daerah',
                    color_discrete_sequence=['#9D4EDD']*10)
                fig.update_layout(
                    xaxis_title='Perangkat Daerah',
                    yaxis_title='Nilai Transaksi',
                    xaxis={'categoryorder':'total descending'},
                    showlegend=False
                )
                fig.update_traces(texttemplate='Rp %{text:,.0f}')
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")

# Mengatur Tampilan Kartu Metrik
style_metric_cards(background_color="#000", border_left_color="#D3D3D3")