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

# URL Dataset Toko Daring
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'BELA': f"{base_url}/Bela-TokoDaringRealisasi{tahun}.parquet",
}

try:
    st.title("TRANSAKSI TOKO DARING")

    # Baca data dan siapkan unduhan
    dfBELA = read_df_duckdb(datasets['BELA'])

    # Tampilkan header dan tombol unduh
    col1, col2 = st.columns((7,3))
    col1.header(f"{pilih} - TAHUN {tahun}")
    col2.download_button(
        label="📥 Unduh Data Toko Daring",
        data=download_excel(dfBELA),
        file_name=f"TransaksiTokoDaring-{kodeFolder}-{tahun}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.divider()

    # Filter data
    col1, col2 = st.columns(2)
    with col1:
        status_verifikasi = st.radio("**Status Verifikasi**", ["Gabungan", "Verified", "Unverified"])
    with col2:
        status_ppmse = st.radio("**Status Konfirmasi PPMSE**", ["Gagal", "Selesai"])
    
    st.write(f"Filter aktif: **{status_verifikasi}** dan **{status_ppmse}**")

    # Query yang lebih ringkas
    query = "SELECT * FROM dfBELA WHERE LENGTH(nama_satker) > 1"
    
    if status_verifikasi != "Gabungan":
        query += f" AND status_verif = '{status_verifikasi.lower()}'"
    
    if status_ppmse.lower() == "selesai":
        query += " AND (status_konfirmasi_ppmse = 'selesai' OR status_konfirmasi_ppmse IS NULL)"
    else:
        query += f" AND status_konfirmasi_ppmse = '{status_ppmse.lower()}'"
    df_BELA_filter = con.execute(query).df()
    
    # Tampilkan metrik
    col1, col2 = st.columns(2)
    col1.metric(
        label="Jumlah Transaksi Toko Daring", 
        value="{:,}".format(df_BELA_filter['order_id'].nunique())
    )
    col2.metric(
        label="Nilai Transaksi Toko Daring", 
        value="{:,.2f}".format(df_BELA_filter['valuasi'].sum())
    )

    st.divider()

    # Visualisasi data berdasarkan Perangkat Daerah (10 Besar)
    with st.container(border=True):
        st.subheader("Berdasarkan Perangkat Daerah (10 Besar)")
        
        tab_pd_jumlah, tab_pd_nilai = st.tabs(["| Jumlah Transaksi |", "| Nilai Transaksi |"])
        
        # Tab Jumlah Transaksi Perangkat Daerah
        with tab_pd_jumlah:
            # Query data jumlah transaksi
            sql_jumlah_pd = """
                SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(order_id)) AS JUMLAH_TRANSAKSI
                FROM df_BELA_filter 
                WHERE nama_satker IS NOT NULL
                GROUP BY nama_satker 
                ORDER BY JUMLAH_TRANSAKSI DESC 
                LIMIT 10
            """
            df_jumlah_pd = con.execute(sql_jumlah_pd).df()
            
            # Tampilkan tabel dan grafik
            col_tabel, col_grafik = st.columns((4,6))
            with col_tabel:
                
                gd_pd_jumlah = GridOptionsBuilder.from_dataframe(df_jumlah_pd)
                gd_pd_jumlah.configure_default_column(autoSizeColumns=True)
                AgGrid(df_jumlah_pd, 
                    gridOptions=gd_pd_jumlah.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    autoSizeColumns=True,
                    width='100%',
                    height=min(350, 35 * (len(df_jumlah_pd) + 1)))

            with col_grafik:
                # Menggunakan grafik horizontal bar dengan warna gradien
                fig = px.bar(df_jumlah_pd, y='NAMA_SATKER', x='JUMLAH_TRANSAKSI', 
                             text_auto='.2s', title='Grafik Jumlah Transaksi Toko Daring Perangkat Daerah',
                             orientation='h', color='JUMLAH_TRANSAKSI', 
                             color_continuous_scale='Viridis',
                             template='plotly_white')
                fig.update_traces(textfont_size=12, textposition="outside", cliponaxis=False)
                fig.update_layout(
                    yaxis_title="Perangkat Daerah",
                    xaxis_title="Jumlah Transaksi",
                    coloraxis_showscale=False,
                    hoverlabel=dict(bgcolor="white", font_size=12),
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        # Tab Nilai Transaksi Perangkat Daerah
        with tab_pd_nilai:
            # Query data nilai transaksi
            sql_nilai_pd = """
                SELECT nama_satker AS NAMA_SATKER, SUM(valuasi) AS NILAI_TRANSAKSI
                FROM df_BELA_filter 
                WHERE nama_satker IS NOT NULL
                GROUP BY nama_satker 
                ORDER BY NILAI_TRANSAKSI DESC 
                LIMIT 10
            """
            df_nilai_pd = con.execute(sql_nilai_pd).df()
            
            # Tampilkan tabel dan grafik
            col_tabel, col_grafik = st.columns((4,6))
            with col_tabel:

                gd_pd_nilai = GridOptionsBuilder.from_dataframe(df_nilai_pd)
                gd_pd_nilai.configure_default_column(autoSizeColumns=True)
                gd_pd_nilai.configure_column("NILAI_TRANSAKSI", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                AgGrid(df_nilai_pd, 
                    gridOptions=gd_pd_nilai.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    width='100%',
                    height=min(350, 35 * (len(df_nilai_pd) + 1)))

            with col_grafik:
                # Menggunakan grafik horizontal bar dengan warna gradien
                fig = px.bar(df_nilai_pd, y='NAMA_SATKER', x='NILAI_TRANSAKSI', 
                             text_auto='.2s', title='Grafik Nilai Transaksi Toko Daring Perangkat Daerah',
                             orientation='h', color='NILAI_TRANSAKSI',
                             color_continuous_scale='Teal',
                             template='plotly_white')
                fig.update_traces(textfont_size=12, textposition="outside", cliponaxis=False)
                fig.update_layout(
                    yaxis_title="Perangkat Daerah",
                    xaxis_title="Nilai Transaksi (Rp)",
                    coloraxis_showscale=False,
                    hoverlabel=dict(bgcolor="white", font_size=12),
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Visualisasi data berdasarkan Pelaku Usaha (10 Besar)
    with st.container(border=True):
        st.subheader("Berdasarkan Pelaku Usaha (10 Besar)")
        
        tab_pu_jumlah, tab_pu_nilai = st.tabs(["| Jumlah Transaksi |", "| Nilai Transaksi |"])
        
        # Tab Jumlah Transaksi Pelaku Usaha
        with tab_pu_jumlah:
            # Query data jumlah transaksi
            sql_jumlah_pu = """
                SELECT nama_merchant AS NAMA_TOKO, COUNT(DISTINCT(order_id)) AS JUMLAH_TRANSAKSI
                FROM df_BELA_filter 
                WHERE nama_merchant IS NOT NULL
                GROUP BY nama_merchant 
                ORDER BY JUMLAH_TRANSAKSI DESC 
                LIMIT 10
            """
            df_jumlah_pu = con.execute(sql_jumlah_pu).df()
            
            # Tampilkan tabel dan grafik
            col_tabel, col_grafik = st.columns((4,6))
            with col_tabel:

                gd_pu_jumlah = GridOptionsBuilder.from_dataframe(df_jumlah_pu)
                gd_pu_jumlah.configure_default_column(autoSizeColumns=True)
                AgGrid(df_jumlah_pu, 
                    gridOptions=gd_pu_jumlah.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    autoSizeColumns=True,
                    width='100%',
                    height=min(350, 35 * (len(df_jumlah_pu) + 1)))
            
            with col_grafik:
                # Menggunakan grafik pie untuk variasi
                fig = px.pie(df_jumlah_pu, values='JUMLAH_TRANSAKSI', names='NAMA_TOKO',
                             title='Grafik Jumlah Transaksi Toko Daring Pelaku Usaha',
                             color_discrete_sequence=px.colors.sequential.Plasma_r,
                             hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label', 
                                 textfont_size=10, pull=[0.05 if i == 0 else 0 for i in range(len(df_jumlah_pu))])
                fig.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        # Tab Nilai Transaksi Pelaku Usaha
        with tab_pu_nilai:
            # Query data nilai transaksi
            sql_nilai_pu = """
                SELECT nama_merchant AS NAMA_TOKO, SUM(valuasi) AS NILAI_TRANSAKSI
                FROM df_BELA_filter 
                WHERE nama_merchant IS NOT NULL
                GROUP BY nama_merchant 
                ORDER BY NILAI_TRANSAKSI DESC 
                LIMIT 10
            """
            df_nilai_pu = con.execute(sql_nilai_pu).df()
            
            # Tampilkan tabel dan grafik
            col_tabel, col_grafik = st.columns((4,6))
            with col_tabel:

                gd_pu_nilai = GridOptionsBuilder.from_dataframe(df_nilai_pu)
                gd_pu_nilai.configure_default_column(autoSizeColumns=True)
                gd_pu_nilai.configure_column("NILAI_TRANSAKSI", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                AgGrid(df_nilai_pu, 
                    gridOptions=gd_pu_nilai.build(),
                    enable_enterprise_modules=True,
                    fit_columns_on_grid_load=True,
                    width='100%',
                    height=min(350, 35 * (len(df_nilai_pu) + 1)))
            
            with col_grafik:
                # Menggunakan grafik treemap untuk variasi
                fig = px.treemap(df_nilai_pu, path=['NAMA_TOKO'], values='NILAI_TRANSAKSI',
                                 title='Grafik Nilai Transaksi Toko Daring Pelaku Usaha',
                                 color='NILAI_TRANSAKSI', color_continuous_scale='RdBu')
                fig.update_traces(textinfo='label+value+percent', textfont_size=12)
                fig.update_layout(
                    margin=dict(l=10, r=10, t=50, b=10),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
