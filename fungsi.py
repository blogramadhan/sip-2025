# Library Utama
import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
import openpyxl
import io
import xlsxwriter
# Library Currency
from babel.numbers import format_currency
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo

# Fungsi untuk membaca dan mengunduh dataframe
@st.cache_data(ttl=21600)
def read_df(url, format='parquet'):
    return pd.read_parquet(url) if format=='parquet' else pd.read_excel(url)

@st.cache_data(ttl=21600) 
def read_df_duckdb(url, format='parquet'):
    return duckdb.read_parquet(url).df() if format=='parquet' else duckdb.read_excel(url).df()

def download_excel(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, sheet_name='Sheet1', engine='xlsxwriter')
    return buffer.getvalue()

# Fungsi untuk membuat logo
def logo():
    st.logo(image="https://storage.googleapis.com/bukanamel/img/instansi-logo.png", icon_image="https://storage.googleapis.com/bukanamel/img/instansi-logo.png", size="large")

# Fungsi page config
def page_config():
    return st.set_page_config(
            page_title="Sistem Informasi Pelaporan Pengadaan Barang dan Jasa",
            page_icon=":bar_chart:",
            layout="wide",
            initial_sidebar_state="expanded",
        )

# Fungsi region config
def region_config():
    return {
        "PROV. KALBAR": {"folder": "prov", "RUP": "D197", "LPSE": "97"},
        "KOTA PONTIANAK": {"folder": "ptk", "RUP": "D199", "LPSE": "62"},
        "KAB. KUBU RAYA": {"folder": "kkr", "RUP": "D202", "LPSE": "188"},
        "KAB. MEMPAWAH": {"folder": "mpw", "RUP": "D552", "LPSE": "118"},
        "KOTA SINGKAWANG": {"folder": "skw", "RUP": "D200", "LPSE": "132"},
        "KAB. BENGKAYANG": {"folder": "bky", "RUP": "D206", "LPSE": "444"},
        "KAB. LANDAK": {"folder": "ldk", "RUP": "D205", "LPSE": "496"},
        "KAB. SANGGAU": {"folder": "sgu", "RUP": "D204", "LPSE": "298"},
        "KAB. SEKADAU": {"folder": "skd", "RUP": "D198", "LPSE": "175"},
        "KAB. MELAWI": {"folder": "mlw", "RUP": "D210", "LPSE": "540"},
        "KAB. SINTANG": {"folder": "stg", "RUP": "D211", "LPSE": "345"},
        "KAB. KAPUAS HULU": {"folder": "kph", "RUP": "D209", "LPSE": "488"},
        "KAB. KETAPANG": {"folder": "ktp", "RUP": "D201", "LPSE": "110"},
        "KAB. TANGGERANG": {"folder": "tgr", "RUP": "D50", "LPSE": "333"},
        "KAB. KATINGAN": {"folder": "ktg", "RUP": "D236", "LPSE": "438"}
    }

# Fungsi untuk membuat menu sidebar
def sidebar_menu():
    pages = {
        "SIRUP": [
            st.Page("SIRUP.py", title="SIRUP"),
        ],
    }
    return st.navigation(pages)

# Fungsi Get Rup Data
def get_rup_data(queries, con):
    """Mengambil dan memproses data RUP"""
    try:
        # Ambil data dari setiap query
        dfs = {}
        for name, query in queries.items():
            result = con.execute(query).df()
            if result.empty:
                st.warning(f"Query {name} tidak menghasilkan data")
                return pd.DataFrame()
            dfs[name] = result

        # Gabungkan data
        keys = list(queries.keys())
        result = dfs[keys[0]]
        for key in keys[1:]:
            result = pd.merge(result, dfs[key], how='left', on='NAMA_SATKER')

        # Hitung total dan persentase
        return (result
            .assign(
                TOTAL_RUP=lambda x: x.RUP_PENYEDIA.fillna(0) + x.RUP_SWAKELOLA.fillna(0),
                SELISIH=lambda x: x.STRUKTUR_ANGGARAN.fillna(0) - x.TOTAL_RUP,
                PERSEN=lambda x: round((x.TOTAL_RUP / x.STRUKTUR_ANGGARAN * 100).fillna(0), 2)
            )
            .fillna(0))

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return pd.DataFrame()

def display_rup_data(data, title, pilih, tahun, suffix=""):
    """Menampilkan data RUP"""
    st.title(title)
    st.header(f"{pilih} TAHUN {tahun}")
    
    try:
        # Tombol download
        st.download_button(
            label=f"📥 Download  % Input RUP{suffix}",
            data=download_excel(data),
            file_name=f"TabelPersenInputRUP{suffix}_{pilih}_{tahun}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Tampilkan tabel
        st.dataframe(
            data,
            column_config={
                "STRUKTUR_ANGGARAN": "STRUKTUR ANGGARAN",
                "RUP_PENYEDIA": "RUP PAKET PENYEDIA", 
                "RUP_SWAKELOLA": "RUP PAKET SWAKELOLA",
                "TOTAL_RUP": "TOTAL RUP",
                "SELISIH": "SELISIH",
                "PERSEN": "PERSENTASE"
            },
            hide_index=True,
            use_container_width=True,
            height=1000
        )

    except Exception as e:
        st.error(f"Error: {e}")