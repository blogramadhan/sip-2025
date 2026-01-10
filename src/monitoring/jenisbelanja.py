# Library Utama
import streamlit as st
import pandas as pd
import duckdb
from datetime import datetime
from babel.numbers import format_currency
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from fungsi import *

# Membuat UKPBJ
daerah = region_config()
pilih = st.sidebar.selectbox("Pilih Daerah", list(daerah.keys()))
tahun = st.sidebar.selectbox("Pilih Tahun", [2025, 2024, 2023])
selected_daerah = daerah.get(pilih, {})
kodeFolder = selected_daerah.get("folder")
kodeRUP = selected_daerah.get("RUP")
kodeLPSE = selected_daerah.get("LPSE")

# Koneksi DuckDB
con = duckdb.connect(database=':memory:');

# URL Dataset Jenis Belanja
base_url = f"https://s3-sip.pbj.my.id/rup/{kodeRUP}"
datasets = {
    'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan/{tahun}/data.parquet",
    'PAP': f"{base_url}/RUP-PaketAnggaranPenyedia/{tahun}/data.parquet"
}

try:
    st.title("JENIS BELANJA")
    st.header(f"{pilih} TAHUN {tahun}")
    st.divider()

    # Baca dan filter data RUP
    dfRUPPP = read_df_duckdb(datasets['PP'])
    dfRUPPAP = read_df_duckdb(datasets['PAP'])
    
    dfRUPPP_filter = con.execute("""
        SELECT a.kd_rup, a.nama_satker, a.nama_paket, a.pagu, 
               a.metode_pengadaan, a.jenis_pengadaan, a.status_pdn, 
               a.status_ukm, b.mak,
               SUBSTRING(b.mak, 19, 6) as kd_belanja
        FROM dfRUPPP a
        LEFT JOIN dfRUPPAP b ON a.kd_rup = b.kd_rup 
        WHERE a.status_umumkan_rup = 'Terumumkan' 
        AND a.status_aktif_rup = 'true'
        AND a.metode_pengadaan <> '0'
    """).df()

    # Buat dataframe nama_satker unik
    namaopd = con.execute("""
        SELECT DISTINCT nama_satker 
        FROM dfRUPPP_filter
        ORDER BY nama_satker
    """).df()['nama_satker']

    # st.dataframe(dfRUPPP_filter)

    with st.container(border=True):
        st.markdown("#### 🔍 Filter Data")
        satker_options = ["SEMUA PERANGKAT DAERAH"] + list(namaopd)
        satker = st.selectbox("🏛️ Perangkat Daerah", satker_options, key="jenis_belanja")

    if satker == "SEMUA PERANGKAT DAERAH":
        dfRUPPP_PD_Profil = dfRUPPP_filter
    else:
        dfRUPPP_PD_Profil = con.execute(f"SELECT * FROM dfRUPPP_filter WHERE nama_satker = '{satker}'").df()

    # Hitung total pagu untuk Belanja Operasi
    # Hitung total pagu untuk Belanja Operasi
    belanja_operasi_pbj = con.execute("SELECT SUM(pagu) FROM dfRUPPP_PD_Profil WHERE kd_belanja = '5.1.02'").fetchone()[0] or 0
    belanja_operasi_bansos = con.execute("SELECT SUM(pagu) FROM dfRUPPP_PD_Profil WHERE kd_belanja = '5.1.05'").fetchone()[0] or 0
    belanja_operasi_hibah = con.execute("SELECT SUM(pagu) FROM dfRUPPP_PD_Profil WHERE kd_belanja = '5.1.06'").fetchone()[0] or 0

    # Hitung total pagu untuk Belanja Modal
    belanja_modal_pbj = con.execute("SELECT SUM(pagu) FROM dfRUPPP_PD_Profil WHERE kd_belanja LIKE '5.2%'").fetchone()[0] or 0

    # Hitung total pagu untuk Belanja Tidak Terduga  
    belanja_tidak_terduga = con.execute("SELECT SUM(pagu) FROM dfRUPPP_PD_Profil WHERE kd_belanja LIKE '5.3%'").fetchone()[0] or 0

    # st.write(f"Total Belanja Operasi PBJ : {belanja_operasi_pbj}")
    # st.write(f"Total Belanja Operasi Bansos : {belanja_operasi_bansos}")
    # st.write(f"Total Belanja Operasi Hibah : {belanja_operasi_hibah}")
    # st.write(f"Total Belanja Modal PBJ : {belanja_modal_pbj}")
    # st.write(f"Total Belanja Tidak Terduga : {belanja_tidak_terduga}")

    ProfilPD1, ProfilPD2 = st.columns((8,2))
    with ProfilPD1:
        st.subheader(f"{satker}")
    with ProfilPD2:
        st.download_button(
            label="📥 Jenis Belanja",
            data=download_excel(dfRUPPP_filter),
            file_name=f"ProfilRUPMAK_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.divider()

    st.subheader("BELANJA OPERASI")
    col_bo1, col_bo2, col_bo3 = st.columns(3)
    col_bo1.metric(label="Belanja Operasi PBJ", value=format_currency(belanja_operasi_pbj, 'IDR', locale='id_ID').replace('Rp', 'Rp. '))
    col_bo2.metric(label="Belanja Operasi Bansos", value=format_currency(belanja_operasi_bansos, 'IDR', locale='id_ID').replace('Rp', 'Rp. '))
    col_bo3.metric(label="Belanja Operasi Hibah", value=format_currency(belanja_operasi_hibah, 'IDR', locale='id_ID').replace('Rp', 'Rp. '))

    st.divider()

    st.subheader("BELANJA MODAL")
    col_bm1, col_bm2, col_bm3 = st.columns(3)
    col_bm1.metric(label="Belanja Modal PBJ", value=format_currency(belanja_modal_pbj, 'IDR', locale='id_ID').replace('Rp', 'Rp. '))
    
    st.divider()

    st.subheader("BELANJA TIDAK TERDUGA")
    col_bt1, col_bt2, col_bt3 = st.columns(3)
    col_bt1.metric(label="Belanja Tidak Terduga", value=format_currency(belanja_tidak_terduga, 'IDR', locale='id_ID').replace('Rp', 'Rp. '))

    style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10)

except Exception as e:
    st.error(f"Error: {e}")
