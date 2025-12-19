# ====================================
# CONTOH PENGGUNAAN CUSTOM CSS
# File: style_examples.py
# ====================================

import streamlit as st

# Fungsi helper untuk membuat custom HTML components

def custom_metric_card(label, value, icon="📊", color="#3b82f6"):
    """
    Membuat metric card dengan custom styling

    Args:
        label: Label metric
        value: Nilai metric
        icon: Icon emoji
        color: Warna border kiri
    """
    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(51, 65, 85, 0.5);
        border-left: 4px solid {color};
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    " onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 12px 24px rgba(0, 0, 0, 0.4)';"
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 16px rgba(0, 0, 0, 0.3)';">
        <div style="color: #94a3b8; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
            {icon} {label}
        </div>
        <div style="color: #60a5fa; font-size: 2rem; font-weight: 700; font-family: 'Poppins', sans-serif;">
            {value}
        </div>
    </div>
    """
    return html


def custom_header(title, subtitle="", gradient_colors=["#667eea", "#764ba2"]):
    """
    Membuat header dengan gradient text

    Args:
        title: Judul utama
        subtitle: Sub judul (optional)
        gradient_colors: List warna gradient [start, end]
    """
    html = f"""
    <div style="margin: 2rem 0;">
        <h1 style="
            background: linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        ">{title}</h1>
        {f'<p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    return html


def status_badge(text, status_type="info"):
    """
    Membuat status badge

    Args:
        text: Text badge
        status_type: Tipe status (success, warning, danger, info)
    """
    colors = {
        "success": "linear-gradient(135deg, #10b981, #059669)",
        "warning": "linear-gradient(135deg, #f59e0b, #d97706)",
        "danger": "linear-gradient(135deg, #ef4444, #dc2626)",
        "info": "linear-gradient(135deg, #3b82f6, #2563eb)"
    }

    html = f"""
    <span style="
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: {colors.get(status_type, colors['info'])};
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    ">{text}</span>
    """
    return html


def info_card(title, content, icon="ℹ️", color="#3b82f6"):
    """
    Membuat info card dengan icon

    Args:
        title: Judul card
        content: Konten card
        icon: Icon emoji
        color: Warna aksen
    """
    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
        border-left: 4px solid {color};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    ">
        <div style="
            font-size: 1.25rem;
            font-weight: 600;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        ">{icon} {title}</div>
        <div style="color: #cbd5e1; line-height: 1.6;">
            {content}
        </div>
    </div>
    """
    return html


def stat_comparison(label1, value1, label2, value2, icon1="📈", icon2="📉"):
    """
    Membuat perbandingan dua statistik

    Args:
        label1, value1: Label dan nilai pertama
        label2, value2: Label dan nilai kedua
        icon1, icon2: Icon untuk masing-masing
    """
    html = f"""
    <div style="
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    ">
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(51, 65, 85, 0.5);
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon1}</div>
            <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{label1}</div>
            <div style="color: #60a5fa; font-size: 1.75rem; font-weight: 700;">{value1}</div>
        </div>
        <div style="
            background: linear-gradient(135deg, #1e293b, #0f172a);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(51, 65, 85, 0.5);
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon2}</div>
            <div style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 0.5rem;">{label2}</div>
            <div style="color: #8b5cf6; font-size: 1.75rem; font-weight: 700;">{value2}</div>
        </div>
    </div>
    """
    return html


def progress_card(title, percentage, color="#3b82f6"):
    """
    Membuat card dengan progress bar

    Args:
        title: Judul progress
        percentage: Persentase (0-100)
        color: Warna progress bar
    """
    html = f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8));
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(51, 65, 85, 0.5);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            align-items: center;
        ">
            <span style="color: #f1f5f9; font-weight: 600;">{title}</span>
            <span style="color: {color}; font-weight: 700; font-size: 1.25rem;">{percentage}%</span>
        </div>
        <div style="
            background: rgba(51, 65, 85, 0.3);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
        ">
            <div style="
                background: {color};
                height: 100%;
                width: {percentage}%;
                border-radius: 10px;
                transition: width 1s ease;
            "></div>
        </div>
    </div>
    """
    return html


def gradient_divider(height="2px", colors=["#3b82f6", "#8b5cf6"]):
    """
    Membuat divider dengan gradient

    Args:
        height: Tinggi divider
        colors: Warna gradient [start, end]
    """
    html = f"""
    <div style="
        height: {height};
        background: linear-gradient(90deg, {colors[0]}, {colors[1]});
        border-radius: 2px;
        margin: 2rem 0;
        opacity: 0.5;
    "></div>
    """
    return html


# ====================================
# CONTOH PENGGUNAAN
# ====================================

if __name__ == "__main__":
    st.set_page_config(page_title="Contoh Custom CSS", layout="wide")

    # Load CSS
    from fungsi import load_css
    load_css()

    # Header dengan gradient
    st.markdown(custom_header(
        "Dashboard E-Katalog",
        "Sistem Informasi Pelaporan Pengadaan Barang dan Jasa"
    ), unsafe_allow_html=True)

    st.markdown(gradient_divider(), unsafe_allow_html=True)

    # Metric cards custom
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(custom_metric_card(
            "Total Produk", "1,234", "📦", "#3b82f6"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(custom_metric_card(
            "Total Penyedia", "567", "🏢", "#8b5cf6"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(custom_metric_card(
            "Total Transaksi", "890", "📝", "#06b6d4"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(custom_metric_card(
            "Total Nilai", "Rp 12.3M", "💰", "#10b981"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Status badges
    col1, col2 = st.columns([8, 2])
    with col1:
        st.subheader("Status Transaksi")
    with col2:
        st.markdown(
            status_badge("AKTIF", "success") + " " +
            status_badge("2025", "info"),
            unsafe_allow_html=True
        )

    # Info card
    st.markdown(info_card(
        "Informasi Penting",
        "Data transaksi e-katalog ditampilkan berdasarkan filter yang dipilih. Gunakan sidebar untuk memilih daerah dan tahun.",
        "💡",
        "#3b82f6"
    ), unsafe_allow_html=True)

    # Stat comparison
    st.markdown(stat_comparison(
        "Transaksi Bulan Ini",
        "156",
        "Transaksi Bulan Lalu",
        "142",
        "📈",
        "📊"
    ), unsafe_allow_html=True)

    # Progress cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(progress_card(
            "Realisasi Target UKM",
            75,
            "#10b981"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(progress_card(
            "Realisasi Target PDN",
            85,
            "#3b82f6"
        ), unsafe_allow_html=True)

    st.markdown(gradient_divider(height="3px"), unsafe_allow_html=True)

    # Standard Streamlit components (akan ter-style otomatis)
    st.subheader("Standard Streamlit Components")

    tab1, tab2, tab3 = st.tabs(["📊 Charts", "📋 Tables", "⚙️ Controls"])

    with tab1:
        st.write("Charts akan ditampilkan di sini dengan styling otomatis")

    with tab2:
        st.write("Tables akan ditampilkan di sini dengan styling otomatis")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.radio("Pilihan", ["Option 1", "Option 2", "Option 3"])
        with col2:
            st.selectbox("Select", ["Choice 1", "Choice 2", "Choice 3"])
