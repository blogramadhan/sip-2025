#!/usr/bin/env python3
"""
Script untuk menambahkan icon ke semua tabs di aplikasi
"""

import re
from pathlib import Path

# Mapping icon berdasarkan kata kunci dalam label tab
ICON_MAPPINGS = [
    # Main tabs
    (r'\| PENGUMUMAN \|', '📢 PENGUMUMAN'),
    (r'\| SPPBJ \|', '📋 SPPBJ'),
    (r'\| KONTRAK \|', '📄 KONTRAK'),
    (r'\| SPMK \|', '✅ SPMK'),
    (r'\| BAPBAST \|', '📝 BAPBAST'),

    # Pencatatan
    (r'\| PENCATATAN NON TENDER \|', '📝 PENCATATAN NON TENDER'),
    (r'\| PENCATATAN SWAKELOLA \|', '🏗️ PENCATATAN SWAKELOLA'),

    # RUP tabs
    (r'\| PAKET PENYEDIA \|', '📦 PAKET PENYEDIA'),
    (r'\| STRUKTUR PAKET \|', '🏗️ STRUKTUR PAKET'),
    (r'\| PAKET SWAKELOLA \|', '👷 PAKET SWAKELOLA'),
    (r'\| STRUKTUR SWAKELOLA \|', '📊 STRUKTUR SWAKELOLA'),
    (r'\| PERUBAHAN RUP \|', '🔄 PERUBAHAN RUP'),
    (r'\| REKAPITULASI RUP \|', '📈 REKAPITULASI RUP'),

    # Sikap
    (r'\| SIKAP TENDER \|', '⭐ SIKAP TENDER'),
    (r'\| SIKAP NON TENDER \|', '⭐ SIKAP NON TENDER'),

    # Analysis tabs dengan Jumlah/Nilai
    (r'\| Jumlah Transaksi - Kategori Pengadaan \|', '📊 Jumlah Transaksi - Kategori Pengadaan'),
    (r'\| Nilai Transaksi - Kategori Pengadaan \|', '💰 Nilai Transaksi - Kategori Pengadaan'),
    (r'\| Jumlah Transaksi - Metode Pemilihan \|', '📊 Jumlah Transaksi - Metode Pemilihan'),
    (r'\| Nilai Transaksi - Metode Pemilihan \|', '💰 Nilai Transaksi - Metode Pemilihan'),

    # Generic patterns - harus di akhir
    (r'\| Berdasarkan Jumlah', '📊 Berdasarkan Jumlah'),
    (r'\| Berdasarkan Nilai', '💰 Berdasarkan Nilai'),
    (r'\| Jumlah Kualifikasi Paket \|', '📊 Jumlah Kualifikasi Paket'),
    (r'\| Nilai Kualifikasi Paket \|', '💰 Nilai Kualifikasi Paket'),
    (r'\| Jumlah Jenis Pengadaan \|', '📊 Jumlah Jenis Pengadaan'),
    (r'\| Nilai Jenis Pengadaan \|', '💰 Nilai Jenis Pengadaan'),
    (r'\| Jumlah Metode Pemilihan \|', '📊 Jumlah Metode Pemilihan'),
    (r'\| Nilai Metode Pemilihan \|', '💰 Nilai Metode Pemilihan'),
    (r'\| Jumlah Metode Evaluasi \|', '📊 Jumlah Metode Evaluasi'),
    (r'\| Nilai Metode Evaluasi \|', '💰 Nilai Metode Evaluasi'),
    (r'\| Jumlah Metode Kualifikasi \|', '📊 Jumlah Metode Kualifikasi'),
    (r'\| Nilai Metode Kualifikasi \|', '💰 Nilai Metode Kualifikasi'),
    (r'\| Jumlah Kontrak Pembayaran \|', '📊 Jumlah Kontrak Pembayaran'),
    (r'\| Nilai Kontrak Pembayaran \|', '💰 Nilai Kontrak Pembayaran'),
    (r'\| Jumlah Transaksi \|', '📊 Jumlah Transaksi'),
    (r'\| Nilai Transaksi \|', '💰 Nilai Transaksi'),
]

def update_file_tabs(file_path):
    """Update tabs dalam satu file"""
    path = Path(file_path)

    if not path.exists():
        print(f"❌ File tidak ditemukan: {file_path}")
        return False

    # Baca file
    content = path.read_text(encoding='utf-8')
    original_content = content

    # Apply semua mapping
    changes_made = 0
    for pattern, replacement in ICON_MAPPINGS:
        if pattern in content:
            content = content.replace(pattern, replacement)
            changes_made += 1

    # Tulis kembali jika ada perubahan
    if content != original_content:
        path.write_text(content, encoding='utf-8')
        print(f"✅ {path.name}: {changes_made} tabs diupdate")
        return True
    else:
        print(f"ℹ️  {path.name}: Tidak ada perubahan")
        return False

def main():
    """Main function"""
    print("🚀 Mulai update icon tabs...\n")

    # Daftar file yang akan diupdate
    files = [
        # Proses
        'src/proses/nontender.py',
        'src/proses/pencatatan.py',
        'src/proses/tender.py',
        'src/proses/tokodaring.py',
        'src/proses/pesertatender.py',

        # Monitoring
        'src/monitoring/nilaisikap.py',
        'src/monitoring/itkp.py',
        'src/monitoring/jenisbelanja.py',

        # Rencana
        'src/rencana/rup.py',
        'src/rencana/sipraja.py',
    ]

    updated_count = 0
    for file_path in files:
        if update_file_tabs(file_path):
            updated_count += 1

    print(f"\n✨ Selesai! {updated_count} file berhasil diupdate")

if __name__ == '__main__':
    main()
