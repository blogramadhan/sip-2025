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
@st.cache_data(ttl=3600)
def read_df(url, format='parquet'):
    return pd.read_parquet(url) if format=='parquet' else pd.read_excel(url)

@st.cache_data(ttl=3600) 
def read_df_duckdb(url, format='parquet'):
    return duckdb.read_parquet(url).df() if format=='parquet' else duckdb.read_excel(url).df()

def download_excel(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, sheet_name='Sheet1', engine='xlsxwriter')
    return buffer.getvalue()

# Fungsi untuk membuat logo
def logo():
    add_logo("https://storage.googleapis.com/bukanamel/img/instansi-logo.png", height=200)