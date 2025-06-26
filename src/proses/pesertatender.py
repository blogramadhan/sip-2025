# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from datetime import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.metric_cards import style_metric_cards
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

# URL Dataset
base_url_tender = f"https://s3-sip.pbj.my.id/spse/{kodeLPSE}"
base_url_rup = f"https://s3-sip.pbj.my.id/rup/{kodeRUP}"
datasets = {
    'SPSETenderPengumuman': f"{base_url_tender}/SPSE-TenderPengumuman/{tahun}/data.parquet",
    'PesertaTender': f"{base_url_tender}/SPSE-PesertaTender/{tahun}/data.parquet",
    'RUPMasterSatker': f"{base_url_rup}/RUP-MasterSatker/{tahun}/data.parquet"
}

st.title("PESERTA TENDER")
st.header(f"{pilih} - TAHUN {tahun}")
st.divider()
try:    
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
        st.subheader("PESERTA TENDER")
    with col2:
        st.download_button(
            label = "📥 Download Data Peserta Tender",
            data = download_excel(df_PesertaTenderDetail),
            file_name = f"SPSEPesertaTenderDetail-{kodeFolder}-{tahun}.xlsx",
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    # Filter berdasarkan sumber dana
    sumber_dana_options = ["SEMUA"] + list(df_PesertaTenderDetail['sumber_dana'].unique())
    sumber_dana_pt = st.radio("**Sumber Dana :**", sumber_dana_options, key="DataPesertaTender")
    
    # Filter data
    df_filtered = df_PesertaTenderDetail if sumber_dana_pt == "SEMUA" else df_PesertaTenderDetail.query(f"sumber_dana == '{sumber_dana_pt}'")
    
    # Hitung statistik
    peserta_daftar = df_filtered.query("nilai_penawaran.isnull() and nilai_terkoreksi.isnull()")
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
        status_pemenang_pt = st.radio("**Tabel Data Peserta :**", ["SEMUA", "PEMENANG", "MENDAFTAR", "MENAWAR"])
    with col_satker:
        satker_options = ["SEMUA"] + list(df_filtered['nama_satker'].unique())
        status_opd_pt = st.selectbox("**Pilih Satker :**", satker_options)

    # Query conditions
    query_conditions = {
        "PEMENANG": "NILAI_PENAWARAN > 0 AND NILAI_TERKOREKSI > 0 AND pemenang = 1",
        "MENDAFTAR": "NILAI_PENAWARAN IS NULL AND NILAI_TERKOREKSI IS NULL",
        "MENAWAR": "NILAI_PENAWARAN > 0 AND NILAI_TERKOREKSI > 0",
        "SEMUA": "1=1"
    }
    
    # SQL query berdasarkan filter
    satker_filter = "" if status_opd_pt == "SEMUA" else f"AND NAMA_SATKER = '{status_opd_pt}'"
    
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
        WHERE {query_conditions[status_pemenang_pt]} {satker_filter}
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

    # Konfigurasi tabel
    gd = GridOptionsBuilder.from_dataframe(jumlah_PeserteTender)
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