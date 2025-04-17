# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from datetime import datetime
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode
# Library Tambahan
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

st.header(f"PENILAIAN SIKAP - {pilih} - TAHUN {tahun}")

menu_tender, menu_nontender = st.tabs(["| SIKAP TENDER |", "| SIKAP NON TENDER |"])

# Fungsi untuk memproses data SIKAP
def proses_data_sikap(jenis, kd_field):
    try:
        st.subheader(f"SIKAP {jenis}")
        
        # Baca dataset
        dataset_pengumuman = f"https://data.pbj.my.id/{kodeLPSE}/spse/SPSE-{jenis}Pengumuman{tahun}.parquet"
        
        # Penyesuaian nama dataset untuk NonTender
        if jenis == "NonTender":
            dataset_sikap = f"https://data.pbj.my.id/{kodeRUP}/sikap/SIKaP-PenilaianKinerjaPenyedia-NonTender{tahun}.parquet"
        else:
            dataset_sikap = f"https://data.pbj.my.id/{kodeRUP}/sikap/SIKaP-PenilaianKinerjaPenyedia-{jenis}{tahun}.parquet"
        
        df_pengumuman = read_df_duckdb(dataset_pengumuman)
        df_sikap = read_df_duckdb(dataset_sikap)
        
        # Query data
        status_field = f"status_{kd_field.lower()}"
        df_pengumuman_filter = con.execute(f"SELECT {kd_field}, nama_satker, pagu, hps, jenis_pengadaan, mtd_pemilihan FROM df_pengumuman WHERE {status_field} = 'Selesai'").df()
        df_sikap_filter = con.execute(f"SELECT {kd_field}, nama_paket, nama_ppk, nama_penyedia, npwp_penyedia, indikator_penilaian, nilai_indikator, total_skors FROM df_sikap").df()
        df_sikap_ok = df_pengumuman_filter.merge(df_sikap_filter, how='right', on=kd_field)
        
        # Hitung statistik
        jumlah_paket_selesai = df_pengumuman_filter[kd_field].nunique()
        jumlah_paket_dinilai = df_sikap_filter[kd_field].nunique()
        selisih_paket = jumlah_paket_selesai - jumlah_paket_dinilai
        
        # Tampilkan metrik
        col1, col2, col3 = st.columns(3)
        label_paket = f"Jumlah Paket {jenis}" if jenis == "NonTender" else "Jumlah Paket Tender Selesai"
        col1.metric(label=label_paket, value="{:,}".format(jumlah_paket_selesai))
        col2.metric(label="Jumlah Paket Sudah Dinilai", value="{:,}".format(jumlah_paket_dinilai))
        col3.metric(label="Jumlah Paket Belum Dinilai", value="{:,}".format(selisih_paket))
        
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
            label = f"📥 Download Data SIKAP {jenis}",
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
            fit_columns_on_grid_load=True,
            height=500,
            width='100%',
            theme='streamlit',
            update_mode=GridUpdateMode.MODEL_CHANGED
        )
        
    # except Exception:
    #     st.error(f"Gagal Analisa Penilaian SIKAP {jenis}")

    except Exception as e:
        st.error(f"Gagal Analisa Penilaian SIKAP {jenis}: {e}")

# Proses data untuk Tender dan NonTender
with menu_tender:
    proses_data_sikap("Tender", "kd_tender")

with menu_nontender:
    proses_data_sikap("NonTender", "kd_nontender")

# Styling
style_metric_cards(background_color="#000", border_left_color="#D3D3D3")