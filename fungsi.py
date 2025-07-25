# Library Utama
import streamlit as st
import pandas as pd
import duckdb
import io
# Library Currency
from babel.numbers import format_currency

# Fungsi untuk membaca dan mengunduh dataframe
@st.cache_data(ttl=21600)
def read_df(url, format='parquet'):
    return pd.read_parquet(url) if format=='parquet' else pd.read_excel(url)

@st.cache_data(ttl=21600) 
def read_df_duckdb(url, format='parquet'):
    return duckdb.read_parquet(url).df() if format=='parquet' else duckdb.read_xlsx(url).df()

def download_excel(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, sheet_name='Sheet1')
    return buffer.getvalue()

# Fungsi untuk membuat logo
def logo():
    st.logo(image="https://storage.googleapis.com/bukanamel/img/sip-spse-new.png", icon_image="https://storage.googleapis.com/bukanamel/img/sip-spse-icon.png", size="large")

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