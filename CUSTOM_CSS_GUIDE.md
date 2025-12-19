# 🎨 Panduan Custom CSS - SIP 2025

## 📋 Daftar Isi
1. [Instalasi](#instalasi)
2. [Fitur Utama](#fitur-utama)
3. [Komponen yang Telah Dikustomisasi](#komponen-yang-telah-dikustomisasi)
4. [Penggunaan](#penggunaan)
5. [Customisasi Warna](#customisasi-warna)
6. [Tips & Trik](#tips--trik)

---

## 🚀 Instalasi

Custom CSS sudah otomatis terintegrasi dengan aplikasi. File-file yang terlibat:

```
SIP-2025/
├── style.css                 # CSS utama
├── style_components.css      # CSS komponen tambahan
├── fungsi.py                 # Fungsi load_css()
├── streamlit_app.py          # Load CSS di sini
└── .streamlit/
    └── config.toml           # Konfigurasi tema
```

CSS akan otomatis dimuat saat aplikasi dijalankan melalui fungsi `load_css()`.

---

## ✨ Fitur Utama

### 1. **Tema Dark Modern**
- Background gradasi gelap yang nyaman di mata
- Kontras tinggi untuk readability
- Warna aksen yang vibrant

### 2. **Animasi Smooth**
- Fade-in untuk konten utama
- Slide-in untuk sidebar
- Hover effects pada semua interactive elements
- Smooth transitions (0.3s ease)

### 3. **Responsive Design**
- Breakpoint mobile: 768px
- Padding & spacing menyesuaikan
- Font size responsif

### 4. **Glass Morphism Effects**
- Backdrop blur pada beberapa komponen
- Semi-transparent backgrounds
- Modern shadow effects

---

## 🎯 Komponen yang Telah Dikustomisasi

### **Sidebar**
```css
✓ Gradient background
✓ Hover effects pada navigation items
✓ Active state dengan gradient biru-ungu
✓ Smooth slide-in animation
✓ Select box dengan rounded corners
```

### **Metric Cards**
```css
✓ Gradient background
✓ Lift effect on hover (translateY -5px)
✓ Border kiri berwarna berbeda per card
✓ Shadow effects (md → xl on hover)
✓ Typography modern dengan Poppins font
```

### **Buttons**
```css
✓ Primary: Gradient biru-ungu
✓ Download: Gradient cyan-biru
✓ Hover: Lift effect + shadow lebih besar
✓ Icon otomatis (📥 untuk download)
✓ Ripple effect on click
```

### **Tabs**
```css
✓ Pill-style modern
✓ Background di tab list
✓ Active state dengan gradient
✓ Tab panel dengan border & shadow
✓ Icon otomatis (📊, 💰)
```

### **Radio Buttons**
```css
✓ Background semi-transparent
✓ Hover state pada setiap option
✓ Active state dengan gradient
✓ Rounded corners
✓ Border highlight on hover
```

### **Select Box**
```css
✓ Dark background
✓ Border highlight on hover/focus
✓ Focus ring dengan glow effect
✓ Smooth transitions
```

### **Charts (Plotly)**
```css
✓ Container dengan border & shadow
✓ Rounded corners
✓ Custom tooltip styling
✓ Background card
```

### **Tables (AG Grid)**
```css
✓ Dark theme custom
✓ Header gradient dengan border biru
✓ Hover row dengan scale effect
✓ Numeric cells highlighted
✓ Custom pagination styling
```

### **Containers**
```css
✓ Border & shadow
✓ Rounded corners
✓ Glass morphism effect
✓ Hover effects
```

---

## 💻 Penggunaan

### Contoh 1: Metric Cards Otomatis Ter-style

```python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Jumlah Produk", "1,234")
col2.metric("Jumlah Penyedia", "567")
col3.metric("Jumlah Transaksi", "890")
col4.metric("Nilai Transaksi", "Rp 12,345,678")
```

Hasil: Setiap metric card akan memiliki:
- Border kiri berwarna berbeda (biru, ungu, cyan, hijau)
- Hover effect dengan lift
- Gradient background

### Contoh 2: Download Button

```python
st.download_button(
    label="📥 Unduh Data",
    data=data,
    file_name="data.xlsx"
)
```

Hasil: Button dengan gradient hijau dan icon 📥 otomatis

### Contoh 3: Tabs dengan Icon

```python
tab1, tab2 = st.tabs(["Jumlah Transaksi", "Nilai Transaksi"])
```

Hasil: Icon 📊 dan 💰 otomatis ditambahkan

### Contoh 4: Container dengan Border

```python
with st.container(border=True):
    st.subheader("Berdasarkan Kualifikasi Usaha")
    # konten...
```

Hasil: Container dengan modern card styling

---

## 🎨 Customisasi Warna

Edit file `style.css` pada bagian `:root`:

```css
:root {
    /* Primary Colors - Ubah sesuai kebutuhan */
    --primary-color: #3b82f6;      /* Biru utama */
    --primary-dark: #2563eb;       /* Biru gelap */
    --primary-light: #60a5fa;      /* Biru terang */

    /* Accent Colors */
    --accent-color: #8b5cf6;       /* Ungu */
    --accent-secondary: #06b6d4;   /* Cyan */
    --success-color: #10b981;      /* Hijau */
    --warning-color: #f59e0b;      /* Orange */
    --danger-color: #ef4444;       /* Merah */

    /* Background Colors */
    --bg-primary: #0f172a;         /* Background utama */
    --bg-secondary: #1e293b;       /* Background sekunder */
    --bg-tertiary: #334155;        /* Background tertiary */
}
```

### Preset Warna Alternatif

**Tema Hijau-Tosca:**
```css
--primary-color: #10b981;
--accent-color: #06b6d4;
```

**Tema Ungu-Pink:**
```css
--primary-color: #8b5cf6;
--accent-color: #ec4899;
```

**Tema Orange-Merah:**
```css
--primary-color: #f59e0b;
--accent-color: #ef4444;
```

---

## 💡 Tips & Trik

### 1. **Gunakan Columns untuk Layout**
```python
col1, col2 = st.columns([7, 3])
with col1:
    # Chart/Grafik
with col2:
    # Table/Data
```

### 2. **Container untuk Grouping**
```python
with st.container(border=True):
    st.subheader("Section Title")
    # Konten akan ter-group dengan styling card
```

### 3. **Expander untuk Konten Tersembunyi**
```python
with st.expander("Lihat Detail"):
    # Konten detail
    # Akan memiliki styling modern
```

### 4. **Kombinasi Tabs + Container**
```python
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    with st.container(border=True):
        # Konten tab 1
```

### 5. **Alert Messages**
```python
st.info("Informasi penting")      # Biru
st.success("Berhasil!")           # Hijau
st.warning("Peringatan")          # Orange
st.error("Error terjadi")         # Merah
```

---

## 🎬 Animasi yang Tersedia

### Fade In (otomatis pada main content)
```css
animation: fadeIn 0.5s ease-out;
```

### Slide In (otomatis pada sidebar)
```css
animation: slideIn 0.4s ease-out;
```

### Hover Lift (otomatis pada cards)
```css
transform: translateY(-5px);
```

### Pulse (loading states)
```css
animation: pulse 2s ease-in-out infinite;
```

---

## 📱 Responsive Breakpoints

- **Desktop**: > 768px (default styling)
- **Mobile**: ≤ 768px
  - Reduced padding
  - Smaller font sizes
  - Adjusted button sizes
  - Optimized metric cards

---

## 🔧 Troubleshooting

### CSS Tidak Muncul?
1. Pastikan `load_css()` dipanggil di `streamlit_app.py`
2. Cek apakah file `style.css` dan `style_components.css` ada di root folder
3. Restart aplikasi Streamlit

### Warna Tidak Sesuai?
1. Cek file `.streamlit/config.toml`
2. Pastikan variabel CSS di `:root` sesuai
3. Clear browser cache

### Animasi Terlalu Lambat/Cepat?
Edit durasi di file CSS:
```css
transition: all 0.3s ease; /* Ubah 0.3s sesuai keinginan */
```

---

## 📚 Referensi CSS Classes

### Utility Classes
- `.text-center` - Center alignment
- `.text-gradient` - Gradient text
- `.card-hover` - Hover effect

### Custom Components
- `.custom-card` - Modern card dengan gradient
- `.stat-card` - Dashboard metric card
- `.status-badge` - Badge untuk status
- `.skeleton` - Loading skeleton

---

## 🌟 Best Practices

1. **Konsistensi**: Gunakan komponen Streamlit standar
2. **Performance**: Hindari terlalu banyak animasi
3. **Accessibility**: Pastikan kontras warna cukup
4. **Mobile First**: Test di berbagai ukuran layar
5. **Dark Theme**: Optimized untuk tema gelap

---

## 📞 Support

Jika ada pertanyaan atau masalah:
1. Lihat dokumentasi Streamlit: https://docs.streamlit.io
2. Cek file README_CSS.md untuk informasi tambahan
3. Review kode di style.css dan style_components.css

---

**Versi**: 1.0
**Tanggal**: Desember 2025
**Dibuat untuk**: Sistem Informasi Pelaporan Pengadaan Barang dan Jasa

---

Enjoy your beautiful dashboard! 🎉
