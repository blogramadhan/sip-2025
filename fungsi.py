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

# Fungsi pengganti style_metric_cards yang tidak bergantung pada streamlit_extras
def style_metric_cards(background_color="#f8fafc", border_left_color="#2f6ea3", border_color="#e2e8f0", border_size_px=1, border_radius_px=10):
    """
    Fungsi pengganti untuk style_metric_cards dari streamlit_extras
    Karena ada konflik dependency dengan streamlit_theme
    """
    # Styling sudah dihandle oleh CSS global di style.css dan style_components.css
    # Fungsi ini dibuat agar tidak perlu mengubah semua file yang sudah menggunakannya
    pass

# Fungsi untuk membuat logo
def logo():
    """
    Menggunakan st.logo untuk support collapse otomatis
    Logo utama (1350x600): Tampil saat sidebar expanded
    Logo icon (800x800): Tampil saat sidebar collapsed
    """
    import os
    import sys
    import base64

    # Coba berbagai cara untuk mendapatkan path yang benar
    # 1. Dari file ini
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Fallback ke current working directory jika perlu
    if not os.path.exists(os.path.join(base_dir, "public")):
        base_dir = os.getcwd()

    # 3. Fallback ke parent directory dari streamlit main script
    if not os.path.exists(os.path.join(base_dir, "public")) and hasattr(sys.modules['__main__'], '__file__'):
        base_dir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

    logo_path = os.path.join(base_dir, "public", "sip-spse.png")
    icon_path = os.path.join(base_dir, "public", "sip-spse-icon.png")

    # Debug: Print paths
    # st.sidebar.caption(f"Base dir: {base_dir}")

    # Verifikasi file exists sebelum digunakan
    if not os.path.exists(logo_path):
        st.sidebar.warning(f"⚠️ Logo file not found at: {logo_path}")
        st.sidebar.caption("Trying to load logo from expected location...")
        return

    if not os.path.exists(icon_path):
        st.sidebar.warning(f"⚠️ Icon file not found at: {icon_path}")
        st.sidebar.caption("Trying to load icon from expected location...")
        return

    try:
        def _img_to_base64(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("ascii")

        logo_b64 = _img_to_base64(logo_path)
        icon_b64 = _img_to_base64(icon_path)

        # Render HTML agar ukuran & toggle collapsed/expanded bisa dikontrol penuh via CSS.
        with st.sidebar:
            st.markdown(
                f"""
                <div class="sidebar-brand">
                    <img class="brand-full" src="data:image/png;base64,{logo_b64}" alt="SIP SPSE" />
                    <img class="brand-icon" src="data:image/png;base64,{icon_b64}" alt="SIP SPSE Icon" />
                </div>
                """,
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.sidebar.error(f"❌ Error loading logo: {str(e)}")
        st.sidebar.caption(f"Logo path: {logo_path}")
        st.sidebar.caption(f"Icon path: {icon_path}")
        # Fallback: tampilkan image biasa
        try:
            with st.sidebar:
                st.image(logo_path, use_container_width=True)
        except:
            pass

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
