# Library Utama
import streamlit as st
import pandas as pd
import numpy as np
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

# URL Dataset SIRUP
sirup_url = f"https://data.pbj.my.id/{kodeRUP}/sirup"
datasets_sirup = {
    'PP': f"{sirup_url}/RUP-PaketPenyedia-Terumumkan{tahun if int(tahun) < 2025 else f'-{tahun}-03-31'}.parquet",
    'PS': f"{sirup_url}/RUP-PaketSwakelola-Terumumkan{tahun if int(tahun) < 2025 else f'-{tahun}-03-31'}.parquet", 
    'SA': f"{sirup_url}/RUP-StrukturAnggaranPD{tahun if int(tahun) < 2025 else f'-{tahun}-03-31'}.parquet"
}

# URL Dataset SPSE dan SIKAP
spse_url = f"https://data.pbj.my.id/{kodeLPSE}/spse"
sikap_url = f"https://data.pbj.my.id/{kodeRUP}/sikap"
epurchasing_url = f"https://data.pbj.my.id/{kodeRUP}/epurchasing"

# Dataset Tender, Non Tender, dan E-Purchasing
datasets_tender = {
    'pengumuman': f"{spse_url}/SPSE-TenderPengumuman{tahun}.parquet",
    'kontrak': f"{spse_url}/SPSE-TenderEkontrak-Kontrak{tahun}.parquet",
    'sikap': f"{sikap_url}/SIKaP-PenilaianKinerjaPenyedia-Tender{tahun}.parquet"
}

datasets_nontender = {
    'pengumuman': f"{spse_url}/SPSE-NonTenderPengumuman{tahun}.parquet",
    'sikap': f"{sikap_url}/SiKAP-PenilaianKinerjaPenyedia-NonTender{tahun}.parquet"
}

datasets_epurchasing = {
    'ecat': f"{epurchasing_url}/Ecat-PaketEPurchasing{tahun}.parquet",
    'ecatis': f"{epurchasing_url}/Ecat-InstansiSatker.parquet",
    'bela': f"{epurchasing_url}/Bela-TokoDaringRealisasi{tahun}.parquet"
}

try:
    # Baca Dataset
    dfRUPPP = read_df_duckdb(datasets_sirup['PP'])
    dfRUPPS = read_df_duckdb(datasets_sirup['PS'])
    dfRUPSA = read_df_duckdb(datasets_sirup['SA'])
    dfSPSE_TenderPengumuman = read_df_duckdb(datasets_tender['pengumuman'])
    dfSPSE_TenderEkontrak = read_df_duckdb(datasets_tender['kontrak'])
    dfSPSE_NonTenderPengumuman = read_df_duckdb(datasets_nontender['pengumuman'])
    dfEcat_PaketEPurchasing = read_df_duckdb(datasets_epurchasing['ecat']).drop('nama_satker', axis=1, errors='ignore')
    dfEcat_InstansiSatker = read_df_duckdb(datasets_epurchasing['ecatis'])
    dfEcat = pd.merge(dfEcat_PaketEPurchasing, dfEcat_InstansiSatker, left_on='satker_id', right_on='kd_satker', how='left')
    dfBela_TokoDaringRealisasi = read_df_duckdb(datasets_epurchasing['bela'])

except Exception as e:
    st.error(f"Error: {e}")

#####
# Konten Data ITKP
#####

st.title(f"PREDIKSI ITKP")
st.header(f"{pilih} - TAHUN {tahun}")

st.divider()

opd_options = ["Semua Perangkat Daerah"] + list(dfRUPPP['nama_satker'].unique())
opd = st.selectbox("Pilih Perangkat Daerah :", opd_options, key='itkp_profil')

### Query RUP
# Menyiapkan query SQL untuk data RUP
RUPPP_umumkan_sql = "SELECT * FROM dfRUPPP WHERE status_umumkan_rup = 'Terumumkan' AND status_aktif_rup = 'TRUE' AND metode_pengadaan <> '0'"
RUPPS_umumkan_sql = """
    SELECT nama_satker, kd_rup, nama_paket, pagu, tipe_swakelola, volume_pekerjaan, uraian_pekerjaan, 
    tgl_pengumuman_paket, tgl_awal_pelaksanaan_kontrak, nama_ppk, status_umumkan_rup
    FROM dfRUPPS
    WHERE status_umumkan_rup = 'Terumumkan'
"""
RUPSA_umumkan_sql = "SELECT * FROM dfRUPSA WHERE 1=1"

# Query untuk data SPSE Tender
SPSETenderPengumuman_sql = "SELECT kd_tender, pagu, hps FROM dfSPSE_TenderPengumuman WHERE status_tender = 'Selesai'"
RUPPP_umumkan_etendering_sql = "SELECT pagu FROM df_RUPPP_umumkan WHERE metode_pengadaan IN ('Tender', 'Tender Cepat', 'Seleksi')"

# Query untuk data SPSE Non-Tender
SPSENonTenderPengumuman_sql = "SELECT pagu, hps FROM dfSPSE_NonTenderPengumuman WHERE status_nontender = 'Selesai'"
RUPPP_umumkan_nonetendering_sql = "SELECT pagu FROM df_RUPPP_umumkan WHERE metode_pengadaan IN ('Pengadaan Langsung', 'Penunjukan Langsung')"

# Query untuk data kontrak dan e-purchasing
SPSETenderKontrak_sql = "SELECT kd_tender FROM dfSPSE_TenderEkontrak WHERE 1=1"
ECAT_sql = "SELECT * FROM dfEcat WHERE 1=1"
ECATSelesai_sql = "SELECT * FROM dfEcat WHERE paket_status_str = 'Paket Selesai'"
BELA_sql = "SELECT nama_satker, valuasi FROM dfBela_TokoDaringRealisasi WHERE status_verif = 'verified' AND status_konfirmasi_ppmse = 'selesai'"

# Filter berdasarkan OPD yang dipilih
if opd != "Semua Perangkat Daerah":
    filter_condition = f" AND nama_satker = '{opd}'"
    RUPPP_umumkan_sql += filter_condition
    RUPPS_umumkan_sql += filter_condition
    RUPSA_umumkan_sql += filter_condition
    SPSETenderPengumuman_sql += filter_condition
    RUPPP_umumkan_etendering_sql += filter_condition
    SPSENonTenderPengumuman_sql += filter_condition
    RUPPP_umumkan_nonetendering_sql += filter_condition
    SPSETenderKontrak_sql += filter_condition
    ECAT_sql += filter_condition
    ECATSelesai_sql += filter_condition
    BELA_sql += filter_condition

# Eksekusi query
df_RUPPP_umumkan = con.execute(RUPPP_umumkan_sql).df()
df_RUPPS_umumkan = con.execute(RUPPS_umumkan_sql).df()
df_RUPSA_umumkan = con.execute(RUPSA_umumkan_sql).df()
df_SPSETenderPengumuman = con.execute(SPSETenderPengumuman_sql).df()
df_RUPPP_umumkan_etendering = con.execute(RUPPP_umumkan_etendering_sql).df()
df_SPSENonTenderPengumuman = con.execute(SPSENonTenderPengumuman_sql).df()
df_RUPPP_umumkan_nonetendering = con.execute(RUPPP_umumkan_nonetendering_sql).df()
df_SPSETenderKontrak = con.execute(SPSETenderKontrak_sql).df()
df_ECATOK = con.execute(ECAT_sql).df()
df_ECATSelesai = con.execute(ECATSelesai_sql).df()
df_BELAOK = con.execute(BELA_sql).df()

try:
    ## Prediksi ITKP RUP
    belanja_pengadaan = df_RUPSA_umumkan['belanja_pengadaan'].sum()
    nilai_total_rup = df_RUPPP_umumkan['pagu'].sum() + df_RUPPS_umumkan['pagu'].sum()
    persen_capaian_rup = nilai_total_rup / belanja_pengadaan
    
    # Hitung prediksi ITKP berdasarkan persentase capaian
    prediksi_itkp_rup = 0
    if persen_capaian_rup > 1:
        prediksi_itkp_rup = (2 - persen_capaian_rup) * 10
    elif persen_capaian_rup > 0.5:
        prediksi_itkp_rup = persen_capaian_rup * 10

    # Tampilkan metrik dalam 4 kolom
    st.subheader("**RENCANA UMUM PENGADAAN**")
    cols = st.columns(4)
    metrik_data = [
        ("BELANJA PENGADAAN (MILYAR)", "{:,.2f}".format(belanja_pengadaan / 1e9)),
        ("NILAI RUP (MILYAR)", "{:,.2f}".format(nilai_total_rup / 1e9)),
        ("PERSENTASE", "{:.2%}".format(persen_capaian_rup)),
        ("NILAI PREDIKSI (DARI 10)", "{:,}".format(round(prediksi_itkp_rup, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP RUP: {e}")

try:
    ## Prediksi ITKP E-Tendering
    nilai_etendering_rup = df_RUPPP_umumkan_etendering['pagu'].sum()
    nilai_etendering_spse = df_SPSETenderPengumuman['pagu'].sum()
    persen_capaian_etendering = nilai_etendering_spse / nilai_etendering_rup
    
    # Hitung prediksi ITKP E-Tendering
    prediksi_itkp_etendering = 0
    if persen_capaian_etendering > 1:
        prediksi_itkp_etendering = (2 - persen_capaian_etendering) * 5
    elif persen_capaian_etendering > 0.5:
        prediksi_itkp_etendering = persen_capaian_etendering * 5

    # Tampilkan metrik dalam 4 kolom
    st.subheader("**E-TENDERING**")
    cols = st.columns(4)
    metrik_data = [
        ("NILAI RUP E-TENDERING (MILYAR)", "{:,.2f}".format(nilai_etendering_rup / 1e9)),
        ("E-TENDERING SELESAI (MILYAR)", "{:,.2f}".format(nilai_etendering_spse / 1e9)),
        ("PERSENTASE", "{:.2%}".format(persen_capaian_etendering)),
        ("NILAI PREDIKSI (DARI 5)", "{:,}".format(round(prediksi_itkp_etendering, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP E-Tendering: {e}")

try:
    ## Prediksi ITKP Non E-Tendering
    nilai_nonetendering_rup = df_RUPPP_umumkan_nonetendering['pagu'].sum()
    nilai_nonetendering_spse = df_SPSENonTenderPengumuman['pagu'].sum()
    persen_capaian_nonetendering = nilai_nonetendering_spse / nilai_nonetendering_rup
    
    # Hitung prediksi ITKP Non E-Tendering
    prediksi_itkp_nonetendering = 0
    if persen_capaian_nonetendering > 1:
        prediksi_itkp_nonetendering = (2 - persen_capaian_nonetendering) * 5
    elif persen_capaian_nonetendering > 0.5:
        prediksi_itkp_nonetendering = persen_capaian_nonetendering * 5

    # Tampilkan metrik dalam 4 kolom
    st.subheader("**NON E-TENDERING**")
    cols = st.columns(4)
    metrik_data = [
        ("NILAI RUP NON E-TENDERING (MILYAR)", "{:,.2f}".format(nilai_nonetendering_rup / 1e9)),
        ("NON E-TENDERING SELESAI (MILYAR)", "{:,.2f}".format(nilai_nonetendering_spse / 1e9)),
        ("PERSENTASE", "{:.2%}".format(persen_capaian_nonetendering)),
        ("NILAI PREDIKSI (DARI 5)", "{:,}".format(round(prediksi_itkp_nonetendering, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP Non E-Tendering: {e}")

try:
    ## Prediksi ITKP E-KONTRAK
    jumlah_tender_selesai = df_SPSETenderPengumuman['kd_tender'].count()
    jumlah_tender_kontrak = df_SPSETenderKontrak['kd_tender'].count()
    persen_capaian_ekontrak = jumlah_tender_kontrak / jumlah_tender_selesai
    
    # Hitung prediksi ITKP E-Kontrak
    prediksi_itkp_ekontrak = 0
    if persen_capaian_ekontrak > 1:
        prediksi_itkp_ekontrak = (2 - persen_capaian_ekontrak) * 5
    elif persen_capaian_ekontrak > 0.2:
        prediksi_itkp_ekontrak = persen_capaian_ekontrak * 5

    # Tampilkan metrik dalam 4 kolom
    st.subheader("**E-KONTRAK**")
    cols = st.columns(4)
    metrik_data = [
        ("JUMLAH PAKET TENDER SELESAI", "{:,}".format(jumlah_tender_selesai)),
        ("JUMLAH PAKET TENDER BERKONTRAK", "{:,}".format(jumlah_tender_kontrak)),
        ("PERSENTASE", "{:.2%}".format(persen_capaian_ekontrak)),
        ("NILAI PREDIKSI (DARI 5)", "{:,}".format(round(prediksi_itkp_ekontrak, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP E-Kontrak: {e}")

try:
    # Prediksi ITKP E-Katalog
    jumlah_trx_ekatalog = df_ECATOK['kd_paket'].nunique()
    jumlah_trx_ekatalog_selesai = df_ECATSelesai['kd_paket'].nunique()
    persen_capaian_ekatalog = jumlah_trx_ekatalog_selesai / jumlah_trx_ekatalog
    
    # Hitung prediksi ITKP E-Katalog
    prediksi_itkp_ekatalog = 0
    if persen_capaian_ekatalog > 1:
        prediksi_itkp_ekatalog = (1 - (persen_capaian_ekatalog - 1)) * 4
    elif persen_capaian_ekatalog > 0.5:
        prediksi_itkp_ekatalog = persen_capaian_ekatalog * 4

    # Tampilkan metrik dalam 4 kolom
    st.subheader("**E-KATALOG**")
    cols = st.columns(4)
    metrik_data = [
        ("JUMLAH TRANSAKSI E-KATALOG", "{:,}".format(jumlah_trx_ekatalog)),
        ("JUMLAH TRANSAKSI SELESAI", "{:,}".format(jumlah_trx_ekatalog_selesai)),
        ("PERSENTASE", "{:.2%}".format(persen_capaian_ekatalog)),
        ("NILAI PREDIKSI (DARI 4)", "{:,}".format(round(prediksi_itkp_ekatalog, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP E-Katalog: {e}")

try:
    # Prediksi ITKP Toko Daring
    jumlah_trx_bela = df_BELAOK['valuasi'].count()
    nilai_trx_bela = df_BELAOK['valuasi'].sum()
    prediksi_itkp_bela = 1 if jumlah_trx_bela >= 1 else 0

    # Tampilkan metrik dalam 3 kolom
    st.subheader("**TOKO DARING**")
    cols = st.columns(3)
    metrik_data = [
        ("JUMLAH TRANSAKSI TOKO DARING", "{:,}".format(jumlah_trx_bela)),
        ("NILAI TRANSAKSI TOKO DARING", "{:,.2f}".format(nilai_trx_bela)),
        ("NILAI PREDIKSI (DARI 1)", "{:,}".format(round(prediksi_itkp_bela, 2)))
    ]
    
    for i, (label, value) in enumerate(metrik_data):
        cols[i].metric(label=label, value=value)
        
except Exception as e:
    st.error(f"Gagal mengolah data ITKP Toko Daring: {e}")


style_metric_cards(background_color="#000", border_left_color="#D3D3D3")