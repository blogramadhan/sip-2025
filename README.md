# SIP-2025 - Sistem Informasi Pelaporan Pengadaan Barang dan Jasa

![SIP-2025](public/sip-spse.png)

Dashboard monitoring dan pelaporan pengadaan barang dan jasa berbasis web untuk pemerintah daerah di Kalimantan Barat. Aplikasi ini menyediakan analisis real-time, visualisasi interaktif, dan pelaporan komprehensif untuk proses pengadaan dari tahap perencanaan hingga pelaksanaan.

## Daftar Isi

- [Tentang Aplikasi](#tentang-aplikasi)
- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Struktur Proyek](#struktur-proyek)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Modul Aplikasi](#modul-aplikasi)
- [Sumber Data](#sumber-data)
- [Daerah yang Didukung](#daerah-yang-didukung)
- [Konfigurasi](#konfigurasi)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Tentang Aplikasi

**SIP-2025** adalah aplikasi dashboard berbasis web yang dikembangkan untuk memantau dan melaporkan pengadaan barang dan jasa pemerintah daerah di Kalimantan Barat. Aplikasi ini mengintegrasikan data dari berbagai sumber seperti SIRUP, SPSE, E-Katalog, dan Toko Daring untuk memberikan gambaran menyeluruh tentang status pengadaan.

### Tujuan

- Meningkatkan transparansi proses pengadaan barang dan jasa
- Menyediakan data real-time untuk pengambilan keputusan
- Memudahkan monitoring dan evaluasi kinerja pengadaan
- Mendukung tata kelola pengadaan yang lebih baik
- Memfasilitasi pelaporan yang cepat dan akurat

### Target Pengguna

- Pejabat pengadaan barang dan jasa
- Kepala Perangkat Daerah
- Unit Layanan Pengadaan (ULP)
- Auditor dan pengawas pengadaan
- Stakeholder pengadaan pemerintah

## Fitur Utama

### 1. Dashboard Interaktif
- Visualisasi data real-time dengan grafik interaktif
- Filter data berdasarkan perangkat daerah, tahun, dan berbagai parameter
- Metric cards dengan indikator kinerja utama
- Tabel data dengan fitur sorting dan filtering

### 2. Ekspor Data
- Download data dalam format Excel
- Nama file otomatis dengan timestamp
- Formatting mata uang dalam Rupiah
- Data terstruktur dan siap untuk analisis lanjutan

### 3. Multi-Regional Support
- Mendukung 14 pemerintah daerah di Kalimantan Barat
- Switching region yang mudah melalui sidebar
- Konfigurasi regional yang fleksibel

### 4. Analisis Mendalam
- Analisis berdasarkan berbagai dimensi (sumber dana, metode pemilihan, status UKM, dll.)
- Tracking 5 tahapan proses tender/non-tender
- Perbandingan data historis (snapshot 31 Maret)
- Analisis Top 10 untuk berbagai kategori

### 5. Monitoring Tata Kelola
- Prediksi nilai ITKP (Indikator Tata Kelola Pengadaan)
- Monitoring nilai SIKAP penyedia
- Analisis realisasi kontrak
- Tracking utilisasi e-procurement

## Teknologi yang Digunakan

### Backend
- **Python 3.8+** - Bahasa pemrograman utama
- **Streamlit** - Framework web untuk dashboard interaktif
- **DuckDB** - Database analitik in-memory untuk query cepat
- **Pandas** - Manipulasi dan analisis data
- **Polars** - High-performance data processing

### Visualisasi
- **Plotly Express** - Grafik interaktif (pie chart, bar chart)
- **Streamlit AgGrid** - Tabel data interaktif dan advanced
- **Streamlit Extras** - Komponen UI tambahan (metric cards, logo)

### Utilities
- **Babel** - Formatting mata uang Rupiah
- **OpenPyXL & XlsxWriter** - Operasi file Excel
- **Validators** - Validasi data
- **st_social_media_links** - Integrasi media sosial

### Storage
- **S3-Compatible Storage** - Penyimpanan data berbasis cloud
- **Parquet Format** - Format columnar untuk efisiensi storage

## Struktur Proyek

```
sip-2025/
├── streamlit_app.py              # Entry point utama aplikasi
├── fungsi.py                      # Fungsi utility bersama
├── requirements.txt               # Dependensi Python
├── README.md                      # Dokumentasi proyek
│
├── .streamlit/
│   └── config.toml               # Konfigurasi Streamlit (tema dark)
│
├── public/                        # Asset statis
│   ├── sip-spse-icon.png         # Icon aplikasi
│   ├── sip-spse.png              # Logo aplikasi
│   └── OPSI-1.png                # Logo tambahan
│
└── src/                           # Source code aplikasi
    ├── rencana/                   # Modul perencanaan
    │   ├── rup.py                # Rencana Umum Pengadaan
    │   └── sipraja.py            # Persiapan pengadaan
    │
    ├── proses/                    # Modul proses pengadaan
    │   ├── tender.py             # Transaksi tender
    │   ├── nontender.py          # Transaksi non-tender
    │   ├── pencatatan.py         # Pencatatan langsung
    │   ├── ekatalog.py           # E-Katalog v5
    │   ├── ekatalogv6.py         # E-Katalog v6
    │   ├── tokodaring.py         # Toko daring (BELA)
    │   └── pesertatender.py      # Analisis peserta tender
    │
    └── monitoring/                # Modul monitoring
        ├── itkp.py               # Indikator Tata Kelola Pengadaan
        ├── nilaisikap.py         # Penilaian kinerja penyedia
        └── jenisbelanja.py       # Analisis jenis belanja
```

## Instalasi

### Prasyarat

- Python 3.8 atau versi lebih baru
- pip (Python package installer)
- Git (untuk cloning repository)
- Koneksi internet (untuk akses data dari S3)

### Langkah Instalasi

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd sip-2025
   ```

2. **Buat Virtual Environment (Opsional tapi Direkomendasikan)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verifikasi Instalasi**
   ```bash
   streamlit --version
   ```

## Penggunaan

### Menjalankan Aplikasi

1. **Jalankan Aplikasi Streamlit**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Akses Aplikasi**
   - Buka browser dan akses `http://localhost:8501`
   - Aplikasi akan terbuka otomatis di browser default

3. **Navigasi Aplikasi**
   - Gunakan sidebar untuk memilih daerah dan tahun
   - Pilih modul dari menu navigasi
   - Gunakan filter untuk menyesuaikan tampilan data
   - Klik tombol download untuk ekspor data ke Excel

### Tips Penggunaan

- **Caching Data**: Data di-cache selama 6 jam untuk performa optimal
- **Refresh Data**: Gunakan tombol "Clear cache" di Streamlit menu (☰) untuk refresh data
- **Download Excel**: Setiap halaman memiliki tombol download untuk ekspor data
- **Filter Dinamis**: Filter akan langsung memperbarui visualisasi tanpa reload halaman

## Modul Aplikasi

### 1. RENCANA DAN PERSIAPAN

#### A. Rencana Umum Pengadaan (RUP)

**Fitur:**
- **Profil RUP**: Overview komprehensif RUP dengan struktur anggaran
- **Struktur Anggaran**: Breakdown belanja operasional dan modal
- **Paket Penyedia**: Daftar detail paket yang dikelola penyedia
- **Paket Swakelola**: Tracking paket swakelola
- **Persentase Input RUP**: Progress tracking input data RUP
- **Data 31 Maret**: Snapshot historis untuk perbandingan

**Dimensi Analisis:**
- Perangkat Daerah (PD)
- Metode Pengadaan (E-Tendering, E-Purchasing, dll.)
- Jenis Pengadaan (Barang, Pekerjaan Konstruksi, Jasa Konsultansi, Jasa Lainnya)
- Status UKM (UKM/Non-UKM)
- Status PDN (Produk Dalam Negeri)

**Visualisasi:**
- Pie chart struktur anggaran
- Bar chart per perangkat daerah
- Metric cards dengan persentase capaian

#### B. Persiapan Pengadaan (SIPRAJA)

Monitoring tahap persiapan pengadaan sebelum proses tender/non-tender.

### 2. PROSES PENGADAAN

#### A. Tender

**5 Tahapan yang Dimonitor:**
1. **Pengumuman**: Paket yang diumumkan
2. **SPPBJ**: Surat Penunjukan Penyedia Barang/Jasa
3. **Kontrak**: Kontrak yang ditandatangani
4. **SPMK**: Surat Perintah Mulai Kerja
5. **BAPBAST**: Berita Acara Pemeriksaan dan Serah Terima

**Dimensi Analisis:**
- Sumber Dana (APBD, APBD Perubahan, BLUD, BOS, dll.)
- Status Tender
- Status PDN
- Status UKM
- Paket Kualifikasi
- Jenis Pengadaan
- Metode Pemilihan
- Metode Evaluasi
- Metode Kualifikasi
- Jenis Kontrak Pembayaran

**Visualisasi:**
- Flow tracking dari pengumuman hingga BAPBAST
- Bar chart per dimensi analisis
- Tabel detail dengan AgGrid

#### B. Non-Tender

Sama seperti Tender dengan 5 tahapan dan dimensi analisis yang serupa.

#### C. Pencatatan

**Jenis Pencatatan:**
- **Pencatatan Non-Tender**: Transaksi non-tender yang dicatat
- **Pencatatan Swakelola**: Transaksi swakelola yang dicatat

**Metrics:**
- Jumlah paket
- Nilai realisasi

#### D. E-Katalog Versi 5

**Fitur:**
- Tracking transaksi per jenis katalog
- Analisis berdasarkan etalase (toko/showcase)
- Analisis kualifikasi penyedia
- Top 10 komoditas
- Metrics produk dan transaksi

**Dimensi:**
- Jenis Katalog (Lokal, Sektoral, PDN)
- Etalase
- Kualifikasi Penyedia

#### E. E-Katalog Versi 6

**Fitur:**
- Enhanced catalog transaction tracking
- Top 10 perangkat daerah
- Analisis jenis kemasan
- Monitoring status pengiriman

#### F. Toko Daring (BELA)

**Fitur:**
- Monitoring transaksi platform BELA
- Tracking status verifikasi
- Konfirmasi PPMSE
- Top 10 PD berdasarkan volume dan nilai transaksi
- Top 10 penyedia berdasarkan volume dan nilai transaksi

**Metrics:**
- Total transaksi
- Total nilai transaksi
- Status verifikasi
- Status konfirmasi PPMSE

#### G. Peserta Tender

**Analisis:**
- Peserta yang mendaftar
- Peserta yang memasukkan penawaran
- Pemenang tender
- Statistik per sumber dana
- Nilai penawaran

### 3. MONITORING

#### A. ITKP (Indikator Tata Kelola Pengadaan)

**Komponen Prediksi:**
- Persentase capaian RUP
- Utilisasi e-tendering
- Utilisasi non-e-tendering
- Adopsi e-purchasing
- Penggunaan toko daring
- Tingkat realisasi kontrak

**Output:**
- Prediksi nilai ITKP
- Breakdown per komponen
- Visualisasi kontribusi setiap indikator

#### B. Nilai SIKAP (Sistem Informasi Kinerja Penyedia)

**Fitur:**
- Penilaian berbasis tender
- Penilaian berbasis non-tender
- Scoring: Sangat Baik (≥3), Baik (≥2), Cukup (≥1), Kurang (<1)
- Perbandingan paket yang dinilai vs. tidak dinilai

**Metrics:**
- Jumlah paket dinilai
- Rata-rata nilai SIKAP
- Distribusi kategori penilaian

#### C. Jenis Belanja

**Klasifikasi Anggaran:**
- **Belanja Operasional**:
  - Belanja PBJ
  - Belanja Bantuan Sosial
  - Belanja Hibah
- **Belanja Modal**:
  - Belanja Modal PBJ
- **Belanja Tidak Terduga**

**Visualisasi:**
- Pie chart proporsi jenis belanja
- Bar chart per perangkat daerah
- Tabel detail alokasi anggaran

## Sumber Data

### Platform Data

1. **SIRUP (Sistem Informasi Rencana Umum Pengadaan)**
   - Data perencanaan pengadaan
   - Struktur anggaran
   - Paket penyedia dan swakelola

2. **SPSE (Sistem Pengadaan Secara Elektronik)**
   - Transaksi tender
   - Transaksi non-tender
   - Pencatatan langsung

3. **E-Katalog**
   - Transaksi katalog versi 5 dan 6
   - Data produk dan penyedia

4. **BELA (Belanja Langsung)**
   - Transaksi toko daring
   - Data marketplace pemerintah

5. **SIKAP**
   - Penilaian kinerja penyedia
   - Rating dan evaluasi

### Arsitektur Penyimpanan Data

**Storage:** S3-Compatible Storage di `https://s3-sip.pbj.my.id/`

**Format:** Parquet (columnar storage untuk efisiensi)

**Struktur URL:**

```
RUP Data:
https://s3-sip.pbj.my.id/rup/{kodeRUP}/{dataset-type}/{year}/data.parquet

SPSE Data:
https://s3-sip.pbj.my.id/spse/{kodeLPSE}/{dataset-type}/{year}/data.parquet

E-Katalog:
https://s3-sip.pbj.my.id/katalog/{kodeRUP}/{dataset-type}/{year}/data.parquet

Toko Daring:
https://s3-sip.pbj.my.id/daring/{kodeRUP}/{dataset-type}/{year}/data.parquet

SIKAP:
https://s3-sip.pbj.my.id/sikap/{kodeRUP}/{dataset-type}/{year}/data.parquet
```

**Dataset Types:**
- `rup-paket-penyedia` - Paket penyedia RUP
- `rup-paket-swakelola` - Paket swakelola RUP
- `rup-struktur` - Struktur anggaran RUP
- `spse-TenderEkontrak` - Kontrak tender
- `spse-Nontender` - Transaksi non-tender
- `spse-Pencatatan` - Pencatatan langsung
- `katalog-tokoreguler` - E-Katalog reguler
- `katalog-tokosektoral` - E-Katalog sektoral
- `daring-bela` - Toko daring BELA
- `sikap-tender` - Nilai SIKAP tender
- `sikap-nontender` - Nilai SIKAP non-tender

### Caching Strategy

- **TTL (Time To Live)**: 6 jam
- **Caching Library**: Streamlit @st.cache_data
- **Benefits**:
  - Mengurangi fetching data redundan
  - Meningkatkan performa aplikasi
  - Mengurangi beban server

## Daerah yang Didukung

Aplikasi ini mendukung 14 pemerintah daerah di Kalimantan Barat:

| No | Daerah | Folder Code | Kode RUP | Kode LPSE |
|----|--------|-------------|----------|-----------|
| 1  | Provinsi Kalimantan Barat | `prov` | D197 | 97 |
| 2  | Kota Pontianak | `ptk` | D199 | 62 |
| 3  | Kabupaten Kubu Raya | `kkr` | D202 | 188 |
| 4  | Kabupaten Mempawah | `mpw` | D552 | 118 |
| 5  | Kota Singkawang | `skw` | D200 | 132 |
| 6  | Kabupaten Bengkayang | `bky` | D206 | 444 |
| 7  | Kabupaten Landak | `ldk` | D205 | 496 |
| 8  | Kabupaten Sanggau | `sgu` | D204 | 298 |
| 9  | Kabupaten Sekadau | `skd` | D198 | 175 |
| 10 | Kabupaten Melawi | `mlw` | D210 | 540 |
| 11 | Kabupaten Sintang | `stg` | D211 | 345 |
| 12 | Kabupaten Kapuas Hulu | `kph` | D209 | 488 |
| 13 | Kabupaten Ketapang | `ktp` | D201 | 110 |
| 14 | Kabupaten Kayong Utara | `ktg` | D236 | 438 |

### Konfigurasi Regional

Konfigurasi untuk setiap daerah tersimpan dalam fungsi `region_config()` di [fungsi.py](fungsi.py) dengan struktur:

```python
{
    'nama_daerah': {
        'folder': 'folder_code',
        'kodeRUP': 'D###',
        'kodeLPSE': '##',
        'tahunlist': [2022, 2023, 2024, 2025]
    }
}
```

## Konfigurasi

### Streamlit Configuration

File: [.streamlit/config.toml](.streamlit/config.toml)

```toml
[theme]
base = "dark"  # Tema gelap untuk penggunaan jangka panjang

[client]
showSidebarNavigation = true  # Menampilkan navigasi sidebar
```

### Fungsi Utility Utama

File: [fungsi.py](fungsi.py)

**Core Functions:**

1. **`read_df(url, format='parquet')`**
   - Membaca DataFrame dengan Pandas
   - Caching otomatis (6 jam TTL)
   - Support format: parquet, csv, json

2. **`read_df_duckdb(url, format='parquet')`**
   - Membaca DataFrame dengan DuckDB
   - Optimized untuk query analitik
   - In-memory processing

3. **`download_excel(df)`**
   - Generate file Excel untuk download
   - Formatting mata uang Rupiah
   - Timestamp otomatis pada nama file

4. **`logo()`**
   - Menampilkan logo aplikasi
   - Centered layout

5. **`region_config()`**
   - Return konfigurasi regional
   - Dictionary dengan semua daerah yang didukung

6. **`sidebar_menu()`**
   - Builder menu navigasi sidebar
   - Pemilihan daerah dan tahun

### Environment Variables

Tidak ada environment variables yang diperlukan. Semua konfigurasi hardcoded dalam file konfigurasi.

## Optimisasi Performa

### 1. Database In-Memory
- **DuckDB** digunakan untuk query analitik cepat
- Processing dalam RAM untuk performa maksimal

### 2. Format Data Efisien
- **Parquet format** untuk kompresi optimal
- Columnar storage untuk query yang efisien
- Reduced I/O overhead

### 3. Caching Strategi
- **6-hour TTL** untuk data caching
- Mengurangi redundant data fetching
- Streamlit native caching (@st.cache_data)

### 4. Lazy Loading
- Data di-load hanya saat diperlukan
- Pagination untuk dataset besar
- Progressive rendering

### 5. Query Optimization
- SQL-like queries dengan DuckDB
- Filter pushdown untuk efisiensi
- Selective column reading

## Troubleshooting

### Issue: Data Tidak Muncul

**Solusi:**
1. Cek koneksi internet
2. Verifikasi URL S3 dapat diakses
3. Clear cache Streamlit (☰ → Clear cache)
4. Restart aplikasi

### Issue: Aplikasi Lambat

**Solusi:**
1. Clear browser cache
2. Tutup tab/aplikasi yang tidak digunakan
3. Gunakan filter untuk mengurangi data yang ditampilkan
4. Restart aplikasi untuk refresh cache

### Issue: Error saat Download Excel

**Solusi:**
1. Cek apakah data tersedia
2. Pastikan openpyxl terinstall dengan benar
3. Cek permission untuk menulis file

### Issue: Modul Tidak Ditemukan

**Solusi:**
```bash
pip install -r requirements.txt --upgrade
```

## Best Practices

### Untuk Developer

1. **Code Organization**
   - Ikuti struktur modular yang ada
   - Gunakan fungsi utility dari fungsi.py
   - Consistent naming conventions

2. **Data Processing**
   - Gunakan DuckDB untuk query besar
   - Implementasi error handling dengan try-except
   - Validasi data sebelum processing

3. **UI/UX**
   - Konsisten dengan tema dark
   - Gunakan metric cards untuk KPI
   - Implementasi loading states

4. **Performance**
   - Cache data yang sering diakses
   - Lazy load untuk data besar
   - Optimize queries

### Untuk User

1. **Navigasi Efisien**
   - Gunakan filter untuk mempersempit data
   - Bookmark halaman yang sering diakses
   - Pahami struktur navigasi

2. **Download Data**
   - Filter data sebelum download untuk file lebih kecil
   - Gunakan nama file yang deskriptif
   - Verifikasi data sebelum ekspor

3. **Interpretasi Data**
   - Pahami definisi setiap metric
   - Perhatikan periode data
   - Cross-check dengan sumber data asli jika diperlukan

## Pengembangan Lanjutan

### Roadmap

- [ ] Integrasi dengan API LKPP
- [ ] Export ke format PDF
- [ ] Dashboard personalisasi
- [ ] Notifikasi real-time
- [ ] Mobile responsive design
- [ ] Multi-bahasa support
- [ ] Advanced analytics dengan ML
- [ ] Role-based access control

### Cara Menambah Modul Baru

1. Buat file Python baru di folder yang sesuai (`src/rencana/`, `src/proses/`, atau `src/monitoring/`)
2. Import fungsi utility dari `fungsi.py`
3. Implementasi logika modul
4. Tambahkan page di `streamlit_app.py`
5. Update README.md

**Template Modul:**

```python
import streamlit as st
from fungsi import read_df, download_excel, region_config

st.set_page_config(page_title="Nama Modul", layout="wide")

# Sidebar
st.sidebar.title("Filter")
selected_pd = st.sidebar.selectbox("Pilih Perangkat Daerah", options)

# Main content
st.title("Nama Modul")

# Load data
df = read_df(url)

# Processing
# ... your logic here ...

# Visualization
st.plotly_chart(fig)

# Download
st.download_button("Download Excel", download_excel(df))
```

## Kontribusi

Kontribusi sangat diterima untuk pengembangan aplikasi ini!

### Cara Berkontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines

- Ikuti coding standards yang ada
- Tambahkan dokumentasi untuk fitur baru
- Test fitur sebelum submit PR
- Update README jika diperlukan

### Reporting Issues

Jika menemukan bug atau memiliki saran fitur:
1. Cek apakah issue sudah dilaporkan
2. Buat issue baru dengan deskripsi jelas
3. Tambahkan screenshot jika relevan
4. Sertakan informasi environment (OS, Python version, dll.)

## Lisensi

[Tentukan lisensi yang sesuai - MIT, GPL, Apache, dll.]

## Tim Pengembang

[Informasi tentang tim pengembang]

## Kontak

Untuk pertanyaan, saran, atau dukungan:

- **Email**: [email@example.com]
- **Website**: [https://example.com]
- **GitHub**: [https://github.com/username/sip-2025]

## Ucapan Terima Kasih

- Tim LKPP untuk platform SPSE dan E-Katalog
- Pemerintah Daerah Kalimantan Barat
- Komunitas Streamlit
- Semua kontributor dan pengguna aplikasi

---

**Catatan:** Aplikasi ini dikembangkan untuk mendukung transparansi dan akuntabilitas pengadaan barang dan jasa pemerintah. Data yang ditampilkan bersumber dari sistem resmi pemerintah.

**Versi:** 1.0
**Terakhir Diperbarui:** 2025
**Status:** Active Development

Made with ❤️ for better procurement governance
