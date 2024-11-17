```markdown
MyVending

MyVending adalah program simulasi mesin vending berbasis Python. Aplikasi ini memungkinkan pengguna untuk membeli produk, mengelola akun, dan melakukan tugas administrasi seperti mengelola stok produk dan memantau status mesin vending.

**Dibuat oleh Kelompok 14, Kelas 30, Computational Thinking, STEI-K ITB 2024.**

Fitur Utama
- **Belanja Produk:**
  - Melihat daftar produk.
  - Menambahkan produk ke keranjang.
  - Membayar dengan berbagai metode:
    - MyPay (Saldo)
    - QRIS
    - Tunai (Cash).

- **Manajemen Akun:**
  - Membuat akun baru.
  - Login dan logout akun.
  - Menambah atau menarik saldo menggunakan MyPay.

- **Fitur Admin:**
  - Melihat riwayat aktivitas.
  - Mengelola stok produk di mesin vending.
  - Memantau status mesin vending (suhu dan kelembapan).
  - Memeriksa ketersediaan saldo kembalian tunai.

## Persyaratan
### 1. Python
Gunakan Python versi **3.7** atau lebih baru.  
[Download Python di sini](https://www.python.org/downloads/).

### 2. Instalasi Pustaka Python
Pastikan pustaka `qrcode` telah terinstal. Jika belum, instal menggunakan perintah:
```bash
pip install qrcode
```

### 3. File Pendukung
#### File yang diperlukan:
- **`accounts.csv`**:
  Menyimpan data akun pengguna. Jika file belum tersedia, buat file dengan format berikut:
  ```
  username,password,saldo
  ```
  Contoh:
  ```
  username,password,saldo
  user1,pass1,50000
  ```

- **`kembalian.csv`**:
  Menyimpan data saldo kembalian tunai. Jika file belum tersedia, program akan membuatnya secara otomatis. Format file:
  ```
  nominal,jumlah
  1000,10
  2000,10
  5000,10
  10000,10
  20000,10
  50000,10
  100000,10
  ```

## Cara Menjalankan
1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/myvending.git
   cd myvending
   ```

2. Jalankan program menggunakan perintah:
   ```bash
   python myvending.py
   ```

## Panduan Penggunaan
### Menu Utama
1. **Belanja Produk:**
   - Pilih produk dengan kode produk dan jumlahnya.
   - Lakukan checkout menggunakan metode pembayaran yang tersedia.

2. **Login atau Kelola Akun:**
   - Login dengan username dan password.
   - Tambah saldo atau tarik saldo menggunakan MyPay.

3. **Menu Admin:**
   - Akses dengan password admin: `Admin#123`.
   - Kelola stok, pantau suhu dan kelembapan, atau lihat riwayat aktivitas.

4. **Keluar:**  
   Pilihan untuk menutup program.

### Fitur Tambahan
- **Pembayaran QRIS:**
  Pembayaran dengan QRIS akan menghasilkan kode QR ASCII yang dapat dipindai.  
  *Catatan:* Kode QR ini hanya untuk simulasi dan berisi tautan dummy.

## Screenshot
![Screenshot Produk](https://via.placeholder.com/600x300.png?text=Screenshot+Produk)
![Screenshot Keranjang](https://via.placeholder.com/600x300.png?text=Screenshot+Keranjang)
![Screenshot Pembayaran](https://via.placeholder.com/600x300.png?text=Screenshot+Pembayaran)

## Catatan
- Simulasi ini tidak terhubung ke sistem pembayaran nyata.
- QRIS menggunakan kode dummy untuk tujuan demonstrasi.

---

Selamat menggunakan MyVending! 🎉
```
