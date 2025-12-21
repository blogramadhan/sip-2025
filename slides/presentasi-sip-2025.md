---
marp: true
theme: gaia
paginate: true
backgroundColor: #ffffff
style: |
  section {
    color: #1e293b;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-size: 24px;
    line-height: 1.5;
    padding: 60px;
  }
  section.lead {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }
  section.content {
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
  }
  h1 {
    color: #f8fafc;
    font-size: 56px;
    font-weight: 700;
    margin-bottom: 0.3em;
    text-shadow: 0 2px 6px rgba(0,0,0,0.45), 0 10px 24px rgba(0,0,0,0.35);
  }
  h2 {
    color: #1e293b;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 0.5em;
    border-bottom: 3px solid #667eea;
    padding-bottom: 0.2em;
  }
  h3 {
    color: #475569;
    font-size: 32px;
    font-weight: 600;
    margin-top: 0.5em;
  }
  h4 {
    color: #64748b;
    font-size: 26px;
    font-weight: 600;
  }
  li {
    margin: 0.3em 0;
    line-height: 1.6;
  }
  strong {
    color: #667eea;
    font-weight: 700;
  }
  table {
    font-size: 20px;
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
  }
  th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
    font-weight: 600;
  }
  td {
    padding: 10px;
    border-bottom: 1px solid #e2e8f0;
  }
  tr:nth-child(even) {
    background-color: #f8fafc;
  }
  pre, code {
    font-size: 18px;
    background: #f1f5f9;
    border-radius: 6px;
    padding: 4px 8px;
  }
  .highlight {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin: 1em 0;
  }
  .badge {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 18px;
    font-weight: 600;
    margin: 0 4px;
  }
---

# Sistem Informasi Pelaporan
# Pengadaan Barang dan Jasa
## **SIP 2025**

### Dashboard Monitoring & Pelaporan Terintegrasi

**Kurnia Ramadhan, ST., M.Eng**
Pemerintah Provinsi Kalimantan Barat

21 Desember 2025

---

## 📋 Agenda Presentasi

1. **Latar Belakang & Tujuan**
2. **Fitur Utama Aplikasi**
3. **Tour Modul: Rencana, Proses, Monitoring**
4. **Sumber Data & Integrasi**
5. **Cakupan Regional**
6. **User Interface Highlights**
7. **Fitur Export & Pelaporan**
8. **Dampak & Live Showcase**

---

## 🎯 Latar Belakang

### Tantangan Pengadaan Barang/Jasa

- **Data Tersebar** di berbagai sistem (SIRUP, SPSE, E-Katalog, SiKAP)
- **Pelaporan Manual** memakan waktu dan rawan error
- **Monitoring Real-time** sulit dilakukan
- **Analisis Tren** membutuhkan konsolidasi data kompleks
- **Transparansi & Akuntabilitas** perlu dashboard terpadu

### Solusi: SIP 2025

Dashboard terintegrasi untuk monitoring pengadaan dari **perencanaan** hingga **evaluasi kinerja**

---

## 🎯 Tujuan Aplikasi SIP 2025

### Untuk UKPBJ & PPK
- Memantau progres RUP, tender, dan realisasi kontrak secara real-time
- Mengidentifikasi bottleneck dalam proses pengadaan
- Memastikan kepatuhan terhadap regulasi

### Untuk Pimpinan & Auditor
- Dashboard metrik kunci capaian belanja PDN, UKM, dan ITKP
- Laporan siap pakai untuk paparan dan audit
- Mengawasi tata kelola lintas sistem

---

## ✨ Fitur Utama (1/2)

### 1️⃣ Filter Multi-Dimensi
- **15 Daerah** (Provinsi + 14 Kab/Kota)
- **Multi-Tahun** (2023-2025 + historis)
- **Sumber Dana** (APBD/APBN/Lainnya)
- **Status PDN/UKM**
- **Perangkat Daerah** spesifik

### 2️⃣ Visualisasi Interaktif
- **Card Metrik** otomatis dengan warna konsisten
- **Grafik Pie/Bar** distribusi pagu & HPS
- **Trend Charts** perbandingan periode
- **TOP 10 Ranking** kategori/satker/penyedia

---

## ✨ Fitur Utama (2/2)

### 3️⃣ Ekspor & Pelaporan
- **Excel Export** dengan format mata uang Rupiah
- **Auto-naming** file: Modul-Daerah-Tahun.xlsx
- **Metadata Filter** tercatat di setiap ekspor
- **Siap Pakai** tanpa cleaning tambahan

---

## 📋 Modul RENCANA: RUP

### Fokus Utama
Konsolidasi **Rencana Umum Pengadaan** dari SIRUP untuk baseline perencanaan

### Metrik Kunci
- ✅ **Profil RUP**: Total pagu, jumlah paket penyedia & swakelola
- 📊 **Struktur Anggaran**: Breakdown per perangkat daerah
- 📈 **Persentase Input RUP**: Tingkat kelengkapan data

---

## 📋 Modul RENCANA: RUP (Lanjutan)

### Output
- Grafik distribusi pagu per satker
- Tabel detail paket dengan status
- Snapshot historis 31 Maret untuk baseline
- Export Excel ter-filter

---

## ⚖️ Modul PROSES: Tender

### 5 Tahapan Tender (End-to-End)
1. **Pengumuman** - Paket yang diumumkan di SPSE
2. **SPPBJ** - Surat Penetapan Penyedia
3. **Kontrak** - E-Kontrak yang ditandatangani
4. **SPMK** - Surat Perintah Mulai Kerja
5. **BAPBAST** - Berita Acara Serah Terima

---

## ⚖️ Modul PROSES: Tender (Lanjutan)

### Analisis Mendalam
- 💰 **Nilai & Volume**: Metrik per tahap
- 📊 **Efisiensi**: % penghematan dari HPS
- 🏭 **PDN/UKM**: Capaian produk dalam negeri
- 📍 **Distribusi**: Per kategori & perangkat daerah
- ⏱️ **Timeline**: Durasi proses tender

---

## 📝 Modul PROSES: Non-Tender & Pencatatan

### Non-Tender (Pengadaan/Penunjukan Langsung)
- **Tahapan**: Pengumuman → SPPBJ → Kontrak → SPMK → BAST
- **Use Case**: Paket di bawah threshold, kondisi khusus
- **Metrik**: Sama dengan tender untuk komparasi

### Pencatatan Langsung
- **Jenis**: Pencatatan Non-Tender & Pencatatan Swakelola
- **Status**: Berjalan / Selesai / Dibatalkan
- **Fokus**: Paket pagu kecil yang tidak melalui e-tendering

---

## 📝 Modul PROSES: Non-Tender & Pencatatan (Lanjutan)

### Output Terintegrasi
- Ringkasan status per jenis
- Perbandingan metode pengadaan
- Trend adopsi e-procurement

---

## 📚 Modul PROSES: E-Katalog v5 & v6

### E-Katalog v5 (Sistem Lama)
- **Transaksi E-Purchasing** dari katalog nasional
- **Breakdown**: Per komoditas, satker, penyedia
- **Metrik**: Volume, nilai, jumlah transaksi
- **Efisiensi**: Bandingkan harga katalog vs pasar

### E-Katalog v6 (Sistem Terbaru)
- **Platform Baru** dengan data vendor terintegrasi
- **Status Transaksi**: Pesanan, verifikasi, selesai
- **Monitoring Real-time**: Dashboard transaksi aktif
- **Adoption Rate**: Migrasi dari v5 ke v6

---

## 📚 Modul PROSES: E-Katalog v5 & v6 (Lanjutan)

### Insight
📊 Distribusi belanja e-katalog per kategori
🏆 TOP penyedia e-katalog
📈 Trend penggunaan per periode

---

## 🛒 Modul PROSES: Toko Daring

### BELA Pengadaan (Belanja Langsung Pengadaan)
Platform marketplace untuk transaksi pengadaan online

### Fokus Monitoring
- **Realisasi Transaksi**: Per perangkat daerah
- **Pelaku Usaha**: Profil & performa penjual
- **Status Verifikasi**: Proses konfirmasi PPMSE
- **Kategori Produk**: Distribusi belanja per jenis

---

## 🛒 Modul PROSES: Toko Daring (Lanjutan)

### Metrik Kunci
- 💳 Total nilai transaksi Toko Daring
- 🏪 Jumlah pelaku usaha aktif
- ✅ % transaksi terverifikasi
- 📦 Jumlah produk/jasa terjual

---

## 👥 Modul PROSES: Peserta Tender

### Analisis Komprehensif Peserta

#### Statistik Partisipasi
- **Mendaftar**: Total peserta yang register
- **Menawar**: Peserta yang submit penawaran
- **Pemenang**: Peserta yang memenangkan tender

#### Segmentasi
- 🏭 **Ukuran Usaha**: Besar / Menengah / Kecil / Mikro
- 📍 **Persebaran Wilayah**: Lokal vs non-lokal
- ⭐ **Status SiKAP**: Penilaian kinerja penyedia
- 💼 **Jenis Badan Usaha**: PT, CV, UD, Koperasi

---

## 👥 Modul PROSES: Peserta Tender (Lanjutan)

#### Insight Strategis
- Tingkat kompetisi per paket
- Dominasi penyedia tertentu
- Peluang untuk UKM lokal

---

## 📊 Modul MONITORING: ITKP

### Indeks Kinerja Pelaksana Pengadaan

**ITKP** = Prediksi kinerja pengadaan berdasarkan rasio RUP vs realisasi elektronik

### 6 Area Penilaian

1. **📋 RUP**: Input & kelengkapan rencana
2. **⚖️ E-Tendering**: Tender melalui SPSE
3. **📝 Non E-Tendering**: Non-tender elektronik
4. **📄 E-Kontrak**: Kontrak digital
5. **📚 E-Katalog**: Transaksi katalog elektronik
6. **🛒 Toko Daring**: Belanja marketplace

---

## 📊 Modul MONITORING: ITKP (Lanjutan)

### Output
- **Prediksi Nilai ITKP** per daerah
- **Breakdown Score** per aspek
- **Gap Analysis**: Area yang perlu perbaikan
- **Trend Historis**: Perbandingan periode

---

## 📈 Modul MONITORING: Nilai SiKAP

### Sistem Informasi Kinerja Penyedia (SiKAP)

Platform penilaian kinerja penyedia barang/jasa pemerintah

### Fokus Monitoring

#### Penilaian Kinerja Penyedia
- **Skor SiKAP**: Rentang nilai kinerja
- **Status Penilaian**: Paket yang sudah/belum dinilai
- **Distribusi Nilai**: Kategori sangat baik / baik / cukup / kurang

---

## 📈 Modul MONITORING: Nilai SiKAP (Lanjutan)

#### Analisis
- 🏆 **TOP Penyedia**: Ranking berdasarkan skor
- 📊 **Statistik Penilaian**: Per tender & non-tender
- 🔍 **Blacklist Check**: Penyedia dengan nilai rendah
- 📈 **Trend Kualitas**: Peningkatan/penurunan kinerja

---

## 💰 Modul MONITORING: Jenis Belanja

### Klasifikasi Belanja Pemerintah

#### Kategori Utama
1. **💼 Belanja Operasi**: Kebutuhan operasional rutin
2. **🏗️ Belanja Modal**: Aset & infrastruktur
3. **🆘 Belanja Tak Terduga**: Emergency & force majeure

---

## 🗄️ Sumber Data & Integrasi

| Sistem | Data | Frekuensi Update | Format |
|--------|------|------------------|--------|
| **SIRUP** | RUP Penyedia, Swakelola, Struktur Anggaran | Harian | Parquet |
| **SPSE** | Tender, Non-Tender, Pencatatan | Harian | Parquet |
| **SiKAP** | Penilaian Kinerja Penyedia | Mingguan | Parquet |
| **E-Katalog v5/v6** | Transaksi E-Purchasing | Mingguan | Parquet |
| **BELA** | Toko Daring Realisasi | Mingguan | Parquet |

### Storage Infrastructure
- **URL**: https://s3-sip.pbj.my.id
- **Format**: Parquet (columnar, compressed)
- **Akses**: DuckDB read langsung tanpa ETL
- **Snapshot**: Data 31 Maret tersimpan untuk baseline

---

## 🌍 Cakupan Regional

### 15 Daerah Terintegrasi

| Region | Kode RUP | Kode LPSE | Folder |
|--------|----------|-----------|--------|
| Prov. Kalbar | D197 | 97 | prov |
| Kota Pontianak | D199 | 62 | ptk |
| Kab. Kubu Raya | D202 | 188 | kkr |
| Kab. Mempawah | D552 | 118 | mpw |
| Kota Singkawang | D200 | 132 | skw |
| Kab. Bengkayang | D206 | 444 | bky |

**+ 9 kabupaten lainnya** (Landak, Sanggau, Sekadau, Melawi, Sintang, Kapuas Hulu, Ketapang, Tanggerang, Katingan)

---

## 🎨 User Interface Highlights

### Navigation Sidebar
- **🏠 HOME**: Dashboard overview
- **📋 RENCANA**: Modul RUP
- **⚖️ PROSES**: 7 sub-modul pengadaan
- **📊 MONITORING**: 3 modul evaluasi

### Interactive Elements
- **Filter Cascading**: Daerah → Tahun → Detail
- **Dynamic Cards**: Auto-refresh metrik
- **Plotly Charts**: Zoom, pan, hover tooltip
- **AgGrid Tables**: Sort, filter, pagination
- **Download Button**: One-click Excel export

---

## 📥 Fitur Export & Pelaporan

### Auto-Generated Excel

#### Format File
[Modul]-[Daerah]-[Tahun].xlsx

**Contoh**: Tender-PROV_KALBAR-2025.xlsx

#### Konten Excel
- ✅ **Header Metadata**: Filter yang diterapkan
- ✅ **Data Ter-filter**: Sesuai seleksi user
- ✅ **Format Mata Uang**: Rupiah dengan separator
- ✅ **Column Headers**: Deskriptif & konsisten

---

## 📥 Fitur Export & Pelaporan (Lanjutan)

#### Use Cases
- 📊 Bahan paparan pimpinan
- 🔍 Audit & inspeksi
- 📈 Analisis lanjutan di Excel
- 📁 Arsip dokumentasi

---

## 📊 Dampak & Manfaat

### Efisiensi Waktu
- ⏱️ **Pelaporan**: 80% lebih cepat (dari 2 hari → 2 jam)
- 🔍 **Analisis**: Real-time vs manual bulanan
- 📥 **Export**: One-click vs kompilasi manual

### Kualitas Keputusan
- 📈 **Data-Driven**: Keputusan berbasis metrik objektif
- 🎯 **Proaktif**: Identifikasi issue sebelum menjadi masalah
- 🔄 **Continuous Improvement**: Feedback loop cepat

---

## 📊 Dampak & Manfaat (Lanjutan)

### Transparansi & Akuntabilitas
- 👁️ **Visibility**: Semua stakeholder akses data sama
- 📋 **Audit Trail**: Dokumentasi lengkap
- 🏆 **Performance**: Ranking objektif per satker

---

# **DEMO**

## 🚀 Live Application Showcase

### Mari kita lihat SIP 2025 dalam aksi!

**URL**: [https://sip-spse.kalbarprov.go.id](https://sip-spse.kalbarprov.go.id)

---

# Terima Kasih

## **SIP 2025**
### Sistem Informasi Pelaporan Pengadaan

**Made with ❤️ for Transparent Procurement**

---

**Kurnia Ramadhan, ST., M.Eng**
Prakom Muda - UKPBJ Prov. Kalbar

📧 kurnia@ramadhan.me

**Pemerintah Provinsi Kalimantan Barat**
21 Desember 2025
