# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
from fungsi import *

# Konfigurasi daerah dan tahun
daerah = region_config()
pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
tahun = st.sidebar.selectbox("Pilih Tahun", range(datetime.now().year, datetime.now().year-3, -1))
selected_daerah = daerah.get(pilih, {})
kodeFolder = selected_daerah.get("folder")
kodeRUP = selected_daerah.get("RUP")
kodeLPSE = selected_daerah.get("LPSE")

# Koneksi DuckDB
con = duckdb.connect(database=':memory:')

st.title(f"PENILAIAN SIKAP")
st.header(f"{pilih} - TAHUN {tahun}")

menu_tender, menu_nontender = st.tabs(["SIKAP TENDER", "SIKAP NON TENDER"])

# Fungsi untuk memproses data SIKAP
def proses_data_sikap(jenis, kd_field):
    try:
        st.subheader(f"SIKAP {jenis}")
        
        # Baca dataset
        dataset_pengumuman = f"https://s3-sip.pbj.my.id/spse/{kodeLPSE}/SPSE-{jenis}Pengumuman/{tahun}/data.parquet"
        
        # Penyesuaian nama dataset untuk NonTender
        if jenis == "NonTender":
            dataset_sikap = f"https://s3-sip.pbj.my.id/sikap/{kodeRUP}/SiKAP-PenilaianKinerjaPenyedia-{jenis}/{tahun}/data.parquet"
        else:
            dataset_sikap = f"https://s3-sip.pbj.my.id/sikap/{kodeRUP}/SIKaP-PenilaianKinerjaPenyedia-{jenis}/{tahun}/data.parquet"
        
        df_pengumuman = read_df_duckdb(dataset_pengumuman)
        df_sikap = read_df_duckdb(dataset_sikap)
        
        # Query data
        if jenis == "NonTender":
            status_field = "status_nontender"
        else:
            status_field = "status_tender"
            
        df_pengumuman_filter = con.execute(f"SELECT {kd_field}, nama_satker, pagu, hps, jenis_pengadaan, mtd_pemilihan FROM df_pengumuman WHERE {status_field} = 'Selesai'").df()
        df_sikap_filter = con.execute(f"SELECT {kd_field}, nama_paket, nama_ppk, nama_penyedia, npwp_penyedia, indikator_penilaian, nilai_indikator, total_skors FROM df_sikap").df()
        df_sikap_ok = df_pengumuman_filter.merge(df_sikap_filter, how='right', on=kd_field)
        
        # Hitung statistik
        jumlah_paket_selesai = df_sikap_ok[kd_field].nunique()
        jumlah_paket_dinilai = df_sikap_ok[kd_field].nunique()
        selisih_paket = jumlah_paket_selesai - jumlah_paket_dinilai
        
        # Tampilkan metrik
        col1, col2, col3 = st.columns(3)
        label_paket = f"Jumlah Paket {jenis}" if jenis == "NonTender" else "Jumlah Paket Tender Selesai"
        col1.metric(label=label_paket, value="{:,}".format(jumlah_paket_selesai))
        col2.metric(label="Jumlah Paket Sudah Dinilai", value="{:,}".format(jumlah_paket_dinilai))
        col3.metric(label="Jumlah Paket Belum Dinilai", value="{:,}".format(selisih_paket))

        style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)
        
        st.divider()
        
        # Olah data untuk tampilan
        df_sikap_filter = con.execute(f"""
            SELECT 
                nama_paket AS NAMA_PAKET, 
                {kd_field} AS KODE_PAKET, 
                jenis_pengadaan AS JENIS_PENGADAAN, 
                nama_ppk AS NAMA_PPK, 
                nama_penyedia AS NAMA_PENYEDIA, 
                AVG(total_skors) AS SKOR_PENILAIAN 
            FROM df_sikap_ok 
            GROUP BY KODE_PAKET, NAMA_PAKET, JENIS_PENGADAAN, NAMA_PPK, NAMA_PENYEDIA
        """).df()
        
        # Tambahkan kolom keterangan
        df_sikap_final = df_sikap_filter.assign(
            KETERANGAN = np.where(df_sikap_filter['SKOR_PENILAIAN'] >= 3, "SANGAT BAIK", 
                        np.where(df_sikap_filter['SKOR_PENILAIAN'] >= 2, "BAIK", 
                        np.where(df_sikap_filter['SKOR_PENILAIAN'] >= 1, "CUKUP", "BURUK")))
        )
        
        # Tombol unduh
        st.download_button(
            label = "📥 Excel",
            data = download_excel(df_sikap_final),
            file_name = f"SIKAP{jenis}-{kodeFolder}-{tahun}.xlsx",
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # Tampilkan data menggunakan AgGrid
        gb = GridOptionsBuilder.from_dataframe(df_sikap_final)
        gb.configure_column("NAMA_PAKET", header_name="NAMA PAKET")
        gb.configure_column("KODE_PAKET", header_name="KODE PAKET")
        gb.configure_column("JENIS_PENGADAAN", header_name="JENIS PENGADAAN")
        gb.configure_column("NAMA_PPK", header_name="NAMA PPK")
        gb.configure_column("NAMA_PENYEDIA", header_name="NAMA PENYEDIA")
        gb.configure_column("SKOR_PENILAIAN", header_name="SKOR")
        gb.configure_column("KETERANGAN", header_name="KETERANGAN")
        gb.configure_grid_options(domLayout='normal')
        gridOptions = gb.build()
        
        AgGrid(
            df_sikap_final,
            gridOptions=gridOptions,
            enable_enterprise_modules=True,
            fit_columns_on_grid_load=True,
            height=800,
            width='100%',
            theme='streamlit',
            update_mode=GridUpdateMode.MODEL_CHANGED
        )
        
    except Exception as e:
        st.error(f"Gagal Analisa Penilaian SIKAP {jenis}: {e}")

# Proses data untuk Tender dan NonTender
with menu_tender:
    proses_data_sikap("Tender", "kd_tender")

with menu_nontender:
    proses_data_sikap("NonTender", "kd_nontender")
