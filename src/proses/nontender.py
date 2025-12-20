# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
from datetime import datetime
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards
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

# URL Dataset NonTender
base_url = f"https://s3-sip.pbj.my.id/spse/{kodeLPSE}"
datasets = {
    'NonTenderPengumuman': f"{base_url}/SPSE-NonTenderPengumuman/{tahun}/data.parquet",
    'NonTenderSelesai': f"{base_url}/SPSE-NonTenderSelesai/{tahun}/data.parquet",
    'NonTenderSPPBJ': f"{base_url}/SPSE-NonTenderEkontrak-SPPBJ/{tahun}/data.parquet",
    'NonTenderKontrak': f"{base_url}/SPSE-NonTenderEkontrak-Kontrak/{tahun}/data.parquet",
    'NonTenderSPMK': f"{base_url}/SPSE-NonTenderEkontrak-SPMKSPP/{tahun}/data.parquet",
    'NonTenderBAST': f"{base_url}/SPSE-NonTenderEkontrak-BAPBAST/{tahun}/data.parquet",
}

# URL Dataset RUP
base_url_rup = f"https://s3-sip.pbj.my.id/rup/{kodeRUP}"
datasets_rup = {
    'PP': f"{base_url_rup}/RUP-PaketPenyedia-Terumumkan/{tahun}/data.parquet",
}

st.title(f"TRANSAKSI NON TENDER")
st.header(f"{pilih} - TAHUN {tahun}")

menu_nontender_1, menu_nontender_2, menu_nontender_3, menu_nontender_4, menu_nontender_5 = st.tabs(["📢 PENGUMUMAN", "📋 SPPBJ", "📄 KONTRAK", "✅ SPMK", "📝 BAPBAST"])

with menu_nontender_1:
    try:
        # Baca dataset RUP
        dfRUPPP = read_df_duckdb(datasets_rup['PP'])[['kd_rup', 'status_pdn', 'status_ukm']]
        dfRUPPP['kd_rup'] = dfRUPPP['kd_rup'].astype(str)

        # Baca dataset pengumuman non tender
        dfNonTenderPengumuman = read_df_duckdb(datasets['NonTenderPengumuman'])
        dfNonTenderPengumuman['kd_rup'] = dfNonTenderPengumuman['kd_rup'].astype(str)

        # Gabungkan dataframe berdasarkan kd_rup
        dfNonTenderPengumuman = dfNonTenderPengumuman.merge(dfRUPPP, on='kd_rup', how='left')
        dfNonTenderPengumuman['status_pdn'] = dfNonTenderPengumuman['status_pdn'].fillna('Tanpa Status')
        dfNonTenderPengumuman['status_ukm'] = dfNonTenderPengumuman['status_ukm'].fillna('Tanpa Status')

        st.subheader("PENGUMUMAN NON TENDER")

        # Filter Section dengan Container
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                sumber_dana_array = np.insert(dfNonTenderPengumuman['sumber_dana'].unique(), 0, "Gabungan")
                sumber_dana_nt = st.selectbox("💵 Sumber Dana", sumber_dana_array, key="Sumber_Dana_NT_Pengumuman")

            with col2:
                status_array = np.insert(dfNonTenderPengumuman['status_nontender'].unique(), 0, "Gabungan")
                status_nontender = st.selectbox("📊 Status Non Tender", status_array, key="Status_NT_Pengumuman")

            with col3:
                status_pdn_array = np.insert(dfNonTenderPengumuman['status_pdn'].unique(), 0, "Gabungan")
                status_pdn = st.selectbox("🏭 Status PDN", status_pdn_array, key="Status_PDN_NT_Pengumuman")

            with col4:
                status_ukm_array = np.insert(dfNonTenderPengumuman['status_ukm'].unique(), 0, "Gabungan")
                status_ukm = st.selectbox("🏪 Status UKM", status_ukm_array, key="Status_UKM_NT_Pengumuman")

            nama_satker_array = np.insert(dfNonTenderPengumuman['nama_satker'].unique(), 0, "Semua Perangkat Daerah")
            nama_satker = st.selectbox("🏛️ Perangkat Daerah", nama_satker_array, key="Nama_Satker_NT_Pengumuman")

        st.divider()
        
        # Build filter query
        filter_query = "SELECT * FROM dfNonTenderPengumuman WHERE 1=1"
        if sumber_dana_nt != "Gabungan":
            filter_query += f" AND sumber_dana = '{sumber_dana_nt}'"
        if status_nontender != "Gabungan":
            filter_query += f" AND status_nontender = '{status_nontender}'"
        if status_pdn != "Gabungan":
            filter_query += f" AND status_pdn = '{status_pdn}'"
        if status_ukm != "Gabungan":
            filter_query += f" AND status_ukm = '{status_ukm}'"
        if nama_satker != "Semua Perangkat Daerah":
            filter_query += f" AND nama_satker = '{nama_satker}'"
        
        df_filter = con.execute(filter_query).df()

        # Tombol unduh di atas kanan
        col_spacer, col_download = st.columns([8, 2])
        with col_download:
            st.download_button(
                label="📥 Excel",
                data=download_excel(df_filter),
                file_name=f"NonTender-Pengumuman-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Jumlah Paket Non Tender", value="{:,}".format(df_filter['kd_nontender'].nunique()))
        col2.metric(label="Nilai Pagu", value="{:,.0f}".format(df_filter['pagu'].sum()))
        col3.metric(label="Nilai HPS", value="{:,.0f}".format(df_filter['hps'].sum()))

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()

        # Warna untuk grafik - warna yang lebih menarik
        color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F9C74F', '#90BE6D', '#577590', '#F94144', '#F3722C', '#7209B7', '#3A86FF', '#FB8500', '#8338EC', '#06D6A0']

        # Visualisasi berdasarkan kualifikasi paket
        with st.container(border=True):
            tab1, tab2 = st.tabs(["📊 Jumlah Kualifikasi Paket", "💰 Nilai Kualifikasi Paket"])
            
            with tab1:
                st.subheader("Jumlah Kualifikasi Paket")
                tabel_jumlah = con.execute("""
                    SELECT kualifikasi_paket AS KUALIFIKASI_PAKET, 
                           COUNT(DISTINCT(kd_nontender)) AS JUMLAH_PAKET
                    FROM df_filter 
                    GROUP BY KUALIFIKASI_PAKET 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_jumlah = GridOptionsBuilder.from_dataframe(tabel_jumlah)
                    gd_jumlah.configure_default_column(autoSizeColumns=True)
                    gd_jumlah.configure_column("KUALIFIKASI_PAKET", header_name="KUALIFIKASI PAKET")
                    gd_jumlah.configure_column("JUMLAH_PAKET", header_name="JUMLAH PAKET")
                    AgGrid(tabel_jumlah, 
                        gridOptions=gd_jumlah.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jumlah) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_jumlah, x='KUALIFIKASI_PAKET', y='JUMLAH_PAKET', 
                                color='KUALIFIKASI_PAKET', color_discrete_sequence=color_palette,
                                text_auto=True)
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Distribusi Jumlah Kualifikasi Paket', 
                        showlegend=False,
                        xaxis_title="Kualifikasi Paket",
                        yaxis_title="Jumlah Paket"
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.subheader("Nilai Kualifikasi Paket")
                tabel_nilai = con.execute("""
                    SELECT kualifikasi_paket AS KUALIFIKASI_PAKET, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM df_filter 
                    GROUP BY KUALIFIKASI_PAKET 
                    ORDER BY NILAI_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_nilai = GridOptionsBuilder.from_dataframe(tabel_nilai)
                    gd_nilai.configure_default_column(autoSizeColumns=True)
                    gd_nilai.configure_column("KUALIFIKASI_PAKET", header_name="KUALIFIKASI PAKET")
                    gd_nilai.configure_column("NILAI_PAKET", header_name="NILAI PAKET (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
                    AgGrid(tabel_nilai, 
                        gridOptions=gd_nilai.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_nilai) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_nilai, x='KUALIFIKASI_PAKET', y='NILAI_PAKET', 
                                color='KUALIFIKASI_PAKET', color_discrete_sequence=color_palette,
                                text_auto='.2s')
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Nilai Paket Berdasarkan Kualifikasi', 
                        showlegend=False,
                        xaxis_title="Kualifikasi Paket",
                        yaxis_title="Nilai Paket (Rp)"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # Visualisasi berdasarkan jenis pengadaan
        with st.container(border=True):
            tab1, tab2 = st.tabs(["📊 Jumlah Jenis Pengadaan", "💰 Nilai Jenis Pengadaan"])
            
            with tab1:
                st.subheader("Jumlah Jenis Pengadaan")
                tabel_jp_jumlah = con.execute("""
                    SELECT jenis_pengadaan AS JENIS_PENGADAAN, 
                           COUNT(DISTINCT(kd_nontender)) AS JUMLAH_PAKET
                    FROM df_filter 
                    GROUP BY JENIS_PENGADAAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_jp_jumlah = GridOptionsBuilder.from_dataframe(tabel_jp_jumlah)
                    gd_jp_jumlah.configure_default_column(autoSizeColumns=True)
                    gd_jp_jumlah.configure_column("JENIS_PENGADAAN", header_name="JENIS PENGADAAN")
                    gd_jp_jumlah.configure_column("JUMLAH_PAKET", header_name="JUMLAH PAKET")
                    AgGrid(tabel_jp_jumlah, 
                        gridOptions=gd_jp_jumlah.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jp_jumlah) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_jp_jumlah, x='JENIS_PENGADAAN', y='JUMLAH_PAKET', 
                                color='JENIS_PENGADAAN', color_discrete_sequence=color_palette,
                                text_auto=True)
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Jumlah Paket Berdasarkan Jenis Pengadaan', 
                        showlegend=False,
                        xaxis_title="Jenis Pengadaan",
                        yaxis_title="Jumlah Paket"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("Nilai Jenis Pengadaan")
                tabel_jp_nilai = con.execute("""
                    SELECT jenis_pengadaan AS JENIS_PENGADAAN, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM df_filter 
                    GROUP BY JENIS_PENGADAAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_jp_nilai = GridOptionsBuilder.from_dataframe(tabel_jp_nilai)
                    gd_jp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_jp_nilai.configure_column("JENIS_PENGADAAN", header_name="JENIS PENGADAAN")
                    gd_jp_nilai.configure_column("NILAI_PAKET", header_name="NILAI PAKET (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
                    AgGrid(tabel_jp_nilai, 
                        gridOptions=gd_jp_nilai.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_jp_nilai) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_jp_nilai, x='NILAI_PAKET', y='JENIS_PENGADAAN', 
                                color='JENIS_PENGADAAN', color_discrete_sequence=color_palette,
                                text_auto='.2s', orientation='h')
                    fig.update_traces(textfont_size=12, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Nilai Paket Berdasarkan Jenis Pengadaan', 
                        showlegend=False,
                        xaxis_title="Nilai Paket (Rp)",
                        yaxis_title="Jenis Pengadaan"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # Visualisasi berdasarkan metode pemilihan
        with st.container(border=True):
            tab1, tab2 = st.tabs(["📊 Jumlah Metode Pemilihan", "💰 Nilai Metode Pemilihan"])
            
            with tab1:
                st.subheader("Jumlah Metode Pemilihan")
                tabel_mp_jumlah = con.execute("""
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, 
                           COUNT(DISTINCT(kd_nontender)) AS JUMLAH_PAKET
                    FROM df_filter 
                    GROUP BY METODE_PEMILIHAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_mp_jumlah = GridOptionsBuilder.from_dataframe(tabel_mp_jumlah)
                    gd_mp_jumlah.configure_default_column(autoSizeColumns=True)
                    gd_mp_jumlah.configure_column("METODE_PEMILIHAN", header_name="METODE PEMILIHAN")
                    gd_mp_jumlah.configure_column("JUMLAH_PAKET", header_name="JUMLAH PAKET")
                    AgGrid(tabel_mp_jumlah, 
                        gridOptions=gd_mp_jumlah.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_mp_jumlah) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_mp_jumlah, y='METODE_PEMILIHAN', x='JUMLAH_PAKET', 
                                color='METODE_PEMILIHAN', color_discrete_sequence=color_palette,
                                text_auto=True, orientation='h')
                    fig.update_traces(textfont_size=12, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Jumlah Paket Berdasarkan Metode Pemilihan', 
                        showlegend=False,
                        xaxis_title="Jumlah Paket",
                        yaxis_title="Metode Pemilihan"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("Nilai Metode Pemilihan")
                tabel_mp_nilai = con.execute("""
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM df_filter 
                    GROUP BY METODE_PEMILIHAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_mp_nilai = GridOptionsBuilder.from_dataframe(tabel_mp_nilai)
                    gd_mp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_mp_nilai.configure_column("METODE_PEMILIHAN", header_name="METODE PEMILIHAN")
                    gd_mp_nilai.configure_column("NILAI_PAKET", header_name="NILAI PAKET (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
                    AgGrid(tabel_mp_nilai, 
                        gridOptions=gd_mp_nilai.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_mp_nilai) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_mp_nilai, x='NILAI_PAKET', y='METODE_PEMILIHAN', 
                                color='METODE_PEMILIHAN', color_discrete_sequence=color_palette,
                                text_auto='.2s', orientation='h')
                    fig.update_traces(textfont_size=12, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Nilai Paket Berdasarkan Metode Pemilihan', 
                        showlegend=False,
                        xaxis_title="Nilai Paket (Rp)",
                        yaxis_title="Metode Pemilihan"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # Visualisasi berdasarkan kontrak pembayaran
        with st.container(border=True):
            tab1, tab2 = st.tabs(["📊 Jumlah Kontrak Pembayaran", "💰 Nilai Kontrak Pembayaran"])
            
            with tab1:
                st.subheader("Jumlah Kontrak Pembayaran")
                tabel_kontrak_jumlah = con.execute("""
                    SELECT kontrak_pembayaran AS KONTRAK_PEMBAYARAN, 
                           COUNT(DISTINCT(kd_nontender)) AS JUMLAH_PAKET
                    FROM df_filter 
                    GROUP BY KONTRAK_PEMBAYARAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_kontrak_jumlah = GridOptionsBuilder.from_dataframe(tabel_kontrak_jumlah)
                    gd_kontrak_jumlah.configure_default_column(autoSizeColumns=True)
                    gd_kontrak_jumlah.configure_column("KONTRAK_PEMBAYARAN", header_name="KONTRAK PEMBAYARAN")
                    gd_kontrak_jumlah.configure_column("JUMLAH_PAKET", header_name="JUMLAH PAKET")
                    AgGrid(tabel_kontrak_jumlah, 
                        gridOptions=gd_kontrak_jumlah.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_kontrak_jumlah) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_kontrak_jumlah, x='KONTRAK_PEMBAYARAN', y='JUMLAH_PAKET', 
                                color='KONTRAK_PEMBAYARAN', color_discrete_sequence=color_palette,
                                text_auto=True)
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Jumlah Berdasarkan Kontrak Pembayaran', 
                        showlegend=False,
                        xaxis_title="Kontrak Pembayaran",
                        yaxis_title="Jumlah Paket"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.subheader("Nilai Kontrak Pembayaran")
                tabel_kontrak_nilai = con.execute("""
                    SELECT kontrak_pembayaran AS KONTRAK_PEMBAYARAN, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM df_filter 
                    GROUP BY KONTRAK_PEMBAYARAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()
                
                col1, col2 = st.columns((3,7))
                with col1:
                    gd_kontrak_nilai = GridOptionsBuilder.from_dataframe(tabel_kontrak_nilai)
                    gd_kontrak_nilai.configure_default_column(autoSizeColumns=True)
                    gd_kontrak_nilai.configure_column("KONTRAK_PEMBAYARAN", header_name="KONTRAK PEMBAYARAN")
                    gd_kontrak_nilai.configure_column("NILAI_PAKET", header_name="NILAI PAKET (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
                    AgGrid(tabel_kontrak_nilai, 
                        gridOptions=gd_kontrak_nilai.build(),
                        enable_enterprise_modules=True,
                        fit_columns_on_grid_load=True,
                        autoSizeColumns=True,
                        width='100%',
                        height=min(350, 35 * (len(tabel_kontrak_nilai) + 1)))
                    
                with col2:
                    fig = px.bar(tabel_kontrak_nilai, x='KONTRAK_PEMBAYARAN', y='NILAI_PAKET', 
                                color='KONTRAK_PEMBAYARAN', color_discrete_sequence=color_palette,
                                text_auto='.2s')
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5,
                                     marker=dict(line=dict(width=1.5, color='black')))
                    fig.update_layout(
                        title_text='Nilai Paket Berdasarkan Kontrak Pembayaran', 
                        showlegend=False,
                        xaxis_title="Kontrak Pembayaran",
                        yaxis_title="Nilai Paket (Rp)"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
    except Exception as e:
        st.error(f"Error: {e}")

with menu_nontender_2:
    try:
        # Baca dataset SPPBJ non tender
        dfNonTenderSPPBJ = read_df_duckdb(datasets["NonTenderSPPBJ"])

        st.subheader("SPPBJ NON TENDER")

        # Filter Section dengan Container
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")

            col1, col2 = st.columns([3, 7])
            with col1:
                status_kontrak_options = ['Semua'] + list(dfNonTenderSPPBJ['status_kontrak'].unique())
                status_kontrak_nt = st.selectbox("📊 Status Kontrak", status_kontrak_options, key="NonTender_Status_SPPBJ")
            with col2:
                opd_options = ['SEMUA PERANGKAT DAERAH'] + list(dfNonTenderSPPBJ['nama_satker'].unique())
                opd_nt = st.selectbox("🏛️ Perangkat Daerah", opd_options, key="NonTender_OPD_SPPBJ")

        st.divider()

        if status_kontrak_nt == 'Semua' and opd_nt == 'SEMUA PERANGKAT DAERAH':
            dfNonTenderSPPBJ_filter = dfNonTenderSPPBJ
        elif status_kontrak_nt == 'Semua':
            dfNonTenderSPPBJ_filter = con.execute(f"""
                SELECT * FROM dfNonTenderSPPBJ
                WHERE nama_satker = '{opd_nt}'
            """).df()
        elif opd_nt == 'SEMUA PERANGKAT DAERAH':
            dfNonTenderSPPBJ_filter = con.execute(f"""
                SELECT * FROM dfNonTenderSPPBJ
                WHERE status_kontrak = '{status_kontrak_nt}'
            """).df()
        else:
            dfNonTenderSPPBJ_filter = con.execute(f"""
                SELECT * FROM dfNonTenderSPPBJ
                WHERE status_kontrak = '{status_kontrak_nt}'
                AND nama_satker = '{opd_nt}'
            """).df()

        # Tombol unduh di atas kanan
        col_spacer, col_download = st.columns([8, 2])
        with col_download:
            st.download_button(
                label="📥 Excel",
                data=download_excel(dfNonTenderSPPBJ_filter),
                file_name=f"NonTender-SPPBJ-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        jumlah_filter = dfNonTenderSPPBJ_filter['kd_nontender'].nunique()
        nilai_filter = dfNonTenderSPPBJ_filter['harga_final'].sum()

        col_metrik1, col_metrik2 = st.columns(2)
        col_metrik1.metric("Jumlah Non Tender SPPBJ", f"{jumlah_filter:,}")
        col_metrik2.metric("Nilai Non Tender SPPBJ", f"{nilai_filter:,.0f}")

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()
        tabel_sppbj_nt_tampil = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, no_sppbj AS NO_SPPBJ, tgl_sppbj AS TGL_SPPBJ, 
                   nama_ppk AS NAMA_PPK, nama_penyedia AS NAMA_PENYEDIA, 
                   npwp_penyedia AS NPWP_PENYEDIA, harga_final AS HARGA_FINAL 
            FROM dfNonTenderSPPBJ_filter
        """).df()

        # Konfigurasi AgGrid
        gb = GridOptionsBuilder.from_dataframe(tabel_sppbj_nt_tampil)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("NAMA_PAKET", header_name="NAMA PAKET", width=300)
        gb.configure_column("NO_SPPBJ", header_name="NO SPPBJ", width=150)
        gb.configure_column("TGL_SPPBJ", header_name="TGL SPPBJ", width=120)
        gb.configure_column("NAMA_PPK", header_name="NAMA PPK", width=200)
        gb.configure_column("NAMA_PENYEDIA", header_name="NAMA PENYEDIA", width=250)
        gb.configure_column("NPWP_PENYEDIA", header_name="NPWP PENYEDIA", width=150)
        gb.configure_column("HARGA_FINAL", 
                           header_name="HARGA FINAL", 
                           width=180, 
                           type=["numericColumn", "numberColumnFilter"],
                           valueFormatter="data.HARGA_FINAL.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
        
        grid_options = gb.build()
        AgGrid(tabel_sppbj_nt_tampil, 
               gridOptions=grid_options, 
               enable_enterprise_modules=True,
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               height=800, 
               width='100%',
               allow_unsafe_jscode=True)

    except Exception as e:
        st.error(f"Error: {e}")

with menu_nontender_3:
    try:
        # Baca data dan siapkan unduhan
        dfSPSENonTenderKontrak = read_df_duckdb(datasets["NonTenderKontrak"])

        st.subheader("KONTRAK NON TENDER")

        # Filter Section dengan Container
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")

            col1, col2 = st.columns([3, 7])
            with col1:
                status_options = ["Semua"] + list(dfSPSENonTenderKontrak['status_kontrak'].unique())
                status_kontrak = st.selectbox("📊 Status Kontrak", status_options, key='NonTender_Kontrak')
            with col2:
                opd_options = ["SEMUA PERANGKAT DAERAH"] + list(dfSPSENonTenderKontrak['nama_satker'].unique())
                opd = st.selectbox("🏛️ Perangkat Daerah", opd_options, key='NonTender_Kontrak_OPD')

        st.divider()

        if status_kontrak == "Semua" and opd == "SEMUA PERANGKAT DAERAH":
            df_filter = dfSPSENonTenderKontrak
        elif status_kontrak == "Semua":
            df_filter = con.execute(f"""
                SELECT * FROM dfSPSENonTenderKontrak
                WHERE nama_satker = '{opd}'
            """).df()
        elif opd == "SEMUA PERANGKAT DAERAH":
            df_filter = con.execute(f"""
                SELECT * FROM dfSPSENonTenderKontrak
                WHERE status_kontrak = '{status_kontrak}'
            """).df()
        else:
            df_filter = con.execute(f"""
                SELECT * FROM dfSPSENonTenderKontrak
                WHERE status_kontrak = '{status_kontrak}'
                AND nama_satker = '{opd}'
            """).df()

        # Tombol unduh di atas kanan
        col_spacer, col_download = st.columns([8, 2])
        with col_download:
            st.download_button(
                label="📥 Excel",
                data=download_excel(df_filter),
                file_name=f"SPSENonTenderKONTRAK-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        jumlah_filter = df_filter['kd_nontender'].nunique()
        nilai_filter = df_filter['nilai_kontrak'].sum()

        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah Non Tender KONTRAK", value="{:,}".format(jumlah_filter))
        col2.metric(label="Nilai Non Tender KONTRAK", value="{:,.0f}".format(nilai_filter))

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()
        tabel_kontrak = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, no_kontrak AS NO_KONTRAK, tgl_kontrak AS TGL_KONTRAK, 
                   nama_ppk AS NAMA_PPK, nama_penyedia AS NAMA_PENYEDIA, npwp_penyedia AS NPWP_PENYEDIA, 
                   wakil_sah_penyedia AS WAKIL_SAH, nilai_kontrak AS NILAI_KONTRAK, 
                   nilai_pdn_kontrak AS NILAI_PDN, nilai_umk_kontrak AS NILAI_UMK 
            FROM df_filter
        """).df()

        # Tampilkan tabel
        gd_kontrak = GridOptionsBuilder.from_dataframe(tabel_kontrak)
        gd_kontrak.configure_default_column(autoSizeColumns=True)
        gd_kontrak.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gd_kontrak.configure_column("NO_KONTRAK", header_name="NO KONTRAK")
        gd_kontrak.configure_column("TGL_KONTRAK", header_name="TGL KONTRAK")
        gd_kontrak.configure_column("NAMA_PPK", header_name="NAMA PPK")
        gd_kontrak.configure_column("NAMA_PENYEDIA", header_name="NAMA PENYEDIA")
        gd_kontrak.configure_column("NPWP_PENYEDIA", header_name="NPWP PENYEDIA")
        gd_kontrak.configure_column("WAKIL_SAH", header_name="WAKIL SAH")
        gd_kontrak.configure_column("NILAI_KONTRAK", header_name="NILAI KONTRAK (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
        gd_kontrak.configure_column("NILAI_PDN", header_name="NILAI PDN (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
        gd_kontrak.configure_column("NILAI_UMK", header_name="NILAI UMK (Rp.)", valueFormatter="'Rp. ' + x.toLocaleString()")
        
        AgGrid(tabel_kontrak, 
               gridOptions=gd_kontrak.build(),
               enable_enterprise_modules=True,
               fit_columns_on_grid_load=True,
               autoSizeColumns=True,
               width='100%',
               height=min(800, 35 * (len(tabel_kontrak) + 1)))

    except Exception as e:
        st.error(f"Error: {e}")

with menu_nontender_4:
    try:
        # Baca dan gabungkan data SPMK dan Kontrak
        dfSPSENonTenderKontrak = read_df_duckdb(datasets["NonTenderKontrak"])
        dfSPSENonTenderSPMK = read_df_duckdb(datasets["NonTenderSPMK"])

        # Gabungkan data kontrak (kolom nilai) dengan SPMK
        df_SPSENonTenderSPMK_OK = dfSPSENonTenderSPMK.merge(
            dfSPSENonTenderKontrak[["kd_nontender", "nilai_kontrak", "nilai_pdn_kontrak", "nilai_umk_kontrak"]],
            how='left',
            on='kd_nontender'
        )

        st.subheader("SPMK NON TENDER")

        # Filter Section dengan Container
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")

            opd_options = ["SEMUA PERANGKAT DAERAH"] + list(df_SPSENonTenderSPMK_OK['nama_satker'].unique())
            opd_SPMK = st.selectbox("🏛️ Perangkat Daerah", opd_options, key='NonTender_OPD_SPMK')

        st.divider()

        # Ambil data terfilter dan metrik
        if opd_SPMK == "SEMUA PERANGKAT DAERAH":
            filtered_spmk = df_SPSENonTenderSPMK_OK
        else:
            filtered_spmk = df_SPSENonTenderSPMK_OK[df_SPSENonTenderSPMK_OK['nama_satker'] == opd_SPMK]

        jumlah_spmk = filtered_spmk['kd_nontender'].nunique()
        nilai_spmk = filtered_spmk['nilai_kontrak'].sum()

        # Tombol unduh di atas kanan
        col_spacer, col_download = st.columns([8, 2])
        with col_download:
            st.download_button(
                label="📥 Excel",
                data=download_excel(filtered_spmk),
                file_name=f"NonTender-SPMK-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        # Metric cards
        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah Non Tender SPMK", value=f"{jumlah_spmk:,}")
        col2.metric(label="Nilai Non Tender SPMK", value=f"{nilai_spmk:,.0f}")

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()

        # Persiapkan data untuk tabel SPMK
        df_filter = filtered_spmk
        jumlah_filter = jumlah_spmk
        nilai_filter = nilai_spmk
        
        # Tabel data
        st.divider()
        tabel_tampil = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, no_spmk_spp AS NO_SPMK, tgl_spmk_spp AS TGL_SPMK, 
                   nama_ppk AS NAMA_PPK, nama_penyedia AS NAMA_PENYEDIA, npwp_penyedia AS NPWP_PENYEDIA, 
                   wakil_sah_penyedia AS WAKIL_SAH, nilai_kontrak AS NILAI_KONTRAK, 
                   nilai_pdn_kontrak AS NILAI_PDN, nilai_umk_kontrak AS NILAI_UMK 
            FROM df_filter
        """).df()
        
        gd = GridOptionsBuilder.from_dataframe(tabel_tampil)
        gd.configure_default_column(autoSizeColumns=True)
        gd.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gd.configure_column("NO_SPMK", header_name="NO SPMK")
        gd.configure_column("TGL_SPMK", header_name="TGL SPMK")
        gd.configure_column("NAMA_PPK", header_name="NAMA PPK")
        gd.configure_column("NAMA_PENYEDIA", header_name="NAMA PENYEDIA")
        gd.configure_column("NPWP_PENYEDIA", header_name="NPWP PENYEDIA")
        gd.configure_column("WAKIL_SAH", header_name="WAKIL SAH")
        gd.configure_column("NILAI_KONTRAK", header_name="NILAI KONTRAK", valueFormatter="'Rp. ' + x.toLocaleString()")
        gd.configure_column("NILAI_PDN", header_name="NILAI PDN", valueFormatter="'Rp. ' + x.toLocaleString()")
        gd.configure_column("NILAI_UMK", header_name="NILAI UMK", valueFormatter="'Rp. ' + x.toLocaleString()")
        
        AgGrid(tabel_tampil, 
            gridOptions=gd.build(),
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            autoSizeColumns=True,
            width='100%',
            height=min(800, 35 * (len(tabel_tampil) + 1)))
        
    except Exception as e:
        st.error(f"Error: {e}")

with menu_nontender_5:
    try:
        # Baca dataset BAPBAST Non Tender
        dfSPSENonTenderBAST = read_df_duckdb(datasets["NonTenderBAST"]).drop_duplicates(subset=['kd_nontender'])

        st.subheader("BAPBAST NON TENDER")

        # Filter Section dengan Container
        with st.container(border=True):
            st.markdown("#### 🔍 Filter Data")

            col1, col2 = st.columns([3, 7])
            with col1:
                status_options = ["Semua"] + list(dfSPSENonTenderBAST['status_kontrak'].unique())
                status = st.selectbox("📊 Status Kontrak", status_options, key='NonTender_Status_BAST')
            with col2:
                opd_options = ["SEMUA PERANGKAT DAERAH"] + list(dfSPSENonTenderBAST['nama_satker'].unique())
                opd = st.selectbox("🏛️ Perangkat Daerah", opd_options, key='NonTender_OPD_BAST')

        st.divider()

        # Data yang sudah difilter
        if status == "Semua" and opd == "SEMUA PERANGKAT DAERAH":
            filtered_df = dfSPSENonTenderBAST
        elif status == "Semua":
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSENonTenderBAST
                WHERE nama_satker = '{opd}'
            """).df()
        elif opd == "SEMUA PERANGKAT DAERAH":
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSENonTenderBAST
                WHERE status_kontrak = '{status}'
            """).df()
        else:
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSENonTenderBAST
                WHERE status_kontrak = '{status}'
                AND nama_satker = '{opd}'
            """).df()

        # Metrik hasil filter
        jumlah_filter = filtered_df['kd_nontender'].nunique()
        nilai_filter = filtered_df['nilai_kontrak'].sum()

        # Tombol unduh di atas kanan
        col_spacer, col_download = st.columns([8, 2])
        with col_download:
            st.download_button(
                label="📥 Excel",
                data=download_excel(filtered_df),
                file_name=f"NonTender-BAPBAST-{kodeFolder}-{tahun}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        # Metric cards
        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah BAPBAST", value=f"{jumlah_filter:,}")
        col2.metric(label="Nilai BAPBAST", value=f"{nilai_filter:,.0f}")

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

        st.divider()

        # Persiapkan data untuk tabel
        df_filter = filtered_df

        # Tabel data
        st.divider()
        tabel_tampil = con.execute("""
            SELECT nama_paket AS NAMA_PAKET, no_bap AS NO_BAP, tgl_bap AS TGL_BAP, 
                   no_bast AS NO_BAST, tgl_bast AS TGL_BAST, nama_ppk AS NAMA_PPK, 
                   nama_penyedia AS NAMA_PENYEDIA, npwp_penyedia AS NPWP_PENYEDIA, 
                   wakil_sah_penyedia AS WAKIL_SAH, nilai_kontrak AS NILAI_KONTRAK, 
                   besar_pembayaran AS NILAI_PEMBAYARAN 
            FROM df_filter
        """).df()

        # Konfigurasi AgGrid
        gb = GridOptionsBuilder.from_dataframe(tabel_tampil)
        gb.configure_default_column(resizable=True, filterable=True, sortable=True)
        gb.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gb.configure_column("NO_BAP", header_name="NO BAP")
        gb.configure_column("TGL_BAP", header_name="TGL BAP")
        gb.configure_column("NO_BAST", header_name="NO BAST")
        gb.configure_column("TGL_BAST", header_name="TGL BAST")
        gb.configure_column("NAMA_PPK", header_name="NAMA PPK")
        gb.configure_column("NAMA_PENYEDIA", header_name="NAMA PENYEDIA")
        gb.configure_column("NPWP_PENYEDIA", header_name="NPWP PENYEDIA")
        gb.configure_column("WAKIL_SAH", header_name="WAKIL SAH")
        gb.configure_column("NILAI_KONTRAK", 
                           header_name="NILAI KONTRAK", 
                           type=["numericColumn", "numberColumnFilter"],
                           valueFormatter="data.NILAI_KONTRAK.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
        gb.configure_column("NILAI_PEMBAYARAN", 
                           header_name="NILAI PEMBAYARAN", 
                           type=["numericColumn", "numberColumnFilter"],
                           valueFormatter="data.NILAI_PEMBAYARAN.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 2})")
        
        grid_options = gb.build()
        
        # Menampilkan tabel dengan AgGrid
        AgGrid(
            tabel_tampil,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            autoSizeColumns=True,
            height=800,
            width='100%',
            allow_unsafe_jscode=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
