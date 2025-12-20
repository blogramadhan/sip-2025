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

# Fungsi untuk memuat custom CSS
def load_css():
    # Load main CSS
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Load components CSS
    with open('style_components.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fungsi untuk membuat logo
def logo():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <img class="brand-full" src="https://storage.googleapis.com/bukanamel/img/sip-spse-new.png" alt="SIP Logo">
            <img class="brand-icon" src="https://storage.googleapis.com/bukanamel/img/sip-spse-icon.png" alt="SIP Icon">
        </div>
        """,
        unsafe_allow_html=True,
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

# Fungsi untuk mendapatkan konfigurasi menu navigasi sidebar
def get_pages():
    beranda = [
        st.Page("beranda.py", title="Beranda", icon="🏠", default=True),
    ]

    rencana_pengadaan = [
        st.Page("src/rencana/rup.py", title="RUP", icon="📋"),
    ]

    proses_pengadaan = [
        st.Page("src/proses/tender.py", title="Tender", icon="⚖️"),
        st.Page("src/proses/nontender.py", title="Non Tender", icon="📝"),
        st.Page("src/proses/pencatatan.py", title="Pencatatan", icon="✍️"),
        st.Page("src/proses/ekatalog.py", title="E-Katalog", icon="📚"),
        st.Page("src/proses/ekatalogv6.py", title="E-Katalog v6", icon="📖"),
        st.Page("src/proses/tokodaring.py", title="Toko Daring", icon="🛒"),
        st.Page("src/proses/pesertatender.py", title="Peserta Tender", icon="👥"),
    ]

    monitoring_pengadaan = [
        st.Page("src/monitoring/itkp.py", title="ITKP", icon="📊"),
        st.Page("src/monitoring/jenisbelanja.py", title="Jenis Belanja", icon="💰"),
        st.Page("src/monitoring/nilaisikap.py", title="Nilai SIKAP", icon="📈"),
    ]

    return {
        "🏠 Beranda": beranda,
        "📋 Rencana": rencana_pengadaan,
        "⚖️ Proses": proses_pengadaan,
        "📊 Monitoring": monitoring_pengadaan,
    }
