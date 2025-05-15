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

# URL Dataset Pencatatan
base_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
datasets = {
    'CatatNonTender': f"{base_url}/SPSE-PencatatanNonTender{tahun}.parquet",
    'CatatNonTenderRealisasi': f"{base_url}/SPSE-PencatatanNonTenderRealisasi{tahun}.parquet",
    'CatatSwakelola': f"{base_url}/SPSE-PencatatanSwakelola{tahun}.parquet",
    'CatatSwakelolaRealisasi': f"{base_url}/SPSE-PencatatanSwakelolaRealisasi{tahun}.parquet",
}

st.title(f"TRANSAKSI PENCATATAN")
st.header(f"{pilih} - TAHUN {tahun}")

menu_pencatatan_1, menu_pencatatan_2 = st.tabs(["| PENCATATAN NON TENDER |", "| PENCATATAN SWAKELOLA |"])

with menu_pencatatan_1:
    try:
        # Baca dan gabungkan dataset pencatatan non tender
        dfCatatNonTender = read_df_duckdb(datasets['CatatNonTender'])
        dfCatatNonTenderRealisasi = read_df_duckdb(datasets['CatatNonTenderRealisasi'])[[
            "kd_nontender_pct", "jenis_realisasi", "no_realisasi", 
            "tgl_realisasi", "nilai_realisasi", "nama_penyedia", "npwp_penyedia"
        ]]
        dfGabung = dfCatatNonTender.merge(dfCatatNonTenderRealisasi, how='left', on='kd_nontender_pct')

        # Header dan tombol unduh
        col1, col2 = st.columns((7,3))
        with col1:
            st.subheader(f"PENCATATAN NON TENDER TAHUN {tahun}")
        with col2:
            st.download_button(
                label = "📥 Download Data Pencatatan Non Tender",
                data = download_excel(dfGabung),
                file_name = f"SPSEPencatatanNonTender-{kodeFolder}-{tahun}.xlsx",
                mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        st.divider()

        # Filter dan metrik
        sumber_dana = st.radio("**Sumber Dana:**", dfCatatNonTender['sumber_dana'].unique(), key="CatatNonTender")
        st.write(f"Anda memilih: **{sumber_dana}**")

        df_filtered = dfCatatNonTender.query(f"sumber_dana == '{sumber_dana}'")
        
        # Hitung jumlah berdasarkan status
        status_counts = {
            'Berjalan': len(df_filtered.query("status_nontender_pct_ket == 'Paket Sedang Berjalan'")),
            'Selesai': len(df_filtered.query("status_nontender_pct_ket == 'Paket Selesai'")), 
            'Dibatalkan': len(df_filtered.query("status_nontender_pct_ket == 'Paket Dibatalkan'"))
        }

        # Tampilkan metrik
        cols = st.columns(3)
        for i, (label, value) in enumerate(status_counts.items()):
            cols[i].metric(f"Jumlah Pencatatan NonTender {label}", "{:,}".format(value))

        st.divider()

        # Container untuk grafik
        with st.container(border=True):
            tabs = st.tabs([
                "| Jumlah - Kategori |",
                "| Nilai - Kategori |", 
                "| Jumlah - Metode |",
                "| Nilai - Metode |"
            ])

            # Tab 1: Jumlah per Kategori
            with tabs[0]:
                st.subheader("Berdasarkan Jumlah Kategori")
                
                sql = """
                    SELECT kategori_pengadaan AS KATEGORI, COUNT(*) AS JUMLAH
                    FROM df_filtered 
                    GROUP BY kategori_pengadaan 
                    ORDER BY JUMLAH DESC
                """
                df_result = con.execute(sql).df()
                
                col1, col2 = st.columns((3,7))
                col1.dataframe(df_result, hide_index=True)
                fig = px.pie(df_result, values="JUMLAH", names="KATEGORI", 
                           title="Jumlah Paket per Kategori", hole=.3)
                col2.plotly_chart(fig, use_container_width=True)

            # Tab 2-4: Implementasi serupa untuk tab lainnya
            # ...

        st.divider()
        
        # Filter status dan OPD
        col1, col2 = st.columns((2,8))
        status = col1.radio("**Status:**", df_filtered['status_nontender_pct_ket'].unique())
        opd = col2.selectbox("**Pilih Satker:**", df_filtered['nama_satker'].unique())

        st.divider()

        # Query dan tampilkan data
        sql = f"""
            SELECT 
                nama_paket AS "Nama Paket",
                jenis_realisasi AS "Jenis Realisasi", 
                no_realisasi AS "No Realisasi",
                tgl_realisasi AS "Tgl Realisasi",
                pagu AS "Pagu",
                total_realisasi AS "Total Realisasi",
                nilai_realisasi AS "Nilai Realisasi"
            FROM df_filtered
            WHERE status_nontender_pct_ket = '{status}'
            AND nama_satker = '{opd}'
        """
        
        df_result = con.execute(sql).df()
        
        # Tampilkan metrik
        cols = st.columns((2,3,3,2))
        cols[1].metric("Jumlah Pencatatan", "{:,}".format(len(df_result)))
        cols[2].metric("Total Nilai", "{:,}".format(df_result['Nilai Realisasi'].sum()))
        
        st.divider()
        
        # Tampilkan tabel
        st.dataframe(df_result, hide_index=True, height=400)

    except Exception as e:
        st.error(f"Error: {e}")

with menu_pencatatan_2:
    st.subheader("PENCATATAN SWAKELOLA")


