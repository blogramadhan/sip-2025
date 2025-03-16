# Library Utama
import streamlit as st
import polars as pl
import plotly.express as px
import duckdb
import openpyxl
import io
import xlsxwriter
import pandas as pd
from io import BytesIO
# Library Currency
from babel.numbers import format_currency
# Library Streamlit-Extras
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.app_logo import add_logo

# Fungsi untuk membaca dan mengunduh dataframe
@st.cache_data(ttl=21600)
def read_df(url, format='parquet'):
    return pl.read_parquet(url) if format=='parquet' else pl.read_excel(url)

@st.cache_data(ttl=21600) 
def read_df_duckdb(url, format='parquet'):
    return duckdb.read_parquet(url).df() if format=='parquet' else duckdb.read_excel(url).df()

def download_excel(df):
    output = BytesIO()
    # Konversi Polars DataFrame ke Pandas DataFrame jika diperlukan
    if hasattr(df, 'to_pandas'):
        df = df.to_pandas()
    # Tulis ke excel
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    return output.read()

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