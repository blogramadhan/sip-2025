# 🎨 Custom CSS untuk SIP 2025

## Ringkasan

Custom CSS ini memberikan tampilan modern, bersih, dan menarik untuk aplikasi Streamlit dengan tema dark.

### ✨ Fitur Utama

- **Tema Dark Modern**: Background gelap yang nyaman di mata
- **Animasi Halus**: Transisi smooth pada semua interaksi
- **Responsive**: Otomatis menyesuaikan di mobile
- **Clean Design**: Desain minimal namun elegan

---

## 📦 File-file CSS

```
SIP-2025/
├── style.css                # CSS utama (wajib)
├── style_components.css     # CSS komponen tambahan (opsional)
└── .streamlit/
    └── config.toml          # Konfigurasi tema
```

---

## 🚀 Instalasi

CSS sudah otomatis aktif! Tidak perlu setup tambahan.

Fungsi `load_css()` di [fungsi.py](fungsi.py:24-31) akan memuat CSS secara otomatis saat aplikasi berjalan.

---

## 🎨 Warna Tema

### Palette Warna

| Warna | Hex | Digunakan Untuk |
|-------|-----|-----------------|
| **Primary** | `#2563eb` | Buttons, links, active states |
| **Accent** | `#8b5cf6` | Highlights, gradients |
| **Success** | `#10b981` | Download buttons, positive |
| **Background** | `#0f172a` | Main background |
| **Card** | `#1e293b` | Cards, containers |

### Mengubah Warna

Edit di [style.css](style.css:11-28):

```css
:root {
    --primary: #2563eb;        /* Warna utama */
    --accent: #8b5cf6;         /* Warna aksen */
    --success: #10b981;        /* Warna sukses */
}
```

---

## 💻 Komponen yang Ter-style

### 1. Metric Cards
```python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Produk", "1,234")
col2.metric("Penyedia", "567")
col3.metric("Transaksi", "890")
col4.metric("Nilai", "Rp 12M")
```

**Hasil:**
- Border kiri berwarna berbeda (biru, ungu, cyan, hijau)
- Hover effect dengan lift animation
- Typography yang jelas

### 2. Tabs
```python
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
```

**Hasil:**
- Pill-style modern
- Active state dengan gradient
- Smooth transitions

### 3. Buttons
```python
st.button("Submit")
st.download_button("Download", data, "file.xlsx")
```

**Hasil:**
- Button: Gradient biru-ungu
- Download: Gradient hijau
- Hover lift effect

### 4. Radio Buttons
```python
st.radio("Pilih", ["Option 1", "Option 2", "Option 3"])
```

**Hasil:**
- Card-style options
- Gradient pada selected
- Hover effects

### 5. Containers
```python
with st.container(border=True):
    st.write("Content")
```

**Hasil:**
- Background card
- Border dan shadow
- Rounded corners

---

## 🎯 Tips Penggunaan

### Layout yang Baik

```python
# Header
st.title("Dashboard E-Katalog")
st.divider()

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Label", "Value")
# ...

st.divider()

# Tabs untuk konten
tab1, tab2 = st.tabs(["📊 Charts", "📋 Data"])
with tab1:
    with st.container(border=True):
        st.subheader("Grafik")
        # Chart di sini
```

### Filter Section

```python
col1, col2, col3 = st.columns(3)
with col1:
    st.radio("Jenis", ["Semua", "Lokal", "Nasional"])
with col2:
    st.radio("Sumber", ["Semua", "APBD", "BLUD"])
with col3:
    st.selectbox("Tahun", [2025, 2024, 2023])
```

---

## 📱 Responsive Design

CSS otomatis menyesuaikan untuk layar kecil (< 768px):

- Padding lebih kecil
- Font size lebih kecil
- Metric cards dioptimasi

---

## 🎬 Animasi

### Fade In
- Main content otomatis fade in saat load
- Durasi: 0.4s

### Hover Effects
- Metric cards: translateY(-3px)
- Buttons: translateY(-2px)
- Navigation: translateX(4px)

### Transitions
- Semua: 0.2s ease

---

## 🔧 Customisasi Lebih Lanjut

### Contoh 1: Ubah Warna Primary Menjadi Hijau

```css
:root {
    --primary: #10b981;
    --primary-light: #34d399;
}
```

### Contoh 2: Ubah Border Radius

```css
[data-testid="stMetric"] {
    border-radius: 16px;  /* default: 12px */
}
```

### Contoh 3: Ubah Durasi Animasi

```css
[data-testid="stMetric"] {
    transition: all 0.3s;  /* default: 0.2s */
}
```

---

## ❓ FAQ

**Q: CSS tidak muncul?**
A: Pastikan `load_css()` dipanggil di [streamlit_app.py](streamlit_app.py:15)

**Q: Cara menghilangkan animasi?**
A: Hapus atau comment animasi di [style.css](style.css:428-441)

**Q: Bisa pakai tema light?**
A: Saat ini hanya optimized untuk dark theme

**Q: Cara update CSS tanpa restart?**
A: Tekan `R` di browser atau `Ctrl+R` untuk reload

---

## 🌟 Preview Komponen

| Komponen | Fitur |
|----------|-------|
| **Sidebar** | Gradient background, active state |
| **Metrics** | Color-coded borders, hover lift |
| **Buttons** | Gradient, shadow on hover |
| **Tabs** | Pill-style, smooth transitions |
| **Radio** | Card-style, gradient selected |
| **Tables** | Dark theme, hover rows |
| **Charts** | Container dengan border |

---

## 📞 Support

File CSS dibuat sederhana agar mudah dikustomisasi sesuai kebutuhan.

**File utama:** [style.css](style.css)
**File tambahan:** [style_components.css](style_components.css)

---

**Versi:** 2.0 - Simple & Modern
**Update:** Desember 2025
**Untuk:** Sistem Informasi Pelaporan Pengadaan Barang dan Jasa
