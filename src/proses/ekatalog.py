# Library Utama
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import duckdb
from datetime import datetime
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
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

# URL Dataset Katalog
base_url = f"https://s3-sip.pbj.my.id/katalog/{kodeRUP}"
datasets = {
    'ECAT': f"{base_url}/Ecat-PaketEPurchasing/{tahun}/data.parquet",
    'ECAT_KD': f"{base_url}/Ecat-KomoditasDetail/{tahun}/data.parquet", 
    'ECAT_IS': f"{base_url}/Ecat-InstansiSatker/{tahun}/data.parquet",
    'ECAT_PD': f"{base_url}/Ecat-PenyediaDetail/{tahun}/data.parquet",
}

# URL Dataset RUP
base_url_rup = f"https://s3-sip.pbj.my.id/rup/{kodeRUP}"
datasets_rup = {
    'PP': f"{base_url_rup}/RUP-PaketPenyedia-Terumumkan/{tahun}/data.parquet",
}

st.title("TRANSAKSI E-KATALOG VERSI 5")
st.header(f"{pilih} - TAHUN {tahun}")

menu_purchasing_1_1, menu_purchasing_1_2, menu_purchasing_1_3 = st.tabs(["🛍️ TRANSAKSI KATALOG", "🏷️ TRANSAKSI KATALOG (ETALASE)", "📊 TABEL NILAI ETALASE"])

try:
    with menu_purchasing_1_1:

        # Baca dataset RUP
        dfRUPPP = read_df_duckdb(datasets_rup['PP'])[['kd_rup', 'status_pdn', 'status_ukm']]
        dfRUPPP['kd_rup'] = dfRUPPP['kd_rup'].astype(str)

        # Baca dan gabungkan dataset E-Katalog
        dfECAT = read_df_duckdb(datasets['ECAT'])
        dfECAT['kd_rup'] = dfECAT['kd_rup'].astype(str)

        dfECAT_OK = (dfECAT
                    .merge(read_df_duckdb(datasets['ECAT_KD']), how='left', on='kd_komoditas')
                    .drop('nama_satker', axis=1)
                    .merge(read_df_duckdb(datasets['ECAT_IS']), left_on='satker_id', right_on='kd_satker', how='left')
                    .merge(read_df_duckdb(datasets['ECAT_PD']), how='left', on='kd_penyedia'))
        
        dfECAT_OK = dfECAT_OK.merge(dfRUPPP, how='left', on='kd_rup')
        dfECAT_OK['status_pdn'] = dfECAT_OK['status_pdn'].fillna('Tanpa Status')
        dfECAT_OK['status_ukm'] = dfECAT_OK['status_ukm'].fillna('Tanpa Status')

        # Header dan tombol unduh
        col1, col2 = st.columns([8,2])
        col1.subheader("TRANSAKSI E-KATALOG")
        col2.download_button(
            label="📥 Transaksi E-Katalog",
            data=download_excel(dfECAT_OK),
            file_name=f"Transaksi_E-Katalog_{pilih}_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.divider()

        # Filter options
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")
            KATALOG_select_1, KATALOG_select_2, KATALOG_select_3, KATALOG_select_4, KATALOG_select_5 = st.columns((1, 1, 1, 1, 1.5))
            with KATALOG_select_1:
                jenis_katalog_array = np.insert(dfECAT_OK['jenis_katalog'].unique(), 0, "Gabungan")
                jenis_katalog = st.selectbox("🗂️ Jenis Katalog", jenis_katalog_array, key="Ekatalog_Jenis_Katalog")
            with KATALOG_select_2:
                nama_sumber_dana = st.selectbox("💵 Sumber Dana", ["Gabungan", "APBD", "BLUD"], key="Ekatalog_Sumber_Dana")
            with KATALOG_select_3:
                status_pdn_array = np.insert(dfECAT_OK['status_pdn'].unique(), 0, "Gabungan")
                status_pdn = st.selectbox("🏭 Status PDN", status_pdn_array, key="Ekatalog_Status_PDN")
            with KATALOG_select_4:
                status_ukm_array = np.insert(dfECAT_OK['status_ukm'].unique(), 0, "Gabungan")
                status_ukm = st.selectbox("🏪 Status UKM", status_ukm_array, key="Ekatalog_Status_UKM")
            with KATALOG_select_5:
                status_paket_array = np.insert(dfECAT_OK['status_paket'].unique(), 0, "Gabungan")
                status_paket = st.selectbox("📦 Status Paket", status_paket_array, key="Ekatalog_Status_Paket")

        st.write(f"Anda memilih : **{status_paket}**, **{jenis_katalog}**, **{nama_sumber_dana}**, **{status_pdn}**, **{status_ukm}**")

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
        if status_pdn != "Gabungan":
            df_ECAT_filter_Query += f" AND status_pdn = '{status_pdn}'"
        if status_ukm != "Gabungan":
            df_ECAT_filter_Query += f" AND status_ukm = '{status_ukm}'"

        df_ECAT_filter = con.execute(df_ECAT_filter_Query).df()

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Jumlah Produk Katalog", value="{:,}".format(df_ECAT_filter['kd_produk'].nunique()))
        col2.metric(label="Jumlah Penyedia Katalog", value="{:,}".format(df_ECAT_filter['kd_penyedia'].nunique()))
        col3.metric(label="Jumlah Transaksi Katalog", value="{:,}".format(df_ECAT_filter['no_paket'].nunique()))
        col4.metric(label="Nilai Transaksi Katalog", value="{:,.2f}".format(df_ECAT_filter['total_harga'].sum()))

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()

        # Berdasarkan Kualifikasi Usaha
        with st.container(border=True):
            st.subheader("Berdasarkan Kualifikasi Usaha")
            
            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi Penyedia", "💰 Nilai Transaksi Penyedia"])
            
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
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jumlah_ukm) + 1)))
                    
                with col2:
                    fig = go.Figure(data=[go.Pie(
                        labels=tabel_jumlah_ukm['PENYEDIA_UKM'],
                        values=tabel_jumlah_ukm['JUMLAH_UKM'],
                        hole=.4,
                        textinfo='label+percent',
                        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'], line=dict(color='#000000', width=1))
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
                
                col1, col2 = st.columns((3,7))
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
                        marker=dict(colors=['#6A0572', '#AB83A1', '#F7A072', '#57C5B6', '#159895'], line=dict(color='#000000', width=1))
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
            
            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi Tiap Komoditas", "💰 Nilai Transaksi Tiap Komoditas"])
            
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
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_jumlah_komoditas = GridOptionsBuilder.from_dataframe(tabel_jumlah_komoditas)
                    gd_jumlah_komoditas.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_jumlah_komoditas, 
                        gridOptions=gd_jumlah_komoditas.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jumlah_komoditas) + 1)))
                    
                with col2:
                    custom_colors = ['#FF9671', '#FFC75F', '#F9F871', '#D65DB1', '#845EC2', '#0089BA', '#008F7A', '#2C73D2', '#0081CF', '#C34A36']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_jumlah_komoditas['NAMA_KOMODITAS'],
                        y=tabel_jumlah_komoditas['JUMLAH_TRANSAKSI'],
                        text=tabel_jumlah_komoditas['JUMLAH_TRANSAKSI'],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_jumlah_komoditas)],
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
                
                col1, col2 = st.columns((3,7))
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
                        height=min(350, 35 * (len(tabel_nilai_komoditas) + 1)))
                    
                with col2:
                    custom_colors = ['#3A86FF', '#FF006E', '#FB5607', '#FFBE0B', '#8338EC', '#06D6A0', '#118AB2', '#073B4C', '#7209B7', '#4CC9F0']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_nilai_komoditas['NAMA_KOMODITAS'],
                        y=tabel_nilai_komoditas['NILAI_TRANSAKSI'],
                        text=[f'{x:,.0f}' for x in tabel_nilai_komoditas['NILAI_TRANSAKSI']],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_nilai_komoditas)],
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
            
            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi Perangkat Daerah", "💰 Nilai Transaksi Perangkat Daerah"])
            
            with tab1:
                tabel_jumlah_pd = con.execute("""
                    SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                    FROM df_ECAT_filter 
                    WHERE NAMA_SATKER IS NOT NULL 
                    GROUP BY NAMA_SATKER 
                    ORDER BY JUMLAH_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
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
                
                col1, col2 = st.columns((3,7))
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
                        text=[f'{x:,.0f}' for x in tabel_nilai_pd['NILAI_TRANSAKSI']],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_nilai_pd)],
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
            
            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi Pelaku Usaha", "💰 Nilai Transaksi Pelaku Usaha"])
            
            with tab1:
                tabel_jumlah_pu = con.execute("""
                    SELECT nama_penyedia AS NAMA_PENYEDIA, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                    FROM df_ECAT_filter 
                    WHERE NAMA_PENYEDIA IS NOT NULL 
                    GROUP BY NAMA_PENYEDIA 
                    ORDER BY JUMLAH_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_jumlah_pu = GridOptionsBuilder.from_dataframe(tabel_jumlah_pu)
                    gd_jumlah_pu.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_jumlah_pu, 
                        gridOptions=gd_jumlah_pu.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jumlah_pu) + 1)))
                with col2:                
                    custom_colors = ['#588157', '#3A5A40', '#344E41', '#4F772D', '#90A955', '#A3B18A', '#B5C99A', '#DAD7CD', '#606C38', '#283618']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_jumlah_pu['NAMA_PENYEDIA'],
                        y=tabel_jumlah_pu['JUMLAH_TRANSAKSI'],
                        text=tabel_jumlah_pu['JUMLAH_TRANSAKSI'],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_jumlah_pu)],
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
                        height=min(350, 35 * (len(tabel_nilai_pu) + 1)))
                    
                with col2:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_nilai_pu['NAMA_PENYEDIA'],
                        y=tabel_nilai_pu['NILAI_TRANSAKSI'],
                        text=[f'{x:,.0f}' for x in tabel_nilai_pu['NILAI_TRANSAKSI']],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_nilai_pu)],
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

    with menu_purchasing_1_2:
        # Header dan tombol unduh
        etalase1, etalase2 = st.columns((8,2))
        with etalase1:
            st.subheader("TRANSAKSI E-KATALOG (ETALASE)")
        with etalase2:
            st.download_button(
                label="📥 Transaksi E-Katalog (Etalase)",
                data=download_excel(dfECAT_OK),
                file_name=f"TransaksiEKATALOG-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key="Download_Katalog_Etalase"
            )

        st.divider()

        # Filter data
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")
            col_filter1, col_filter2, col_filter3 = st.columns((1, 1, 1))
            
            with col_filter1:
                jenis_katalog_array = np.insert(dfECAT_OK['jenis_katalog'].unique(), 0, "Gabungan")
                jenis_katalog_etalase = st.selectbox("🗂️ Jenis Katalog", jenis_katalog_array, key="Etalase_Jenis_Katalog")
            
            with col_filter2:
                nama_sumber_dana_etalase = st.selectbox("💵 Sumber Dana", ["Gabungan", "APBD", "BLUD"], key="Etalase_Sumber_Dana")
            
            with col_filter3:
                status_paket_array = np.insert(dfECAT_OK['status_paket'].unique(), 0, "Gabungan")
                status_paket_etalase = st.selectbox("📦 Status Paket", status_paket_array, key="Etalase_Status_Paket")

        # Query data berdasarkan filter
        df_ECAT_ETALASE_Query = "SELECT * FROM dfECAT_OK WHERE 1=1"
        
        if jenis_katalog_etalase != "Gabungan":
            df_ECAT_ETALASE_Query += f" AND jenis_katalog = '{jenis_katalog_etalase}'"
        
        if nama_sumber_dana_etalase != "Gabungan":
            if "APBD" in nama_sumber_dana_etalase:
                df_ECAT_ETALASE_Query += f" AND nama_sumber_dana LIKE '%APBD%'"
            else:
                df_ECAT_ETALASE_Query += f" AND nama_sumber_dana = '{nama_sumber_dana_etalase}'"
        
        if status_paket_etalase != "Gabungan":
            df_ECAT_ETALASE_Query += f" AND status_paket = '{status_paket_etalase}'"

        df_ECAT_ETALASE = con.execute(df_ECAT_ETALASE_Query).df()

        nama_komoditas = st.selectbox("🏷️ Etalase Belanja", df_ECAT_ETALASE['nama_komoditas'].unique(), key="Etalase_Nama_Komoditas")
        
        st.write(f"Filter: **{jenis_katalog_etalase}** | **{nama_sumber_dana_etalase}** | **{status_paket_etalase}**")

        # Filter data berdasarkan komoditas
        df_ECAT_ETALASE_filter = con.execute(f"SELECT * FROM df_ECAT_ETALASE WHERE nama_komoditas = '{nama_komoditas}'").df()

        # Hitung metrik
        jumlah_produk = df_ECAT_ETALASE_filter['kd_produk'].nunique()
        jumlah_penyedia = df_ECAT_ETALASE_filter['kd_penyedia'].nunique()
        jumlah_trx = df_ECAT_ETALASE_filter['no_paket'].nunique()
        nilai_trx = df_ECAT_ETALASE_filter['total_harga'].sum()

        # Tampilkan metrik
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Jumlah Produk", value=f"{jumlah_produk:,}")
        col2.metric(label="Jumlah Penyedia", value=f"{jumlah_penyedia:,}")
        col3.metric(label="Jumlah Transaksi", value=f"{jumlah_trx:,}")
        col4.metric(label="Nilai Transaksi", value=f"Rp {nilai_trx:,.2f}")

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()

        # Analisis berdasarkan Kualifikasi Usaha
        with st.container(border=True):
            st.subheader("Berdasarkan Kualifikasi Usaha")

            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi Penyedia", "💰 Nilai Transaksi Penyedia"])

            with tab1:
                tabel_etalase_jumlah_ukm = con.execute("""
                    SELECT penyedia_ukm AS PENYEDIA_UKM, COUNT(DISTINCT(kd_penyedia)) AS JUMLAH_UKM
                    FROM df_ECAT_ETALASE_filter GROUP BY PENYEDIA_UKM
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_etalase_jumlah_ukm = GridOptionsBuilder.from_dataframe(tabel_etalase_jumlah_ukm)
                    gd_etalase_jumlah_ukm.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_etalase_jumlah_ukm, 
                        gridOptions=gd_etalase_jumlah_ukm.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_jumlah_ukm) + 1)))
                    
                with col2:
                    fig = go.Figure(data=[go.Pie(
                        labels=tabel_etalase_jumlah_ukm['PENYEDIA_UKM'],
                        values=tabel_etalase_jumlah_ukm['JUMLAH_UKM'],
                        hole=.4,
                        textinfo='label+percent',
                        marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'], line=dict(color='#000000', width=1))
                    )])
                    fig.update_layout(
                        title='Grafik Jumlah Transaksi Katalog PENYEDIA UKM',
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                        margin=dict(t=50, b=50, l=10, r=10)
                    )
                    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
            
            with tab2:
                tabel_etalase_nilai_ukm = con.execute("""
                    SELECT penyedia_ukm AS PENYEDIA_UKM, SUM(total_harga) AS NILAI_UKM
                    FROM df_ECAT_ETALASE_filter GROUP BY PENYEDIA_UKM
                """).df()
                
                col1, col2 = st.columns((3.5,6.5))
                with col1:
                    gb_etalase_nilai_ukm = GridOptionsBuilder.from_dataframe(tabel_etalase_nilai_ukm)
                    gb_etalase_nilai_ukm.configure_default_column(autoSizeColumns=True)
                    gb_etalase_nilai_ukm.configure_column("NILAI_UKM", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_UKM.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    
                    AgGrid(tabel_etalase_nilai_ukm, 
                        gridOptions=gb_etalase_nilai_ukm.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_nilai_ukm) + 1)))
                    
                with col2:
                    fig = go.Figure(data=[go.Pie(
                        labels=tabel_etalase_nilai_ukm['PENYEDIA_UKM'],
                        values=tabel_etalase_nilai_ukm['NILAI_UKM'],
                        hole=.4,
                        textinfo='label+percent',
                        marker=dict(colors=['#6A0572', '#AB83A1', '#F7A072', '#57C5B6', '#159895'], line=dict(color='#000000', width=1))
                    )])
                    fig.update_layout(
                        title='Grafik Nilai Transaksi Katalog PENYEDIA UKM',
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                        margin=dict(t=50, b=50, l=10, r=10)
                    )
                    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

        # Analisis berdasarkan Perangkat Daerah
        with st.container(border=True):
            st.subheader("Berdasarkan Perangkat Daerah (10 Besar)")

            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi", "💰 Nilai Transaksi"])
            
            with tab1:
                tabel_etalase_jumlah_pd = con.execute("""
                    SELECT nama_satker AS NAMA_SATKER, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                    FROM df_ECAT_ETALASE_filter 
                    WHERE NAMA_SATKER IS NOT NULL 
                    GROUP BY NAMA_SATKER 
                    ORDER BY JUMLAH_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_etalase_jumlah_pd = GridOptionsBuilder.from_dataframe(tabel_etalase_jumlah_pd)
                    gd_etalase_jumlah_pd.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_etalase_jumlah_pd, 
                        gridOptions=gd_etalase_jumlah_pd.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_jumlah_pd) + 1)))
                    
                with col2:
                    custom_colors = ['#00B4D8', '#0077B6', '#023E8A', '#0096C7', '#48CAE4', '#90E0EF', '#ADE8F4', '#CAF0F8', '#03045E', '#014F86']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_etalase_jumlah_pd['NAMA_SATKER'],
                        y=tabel_etalase_jumlah_pd['JUMLAH_TRANSAKSI'],
                        text=tabel_etalase_jumlah_pd['JUMLAH_TRANSAKSI'],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_etalase_jumlah_pd)],
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
                tabel_etalase_nilai_pd = con.execute("""
                    SELECT nama_satker AS NAMA_SATKER, SUM(total_harga) AS NILAI_TRANSAKSI
                    FROM df_ECAT_ETALASE_filter 
                    WHERE NAMA_SATKER IS NOT NULL
                    GROUP BY NAMA_SATKER 
                    ORDER BY NILAI_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gb_etalase_nilai_pd = GridOptionsBuilder.from_dataframe(tabel_etalase_nilai_pd)  
                    gb_etalase_nilai_pd.configure_default_column(autoSizeColumns=True)
                    gb_etalase_nilai_pd.configure_column("NILAI_TRANSAKSI", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    
                    AgGrid(tabel_etalase_nilai_pd, 
                        gridOptions=gb_etalase_nilai_pd.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_nilai_pd) + 1)))
                    
                with col2:
                    custom_colors = ['#9D4EDD', '#C77DFF', '#E0AAFF', '#7B2CBF', '#5A189A', '#3C096C', '#240046', '#10002B', '#E500A4', '#DB00B6']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_etalase_nilai_pd['NAMA_SATKER'],
                        y=tabel_etalase_nilai_pd['NILAI_TRANSAKSI'],
                        text=[f'{x:,.0f}' for x in tabel_etalase_nilai_pd['NILAI_TRANSAKSI']],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_etalase_nilai_pd)],
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

        # Analisis berdasarkan Pelaku Usaha
        with st.container(border=True):

            st.subheader("Berdasarkan Pelaku Usaha (10 Besar)")
            
            tab1, tab2 = st.tabs(["📊 Jumlah Transaksi", "💰 Nilai Transaksi"])
            
            with tab1:
                # Query data jumlah transaksi
                tabel_etalase_jumlah_pu = con.execute("""
                    SELECT nama_penyedia AS NAMA_PENYEDIA, COUNT(DISTINCT(no_paket)) AS JUMLAH_TRANSAKSI
                    FROM df_ECAT_ETALASE_filter 
                    WHERE NAMA_PENYEDIA IS NOT NULL
                    GROUP BY NAMA_PENYEDIA 
                    ORDER BY JUMLAH_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_etalase_jumlah_pu = GridOptionsBuilder.from_dataframe(tabel_etalase_jumlah_pu)
                    gd_etalase_jumlah_pu.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_etalase_jumlah_pu, 
                        gridOptions=gd_etalase_jumlah_pu.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_jumlah_pu) + 1)))
                        
                with col2:
                    custom_colors = ['#9D4EDD', '#C77DFF', '#E0AAFF', '#7B2CBF', '#5A189A', '#3C096C', '#240046', '#10002B', '#E500A4', '#DB00B6']
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_etalase_jumlah_pu['NAMA_PENYEDIA'],
                        y=tabel_etalase_jumlah_pu['JUMLAH_TRANSAKSI'],
                        text=tabel_etalase_jumlah_pu['JUMLAH_TRANSAKSI'],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_etalase_jumlah_pu)],
                            line=dict(width=1.5, color='rgba(0,0,0,0.5)'),
                            opacity=0.9
                        ),
                        hoverinfo='x+y',
                        hovertemplate='<b>%{x}</b><br>Jumlah: %{y}<extra></extra>'
                    ))
                    fig.update_layout(
                        title={
                            'text': 'Grafik Jumlah Transaksi Katalog per Pelaku Usaha',
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
                # Query data nilai transaksi
                tabel_etalase_nilai_pu = con.execute("""
                    SELECT nama_penyedia AS NAMA_PENYEDIA, SUM(total_harga) AS NILAI_TRANSAKSI
                    FROM df_ECAT_ETALASE_filter 
                    WHERE NAMA_PENYEDIA IS NOT NULL
                    GROUP BY NAMA_PENYEDIA 
                    ORDER BY NILAI_TRANSAKSI DESC 
                    LIMIT 10
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gb_etalase_nilai_pu = GridOptionsBuilder.from_dataframe(tabel_etalase_nilai_pu)
                    gb_etalase_nilai_pu.configure_default_column(autoSizeColumns=True)
                    gb_etalase_nilai_pu.configure_column("NILAI_TRANSAKSI", 
                                    type=["numericColumn", "numberColumnFilter", "customNumericFormat"], 
                                    valueGetter="data.NILAI_TRANSAKSI.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', maximumFractionDigits:2})")
                    
                    AgGrid(tabel_etalase_nilai_pu, 
                        gridOptions=gb_etalase_nilai_pu.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_etalase_nilai_pu) + 1)))
                
                with col2:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=tabel_etalase_nilai_pu['NAMA_PENYEDIA'],
                        y=tabel_etalase_nilai_pu['NILAI_TRANSAKSI'],
                        text=[f'{x:,.0f}' for x in tabel_etalase_nilai_pu['NILAI_TRANSAKSI']],
                        textposition='outside',
                        marker=dict(
                            color=custom_colors[:len(tabel_etalase_nilai_pu)],
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
                        title='Grafik Nilai Transaksi Katalog per Pelaku Usaha',
                        xaxis_title='Pelaku Usaha',
                        yaxis_title='Nilai Transaksi',
                        xaxis={'categoryorder':'total descending'},
                        margin=dict(t=50, b=100, l=10, r=10)
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    with menu_purchasing_1_3:
        # Ambil dan olah data etalase
        df_etalase = con.execute("""
            SELECT 
                nama_komoditas AS NAMA_KOMODITAS,
                SUM(CASE WHEN jenis_katalog = 'Lokal' THEN total_harga ELSE 0 END) AS LOKAL,
                SUM(CASE WHEN jenis_katalog = 'Nasional' THEN total_harga ELSE 0 END) AS NASIONAL,
                SUM(CASE WHEN jenis_katalog = 'Sektoral' THEN total_harga ELSE 0 END) AS SEKTORAL
            FROM dfECAT_OK
            GROUP BY nama_komoditas
        """).df()

        # Siapkan unduhan dan tampilkan header
        col1, col2 = st.columns((8,2))
        with col1:
            st.subheader("TABEL NILAI ETALASE")
        with col2:
            st.download_button(
                label = "📥 Tabel Nilai Etalase",
                data = download_excel(df_etalase),
                file_name = f"TabelNilaiEtalase-{kodeFolder}-{tahun}.xlsx",
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        st.divider()

        # Tampilkan data dengan AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_etalase)
        gb.configure_column("NAMA_KOMODITAS", header_name="NAMA KOMODITAS", width=300)
        
        # Konfigurasi kolom nilai dengan format mata uang Indonesia
        for kolom in ["LOKAL", "NASIONAL", "SEKTORAL"]:
            gb.configure_column(
                kolom, 
                header_name=f"{kolom} (Rp.)", 
                type=["numericColumn", "numberColumnFilter"],
                valueGetter=f"data.{kolom}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})",
                width=200
            )
        
        # Konfigurasi pagination dan layout
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)
        gb.configure_grid_options(domLayout='normal')
        
        # Tampilkan tabel dengan tinggi yang menyesuaikan secara otomatis
        AgGrid(
            df_etalase,
            gridOptions=gb.build(),
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            theme='streamlit',
            height=900
        )
            
except Exception as e:
    st.error(f"Error: {e}")
