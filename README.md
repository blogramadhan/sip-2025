# SIP-2025 – Sistem Informasi Pelaporan Pengadaan Barang dan Jasa

![SIP-2025](public/sip-spse.png)

Dashboard Streamlit untuk monitoring dan pelaporan pengadaan barang/jasa pemerintah daerah Kalimantan Barat beserta dua mitra eksternal. SIP-2025 menyatukan data RUP, SPSE, E-Katalog, Toko Daring, dan SiKAP menjadi visualisasi interaktif serta laporan siap unduh.

## Daftar Isi

- [Tentang SIP-2025](#tentang-sip-2025)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Fitur Utama](#fitur-utama)
- [Modul dan Navigasi](#modul-dan-navigasi)
- [Sumber Data dan Refresh](#sumber-data-dan-refresh)
- [Daerah & Kode Integrasi](#daerah--kode-integrasi)
- [Struktur Proyek](#struktur-proyek)
- [Prasyarat](#prasyarat)
- [Instalasi & Menjalankan Aplikasi](#instalasi--menjalankan-aplikasi)
- [Konfigurasi Tambahan](#konfigurasi-tambahan)
- [Workflow Ekspor & Pelaporan](#workflow-ekspor--pelaporan)
- [Pengembangan & Roadmap](#pengembangan--roadmap)
- [Kontribusi](#kontribusi)
- [Lisensi & Kontak](#lisensi--kontak)
- [Ucapan Terima Kasih](#ucapan-terima-kasih)

## Tentang SIP-2025

SIP-2025 membantu Unit Kerja Pengadaan Barang/Jasa (UKPBJ) memantau progres pengadaan dari perencanaan hingga evaluasi. Data diproses secara periodik dan ditampilkan sebagai kartu metrik, grafik Plotly, serta tabel interaktif AgGrid dengan opsi ekspor ke Excel.

### Sasaran Pengguna & Kasus Penggunaan

- Pejabat Pengadaan & PPK – memantau RUP, tender, dan realisasi kontrak.
- Kepala Perangkat Daerah – memastikan capaian belanja PDN, UKM, dan ITKP.
- Auditor dan inspektorat – mengawasi tata kelola serta konsistensi data lintas sistem.
- Analis data – mengunduh dataset ter-filter untuk analisis lanjutan di Excel/BI.

### Kapabilitas Data

- Cakupan tahun berjalan + dua tahun sebelumnya.
- Data historis snapshot (31 Maret) untuk baseline perbandingan indikator.
- Penyimpanan Parquet di storage kompatibel S3 (`https://s3-sip.pbj.my.id`).
- Caching Streamlit (`@st.cache_data`) selama 6 jam agar akses cepat.

## Arsitektur Sistem

```
Pengguna → Streamlit UI (streamlit_app.py)
          → Module Page (src/rencana|proses|monitoring)
          → Fungsi utilitas (fungsi.py: cache, region_config, download)
          → DuckDB in-memory engine
          → S3-compatible parquet objects (RUP, SPSE, SiKAP, Katalog, Daring)
```

- **Front-end:** Streamlit multipage dengan sidebar filter daerah/tahun.
- **Pengolahan:** DuckDB mengeksekusi query SQL pada Parquet langsung di memori.
- **Visualisasi:** Plotly Express untuk grafik, Streamlit AgGrid untuk tabel interaktif.
- **Ekspor:** `download_excel` menghasilkan file Excel siap kirim.

## Fitur Utama

### 1. Dashboard Interaktif
- Filter per daerah, tahun anggaran, sumber dana, status PDN/UKM, dan perangkat daerah.
- Card metrik otomatis & gaya konsisten menggunakan `streamlit_extras.metric_cards`.
- Grafik pie/bar dinamika pagu, HPS, serta TOP 10 kategori.

### 2. Analitik Proses Pengadaan
- Tender & Non-Tender lengkap 5 tahapan (Pengumuman → BAST).
- Monitoring E-Katalog v5/v6, Toko Daring BELA, dan pencatatan langsung.
- Analisis peserta tender (ukuran usaha, persebaran penyedia, status SIKaP).

### 3. Monitoring Tata Kelola
- Prediksi ITKP berbasis rasio RUP vs realisasi elektronik.
- Nilai SiKAP penyedia pada tender/non-tender.
- Profil belanja menurut jenis belanja & PDN.

### 4. Ekspor dan Pelaporan
- Unduh Excel sesuai filter aktif (nama file otomatis `Modul-Daerah-Tahun.xlsx`).
- Format mata uang Rupiah dengan Babel.
- Data siap pakai untuk bahan paparan atau audit.

### 5. Multi-Regional & Skalabilitas
- 15 daerah sudah terkonfigurasi (lihat tabel di bawah).
- Penambahan daerah cukup mengubah `region_config()` tanpa refactor modul.
- Dukungan lazy load Parquet + DuckDB memungkinkan jutaan baris.

## Modul dan Navigasi

| Kategori | Halaman (Streamlit) | File | Ringkasan | Dataset Utama |
| --- | --- | --- | --- | --- |
| Rencana | 📋 Rencana Pengadaan | `src/rencana/rup.py` | Konsolidasi paket penyedia & swakelola SIRUP, baseline anggaran & pagu per satker. | `RUP-PaketPenyedia-Terumumkan`, `RUP-PaketSwakelola`, `RUP-StrukturAnggaranPD` |
| Proses | 🏆 Tender | `src/proses/tender.py` | Analisis tender SPSE dari pengumuman sampai BAST, lengkap filter PDN/UKM. | `SPSE-TenderPengumuman`, `SPSE-TenderSelesai`, `SPSE-TenderEkontrak-*` |
| Proses | 📄 Non Tender | `src/proses/nontender.py` | Pemantauan Pengadaan Langsung / Penunjukan langsung. | `SPSE-NonTenderPengumuman`, `SPSE-NonTenderEkontrak-*` |
| Proses | ✏️ Pencatatan | `src/proses/pencatatan.py` | Transaksi pencatatan langsung SPSE (pagu kecil, swakelola). | `SPSE-Pencatatan*` |
| Proses | 🏪 E-Katalog v5 | `src/proses/ekatalog.py` | Paket e-purchasing katalog nasional v5. | `Ecat-PaketEPurchasing`, `Ecat-InstansiSatker` |
| Proses | 🛍️ E-Katalog v6 | `src/proses/ekatalogv6.py` | Adopsi katalog terbaru dengan data vendor & status transaksi. | `Ecatv6-*` (folder `katalog/`) |
| Proses | 🏪 Toko Daring | `src/proses/tokodaring.py` | Monitoring BELA Pengadaan (Toko Daring). | `Bela-TokoDaringRealisasi` |
| Proses | 👥 Peserta Tender | `src/proses/pesertatender.py` | Statistik peserta, jenis usaha, persebaran wilayah, status SIKaP. | `SPSE-PesertaTender` + `SIKaP-PenilaianKinerja` |
| Monitoring | 📈 ITKP | `src/monitoring/itkp.py` | Prediksi nilai ITKP per aspek RUP, e-tendering, non e-tendering, e-purchasing, toko daring. | Kombinasi RUP/SPSE/Ecat/Bela/SIKaP |
| Monitoring | ⭐ Nilai SiKAP | `src/monitoring/nilaisikap.py` | Skor kinerja penyedia tender & non-tender. | `SIKaP-PenilaianKinerjaPenyedia-*` |
| Monitoring | 💰 Jenis Belanja | `src/monitoring/jenisbelanja.py` | Komposisi belanja modal/barang/jasa, PDN vs non-PDN. | `RUP-StrukturAnggaranPD`, `SPSE-*` |

> **Catatan:** `src/rencana/sipraja.py` disiapkan untuk modul persiapan pengadaan dan dapat diaktifkan kembali dari `streamlit_app.py` bila data tersedia.

## Sumber Data dan Refresh

| Kategori | Lokasi Bucket | Frekuensi | Catatan |
| --- | --- | --- | --- |
| RUP (Penyedia, Swakelola, Struktur Anggaran) | `https://s3-sip.pbj.my.id/rup/{kodeRUP}/.../data.parquet` | Harian / saat sinkronisasi SIRUP | Snapshot 31 Maret tersedia (`data31.parquet`) untuk analisis historis. |
| SPSE Tender / Non Tender | `https://s3-sip.pbj.my.id/spse/{kodeLPSE}/SPSE-*/{tahun}/data.parquet` | Harian | Folder per tahapan (Pengumuman, Selesai, SPPBJ, Kontrak, SPMK, BAST). |
| Pencatatan Langsung | `spse/{kodeLPSE}/SPSE-Pencatatan*` | Harian | Dipakai modul Pencatatan. |
| SiKAP | `sikap/{kodeRUP}/SiKAP-*` | Mingguan | Digabung untuk metrik kinerja penyedia. |
| E-Katalog v5/v6 | `katalog/{kodeRUP}/Ecat-*` | Mingguan | Mengandung detail paket, satker, vendor, status transaksi. |
| BELA / Toko Daring | `daring/{kodeRUP}/Bela-TokoDaringRealisasi` | Mingguan | Status verifikasi dan konfirmasi PPMSE. |

Semua dataset dikonsumsi langsung dalam format Parquet melalui DuckDB tanpa ETL tambahan, sehingga struktur kolom mengikuti sumber resmi LKPP.

## Daerah & Kode Integrasi

| Daerah | Folder | Kode RUP | Kode LPSE |
| --- | --- | --- | --- |
| PROV. KALBAR | `prov` | D197 | 97 |
| KOTA PONTIANAK | `ptk` | D199 | 62 |
| KAB. KUBU RAYA | `kkr` | D202 | 188 |
| KAB. MEMPAWAH | `mpw` | D552 | 118 |
| KOTA SINGKAWANG | `skw` | D200 | 132 |
| KAB. BENGKAYANG | `bky` | D206 | 444 |
| KAB. LANDAK | `ldk` | D205 | 496 |
| KAB. SANGGAU | `sgu` | D204 | 298 |
| KAB. SEKADAU | `skd` | D198 | 175 |
| KAB. MELAWI | `mlw` | D210 | 540 |
| KAB. SINTANG | `stg` | D211 | 345 |
| KAB. KAPUAS HULU | `kph` | D209 | 488 |
| KAB. KETAPANG | `ktp` | D201 | 110 |
| KAB. TANGGERANG | `tgr` | D050 | 333 |
| KAB. KATINGAN | `ktg` | D236 | 438 |

Penambahan daerah cukup dengan menambah entri baru pada `region_config()` di `fungsi.py`.

## Struktur Proyek

```text
SIP-2025/
├── streamlit_app.py          # Entry point & konfigurasi multipage
├── fungsi.py                 # Utilitas: cache, logo, region config, ekspor
├── requirements.txt
├── public/                   # Asset logo
├── src/
│   ├── rencana/
│   │   ├── rup.py
│   │   └── sipraja.py
│   ├── proses/
│   │   ├── tender.py
│   │   ├── nontender.py
│   │   ├── pencatatan.py
│   │   ├── ekatalog.py
│   │   ├── ekatalogv6.py
│   │   ├── tokodaring.py
│   │   └── pesertatender.py
│   └── monitoring/
│       ├── itkp.py
│       ├── nilaisikap.py
│       └── jenisbelanja.py
└── .streamlit/config.toml    # Tema & opsi server
```

## Prasyarat

- Python 3.10 atau lebih baru (disarankan 3.12 sesuai `.venv` lokal).
- Pip modern (>=23).
- Akses ke bucket `s3-sip.pbj.my.id` atau mirror internal.
- (Opsional) Google Cloud Storage / S3 credentials jika bucket privat.

## Instalasi & Menjalankan Aplikasi

1. **Kloning repositori**
   ```bash
   git clone <repo-url>
   cd SIP-2025
   ```
2. **Buat virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **Instal dependensi**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **(Opsional) sesuaikan tema di `.streamlit/config.toml`.**
5. **Jalankan Streamlit**
   ```bash
   streamlit run streamlit_app.py
   ```
6. **Akses aplikasi** melalui `http://localhost:8501`. Pilih daerah & tahun di sidebar untuk mulai eksplorasi.

> Jika bucket berada di jaringan privat, pastikan koneksi VPN aktif sebelum menjalankan aplikasi.

## Konfigurasi Tambahan

- **Tema & Layout:** atur di `.streamlit/config.toml` (mode dark sudah diset default).
- **Penyesuaian Daerah:** ubah `region_config()` pada `fungsi.py`.
- **Caching:** TTL cache 6 jam (`@st.cache_data(ttl=21600)`). Atur sesuai kebutuhan dengan mengubah parameter dekorator.
- **Logo:** gunakan `logo()` pada `fungsi.py`. Ganti URL logo sesuai branding instansi.
- **Port / Headless:** set environment `STREAMLIT_SERVER_PORT`, `STREAMLIT_HEADLESS=true`, dll saat deploy.

## Workflow Ekspor & Pelaporan

1. Terapkan filter pada modul (contoh: Tender → status PDN “TKDN >= 40%”).
2. Gunakan tombol unduh di kanan atas tabel untuk menghasilkan Excel.
3. Nama file otomatis memuat jenis modul, daerah, dan tahun.
4. File siap dikirim ke pimpinan/auditor tanpa pembersihan tambahan karena:
   - Kolom mata uang sudah diformat Rupiah.
   - Terdapat metadata filter pada teks deskripsi sebelum tabel.

## Pengembangan & Roadmap

- [ ] Integrasi API LKPP real-time untuk mengurangi ketergantungan pada dump Parquet.
- [ ] Ekspor PDF / PPT untuk bahan paparan cepat.
- [ ] Personalisasi dashboard per role (PPK, Pokja, Auditor).
- [ ] Notifikasi real-time (email/WhatsApp) saat terjadi deviasi indikator.
- [ ] Responsif mobile + mode kiosk.
- [ ] Multi-bahasa (ID/EN) untuk audiens nasional.
- [ ] Role-based access control berbasis akun Streamlit/Keycloak.
- [ ] Modul analitik lanjutan (forecasting belanja, deteksi anomali).

Silakan tambah item roadmap lain pada bagian ini saat kebutuhan baru muncul.

## Kontribusi

1. Fork repositori kemudian buat branch fitur (`git checkout -b feature/nama-fitur`).
2. Terapkan perubahan dan sertakan deskripsi jelas pada kode/README.
3. Jalankan `streamlit run streamlit_app.py` untuk uji manual di setiap modul yang terdampak.
4. Pastikan tidak menghapus cache penting atau konfigurasi daerah.
5. Kirim Pull Request disertai:
   - Ringkasan perubahan.
   - Screenshot sebelum/sesudah (jika UI).
   - Panduan reproduksi untuk reviewer.

Bug report atau permintaan fitur: gunakan GitHub Issues dengan templat *bug/feature*, sertakan OS, versi Python, langkah reproduksi, serta screenshot/log relevan.

## Lisensi & Kontak

- Proyek ini saat ini digunakan secara internal oleh Pemerintah Provinsi Kalimantan Barat dan belum memiliki lisensi publik. Silakan hubungi pengelola apabila memerlukan penyesuaian lisensi.
- Untuk dukungan teknis, gunakan kanal komunikasi resmi UKPBJ (helpdesk internal, email dinas, atau tiket GitHub Issues) sesuai kebijakan organisasi.

## Ucapan Terima Kasih

- LKPP atas akses data SPSE, SIRUP, SiKAP, dan E-Katalog.
- Pemerintah Daerah Kalimantan Barat dan mitra kabupaten/kota atas kolaborasi data.
- Komunitas Streamlit & kontributor open-source lain yang dimanfaatkan di proyek ini.

---

**Versi Dokumen:** 2025-03  
**Status Proyek:** Active Development  
**Made with ❤️ untuk tata kelola pengadaan yang lebih transparan.**
