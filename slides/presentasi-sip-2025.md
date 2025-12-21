---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: 'SIP-2025 - Sistem Informasi Pelaporan Pengadaan Barang dan Jasa'
footer: 'Pemerintah Provinsi Kalimantan Barat | 2025'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# SIP-2025

## Sistem Informasi Pelaporan Pengadaan Barang dan Jasa

**Dashboard Monitoring dan Pelaporan Pengadaan Pemerintah Daerah Kalimantan Barat**

---

## Tentang SIP-2025

SIP-2025 adalah dashboard Streamlit yang membantu Unit Kerja Pengadaan Barang/Jasa (UKPBJ) memantau progres pengadaan dari perencanaan hingga evaluasi.

### Tujuan Utama
- Menyatukan data RUP, SPSE, E-Katalog, Toko Daring, dan SiKAP
- Visualisasi interaktif dan laporan siap unduh
- Monitoring real-time untuk pengambilan keputusan yang lebih baik

---

## Sasaran Pengguna

### 👥 Target Pengguna

1. **Pejabat Pengadaan & PPK**
   - Memantau RUP, tender, dan realisasi kontrak

2. **Kepala Perangkat Daerah**
   - Memastikan capaian belanja PDN, UKM, dan ITKP

3. **Auditor dan Inspektorat**
   - Mengawasi tata kelola serta konsistensi data lintas sistem

4. **Analis Data**
   - Mengunduh dataset ter-filter untuk analisis lanjutan

---

## Arsitektur Sistem

```
Pengguna → Streamlit UI (streamlit_app.py)
          ↓
       Module Page (src/rencana|proses|monitoring)
          ↓
       Fungsi utilitas (fungsi.py)
          ↓
       DuckDB in-memory engine
          ↓
       S3-compatible parquet objects
       (RUP, SPSE, SiKAP, Katalog, Daring)
```

---

## Teknologi yang Digunakan

### Stack Teknologi

- **Front-end:** Streamlit Multipage
- **Database:** DuckDB (in-memory)
- **Storage:** S3-compatible Parquet (https://s3-sip.pbj.my.id)
- **Visualisasi:** Plotly Express
- **Data Grid:** Streamlit AgGrid
- **Caching:** Streamlit `@st.cache_data` (6 jam)

---

## Fitur Utama - Dashboard Interaktif

### 📊 Visualisasi Data

- Filter per daerah, tahun anggaran, sumber dana
- Filter status PDN/UKM dan perangkat daerah
- Card metrik otomatis dengan gaya konsisten
- Grafik pie/bar dinamis untuk pagu dan HPS
- TOP 10 kategori pengadaan

---

## Fitur Utama - Analitik Proses

### ⚖️ Monitoring Pengadaan

- **Tender & Non-Tender:** 5 tahapan lengkap
  - Pengumuman → SPPBJ → Kontrak → SPMK → BAST

- **E-Katalog:** Versi 5 dan Versi 6

- **Toko Daring BELA:** Monitoring transaksi

- **Pencatatan Langsung:** Data pencatatan

- **Analisis Peserta:** Ukuran usaha, persebaran, status SiKAP

---

## Fitur Utama - Monitoring Tata Kelola

### 📈 Indikator Kinerja

1. **ITKP (Indikator Kinerja Pengadaan)**
   - Prediksi berbasis rasio RUP vs realisasi elektronik

2. **Nilai SiKAP**
   - Penilaian kinerja penyedia pada tender/non-tender

3. **Profil Belanja**
   - Analisis jenis belanja (Modal, Barang, Jasa)
   - Status PDN vs non-PDN

---

## Fitur Utama - Ekspor dan Pelaporan

### 📥 Download Data

- Unduh Excel sesuai filter aktif
- Nama file otomatis: `Modul-Daerah-Tahun.xlsx`
- Format mata uang Rupiah otomatis
- Data siap pakai untuk paparan atau audit
- Metadata filter tersimpan dalam file

---

## Modul dan Navigasi

### 📋 Rencana Pengadaan

| Modul | Deskripsi |
|-------|-----------|
| **RUP** | Konsolidasi paket penyedia & swakelola SIRUP, baseline anggaran & pagu per satker |

**Dataset:** RUP-PaketPenyedia-Terumumkan, RUP-PaketSwakelola, RUP-StrukturAnggaranPD

---

## Modul - Proses Pengadaan (1/2)

### ⚖️ Proses Pengadaan

| Modul | Deskripsi |
|-------|-----------|
| **Tender** | Analisis tender SPSE dari pengumuman sampai BAST |
| **Non Tender** | Pemantauan Pengadaan Langsung / Penunjukan langsung |
| **Pencatatan** | Transaksi pencatatan langsung SPSE (pagu kecil, swakelola) |

---

## Modul - Proses Pengadaan (2/2)

### 🛒 E-Purchasing

| Modul | Deskripsi |
|-------|-----------|
| **E-Katalog v5** | Paket e-purchasing katalog nasional v5 |
| **E-Katalog v6** | Adopsi katalog terbaru dengan data vendor & status transaksi |
| **Toko Daring** | Monitoring BELA Pengadaan (Toko Daring) |
| **Peserta Tender** | Statistik peserta, jenis usaha, persebaran wilayah |

---

## Modul - Monitoring

### 📊 Monitoring & Evaluasi

| Modul | Deskripsi |
|-------|-----------|
| **ITKP** | Prediksi nilai ITKP per aspek (RUP, e-tendering, non e-tendering, e-purchasing) |
| **Nilai SiKAP** | Skor kinerja penyedia tender & non-tender |
| **Jenis Belanja** | Komposisi belanja modal/barang/jasa, PDN vs non-PDN |

---

## Sumber Data

### 📦 Dataset dan Frekuensi Update

| Kategori | Frekuensi | Snapshot |
|----------|-----------|----------|
| **RUP** (Penyedia, Swakelola, Struktur Anggaran) | Harian | 31 Maret |
| **SPSE** Tender / Non Tender | Harian | - |
| **Pencatatan Langsung** | Harian | - |
| **SiKAP** | Mingguan | - |
| **E-Katalog v5/v6** | Mingguan | - |
| **BELA / Toko Daring** | Mingguan | - |

---

## Kapabilitas Data

### 💾 Coverage dan Storage

- **Cakupan:** Tahun berjalan + 2 tahun sebelumnya
- **Data Historis:** Snapshot 31 Maret untuk baseline perbandingan
- **Storage:** Parquet di S3-compatible (`https://s3-sip.pbj.my.id`)
- **Performance:** Caching 6 jam untuk akses cepat
- **Skalabilitas:** Lazy load Parquet + DuckDB support jutaan baris

---

## Daerah yang Terdaftar

### 🗺️ Cakupan Regional (15 Daerah)

| Daerah | Kode RUP | Kode LPSE |
|--------|----------|-----------|
| Provinsi Kalbar | D197 | 97 |
| Kota Pontianak | D199 | 62 |
| Kab. Kubu Raya | D202 | 188 |
| Kab. Mempawah | D552 | 118 |
| Kota Singkawang | D200 | 132 |
| Kab. Bengkayang | D206 | 444 |

**+ 9 daerah lainnya** (Landak, Sanggau, Sekadau, Melawi, Sintang, Kapuas Hulu, Ketapang, Tanggerang, Katingan)

---

## Multi-Regional & Skalabilitas

### 🌍 Ekspansi Mudah

- 15 daerah sudah terkonfigurasi
- Penambahan daerah cukup mengubah `region_config()`
- Tidak perlu refactor modul
- Support untuk mitra eksternal
- Dukungan lazy load untuk big data

---

## Workflow Ekspor & Pelaporan

### 📋 Langkah Penggunaan

1. **Filter Data**
   - Pilih daerah, tahun, status PDN/UKM, dll

2. **Download Excel**
   - Klik tombol unduh di kanan atas tabel

3. **File Siap Pakai**
   - Format mata uang Rupiah otomatis
   - Metadata filter tersimpan
   - Siap kirim ke pimpinan/auditor

---

## Struktur Proyek

```
SIP-2025/
├── streamlit_app.py       # Entry point & konfigurasi multipage
├── fungsi.py              # Utilitas: cache, logo, region config
├── requirements.txt
├── public/                # Asset logo
├── src/
│   ├── rencana/          # RUP
│   ├── proses/           # Tender, Non Tender, E-Katalog, dll
│   └── monitoring/       # ITKP, SiKAP, Jenis Belanja
└── .streamlit/           # Konfigurasi tema
```

---

## Instalasi

### 🚀 Quick Start

```bash
# Clone repository
git clone <repo-url>
cd SIP-2025

# Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run streamlit_app.py
```

Akses: `http://localhost:8501`

---

## Konfigurasi

### ⚙️ Customization

- **Tema & Layout:** `.streamlit/config.toml` (dark mode default)
- **Penyesuaian Daerah:** `region_config()` pada `fungsi.py`
- **Caching:** TTL cache 6 jam (dapat disesuaikan)
- **Logo:** `logo()` pada `fungsi.py`
- **Port:** Environment `STREAMLIT_SERVER_PORT`

---

## Roadmap Pengembangan

### 🚧 Future Development

- [ ] Integrasi API LKPP real-time
- [ ] Ekspor PDF/PPT untuk paparan
- [ ] Personalisasi dashboard per role (PPK, Pokja, Auditor)
- [ ] Notifikasi real-time (email/WhatsApp)
- [ ] Responsif mobile + mode kiosk
- [ ] Multi-bahasa (ID/EN)
- [ ] Role-based access control
- [ ] Analitik lanjutan (forecasting, deteksi anomali)

---

## Keunggulan SIP-2025

### ✨ Value Proposition

1. **Konsolidasi Data:** Semua sistem dalam satu dashboard
2. **Real-time Monitoring:** Data update harian/mingguan
3. **User-Friendly:** Interface intuitif dengan Streamlit
4. **Exportable:** Download Excel siap pakai
5. **Scalable:** Support jutaan baris data
6. **Customizable:** Mudah disesuaikan per daerah

---

## Dampak dan Manfaat

### 📈 Impact

- **Transparansi:** Data pengadaan terpusat dan mudah diakses
- **Efisiensi:** Pengurangan waktu pelaporan manual
- **Akuntabilitas:** Monitoring kinerja penyedia dan tata kelola
- **Data-Driven Decision:** Visualisasi membantu pengambilan keputusan
- **Audit Trail:** Riwayat data historis untuk compliance

---

## Demo Aplikasi

### 🎯 Fitur Navigasi

**Sidebar Menu:**
- 🏠 HOME
- 📋 Rencana Pengadaan (RUP)
- ⚖️ Proses Pengadaan (Tender, Non Tender, E-Katalog, dll)
- 📊 Monitoring (ITKP, SiKAP, Jenis Belanja)

**Filter Global:**
- Daerah (15 pilihan)
- Tahun Anggaran
- Perangkat Daerah
- Status PDN/UKM

---

## Kontribusi

### 🤝 How to Contribute

1. Fork repositori
2. Buat branch fitur (`git checkout -b feature/nama-fitur`)
3. Terapkan perubahan dengan deskripsi jelas
4. Jalankan uji coba di semua modul terdampak
5. Kirim Pull Request dengan:
   - Ringkasan perubahan
   - Screenshot (jika UI)
   - Panduan reproduksi

**Bug Report:** Gunakan GitHub Issues

---

## Teknologi & Dependencies

### 📦 Key Libraries

- **streamlit** - Web framework
- **streamlit-extras** - UI components
- **plotly** - Interactive charts
- **streamlit-aggrid** - Data grid
- **duckdb** - In-memory SQL engine
- **pandas** - Data manipulation
- **babel** - Currency formatting
- **openpyxl** - Excel export

---

## Keamanan & Privacy

### 🔒 Security Considerations

- Data disimpan di S3-compatible storage
- Akses terbatas untuk UKPBJ dan auditor
- VPN requirement untuk akses bucket privat
- No sensitive data exposure
- Audit trail untuk tracking

---

## Support & Kontak

### 📞 Getting Help

- **Dokumentasi:** README.md lengkap
- **Helpdesk:** Kanal komunikasi resmi UKPBJ
- **Email:** Email dinas
- **GitHub Issues:** Bug report dan feature request
- **Status:** Active Development

---

## Ucapan Terima Kasih

### 🙏 Acknowledgments

- **LKPP** - Akses data SPSE, SIRUP, SiKAP, E-Katalog
- **Pemerintah Daerah Kalbar** - Kolaborasi data regional
- **Kabupaten/Kota Mitra** - Partnership dan feedback
- **Komunitas Streamlit** - Open-source tools
- **Tim Developer** - Dedikasi dan inovasi

---

<!-- _class: lead -->
<!-- _paginate: false -->

# Terima Kasih

## Mari Wujudkan Tata Kelola Pengadaan yang Lebih Transparan

**SIP-2025**
Made with ❤️ untuk Pengadaan Barang dan Jasa

**Pemerintah Provinsi Kalimantan Barat**

---

## Q&A

### Pertanyaan dan Diskusi

Silakan ajukan pertanyaan Anda
