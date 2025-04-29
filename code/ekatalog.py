# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import duckdb
import openpyxl
from datetime import datetime
from babel.numbers import format_currency
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo
from st_social_media_links import SocialMediaIcons
from fungsi import *

# Konfigurasi UKPBJ
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
base_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"
datasets = {
    'ECAT': f"{base_url}/Ecat-PaketEPurchasing{tahun}.parquet",
    'ECAT_KD': f"{base_url}/ECATKomoditasDetail{tahun}.parquet", 
    'ECAT_IS': f"{base_url}/Ecat-InstansiSatker{tahun}.parquet",
    'ECAT_PD': f"{base_url}/ECATPenyediaDetail{tahun}.parquet",
}

try:
    st.title("TRANSAKSI E-KATALOG")

    # Baca dan gabungkan dataset E-Katalog
    dfECAT = read_df_duckdb(datasets['ECAT'])
    dfECAT_OK = (dfECAT
                 .merge(read_df_duckdb(datasets['ECAT_KD']), how='left', on='kd_komoditas')
                 .drop('nama_satker', axis=1)
                 .merge(read_df_duckdb(datasets['ECAT_IS']), left_on='satker_id', right_on='kd_satker', how='left')
                 .merge(read_df_duckdb(datasets['ECAT_PD']), how='left', on='kd_penyedia'))

    # Header dan tombol unduh
    col1, col2 = st.columns([8,2])
    col1.header(f"{pilih} TAHUN {tahun}")
    col2.download_button(
        label="📥 Unduh E-Katalog",
        data=download_excel(dfECAT_OK),
        file_name=f"Transaksi_E-Katalog_{pilih}_{tahun}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.divider()

    # Filter options
    KATALOG_radio_1, KATALOG_radio_2, KATALOG_radio_3, KATALOG_radio_4 = st.columns((1,1,3,5))
    with KATALOG_radio_1:
        jenis_katalog_array = np.insert(dfECAT_OK['jenis_katalog'].unique(), 0, "Gabungan")
        jenis_katalog = st.radio("**Jenis Katalog**", jenis_katalog_array)
    with KATALOG_radio_2:
        nama_sumber_dana = st.radio("**Sumber Dana**", ["Gabungan", "APBD", "BLUD"])
    with KATALOG_radio_3:
        status_paket_array = np.insert(dfECAT_OK['status_paket'].unique(), 0, "Gabungan")
        status_paket = st.radio("**Status Paket**", status_paket_array)
    st.write(f"Anda memilih : **{status_paket}** dan **{jenis_katalog}** dan **{nama_sumber_dana}**")

    # Build filter query
    df_ECAT_filter_Query = "SELECT * FROM dfECAT_OK WHERE 1=1"
    if jenis_katalog != "Gabungan":
        df_ECAT_filter_Query += f" AND jenis_katalog = '{jenis_katalog}'"
    if nama_sumber_dana != "Gabungan":
        if "APBD" in nama_sumber_dana:
            df_ECAT_filter_Query += f" AND nama_sumber_dana LIKE '%APBD%'"
        else:
            df_ECAT_filter_Query += f" AND nama_sumber_dana = '{nama_sumber_dana}'"
    if status_paket != "Gabungan":
        df_ECAT_filter_Query += f" AND status_paket = '{status_paket}'"

    df_ECAT_filter = con.execute(df_ECAT_filter_Query).df()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Jumlah Produk Katalog", value="{:,}".format(df_ECAT_filter['kd_produk'].nunique()))
    col2.metric(label="Jumlah Penyedia Katalog", value="{:,}".format(df_ECAT_filter['kd_penyedia'].nunique()))
    col3.metric(label="Jumlah Transaksi Katalog", value="{:,}".format(df_ECAT_filter['no_paket'].nunique()))
    col4.metric(label="Nilai Transaksi Katalog", value="{:,.2f}".format(df_ECAT_filter['total_harga'].sum()))

    st.divider()

    # Berdasarkan Kualifikasi Usaha
    with st.container(border=True):
        st.subheader("Berdasarkan Kualifikasi Usaha")
        
        tab1, tab2 = st.tabs(["| Jumlah Transaksi Penyedia |", "| Nilai Transaksi Penyedia |"])
        
        with tab1:
            tabel_jumlah_ukm = con.execute("""
                SELECT penyedia_ukm AS PENYEDIA_UKM, COUNT(DISTINCT(kd_penyedia)) AS JUMLAH_UKM
                FROM df_ECAT_filter GROUP BY PENYEDIA_UKM
            """).df()
            
            col1, col2 = st.columns((3,7))
            with col1:
                gd_ukm_hitung = GridOptionsBuilder.from_dataframe(tabel_jumlah_ukm)
                gd_ukm_hitung.configure_default_column(autoSizeColumns=True)
                AgGrid(tabel_jumlah_ukm, 
                       gridOptions=gd_ukm_hitung.build(),
                       fit_columns_on_grid_load=True,
                       autoSizeColumns=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_jumlah_ukm) + 1)))
            with col2:
                fig = go.Figure(data=[go.Pie(
                    labels=tabel_jumlah_ukm['PENYEDIA_UKM'],
                    values=tabel_jumlah_ukm['JUMLAH_UKM'],
                    hole=.4,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Pastel, line=dict(color='#000000', width=1))
                )])
                fig.update_layout(
                    title='Grafik Jumlah Transaksi Katalog PENYEDIA UKM',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=50, b=50, l=10, r=10)
                )
                st.plotly_chart(fig, theme='streamlit', use_container_width=True)
        
        with tab2:
            tabel_nilai_ukm = con.execute("""
                SELECT penyedia_ukm AS PENYEDIA_UKM, SUM(total_harga) AS NILAI_UKM
                FROM df_ECAT_filter GROUP BY PENYEDIA_UKM
            """).df()
            
            col1, col2 = st.columns((3.5,6.5))
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_nilai_ukm)
                gb.configure_default_column(autoSizeColumns=True)
                gb.configure_column("NILAI_UKM", 
                                  type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                  valueGetter="data.NILAI_UKM.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                
                AgGrid(tabel_nilai_ukm, 
                       gridOptions=gb.build(),
                       enable_enterprise_modules=True,
                       fit_columns_on_grid_load=True,
                       width='100%',
                       height=min(350, 35 * (len(tabel_nilai_ukm) + 1)))
                
            with col2:
                fig = go.Figure(data=[go.Pie(
                    labels=tabel_nilai_ukm['PENYEDIA_UKM'],
                    values=tabel_nilai_ukm['NILAI_UKM'],
                    hole=.4,
                    textinfo='label+percent',
                    marker=dict(colors=px.colors.qualitative.Bold, line=dict(color='#000000', width=1))
                )])
                fig.update_layout(
                    title='Grafik Nilai Transaksi Katalog PENYEDIA UKM',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                    margin=dict(t=50, b=50, l=10, r=10)
                )
                st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    # Berdasarkan Nama Komoditas
    with st.container(border=True):
        st.subheader("Berdasarkan Nama Komoditas (10 Besar)")
        
        tab1, tab2 = st.tabs(["| Jumlah Transaksi Tiap Komoditas |", "| Nilai Transaksi Tiap Komoditas |"])
        
        with tab1:
            komoditas_filter = f"AND kd_instansi_katalog = '{kodeRUP}'" if jenis_katalog == "Lokal" else ""
            tabel_jumlah_komoditas = con.execute(f"""
                SELECT nama_komoditas AS NAMA_KOMODITAS, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                FROM df_ECAT_filter 
                WHERE NAMA_KOMODITAS IS NOT NULL {komoditas_filter}
                GROUP BY NAMA_KOMODITAS 
                ORDER BY JUMLAH_TRANSAKSI DESC 
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))
            with col1:
                gd_jumlah_komoditas = GridOptionsBuilder.from_dataframe(tabel_jumlah_komoditas)
                gd_jumlah_komoditas.configure_default_column(autoSizeColumns=True)
                AgGrid(tabel_jumlah_komoditas, 
                       gridOptions=gd_jumlah_komoditas.build(),
                       fit_columns_on_grid_load=True,
                       autoSizeColumns=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_jumlah_komoditas) + 1)))
            with col2:
                colors = px.colors.sequential.Viridis
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_jumlah_komoditas['NAMA_KOMODITAS'],
                    y=tabel_jumlah_komoditas['JUMLAH_TRANSAKSI'],
                    text=tabel_jumlah_komoditas['JUMLAH_TRANSAKSI'],
                    textposition='outside',
                    marker=dict(
                        color=colors,
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)')
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
                ))
                fig.update_layout(
                    title={
                        'text': 'Grafik Jumlah Transaksi e-Katalog - Nama Komoditas',
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18, color='#1f77b4')
                    },
                    xaxis_title='<b>Nama Komoditas</b>',
                    yaxis_title='<b>Jumlah Transaksi</b>',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        with tab2:
            komoditas_filter = f"AND kd_instansi_katalog = '{kodeRUP}'" if jenis_katalog == "Lokal" else ""
            tabel_nilai_komoditas = con.execute(f"""
                SELECT nama_komoditas AS NAMA_KOMODITAS, SUM(total_harga) AS NILAI_TRANSAKSI
                FROM df_ECAT_filter 
                WHERE NAMA_KOMODITAS IS NOT NULL {komoditas_filter}
                GROUP BY NAMA_KOMODITAS 
                ORDER BY NILAI_TRANSAKSI DESC 
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_nilai_komoditas)
                gb.configure_default_column(autoSizeColumns=True)
                gb.configure_column("NILAI_TRANSAKSI", 
                                  type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                  valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")    
                
                AgGrid(tabel_nilai_komoditas, 
                       gridOptions=gb.build(),
                       enable_enterprise_modules=True,
                       fit_columns_on_grid_load=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_nilai_komoditas) + 1)))
                
            with col2:
                colors = px.colors.sequential.Plasma
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_nilai_komoditas['NAMA_KOMODITAS'],
                    y=tabel_nilai_komoditas['NILAI_TRANSAKSI'],
                    text=[f'{x:,.0f}' for x in tabel_nilai_komoditas['NILAI_TRANSAKSI']],
                    textposition='outside',
                    marker=dict(
                        color=tabel_nilai_komoditas['NILAI_TRANSAKSI'],
                        colorscale='Bluered',
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)')
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Nilai: Rp %{y:,.0f}<extra></extra>'
                ))
                fig.update_layout(
                    title={
                        'text': 'Grafik Nilai Transaksi e-Katalog - Nama Komoditas',
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18, color='#1f77b4')
                    },
                    xaxis_title='<b>Nama Komoditas</b>',
                    yaxis_title='<b>Nilai Transaksi</b>',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Berdasarkan Perangkat Daerah
    with st.container(border=True):
        st.subheader("Berdasarkan Perangkat Daerah (10 Besar)")
        
        tab1, tab2 = st.tabs(["| Jumlah Transaksi Perangkat Daerah |", "| Nilai Transaksi Perangkat Daerah |"])
        
        with tab1:
            tabel_jumlah_pd = con.execute("""
                SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                FROM df_ECAT_filter 
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
                       fit_columns_on_grid_load=True,
                       autoSizeColumns=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_jumlah_pd) + 1)))
            with col2:
                colors = px.colors.qualitative.Prism
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_jumlah_pd['NAMA_SATKER'],
                    y=tabel_jumlah_pd['JUMLAH_TRANSAKSI'],
                    text=tabel_jumlah_pd['JUMLAH_TRANSAKSI'],
                    textposition='outside',
                    marker=dict(
                        color=colors[:len(tabel_jumlah_pd)],
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                        opacity=0.9
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
                ))
                fig.update_layout(
                    title={
                        'text': 'Grafik Jumlah Transaksi e-Katalog - Perangkat Daerah',
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18, color='#1f77b4')
                    },
                    xaxis_title='<b>Perangkat Daerah</b>',
                    yaxis_title='<b>Jumlah Transaksi</b>',
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
                FROM df_ECAT_filter 
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
                       height=min(400, 35 * (len(tabel_nilai_pd) + 1)))
                
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_nilai_pd['NAMA_SATKER'],
                    y=tabel_nilai_pd['NILAI_TRANSAKSI'],
                    text=[f'{x:,.0f}' for x in tabel_nilai_pd['NILAI_TRANSAKSI']],
                    textposition='outside',
                    marker=dict(
                        color=tabel_nilai_pd['NILAI_TRANSAKSI'],
                        colorscale='Tealrose',
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                        opacity=0.9
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Nilai: Rp %{y:,.0f}<extra></extra>'
                ))
                fig.update_layout(
                    title={
                        'text': 'Grafik Nilai Transaksi e-Katalog - Perangkat Daerah',
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18, color='#1f77b4')
                    },
                    xaxis_title='<b>Perangkat Daerah</b>',
                    yaxis_title='<b>Nilai Transaksi</b>',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # Berdasarkan Pelaku Usaha
    with st.container(border=True):
        st.subheader("Berdasarkan Pelaku Usaha (10 Besar)")
        
        tab1, tab2 = st.tabs(["| Jumlah Transaksi Pelaku Usaha |", "| Nilai Transaksi Pelaku Usaha |"])
        
        with tab1:
            tabel_jumlah_pu = con.execute("""
                SELECT nama_penyedia AS NAMA_PENYEDIA, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                FROM df_ECAT_filter 
                WHERE NAMA_PENYEDIA IS NOT NULL 
                GROUP BY NAMA_PENYEDIA 
                ORDER BY JUMLAH_TRANSAKSI DESC 
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))
            with col1:
                gd_jumlah_pu = GridOptionsBuilder.from_dataframe(tabel_jumlah_pu)
                gd_jumlah_pu.configure_default_column(autoSizeColumns=True)
                AgGrid(tabel_jumlah_pu, 
                       gridOptions=gd_jumlah_pu.build(),
                       enable_enterprise_modules=True,
                       fit_columns_on_grid_load=True,
                       autoSizeColumns=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_jumlah_pu) + 1)))
            with col2:                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_jumlah_pu['NAMA_PENYEDIA'],
                    y=tabel_jumlah_pu['JUMLAH_TRANSAKSI'],
                    text=tabel_jumlah_pu['JUMLAH_TRANSAKSI'],
                    textposition='outside',
                    marker=dict(
                        color=tabel_jumlah_pu['JUMLAH_TRANSAKSI'],
                        colorscale='Greens',
                        line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                        opacity=0.9
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
                ))
                fig.update_layout(
                    title={
                        'text': 'Grafik Jumlah Transaksi Katalog - Pelaku Usaha',
                        'y':0.95,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': dict(size=18, color='#1f77b4')
                    },
                    xaxis_title='<b>Pelaku Usaha</b>',
                    yaxis_title='<b>Jumlah Transaksi</b>',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=80, b=100, l=10, r=10),
                    showlegend=False
                )
                fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
                fig.update_yaxes(gridcolor='rgba(0,0,0,0.1)')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        
        with tab2:
            tabel_nilai_pu = con.execute("""
                SELECT nama_penyedia AS NAMA_PENYEDIA, SUM(total_harga) AS NILAI_TRANSAKSI
                FROM df_ECAT_filter 
                WHERE NAMA_PENYEDIA IS NOT NULL
                GROUP BY NAMA_PENYEDIA 
                ORDER BY NILAI_TRANSAKSI DESC 
                LIMIT 10
            """).df()
            
            col1, col2 = st.columns((4,6))
            with col1:
                gb = GridOptionsBuilder.from_dataframe(tabel_nilai_pu)
                gb.configure_default_column(autoSizeColumns=True)
                gb.configure_column("NILAI_TRANSAKSI", 
                                  type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                  valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                
                AgGrid(tabel_nilai_pu, 
                       gridOptions=gb.build(),
                       enable_enterprise_modules=True,
                       fit_columns_on_grid_load=True,
                       width='100%',
                       height=min(400, 35 * (len(tabel_nilai_pu) + 1)))
                
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=tabel_nilai_pu['NAMA_PENYEDIA'],
                    y=tabel_nilai_pu['NILAI_TRANSAKSI'],
                    text=[f'{x:,.0f}' for x in tabel_nilai_pu['NILAI_TRANSAKSI']],
                    textposition='outside',
                    marker=dict(
                        color=tabel_nilai_pu['NILAI_TRANSAKSI'],
                        colorscale='Oranges',
                        line=dict(
                            color='rgba(204, 85, 0, 1.0)',
                            width=1.5
                        ),
                        opacity=0.8
                    ),
                    hoverinfo='x+y',
                    hovertemplate='<b>%{x}</b><br>Nilai: Rp %{y:,.0f}<extra></extra>'
                ))
                fig.update_layout(
                    title='Grafik Nilai Transaksi Katalog - Pelaku Usaha',
                    xaxis_title='Pelaku Usaha',
                    yaxis_title='Nilai Transaksi',
                    xaxis={'categoryorder':'total descending'},
                    margin=dict(t=50, b=100, l=10, r=10)
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")