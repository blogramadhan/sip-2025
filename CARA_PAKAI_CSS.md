# 🎨 Cara Pakai Custom CSS

## Sudah Aktif! ✅

CSS sudah otomatis aktif di aplikasi. Anda tidak perlu melakukan apa-apa.

---

## 📸 Apa yang Berubah?

### Sebelum
- Tampilan default Streamlit
- Warna standar
- Tidak ada animasi
- Tabs tanpa icon

### Sesudah ✨
- **Metric Cards**: Border warna-warni, hover effect
- **Buttons**: Gradient biru-ungu, shadow saat hover
- **Tabs**: Pill-style modern dengan icon emoji 📊 💰 📦 🏪
- **Radio Buttons**: Card-style dengan gradient
- **Sidebar**: Gradient background, smooth navigation
- **Animasi**: Fade in, hover effects di semua tombol

### Icon di Tabs
- 📦 Transaksi Katalog
- 🏪 Transaksi Etalase
- 📋 Tabel Data
- 📊 Jumlah/Chart
- 💰 Nilai Rupiah

Lihat panduan lengkap: [ICON_GUIDE.md](ICON_GUIDE.md)

---

## 🎨 Warna Tema

| Warna | Untuk Apa |
|-------|-----------|
| 🔵 Biru (`#2563eb`) | Primary - Buttons, links |
| 🟣 Ungu (`#8b5cf6`) | Accent - Highlights |
| 🟢 Hijau (`#10b981`) | Success - Download button |
| ⚫ Gelap (`#0f172a`) | Background |

---

## ⚙️ Cara Ubah Warna

Buka file [style.css](style.css) baris 11-17:

```css
:root {
    --primary: #2563eb;     /* Ganti dengan warna favorit */
    --accent: #8b5cf6;      /* Ganti dengan warna aksen */
    --success: #10b981;     /* Warna untuk download button */
}
```

### Contoh: Ganti Jadi Hijau-Tosca
```css
:root {
    --primary: #10b981;     /* Hijau */
    --accent: #06b6d4;      /* Tosca */
    --success: #059669;     /* Hijau tua */
}
```

---

## 🔄 Cara Refresh Tampilan

Setelah ubah CSS:
1. Save file CSS
2. Tekan `R` di browser
3. Atau tekan `Ctrl+R` / `Cmd+R`

---

## 📱 Support Mobile

CSS otomatis menyesuaikan untuk:
- 📱 Mobile (< 768px)
- 💻 Desktop (> 768px)

---

## ❓ Troubleshooting

**CSS tidak muncul?**
- Cek file `style.css` ada di folder root
- Pastikan `load_css()` dipanggil di `streamlit_app.py`
- Restart aplikasi: `streamlit run streamlit_app.py`

**Warna tidak berubah?**
- Clear browser cache: `Ctrl+Shift+Del`
- Hard reload: `Ctrl+Shift+R`

---

## 💡 Tips

1. **Jangan ubah struktur CSS** - hanya ubah nilai warna
2. **Backup dulu** sebelum edit
3. **Test di browser lain** kalau ada masalah
4. **Pakai Developer Tools** (F12) untuk debug

---

## 📞 Butuh Bantuan?

Baca dokumentasi lengkap: [README_CSS.md](README_CSS.md)

---

**Happy Coding! 🚀**
