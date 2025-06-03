# Library Utama
import streamlit as st
import pandas as pd
import duckdb
from datetime import datetime
# Library Currency
from babel.numbers import format_currency
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
con = duckdb.connect(database=':memory:');

# URL Dataset Jenis Belanja
base_url = f"https://data.pbj.my.id/{kodeRUP}/sirup"
datasets = {
    'PP': f"{base_url}/RUP-PaketPenyedia-Terumumkan{tahun}.parquet",
    'PAP': f"{base_url}/RUP-PaketAnggaranPenyedia{tahun}.parquet"
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

    satker_options = ["SEMUA PERANGKAT DAERAH"] + list(namaopd)
    satker = st.selectbox("Pilih Perangkat Daerah :", satker_options, key="jenis_belanja")

    if satker == "SEMUA PERANGKAT DAERAH":
        dfRUPPP_PD_Profil = dfRUPPP_filter
    else:
        dfRUPPP_PD_Profil = con.execute(f"SELECT * FROM dfRUPPP_filter WHERE nama_satker = '{satker}'").df()

    # Hitung total pagu untuk Belanja Operasi
    belanja_operasi_pbj = dfRUPPP_PD_Profil[dfRUPPP_PD_Profil['kd_belanja'] == '5.1.02']['pagu'].sum()
    belanja_operasi_bansos = dfRUPPP_PD_Profil[dfRUPPP_PD_Profil['kd_belanja'] == '5.1.05']['pagu'].sum()
    belanja_operasi_hibah = dfRUPPP_PD_Profil[dfRUPPP_PD_Profil['kd_belanja'] == '5.1.06']['pagu'].sum()

    # Hitung total pagu untuk Belanja Modal
    belanja_modal_pbj = dfRUPPP_PD_Profil[dfRUPPP_PD_Profil['kd_belanja'].str.startswith('5.2', na=False)]['pagu'].sum()

    # Hitung total pagu untuk Belanja Tidak Terduga
    belanja_tidak_terduga = dfRUPPP_PD_Profil[dfRUPPP_PD_Profil['kd_belanja'].str.startswith('5.3', na=False)]['pagu'].sum()

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
            label="📥 Unduh RUP Jenis Belanja",
            data=download_excel(dfRUPPP_filter),
            file_name=f"ProfilRUPMAK_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.divider()

    st.subheader("BELANJA OPERASIONAL")

except Exception as e:
    st.error(f"Error: {e}")
