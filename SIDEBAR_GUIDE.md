# 🎯 Panduan Sidebar - SIP 2025

## Struktur Sidebar

Sidebar sekarang dibagi menjadi **3 blok section** yang terorganisir dengan baik:

### 1. 📋 RENCANA PENGADAAN
Menu untuk perencanaan pengadaan:
- 📋 Rencana Pengadaan (RUP)
- 🛠️ Persiapan Pengadaan (coming soon)

### 2. ⚙️ PROSES PENGADAAN
Menu untuk proses pengadaan:
- 🏆 Tender
- 📄 Non Tender
- ✏️ Pencatatan
- 🏪 E-Katalog Versi 5
- 🏪 E-Katalog Versi 6
- 🛒 Toko Daring
- 👥 Peserta Tender

### 3. 📊 MONITORING
Menu untuk monitoring:
- 📈 ITKP
- ⭐ Nilai SIKAP
- 💰 Jenis Belanja

---

## Fitur Sidebar

### ✨ Section Headers
- Background gradient biru
- Border kiri biru
- Icon section otomatis
- Font kecil & uppercase

### ✨ Menu Items
- Icon otomatis berdasarkan nama file
- Hover effect dengan slide ke kanan
- Active state dengan gradient biru-ungu
- Shadow pada item aktif

### ✨ Divider
- Garis pemisah antar section
- Warna subtle untuk tidak mengganggu

---

## Customisasi

### Mengubah Icon Section

Edit [style_components.css](style_components.css:28-41):

```css
/* Section 1: Rencana */
[data-testid="stSidebarNav"] > ul > li:nth-child(1) > div > div::before {
    content: "📋 ";
}

/* Section 2: Proses */
[data-testid="stSidebarNav"] > ul > li:nth-child(2) > div > div::before {
    content: "⚙️ ";
}

/* Section 3: Monitoring */
[data-testid="stSidebarNav"] > ul > li:nth-child(3) > div > div::before {
    content: "📊 ";
}
```

### Mengubah Icon Menu Items

Edit [style_components.css](style_components.css:45-85):

```css
[data-testid="stSidebarNav"] a[href*="tender"]::before {
    content: "🏆 ";  /* Ganti icon sesuai keinginan */
}
```

### Menambah Menu Baru

Edit [streamlit_app.py](streamlit_app.py:22-40):

```python
pages = {
    "RENCANA PENGADAAN": [
        st.Page("./src/rencana/rup.py", title="Rencana Pengadaan"),
        st.Page("./src/rencana/new_menu.py", title="Menu Baru"),  # Tambah di sini
    ],
    # ...
}
```

Jangan lupa tambahkan icon di CSS:
```css
[data-testid="stSidebarNav"] a[href*="new_menu"]::before {
    content: "🆕 ";
}
```

---

## Troubleshooting

### Sidebar tidak muncul?
1. Cek `initial_sidebar_state="expanded"` di `st.set_page_config()`
2. Refresh browser dengan `Ctrl+R`
3. Clear cache: `Ctrl+Shift+R`

### Section tidak terpisah?
1. Pastikan structure `pages` dict benar di `streamlit_app.py`
2. CSS sudah dimuat dengan `load_css()`

### Icon tidak muncul?
1. Cek `style_components.css` sudah dimuat
2. Periksa selector CSS sesuai dengan href
3. Clear browser cache

---

## Warna Sidebar

### Background
- Top: `#334155`
- Bottom: `#1e293b`
- Gradient: `linear-gradient(180deg, #334155 0%, #1e293b 100%)`

### Section Header
- Background: `rgba(59, 130, 246, 0.1)`
- Border left: `#3b82f6` (3px)
- Text: `#cbd5e1`

### Menu Items
- Normal: `#e2e8f0`
- Hover: `#ffffff` on `#475569`
- Active: `white` on `linear-gradient(135deg, #3b82f6, #a78bfa)`

---

## Tips

1. **Konsisten Icon**: Gunakan icon yang relevan dengan fungsi
2. **Nama Jelas**: Title menu harus deskriptif
3. **Grouping**: Kelompokkan menu serupa dalam satu section
4. **Max Items**: Usahakan max 7-8 items per section agar tidak scroll panjang

---

## Preview Sidebar

```
┌─────────────────────────────────┐
│ 📋 RENCANA PENGADAAN           │
├─────────────────────────────────┤
│  📋 Rencana Pengadaan          │
├─────────────────────────────────┤
│ ⚙️ PROSES PENGADAAN            │
├─────────────────────────────────┤
│  🏆 Tender                     │
│  📄 Non Tender                 │
│  ✏️ Pencatatan                 │
│  🏪 E-Katalog Versi 5          │
│  🏪 E-Katalog Versi 6          │
│  🛒 Toko Daring                │
│  👥 Peserta Tender             │
├─────────────────────────────────┤
│ 📊 MONITORING                  │
├─────────────────────────────────┤
│  📈 ITKP                       │
│  ⭐ Nilai SIKAP                │
│  💰 Jenis Belanja              │
└─────────────────────────────────┘
```

---

**Update:** Desember 2025
**Version:** 2.0
