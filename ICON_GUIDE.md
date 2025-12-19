# 🎨 Icon Guide untuk Tabs

## Icon yang Digunakan di Aplikasi

### Tabs Utama (Main Navigation)

| Icon | Nama Tab | Deskripsi |
|------|----------|-----------|
| 📦 | TRANSAKSI KATALOG | Data transaksi e-katalog utama |
| 🏪 | TRANSAKSI KATALOG (ETALASE) | Data transaksi per etalase |
| 📋 | TABEL NILAI ETALASE | Tabel nilai per etalase |

### Tabs Analisis (Secondary Tabs)

| Icon | Nama Tab | Kapan Digunakan |
|------|----------|-----------------|
| 📊 | Jumlah Transaksi | Menampilkan grafik/data jumlah |
| 💰 | Nilai Transaksi | Menampilkan grafik/data nilai Rupiah |

## Daftar Icon untuk Berbagai Keperluan

### Data & Analytics
- 📊 Chart/Grafik
- 📈 Trend naik
- 📉 Trend turun
- 📋 Tabel/List
- 💰 Nilai/Uang
- 💵 Rupiah
- 💳 Transaksi

### Kategori Bisnis
- 📦 Produk/Katalog
- 🏪 Toko/Etalase
- 🏢 Perusahaan/Penyedia
- 👥 Pelaku Usaha/People
- 🏛️ Instansi/Perangkat Daerah
- 🏭 Manufaktur

### Status & Actions
- ✅ Sukses/Selesai
- ❌ Error/Gagal
- ⚠️ Peringatan
- ℹ️ Informasi
- 📥 Download
- 📤 Upload
- ⚙️ Settings

### Waktu & Lokasi
- 📅 Tanggal/Kalender
- ⏰ Waktu
- 📍 Lokasi
- 🌍 Global

## Cara Menambahkan Icon ke Tabs

### Python Code
```python
# Format: "Icon Nama Tab"
tab1, tab2 = st.tabs(["📊 Jumlah Transaksi", "💰 Nilai Transaksi"])
```

### Tips Memilih Icon

1. **Konsisten**: Gunakan icon yang sama untuk tipe data yang sama
   - 📊 selalu untuk Jumlah
   - 💰 selalu untuk Nilai

2. **Jelas**: Icon harus mencerminkan konten
   - 🏪 untuk Etalase
   - 📦 untuk Katalog Produk

3. **Simpel**: Jangan terlalu banyak icon berbeda

4. **Kontras**: Gunakan icon yang terlihat jelas di dark theme

## Contoh Penggunaan

### Main Tabs
```python
tab1, tab2, tab3 = st.tabs([
    "📦 TRANSAKSI KATALOG",
    "🏪 TRANSAKSI KATALOG (ETALASE)",
    "📋 TABEL NILAI ETALASE"
])
```

### Analysis Tabs
```python
# Berdasarkan Kualifikasi Usaha
tab1, tab2 = st.tabs([
    "📊 Jumlah Transaksi Penyedia",
    "💰 Nilai Transaksi Penyedia"
])

# Berdasarkan Komoditas
tab1, tab2 = st.tabs([
    "📊 Jumlah Transaksi Tiap Komoditas",
    "💰 Nilai Transaksi Tiap Komoditas"
])

# Berdasarkan Perangkat Daerah
tab1, tab2 = st.tabs([
    "📊 Jumlah Transaksi Perangkat Daerah",
    "💰 Nilai Transaksi Perangkat Daerah"
])
```

## Icon Reference Quick

| Kategori | Icon Options |
|----------|-------------|
| **Numbers** | 📊 📈 📉 💯 |
| **Money** | 💰 💵 💳 💸 |
| **Products** | 📦 🏪 🛒 🛍️ |
| **Business** | 🏢 🏛️ 🏭 👥 |
| **Documents** | 📋 📄 📃 📑 |
| **Actions** | ✅ ❌ ⚠️ ℹ️ |
| **Upload/Download** | 📥 📤 💾 📁 |

## Update Icon

Untuk mengubah icon, edit langsung di file Python:

```python
# Sebelum
tab1, tab2 = st.tabs(["Jumlah", "Nilai"])

# Sesudah
tab1, tab2 = st.tabs(["📊 Jumlah", "💰 Nilai"])
```

Kemudian refresh browser (Ctrl+R atau Cmd+R).

---

**Catatan**: Icon emoji akan terlihat berbeda di setiap OS/browser, tapi tetap menarik! 🎉
