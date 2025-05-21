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

    # Berdasarkan Perangkat Daerah
    with st.container(border=True):
        st.subheader("Berdasarkan Perangkat Daerah (10 Besar)")

        tab1, tab2 = st.tabs(["| Jumlah Transaksi Perangkat Daerah |", "| Nilai Transaksi Perangkat Daerah |"])

        with tab1:
            tabel_jumlah_pd = con.execute("""
                SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(kd_paket)) AS JUMLAH_TRANSAKSI
                FROM df_ECATV6_filter
                WHERE NAMA_SATKER IS NOT NULL
                GROUP BY NAMA_SATKER
                ORDER BY JUMLAH_TRANSAKSI DESC
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))
            with col1:
                gd_jumlah_pd = GridOptionsBuilder.from_dataframe(tabel_jumlah_pd)
                gd_jumlah_pd.configure_default_column(autoSizeColumns=True)
                AgGrid(tabel_jumlah_pd, 
                    gridOptions=gd_jumlah_pd.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    autoSizeColumns=True,
                    width='100%',
                    height=min(350, 35 * (len(tabel_jumlah_pd) + 1)))
            with col2:  
                custom_colors = ['#00B4D8', '#0077B6', '#023E8A', '#0096C7', '#48CAE4', '#90E0EF', '#ADE8F4', '#CAF0F8', '#03045E', '#014F86']
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_jumlah_pd['NAMA_SATKER'],
                    y=tabel_jumlah_pd['JUMLAH_TRANSAKSI'],
                    text=tabel_jumlah_pd['JUMLAH_TRANSAKSI'],
                    textposition='outside',
                    marker=dict(
                        color=custom_colors[:len(tabel_jumlah_pd)],
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                        opacity=0.9
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
                ))
                fig.update_layout(
                    title='Jumlah Transaksi Perangkat Daerah',
                    xaxis_title='Perangkat Daerah',
                    yaxis_title='Jumlah Transaksi',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        with tab2:
            tabel_nilai_pd = con.execute("""
                SELECT nama_satker AS NAMA_SATKER, SUM(total_harga) AS NILAI_TRANSAKSI
                FROM df_ECATV6_filter
                WHERE NAMA_SATKER IS NOT NULL
                GROUP BY NAMA_SATKER
                ORDER BY NILAI_TRANSAKSI DESC
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))  
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_nilai_pd)
                gb.configure_default_column(autoSizeColumns=True)
                gb.configure_column("NILAI_TRANSAKSI", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")  
                
                AgGrid(tabel_nilai_pd, 
                    gridOptions=gb.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    width='100%',
                    height=min(350, 35 * (len(tabel_nilai_pd) + 1)))

            with col2:
                custom_colors = ['#9D4EDD', '#C77DFF', '#E0AAFF', '#7B2CBF', '#5A189A', '#3C096C', '#240046', '#10002B', '#E500A4', '#DB00B6']
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_nilai_pd['NAMA_SATKER'],
                    y=tabel_nilai_pd['NILAI_TRANSAKSI'],
                    text=tabel_nilai_pd['NILAI_TRANSAKSI'],
                    textposition='outside',
                    marker=dict(
                        color=custom_colors[:len(tabel_nilai_pd)],
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                        opacity=0.9
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Nilai: Rp %{y:,.2f}<extra></extra>'
                ))
                fig.update_layout(
                    title='Nilai Transaksi Perangkat Daerah',
                    xaxis_title='Perangkat Daerah',
                    yaxis_title='Nilai Transaksi',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)                

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
