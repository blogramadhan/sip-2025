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

# URL Dataset
base_url_tender = f"https://data.pbj.my.id/{kodeLPSE}/spse"
base_url_rup = f"https://data.pbj.my.id/{kodeRUP}/sirup"
datasets = {
    'SPSETenderPengumuman': f"{base_url_tender}/SPSE-TenderPengumuman{tahun}.parquet",
    'PesertaTender': f"{base_url_tender}/SPSE-PesertaTender{tahun}.parquet",
    'RUPMasterSatker': f"{base_url_rup}/RUP-MasterSatker{tahun}.parquet"
}

try:
    st.title("PESERTA TENDER")

    # Baca dataset
    df_RUPMasterSatker = read_df_duckdb(datasets['RUPMasterSatker'])
    df_SPSETenderPengumuman = read_df_duckdb(datasets['SPSETenderPengumuman'])
    df_PesertaTender = read_df_duckdb(datasets['PesertaTender'])

    # Gabungkan dataset
    df_PesertaTenderDetail = (df_PesertaTender
        .merge(df_RUPMasterSatker[["kd_satker_str", "nama_satker"]], how='left', on='kd_satker_str')
        .merge(df_SPSETenderPengumuman[["kd_tender", "nama_paket", "pagu", "hps", "sumber_dana"]], how='left', on='kd_tender')
    )

    # Header dan tombol unduh
    col1, col2 = st.columns((7,3))
    with col1:
        st.header(f"SPSE - PESERTA TENDER - {pilih} - TAHUN {tahun}")
    with col2:
        st.download_button(
            label = "📥 Download Data Peserta Tender",
            data = download_excel(df_PesertaTenderDetail),
            file_name = f"SPSEPesertaTenderDetail-{kodeFolder}-{tahun}.xlsx",
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    st.divider()

    # Filter berdasarkan sumber dana
    sumber_dana_options = list(df_PesertaTenderDetail['sumber_dana'].unique())
    sumber_dana_options.insert(0, "SEMUA")
    sumber_dana_pt = st.radio("**Sumber Dana :**", sumber_dana_options, key="DataPesertaTender")
    st.write(f"Anda memilih : **{sumber_dana_pt}**")

    # Filter data
    if sumber_dana_pt == "SEMUA":
        df_filtered = df_PesertaTenderDetail
    else:
        df_filtered = df_PesertaTenderDetail.query(f"sumber_dana == '{sumber_dana_pt}'")
    
    # Hitung statistik
    peserta_daftar = df_filtered.query("nilai_penawaran == 0 and nilai_terkoreksi == 0")
    peserta_nawar = df_filtered.query("nilai_penawaran > 0 and nilai_terkoreksi > 0")
    peserta_menang = df_filtered.query("nilai_penawaran > 0 and nilai_terkoreksi > 0 and pemenang == 1")

    # Tampilkan metrik
    cols = st.columns(4)
    cols[0].metric(label="Jumlah Peserta Yang Mendaftar", value="{:,}".format(len(peserta_daftar)))
    cols[1].metric(label="Jumlah Peserta Yang Menawar", value="{:,}".format(len(peserta_nawar)))
    cols[2].metric(label="Jumlah Peserta Yang Menang", value="{:,}".format(len(peserta_menang)))
    cols[3].metric(label="Nilai Total Terkoreksi Rp. (Pemenang)", value="{:,.2f}".format(peserta_menang['nilai_terkoreksi'].sum()))

    st.divider()

    # Filter berdasarkan status dan satker
    col_status, col_satker = st.columns((2,8))
    with col_status:
        status_pemenang_options = ["PEMENANG", "MENDAFTAR", "MENAWAR", "SEMUA"]
        status_pemenang_pt = st.radio("**Tabel Data Peserta :**", status_pemenang_options)
    with col_satker:
        satker_options = list(df_filtered['nama_satker'].unique())
        satker_options.insert(0, "SEMUA")
        status_opd_pt = st.selectbox("**Pilih Satker :**", satker_options)

    st.divider()

    # Query berdasarkan status
    query_conditions = {
        "PEMENANG": "NILAI_PENAWARAN > 0 AND NILAI_TERKOREKSI > 0 AND pemenang = 1",
        "MENDAFTAR": "NILAI_PENAWARAN = 0 AND NILAI_TERKOREKSI = 0",
        "MENAWAR": "NILAI_PENAWARAN > 0 AND NILAI_TERKOREKSI > 0",
        "SEMUA": "1=1"  # Kondisi yang selalu benar untuk menampilkan semua data
    }
    
    # Ambil data sesuai filter
    if status_opd_pt == "SEMUA":
        jumlah_PeserteTender = con.execute(f"""
            SELECT 
                nama_paket AS NAMA_PAKET, 
                nama_penyedia AS NAMA_PENYEDIA, 
                npwp_penyedia AS NPWP_PENYEDIA, 
                pagu AS PAGU, 
                hps AS HPS, 
                nilai_penawaran AS NILAI_PENAWARAN, 
                nilai_terkoreksi AS NILAI_TERKOREKSI 
            FROM df_filtered 
            WHERE {query_conditions[status_pemenang_pt]}
        """).df()
    else:
        jumlah_PeserteTender = con.execute(f"""
            SELECT 
                nama_paket AS NAMA_PAKET, 
                nama_penyedia AS NAMA_PENYEDIA, 
                npwp_penyedia AS NPWP_PENYEDIA, 
                pagu AS PAGU, 
                hps AS HPS, 
                nilai_penawaran AS NILAI_PENAWARAN, 
                nilai_terkoreksi AS NILAI_TERKOREKSI 
            FROM df_filtered 
            WHERE NAMA_SATKER = '{status_opd_pt}' 
            AND {query_conditions[status_pemenang_pt]}
        """).df()

    # Tampilkan metrik hasil filter
    cols = st.columns(4)
    cols[1].metric(
        label=f"Jumlah Peserta Tender ({status_pemenang_pt})", 
        value="{:,}".format(len(jumlah_PeserteTender))
    )
    cols[2].metric(
        label=f"Nilai Total Terkoreksi ({status_pemenang_pt})", 
        value="{:,.2f}".format(jumlah_PeserteTender['NILAI_TERKOREKSI'].sum())
    )

    st.divider()

    # Konfigurasi dan tampilkan tabel
    gd = GridOptionsBuilder.from_dataframe(jumlah_PeserteTender)
    
    # Konfigurasi kolom
    gd.configure_default_column(groupable=True, value=True, enableRowGroup=True, 
                              aggFunc="sum", editable=True, autoSizeColumns=True)
    
    # Format kolom mata uang
    for col in ["PAGU", "HPS", "NILAI_PENAWARAN", "NILAI_TERKOREKSI"]:
        gd.configure_column(col, 
                          type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                          valueGetter=f"data.{col}.toLocaleString('id-ID', {{style: 'currency', currency: 'IDR', maximumFractionDigits:2}})")
    
    # Konfigurasi nama kolom
    gd.configure_column("NAMA_PAKET", headerName="NAMA PAKET")
    gd.configure_column("NAMA_PENYEDIA", headerName="NAMA PENYEDIA")
    gd.configure_column("NPWP_PENYEDIA", headerName="NPWP PENYEDIA")
    gd.configure_pagination(paginationAutoPageSize=False)
    
    # Tampilkan tabel
    AgGrid(jumlah_PeserteTender,
           gridOptions=gd.build(),
           enable_enterprise_modules=True, 
           update_mode=GridUpdateMode.MODEL_CHANGED,
           fit_columns_on_grid_load=True,
           height=800,
           key='PesertaTender')

except Exception as e:
    st.error(f"Error: {e}")

style_metric_cards(background_color="#000", border_left_color="#D3D3D3")
