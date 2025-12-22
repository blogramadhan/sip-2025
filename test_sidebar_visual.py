#!/usr/bin/env python3
"""
Visual Test - Sidebar & Logo
Jalankan dengan: streamlit run test_sidebar_visual.py
"""
import streamlit as st
from fungsi import load_css, logo

# Page config
st.set_page_config(
    page_title="Sidebar & Logo Test",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS
load_css()

# Display logo
logo()

# Sidebar content
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📋 Test Navigation")
    st.page_link("test_sidebar_visual.py", label="Home", icon="🏠")
    st.markdown("**Test Items**")
    if st.button("Test 1", use_container_width=True):
        st.toast("Test 1 clicked!")
    if st.button("Test 2", use_container_width=True):
        st.toast("Test 2 clicked!")
    if st.button("Test 3", use_container_width=True):
        st.toast("Test 3 clicked!")
    st.markdown("---")

# Main content
st.title("🎨 Sidebar & Logo Visual Test")
st.caption("Test halaman untuk memverifikasi sidebar dan logo")

st.divider()

# Instructions
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("✅ Test Checklist - Logo")
        st.markdown("""
        **Sidebar Expanded (288px):**
        1. Logo utama muncul (horizontal)
        2. Width: 100% dari sidebar (~272px efektif)
        3. Height: auto, 120-180px range (2X BESAR!)
        4. Tidak terdistorsi (rasio 2.25:1)
        5. Ukuran SANGAT BESAR & proporsional
        6. Background putih transparan
        7. Border radius halus
        8. Minimal padding untuk maksimalkan ukuran

        **Sidebar Collapsed (80px):**
        1. Logo utama hilang
        2. Icon muncul (square)
        3. Ukuran 56×56 px
        4. Background putih lebih solid
        5. Centered di sidebar
        """)

with col2:
    with st.container(border=True):
        st.subheader("✅ Test Checklist - Sidebar")
        st.markdown("""
        **Functionality:**
        1. Collapse button berfungsi
        2. Hover effect pada button
        3. Smooth transition (0.3s)
        4. Sidebar tidak hilang
        5. Width: 288px → 80px

        **Navigation:**
        1. Menu items visible (expanded)
        2. Icon-only mode (collapsed)
        3. Tooltip muncul (collapsed)
        4. Active state berfungsi
        5. Hover effect berfungsi
        """)

st.divider()

# Visual indicators
st.subheader("📊 Current State")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric(
        label="Sidebar State",
        value="Check DevTools",
        help="Inspect aria-expanded attribute"
    )

with col_b:
    st.metric(
        label="Logo Files",
        value="✅ Accessible",
        help="Verified by test_logo.py"
    )

with col_c:
    st.metric(
        label="CSS Loaded",
        value="✅ Active",
        help="Custom CSS from style.css"
    )

st.divider()

# Logo file info
with st.expander("📁 Logo File Information"):
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "public", "sip-spse.png")
    icon_path = os.path.join(base_dir, "public", "sip-spse-icon.png")

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown("**Main Logo**")
        st.code(f"""
Path: {logo_path}
Exists: {os.path.exists(logo_path)}
Size: {os.path.getsize(logo_path) if os.path.exists(logo_path) else 'N/A'} bytes
Dimensions: 1350 × 600 px
Aspect Ratio: 2.25:1
Display: 100% width (~250px), height 80-120px
        """)

    with col_info2:
        st.markdown("**Icon Logo**")
        st.code(f"""
Path: {icon_path}
Exists: {os.path.exists(icon_path)}
Size: {os.path.getsize(icon_path) if os.path.exists(icon_path) else 'N/A'} bytes
Dimensions: 800 × 800 px
Aspect Ratio: 1:1
        """)

st.divider()

# Testing instructions
with st.container(border=True):
    st.subheader("🧪 How to Test")
    st.markdown("""
    ### Step-by-step Testing:

    1. **Initial State (Expanded)**
       - Logo utama harus terlihat di sidebar atas
       - Ukuran harus proporsional (tidak gepeng/tinggi)
       - Background putih transparan dengan border radius

    2. **Click Collapse Button**
       - Button ada di pojok kiri atas sidebar
       - Hover harus menampilkan highlight biru
       - Click untuk collapse

    3. **Collapsed State**
       - Sidebar menyusut jadi ~80px
       - Logo utama hilang
       - Icon square muncul (56×56px)
       - Menu items hanya tampil icon

    4. **Click Expand Button**
       - Button sekarang di luar sidebar (fixed position)
       - Click untuk expand kembali
       - Logo utama muncul lagi

    5. **Smooth Transition**
       - Animasi harus smooth (0.3 detik)
       - Tidak ada glitch atau jumping
       - Logo swap smooth

    ### Browser DevTools:

    Open Chrome DevTools (F12) dan inspect:
    ```
    [data-testid="stSidebar"]
    ```

    Check attributes:
    - `aria-expanded="true"` → Expanded state
    - `aria-expanded="false"` → Collapsed state

    Check computed styles:
    - width: `288px` (expanded) atau `80px` (collapsed)
    - Logo img: check display, visibility, opacity
    """)

st.divider()

# Debug info
with st.expander("🔧 Debug Information"):
    st.markdown("**CSS Selectors Used:**")
    st.code("""
    /* Sidebar States */
    [data-testid="stSidebar"]                          → Base
    [data-testid="stSidebar"][aria-expanded="false"]   → Collapsed
    [data-testid="stSidebar"].collapsed                → Collapsed (alt)

    /* Logo Display */
    [data-testid="stLogo"] img:not([src*="icon"])      → Main logo
    [data-testid="stLogo"] img[src*="icon"]            → Icon logo

    /* Collapsed Icon Override */
    [aria-expanded="false"] [data-testid="stLogo"] img[src*="icon"]
    """, language="css")

    st.markdown("**Expected Behavior:**")
    st.code("""
    Expanded:
    - Main logo: display: block, height: 70px, width: auto
    - Icon logo: display: none, opacity: 0

    Collapsed:
    - Main logo: display: none, opacity: 0
    - Icon logo: display: block, 56×56px, opacity: 1
    """)

st.success("✨ Visual test page loaded successfully! Sekarang test collapse/expand sidebar.")
