# Troubleshooting Guide - Logo Issues in Production

## Masalah: Logo Bermasalah di Server Production

### Diagnostic Steps

#### 1. Build Docker Image dengan Verbose Output
```bash
docker build --progress=plain --no-cache -t sip-spse:debug .
```

Perhatikan output di bagian:
- `Public directory found, setting permissions...`
- `✓ Logo file found: public/sip-spse.png`
- `✓ Icon file found: public/sip-spse-icon.png`

#### 2. Jalankan Debug Script di Container
```bash
# Run container interactively
docker run -it --rm sip-spse:debug /bin/bash

# Di dalam container, jalankan:
python3 debug_docker.py
```

Atau jalankan langsung:
```bash
docker run --rm sip-spse:debug python3 debug_docker.py
```

#### 3. Test Logo Paths di Container
```bash
docker run --rm sip-spse:debug python3 test_logo.py
```

#### 4. Inspect Container yang Sedang Berjalan
```bash
# Dapatkan container ID
docker ps

# Masuk ke container
docker exec -it <container_id> /bin/bash

# Cek file structure
ls -la /app/
ls -la /app/public/
cat /app/public/sip-spse.png | wc -c  # Cek ukuran file
```

### Common Issues dan Solutions

#### Issue 1: File Tidak Tersalin ke Docker Image
**Symptoms:**
- Error: "Logo file not found at: /app/public/sip-spse.png"
- Build log tidak menampilkan "✓ Logo file found"

**Solution:**
```bash
# Pastikan .dockerignore tidak mengabaikan public/
# Periksa bahwa baris ini ada di .dockerignore:
!public/
!public/*.png

# Rebuild dengan --no-cache
docker build --no-cache -t sip-spse:latest .
```

#### Issue 2: Permission Denied
**Symptoms:**
- Error: "Permission denied" saat mengakses logo
- Files ada tapi tidak bisa dibaca

**Solution:**
```bash
# Cek di Dockerfile bahwa chmod dijalankan SEBELUM switch ke appuser
# Urutan harus:
# 1. COPY . .
# 2. chmod -R 755 public
# 3. chown -R appuser:appuser /app
# 4. USER appuser
```

#### Issue 3: Streamlit Tidak Bisa Load Local Files
**Symptoms:**
- File exists tapi Streamlit tidak bisa render logo
- Error di Streamlit console

**Solution:**
Gunakan absolute path dan pastikan working directory benar:

```python
import os
base_dir = os.getcwd()  # Di Docker, ini seharusnya /app
logo_path = os.path.join(base_dir, "public", "sip-spse.png")
```

#### Issue 4: Logo Muncul di Localhost Tapi Tidak di Production
**Symptoms:**
- Berfungsi di `streamlit run streamlit_app.py`
- Tidak berfungsi di Docker container

**Possible Causes:**
1. Path resolution berbeda
2. File tidak tersalin ke image
3. Streamlit version berbeda
4. Working directory berbeda

**Solution:**
Gunakan fungsi logo() yang sudah diperbaiki di `fungsi.py` yang memiliki fallback:
```python
# Fungsi sudah menghandle multiple fallback paths
# 1. Dari __file__ directory
# 2. Dari os.getcwd()
# 3. Dari sys.modules['__main__'].__file__
```

### Quick Fix Commands

#### Rebuild Image Completely
```bash
# Hapus image lama
docker rmi sip-spse:latest

# Build ulang tanpa cache
docker build --no-cache -t sip-spse:latest .

# Test run
docker run -p 8502:8502 sip-spse:latest
```

#### Check Logs
```bash
# Lihat logs container
docker logs <container_id>

# Follow logs real-time
docker logs -f <container_id>
```

#### Interactive Debugging
```bash
# Run dengan shell access
docker run -it --rm -p 8502:8502 sip-spse:latest /bin/bash

# Di dalam container:
# 1. Cek files
ls -la /app/public/

# 2. Test paths
python3 test_logo.py

# 3. Run debug
python3 debug_docker.py

# 4. Start Streamlit manually
streamlit run streamlit_app.py --server.port=8502 --server.address=0.0.0.0
```

### Environment-Specific Issues

#### WSL2 / Windows
```bash
# Pastikan line endings benar (LF, bukan CRLF)
git config --global core.autocrlf input

# Rebuild image
docker build --no-cache -t sip-spse:latest .
```

#### Linux Server
```bash
# Pastikan SELinux tidak blocking (jika applicable)
getenforce  # Cek status SELinux

# Jika enforcing, set ke permissive temporarily
sudo setenforce 0
```

#### Docker Compose
Jika menggunakan docker-compose, pastikan volume mapping tidak override files:
```yaml
# JANGAN map volume yang override public/
# BAD:
volumes:
  - .:/app  # Ini akan override public/ di container

# GOOD:
volumes:
  - ./.cache:/app/.cache  # Hanya map specific directories
```

### Contact Points

Jika masalah masih berlanjut setelah semua langkah di atas:

1. Jalankan `docker run --rm sip-spse:latest python3 debug_docker.py > debug_output.txt`
2. Simpan build logs: `docker build --progress=plain . 2>&1 | tee build.log`
3. Simpan runtime logs: `docker logs <container_id> > runtime.log`
4. Share file debug_output.txt, build.log, dan runtime.log untuk analisis lebih lanjut
