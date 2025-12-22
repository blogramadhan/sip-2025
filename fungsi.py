# Library Utama
import streamlit as st
import pandas as pd
import io
# Library Currency
from babel.numbers import format_currency
# Import Cache Manager
from cache_manager import get_cache_manager, cached_read_parquet, get_duckdb_pool

# Fungsi untuk membaca dan mengunduh dataframe dengan Advanced Caching
@st.cache_data(ttl=21600, show_spinner=False)
def read_df(url, format='parquet'):
    """Load DataFrame dengan basic Streamlit caching"""
    return pd.read_parquet(url) if format=='parquet' else pd.read_excel(url)

@st.cache_data(ttl=21600, show_spinner=False)
def read_df_duckdb(url, format='parquet'):
    """
    Load DataFrame menggunakan DuckDB dengan multi-layer caching

    Fitur:
    - Memory cache layer untuk akses ultra-cepat
    - Persistent disk cache dengan DuckDB
    - Automatic cache invalidation setelah 6 jam
    - Compressed parquet storage untuk efisiensi
    """
    try:
        # Try cache first
        if format == 'parquet':
            return cached_read_parquet(url)
        else:
            # For Excel, use DuckDB direct
            con = get_duckdb_pool().get_connection()
            df = con.execute(f"SELECT * FROM read_xlsx('{url}')").df()
            get_duckdb_pool().return_connection(con)

            # Cache hasil
            cache_mgr = get_cache_manager()
            cache_mgr.set_cached_data(url, df, {'format': 'xlsx'})

            return df
    except Exception as e:
        st.error(f"Error loading {url}: {str(e)}")
        # Fallback to pandas jika DuckDB gagal
        return pd.read_parquet(url) if format=='parquet' else pd.read_excel(url)

def execute_cached_query(query, dataframes_dict, cache_key=None):
    """
    Execute DuckDB query dengan intelligent caching

    Args:
        query: SQL query string
        dataframes_dict: Dictionary of {table_name: dataframe}
        cache_key: Optional cache key untuk hasil query

    Returns:
        Query result DataFrame
    """
    con = get_duckdb_pool().get_connection()

    try:
        # Register all dataframes as tables
        for table_name, df in dataframes_dict.items():
            con.register(table_name, df)

        # Check cache jika ada cache_key
        if cache_key:
            cache_mgr = get_cache_manager()
            cached_result = cache_mgr.get_cached_data(cache_key)
            if cached_result is not None:
                return cached_result

        # Execute query
        result = con.execute(query).df()

        # Cache result
        if cache_key:
            cache_mgr.set_cached_data(cache_key, result)

        return result

    finally:
        get_duckdb_pool().return_connection(con)

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
    # Menggunakan st.logo untuk support collapse otomatis
    # Gunakan URL untuk logo utama dan path lokal untuk icon
    st.logo(
        "https://storage.googleapis.com/bukanamel/img/sip-spse-new.png",
        icon_image="public/sip-spse-icon.png"
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
