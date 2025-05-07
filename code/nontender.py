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

st.title(f"TRANSAKSI NON TENDER - {pilih} - {tahun}")

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
                    st.dataframe(tabel_jumlah, 
                        column_config={"KUALIFIKASI_PAKET": "KUALIFIKASI PAKET", "JUMLAH_PAKET": "JUMLAH PAKET"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_nilai,
                        column_config={"KUALIFIKASI_PAKET": "KUALIFIKASI PAKET", "NILAI_PAKET": "NILAI PAKET (Rp.)"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_jp_jumlah,
                        column_config={"JENIS_PENGADAAN": "JENIS PENGADAAN", "JUMLAH_PAKET": "JUMLAH PAKET"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_jp_nilai,
                        column_config={"JENIS_PENGADAAN": "JENIS PENGADAAN", "NILAI_PAKET": "NILAI PAKET (Rp.)"},
                        use_container_width=True, hide_index=True)
                with col2:
                    fig = px.bar(tabel_jp_nilai, x='JENIS_PENGADAAN', y='NILAI_PAKET', 
                                color='JENIS_PENGADAAN', color_discrete_sequence=color_palette,
                                text_auto='.2s')
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", 
                                     marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
                    fig.update_layout(
                        title_text='Nilai Berdasarkan Jenis Pengadaan', 
                        showlegend=False,
                        xaxis_title="Jenis Pengadaan",
                        yaxis_title="Nilai Paket (Rp)"
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
                    st.dataframe(tabel_mp_jumlah,
                        column_config={"METODE_PEMILIHAN": "METODE PEMILIHAN", "JUMLAH_PAKET": "JUMLAH PAKET"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_mp_nilai,
                        column_config={"METODE_PEMILIHAN": "METODE PEMILIHAN", "NILAI_PAKET": "NILAI PAKET (Rp.)"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_kontrak_jumlah,
                        column_config={"KONTRAK_PEMBAYARAN": "KONTRAK PEMBAYARAN", "JUMLAH_PAKET": "JUMLAH PAKET"},
                        use_container_width=True, hide_index=True)
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
                    st.dataframe(tabel_kontrak_nilai,
                        column_config={"KONTRAK_PEMBAYARAN": "KONTRAK PEMBAYARAN", "NILAI_PAKET": "NILAI PAKET (Rp.)"},
                        use_container_width=True, hide_index=True)
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
    st.header("SPPBJ NON TENDER")

with menu_nontender_3:
    st.header("KONTRAK NON TENDER")

with menu_nontender_4:
    st.header("SPMK NON TENDER")
    
with menu_nontender_5:
    st.header("BAPBAST NON TENDER")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")