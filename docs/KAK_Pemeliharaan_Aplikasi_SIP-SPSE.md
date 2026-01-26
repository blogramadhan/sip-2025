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

Pemerintah Provinsi Kalimantan Barat dalam melaksanakan kegiatan pengadaan barang dan jasa telah mengembangkan **Sistem Informasi Pelaporan Pengadaan Barang dan Jasa (SIP-SPSE)** sebagai platform terintegrasi untuk monitoring dan pelaporan kegiatan pengadaan. Aplikasi ini mengkonsolidasikan data dari berbagai sumber sistem pengadaan elektronik termasuk SIRUP (Sistem Informasi Rencana Umum Pengadaan), SPSE (Sistem Pengadaan Secara Elektronik), SIKAP (Sistem Informasi Kinerja Penyedia), E-Katalog, dan Toko Daring BELA.

Aplikasi SIP-SPSE telah beroperasi dan melayani kebutuhan monitoring pengadaan untuk 15 (lima belas) wilayah di lingkungan Pemerintah Provinsi Kalimantan Barat dan Kabupaten/Kota mitra. Sejak diluncurkan, aplikasi ini telah mengelola dan mengintegrasikan data dari lebih dari 10.000+ paket pengadaan tahunan dengan total nilai pengadaan mencapai triliunan rupiah, melayani ratusan pengguna dari berbagai satuan kerja perangkat daerah (SKPD), dan memproses data real-time dari 5 sumber data eksternal yang berbeda.

### Kondisi dan Statistik Sistem Saat Ini:

**A. Volume Data dan Transaksi:**
- Total paket RUP yang dikelola: ±12.000 paket per tahun
- Total paket tender (lelang/seleksi): ±3.500 paket per tahun
- Total paket non-tender: ±2.000 paket per tahun
- Total transaksi e-katalog: ±5.000 transaksi per tahun
- Total penyedia terdaftar dengan skor SIKAP: ±2.500 penyedia
- Volume data Parquet storage: ±15 GB (meningkat 20% per tahun)

**B. Pengguna dan Akses:**
- Jumlah pengguna aktif: ±250 pengguna dari 15 wilayah
- Rata-rata concurrent users: 30-50 pengguna
- Peak usage: Akhir triwulan dan akhir tahun anggaran
- Jam operasional: 24/7 dengan maintenance window terjadwal

**C. Performa dan Ketersediaan:**
- Uptime sistem tahun berjalan: 98.5%
- Average response time: 2-4 detik
- Cache hit rate: 75-80%
- Data refresh cycle: Harian (SIRUP, SPSE), Mingguan (SIKAP, E-Katalog, BELA)

**D. Tantangan Operasional:**
1. Kebutuhan monitoring dan troubleshooting 24/7
2. Perubahan format data dan API dari sumber eksternal (LKPP)
3. Peningkatan volume data yang memerlukan optimasi storage dan query
4. Kebutuhan peningkatan fitur sesuai feedback pengguna
5. Keamanan data dan compliance terhadap regulasi
6. Sinkronisasi data yang kompleks dari 5 sistem berbeda

Untuk menjamin keberlangsungan operasional sistem, keamanan data, akurasi informasi, serta peningkatan kualitas layanan secara berkelanjutan, diperlukan kegiatan pemeliharaan aplikasi yang terencana, sistematis, dan profesional dengan dukungan tim yang kompeten.

Berdasarkan hal tersebut, perlu disusun Kerangka Acuan Kerja (KAK) sebagai pedoman pelaksanaan kegiatan Pemeliharaan Aplikasi SIP-SPSE Tahun Anggaran 2025.

---

## II. DEFINISI DAN ISTILAH

Untuk keseragaman pemahaman, berikut definisi istilah yang digunakan dalam dokumen ini:

| Istilah | Definisi |
|---------|----------|
| **SIP-SPSE** | Sistem Informasi Pelaporan Pengadaan Barang dan Jasa - aplikasi terintegrasi untuk monitoring dan pelaporan kegiatan pengadaan |
| **SIRUP** | Sistem Informasi Rencana Umum Pengadaan - sistem untuk perencanaan pengadaan |
| **SPSE** | Sistem Pengadaan Secara Elektronik - platform e-procurement |
| **SIKAP** | Sistem Informasi Kinerja Penyedia - sistem penilaian kinerja vendor |
| **ITKP** | Indikator Tata Kelola Pengadaan - metrik untuk menilai kualitas proses pengadaan |
| **E-Katalog** | Platform katalog elektronik untuk e-purchasing barang/jasa standar |
| **BELA** | Belanja Langsung - marketplace online pengadaan |
| **RUP** | Rencana Umum Pengadaan - dokumen perencanaan pengadaan tahunan |
| **PPK** | Pejabat Pembuat Komitmen - pejabat yang bertanggung jawab atas pelaksanaan pengadaan |
| **SKPD** | Satuan Kerja Perangkat Daerah - unit organisasi pemerintah daerah |
| **Uptime** | Persentase waktu sistem tersedia dan dapat diakses |
| **Downtime** | Periode waktu sistem tidak dapat diakses atau tidak berfungsi |
| **SLA** | Service Level Agreement - kesepakatan tingkat layanan |
| **KPI** | Key Performance Indicator - indikator kinerja kunci |
| **Bug** | Kesalahan atau cacat dalam program yang menyebabkan hasil tidak sesuai harapan |
| **Enhancement** | Peningkatan atau penambahan fitur aplikasi |
| **Parquet** | Format file kolumnar untuk data analytics yang efisien |
| **DuckDB** | In-memory analytical database engine |
| **Streamlit** | Framework Python untuk membuat web aplikasi data science |
| **Cache** | Penyimpanan sementara data untuk mempercepat akses |
| **API** | Application Programming Interface - antarmuka untuk integrasi sistem |
| **Incident** | Kejadian yang mengganggu atau berisiko mengganggu layanan |
| **UAT** | User Acceptance Testing - pengujian penerimaan oleh pengguna |
| **Backup** | Salinan data untuk keperluan pemulihan |
| **Recovery** | Proses pemulihan sistem atau data setelah kegagalan |
| **Force Majeure** | Kondisi di luar kendali yang mempengaruhi pelaksanaan kontrak |

---

## III. DASAR HUKUM

### A. Peraturan Perundang-undangan Tingkat Pusat

1. Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik sebagaimana telah diubah dengan Undang-Undang Nomor 19 Tahun 2016;
2. Undang-Undang Nomor 14 Tahun 2008 tentang Keterbukaan Informasi Publik;
3. Undang-Undang Nomor 25 Tahun 2009 tentang Pelayanan Publik;
4. Undang-Undang Nomor 23 Tahun 2014 tentang Pemerintahan Daerah sebagaimana telah diubah beberapa kali terakhir dengan Undang-Undang Nomor 9 Tahun 2015;
5. Peraturan Pemerintah Nomor 82 Tahun 2012 tentang Penyelenggaraan Sistem dan Transaksi Elektronik;
6. Peraturan Pemerintah Nomor 71 Tahun 2019 tentang Penyelenggaraan Sistem dan Transaksi Elektronik;
7. Peraturan Presiden Nomor 16 Tahun 2018 tentang Pengadaan Barang/Jasa Pemerintah sebagaimana telah diubah dengan Peraturan Presiden Nomor 12 Tahun 2021;
8. Peraturan Presiden Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik;
9. Peraturan Menteri Komunikasi dan Informatika Nomor 4 Tahun 2016 tentang Sistem Manajemen Pengamanan Informasi;
10. Peraturan LKPP Nomor 12 Tahun 2021 tentang Pedoman Pelaksanaan Pengadaan Barang/Jasa Pemerintah Melalui Penyedia;
11. Peraturan LKPP Nomor 14 Tahun 2022 tentang Standar Teknis Sistem Pengadaan Secara Elektronik (SPSE);
12. Peraturan Kepala Badan Siber dan Sandi Negara tentang Pedoman Teknis Evaluasi Keamanan Teknologi Informasi dan Komunikasi.

### B. Peraturan Daerah

1. Peraturan Daerah Provinsi Kalimantan Barat tentang Anggaran Pendapatan dan Belanja Daerah Tahun Anggaran 2025;
2. Peraturan Gubernur Kalimantan Barat tentang Kebijakan Teknologi Informasi dan Komunikasi (jika ada);
3. Keputusan Gubernur Kalimantan Barat tentang Penetapan Dokumen Pelaksanaan Anggaran (DPA) Tahun Anggaran 2025.

---

## IV. MAKSUD DAN TUJUAN

### A. Maksud

Kegiatan pemeliharaan aplikasi SIP-SPSE dimaksudkan untuk:

1. Menjamin ketersediaan dan keandalan sistem informasi pengadaan secara berkelanjutan;
2. Memastikan data pengadaan dari berbagai sumber terintegrasi dengan baik dan akurat;
3. Memberikan dukungan teknis kepada pengguna aplikasi di seluruh wilayah layanan;
4. Melakukan perbaikan dan peningkatan fitur sesuai kebutuhan pengguna.

### B. Tujuan

Tujuan dari kegiatan pemeliharaan aplikasi SIP-SPSE adalah:

1. Tercapainya tingkat ketersediaan sistem (*uptime*) minimal 99% selama periode pemeliharaan;
2. Terpeliharanya integrasi data dari 5 (lima) sumber data utama: SIRUP, SPSE, SIKAP, E-Katalog, dan Toko Daring BELA;
3. Terselesaikannya permasalahan teknis (*bug fixing*) dalam waktu maksimal 1x24 jam untuk kategori kritis dan 3x24 jam untuk kategori non-kritis;
4. Terlaksananya pembaruan sistem sesuai dengan perkembangan regulasi dan kebutuhan pengguna.

---

## V. RUANG LINGKUP PEKERJAAN

### A. Pemeliharaan Infrastruktur

| No | Komponen | Deskripsi Pekerjaan |
|----|----------|---------------------|
| 1 | Server & Container | Monitoring dan pemeliharaan Docker container, optimasi resource |
| 2 | Database | Pemeliharaan DuckDB engine, optimasi query, backup data |
| 3 | Storage | Pemeliharaan S3-compatible storage untuk file Parquet |
| 4 | Caching | Pemeliharaan sistem multi-layer cache (Memory, Disk, Remote) |
| 5 | Jaringan | Monitoring konektivitas ke sumber data eksternal |

### B. Pemeliharaan Modul Aplikasi

Aplikasi SIP-SPSE terdiri dari 11 (sebelas) modul yang harus dipelihara:

**1. Modul RUP (Rencana Umum Pengadaan)**

Detail Fitur:
- Konsolidasi data SIRUP dari berbagai satuan kerja
- Visualisasi struktur anggaran per SKPD dan per jenis belanja
- Tracking paket penyedia vs paket swakelola
- Analisis pagu anggaran dan realisasi
- Filter multi-dimensi (wilayah, SKPD, jenis paket, sumber dana)
- Export data untuk pelaporan

Tanggung Jawab Pemeliharaan:
- Memastikan sinkronisasi harian data SIRUP berjalan normal
- Validasi akurasi perhitungan agregasi dan subtotal
- Monitoring perubahan struktur data SIRUP dari LKPP
- Optimasi query untuk dataset besar (>10K records)
- Bug fixing terkait filter dan pencarian

**2. Modul Tender**

Detail Fitur:
- Dashboard status tender (pengumuman, kualifikasi, evaluasi, pemenang)
- Timeline visualization untuk setiap tahapan tender
- Analisis metode pemilihan (lelang umum, sederhana, pemilihan langsung)
- Statistik peserta dan tingkat kompetisi
- Monitoring dokumen BAST (Berita Acara Serah Terima)
- Alerting untuk paket tender bermasalah atau terlambat

Tanggung Jawab Pemeliharaan:
- Sinkronisasi harian data tender dari SPSE
- Validasi mapping status tender
- Perbaikan bug terkait perhitungan timeline
- Optimasi loading untuk data tender historis
- Update sesuai perubahan regulasi lelang

**3. Modul Non Tender**

Detail Fitur:
- Monitoring pengadaan langsung dan penunjukan langsung
- Tracking proses dari pengumuman hingga kontrak
- Analisis nilai dan volume non-tender per wilayah
- Compliance check terhadap threshold non-tender
- Statistik vendor pemenang non-tender

Tanggung Jawab Pemeliharaan:
- Sinkronisasi harian data non-tender
- Validasi business rules compliance
- Bug fixing terkait filter dan aggregasi
- Performance optimization

**4. Modul Pencatatan**

Detail Fitur:
- Tracking pencatatan transaksi pengadaan di SPSE
- Monitoring dokumen pendukung pencatatan
- Analisis volume dan nilai pencatatan per periode
- Validasi kelengkapan data pencatatan

Tanggung Jawab Pemeliharaan:
- Sinkronisasi data pencatatan
- Validasi completeness data
- Bug fixing dan performance tuning

**5. Modul E-Katalog v5 (Legacy)**

Detail Fitur:
- Monitoring transaksi e-purchasing katalog nasional versi lama
- Statistik penggunaan e-katalog per SKPD
- Analisis produk katalog yang sering digunakan
- Tracking nilai transaksi e-katalog

Tanggung Jawab Pemeliharaan:
- Sinkronisasi mingguan data e-katalog v5
- Maintain kompatibilitas dengan API legacy
- Monitoring untuk eventual deprecation

**6. Modul E-Katalog v6 (Modern)**

Detail Fitur:
- Dashboard modern untuk transaksi e-katalog terbaru
- Detail informasi vendor dan produk katalog
- Status tracking dari order hingga delivery
- Rating dan review produk katalog
- Integrasi dengan sistem pembayaran

Tanggung Jawab Pemeliharaan:
- Sinkronisasi mingguan data e-katalog v6
- Adaptasi terhadap perubahan API e-katalog
- Enhancement fitur sesuai feedback pengguna
- Performance optimization untuk large dataset

**7. Modul Toko Daring (BELA)**

Detail Fitur:
- Monitoring transaksi marketplace online BELA
- Statistik merchant dan produk
- Tracking order dan delivery status
- Analisis tren belanja online
- Comparison dengan e-katalog

Tanggung Jawab Pemeliharaan:
- Sinkronisasi mingguan data BELA
- Validasi integritas data transaksi
- Bug fixing dan feature enhancement
- API adaptation untuk perubahan platform BELA

**8. Modul Peserta Tender**

Detail Fitur:
- Analisis statistik peserta tender per paket
- Distribusi peserta per wilayah dan kategori
- Tingkat kompetisi dan rata-rata peserta
- Integrasi dengan skor SIKAP peserta
- Analisis win rate vendor
- Blacklist dan vendor monitoring

Tanggung Jawab Pemeliharaan:
- Data aggregation dari multiple sources
- Calculation accuracy untuk statistik kompleks
- Performance optimization untuk analisis besar
- Visualization enhancement

**9. Modul ITKP (Indikator Tata Kelola Pengadaan)**

Detail Fitur:
- Prediksi scoring ITKP berdasarkan data aktual
- Breakdown indikator per dimensi
- Benchmarking antar wilayah
- Rekomendasi perbaikan skor
- Historical trend analysis
- Early warning untuk indikator rendah

Tanggung Jawab Pemeliharaan:
- Update formula sesuai ketentuan LKPP terbaru
- Validasi akurasi perhitungan
- Enhancement algoritma prediksi
- Bug fixing calculation logic

**10. Modul Nilai SIKAP**

Detail Fitur:
- Display skor kinerja penyedia
- Kategorisasi penyedia (baik, cukup, kurang)
- Historical tracking perubahan skor
- Filter dan pencarian penyedia
- Integration dengan modul tender untuk vendor screening

Tanggung Jawab Pemeliharaan:
- Sinkronisasi mingguan data SIKAP
- Validasi scoring accuracy
- Enhancement tampilan dan filter
- Bug fixing

**11. Modul Jenis Belanja**

Detail Fitur:
- Analisis komposisi belanja (modal/barang/jasa)
- Breakdown PDN (Produk Dalam Negeri) vs non-PDN
- Trend analysis belanja per periode
- Compliance monitoring terhadap target PDN
- Benchmarking antar wilayah
- Drill-down capability ke level paket

Tanggung Jawab Pemeliharaan:
- Data aggregation dan calculation accuracy
- Enhancement visualization dan reporting
- Performance optimization
- Bug fixing terkait categorization

### C. Pemeliharaan Integrasi Data

| No | Sumber Data | Frekuensi Sinkronisasi | Keterangan |
|----|-------------|------------------------|------------|
| 1 | SIRUP | Harian | Data RUP dan struktur anggaran |
| 2 | SPSE | Harian | Data tender dan non-tender |
| 3 | SIKAP | Mingguan | Skor kinerja penyedia |
| 4 | E-Katalog v5/v6 | Mingguan | Paket dan transaksi katalog |
| 5 | BELA/Toko Daring | Mingguan | Data marketplace |

### D. Cakupan Wilayah Layanan

Pemeliharaan mencakup dukungan untuk 15 (lima belas) wilayah:

| No | Kode | Nama Daerah |
|----|------|-------------|
| 1 | D197 | Provinsi Kalimantan Barat |
| 2 | D199 | Kabupaten Bengkayang |
| 3 | D200 | Kabupaten Kapuas Hulu |
| 4 | D201 | Kabupaten Kayong Utara |
| 5 | D202 | Kabupaten Ketapang |
| 6 | D203 | Kabupaten Kubu Raya |
| 7 | D204 | Kabupaten Landak |
| 8 | D205 | Kabupaten Melawi |
| 9 | D206 | Kabupaten Mempawah |
| 10 | D207 | Kabupaten Sambas |
| 11 | D208 | Kabupaten Sanggau |
| 12 | D209 | Kabupaten Sekadau |
| 13 | D210 | Kabupaten Sintang |
| 14 | D211 | Kota Pontianak |
| 15 | D212 | Kota Singkawang |

### E. Lingkup Teknis Pemeliharaan

1. **Corrective Maintenance (Perbaikan)**
   - Identifikasi dan perbaikan bug/error pada aplikasi
   - Penanganan insiden dan troubleshooting
   - Pemulihan sistem dari kondisi tidak normal

2. **Preventive Maintenance (Pencegahan)**
   - Monitoring performa sistem secara berkala
   - Optimasi query database dan caching
   - Pembaruan library dan dependencies
   - Backup data secara terjadwal

3. **Adaptive Maintenance (Penyesuaian)**
   - Penyesuaian sistem terhadap perubahan regulasi LKPP
   - Penyesuaian terhadap perubahan format data sumber
   - Penyesuaian terhadap perubahan API eksternal

4. **Perfective Maintenance (Peningkatan)**
   - Peningkatan performa loading dan query
   - Perbaikan user interface dan user experience
   - Penambahan fitur minor sesuai kebutuhan pengguna

---

## VI. SPESIFIKASI TEKNIS

### A. Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│           User Interface (Streamlit Dashboard)           │
│  - Navigasi multipage dengan filter sidebar              │
│  - Dashboard tema gelap dengan metric cards              │
│  - Grafik interaktif Plotly & tabel AgGrid               │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│            Caching & Data Loading Layer                  │
│  - Multi-layer cache (Memory LRU → DiskDB → S3)          │
│  - TTL cache Streamlit 6 jam                             │
│  - Intelligent cache invalidation                        │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│         Data Processing & Query Engine                   │
│  - DuckDB in-memory SQL engine                           │
│  - Direct Parquet file querying                          │
│  - Pandas untuk manipulasi data                          │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│            Data Storage Layer                            │
│  - S3-compatible bucket                                  │
│  - Format file Parquet                                   │
│  - Organisasi per wilayah, dataset, dan tahun            │
└─────────────────────────────────────────────────────────┘
```

### B. Stack Teknologi

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Framework Web | Streamlit | ≥ 1.40.0 |
| Bahasa Pemrograman | Python | 3.11 - 3.12 |
| Database Engine | DuckDB | ≥ 1.1.0 |
| Data Processing | Pandas | ≥ 2.2.0 |
| Visualisasi | Plotly Express | ≥ 5.24.0 |
| Data Table | Streamlit AgGrid | ≥ 1.0.5 |
| File Format | PyArrow/FastParquet | ≥ 18.1.0 |
| Containerization | Docker | Latest |

### C. Kebutuhan Performa

| Parameter | Target |
|-----------|--------|
| Uptime | ≥ 99% |
| Response Time | < 3 detik untuk halaman standar |
| Data Freshness | Sesuai frekuensi sinkronisasi |
| Concurrent Users | Minimal 50 pengguna |
| Cache Hit Rate | ≥ 80% |

### D. Keamanan Sistem

| Aspek Keamanan | Implementasi |
|----------------|--------------|
| Authentication | Multi-level user access control |
| Authorization | Role-based access control (RBAC) |
| Data Encryption | TLS 1.3 untuk data in-transit |
| Audit Trail | Logging aktivitas pengguna dan sistem |
| Backup Security | Encrypted backup dengan retention policy |
| Vulnerability Management | Regular security scanning dan patching |
| Network Security | Firewall, IP whitelisting untuk akses admin |
| DDOS Protection | Rate limiting dan traffic monitoring |

### E. Monitoring dan Observability

| Komponen | Tools/Metode | Metrik |
|----------|--------------|--------|
| Application Monitoring | Health check endpoint | Response time, error rate, request count |
| Infrastructure Monitoring | Docker stats, system metrics | CPU, memory, disk usage |
| Log Management | Centralized logging | Error logs, access logs, audit logs |
| Performance Monitoring | Query profiling | Database query time, cache performance |
| Uptime Monitoring | External monitoring service | Availability, downtime alerts |

---

## VII. KELUARAN (OUTPUT)

Keluaran yang diharapkan dari kegiatan pemeliharaan ini adalah:

### A. Deliverables Rutin

| No | Keluaran | Frekuensi | Format | Deadline |
|----|----------|-----------|--------|----------|
| 1 | Laporan Pemeliharaan Bulanan | Bulanan | PDF + Excel | Tanggal 5 bulan berikutnya |
| 2 | Laporan Insiden | Per Kejadian | PDF | 1x24 jam setelah resolusi |
| 3 | Log Perubahan Sistem | Setiap Perubahan | Markdown/PDF | Real-time update |
| 4 | Monitoring Report | Mingguan | Dashboard + PDF | Setiap Senin pagi |
| 5 | Backup Verification Report | Mingguan | PDF | Setiap Senin |

### B. Deliverables Periodik

| No | Keluaran | Frekuensi | Format | Deadline |
|----|----------|-----------|--------|----------|
| 1 | Performance Analysis Report | Triwulanan | PDF + PPT | Minggu pertama setelah akhir triwulan |
| 2 | Capacity Planning Report | Semesteran | PDF + Excel | 2 minggu setelah akhir semester |
| 3 | Security Audit Report | Semesteran | PDF | 2 minggu setelah akhir semester |
| 4 | User Satisfaction Survey | Triwulanan | PDF + Excel | Minggu kedua setelah survey |

### C. Deliverables Akhir Kontrak

| No | Keluaran | Keterangan | Format |
|----|----------|------------|--------|
| 1 | Laporan Akhir Komprehensif | Summary 12 bulan pemeliharaan, achievements, challenges, recommendations | PDF + PPT |
| 2 | Dokumentasi Sistem Terupdate | Architecture, API docs, user manual, troubleshooting guide | PDF + HTML |
| 3 | Source Code & Configuration | Semua perubahan yang dilakukan selama masa kontrak | Git Repository |
| 4 | Knowledge Base | FAQ, best practices, lesson learned | Wiki/Confluence |
| 5 | Backup Final & Restore Guide | Full backup data dan prosedur restore | Encrypted Archive + PDF |
| 6 | Handover Document | Prosedur serah terima, akses, kredensial (sealed) | PDF (Confidential) |

### D. Spesifikasi Detail Laporan Bulanan

Laporan bulanan harus mencakup minimal:

1. **Executive Summary (1-2 halaman)**
   - Key metrics: Uptime, response time, incidents
   - Major achievements dan issues
   - Action items untuk bulan depan

2. **System Availability (2-3 halaman)**
   - Uptime percentage dengan breakdown per hari
   - Downtime analysis dengan root cause
   - Scheduled vs unscheduled downtime
   - Comparison dengan bulan sebelumnya

3. **Performance Metrics (2-3 halaman)**
   - Response time trends dengan grafik
   - Resource utilization (CPU, Memory, Disk)
   - Cache hit rate dan optimization efforts
   - User concurrency analysis

4. **Data Synchronization (1-2 halaman)**
   - Status sync per data source
   - Success rate dan failure analysis
   - Data volume dan growth trend
   - API changes atau issues

5. **Maintenance Activities (3-4 halaman)**
   - Preventive maintenance checklist
   - Corrective actions (bug fixes)
   - Adaptive changes (regulation updates)
   - Perfective improvements (enhancements)

6. **Incident Management (2-3 halaman)**
   - Incident log dengan detail
   - Response dan resolution time
   - Root cause analysis untuk major incidents
   - Preventive measures implemented

7. **Security & Compliance (1-2 halaman)**
   - Security events dan threats
   - Patch management status
   - Compliance status
   - Vulnerability findings dan remediation

8. **User Support (1-2 halaman)**
   - Support tickets statistics
   - Common issues dan resolutions
   - User feedback dan satisfaction
   - Training atau assistance provided

9. **Recommendations & Next Steps (1-2 halaman)**
   - Identified improvements
   - Risk mitigation plans
   - Planned activities untuk bulan depan
   - Resource needs atau concerns

---

## VIII. JANGKA WAKTU PELAKSANAAN

Jangka waktu pelaksanaan kegiatan pemeliharaan adalah **12 (dua belas) bulan kalender** terhitung sejak Surat Perintah Kerja (SPK) diterbitkan.

| Tahap | Kegiatan | Waktu |
|-------|----------|-------|
| 1 | Serah Terima dan Handover | Bulan ke-1 (minggu 1-2) |
| 2 | Operasional Pemeliharaan | Bulan ke-1 s.d. ke-12 |
| 3 | Laporan Bulanan | Setiap akhir bulan |
| 4 | Evaluasi Tengah Periode | Bulan ke-6 |
| 5 | Serah Terima Akhir | Bulan ke-12 (minggu terakhir) |

---

## IX. KUALIFIKASI PENYEDIA

### A. Persyaratan Administrasi

1. Berbadan hukum dan memiliki izin usaha yang masih berlaku;
2. Memiliki NPWP dan telah memenuhi kewajiban perpajakan tahun terakhir;
3. Tidak masuk dalam daftar hitam LKPP;
4. Memiliki pengalaman minimal 2 (dua) tahun dalam pemeliharaan aplikasi berbasis web.

### B. Persyaratan Teknis

1. **Memiliki tenaga ahli dengan kompetensi:**

| No | Posisi | Kualifikasi Minimal | Kompetensi Teknis | Jumlah | Alokasi |
|----|--------|---------------------|-------------------|--------|---------|
| 1 | Project Manager | • S1 Teknik Informatika/SI/sejenis<br>• Pengalaman min. 5 tahun<br>• Sertifikat PMP/Prince2 (preferred) | • Project management<br>• Risk management<br>• Stakeholder communication<br>• Budgeting & reporting | 1 orang | Full-time |
| 2 | Technical Lead | • S1 Teknik Informatika/SI<br>• Pengalaman min. 4 tahun<br>• Pengalaman arsitektur sistem | • System architecture<br>• Python advanced<br>• Database design<br>• Technical decision making | 1 orang | Full-time |
| 3 | Full Stack Developer | • S1 Teknik Informatika/SI<br>• Pengalaman min. 3 tahun<br>• Portfolio aplikasi web | • Python & Streamlit<br>• Pandas & data processing<br>• Plotly visualization<br>• API integration<br>• Git version control | 2 orang | Full-time |
| 4 | Database Administrator | • S1 Teknik Informatika/SI<br>• Pengalaman min. 3 tahun<br>• Sertifikat DBA (preferred) | • DuckDB proficient<br>• SQL advanced<br>• Query optimization<br>• Backup & recovery<br>• Data migration | 1 orang | Full-time |
| 5 | DevOps Engineer | • S1 Teknik Informatika/SI<br>• Pengalaman min. 3 tahun<br>• Pengalaman containerization | • Docker & containerization<br>• Linux system admin<br>• CI/CD pipeline<br>• Monitoring tools<br>• Shell scripting | 1 orang | Full-time |
| 6 | Technical Support | • D3/S1 Teknik Informatika/SI<br>• Pengalaman min. 2 tahun<br>• Customer service oriented | • Troubleshooting<br>• User training<br>• Documentation<br>• Ticketing system<br>• Communication skills | 2 orang | Full-time |

**Catatan Penting:**
- Minimal 1 orang dari tim harus memiliki pengalaman dengan sistem pengadaan pemerintah (SPSE/SIRUP)
- CV dan portofolio setiap personel wajib dilampirkan
- Penggantian personel hanya diizinkan dengan persetujuan PPK dan kualifikasi setara/lebih baik
- Kehadiran personel kunci (PM, Tech Lead) di kantor minimal 3 hari per minggu

2. **Persyaratan Perusahaan:**
   - Memiliki pengalaman minimal 2 (dua) tahun dalam pemeliharaan aplikasi berbasis web
   - Memiliki minimal 3 (tiga) referensi proyek sejenis dari instansi pemerintah atau swasta
   - Memiliki kantor operasional yang jelas dan dapat diverifikasi
   - Memiliki infrastruktur pendukung (server development, testing environment)

3. **Persyaratan Kompetensi:**
   - Memiliki pemahaman tentang sistem pengadaan barang/jasa pemerintah (SPSE, SIRUP, SIKAP)
   - Memiliki kemampuan dalam pengembangan dashboard dan visualisasi data
   - Memiliki pengalaman dalam integrasi multi-sumber data
   - Memiliki kemampuan dalam performance tuning dan optimization

4. **Sertifikasi (Preferred but not mandatory):**
   - Project Management Professional (PMP) / Prince2 untuk PM
   - Database certification (Oracle, PostgreSQL, atau sejenis) untuk DBA
   - Cloud certification (AWS, GCP, atau sejenis) untuk DevOps
   - ITIL Foundation untuk Technical Support
   - Certified Ethical Hacker (CEH) atau sejenis untuk security awareness

### C. Jaminan dan Asuransi

1. **Jaminan Pemeliharaan**
   - Nilai: 5% dari nilai kontrak
   - Bentuk: Bank garansi atau surety bond
   - Masa berlaku: Selama masa kontrak + 1 bulan
   - Dicairkan jika penyedia cidera janji atau kinerja tidak memenuhi standar

2. **Jaminan Kerahasiaan Data**
   - Penyedia wajib menandatangani Non-Disclosure Agreement (NDA)
   - Sanksi pelanggaran sesuai ketentuan hukum yang berlaku
   - Penyedia bertanggung jawab atas keamanan data yang diakses

3. **Asuransi Tanggung Gugat**
   - Penyedia wajib memiliki asuransi pertanggungjawaban profesional
   - Coverage minimal Rp 500.000.000,-
   - Untuk menutup risiko kerugian akibat kelalaian atau kesalahan

4. **Masa Garansi**
   - Garansi 3 (tiga) bulan setelah masa kontrak berakhir
   - Mencakup bug fixing untuk masalah yang timbul dari pekerjaan selama masa kontrak
   - Tidak mencakup perubahan requirement baru atau force majeure

---

## X. METODE PELAKSANAAN

### A. Manajemen Layanan

1. **Service Desk**
   - Penyediaan kanal pelaporan insiden (email, telepon, ticketing)
   - Jam layanan: Senin-Jumat, 08.00-17.00 WIB
   - Layanan darurat 24/7 untuk insiden kritis

2. **Tingkat Layanan (SLA)**

| Kategori | Deskripsi | Waktu Respon | Waktu Resolusi |
|----------|-----------|--------------|----------------|
| Kritis | Sistem tidak dapat diakses | 1 jam | 4 jam |
| Tinggi | Fitur utama tidak berfungsi | 2 jam | 8 jam |
| Sedang | Fitur pendukung bermasalah | 4 jam | 24 jam |
| Rendah | Permintaan informasi/enhancement | 8 jam | 72 jam |

### B. Prosedur Perubahan

1. Pencatatan permintaan perubahan;
2. Analisis dampak dan estimasi effort;
3. Persetujuan dari pemilik pekerjaan;
4. Pelaksanaan perubahan di environment testing;
5. User Acceptance Test (UAT);
6. Deployment ke production;
7. Dokumentasi perubahan.

### C. Backup dan Recovery

| Jenis Backup | Frekuensi | Retensi |
|--------------|-----------|---------|
| Full Backup | Mingguan | 4 minggu |
| Incremental Backup | Harian | 7 hari |
| Configuration Backup | Setiap perubahan | 12 bulan |

**Prosedur Recovery:**
1. Identifikasi tingkat kerusakan dan pilih strategi recovery
2. Restore dari backup terdekat (RTO target: 2 jam)
3. Verifikasi integritas data hasil restore
4. Testing fungsional sistem
5. Dokumentasi insiden dan langkah recovery

**Recovery Point Objective (RPO):** Maksimal 24 jam
**Recovery Time Objective (RTO):** Maksimal 4 jam untuk sistem kritis

### D. Monitoring dan Pelaporan

**1. Monitoring Harian:**
- Status availability sistem
- Performa aplikasi (response time, error rate)
- Kapasitas storage dan resource
- Status sinkronisasi data
- Alert dan notifikasi insiden

**2. Laporan Mingguan:**
- Summary uptime dan downtime
- Statistik penggunaan per wilayah
- Insiden dan resolusi
- Performa sistem (trend analysis)

**3. Laporan Bulanan:**
- Executive summary ketersediaan sistem
- Statistik penggunaan detail
- Analisis tren performa
- Daftar perubahan dan enhancement
- Rekomendasi perbaikan
- Plan untuk bulan berikutnya

**4. Laporan Insiden (Sesuai Kejadian):**
- Kronologi kejadian
- Root cause analysis
- Dampak terhadap layanan
- Langkah mitigasi dan resolusi
- Preventive action

### E. Koordinasi dan Komunikasi

**1. Mekanisme Koordinasi:**

| Kegiatan | Frekuensi | Peserta | Media |
|----------|-----------|---------|-------|
| Daily Standup | Harian | Tim internal | Online meeting |
| Progress Review | Mingguan | Tim + PPK | Meeting/Video call |
| Steering Committee | Bulanan | Stakeholder + Tim | Formal meeting |
| Incident Response | Sesuai kebutuhan | Tim teknis | Teleconference/Chat |

**2. Kanal Komunikasi:**
- Email: [email-support@domain.go.id] (Jam kerja)
- Hotline: [Nomor telepon] (Darurat 24/7)
- Ticketing System: [URL sistem tiket] (Preferred)
- WhatsApp Group: [Untuk koordinasi cepat]
- Knowledge Base: [URL dokumentasi]

---

## XI. PEMBIAYAAN

### A. Sumber Pembiayaan

Biaya pemeliharaan aplikasi SIP-SPSE dibebankan pada:

- **Mata Anggaran:** [Disesuaikan dengan DPA]
- **Program:** [Disesuaikan dengan DPA]
- **Kegiatan:** [Disesuaikan dengan DPA]
- **Sub Kegiatan:** Pemeliharaan Aplikasi Sistem Informasi Pelaporan Pengadaan
- **Tahun Anggaran:** 2025
- **Sumber Dana:** APBD Provinsi Kalimantan Barat

### B. Rincian Komponen Biaya

| No | Komponen | Sub Komponen | Persentase Estimasi | Keterangan |
|----|----------|--------------|---------------------|------------|
| 1 | Biaya Tenaga Ahli | - Project Manager<br>- Technical Lead<br>- Full Stack Developer (2)<br>- Database Administrator<br>- DevOps Engineer<br>- Technical Support (2) | 60-70% | Gaji dan tunjangan tim pemeliharaan selama 12 bulan |
| 2 | Biaya Infrastruktur | - Server/Cloud hosting<br>- Storage (S3-compatible)<br>- Bandwidth<br>- Backup storage<br>- Monitoring tools | 15-20% | Biaya operasional infrastruktur 12 bulan |
| 3 | Biaya Lisensi | - Software berlisensi (jika ada)<br>- SSL certificate<br>- Security tools<br>- Monitoring services | 3-5% | License renewal dan subscription |
| 4 | Biaya Operasional | - Transportasi<br>- Komunikasi<br>- Meeting & koordinasi<br>- Dokumentasi & pelaporan | 5-8% | Biaya operasional rutin |
| 5 | Biaya Lain-lain | - Kontingensi<br>- Emergency response<br>- Pelatihan<br>- Sertifikasi | 5-7% | Buffer untuk kebutuhan tak terduga |

### C. Tata Cara Pembayaran

**1. Mekanisme Pembayaran:**

Pembayaran dilakukan secara bertahap (termin) sebagai berikut:

| Termin | Waktu Pembayaran | Persentase | Syarat Pembayaran |
|--------|------------------|------------|-------------------|
| 1 | Bulan ke-1 | 15% | • Serah terima awal<br>• Berita Acara Handover<br>• Laporan bulan pertama |
| 2 | Bulan ke-2 | 8% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 3 | Bulan ke-3 | 8% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 4 | Bulan ke-4 | 8% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 5 | Bulan ke-5 | 8% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 6 | Bulan ke-6 | 8% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Evaluasi tengah periode<br>• Tidak ada sanksi |
| 7 | Bulan ke-7 | 7% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 8 | Bulan ke-8 | 7% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 9 | Bulan ke-9 | 7% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 10 | Bulan ke-10 | 7% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 11 | Bulan ke-11 | 7% | • Laporan bulanan lengkap<br>• System uptime ≥ 99%<br>• Tidak ada sanksi |
| 12 | Bulan ke-12 | 10% | • Laporan bulanan lengkap<br>• Laporan akhir komprehensif<br>• Serah terima akhir<br>• System uptime ≥ 99%<br>• Tidak ada outstanding issues<br>• Tidak ada sanksi<br>• Knowledge transfer selesai |

**Total: 100%**

**2. Dokumen Persyaratan Pembayaran:**

Setiap termin pembayaran harus dilengkapi dengan:
- Kuitansi bermaterai
- Faktur pajak (jika PKP)
- Berita Acara Pemeriksaan Pekerjaan
- Laporan sesuai periode (bulanan atau akhir)
- Bukti pemenuhan KPI periode terkait
- Surat pernyataan tidak ada sanksi yang belum diselesaikan
- SPTJM (Surat Pertanggungjawaban Mutlak) kebenaran dokumen

**3. Proses Verifikasi Pembayaran:**

1. Penyedia mengajukan tagihan dengan melampirkan dokumen lengkap
2. PPK melakukan verifikasi dokumen dan kinerja (maks 5 hari kerja)
3. Jika memenuhi syarat, PPK menerbitkan Berita Acara Pemeriksaan
4. Dokumen diteruskan ke Bendahara untuk proses pembayaran
5. Pembayaran dilakukan sesuai mekanisme APBD (maks 14 hari kerja setelah verifikasi)

**4. Pemotongan dan Pajak:**

Pembayaran akan dipotong:
- PPh Pasal 23 sebesar 2% (untuk jasa)
- PPN 11% (jika penyedia adalah PKP)
- Denda/sanksi (jika ada)

**5. Retensi:**

Tidak ada retensi khusus, namun:
- Pembayaran termin terakhir (10%) baru dilakukan setelah serah terima akhir
- Jaminan pemeliharaan tetap berlaku hingga +1 bulan setelah kontrak

---

## XII. KRITERIA EVALUASI KINERJA

Evaluasi kinerja penyedia akan dilakukan secara berkala berdasarkan parameter berikut:

### A. Key Performance Indicator (KPI)

| No | Indikator | Target | Bobot | Metode Pengukuran |
|----|-----------|--------|-------|-------------------|
| 1 | System Uptime | ≥ 99% | 25% | Monitoring tool log |
| 2 | Response Time | < 3 detik | 15% | Performance monitoring |
| 3 | Incident Resolution Time | Sesuai SLA | 20% | Ticketing system data |
| 4 | Data Synchronization Success | ≥ 98% | 15% | Sync log analysis |
| 5 | User Satisfaction | ≥ 4.0/5.0 | 10% | Survey triwulanan |
| 6 | Documentation Quality | Lengkap & up-to-date | 5% | Document review |
| 7 | Proactive Monitoring | 100% adherence | 5% | Monitoring checklist |
| 8 | Change Success Rate | ≥ 95% | 5% | Change management log |

### B. Penilaian Kinerja

**Kategori Nilai:**
- **Sangat Baik (90-100):** Bonus reputasi untuk pekerjaan selanjutnya
- **Baik (80-89):** Kinerja sesuai harapan
- **Cukup (70-79):** Perlu perbaikan, peringatan tertulis
- **Kurang (< 70):** Denda sesuai ketentuan kontrak

**Periode Evaluasi:**
- Evaluasi bulanan untuk KPI operasional
- Evaluasi triwulanan untuk kepuasan pengguna
- Evaluasi semesteran untuk kinerja keseluruhan
- Evaluasi akhir tahun untuk perpanjangan kontrak

---

## XIII. MANAJEMEN RISIKO

### A. Identifikasi Risiko

| No | Risiko | Dampak | Probabilitas | Mitigasi |
|----|--------|--------|--------------|----------|
| 1 | Perubahan API sumber data eksternal | Tinggi | Sedang | Monitoring API changes, adaptasi cepat, redundansi data source |
| 2 | Lonjakan traffic di akhir periode | Sedang | Tinggi | Auto-scaling, load balancing, cache optimization |
| 3 | Kehilangan data akibat kegagalan sistem | Tinggi | Rendah | Backup berkala, disaster recovery plan, redundant storage |
| 4 | Serangan keamanan siber | Tinggi | Sedang | Security hardening, regular patching, penetration testing |
| 5 | Ketergantungan pada personel kunci | Sedang | Sedang | Knowledge transfer, dokumentasi lengkap, backup team |
| 6 | Perubahan regulasi LKPP mendadak | Sedang | Sedang | Monitoring regulasi, arsitektur adaptif, consultation with LKPP |
| 7 | Keterbatasan anggaran pemeliharaan | Sedang | Rendah | Optimasi resource, prioritas fitur, cost control |
| 8 | Kegagalan infrastruktur cloud/hosting | Tinggi | Rendah | Multi-AZ deployment, disaster recovery site, SLA provider |

### B. Rencana Kontingensi

**1. Sistem Down Total (Severity: Critical)**
- Aktivasi tim emergency response dalam 30 menit
- Komunikasi ke semua stakeholder
- Rollback ke versi stabil terakhir
- Aktivasi disaster recovery jika diperlukan
- Post-mortem analysis wajib dilakukan

**2. Kegagalan Sinkronisasi Data (Severity: High)**
- Identifikasi sumber masalah (API down/format changed)
- Gunakan data cache terakhir
- Manual sync jika memungkinkan
- Koordinasi dengan LKPP jika masalah dari source
- Update user tentang delay data

**3. Performa Menurun (Severity: Medium)**
- Analisis bottleneck (query, cache, network)
- Optimasi query dan cache
- Scaling resource jika diperlukan
- Review dan refactoring code

---

## XIV. KETENTUAN SANKSI DAN DENDA

### A. Jenis Pelanggaran dan Sanksi

| No | Jenis Pelanggaran | Sanksi | Denda |
|----|-------------------|--------|-------|
| 1 | Uptime < 95% | Peringatan tertulis ke-1 | 0.5% nilai kontrak per bulan |
| 2 | Uptime < 90% | Peringatan tertulis ke-2 | 1% nilai kontrak per bulan |
| 3 | Uptime < 85% | Pemutusan kontrak | 5% nilai kontrak |
| 4 | Keterlambatan laporan bulanan > 5 hari | Peringatan tertulis | Rp 500.000 per hari |
| 5 | Tidak merespon insiden kritis > 2 jam | Peringatan tertulis | 0.1% nilai kontrak per kejadian |
| 6 | Kehilangan data tanpa backup | Pemutusan kontrak | 10% nilai kontrak + ganti rugi |
| 7 | Pelanggaran keamanan data | Pemutusan kontrak | Sesuai kerugian yang timbul |
| 8 | Ketidakhadiran meeting tanpa pemberitahuan | Teguran lisan | Rp 250.000 per kejadian |

### B. Mekanisme Pengenaan Sanksi

1. Identifikasi pelanggaran berdasarkan monitoring atau laporan
2. Verifikasi pelanggaran oleh PPK dan tim teknis
3. Pemberitahuan tertulis kepada penyedia (maks 3 hari kerja)
4. Kesempatan klarifikasi dari penyedia (2 hari kerja)
5. Keputusan final dari PPK
6. Pengenaan sanksi dan pemotongan pembayaran

### C. Ketentuan Force Majeure

Sanksi tidak diberlakukan untuk kondisi force majeure yang meliputi:
- Bencana alam (gempa bumi, banjir, kebakaran)
- Kerusuhan atau huru-hara
- Perang atau kondisi darurat nasional
- Kebijakan pemerintah yang berdampak langsung
- Gangguan infrastruktur dari pihak ketiga di luar kendali

**Syarat pengakuan force majeure:**
- Pemberitahuan dalam 2x24 jam sejak kejadian
- Bukti dokumentasi kejadian
- Upaya mitigasi yang telah dilakukan
- Persetujuan dari PPK

---

## XV. KRITERIA PENERIMAAN PEKERJAAN

### A. Kriteria Penerimaan Bulanan

Pekerjaan dinyatakan diterima setiap bulan jika memenuhi:

1. **Ketersediaan Sistem:**
   - Uptime mencapai target minimal 99%
   - Tidak ada downtime tidak terencana > 2 jam

2. **Penanganan Insiden:**
   - Semua insiden kritis terselesaikan sesuai SLA
   - Dokumentasi lengkap untuk setiap insiden

3. **Pelaporan:**
   - Laporan bulanan diserahkan tepat waktu
   - Laporan lengkap sesuai format yang ditentukan

4. **Sinkronisasi Data:**
   - Data tersinkronisasi sesuai jadwal
   - Data accuracy rate ≥ 98%

### B. Kriteria Penerimaan Akhir (Serah Terima Pekerjaan)

Pekerjaan dinyatakan selesai dan diterima jika memenuhi:

1. **Dokumen Serah Terima:**
   - Laporan akhir komprehensif
   - Dokumentasi sistem terupdate
   - Panduan operasional dan troubleshooting
   - Source code dan konfigurasi (jika ada perubahan)
   - Dokumentasi perubahan selama masa kontrak

2. **Knowledge Transfer:**
   - Pelatihan kepada tim internal
   - Sesi handover dengan dokumentasi
   - Transfer akses dan kredensial

3. **Kondisi Sistem:**
   - Sistem berjalan normal dan stabil
   - Tidak ada bug kritis yang outstanding
   - Semua fitur berfungsi sesuai spesifikasi
   - Backup data terbaru tersedia

4. **Administrasi:**
   - Semua laporan bulanan lengkap
   - Tidak ada sanksi yang belum diselesaikan
   - Berita Acara Serah Terima ditandatangani

### C. User Acceptance Test (UAT)

Untuk setiap perubahan signifikan atau enhancement:

1. **Persiapan UAT:**
   - Test case disusun bersama PPK
   - Environment testing disiapkan
   - Test data representatif

2. **Pelaksanaan UAT:**
   - Eksekusi test case oleh tim PPK
   - Dokumentasi hasil testing
   - Identifikasi bug/issue

3. **Kriteria Pass UAT:**
   - 100% critical test case passed
   - < 5% non-critical issues
   - Performance sesuai requirement

4. **Sign-off:**
   - Berita Acara UAT ditandatangani
   - Issue list untuk follow-up
   - Jadwal deployment ke production

---

## XVI. HAK DAN KEWAJIBAN

### A. Hak Penyedia Jasa

1. Menerima pembayaran sesuai kontrak dan jadwal yang disepakati
2. Mendapatkan akses ke sistem dan infrastruktur yang diperlukan
3. Mendapatkan informasi dan data yang diperlukan untuk pemeliharaan
4. Mengajukan perubahan lingkup pekerjaan jika ada perubahan requirement
5. Mendapatkan dukungan dari tim internal untuk koordinasi

### B. Kewajiban Penyedia Jasa

1. Melaksanakan pekerjaan sesuai KAK dan kontrak
2. Menjaga kerahasiaan data dan informasi
3. Menyediakan tenaga ahli sesuai kualifikasi yang dipersyaratkan
4. Membuat laporan berkala sesuai ketentuan
5. Bertanggung jawab atas kualitas pekerjaan
6. Mengikuti prosedur dan kebijakan yang berlaku
7. Memberikan garansi untuk pekerjaan yang dilakukan
8. Melakukan knowledge transfer di akhir periode

### C. Hak Pemberi Kerja (PPK)

1. Mendapatkan layanan pemeliharaan sesuai KAK
2. Meminta laporan dan dokumentasi pekerjaan
3. Melakukan evaluasi kinerja secara berkala
4. Meminta perubahan atau enhancement sesuai kebutuhan
5. Menolak pekerjaan yang tidak sesuai spesifikasi
6. Memberikan sanksi atas pelanggaran kontrak
7. Memutuskan kontrak jika terjadi pelanggaran serius

### D. Kewajiban Pemberi Kerja (PPK)

1. Melakukan pembayaran sesuai termin dan ketentuan
2. Menyediakan akses dan infrastruktur yang diperlukan
3. Memberikan informasi dan koordinasi yang dibutuhkan
4. Melakukan evaluasi secara objektif dan transparan
5. Menyediakan narasumber untuk konsultasi teknis

---

## XVII. KETENTUAN PERUBAHAN KONTRAK

### A. Addendum Kontrak

Perubahan terhadap kontrak dapat dilakukan melalui addendum dengan ketentuan:

1. **Perubahan yang Diizinkan:**
   - Perubahan lingkup pekerjaan minor (< 10% nilai kontrak)
   - Perubahan personel dengan kualifikasi setara atau lebih baik
   - Penyesuaian jadwal karena force majeure
   - Perubahan spesifikasi teknis karena regulasi baru
   - Penambahan/pengurangan fitur sesuai kebutuhan

2. **Prosedur Perubahan:**
   - Penyedia mengajukan permohonan tertulis dengan justifikasi
   - PPK melakukan kajian dan verifikasi
   - Negosiasi perubahan dan dampaknya
   - Persetujuan dari pejabat berwenang
   - Penandatanganan addendum kontrak
   - Sosialisasi perubahan kepada stakeholder

3. **Batasan Perubahan:**
   - Total perubahan maksimal 10% dari nilai kontrak awal
   - Tidak boleh merubah esensi/tujuan utama pekerjaan
   - Harus sesuai dengan peraturan pengadaan yang berlaku
   - Tidak boleh merugikan negara

### B. Perpanjangan Kontrak

1. **Ketentuan Perpanjangan:**
   - Perpanjangan dapat dilakukan maksimal 1 (satu) kali untuk periode 12 bulan
   - Syarat: Kinerja periode sebelumnya minimal kategori "Baik" (≥ 80)
   - Harus ada ketersediaan anggaran di tahun berikutnya
   - Didasarkan pada kebutuhan operasional yang berkelanjutan

2. **Prosedur Perpanjangan:**
   - Evaluasi kinerja menyeluruh di bulan ke-10
   - Rekomendasi perpanjangan dari PPK
   - Persetujuan dari pejabat berwenang
   - Negosiasi harga (jika ada penyesuaian)
   - Penerbitan SPK perpanjangan

### C. Pemutusan Kontrak

**1. Pemutusan oleh Pemberi Kerja:**

Kontrak dapat diputuskan sepihak oleh PPK jika:
- Penyedia cidera janji berat (uptime < 85% berturut-turut 2 bulan)
- Penyedia tidak mampu melanjutkan pekerjaan
- Penyedia melakukan pelanggaran serius (kehilangan data, breach keamanan)
- Penyedia pailit atau mengalami masalah hukum serius

Konsekuensi:
- Pencairan jaminan pemeliharaan
- Blacklist sesuai ketentuan LKPP
- Tuntutan ganti rugi jika ada kerugian negara
- Pekerjaan dilanjutkan oleh penyedia lain

**2. Pemutusan oleh Penyedia:**

Penyedia dapat mengajukan pemutusan jika:
- Pemberi kerja tidak melakukan pembayaran > 3 bulan berturut-turut tanpa alasan yang sah
- Force majeure yang berkepanjangan
- Perubahan lingkup pekerjaan yang fundamental tanpa penyesuaian kontrak

Prosedur:
- Pemberitahuan tertulis 30 hari sebelumnya
- Negosiasi penyelesaian
- Serah terima pekerjaan yang sudah dilakukan
- Pembayaran sesuai progres pekerjaan

**3. Pemutusan Bersama:**

Dapat dilakukan dengan kesepakatan kedua belah pihak dengan syarat:
- Tidak merugikan kepentingan negara
- Ada kompensasi yang adil untuk kedua belah pihak
- Dilakukan serah terima pekerjaan dengan baik

---

## XVIII. PENYELESAIAN PERSELISIHAN

### A. Hierarki Penyelesaian

**1. Musyawarah (Tingkat Pertama):**
- Perselisihan diselesaikan terlebih dahulu melalui musyawarah
- Melibatkan Project Manager dan PPK
- Waktu maksimal: 14 hari kerja
- Hasil dicatat dalam Berita Acara

**2. Mediasi (Tingkat Kedua):**
- Jika musyawarah gagal, dilakukan mediasi
- Melibatkan pejabat yang lebih tinggi dari kedua belah pihak
- Dapat melibatkan mediator independen
- Waktu maksimal: 30 hari kerja
- Hasil mediasi bersifat mengikat jika disepakati

**3. Arbitrase atau Pengadilan (Tingkat Ketiga):**
- Jika mediasi gagal, dapat ditempuh jalur arbitrase atau pengadilan
- Arbitrase melalui Badan Arbitrase Nasional Indonesia (BANI)
- Atau melalui Pengadilan Negeri di wilayah pemberi kerja
- Keputusan bersifat final dan mengikat

### B. Jenis Perselisihan

**1. Perselisihan Teknis:**
- Interpretasi spesifikasi teknis
- Kriteria penerimaan pekerjaan
- Performance metrics dan KPI
- Diselesaikan melalui expert judgment atau konsultan independen

**2. Perselisihan Komersial:**
- Pembayaran dan penagihan
- Denda dan sanksi
- Perubahan lingkup dan harga
- Diselesaikan sesuai ketentuan kontrak dan peraturan yang berlaku

**3. Perselisihan Force Majeure:**
- Pengakuan kondisi force majeure
- Dampak terhadap kewajiban para pihak
- Kompensasi atau perpanjangan waktu
- Diselesaikan dengan mempertimbangkan bukti dan kondisi faktual

### C. Prinsip Penyelesaian

1. **Itikad Baik:**
   - Kedua belah pihak wajib beritikad baik dalam penyelesaian
   - Mengutamakan kepentingan kelancaran pekerjaan
   - Menghindari tindakan yang merugikan pihak lain

2. **Transparansi:**
   - Semua informasi relevan diungkapkan
   - Dokumentasi lengkap dan akurat
   - Komunikasi terbuka dan jujur

3. **Win-Win Solution:**
   - Mencari solusi yang menguntungkan kedua belah pihak
   - Mempertimbangkan kepentingan jangka panjang
   - Menjaga hubungan baik

4. **Kepatuhan Hukum:**
   - Penyelesaian sesuai peraturan perundangan yang berlaku
   - Mempertimbangkan ketentuan pengadaan barang/jasa pemerintah
   - Tidak melanggar kode etik dan integritas

---

## XIX. LAMPIRAN

### Lampiran A: Format Laporan Bulanan

**LAPORAN PEMELIHARAAN APLIKASI SIP-SPSE**
**BULAN: [Bulan] TAHUN: [Tahun]**

**I. RINGKASAN EKSEKUTIF**
- Overview ketersediaan sistem bulan ini
- Highlight pencapaian dan isu utama
- Rekomendasi kunci

**II. STATISTIK SISTEM**
- Uptime/Downtime
- Response time rata-rata
- Jumlah pengguna aktif
- Volume data yang diproses

**III. AKTIVITAS PEMELIHARAAN**
- Preventive maintenance yang dilakukan
- Corrective maintenance (bug fixes)
- Adaptive maintenance (penyesuaian)
- Perfective maintenance (enhancement)

**IV. INSIDEN DAN PENANGANAN**
| No | Tanggal | Kategori | Deskripsi | Status | Waktu Resolusi |
|----|---------|----------|-----------|--------|----------------|
| | | | | | |

**V. SINKRONISASI DATA**
| Sumber | Frekuensi | Success Rate | Isu | Tindakan |
|--------|-----------|--------------|-----|----------|
| SIRUP | Harian | | | |
| SPSE | Harian | | | |
| SIKAP | Mingguan | | | |
| E-Katalog | Mingguan | | | |
| BELA | Mingguan | | | |

**VI. PERFORMA SISTEM**
- Grafik uptime
- Grafik response time
- Grafik penggunaan resource
- Analisis tren

**VII. RENCANA BULAN DEPAN**
- Scheduled maintenance
- Enhancement yang direncanakan
- Potensi risiko dan mitigasi

**VIII. LAMPIRAN**
- Screenshot monitoring
- Log insiden detail
- Dokumentasi perubahan

---

### Lampiran B: Format Berita Acara Serah Terima

**BERITA ACARA SERAH TERIMA PEKERJAAN**
**PEMELIHARAAN APLIKASI SIP-SPSE**

Pada hari ini [hari], tanggal [tanggal], bulan [bulan], tahun [tahun], yang bertanda tangan di bawah ini:

**PIHAK PERTAMA:**
Nama        : [Nama PPK]
Jabatan     : Pejabat Pembuat Komitmen
NIP         : [NIP]
Instansi    : [Nama SKPD]

Selanjutnya disebut sebagai **PIHAK PERTAMA**

**PIHAK KEDUA:**
Nama Perusahaan : [Nama Penyedia]
Direktur        : [Nama Direktur]
NPWP            : [NPWP]
Alamat          : [Alamat]

Selanjutnya disebut sebagai **PIHAK KEDUA**

Dengan ini menyatakan bahwa:

1. PIHAK KEDUA telah menyelesaikan pekerjaan sesuai kontrak
2. PIHAK PERTAMA telah memeriksa dan menerima hasil pekerjaan
3. Dokumentasi dan knowledge transfer telah dilaksanakan
4. Sistem berjalan normal dan stabil

**Dokumen yang diserahkan:**
- [ ] Laporan akhir pemeliharaan
- [ ] Dokumentasi teknis sistem
- [ ] Source code dan konfigurasi (jika ada perubahan)
- [ ] Panduan operasional
- [ ] Backup data terbaru
- [ ] Akses dan kredensial sistem

**Kondisi Sistem:**
- Uptime rata-rata periode kontrak: [...]%
- Status: Normal/Stabil
- Outstanding issues: [...]

Demikian Berita Acara ini dibuat untuk dipergunakan sebagaimana mestinya.

| PIHAK PERTAMA | PIHAK KEDUA |
|---------------|-------------|
| [TTD & Materai] | [TTD & Materai] |
| [Nama] | [Nama] |
| NIP. [...] | Direktur |

---

### Lampiran C: Service Level Agreement (SLA) Detail

**1. AVAILABILITY SLA**

| Metric | Target | Measurement | Penalty |
|--------|--------|-------------|---------|
| Monthly Uptime | ≥ 99.0% | Automated monitoring | 0.5% contract value per month below target |
| Quarterly Uptime | ≥ 99.2% | Automated monitoring | Additional 0.3% contract value |
| Annual Uptime | ≥ 99.5% | Automated monitoring | Performance review impact |

**Excluded from Uptime Calculation:**
- Scheduled maintenance windows (max 4 hours/month, notified 7 days prior)
- Force majeure events
- Issues caused by third-party systems (LKPP APIs)
- DDoS attacks or security incidents beyond control

**2. RESPONSE TIME SLA**

| Page Type | Target Response Time | Measurement Method |
|-----------|---------------------|-------------------|
| Dashboard Landing | < 2 seconds | 95th percentile |
| Data Tables | < 3 seconds | 95th percentile |
| Complex Reports | < 5 seconds | 95th percentile |
| Data Export | < 10 seconds | 95th percentile |

**3. INCIDENT RESPONSE SLA**

Detailed breakdown:

**Critical (P1):**
- Definition: Complete system outage, data loss risk, security breach
- Response Time: 30 minutes
- Resolution Time: 4 hours
- Communication: Immediate notification + hourly updates
- Escalation: Automatic escalation to management if not resolved in 2 hours

**High (P2):**
- Definition: Major feature not working, significant performance degradation
- Response Time: 1 hour
- Resolution Time: 8 hours
- Communication: Initial response + updates every 4 hours
- Escalation: Escalation if not resolved in 6 hours

**Medium (P3):**
- Definition: Minor feature issue, workaround available
- Response Time: 4 hours
- Resolution Time: 24 hours
- Communication: Acknowledgment + resolution update
- Escalation: Daily review if not resolved

**Low (P4):**
- Definition: Cosmetic issues, enhancement requests, questions
- Response Time: 8 hours (next business day)
- Resolution Time: 72 hours
- Communication: Email acknowledgment
- Escalation: Weekly review for backlog

**4. DATA SYNC SLA**

| Data Source | Sync Frequency | Success Rate | Max Delay | Alert Threshold |
|-------------|----------------|--------------|-----------|-----------------|
| SIRUP | Daily @ 02:00 | ≥ 99% | 6 hours | > 3 hours delay |
| SPSE Tender | Daily @ 03:00 | ≥ 98% | 6 hours | > 3 hours delay |
| SPSE Non-Tender | Daily @ 04:00 | ≥ 98% | 6 hours | > 3 hours delay |
| SIKAP | Weekly @ Sun 01:00 | ≥ 95% | 12 hours | > 6 hours delay |
| E-Katalog | Weekly @ Sun 02:00 | ≥ 95% | 12 hours | > 6 hours delay |
| BELA | Weekly @ Sun 03:00 | ≥ 95% | 12 hours | > 6 hours delay |

---

### Lampiran D: Daftar Perangkat dan Akses

**1. INFRASTRUKTUR SISTEM**

| Komponen | Spesifikasi | Lokasi | PIC |
|----------|-------------|--------|-----|
| Application Server | [...] | [...] | [...] |
| Database Server | [...] | [...] | [...] |
| Storage Server | [...] | [...] | [...] |
| Backup Server | [...] | [...] | [...] |

**2. AKSES SISTEM**

| Level Akses | Credential | Purpose | Holder |
|-------------|-----------|---------|--------|
| Server Root | SSH Key | Infrastructure management | DevOps Team |
| Database Admin | DB Credentials | Database operations | DBA |
| Application Admin | App Admin Panel | Application configuration | Tech Lead |
| Monitoring Access | Monitoring Dashboard | System monitoring | All Team |

**3. THIRD-PARTY SERVICES**

| Service | Provider | Purpose | Credentials Location |
|---------|----------|---------|---------------------|
| S3 Storage | [...] | Data storage | Password vault |
| CDN | [...] | Content delivery | Password vault |
| Monitoring | [...] | System monitoring | Password vault |
| Backup Service | [...] | Data backup | Password vault |

---

### Lampiran E: Checklist Preventive Maintenance

**HARIAN:**
- [ ] Cek status uptime dan availability
- [ ] Review error logs untuk anomali
- [ ] Monitor response time dan performa
- [ ] Verifikasi proses sinkronisasi data berjalan
- [ ] Cek kapasitas disk dan resource usage
- [ ] Review security logs untuk aktivitas mencurigakan

**MINGGUAN:**
- [ ] Review dan analisis tren performa
- [ ] Optimasi cache dan cleanup data temporary
- [ ] Backup verification dan restore test
- [ ] Review pending tickets dan prioritas
- [ ] Update dokumentasi jika ada perubahan
- [ ] Security scan dan vulnerability check

**BULANAN:**
- [ ] Full system health check
- [ ] Database optimization (vacuum, analyze, reindex)
- [ ] Review dan rotate log files
- [ ] Test disaster recovery procedure
- [ ] Update dependencies dan security patches
- [ ] Capacity planning review
- [ ] Generate monthly report
- [ ] Stakeholder meeting dan review

**TRIWULANAN:**
- [ ] Comprehensive security audit
- [ ] User satisfaction survey
- [ ] Performance benchmark testing
- [ ] Documentation review dan update
- [ ] Training refresher untuk tim
- [ ] Disaster recovery drill

**SEMESTERAN:**
- [ ] Architecture review
- [ ] Capacity planning untuk 6 bulan kedepan
- [ ] Major version updates evaluation
- [ ] Business continuity plan review
- [ ] Contract compliance audit

---

### Lampiran F: Prosedur Eskalasi

**TINGKAT ESKALASI:**

**Level 1: Technical Support**
- First responder untuk semua insiden
- Handle P3 dan P4 independently
- Eskalasi P1 dan P2 jika tidak dapat resolve dalam 30 menit
- Contact: [Email/Phone]

**Level 2: Senior Developer/Engineer**
- Handle P1 dan P2 incidents
- Technical consultation untuk P3/P4
- Eskalasi ke Level 3 jika masalah kompleks atau P1 tidak resolve dalam 2 jam
- Contact: [Email/Phone]

**Level 3: Technical Lead/Architect**
- Handle critical issues yang memerlukan architectural decisions
- Coordinate dengan external parties (LKPP, hosting provider)
- Decision making untuk major changes
- Contact: [Email/Phone]

**Level 4: Project Manager**
- Overall project coordination
- Client communication untuk major incidents
- Contract dan commercial issues
- Contact: [Email/Phone]

**Level 5: Management (Both Sides)**
- Critical decisions affecting business continuity
- Force majeure situations
- Contract disputes
- Contact: [Email/Phone PPK] & [Email/Phone Vendor Management]

**ESKALASI PATH:**

```
P4 (Low)     : L1 ━━━━━━━━━━━━━━━━━━━━━━━━━━→ Resolution

P3 (Medium)  : L1 ━━━━━━━━━━━━━━━━━━━━━━━━━━→ Resolution
                ↓ (if needed)
               L2

P2 (High)    : L1 ━→ L2 ━━━━━━━━━━━━━━━━━━━→ Resolution
                      ↓ (if needed)
                     L3

P1 (Critical): L1 ━→ L2 ━→ L3 ━━━━━━━━━━━━→ Resolution
                           ↓ (if needed)
                          L4 ━→ L5
```

---

## XX. PENUTUP

Kerangka Acuan Kerja ini disusun sebagai pedoman dalam pelaksanaan kegiatan Pemeliharaan Aplikasi SIP-SPSE Tahun Anggaran 2025. Hal-hal yang belum diatur dalam KAK ini akan diatur kemudian sesuai dengan ketentuan yang berlaku dan berdasarkan kesepakatan bersama antara Pemberi Kerja dan Penyedia Jasa.

KAK ini merupakan dokumen yang mengikat dan menjadi acuan utama dalam pelaksanaan pekerjaan. Perubahan terhadap KAK ini hanya dapat dilakukan melalui addendum yang disepakati oleh kedua belah pihak dan sesuai dengan peraturan yang berlaku.

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
