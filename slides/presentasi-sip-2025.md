# Sistem Informasi Pelaporan Pengadaan (SIP) 2025

Tanggal: __/__/____
Pemapar: __________________

---

## Tujuan Presentasi

- Memahami alur penggunaan aplikasi SIP 2025
- Mengetahui fitur utama per modul
- Mampu mengekspor data untuk analisis lanjutan

---

## Gambaran Umum Aplikasi

SIP 2025 menyajikan informasi pengadaan barang dan jasa secara terstruktur,
mulai dari perencanaan, proses pelaksanaan, hingga monitoring kinerja.

Fokus utama:
- Ringkas dan cepat dibaca
- Filter daerah dan tahun di setiap modul
- Unduh data ke Excel untuk pelaporan

---

## Peta Modul (Visual Ringkas)

```
Rencana  ->  Proses  ->  Monitoring
   |           |            |
  RUP    Tender/NonTender   ITKP
           Pencatatan       Jenis Belanja
           E-Katalog        Nilai SIKAP
           Toko Daring
           Peserta Tender
```

---

## Alur Penggunaan (Flow)

```mermaid
flowchart LR
    A[Beranda] --> B[Pilih Modul]
    B --> C[Pilih Daerah & Tahun]
    C --> D[Filter Data]
    D --> E[Lihat Metrik & Grafik]
    E --> F[Unduh Excel]
```

---

## Navigasi Sidebar

Struktur menu:
- Rencana: RUP
- Proses: Tender, Non Tender, Pencatatan, E-Katalog v5/v6, Toko Daring, Peserta Tender
- Monitoring: ITKP, Jenis Belanja, Nilai SIKAP

Tips:
- Gunakan filter data untuk fokus pada perangkat daerah tertentu.
- Gunakan tombol unduh di setiap halaman untuk ekspor cepat.

---

## Modul Rencana: RUP

Fokus:
- Profil RUP
- Struktur anggaran
- Paket penyedia & swakelola
- Persentase input RUP

Output:
- Grafik ringkas
- Tabel detail paket
- Export Excel

---

## Modul Proses: Tender

Fokus:
- Pengumuman tender
- SPPBJ, Kontrak, SPMK, BAPBAST

Output:
- Metrik jumlah dan nilai
- Grafik per kategori
- Tabel transaksi detail

---

## Modul Proses: Non Tender & Pencatatan

Non Tender:
- Pengumuman, SPPBJ, Kontrak, SPMK, BAPBAST

Pencatatan:
- Non Tender dan Swakelola
- Status berjalan/selesai/dibatalkan

Output:
- Ringkasan status
- Unduhan Excel

---

## Modul Proses: E-Katalog & Toko Daring

E-Katalog v5/v6:
- Transaksi per komoditas, satker, penyedia

Toko Daring:
- Transaksi per perangkat daerah dan pelaku usaha

Output:
- Grafik distribusi
- Tabel dan ekspor

---

## Modul Proses: Peserta Tender

Fokus:
- Mendaftar, menawar, pemenang
- Filter sumber dana dan perangkat daerah

Output:
- Metrik peserta
- Tabel detail penawaran

---

## Modul Monitoring: ITKP

Fokus:
- Prediksi kinerja pengadaan
- Ringkasan per area: RUP, E-Tendering, Non E-Tendering, E-Kontrak, E-Katalog, Toko Daring

Output:
- Metrik prediksi dan capaian

---

## Modul Monitoring: Jenis Belanja & Nilai SIKAP

Jenis Belanja:
- Belanja operasi, modal, tak terduga

Nilai SIKAP:
- Penilaian kinerja penyedia
- Status penilaian paket

Output:
- Metrik utama dan tabel ekspor

---

## Fitur Kunci (Ringkas)

| Fitur | Manfaat |
|------|---------|
| Filter daerah & tahun | Fokus analisis |
| Metrik otomatis | Ringkas & cepat dibaca |
| Grafik interaktif | Insight visual |
| Unduh Excel | Pelaporan cepat |

---

## Contoh Skema Filter

```
Pilih Daerah -> Pilih Tahun -> Terapkan Filter -> Hasil Metrik & Grafik
```

Catatan:
- Gunakan filter gabungan untuk melihat ringkasan global.

---

## Sumber Data Utama

- SIRUP (RUP)
- SPSE (Tender, Non Tender)
- SIKAP (Penilaian Kinerja Penyedia)
- E-Katalog
- Toko Daring

---

## Praktik Baik Penggunaan

- Mulai dari Beranda untuk melihat gambaran modul
- Pilih perangkat daerah sebelum analisis detail
- Bandingkan periode berbeda untuk tren
- Simpan hasil unduhan untuk arsip laporan

---

## FAQ Singkat

Q: Data kosong setelah filter?
A: Pastikan periode/tahun sesuai ketersediaan data.

Q: Kenapa grafik tidak tampil?
A: Cek koneksi dan ulangi filter.

Q: Export gagal?
A: Coba ulangi setelah refresh halaman.

---

## Penutup

SIP 2025 membantu memantau pengadaan secara terpadu dan transparan.
Gunakan filter dan unduhan untuk mendukung analisis dan pelaporan.

Terima kasih.
