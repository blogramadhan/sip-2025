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

Aplikasi SIP-SPSE telah beroperasi dan melayani kebutuhan monitoring pengadaan untuk 15 (lima belas) wilayah di lingkungan Pemerintah Provinsi Kalimantan Barat dan Kabupaten/Kota mitra. Untuk menjamin keberlangsungan operasional sistem, keamanan data, serta peningkatan kualitas layanan secara berkelanjutan, diperlukan kegiatan pemeliharaan aplikasi yang terencana dan sistematis.

Berdasarkan hal tersebut, perlu disusun Kerangka Acuan Kerja (KAK) sebagai pedoman pelaksanaan kegiatan Pemeliharaan Aplikasi SIP-SPSE Tahun Anggaran 2025.

---

## II. DASAR HUKUM

1. Undang-Undang Nomor 11 Tahun 2008 tentang Informasi dan Transaksi Elektronik sebagaimana telah diubah dengan Undang-Undang Nomor 19 Tahun 2016;
2. Peraturan Presiden Nomor 12 Tahun 2021 tentang Perubahan atas Peraturan Presiden Nomor 16 Tahun 2018 tentang Pengadaan Barang/Jasa Pemerintah;
3. Peraturan Presiden Nomor 95 Tahun 2018 tentang Sistem Pemerintahan Berbasis Elektronik;
4. Peraturan LKPP Nomor 12 Tahun 2021 tentang Pedoman Pelaksanaan Pengadaan Barang/Jasa Pemerintah Melalui Penyedia;
5. Peraturan Daerah Provinsi Kalimantan Barat tentang Anggaran Pendapatan dan Belanja Daerah Tahun Anggaran 2025.

---

## III. MAKSUD DAN TUJUAN

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

## IV. RUANG LINGKUP PEKERJAAN

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

**1. Modul Rencana Pengadaan:**
- RUP (Rencana Umum Pengadaan) - Konsolidasi data SIRUP termasuk paket penyedia, paket swakelola, struktur anggaran, dan alokasi per satuan kerja.

**2. Modul Proses Pengadaan:**
- Tender - Analisis siklus tender elektronik (pengumuman hingga BAST)
- Non Tender - Monitoring pengadaan langsung dan penunjukan langsung
- Pencatatan - Tracking pencatatan transaksi di SPSE
- E-Katalog v5 - Monitoring paket e-purchasing katalog nasional (legacy)
- E-Katalog v6 - Monitoring katalog modern dengan detail vendor dan status transaksi
- Toko Daring - Monitoring marketplace online BELA
- Peserta Tender - Analisis statistik peserta lelang, distribusi, dan status SIKaP

**3. Modul Monitoring:**
- ITKP (Indikator Tata Kelola Pengadaan) - Prediksi indikator kinerja pengadaan
- Nilai SIKAP - Tampilan skor kinerja penyedia
- Jenis Belanja - Analisis komposisi belanja (modal/barang/jasa, PDN vs non-PDN)

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

## V. SPESIFIKASI TEKNIS

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

---

## VI. KELUARAN (OUTPUT)

Keluaran yang diharapkan dari kegiatan pemeliharaan ini adalah:

| No | Keluaran | Keterangan |
|----|----------|------------|
| 1 | Laporan Bulanan Pemeliharaan | Dokumentasi aktivitas pemeliharaan setiap bulan |
| 2 | Laporan Insiden | Dokumentasi setiap insiden dan penanganannya |
| 3 | Log Perubahan Sistem | Catatan setiap perubahan/update yang dilakukan |
| 4 | Dokumentasi Teknis Terbaru | Update dokumentasi sistem jika ada perubahan |
| 5 | Backup Data | Backup berkala sesuai jadwal yang ditetapkan |
| 6 | Laporan Akhir Pemeliharaan | Laporan komprehensif di akhir periode kontrak |

---

## VII. JANGKA WAKTU PELAKSANAAN

Jangka waktu pelaksanaan kegiatan pemeliharaan adalah **12 (dua belas) bulan kalender** terhitung sejak Surat Perintah Kerja (SPK) diterbitkan.

| Tahap | Kegiatan | Waktu |
|-------|----------|-------|
| 1 | Serah Terima dan Handover | Bulan ke-1 (minggu 1-2) |
| 2 | Operasional Pemeliharaan | Bulan ke-1 s.d. ke-12 |
| 3 | Laporan Bulanan | Setiap akhir bulan |
| 4 | Evaluasi Tengah Periode | Bulan ke-6 |
| 5 | Serah Terima Akhir | Bulan ke-12 (minggu terakhir) |

---

## VIII. KUALIFIKASI PENYEDIA

### A. Persyaratan Administrasi

1. Berbadan hukum dan memiliki izin usaha yang masih berlaku;
2. Memiliki NPWP dan telah memenuhi kewajiban perpajakan tahun terakhir;
3. Tidak masuk dalam daftar hitam LKPP;
4. Memiliki pengalaman minimal 2 (dua) tahun dalam pemeliharaan aplikasi berbasis web.

### B. Persyaratan Teknis

1. Memiliki tenaga ahli dengan kompetensi:

| No | Posisi | Kualifikasi | Jumlah |
|----|--------|-------------|--------|
| 1 | Project Manager | S1 Teknik Informatika/SI, pengalaman min. 5 tahun | 1 orang |
| 2 | Full Stack Developer | S1 Teknik Informatika/SI, menguasai Python, Streamlit | 2 orang |
| 3 | Database Administrator | S1 Teknik Informatika/SI, menguasai DuckDB, SQL | 1 orang |
| 4 | DevOps Engineer | S1 Teknik Informatika/SI, menguasai Docker, Linux | 1 orang |
| 5 | Technical Support | D3/S1 Teknik Informatika/SI | 2 orang |

2. Memiliki pemahaman tentang sistem pengadaan barang/jasa pemerintah (SPSE, SIRUP, SIKAP);
3. Memiliki kemampuan dalam pengembangan dashboard dan visualisasi data;
4. Memiliki sertifikasi atau bukti kompetensi yang relevan.

---

## IX. METODE PELAKSANAAN

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

---

## X. PEMBIAYAAN

Biaya pemeliharaan aplikasi SIP-SPSE dibebankan pada:

- **Mata Anggaran:** [Disesuaikan dengan DPA]
- **Program:** [Disesuaikan dengan DPA]
- **Kegiatan:** [Disesuaikan dengan DPA]
- **Tahun Anggaran:** 2025

Rincian komponen biaya:

| No | Komponen | Keterangan |
|----|----------|------------|
| 1 | Biaya Tenaga Ahli | Gaji tim pemeliharaan |
| 2 | Biaya Infrastruktur | Server, storage, bandwidth |
| 3 | Biaya Lisensi | Software berlisensi (jika ada) |
| 4 | Biaya Operasional | Transportasi, komunikasi |
| 5 | Biaya Lain-lain | Kontingensi |

---

## XI. PENUTUP

Kerangka Acuan Kerja ini disusun sebagai pedoman dalam pelaksanaan kegiatan Pemeliharaan Aplikasi SIP-SPSE Tahun Anggaran 2025. Hal-hal yang belum diatur dalam KAK ini akan diatur kemudian sesuai dengan ketentuan yang berlaku.

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
