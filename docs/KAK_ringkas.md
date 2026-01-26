<style>
@page {
  size: A4;
  margin: 2.5cm 2cm 2cm 3cm;
}
body {
  font-family: "Times New Roman", serif;
  font-size: 12pt;
  line-height: 1.5;
  text-align: justify;
}
h1 { font-size: 14pt; text-align: center; font-weight: bold; }
h2 { font-size: 12pt; font-weight: bold; }
h3 { font-size: 12pt; font-weight: bold; }
table { width: 100%; border-collapse: collapse; margin: 10px 0; }
th, td { border: 1px solid black; padding: 8px; text-align: left; }
th { background-color: #f0f0f0; }
</style>

# KERANGKA ACUAN KERJA (KAK)
# PEMELIHARAAN APLIKASI SISTEM INFORMASI PELAPORAN PENGADAAN BARANG DAN JASA (SIP-SPSE)
# TAHUN ANGGARAN 2025

---

## I. LATAR BELAKANG

Pemerintah Provinsi Kalimantan Barat telah mengembangkan **Sistem Informasi Pelaporan Pengadaan Barang dan Jasa (SIP-SPSE)** sebagai platform terintegrasi untuk monitoring dan pelaporan kegiatan pengadaan. Aplikasi ini mengkonsolidasikan data dari berbagai sumber sistem pengadaan elektronik termasuk SIRUP, SPSE, SIKAP, E-Katalog, dan Toko Daring BELA.

Aplikasi SIP-SPSE melayani kebutuhan monitoring pengadaan untuk 15 wilayah di lingkungan Pemerintah Provinsi Kalimantan Barat dan Kabupaten/Kota, dengan volume data lebih dari 12.000 paket RUP per tahun, 250 pengguna aktif, dan uptime sistem 98.5%.

Untuk menjamin keberlangsungan operasional sistem, keamanan data, dan peningkatan kualitas layanan, diperlukan kegiatan pemeliharaan aplikasi yang terencana dan profesional.

---

## II. DASAR HUKUM

1. Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik sebagaimana telah diubah dengan Undang-Undang Nomor 19 Tahun 2016
2. Peraturan Presiden Nomor 16 Tahun 2018 tentang Pengadaan Barang/Jasa Pemerintah sebagaimana telah diubah dengan Peraturan Presiden Nomor 12 Tahun 2021
3. Peraturan Presiden Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik
4. Peraturan LKPP Nomor 12 Tahun 2021 tentang Pedoman Pelaksanaan Pengadaan Barang/Jasa Pemerintah Melalui Penyedia
5. Peraturan Daerah Provinsi Kalimantan Barat tentang APBD Tahun Anggaran 2025

---

## III. MAKSUD DAN TUJUAN

### A. Maksud

1. Menjamin ketersediaan dan keandalan sistem informasi pengadaan secara berkelanjutan
2. Memastikan data pengadaan dari berbagai sumber terintegrasi dengan baik dan akurat
3. Memberikan dukungan teknis kepada pengguna aplikasi

### B. Tujuan

1. Tercapainya tingkat ketersediaan sistem (*uptime*) minimal 99%
2. Terpeliharanya integrasi data dari 5 sumber data utama (SIRUP, SPSE, SIKAP, E-Katalog, BELA)
3. Terselesaikannya permasalahan teknis dalam waktu sesuai SLA yang ditetapkan
4. Terlaksananya pembaruan sistem sesuai perkembangan regulasi

---

## IV. RUANG LINGKUP PEKERJAAN

### A. Pemeliharaan Infrastruktur

| Komponen | Deskripsi |
|----------|-----------|
| Server & Container | Monitoring dan pemeliharaan Docker container |
| Database | Pemeliharaan DuckDB engine, optimasi query |
| Storage | Pemeliharaan S3-compatible storage (Parquet files) |
| Caching | Pemeliharaan sistem multi-layer cache |

### B. Pemeliharaan Modul Aplikasi

Aplikasi SIP-SPSE terdiri dari 11 modul:

1. **RUP** - Rencana Umum Pengadaan
2. **Tender** - Proses tender elektronik
3. **Non Tender** - Pengadaan langsung dan penunjukan langsung
4. **Pencatatan** - Tracking pencatatan transaksi
5. **E-Katalog v5** - Katalog nasional legacy
6. **E-Katalog v6** - Katalog modern
7. **Toko Daring** - Marketplace BELA
8. **Peserta Tender** - Analisis peserta lelang
9. **ITKP** - Indikator Tata Kelola Pengadaan
10. **Nilai SIKAP** - Skor kinerja penyedia
11. **Jenis Belanja** - Analisis komposisi belanja

### C. Integrasi Data

| Sumber Data | Frekuensi Sinkronisasi |
|-------------|------------------------|
| SIRUP | Harian |
| SPSE | Harian |
| SIKAP | Mingguan |
| E-Katalog | Mingguan |
| BELA/Toko Daring | Mingguan |

### D. Cakupan Wilayah

Pemeliharaan mencakup 15 wilayah: Provinsi Kalimantan Barat dan 14 Kabupaten/Kota (Bengkayang, Kapuas Hulu, Kayong Utara, Ketapang, Kubu Raya, Landak, Melawi, Mempawah, Sambas, Sanggau, Sekadau, Sintang, Pontianak, Singkawang).

### E. Jenis Pemeliharaan

1. **Corrective** - Perbaikan bug dan troubleshooting
2. **Preventive** - Monitoring, optimasi, backup terjadwal
3. **Adaptive** - Penyesuaian regulasi dan format data
4. **Perfective** - Peningkatan performa dan fitur minor

---

## V. SPESIFIKASI TEKNIS

### A. Stack Teknologi

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Framework Web | Streamlit | ≥ 1.40.0 |
| Bahasa Pemrograman | Python | 3.11 - 3.12 |
| Database Engine | DuckDB | ≥ 1.1.0 |
| Data Processing | Pandas | ≥ 2.2.0 |
| Visualisasi | Plotly Express | ≥ 5.24.0 |
| Containerization | Docker | Latest |

### B. Target Performa

| Parameter | Target |
|-----------|--------|
| Uptime | ≥ 99% |
| Response Time | < 3 detik |
| Concurrent Users | Min 50 pengguna |
| Cache Hit Rate | ≥ 80% |

---

## VI. SERVICE LEVEL AGREEMENT (SLA)

### A. Incident Response

| Kategori | Deskripsi | Waktu Respon | Waktu Resolusi |
|----------|-----------|--------------|----------------|
| Kritis | Sistem tidak dapat diakses | 1 jam | 4 jam |
| Tinggi | Fitur utama tidak berfungsi | 2 jam | 8 jam |
| Sedang | Fitur pendukung bermasalah | 4 jam | 24 jam |
| Rendah | Enhancement/informasi | 8 jam | 72 jam |

### B. Jam Layanan

- Jam kerja: Senin-Jumat, 08.00-17.00 WIB
- Layanan darurat 24/7 untuk insiden kritis

---

## VII. KELUARAN (OUTPUT)

| No | Keluaran | Frekuensi |
|----|----------|-----------|
| 1 | Laporan Pemeliharaan Bulanan | Bulanan |
| 2 | Laporan Insiden | Per Kejadian |
| 3 | Log Perubahan Sistem | Setiap Perubahan |
| 4 | Backup Data | Mingguan (full), Harian (incremental) |
| 5 | Laporan Akhir Pemeliharaan | Akhir Kontrak |

**Laporan Bulanan mencakup:**
- Executive summary (uptime, incidents, achievements)
- Statistik sistem dan performa
- Status sinkronisasi data
- Aktivitas pemeliharaan
- Rekomendasi perbaikan

---

## VIII. JANGKA WAKTU PELAKSANAAN

Jangka waktu pelaksanaan: **12 (dua belas) bulan kalender** sejak SPK diterbitkan.

| Tahap | Waktu |
|-------|-------|
| Serah Terima dan Handover | Bulan ke-1 (minggu 1-2) |
| Operasional Pemeliharaan | Bulan ke-1 s.d. ke-12 |
| Evaluasi Tengah Periode | Bulan ke-6 |
| Serah Terima Akhir | Bulan ke-12 (minggu terakhir) |

---

## IX. KUALIFIKASI PENYEDIA

### A. Persyaratan Administrasi

1. Berbadan hukum dan memiliki izin usaha yang masih berlaku
2. Memiliki NPWP dan telah memenuhi kewajiban perpajakan
3. Tidak masuk dalam daftar hitam LKPP
4. Memiliki pengalaman minimal 2 tahun dalam pemeliharaan aplikasi berbasis web
5. Memiliki minimal 2 referensi proyek sejenis

### B. Persyaratan Teknis

1. Memiliki tim teknis dengan kompetensi:
   - Python programming (Streamlit, Pandas, Plotly)
   - Database management (DuckDB, SQL)
   - DevOps (Docker, Linux)
   - System administration dan troubleshooting

2. Memiliki pemahaman tentang sistem pengadaan pemerintah (SPSE, SIRUP, SIKAP)
3. Memiliki kemampuan visualisasi data dan dashboard development
4. Memiliki pengalaman integrasi multi-sumber data

### C. Jaminan

1. Jaminan Pemeliharaan: 5% nilai kontrak (bank garansi/surety bond)
2. Non-Disclosure Agreement (NDA) untuk kerahasiaan data
3. Masa Garansi: 3 bulan setelah kontrak berakhir

---

## X. METODE PELAKSANAAN

### A. Prosedur Kerja

1. **Handover Awal** - Transfer knowledge dan akses sistem
2. **Monitoring Harian** - Status sistem, performa, sinkronisasi data
3. **Preventive Maintenance** - Backup, optimasi, patching (terjadwal)
4. **Incident Management** - Pelaporan, troubleshooting, resolusi
5. **Change Management** - Analisis, testing, approval, deployment
6. **Pelaporan** - Laporan bulanan dan dokumentasi

### B. Backup dan Recovery

| Jenis | Frekuensi | Retensi |
|-------|-----------|---------|
| Full Backup | Mingguan | 4 minggu |
| Incremental Backup | Harian | 7 hari |
| Configuration Backup | Setiap perubahan | 12 bulan |

**Recovery Objective:**
- RPO (Recovery Point Objective): Maksimal 24 jam
- RTO (Recovery Time Objective): Maksimal 4 jam

### C. Kanal Komunikasi

- Email support (jam kerja)
- Hotline darurat 24/7
- Ticketing system (preferred)
- Meeting koordinasi rutin (mingguan/bulanan)

---

## XI. PEMBIAYAAN

### A. Sumber Dana

- Sumber Dana: APBD Provinsi Kalimantan Barat
- Tahun Anggaran: 2025
- Mata Anggaran: [Disesuaikan dengan DPA]

### B. Komponen Biaya

| Komponen | Persentase Estimasi |
|----------|---------------------|
| Biaya Sumber Daya Manusia | 60-70% |
| Biaya Infrastruktur (hosting, storage, bandwidth) | 15-20% |
| Biaya Lisensi dan Tools | 3-5% |
| Biaya Operasional | 5-8% |
| Biaya Kontingensi | 5-7% |

### C. Mekanisme Pembayaran

Pembayaran dilakukan secara termin bulanan dengan syarat:
- Laporan bulanan lengkap dan tepat waktu
- System uptime mencapai target (≥ 99%)
- Tidak ada sanksi atau pelanggaran
- Berita Acara Pemeriksaan Pekerjaan

**Pembayaran akhir (bulan ke-12)** dilakukan setelah:
- Serah terima akhir lengkap
- Dokumentasi sistem terupdate
- Knowledge transfer selesai
- Tidak ada outstanding issues

---

## XII. EVALUASI KINERJA

### A. Key Performance Indicator (KPI)

| Indikator | Target | Bobot |
|-----------|--------|-------|
| System Uptime | ≥ 99% | 30% |
| Incident Resolution Time | Sesuai SLA | 25% |
| Data Sync Success Rate | ≥ 98% | 20% |
| Report Quality & Timeliness | 100% lengkap & tepat waktu | 15% |
| User Satisfaction | ≥ 4.0/5.0 | 10% |

**Penilaian:**
- Sangat Baik: 90-100
- Baik: 80-89
- Cukup: 70-79 (perlu perbaikan)
- Kurang: < 70 (denda sesuai kontrak)

### B. Periode Evaluasi

- Evaluasi bulanan untuk KPI operasional
- Evaluasi semesteran untuk kinerja keseluruhan
- User satisfaction survey triwulanan

---

## XIII. SANKSI DAN DENDA

| Pelanggaran | Sanksi |
|-------------|--------|
| Uptime < 95% | Peringatan + 0.5% nilai kontrak per bulan |
| Uptime < 90% | Peringatan ke-2 + 1% nilai kontrak per bulan |
| Keterlambatan laporan > 5 hari | Rp 500.000 per hari |
| Tidak respon insiden kritis > 2 jam | 0.1% nilai kontrak per kejadian |
| Kehilangan data tanpa backup | Pemutusan kontrak + 10% nilai kontrak |

**Catatan:** Sanksi tidak berlaku untuk kondisi force majeure yang telah dikonfirmasi.

---

## XIV. HAK DAN KEWAJIBAN

### A. Kewajiban Penyedia

1. Melaksanakan pekerjaan sesuai KAK dan kontrak
2. Menjaga kerahasiaan data dan informasi
3. Membuat laporan berkala lengkap dan tepat waktu
4. Bertanggung jawab atas kualitas pekerjaan
5. Melakukan knowledge transfer di akhir periode

### B. Kewajiban Pemberi Kerja

1. Melakukan pembayaran sesuai termin dan ketentuan
2. Menyediakan akses dan infrastruktur yang diperlukan
3. Memberikan informasi dan koordinasi yang dibutuhkan
4. Melakukan evaluasi secara objektif

---

## XV. KRITERIA PENERIMAAN PEKERJAAN

### A. Penerimaan Bulanan

Pekerjaan diterima setiap bulan jika:
- Uptime mencapai minimal 99%
- Semua insiden terselesaikan sesuai SLA
- Laporan bulanan lengkap dan tepat waktu
- Data tersinkronisasi sesuai jadwal

### B. Penerimaan Akhir

Pekerjaan diterima di akhir periode jika:
- Laporan akhir komprehensif diserahkan
- Dokumentasi sistem terupdate
- Knowledge transfer selesai dilakukan
- Sistem berjalan normal dan stabil
- Tidak ada bug kritis outstanding
- Berita Acara Serah Terima ditandatangani

---

## XVI. PENYELESAIAN PERSELISIHAN

Penyelesaian perselisihan dilakukan secara bertingkat:

1. **Musyawarah** (maks 14 hari kerja)
2. **Mediasi** dengan pejabat lebih tinggi (maks 30 hari kerja)
3. **Arbitrase** (BANI) atau Pengadilan Negeri

Prinsip penyelesaian: itikad baik, transparansi, win-win solution, dan kepatuhan hukum.

---

## XVII. PENUTUP

Kerangka Acuan Kerja ini disusun sebagai pedoman pelaksanaan kegiatan Pemeliharaan Aplikasi SIP-SPSE Tahun Anggaran 2025. Hal-hal yang belum diatur akan disesuaikan dengan ketentuan yang berlaku.

Demikian Kerangka Acuan Kerja ini dibuat untuk dapat dipergunakan sebagaimana mestinya.

---

<br><br><br>

|  |  |
|--|--|
| | **[Kota], [Tanggal Bulan Tahun]** |
| | **Pejabat Pembuat Komitmen** |
| | |
| | |
| | |
| | **[Nama Pejabat]** |
| | **NIP. [NIP]** |

---

*Dokumen ini dibuat dalam format Markdown dan dapat dikonversi ke PDF dengan ukuran kertas A4.*
