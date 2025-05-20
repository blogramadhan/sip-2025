# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import duckdb
from datetime import datetime
# Library Currency
from babel.numbers import format_currency
# Library Aggrid
from st_aggrid import AgGrid, GridUpdateMode
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

# URL Dataset Tender
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'TenderPengumuman': f"{base_url}/SPSE-TenderPengumuman{tahun}.parquet",
    'TenderSelesai': f"{base_url}/SPSE-TenderSelesai{tahun}.parquet",
    'TenderSelesaiNilai': f"{base_url}/SPSE-TenderSelesaiNilai{tahun}.parquet",
    'TenderSPPBJ': f"{base_url}/SPSE-TenderEkontrak-SPPBJ{tahun}.parquet",
    'TenderKontrak': f"{base_url}/SPSE-TenderEkontrak-Kontrak{tahun}.parquet",
    'TenderSPMK': f"{base_url}/SPSE-TenderEkontrak-SPMKSPP{tahun}.parquet",
    'TenderBAST': f"{base_url}/SPSE-TenderEkontrak-BAPBAST{tahun}.parquet",
}

st.title("TRANSAKSI TENDER")
st.header(f"{pilih} - TAHUN {tahun}")

menu_tender_1, menu_tender_2, menu_tender_3, menu_tender_4, menu_tender_5 = st.tabs(["| PENGUMUMAN |", "| SPPBJ |", "| KONTRAK |", "| SPMK |", "| BAPBAST |"])

with menu_tender_1:
    try:
        # Baca dataset pengumuman Tender Selesai
        dfSPSETenderPengumuman = read_df_duckdb(datasets['TenderPengumuman']).drop(columns=['nama_pokja'])

        # Tampilkan header dan tombol unduh
        col1, col2 = st.columns([7,3])
        col1.subheader("PENGUMUMAN TENDER")
        col2.download_button(
            label="📥 Unduh Data Pengumuman Tender",
            data=download_excel(dfSPSETenderPengumuman),
            file_name=f"Tender-Pengumuman-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.divider()

        SPSE_radio_1, SPSE_radio_2, SPSE_radio_3 = st.columns((1,1,8))
        with SPSE_radio_1:
            sumber_dana_unik_array = dfSPSETenderPengumuman['sumber_dana'].unique()
            sumber_dana_unik_array_ok = np.insert(sumber_dana_unik_array, 0, "Gabungan")
            sumber_dana = st.radio("**Sumber Dana**", sumber_dana_unik_array_ok, key="Sumber_Dana_Tender_pengumuman")
        with SPSE_radio_2:
            status_tender_unik_array = dfSPSETenderPengumuman['status_tender'].unique()
            status_tender_unik_array_ok = np.insert(status_tender_unik_array, 0, "Gabungan")
            status_tender = st.radio("**Status Tender**", status_tender_unik_array_ok, key="Status_Tender_Pengumuman")
        with SPSE_radio_3:
            nama_satker_unik_array = dfSPSETenderPengumuman['nama_satker'].unique()
            nama_satker_unik_array_ok = np.insert(nama_satker_unik_array, 0, "Semua Perangkat Daerah")
            nama_satker = st.selectbox("Pilih Perangkat Daerah :", nama_satker_unik_array_ok, key='Nama_Satker_Pengumuman')
        st.write(f"Anda memilih : **{sumber_dana}** dan **{status_tender}**")

        SPSETenderPengumuman_filter_query = f"SELECT * FROM dfSPSETenderPengumuman WHERE 1=1"

        if sumber_dana != "Gabungan":
            SPSETenderPengumuman_filter_query += f" AND sumber_dana = '{sumber_dana}'"
        if status_tender != "Gabungan":
            SPSETenderPengumuman_filter_query += f" AND status_tender = '{status_tender}'"
        if nama_satker != "Semua Perangkat Daerah":
            SPSETenderPengumuman_filter_query += f" AND nama_satker = '{nama_satker}'"

        SPSETenderPengumuman_filter = con.execute(SPSETenderPengumuman_filter_query).df()
        
        jumlah_trx_spse_pengumuman = SPSETenderPengumuman_filter['kd_tender'].unique().shape[0]
        nilai_trx_spse_pengumuman_pagu = SPSETenderPengumuman_filter['pagu'].sum()
        nilai_trx_spse_pengumuman_hps = SPSETenderPengumuman_filter['hps'].sum()

        data_umum_1, data_umum_2, data_umum_3 = st.columns(3)
        data_umum_1.metric(label="Jumlah Tender Diumumkan", value="{:,}".format(jumlah_trx_spse_pengumuman))
        data_umum_2.metric(label="Nilai Pagu Tender Diumumkan", value="{:,.2f}".format(nilai_trx_spse_pengumuman_pagu))
        data_umum_3.metric(label="Nilai HPS Tender Diumumkan", value="{:,.2f}".format(nilai_trx_spse_pengumuman_hps))

        st.divider()

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Kualifikasi Paket
            grafik_kp_1, grafik_kp_2 = st.tabs(["| Berdasarkan Jumlah Kualifikasi Paket |", "| Berdasarkan Nilai Kualifikasi Paket |"])

            with grafik_kp_1:

                st.subheader("Berdasarkan Jumlah Kualifikasi Paket")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan kualifikasi paket

                tabel_kp_jumlah_trx = con.execute("""
                    SELECT kualifikasi_paket AS KUALIFIKASI_PAKET, 
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY KUALIFIKASI_PAKET 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_kp_1_1, grafik_kp_1_2 = st.columns((3,7))

                with grafik_kp_1_1:

                    gd_kp_hitung = GridOptionsBuilder.from_dataframe(tabel_kp_jumlah_trx)
                    gd_kp_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_kp_jumlah_trx, 
                           gridOptions=gd_kp_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_kp_jumlah_trx) + 1)))

                with grafik_kp_1_2:
                    fig = px.bar(tabel_kp_jumlah_trx, 
                               x="KUALIFIKASI_PAKET", 
                               y="JUMLAH_PAKET",
                               color="KUALIFIKASI_PAKET",
                               color_discrete_sequence=px.colors.qualitative.Set3,
                               title="Jumlah Paket per Kualifikasi",
                               labels={"KUALIFIKASI_PAKET": "Kualifikasi Paket",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_kp_2:

                st.subheader("Berdasarkan Nilai Kualifikasi Paket")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan kualifikasi paket

                tabel_kp_nilai_trx = con.execute("""
                    SELECT kualifikasi_paket AS KUALIFIKASI_PAKET, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY KUALIFIKASI_PAKET 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_kp_2_1, grafik_kp_2_2 = st.columns((3,7))

                with grafik_kp_2_1:

                    gd_kp_nilai = GridOptionsBuilder.from_dataframe(tabel_kp_nilai_trx)
                    gd_kp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_kp_nilai.configure_column("NILAI_PAKET", valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_kp_nilai_trx,
                          gridOptions=gd_kp_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_kp_nilai_trx) + 1)))

                with grafik_kp_2_2:
                    fig = px.bar(tabel_kp_nilai_trx,
                               x="KUALIFIKASI_PAKET",
                               y="NILAI_PAKET", 
                               color="KUALIFIKASI_PAKET",
                               color_discrete_sequence=px.colors.qualitative.Set3,
                               title="Nilai Paket per Kualifikasi",
                               labels={"KUALIFIKASI_PAKET": "Kualifikasi Paket",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Jenis Pengadaan
            grafik_jp_1, grafik_jp_2 = st.tabs(["| Berdasarkan Jumlah Jenis Pengadaan |", "| Berdasarkan Nilai Jenis Pengadaan |"])

            with grafik_jp_1:

                st.subheader("Berdasarkan Jumlah Jenis Pengadaan")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Jenis Pengadaan

                tabel_jp_jumlah_trx = con.execute("""
                    SELECT jenis_pengadaan AS JENIS_PENGADAAN, 
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY JENIS_PENGADAAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_jp_1_1, grafik_jp_1_2 = st.columns((3,7))

                with grafik_jp_1_1:

                    gd_jp_hitung = GridOptionsBuilder.from_dataframe(tabel_jp_jumlah_trx)
                    gd_jp_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_jp_jumlah_trx, 
                           gridOptions=gd_jp_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_jp_jumlah_trx) + 1)))

                with grafik_jp_1_2:
                    fig = px.bar(tabel_jp_jumlah_trx,
                               x="JENIS_PENGADAAN",
                               y="JUMLAH_PAKET",
                               color="JENIS_PENGADAAN", 
                               color_discrete_sequence=px.colors.qualitative.Pastel,
                               title="Jumlah Paket per Jenis Pengadaan",
                               labels={"JENIS_PENGADAAN": "Jenis Pengadaan",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_jp_2:

                st.subheader("Berdasarkan Nilai Jenis Pengadaan")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan Jenis Pengadaan

                tabel_jp_nilai_trx = con.execute("""
                    SELECT jenis_pengadaan AS JENIS_PENGADAAN, 
                           SUM(pagu) AS NILAI_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY JENIS_PENGADAAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_jp_2_1, grafik_jp_2_2 = st.columns((3,7))

                with grafik_jp_2_1:

                    gd_jp_nilai = GridOptionsBuilder.from_dataframe(tabel_jp_nilai_trx)
                    gd_jp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_jp_nilai.configure_column('NILAI_PAKET', valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_jp_nilai_trx,
                          gridOptions=gd_jp_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_jp_nilai_trx) + 1)))

                with grafik_jp_2_2:
                    fig = px.bar(tabel_jp_nilai_trx,
                               x="JENIS_PENGADAAN",
                               y="NILAI_PAKET",
                               color="JENIS_PENGADAAN",
                               color_discrete_sequence=px.colors.qualitative.Pastel,
                               title="Nilai Paket per Jenis Pengadaan", 
                               labels={"JENIS_PENGADAAN": "Jenis Pengadaan",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Metode Pemilihan
            grafik_mp_1, grafik_mp_2 = st.tabs(["| Berdasarkan Jumlah Metode Pemilihan |", "| Berdasarkan Nilai Metode Pemilihan |"])

            with grafik_mp_1:

                st.subheader("Berdasarkan Jumlah Metode Pemilihan")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Metode Pemilihan

                tabel_mp_jumlah_trx = con.execute("""
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, 
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_PEMILIHAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_mp_1_1, grafik_mp_1_2 = st.columns((3,7))

                with grafik_mp_1_1:

                    gd_mp_hitung = GridOptionsBuilder.from_dataframe(tabel_mp_jumlah_trx)
                    gd_mp_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_mp_jumlah_trx, 
                           gridOptions=gd_mp_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_mp_jumlah_trx) + 1)))

                with grafik_mp_1_2:
                    fig = px.bar(tabel_mp_jumlah_trx,
                               x="METODE_PEMILIHAN",
                               y="JUMLAH_PAKET",
                               color="METODE_PEMILIHAN",
                               color_discrete_sequence=px.colors.qualitative.Bold,
                               title="Jumlah Paket per Metode Pemilihan",
                               labels={"METODE_PEMILIHAN": "Metode Pemilihan",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_mp_2:

                st.subheader("Berdasarkan Nilai Metode Pemilihan")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan Metode Pemilihan

                tabel_mp_nilai_trx = con.execute("""
                    SELECT mtd_pemilihan AS METODE_PEMILIHAN, 
                           SUM(pagu) AS NILAI_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_PEMILIHAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_mp_2_1, grafik_mp_2_2 = st.columns((3,7))

                with grafik_mp_2_1:

                    gd_mp_nilai = GridOptionsBuilder.from_dataframe(tabel_mp_nilai_trx)
                    gd_mp_nilai.configure_default_column(autoSizeColumns=True)
                    gd_mp_nilai.configure_column("NILAI_PAKET", valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_mp_nilai_trx,
                          gridOptions=gd_mp_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_mp_nilai_trx) + 1)))

                with grafik_mp_2_2:
                    fig = px.bar(tabel_mp_nilai_trx,
                               x="METODE_PEMILIHAN",
                               y="NILAI_PAKET",
                               color="METODE_PEMILIHAN",
                               color_discrete_sequence=px.colors.qualitative.Bold,
                               title="Nilai Paket per Metode Pemilihan",
                               labels={"METODE_PEMILIHAN": "Metode Pemilihan",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Metode Evaluasi
            grafik_me_1, grafik_me_2 = st.tabs(["| Berdasarkan Jumlah Metode Evaluasi |", "| Berdasarkan Nilai Metode Evaluasi |"])

            with grafik_me_1:

                st.subheader("Berdasarkan Jumlah Metode Evaluasi")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Metode Evaluasi

                tabel_me_jumlah_trx = con.execute("""
                    SELECT mtd_evaluasi AS METODE_EVALUASI, 
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_EVALUASI 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_me_1_1, grafik_me_1_2 = st.columns((3,7))

                with grafik_me_1_1:

                    gd_me_hitung = GridOptionsBuilder.from_dataframe(tabel_me_jumlah_trx)
                    gd_me_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_me_jumlah_trx, 
                           gridOptions=gd_me_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_me_jumlah_trx) + 1)))

                with grafik_me_1_2:
                    fig = px.bar(tabel_me_jumlah_trx,
                               x="METODE_EVALUASI",
                               y="JUMLAH_PAKET",
                               color="METODE_EVALUASI",
                               color_discrete_sequence=px.colors.qualitative.Safe,
                               title="Jumlah Paket per Metode Evaluasi",
                               labels={"METODE_EVALUASI": "Metode Evaluasi",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_me_2:

                st.subheader("Berdasarkan Nilai Metode Evaluasi")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan Metode Evaluasi

                tabel_me_nilai_trx = con.execute("""
                    SELECT mtd_evaluasi AS METODE_EVALUASI, 
                           SUM(pagu) AS NILAI_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_EVALUASI 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_me_2_1, grafik_me_2_2 = st.columns((3,7))

                with grafik_me_2_1:

                    gd_me_nilai = GridOptionsBuilder.from_dataframe(tabel_me_nilai_trx)
                    gd_me_nilai.configure_default_column(autoSizeColumns=True)
                    gd_me_nilai.configure_column("NILAI_PAKET", valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_me_nilai_trx,
                          gridOptions=gd_me_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_me_nilai_trx) + 1)))

                with grafik_me_2_2:

                    fig = px.bar(tabel_me_nilai_trx,
                               x="METODE_EVALUASI",
                               y="NILAI_PAKET",
                               color="METODE_EVALUASI",
                               color_discrete_sequence=px.colors.qualitative.Safe,
                               title="Nilai Paket per Metode Evaluasi",
                               labels={"METODE_EVALUASI": "Metode Evaluasi",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Metode Kualifikasi
            grafik_mk_1, grafik_mk_2 = st.tabs(["| Berdasarkan Jumlah Metode Kualifikasi |", "| Berdasarkan Nilai Metode Kualifikasi |"])

            with grafik_mk_1:

                st.subheader("Berdasarkan Jumlah Metode Kualifikasi")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Metode Kualifikasi

                tabel_mk_jumlah_trx = con.execute("""
                    SELECT mtd_kualifikasi AS METODE_KUALIFIKASI, 
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_KUALIFIKASI 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_mk_1_1, grafik_mk_1_2 = st.columns((3,7))

                with grafik_mk_1_1:

                    gd_mk_hitung = GridOptionsBuilder.from_dataframe(tabel_mk_jumlah_trx)
                    gd_mk_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_mk_jumlah_trx, 
                           gridOptions=gd_mk_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_mk_jumlah_trx) + 1)))

                with grafik_mk_1_2:
                    fig = px.bar(tabel_mk_jumlah_trx,
                               x="METODE_KUALIFIKASI",
                               y="JUMLAH_PAKET",
                               color="METODE_KUALIFIKASI",
                               color_discrete_sequence=px.colors.qualitative.Vivid,
                               title="Jumlah Paket per Metode Kualifikasi",
                               labels={"METODE_KUALIFIKASI": "Metode Kualifikasi",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_mk_2:

                st.subheader("Berdasarkan Nilai Metode Kualifikasi")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan Metode Kualifikasi

                tabel_mk_nilai_trx = con.execute("""
                    SELECT mtd_kualifikasi AS METODE_KUALIFIKASI, 
                           SUM(pagu) AS NILAI_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_KUALIFIKASI 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_mk_2_1, grafik_mk_2_2 = st.columns((3,7))

                with grafik_mk_2_1:

                    gd_mk_nilai = GridOptionsBuilder.from_dataframe(tabel_mk_nilai_trx)
                    gd_mk_nilai.configure_default_column(autoSizeColumns=True)
                    gd_mk_nilai.configure_column("NILAI_PAKET", valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_mk_nilai_trx,
                          gridOptions=gd_mk_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_mk_nilai_trx) + 1)))

                with grafik_mk_2_2:

                    fig = px.bar(tabel_mk_nilai_trx,
                               x="METODE_KUALIFIKASI",
                               y="NILAI_PAKET",
                               color="METODE_KUALIFIKASI",
                               color_discrete_sequence=px.colors.qualitative.Vivid,
                               title="Nilai Paket per Metode Kualifikasi",
                               labels={"METODE_KUALIFIKASI": "Metode Kualifikasi",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Kontrak Pembayaran
            grafik_kontrak_1, grafik_kontrak_2 = st.tabs(["| Berdasarkan Jumlah Kontrak Pembayaran |", "| Berdasarkan Nilai Kontrak Pembayaran |"])

            with grafik_kontrak_1:

                st.subheader("Berdasarkan Jumlah Kontrak Pembayaran")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Kontrak Pembayaran

                tabel_kontrak_jumlah_trx = con.execute("""
                    SELECT kontrak_pembayaran AS KONTRAK_PEMBAYARAN,
                           COUNT(DISTINCT kd_tender) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY KONTRAK_PEMBAYARAN 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_kontrak_1_1, grafik_kontrak_1_2 = st.columns((3,7))

                with grafik_kontrak_1_1:

                    gd_kontrak_hitung = GridOptionsBuilder.from_dataframe(tabel_kontrak_jumlah_trx)
                    gd_kontrak_hitung.configure_default_column(autoSizeColumns=True)
                    AgGrid(tabel_kontrak_jumlah_trx, 
                           gridOptions=gd_kontrak_hitung.build(),
                           fit_columns_on_grid_load=True,
                           autoSizeColumns=True,
                           width='100%',
                           height=min(400, 35 * (len(tabel_kontrak_jumlah_trx) + 1)))

                with grafik_kontrak_1_2:

                    fig = px.bar(tabel_kontrak_jumlah_trx,
                               x="KONTRAK_PEMBAYARAN",
                               y="JUMLAH_PAKET",
                               color="KONTRAK_PEMBAYARAN", 
                               color_discrete_sequence=px.colors.qualitative.Set3,
                               title="Jumlah Paket per Kontrak Pembayaran",
                               labels={"KONTRAK_PEMBAYARAN": "Kontrak Pembayaran",
                                     "JUMLAH_PAKET": "Jumlah Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)
        
            with grafik_kontrak_2:

                st.subheader("Berdasarkan Nilai Kontrak Pembayaran")

                #### Query data grafik nilai transaksi pengumuman SPSE berdasarkan Kontrak Pembayaran

                tabel_kontrak_nilai_trx = con.execute("""
                    SELECT kontrak_pembayaran AS KONTRAK_PEMBAYARAN, 
                           SUM(pagu) AS NILAI_PAKET
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY KONTRAK_PEMBAYARAN 
                    ORDER BY NILAI_PAKET DESC
                """).df()

                grafik_kontrak_2_1, grafik_kontrak_2_2 = st.columns((3,7))

                with grafik_kontrak_2_1:

                    gd_kontrak_nilai = GridOptionsBuilder.from_dataframe(tabel_kontrak_nilai_trx)
                    gd_kontrak_nilai.configure_default_column(autoSizeColumns=True)
                    gd_kontrak_nilai.configure_column("NILAI_PAKET", valueFormatter="data.NILAI_PAKET.toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
                    AgGrid(tabel_kontrak_nilai_trx,
                          gridOptions=gd_kontrak_nilai.build(),
                          fit_columns_on_grid_load=True,
                          autoSizeColumns=True,
                          width='100%',
                          height=min(400, 35 * (len(tabel_kontrak_nilai_trx) + 1)))

                with grafik_kontrak_2_2:

                    fig = px.bar(tabel_kontrak_nilai_trx,
                               x="KONTRAK_PEMBAYARAN",
                               y="NILAI_PAKET", 
                               color="KONTRAK_PEMBAYARAN",
                               color_discrete_sequence=px.colors.qualitative.Set3,
                               title="Nilai Paket per Kontrak Pembayaran",
                               labels={"KONTRAK_PEMBAYARAN": "Kontrak Pembayaran",
                                     "NILAI_PAKET": "Nilai Paket"})
                    fig.update_layout(showlegend=False)
                    fig.update_traces(marker_line_color='rgb(8,48,107)',
                                    marker_line_width=1.5,
                                    opacity=0.8)
                    st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

with menu_tender_2:
    st.subheader("SPPBJ TENDER")

with menu_tender_3:
    st.subheader("KONTRAK TENDER")

with menu_tender_4:
    try:
        # Baca dataset kontrak
        dfSPSETenderKontrak = read_df_duckdb(datasets["TenderKontrak"])
        # Baca dataset SPMK
        dfSPSETenderSPMK = read_df_duckdb(datasets["TenderSPMK"])
        # Filter kolom kontrak
        dfSPSETenderKontrak_filter_kolom = dfSPSETenderKontrak[["kd_tender", "nilai_kontrak", "nilai_pdn_kontrak", "nilai_umk_kontrak"]]
        dfSPSETenderSPMK_OK = dfSPSETenderSPMK.merge(dfSPSETenderKontrak_filter_kolom, how='left', on='kd_tender')

        # Header dan tombol unduh
        col1, col2 = st.columns([7,3])
        col1.subheader("SPMK TENDER")
        col2.download_button(
            label="📥 Unduh Data SPMK Tender",
            data=download_excel(dfSPSETenderSPMK_OK),
            file_name=f"Tender-SPMK-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.divider()

        jumlah_spmk = dfSPSETenderSPMK_OK['kd_tender'].nunique()
        nilai_spmk = dfSPSETenderSPMK_OK['nilai_kontrak'].sum()

        col1, col2 = st.columns(2)
        col1.metric("Jumlah Total SPMK", f"{jumlah_spmk:,}")
        col2.metric("Nilai Total SPMK", f"{nilai_spmk:,.2f}")

        st.divider()

        # Filter by OPD
        opd_TSPMK = st.selectbox("Pilih Perangkat Daerah:", dfSPSETenderSPMK_OK['nama_satker'].unique(), key='Tender_OPD_SPMK')
        st.write(f"Anda memilih: **{opd_TSPMK}**")

        # Get filtered data and metrics
        filtered_spmk = dfSPSETenderSPMK_OK[dfSPSETenderSPMK_OK['nama_satker'] == opd_TSPMK]
        jumlah_spmk = filtered_spmk['kd_tender'].nunique()
        nilai_spmk = filtered_spmk['nilai_kontrak'].sum()

        # Display metrics
        col1, col2 = st.columns(2)
        col1.metric("Jumlah Tender SPMK", f"{jumlah_spmk:,}")
        col2.metric("Nilai Tender SPMK", f"{nilai_spmk:,.2f}")

        st.divider()

        # Persiapkan data untuk tabel SPMK
        tabel_tender_spmk = filtered_spmk[['nama_paket', 'no_spmk_spp', 'tgl_spmk_spp', 
                                         'nama_ppk', 'nama_penyedia', 'wakil_sah_penyedia',
                                         'npwp_penyedia', 'nilai_kontrak', 'nilai_pdn_kontrak', 
                                         'nilai_umk_kontrak']]

        # Konfigurasi AgGrid
        gb = GridOptionsBuilder.from_dataframe(tabel_tender_spmk)
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
        
        # Format kolom nilai ke rupiah
        gb.configure_column('nilai_kontrak', type=["numericColumn", "numberColumnFilter"], valueFormatter="data.nilai_kontrak.toLocaleString('id-ID', {style: 'currency', currency: 'IDR'})")
        gb.configure_column('nilai_pdn_kontrak', type=["numericColumn", "numberColumnFilter"], valueFormatter="data.nilai_pdn_kontrak.toLocaleString('id-ID', {style: 'currency', currency: 'IDR'})")
        gb.configure_column('nilai_umk_kontrak', type=["numericColumn", "numberColumnFilter"], valueFormatter="data.nilai_umk_kontrak.toLocaleString('id-ID', {style: 'currency', currency: 'IDR'})")

        # Rename kolom untuk tampilan
        gb.configure_columns({
            'nama_paket': 'NAMA PAKET',
            'no_spmk_spp': 'NO SPMK', 
            'tgl_spmk_spp': 'TGL SPMK',
            'nama_ppk': 'NAMA PPK',
            'nama_penyedia': 'NAMA PENYEDIA',
            'wakil_sah_penyedia': 'WAKIL SAH',
            'npwp_penyedia': 'NPWP PENYEDIA',
            'nilai_kontrak': 'NILAI KONTRAK',
            'nilai_pdn_kontrak': 'NILAI PDN',
            'nilai_umk_kontrak': 'NILAI UMK'
        })

        gridOptions = gb.build()
        
        AgGrid(tabel_tender_spmk,
               gridOptions=gridOptions,
               enable_enterprise_modules=True,
               update_mode=GridUpdateMode.MODEL_CHANGED,
               height=800)
        

    except Exception as e:
        st.error(f"Error: {e}")

with menu_tender_5:
    try:
        # Baca dataset BAPBAST
        dfSPSETenderBAST = read_df_duckdb(datasets["TenderBAST"]).drop_duplicates(subset=['kd_tender'])

        # Header dan tombol unduh
        col1, col2 = st.columns([7,3])
        col1.subheader("BAPBAST TENDER") 
        col2.download_button(
            label="📥 Unduh Data BAPBAST Tender",
            data=download_excel(dfSPSETenderBAST),
            file_name=f"Tender-BAPBAST-{kodeFolder}-{tahun}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        st.divider()

        # Metrics total
        jumlah_bast = dfSPSETenderBAST['kd_tender'].nunique()
        nilai_bast = dfSPSETenderBAST['nilai_kontrak'].sum()

        col3, col4 = st.columns(2)
        col3.metric("Jumlah Total BAPBAST", f"{jumlah_bast:,}")
        col4.metric("Nilai Total BAPBAST", f"{nilai_bast:,.2f}")

        st.divider()

        # Filter
        col5, col6 = st.columns([2,8])
        with col5:
            status_options = ["Semua"] + list(dfSPSETenderBAST['status_kontrak'].unique())
            status = st.radio("**Status Kontrak**", status_options)
        with col6:
            opd_options = ["SEMUA PERANGKAT DAERAH"] + list(dfSPSETenderBAST['nama_satker'].unique())
            opd = st.selectbox("Pilih Perangkat Daerah:", opd_options)
        st.write(f"Anda memilih: **{status}** dari **{opd}**")

        # Data terfilter
        if status == "Semua" and opd == "SEMUA PERANGKAT DAERAH":
            filtered_df = dfSPSETenderBAST
        elif status == "Semua":
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSETenderBAST 
                WHERE nama_satker = '{opd}'
            """).df()
        elif opd == "SEMUA PERANGKAT DAERAH":
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSETenderBAST 
                WHERE status_kontrak = '{status}'
            """).df()
        else:
            filtered_df = con.execute(f"""
                SELECT * FROM dfSPSETenderBAST 
                WHERE status_kontrak = '{status}' 
                AND nama_satker = '{opd}'
            """).df()

        # Metrics filter
        jumlah_filter = filtered_df['kd_tender'].nunique()
        nilai_filter = filtered_df['nilai_kontrak'].sum()

        col7, col8 = st.columns(2)
        col7.metric("Jumlah BAPBAST", f"{jumlah_filter:,}")
        col8.metric("Nilai BAPBAST", f"{nilai_filter:,.2f}")

        st.divider()

        # Tabel
        renamed_columns = {
            'nama_paket': 'NAMA PAKET',
            'no_bast': 'NOMOR BAST', 
            'tgl_bast': 'TANGGAL BAST',
            'nama_ppk': 'NAMA PPK',
            'nama_penyedia': 'NAMA PENYEDIA',
            'wakil_sah_penyedia': 'WAKIL SAH PENYEDIA',
            'npwp_penyedia': 'NPWP PENYEDIA',
            'nilai_kontrak': 'NILAI KONTRAK',
            'besar_pembayaran': 'BESAR PEMBAYARAN'
        }
        
        display_df = filtered_df[list(renamed_columns.keys())].rename(columns=renamed_columns)
        
        gd = GridOptionsBuilder.from_dataframe(display_df)
        gd.configure_default_column(autoSizeColumns=True)
        gd.configure_column("NILAI KONTRAK", valueFormatter="data['NILAI KONTRAK'].toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
        gd.configure_column("BESAR PEMBAYARAN", valueFormatter="data['BESAR PEMBAYARAN'].toLocaleString('id-ID', {style: 'currency', currency: 'IDR', minimumFractionDigits: 0})")
        
        AgGrid(display_df,
              gridOptions=gd.build(),
              enable_enterprise_modules=True,
              fit_columns_on_grid_load=True,
              autoSizeColumns=True,
              width='100%',
              height=800)

    except Exception as e:
        st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")