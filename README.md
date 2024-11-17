# MyVending

**MyVending** adalah program simulasi mesin vending berbasis Python. Program ini memungkinkan pengguna untuk membeli produk, mengelola akun, dan melaksanakan tugas administrasi seperti mengelola stok produk dan memantau status mesin vending. 

---

## ✨ Fitur Utama
1. **Belanja Produk**
   - Melihat daftar produk.
   - Menambahkan produk ke keranjang belanja.
   - Melakukan pembayaran dengan metode:
     - **Saldo MyPay**
     - **QRIS** (Simulasi QR code ASCII)
     - **Tunai** (Cash).

2. **Manajemen Akun**
   - Membuat akun baru.
   - Login dan logout akun.
   - Menambah atau menarik saldo dengan MyPay.

3. **Fitur Admin**
   - Melihat riwayat aktivitas.
   - Mengelola stok produk di mesin vending.
   - Memantau status mesin vending (suhu dan kelembapan).
   - Memeriksa ketersediaan saldo kembalian tunai.

---

## ⚙️ Persyaratan
1. **Python**  
   Gunakan Python versi **3.7** atau lebih baru.  
   [Download Python di sini](https://www.python.org/downloads/).

2. **Instalasi Modul Python**
   Pastikan modul **`qrcode`** telah terinstal. Jika belum, instal dengan perintah:
   ```bash
   pip install qrcode
   ```

3. **File Pendukung**
   - **`accounts.csv`**: Menyimpan data akun pengguna. Jika file belum tersedia, buat file dengan format berikut:
     ```
     username,password,saldo
     ```
     Contoh:
     ```
     username,password,saldo
     user1,pass1,50000
     user2,pass2,100000
     ```
   - **`kembalian.csv`**: Menyimpan data saldo kembalian tunai. Jika file belum tersedia, program akan membuatnya secara otomatis. Format:
     ```
     nominal,jumlah
     1000,50
     2000,40
     5000,30
     10000,20
     20000,10
     50000,6
     100000,2
     ```

---

## 🚀 Cara Menjalankan
1. Clone repositori ini:
   ```bash
   git clone https://github.com/username/myvending.git
   cd myvending
   ```

2. Jalankan program dengan perintah:
   ```bash
   python myvending.py
   ```

---

## 📖 Panduan Penggunaan
### **Menu Utama**
1. **Belanja Produk**
   - Pilih produk berdasarkan kode produk dan tentukan jumlah yang ingin dibeli.
   - Lakukan checkout dengan metode pembayaran yang tersedia.

2. **Manajemen Akun**
   - Login dengan username dan password.
   - Tambah saldo atau tarik saldo menggunakan MyPay.

3. **Menu Admin**
   - Akses menggunakan password: `Admin#123`.
   - Mengelola stok produk, memantau suhu dan kelembapan, atau melihat riwayat aktivitas.

4. **Keluar**
   - Pilihan untuk menutup program.

---

## 🛠️ Fitur Tambahan
- **QRIS Simulasi**
  - Pembayaran melalui QRIS menghasilkan kode QR ASCII yang dapat dipindai.
  - Catatan: QRIS ini hanya simulasi dan mengarahkan ke tautan dummy.

---

## 📷 Screenshot
Berikut adalah beberapa tangkapan layar dari program:
- **Menu Utama**  
  ![Menu Utama](https://i.imgur.com/r8kpwJr.png).

- **Keranjang Belanja**  
  ![Screenshot Keranjang](https://via.placeholder.com/600x300.png?text=Screenshot+Keranjang)

- **Proses Pembayaran**  
  ![Screenshot Pembayaran](https://via.placeholder.com/600x300.png?text=Screenshot+Pembayaran)

---

## 📝 Catatan
- Program ini hanya simulasi dan tidak terhubung ke sistem pembayaran nyata.
- Semua transaksi QRIS menggunakan kode dummy untuk tujuan demonstrasi.

---

## 📍 Informasi Tim
**Dibuat oleh Kelompok 14, Kelas 30, Computational Thinking, STEI-K ITB 2024.**  
Selamat menggunakan MyVending! 🎉  
