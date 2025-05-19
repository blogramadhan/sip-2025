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

                    st.dataframe(
                        tabel_kp_jumlah_trx,
                        column_config={
                            "KUALIFIKASI_PAKET": "KUALIFIKASI PAKET",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                with grafik_kp_1_2:

                    st.bar_chart(tabel_kp_jumlah_trx, x="KUALIFIKASI_PAKET", y="JUMLAH_PAKET", color="KUALIFIKASI_PAKET")
        
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

                    st.dataframe(
                        tabel_kp_nilai_trx,
                        column_config={
                            "KUALIFIKASI_PAKET": "KUALIFIKASI PAKET",
                            "NILAI_PAKET": "NILAI PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_kp_2_2:

                    st.bar_chart(tabel_kp_nilai_trx, x="KUALIFIKASI_PAKET", y="NILAI_PAKET", color="KUALIFIKASI_PAKET")

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

                    st.dataframe(
                        tabel_jp_jumlah_trx,
                        column_config={
                            "JENIS_PENGADAAN": "JENIS PENGADAAN",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_jp_1_2:

                    st.bar_chart(tabel_jp_jumlah_trx, x="JENIS_PENGADAAN", y="JUMLAH_PAKET", color="JENIS_PENGADAAN")
        
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

                    st.dataframe(
                        tabel_jp_nilai_trx,
                        column_config={
                            "JENIS_PENGADAAN": "JENIS PENGADAAN",
                            "NILAI_PAKET": "NILAI PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_jp_2_2:

                    st.bar_chart(tabel_jp_nilai_trx, x="JENIS_PENGADAAN", y="NILAI_PAKET", color="JENIS_PENGADAAN")

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

                    st.dataframe(
                        tabel_mp_jumlah_trx,
                        column_config={
                            "METODE_PEMILIHAN": "METODE PEMILIHAN",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                with grafik_mp_1_2:

                    st.bar_chart(tabel_mp_jumlah_trx, x="METODE_PEMILIHAN", y="JUMLAH_PAKET", color="METODE_PEMILIHAN")
        
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

                    st.dataframe(
                        tabel_mp_nilai_trx,
                        column_config={
                            "METODE_PEMILIHAN": "METODE PEMILIHAN",
                            "NILAI_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                with grafik_mp_2_2:

                    st.bar_chart(tabel_mp_nilai_trx, x="METODE_PEMILIHAN", y="NILAI_PAKET", color="METODE_PEMILIHAN")

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

                    st.dataframe(
                        tabel_me_jumlah_trx,
                        column_config={
                            "METODE_EVALUASI": "METODE EVALUASI",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_me_1_2:

                    st.bar_chart(tabel_me_jumlah_trx, x="METODE_EVALUASI", y="JUMLAH_PAKET", color="METODE_EVALUASI")
        
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

                    st.dataframe(
                        tabel_me_nilai_trx,
                        column_config={
                            "METODE_EVALUASI": "METODE EVALUASI",
                            "NILAI_PAKET": "NILAI PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_me_2_2:

                    st.bar_chart(tabel_me_nilai_trx, x="METODE_EVALUASI", y="NILAI_PAKET", color="METODE_EVALUASI")

        with st.container(border=True):

            ### Tabel dan Grafik Jumlah dan Nilai Transaksi SPSE - Tender - Pengumuman Berdasarkan Metode Kualifikasi
            grafik_mk_1, grafik_mk_2 = st.tabs(["| Berdasarkan Jumlah Metode Kualifikasi |", "| Berdasarkan Nilai Metode Kualifikasi |"])

            with grafik_mk_1:

                st.subheader("Berdasarkan Jumlah Metode Kualifikasi")

                #### Query data grafik jumlah transaksi pengumuman SPSE berdasarkan Metode Kualifikasi

                tabel_mk_jumlah_trx = con.execute("""
                    SELECT mtd_kualifikasi AS METODE_KUALIFIKASI, 
                           COUNT(DISTINCT(kd_tender)) AS JUMLAH_PAKET 
                    FROM SPSETenderPengumuman_filter 
                    GROUP BY METODE_KUALIFIKASI 
                    ORDER BY JUMLAH_PAKET DESC
                """).df()

                grafik_mk_1_1, grafik_mk_1_2 = st.columns((3,7))

                with grafik_mk_1_1:

                    st.dataframe(
                        tabel_mk_jumlah_trx,
                        column_config={
                            "METODE_KUALIFIKASI": "METODE KUALIFIKASI",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_mk_1_2:

                    st.bar_chart(tabel_mk_jumlah_trx, x="METODE_KUALIFIKASI", y="JUMLAH_PAKET", color="METODE_KUALIFIKASI")
        
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

                    st.dataframe(
                        tabel_mk_nilai_trx,
                        column_config={
                            "METODE_KUALIFIKASI": "METODE KUALIFIKASI",
                            "NILAI_PAKET": "NILAI PAKET"
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                with grafik_mk_2_2:

                    st.bar_chart(tabel_mk_nilai_trx, x="METODE_KUALIFIKASI", y="NILAI_PAKET", color="METODE_KUALIFIKASI")

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

                    st.dataframe(
                        tabel_kontrak_jumlah_trx,
                        column_config={
                            "KONTRAK_PEMBAYARAN": "KONTRAK PEMBAYARAN",
                            "JUMLAH_PAKET": "JUMLAH PAKET"
                        },
                        use_container_width=True,
                        hide_index=True    
                    )

                with grafik_kontrak_1_2:

                    st.bar_chart(tabel_kontrak_jumlah_trx, x="KONTRAK_PEMBAYARAN", y="JUMLAH_PAKET", color="KONTRAK_PEMBAYARAN")
        
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

                    st.dataframe(
                        tabel_kontrak_nilai_trx, 
                        column_config={
                            "KONTRAK_PEMBAYARAN": "KONTRAK PEMBAYARAN",
                            "NILAI_PAKET": "NILAI PAKET"
                        }    
                    )

                with grafik_kontrak_2_2:

                    st.bar_chart(tabel_kontrak_nilai_trx, x="KONTRAK_PEMBAYARAN", y="NILAI_PAKET", color="KONTRAK_PEMBAYARAN")

    except Exception as e:
        st.error(f"Error: {e}")

with menu_tender_2:
    st.subheader("SPPBJ TENDER")

with menu_tender_3:
    st.subheader("KONTRAK TENDER")

with menu_tender_4:
    st.subheader("SPMK TENDER")

with menu_tender_5:
    st.subheader("BAPBAST TENDER")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")