# Sistem Informasi Pelaporan Pengadaan Barang dan Jasa (SIP-2025)

Aplikasi berbasis web untuk monitoring dan pelaporan pengadaan barang dan jasa pemerintah daerah di Indonesia, khususnya di Kalimantan Barat. Aplikasi ini dikembangkan menggunakan Streamlit dan didesain untuk memudahkan proses monitoring pengadaan barang dan jasa dari tahap perencanaan hingga pelaksanaan.

## Fitur Utama

Aplikasi ini terbagi menjadi tiga modul utama:

### 1. Modul Rencana dan Persiapan
- **Rencana Pengadaan (RUP)**: Monitoring rencana umum pengadaan, termasuk profil RUP, struktur anggaran, paket penyedia, paket swakelola, dan persentase input RUP.
- **Persiapan Pengadaan**: Fitur untuk memantau persiapan pengadaan barang dan jasa.

### 2. Modul Proses Pengadaan
- **Tender**: Monitoring proses tender dari pengumuman hingga BAPBAST.
- **Non Tender**: Monitoring proses pengadaan non tender.
- **Pencatatan**: Monitoring proses pencatatan langsung.
- **E-Katalog**: Monitoring pengadaan melalui E-Katalog (versi 5 dan 6).
- **Toko Daring**: Monitoring pengadaan melalui toko daring.
- **Peserta Tender**: Analisis peserta tender.

### 3. Modul Monitoring
- **ITKP**: Indikator Tata Kelola Pengadaan.
- **Nilai SIKAP**: Monitoring nilai SIKAP penyedia.
- **Jenis Belanja**: Analisis berdasarkan jenis belanja.

## Teknologi yang Digunakan

- **Streamlit**: Framework utama untuk membangun aplikasi web interaktif.
- **DuckDB**: Database analitik in-memory untuk pemrosesan data cepat.
- **Pandas & Polars**: Library untuk manipulasi dan analisis data.
- **Plotly Express**: Visualisasi data interaktif.
- **Streamlit AgGrid**: Komponen tabel interaktif.
- **Babel**: Untuk format mata uang.

## Instalasi dan Penggunaan

### Prasyarat
- Python 3.8 atau lebih baru
- pip (Python package installer)

### Langkah Instalasi

1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/SIP-2025.git
   cd SIP-2025
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Buka browser dan akses `http://localhost:8501`

## Struktur Data

Aplikasi ini menggunakan data dari beberapa sumber:
- Data RUP (Rencana Umum Pengadaan) dari SIRUP
- Data SPSE (Sistem Pengadaan Secara Elektronik) dari LPSE
- Data struktur anggaran dari sistem keuangan daerah

Data disimpan dalam format Parquet dan diakses melalui URL S3 dengan pola:
- RUP: `https://s3-sip.pbj.my.id/rup/{kodeRUP}/...`
- SPSE: `https://s3-sip.pbj.my.id/spse/{kodeLPSE}/...`

## Konfigurasi Daerah

Aplikasi mendukung beberapa daerah di Kalimantan Barat, termasuk:
- Provinsi Kalimantan Barat
- Kota Pontianak
- Kabupaten Kubu Raya
- Kabupaten Mempawah
- Kota Singkawang
- Dan daerah lainnya

## Kontribusi

Kontribusi untuk pengembangan aplikasi ini sangat diterima. Silakan buat pull request atau laporkan masalah melalui issue tracker.

## Lisensi

[Masukkan informasi lisensi di sini]

## Kontak

[Masukkan informasi kontak di sini] 