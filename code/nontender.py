# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
import openpyxl
from datetime import datetime
# Library Aggrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
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

# URL Dataset NonTender
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'NonTenderPengumuman': f"{base_url}/SPSE-NonTenderPengumuman{tahun}.parquet",
    'NonTenderSelesai': f"{base_url}/SPSE-NonTenderSelesai{tahun}.parquet",
    'NonTenderSPPBJ': f"{base_url}/SPSE-NonTenderEkontrak-SPPBJ{tahun}.parquet",
    'NonTenderKontrak': f"{base_url}/SPSE-NonTenderEkontrak-Kontrak{tahun}.parquet",
    'NonTenderSPMK': f"{base_url}/SPSE-NonTenderEkontrak-SPMKSPP{tahun}.parquet",
    'NonTenderBAST': f"{base_url}/SPSE-NonTenderEkontrak-BAPBAST{tahun}.parquet",
}

st.title(f"TRANSAKSI NON TENDER")
st.header(f"{pilih} - TAHUN {tahun}")

menu_nontender_1, menu_nontender_2, menu_nontender_3, menu_nontender_4, menu_nontender_5 = st.tabs(["| PENGUMUMAN |", "| SPPBJ |", "| KONTRAK |", "| SPMK |", "| BAPBAST |"])

with menu_nontender_1:
    try:
        # Baca dataset pengumuman non tender
        dfNonTenderPengumuman = read_df_duckdb(datasets['NonTenderPengumuman'])

        # Tampilkan header dan tombol unduh
        col1, col2 = st.columns([7,3])
        col1.header("PENGUMUMAN NON TENDER")
        col2.download_button(
            label="📥 Unduh Data Pengumuman Non Tender",
            data=download_excel(dfNonTenderPengumuman),
            file_name=f"NonTender-Pengumuman-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.divider()

        # Filter options
        SPSE_NT_radio_1, SPSE_NT_radio_2, SPSE_NT_radio_3 = st.columns((1,1,8))
        with SPSE_NT_radio_1:
            sumber_dana_array = np.insert(dfNonTenderPengumuman['sumber_dana'].unique(), 0, "Gabungan")
            sumber_dana_nt = st.radio("**Sumber Dana**", sumber_dana_array, key="Sumber_Dana_NT_Pengumuman")
        with SPSE_NT_radio_2:
            status_array = np.insert(dfNonTenderPengumuman['status_nontender'].unique(), 0, "Gabungan")
            status_nontender = st.radio("**Status Non Tender**", status_array, key="Status_NT_Pengumuman")
        st.write(f"Anda memilih : **{sumber_dana_nt}** dan **{status_nontender}**")

        # Build filter query
        filter_query = "SELECT * FROM dfNonTenderPengumuman WHERE 1=1"
        if sumber_dana_nt != "Gabungan":
            filter_query += f" AND sumber_dana = '{sumber_dana_nt}'"
        if status_nontender != "Gabungan":
            filter_query += f" AND status_nontender = '{status_nontender}'"
        
        df_filter = con.execute(filter_query).df()
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Jumlah Paket Non Tender", value="{:,}".format(df_filter['kd_nontender'].nunique()))
        col2.metric(label="Nilai Pagu", value="{:,.2f}".format(df_filter['pagu'].sum()))
        col3.metric(label="Nilai HPS", value="{:,.2f}".format(df_filter['hps'].sum()))

        st.divider()

        # Warna untuk grafik - warna yang lebih menarik
        color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F9C74F', '#90BE6D', '#577590', '#F94144', '#F3722C', '#7209B7', '#3A86FF', '#FB8500', '#8338EC', '#06D6A0']

        # Visualisasi berdasarkan kualifikasi paket
        with st.container(border=True):
            tab1, tab2 = st.tabs(["| Jumlah Kualifikasi Paket |", "| Nilai Kualifikasi Paket |"])
            
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
            tab1, tab2 = st.tabs(["| Jumlah Jenis Pengadaan |", "| Nilai Jenis Pengadaan |"])
            
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
            tab1, tab2 = st.tabs(["| Jumlah Metode Pemilihan |", "| Nilai Metode Pemilihan |"])
            
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
            tab1, tab2 = st.tabs(["| Jumlah Kontrak Pembayaran |", "| Nilai Kontrak Pembayaran |"])
            
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

        # Header dan tombol unduh
        col1, col2 = st.columns((7,3))
        col1.header("SPPBJ NON TENDER")
        col2.download_button(
            label="📥 Unduh Data SPPBJ Non Tender",
            data=download_excel(dfNonTenderSPPBJ),
            file_name=f"NonTender-SPPBJ-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Metrik total
        jumlah_total = dfNonTenderSPPBJ['kd_nontender'].nunique()
        nilai_total = dfNonTenderSPPBJ['harga_final'].sum()
        
        st.divider()
        col_metrik1, col_metrik2 = st.columns(2)
        col_metrik1.metric("Jumlah Total Non Tender SPPBJ", f"{jumlah_total:,}")
        col_metrik2.metric("Nilai Total Non Tender SPPBJ", f"{nilai_total:,.2f}")

        # Filter data
        st.divider()
        col_filter1, col_filter2 = st.columns((2,8))
        with col_filter1:
            status_kontrak_options = np.append(["Semua"], dfNonTenderSPPBJ['status_kontrak'].unique())
            status_kontrak_nt = st.radio("**Status Kontrak**", status_kontrak_options)
        with col_filter2:
            # Tambahkan opsi "Semua" untuk perangkat daerah
            opd_options = np.append(["Semua"], dfNonTenderSPPBJ['nama_satker'].unique())
            opd_nt = st.selectbox("Pilih Perangkat Daerah:", opd_options)
        
        st.write(f"Anda memilih: **{status_kontrak_nt}** dari **{opd_nt}**")

        # Data terfilter dan metrik
        filter_query = "SELECT * FROM dfNonTenderSPPBJ WHERE 1=1"
        if status_kontrak_nt != "Semua":
            filter_query += f" AND status_kontrak = '{status_kontrak_nt}'"
        if opd_nt != "Semua":
            filter_query += f" AND nama_satker = '{opd_nt}'"
            
        dfNonTenderSPPBJ_filter = con.execute(filter_query).df()
        
        jumlah_filter = dfNonTenderSPPBJ_filter['kd_nontender'].nunique()
        nilai_filter = dfNonTenderSPPBJ_filter['harga_final'].sum()
        
        col_metrik1, col_metrik2 = st.columns(2)
        col_metrik1.metric("Jumlah Non Tender SPPBJ", f"{jumlah_filter:,}")
        col_metrik2.metric("Nilai Non Tender SPPBJ", f"{nilai_filter:,.2f}")

        # Tabel data
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
               height=400, 
               width='100%',
               fit_columns_on_grid_load=False,
               allow_unsafe_jscode=True)

    except Exception as e:
        st.error(f"Error: {e}")

with menu_nontender_3:
    st.header("KONTRAK NON TENDER")

with menu_nontender_4:
    st.header("SPMK NON TENDER")
    
with menu_nontender_5:
    try:
        # Baca dataset BAPBAST Non Tender
        dfSPSENonTenderBAST = read_df_duckdb(datasets["NonTenderBAST"])
        
        # Header dan tombol unduh
        col1, col2 = st.columns((7,3))
        col1.subheader("SPSE - NON TENDER - BAPBAST")
        col2.download_button(
            label = "📥 Download Data BAPBAST",
            data = download_excel(dfSPSENonTenderBAST),
            file_name = f"SPSENonTenderBAPBAST-{kodeFolder}-{tahun}.xlsx",
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Metrik total
        st.divider()
        jumlah_total = dfSPSENonTenderBAST['kd_nontender'].nunique()
        nilai_total = dfSPSENonTenderBAST['nilai_kontrak'].sum()
        
        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah Total BAPBAST", value="{:,}".format(jumlah_total))
        col2.metric(label="Nilai Total BAPBAST", value="{:,.2f}".format(nilai_total))

        # Filter data
        st.divider()
        col1, col2 = st.columns((2,8))
        with col1:
            status_kontrak = st.radio("**Status Kontrak**", dfSPSENonTenderBAST['status_kontrak'].unique(), key='NonTender_Status_BAST')
        with col2:
            opd = st.selectbox("Pilih Perangkat Daerah:", dfSPSENonTenderBAST['nama_satker'].unique(), key='NonTender_OPD_BAST')
        st.write(f"Anda memilih: **{status_kontrak}** dari **{opd}**")

        # Data terfilter
        df_filter = con.execute(f"SELECT * FROM dfSPSENonTenderBAST WHERE nama_satker = '{opd}' AND status_kontrak = '{status_kontrak}'").df()
        jumlah_filter = df_filter['kd_nontender'].nunique()
        nilai_filter = df_filter['nilai_kontrak'].sum()
        
        col1, col2 = st.columns(2)
        col1.metric(label="Jumlah BAPBAST Terfilter", value="{:,}".format(jumlah_filter))
        col2.metric(label="Nilai BAPBAST Terfilter", value="{:,.2f}".format(nilai_filter))

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

        st.dataframe(
            tabel_tampil,
            column_config={
                "NAMA_PAKET": "NAMA PAKET",
                "NO_BAP": "NO BAP",
                "TGL_BAP": "TGL BAP",
                "NO_BAST": "NO BAST",
                "TGL_BAST": "TGL BAST",
                "NAMA_PPK": "NAMA PPK",
                "NAMA_PENYEDIA": "NAMA PENYEDIA",
                "NPWP_PENYEDIA": "NPWP PENYEDIA",
                "WAKIL_SAH": "WAKIL SAH",
                "NILAI_KONTRAK": st.column_config.NumberColumn("NILAI KONTRAK", format="Rp %,.2f"),
                "NILAI_PEMBAYARAN": st.column_config.NumberColumn("NILAI PEMBAYARAN", format="Rp %,.2f")
            },
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")