# Program MyVending
# Spesifikasi Program:
# Program ini adalah simulasi vending machine yang mendukung pembelian produk,
# pengelolaan akun, dan fitur admin untuk memantau serta mengelola sistem.

# KAMUS
# stok : Objek dari kelas StokBarang untuk mengelola produk di vending machine
# log : Objek dari kelas LogAktivitas untuk mencatat aktivitas sistem
# kembalian : Objek dari kelas SistemKembalian untuk mengelola saldo uang kembalian
# akun : Objek dari kelas Akun untuk fitur login, pembuatan akun, dan pengelolaan saldo
# pembayaran : Objek dari kelas SistemPembayaran untuk memproses pembayaran (tunai, QRIS, atau saldo)
# pesanan : Objek dari kelas PemrosesanPesanan untuk menambahkan produk ke keranjang dan checkout
# vending_status : Objek dari kelas MyVendingStatus untuk memonitor suhu dan kelembapan mesin
# admin_password : String, kata sandi untuk mengakses menu admin
# pilihan_menu : Integer, input pilihan pengguna untuk menu utama
# pilihan_menubelanja : Integer, input pilihan pengguna untuk menu belanja
# pilihan_akun : Integer, input pilihan pengguna untuk menu akun
# pilihan_menuadmin : Integer, input pilihan pengguna untuk menu admin

# kembalian.csv : File CSV yang digunakan untuk menyimpan data saldo uang kembalian
# Format file kembalian.csv:
# nominal : Integer, nilai pecahan uang (contoh: 1000, 2000, 5000, dst.)
# jumlah : Integer, jumlah lembar uang untuk setiap pecahan
#
# Contoh isi file kembalian.csv:
# nominal,jumlah
# 1000,50
# 2000,40
# 5000,30
# 10000,20
# 20000,10
# 50000,6
# 100000,2
#
# Fungsi:
# - File ini diakses oleh kelas SistemKembalian untuk memuat dan memperbarui data uang kembalian.

# accounts.csv : File CSV yang digunakan untuk menyimpan data akun pengguna
# Format file accounts.csv:
# username : String, nama pengguna yang unik untuk setiap akun
# password : String, kata sandi untuk mengakses akun (disimpan dalam bentuk teks biasa di program ini)
# saldo : Integer, jumlah saldo MyPay yang dimiliki oleh pengguna
#
# Contoh isi file accounts.csv:
# username,password,saldo
# user1,pass123,50000
# user2,secure456,100000
# admin,adminpass,150000
#
# Fungsi:
# - File ini diakses oleh kelas Akun untuk memuat, membuat, memperbarui, dan memvalidasi data akun pengguna.
# - Saldo pada file ini digunakan untuk sistem pembayaran melalui MyPay.

# feedback.csv : File CSV yang digunakan untuk menyimpan feedback pengguna
# Format file feedback.csv:
# rating : Integer, nilai umpan balik dari pengguna (contoh: 1-5)
# feedback : String, komentar atau masukan dari pengguna
#
# Contoh isi file feedback.csv:
# rating,feedback
# 4,Sangat memuaskan
# 2,Layanan kurang memadai
#
# Fungsi:
# - File ini digunakan untuk mencatat dan menampilkan umpan balik pengguna terhadap vending machine.

# keranjang.csv : File CSV yang digunakan untuk menyimpan data keranjang belanja sementara
# Format file keranjang.csv:
# code : Integer, kode produk
# name : String, nama produk
# quantity : Integer, jumlah item
# price : Integer, harga total untuk item tersebut
#
# Contoh isi file keranjang.csv:
# code,name,quantity,price
# 1,Aqua,2,8000
# 2,Pocari Sweat,1,8000
#
# Fungsi:
# - File ini digunakan untuk mencatat sementara produk-produk yang ditambahkan ke keranjang belanja.

# log_aktivitas.csv : File CSV yang digunakan untuk mencatat aktivitas sistem
# Format file log_aktivitas.csv:
# timestamp : String, waktu aktivitas dalam format YYYY-MM-DD HH:MM:SS
# action : String, jenis aktivitas yang dilakukan
# detail : String, detail tambahan tentang aktivitas
#
# Contoh isi file log_aktivitas.csv:
# timestamp,action,detail
# 2024-12-23 07:34:41,Update Expired,Produk Aqua -> 07/25
# 2024-12-23 08:00:00,Tambah Stok,Produk Pocari Sweat +10
#
# Fungsi:
# - File ini digunakan untuk mencatat semua aktivitas yang terjadi di sistem, seperti perubahan stok, pembaruan expired, atau penambahan saldo.

# stok.csv : File CSV yang digunakan untuk menyimpan data produk dalam vending machine
# Format file stok.csv:
# code : Integer, kode produk unik
# name : String, nama produk
# price : Integer, harga produk
# stock : Integer, jumlah stok produk
# expired : String, tanggal kadaluarsa produk dalam format MM/YY atau lainnya
#
# Contoh isi file stok.csv:
# code,name,price,stock,expired
# 1,Aqua,4000,20,07/25
# 2,Pocari Sweat,8000,10,Unknown
# 3,Teh Pucuk,5000,16,09/25
#
# Fungsi:
# - File ini digunakan untuk memuat dan menyimpan data stok produk, termasuk informasi kadaluarsa.

# ALGORITMA
import os
# Modul `os` digunakan untuk berinteraksi dengan sistem operasi, seperti membersihkan layar terminal.

import time
# Modul `time` digunakan untuk menangani operasi terkait waktu, seperti mencatat waktu transaksi.

import csv
# Modul `csv` digunakan untuk membaca dan menulis file dalam format CSV, seperti data akun atau saldo.

import getpass
# Modul `getpass` digunakan untuk mengambil input password secara aman (input tidak terlihat saat diketik).

from datetime import datetime

def clear_screen():
    # Fungsi untuk membersihkan layar terminal agar tampilan menu lebih rapi setiap kali di-refresh.
    # `os.system` akan memanggil perintah bawaan sistem operasi:
    # - 'cls' untuk Windows
    # - 'clear' untuk sistem berbasis UNIX (Linux, macOS)
    os.system('cls' if os.name == 'nt' else 'clear')

class StokBarang:
    def __init__(self, file_name="stok.csv"):
        self.file_name = file_name  # Menyimpan nama file CSV yang digunakan untuk menyimpan data produk.
        self.products = self.load_products()  # Memuat data produk dari file atau membuat data default jika file tidak ada.

    def load_products(self):
        if not os.path.exists(self.file_name):  # Mengecek apakah file stok ada.
            # Jika file tidak ada, membuat data default produk.
            return {
                1: {"name": "Aqua", "price": 4000, "stock": 10, "expired": "Jul 2025"},
                2: {"name": "Pocari Sweat", "price": 8000, "stock": 10, "expired": "Jul 2025"},
                3: {"name": "Teh Pucuk", "price": 5000, "stock": 10, "expired": "Jul 2025"},
                4: {"name": "Lime", "price": 5000, "stock": 10, "expired": "Jul 2025"},
                5: {"name": "Coca cola", "price": 5000, "stock": 10, "expired": "Jul 2025"},
                6: {"name": "Cap Kaki Tiga", "price": 9000, "stock": 10, "expired": "Jul 2025"},
                7: {"name": "Floridina", "price": 5000, "stock": 10, "expired": "Jul 2025"}
            }

        products = {}  # Dictionary untuk menyimpan data produk dari file CSV.
        with open(self.file_name, mode='r') as file:  # Membuka file CSV dalam mode baca.
            reader = csv.DictReader(file)  # Membaca file CSV sebagai dictionary.
            for row in reader:
                try:
                    # Mengisi dictionary produk berdasarkan data dalam file.
                    products[int(row["code"])] = {
                        "name": row["name"],  # Nama produk.
                        "price": int(row["price"]),  # Harga produk.
                        "stock": int(row["stock"]),  # Jumlah stok produk.
                        "expired": row.get("expired", "Unknown")  # Tanggal expired produk.
                    }
                except KeyError as e:
                    # Menampilkan pesan error jika ada kolom yang hilang.
                    print(f"Error reading product: Missing key {e}")
        return products  # Mengembalikan data produk sebagai dictionary.

    def save_products(self):
        with open(self.file_name, mode='w', newline='') as file:  # Membuka file CSV dalam mode tulis.
            fieldnames = ["code", "name", "price", "stock", "expired"]  # Kolom yang akan ditulis ke file.
            writer = csv.DictWriter(file, fieldnames=fieldnames)  # Membuat writer untuk menulis data ke CSV.
            writer.writeheader()  # Menulis header kolom.
            for code, product in self.products.items():
                # Menulis setiap produk ke file CSV.
                writer.writerow({
                    "code": code,  # Kode produk.
                    "name": product["name"],  # Nama produk.
                    "price": product["price"],  # Harga produk.
                    "stock": product["stock"],  # Stok produk.
                    "expired": product["expired"]  # Tanggal expired produk.
                })

    def display_products(self):
        # Menampilkan daftar produk dalam vending machine.
        print("                    DAFTAR PRODUK                    ")
        print("|---------------------------------------------------|")
        print("| Kode | Produk           | Harga      | Stok       |")
        print("|---------------------------------------------------|")
        for code, product in self.products.items():
            # Menampilkan detail produk: kode, nama, harga, stok.
            print(f"| {code:<4} | {product['name']:<16} | Rp{product['price']:<8} | {product['stock']:<8}   |")
        print("|---------------------------------------------------|")
    
    def display_products_admin(self):
        # Menampilkan daftar produk untuk admin dengan tambahan tanggal expired.
        print("                            DAFTAR PRODUK                            ")
        print("|---------------------------------------------------|---------------|")
        print("| Kode | Produk           | Harga      | Stok       | Expired       |")
        print("|---------------------------------------------------|---------------|")
        for code, product in self.products.items():
            # Menampilkan detail produk: kode, nama, harga, stok, dan tanggal expired.
            print(f"| {code:<4} | {product['name']:<16} | Rp{product['price']:<8} | {product['stock']:<8}   | {product['expired']:<13} |")
        print("|-------------------------------------------------------------------|")
    
    def check_stock_and_update(self, product_code, quantity):
        # Fungsi untuk mengecek stok produk dan mengurangi stok jika tersedia.
        # Parameter:
        # - product_code: Kode produk yang ingin dibeli.
        # - quantity: Jumlah produk yang ingin dibeli.
        # Return:
        # - True jika stok mencukupi, False jika stok tidak mencukupi atau kode produk tidak valid.

        if product_code in self.products: # Mengecek apakah kode produk valid.
            product = self.products[product_code]
            if product["stock"] >= quantity:
                # Jika stok mencukupi, kurangi stok sesuai jumlah yang diminta.
                product["stock"] -= quantity
                return True
            else:
                # Jika stok tidak mencukupi, tampilkan pesan kesalahan.
                print(f"Stok tidak cukup untuk {product['name']}!")
                return False
        return False # Mengembalikan False jika kode produk tidak valid.
    
    def tambah_stok(self, product_code, tambahan, log):
        # Fungsi untuk menambah stok suatu produk.
        # Parameter:
        # - product_code: Kode produk yang ingin ditambah stoknya.
        # - tambahan: Jumlah stok yang ingin ditambahkan.
        # - log: Objek LogAktivitas untuk mencatat riwayat penambahan stok.

        if product_code in self.products:
            current_stock = self.products[product_code]["stock"]
            if current_stock + tambahan > 25:
                # Jika total stok melebihi kapasitas maksimum (25), tampilkan pesan peringatan.
                print(f"\nStok akan overload! Kapasitas maksimal per produk adalah 25. \nStok saat ini\t: {current_stock} \nTambahan\t: {tambahan}.")
                print("Penambahan stok produk tidak dapat dilakukan!")
                return False
            else:
                # Jika kapasitas mencukupi, tambahkan stok dan catat riwayatnya.
                self.products[product_code]["stock"] += tambahan
                self.save_products()
                log.add_log("Tambah Stok", f"{self.products[product_code]['name']} - Tambah {tambahan} (Total: {self.products[product_code]['stock']})")
                print(f"\nStok {self.products[product_code]['name']} berhasil ditambahkan sebanyak {tambahan}. \nTotal stok {self.products[product_code]['name']}: {self.products[product_code]['stock']}.")
                return True
        else:
            # Jika kode produk tidak valid, tampilkan pesan kesalahan.
            print("Kode produk tidak valid.")
            return False
        
    def kurangi_stok(self, product_code, pengurangan, log):
        # Fungsi untuk mengurangi stok suatu produk.
        # Parameter:
        # - product_code: Kode produk yang ingin dikurangi stoknya.
        # - pengurangan: Jumlah stok yang ingin dikurangi.
        # - log: Objek LogAktivitas untuk mencatat riwayat pengurangan stok.

        if product_code in self.products:
            current_stock = self.products[product_code]["stock"]
            if current_stock - pengurangan < 0:
                # Jika total stok melebihi kapasitas minimum (0), tampilkan pesan peringatan.
                print(f"\nPengurangan stok melebihi jumlah stok yang tersedia saat ini. \nStok saat ini\t: {current_stock} \nPengurangan\t: {pengurangan}")
                print("Pengurangan stok produk tidak dapat dilakukan!")
                return False
            else:
                # Jika kapasitas mencukupi, kurangi stok dan catat riwayatnya.
                self.products[product_code]["stock"] -= pengurangan
                self.save_products()
                log.add_log("Kurangi Stok", f"{self.products[product_code]['name']} - Pengurangan {pengurangan} (Total: {self.products[product_code]['stock']})")
                print(f"\nStok {self.products[product_code]['name']} berhasil dikurangi sebanyak {pengurangan}. \nTotal stok {self.products[product_code]['name']}: {self.products[product_code]['stock']}")
                return True
        else:
            # Jika kode produk tidak valid, tampilkan pesan kesalahan.
            print("Kode produk tidak valid.")
            return False
    
    def atur_expired(self, product_code, expired_baru, log):
        import re       
        # Fungsi untuk mengatur expired baru suatu produk.
        # Parameter:
        # - product_code: Kode produk yang ingin dikurangi stoknya.
        # - expired_baru: Batas kadaluarsa baru suatu produk setelah diganti dengan produk baru.
        # - log: Objek LogAktivitas untuk mencatat riwayat pengurangan stok.
            # Validasi input hanya berupa bulan dan tahun
        pattern = r"^(0[1-9]|1[0-2])\/\d{2}$"
        if not re.match(pattern, expired_baru):
            print("Input tidak valid. Format kadaluarsa harus berupa 'MM/YY' (contoh: 07/25).")
            return False

        if product_code in self.products:
            # Perbarui data expired pada produk
            self.products[product_code]["expired"] = expired_baru
            self.save_products()
            log.add_log("Update Expired", f"Produk {self.products[product_code]['name']} -> {expired_baru}")
            print("Tanggal expired berhasil diperbarui.")
            return True
        else:
            print("Kode produk tidak valid.")
            return False

    def tambahkan_produk_baru(self, code, name, price, stock, expired):
        # Menambahkan produk baru ke vending machine.
        self.products[code] = {
            "name": name,  # Nama produk.
            "price": price,  # Harga produk.
            "stock": stock,  # Jumlah stok produk.
            "expired": expired  # Tanggal expired produk.
        }
        self.save_products()  # Menyimpan data produk ke file.
        print(f"Produk baru {name} berhasil ditambahkan.")  # Menampilkan pesan sukses.

class LogAktivitas:
    def __init__(self, log_file="log_aktivitas.csv"):
        # Inisialisasi atribut untuk mencatat log aktivitas.
        self.log_file = log_file  # Menyimpan nama file CSV untuk menyimpan data log aktivitas.
        self.history = []  # List untuk menyimpan riwayat aktivitas selama runtime program.

    def add_log(self, action, detail):
        # Fungsi untuk menambahkan entri log ke dalam riwayat aktivitas.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
        # Mendapatkan waktu saat ini dalam format YYYY-MM-DD HH:MM:SS.

        entry = {"timestamp": timestamp, "action": action, "detail": detail}  
        # Membuat dictionary untuk menyimpan data log: waktu, aksi, dan detail.

        self.history.append(entry)  
        # Menambahkan entri log ke dalam list history untuk mencatat aktivitas selama runtime.

        with open(self.log_file, mode='a', newline='') as file:  
            # Membuka file log dalam mode append untuk menambahkan data baru tanpa menghapus data lama.
            writer = csv.DictWriter(file, fieldnames=["timestamp", "action", "detail"])  
            # Membuat writer untuk menulis data log ke file CSV.
            
            if file.tell() == 0:  
                # Mengecek apakah file kosong. Jika iya, tambahkan header kolom.
                writer.writeheader()
            
            writer.writerow(entry)  
            # Menulis entri log ke dalam file CSV.

    def show_history(self):
        # Fungsi untuk menampilkan semua riwayat aktivitas dari file CSV.
        if not os.path.exists(self.log_file):  
            # Mengecek apakah file log ada. Jika tidak, tampilkan pesan bahwa belum ada riwayat aktivitas.
            print("Belum ada riwayat aktivitas.")
            return

        with open(self.log_file, mode='r') as file:  
            # Membuka file log dalam mode baca.
            reader = csv.DictReader(file)  
            # Membaca file CSV sebagai dictionary untuk mempermudah akses data kolom.

            print("\n| Timestamp            | Action          | Detail")
            print("|----------------------|-----------------|-------------------------------")
            for row in reader:  
                # Iterasi setiap baris dalam file log dan menampilkan data ke layar.
                print(f"| {row['timestamp']:<20} | {row['action']:<15} | {row['detail']:<30}")

class SistemPembayaran:
    # Kelas untuk mengatur berbagai metode pembayaran dalam sistem vending machine.

    def __init__(self, kembalian, akun):
        # Konstruktor untuk menginisialisasi objek SistemPembayaran.
        # Parameter:
        # - kembalian: Objek dari kelas SistemKembalian untuk mengatur uang kembalian.
        # - akun: Objek dari kelas Akun untuk mengatur akun pelanggan.
        self.saldo = 10000  # Saldo awal sistem, digunakan untuk simulasi (tidak terkait langsung dengan pengguna).
        self.kembalian = kembalian  # Referensi ke sistem kembalian untuk memproses pembayaran tunai.
        self.akun = akun  # Referensi ke sistem akun untuk memproses pembayaran dengan saldo MyPay.

    def bayar_dengan_saldo(self, total_harga):
        # Metode untuk memproses pembayaran menggunakan saldo MyPay pengguna.
        # Parameter:
        # - total_harga: Jumlah total harga yang harus dibayar.
        if not self.akun.logged_in_user:
            # Jika pengguna belum login, tampilkan pesan dan batalkan pembayaran.
            print("\nAnda belum login. Silakan login terlebih dahulu untuk menggunakan saldo MyPay.")
            return False
        
        if self.akun.logged_in_user and int(self.akun.logged_in_user['saldo']) >= total_harga:
            # Jika saldo pengguna mencukupi, kurangi saldo dengan total harga.
            self.akun.logged_in_user['saldo'] = int(self.akun.logged_in_user['saldo']) - total_harga
            print(f"Pembayaran berhasil menggunakan saldo MyPay. Sisa saldo: Rp{self.akun.logged_in_user['saldo']}.")      
            self.akun.update_saldo_csv()  # Perbarui saldo pengguna di file CSV.
            return True
        else:
            # Jika saldo tidak mencukupi, tampilkan pesan kesalahan.
            print("Saldo MyPay tidak mencukupi.")
            return False

    def generate_qris_ascii(self, data):
        # Metode untuk membuat dan menampilkan QR code ASCII untuk pembayaran QRIS.
        # Parameter:
        # - data: Informasi yang dikodekan ke dalam QR code.
        import qrcode  # Mengimpor library untuk membuat QR code.
        qr = qrcode.QRCode(
            version=1,  # Menentukan versi QR code (1 adalah ukuran terkecil).
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Tingkat koreksi kesalahan rendah.
            box_size=1,  # Ukuran tiap kotak dalam QR code.
            border=1,  # Ukuran border di sekitar QR code.
        )
        qr.add_data(data)  # Menambahkan data ke dalam QR code.
        qr.make(fit=True)  # Menyesuaikan ukuran QR code.
        qr.print_ascii(tty=True)  # Menampilkan QR code dalam format ASCII.
        print("\nQRIS berhasil dibuat. Silakan pindai kode QR di atas untuk menyelesaikan pembayaran.")
        return True

    def bayar_dengan_tunai(self, total_harga):
        # Metode untuk memproses pembayaran menggunakan uang tunai.
        # Parameter:
        # - total_harga: Jumlah total harga yang harus dibayar.
        print("\nMasukkan nominal uang yang digunakan untuk membayar (gunakan pecahan Rp1000, Rp2000, Rp5000, Rp10000, Rp20000, Rp50000, Rp100000).")
        sisa_pembayaran = total_harga  # Inisialisasi sisa pembayaran dengan total harga.
        while sisa_pembayaran > 0:
            # Loop untuk meminta input uang dari pengguna hingga total pembayaran terpenuhi.
            nominal = int(input(f"Sisa pembayaran\t\t: Rp{sisa_pembayaran} \nNominal\t\t\t: Rp"))
            jumlah = int(input(f"Banyak lembar Rp{nominal}\t: "))
            total_input = nominal * jumlah  # Menghitung total uang yang dimasukkan.

            if total_input >= sisa_pembayaran:
                # Jika uang yang dimasukkan cukup atau lebih, hitung kembalian.
                kembalian = total_input - sisa_pembayaran
                if kembalian > 0:
                    print(f"Kembalian\t\t: Rp{kembalian}")
                    self.kembalian.update_kembalian(nominal, jumlah)  # Tambahkan uang kembalian ke sistem.
                print("Pembayaran berhasil!")
                return True
            else:
                # Jika uang yang dimasukkan kurang, kurangi sisa pembayaran.
                sisa_pembayaran -= total_input
                self.kembalian.update_kembalian(nominal, jumlah)  # Tambahkan uang yang diterima ke sistem.
        return True

    def proses_checkout(self, total_harga):
        # Metode untuk memproses checkout dengan memilih metode pembayaran.
        # Parameter:
        # - total_harga: Jumlah total harga yang harus dibayar.
        print("Pilih metode pembayaran:")
        print("1. MyPay (Saldo)")
        print("2. QRIS")
        print("3. Tunai")

        pilihan_pembayaran = int(input("Pilihan: "))
        if pilihan_pembayaran == 1:
            # Proses pembayaran menggunakan saldo MyPay.
            return self.bayar_dengan_saldo(total_harga)
        elif pilihan_pembayaran == 2:
            # Proses pembayaran menggunakan QRIS.
            link_qris = "https://i.imgur.com/XMC9cZy.jpeg"  # Contoh link QRIS.
            print("\nPembayaran melalui QRIS sedang diproses...")
            self.generate_qris_ascii(link_qris)  # Membuat QR code ASCII untuk QRIS.
            input("Tekan Enter setelah melakukan pembayaran.")
            print("Pembayaran dengan QRIS berhasil.")
            return True
        elif pilihan_pembayaran == 3:
            # Proses pembayaran menggunakan uang tunai.
            return self.bayar_dengan_tunai(total_harga)
        else:
            # Jika metode pembayaran tidak valid, tampilkan pesan kesalahan.
            print("\nMetode pembayaran tidak valid. Kembali ke menu pembayaran.")
            return False

class PemrosesanPesanan:
    # Kelas untuk menangani proses pemesanan, keranjang belanja, dan checkout dalam vending machine.

    def __init__(self, stok, log, pembayaran, cart_file="keranjang.csv"):
        # Konstruktor untuk menginisialisasi objek PemrosesanPesanan.
        # Parameter:
        # - stok: Objek StokBarang untuk mengelola data produk di vending machine.
        # - log: Objek LogAktivitas untuk mencatat aktivitas sistem.
        # - pembayaran: Objek SistemPembayaran untuk memproses transaksi pembayaran.
        # - cart_file: Nama file CSV untuk menyimpan data keranjang belanja (default: keranjang.csv).
        self.stok = stok  # Referensi ke objek StokBarang.
        self.log = log  # Referensi ke objek LogAktivitas.
        self.pembayaran = pembayaran  # Referensi ke objek SistemPembayaran.
        self.cart_file = cart_file  # File CSV untuk menyimpan data keranjang.
        self.cart = self.load_cart()  # Memuat data keranjang dari file CSV.
        self.total_harga = 0  # Variabel untuk menyimpan total harga barang di keranjang.

    def load_cart(self):
        # Fungsi untuk memuat data keranjang belanja dari file CSV.
        # Return: Daftar item yang ada di keranjang beserta informasi terkait.

        if not os.path.exists(self.cart_file):  # Periksa apakah file keranjang ada.
            return []  # Jika file tidak ditemukan, kembalikan daftar kosong.

        cart = []  # Inisialisasi daftar untuk menyimpan data keranjang.
        self.total_harga = 0  # Reset total harga saat memuat ulang data keranjang.

        with open(self.cart_file, mode='r') as file:  # Buka file CSV untuk membaca data.
            reader = csv.DictReader(file)  # Membaca data CSV sebagai dictionary.
            for row in reader:  # Iterasi setiap baris data di file CSV.
                try:
                    quantity = int(row["quantity"])  # Pastikan jumlah item berupa angka.
                    price = int(row["price"])  # Pastikan harga berupa angka.
                    cart.append({
                        "code": int(row["code"]),  # Tambahkan kode produk ke keranjang.
                        "name": row["name"],  # Tambahkan nama produk ke keranjang.
                        "quantity": quantity,  # Tambahkan jumlah item ke keranjang.
                        "price": price  # Tambahkan harga item ke keranjang.
                    })
                    self.total_harga += price  # Tambahkan harga item ke total harga.
                except ValueError:  # Tangkap kesalahan format data.
                    print(f"Kesalahan format data pada baris: {row}")  # Tampilkan pesan kesalahan.
                    continue  # Abaikan baris dengan format salah.

        return cart  # Kembalikan daftar keranjang belanja yang berhasil dimuat.

    def save_cart(self):
        # Fungsi untuk menyimpan data keranjang belanja ke file CSV.
        with open(self.cart_file, mode='w', newline='') as file:  # Buka file CSV untuk menulis data.
            fieldnames = ["code", "name", "quantity", "price"]  # Header kolom untuk file CSV.
            writer = csv.DictWriter(file, fieldnames=fieldnames)  # Inisialisasi writer untuk file CSV.
            writer.writeheader()  # Tulis header ke file CSV.
            for item in self.cart:  # Iterasi setiap item di keranjang.
                writer.writerow(item)  # Tulis data item ke file CSV.

    def tambah_ke_keranjang(self, product_code, quantity):
        # Fungsi untuk menambahkan produk ke keranjang belanja.
        # Parameter:
        # - product_code: Kode produk yang ingin ditambahkan.
        # - quantity: Jumlah produk yang ingin ditambahkan.
        product = self.stok.products.get(product_code)  # Dapatkan data produk berdasarkan kode.
        if not product or product["stock"] < quantity:  # Periksa apakah stok mencukupi.
            print(f"Stok tidak cukup untuk {product['name']}!")  # Tampilkan pesan jika stok kurang.
            return False  # Gagal menambahkan ke keranjang.

        product_in_cart = next((item for item in self.cart if item["code"] == product_code), None)  
        # Periksa apakah produk sudah ada di keranjang.
        if product_in_cart:  # Jika produk sudah ada di keranjang.
            product_in_cart["quantity"] += quantity  # Tambahkan jumlah produk di keranjang.
            product_in_cart["price"] += product["price"] * quantity  # Hitung ulang harga total produk.
        else:
            self.cart.append({
                "code": product_code,
                "name": product["name"],
                "quantity": quantity,
                "price": product["price"] * quantity
            })  # Tambahkan produk baru ke keranjang.

        self.stok.products[product_code]["stock"] -= quantity  # Kurangi stok produk di vending machine.
        self.total_harga = sum(item["price"] for item in self.cart)  # Hitung ulang total harga keranjang.
        self.save_cart()  # Simpan data keranjang ke file CSV.
        self.stok.save_products()  # Simpan perubahan stok ke file CSV.

        print(f"{quantity} {product['name']} telah ditambahkan ke keranjang. Total sementara: Rp{self.total_harga}")
        return True  # Berhasil menambahkan ke keranjang.

    def kurangi_dari_keranjang(self, product_code, quantity):
        # Fungsi untuk mengurangi produk dari keranjang belanja.
        # Parameter:
        # - product_code: Kode produk yang ingin dikurangi.
        # - quantity: Jumlah produk yang ingin dikurangi.
        product = self.stok.products.get(product_code)  # Dapatkan data produk berdasarkan kode.
        product_in_cart = next((item for item in self.cart if item["code"] == product_code), None)  
        # Cari produk di keranjang berdasarkan kode.
        if product_in_cart:  # Jika produk ditemukan di keranjang.
            if product_in_cart["quantity"] > quantity:  # Jika jumlah di keranjang lebih dari yang ingin dikurangi.
                product_in_cart["quantity"] -= quantity  # Kurangi jumlah produk di keranjang.
                product_in_cart["price"] -= quantity * product["price"]  # Hitung ulang harga total produk.
                self.stok.products[product_code]["stock"] += quantity  # Tambahkan kembali stok ke vending machine.
                self.save_cart()  # Simpan perubahan ke file CSV.
                print(f"{quantity} dari {product_in_cart['name']} dikurangi di keranjang.")
            elif product_in_cart["quantity"] == quantity:  # Jika jumlah yang ingin dikurangi sama dengan yang di keranjang.
                self.cart.remove(product_in_cart)  # Hapus produk dari keranjang.
                self.stok.products[product_code]["stock"] += quantity  # Tambahkan kembali stok ke vending machine.
                self.stok.save_products()  # Simpan perubahan stok ke file CSV.
                print(f"{product_in_cart['name']} dihapus dari keranjang.")
            else:
                print(f"Tidak bisa mengurangi lebih dari kuantitas yang ada di keranjang.")  # Jumlah melebihi kuantitas di keranjang.
        else:
            print(f"Item {product_code} tidak ditemukan di keranjang.")  # Produk tidak ditemukan di keranjang.

    def cek_keranjang(self):
        # Fungsi untuk memeriksa apakah keranjang belanja kosong.
        if not self.cart:  # Jika keranjang kosong.
            print("\n" + "Keranjang Anda kosong.\n".center(55))  # Tampilkan pesan bahwa keranjang kosong.
            return False  # Keranjang kosong.
        else:
            return True  # Keranjang berisi item.

    def tampilkan_keranjang(self):
        # Fungsi untuk menampilkan isi keranjang belanja.
        self.total_harga = sum(item['price'] for item in self.cart)  # Hitung ulang total harga.
        print("\n|---------------------------------------------------|")
        print("|                   KERANJANG BELANJA               |")
        print("|---------------------------------------------------|")
        print("| Kode | Nama Produk           | Jumlah | Harga     |")
        print("|---------------------------------------------------|")
        for item in self.cart:  # Iterasi setiap item di keranjang.
            print(f"| {item['code']:<4} | {item['name']:<21} | {'x' + str(item['quantity']):^6} | Rp{item['price']:<7} |")
        print("|---------------------------------------------------|")
        print(f"| Total Harga: {' ':<25}  Rp{self.total_harga:<7} |")  # Tampilkan total harga.
        print("|---------------------------------------------------|\n")

    def proses_checkout(self):
        # Fungsi untuk memproses pembayaran keranjang belanja.
        if not self.cart:  # Periksa apakah keranjang kosong.
            print("Keranjang Anda kosong. Tambahkan produk terlebih dahulu.\n")  # Tampilkan pesan jika kosong.
            return

        self.tampilkan_keranjang()  # Tampilkan isi keranjang.

        if self.pembayaran.proses_checkout(self.total_harga):  # Proses pembayaran.
            for item in self.cart:  # Catat riwayat pembelian.
                self.log.add_log("Pembelian", f"{item['name']} x{item['quantity']} - Rp{item['price']}")
            self.cetak_struk()  # Cetak struk pembayaran.
            print("\nTransaksi berhasil!")  # Tampilkan pesan berhasil.

            self.cart.clear()  # Kosongkan keranjang.
            self.total_harga = 0  # Reset total harga.
            self.save_cart()  # Simpan perubahan keranjang.
            self.stok.save_products()  # Simpan perubahan stok.
            feedback_handler = Feedback()  # Inisialisasi handler feedback.
            while True:
                try:
                    rating = int(input("\nSilakan beri rating (1-5): ").strip())  # Minta input rating.
                    if rating < 1 or rating > 5:
                        raise ValueError("Rating harus antara 1 hingga 5.")  # Validasi rating.
                    break
                except ValueError:
                    print("Input tidak valid. Masukkan angka 1 sampai 5.")  # Tampilkan pesan error.

            feedback = input("Silakan tuliskan feedback Anda: ").strip()  # Minta feedback dari pengguna.
            feedback_handler.save_feedback(rating, feedback)  # Simpan feedback ke sistem.
            print("Feedback Anda telah tersimpan. Terima kasih telah berbelanja di MyVending. Sampai jumpa lagi!")
        else:
            print("Pembayaran gagal. Silakan coba lagi.")  # Tampilkan pesan jika pembayaran gagal.

    def cetak_struk(self):
        # Fungsi untuk mencetak struk pembayaran.
        print("\n|================= STRUK PEMBAYARAN ================|")
        print(f"| Waktu Transaksi:              {time.strftime('%Y-%m-%d %H:%M:%S')} |")  # Tampilkan waktu transaksi.
        print("|---------------------------------------------------|")
        print("| Produk               | Jumlah | Harga Total       |")
        print("|---------------------------------------------------|")
        for item in self.cart:  # Iterasi setiap item di keranjang.
            print(f"| {item['name']:<20} | {item['quantity']:<6} | Rp{item['price']:<15} |")
        print("|---------------------------------------------------|")
        print(f"| Total Harga: {' ':<18} Rp{self.total_harga:<15} |")  # Tampilkan total harga.
        print("|---------------------------------------------------|")
        print("|    Terima kasih telah berbelanja di MYVENDING!    |")  # Tampilkan pesan terima kasih.
        print("|===================================================|")

class Akun:
    # Kelas untuk mengelola akun pengguna, termasuk login, logout, pembuatan akun, dan pengelolaan saldo.

    def __init__(self):
        # Konstruktor untuk menginisialisasi objek Akun.
        self.logged_in_user = None  # Variabel untuk menyimpan data pengguna yang sedang login.

    def login(self):
        # Metode untuk menangani proses login pengguna.
        if self.logged_in_user:
            # Jika pengguna sudah login, tampilkan pesan peringatan.
            print("\nAnda sudah login. Silakan logout terlebih dahulu untuk login dengan akun lain.\n")
            return
        
        # Meminta input username dan password dari pengguna.
        username = input("\nUsername\t: ")
        password = getpass.getpass("Password (hide)\t: ")  # Menggunakan getpass untuk menyembunyikan input password.
        
        # Membuka file CSV yang menyimpan data akun untuk verifikasi.
        with open('accounts.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    # Jika username dan password cocok, login berhasil.
                    self.logged_in_user = row  # Simpan data akun yang login.
                    print("Login berhasil!")
                    print(f"Saldo saat ini: Rp{row['saldo']}\n")
                    return True
            # Jika username atau password salah, tampilkan pesan kesalahan.
            print("Username atau password salah.\n")
            return False

    def buat_akun_baru(self):
        # Metode untuk membuat akun baru.
        if self.logged_in_user:
            # Jika pengguna sudah login, tampilkan pesan peringatan.
            print("\nAnda sudah login. Silakan logout terlebih dahulu untuk membuat akun baru.\n")
            return
        
        # Meminta input username baru dari pengguna.
        username = input("\nUsername baru\t: ")
        
        # Periksa apakah username sudah ada dalam file CSV.
        with open('accounts.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    # Jika username sudah digunakan, tampilkan pesan kesalahan.
                    print("Username sudah digunakan. Silakan pilih yang lain.\n")
                    return
        
        # Meminta input password baru dan mengatur saldo awal ke Rp0.
        password = input("Password baru\t: ")
        saldo = 0  # Set saldo awal ke Rp0.

        # Menyimpan data akun baru ke file CSV.
        with open('accounts.csv', mode='a', newline='') as csvfile:
            fieldnames = ['username', 'password', 'saldo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Jika file kosong, tulis header.
            csvfile.seek(0, os.SEEK_END)
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerow({'username': username, 'password': password, 'saldo': saldo})
        
        print("- Akun berhasil dibuat dengan saldo Rp0. Tambahkan saldo melalui menu Tambah Saldo MyPay -")

    def tambah_saldo_mypay(self):
        # Metode untuk menambah saldo MyPay akun pengguna.
        if not self.logged_in_user:
            # Jika pengguna belum login, tampilkan pesan peringatan.
            print("\nAnda harus login terlebih dahulu untuk menambah saldo.\n")
            return

        # Meminta pengguna memilih metode pembayaran.
        metode = input("\nPilih metode tambah saldo (Gopay/Ovo/Dana): ").strip().lower()
        if metode not in ['gopay', 'ovo', 'dana']:
            # Jika metode tidak valid, tampilkan pesan kesalahan.
            print("Metode tidak valid. Silakan pilih kembali.\n")
            return

        # Meminta input nominal saldo yang ingin ditambahkan.
        try:
            amount = int(input("Nominal tambah\t: "))
            if amount <= 0:
                # Jika nominal tidak valid, tampilkan pesan kesalahan.
                print("Nominal tidak valid. Harap masukkan angka positif.")
                return
        except ValueError:
            # Jika input bukan angka, tampilkan pesan kesalahan.
            print("Input tidak valid. Harap masukkan angka.")
            return

        # Konfirmasi dengan PIN setelah memilih metode pembayaran.
        pin = getpass.getpass("PIN\t\t: ")
        if pin != self.logged_in_user['password']:
            # Jika PIN salah, tampilkan pesan kesalahan.
            print("PIN salah. Tidak dapat melanjutkan penambahan saldo.\n")
            return

        # Simulasi pembayaran berhasil.
        print(f"Silakan transfer Rp{amount} melalui {metode.capitalize()}.\n")
        konfirmasi = input("Ketik 'YA' jika sudah melakukan pembayaran: ").strip().upper()
        if konfirmasi == 'YA':
            # Jika pembayaran berhasil, tambahkan saldo pengguna dan perbarui di file CSV.
            self.logged_in_user['saldo'] = str(int(self.logged_in_user['saldo']) + amount)
            self.update_saldo_csv()
            print(f"Saldo sebesar Rp{amount} berhasil ditambahkan. Saldo saat ini: Rp{self.logged_in_user['saldo']}\n")
        else:
            # Jika pembayaran belum dikonfirmasi, tampilkan pesan.
            print("Pembayaran belum dikonfirmasi.\n")

    def tarik_saldo_mypay(self):
        # Metode untuk menarik saldo dari akun MyPay pengguna.
        if not self.logged_in_user:
            # Jika pengguna belum login, tampilkan pesan peringatan.
            print("Anda harus login terlebih dahulu untuk menarik saldo.")
            return

        # Meminta input nominal saldo yang ingin ditarik.
        try:
            amount = int(input("Nominal tarik\t: "))
            if amount <= 0:
                # Jika nominal tidak valid, tampilkan pesan kesalahan.
                print("Nominal tidak valid. Harap masukkan angka positif.")
                return
        except ValueError:
            # Jika input bukan angka, tampilkan pesan kesalahan.
            print("Input tidak valid. Harap masukkan angka.")
            return

        # Konfirmasi dengan PIN sebelum menarik saldo.
        pin = getpass.getpass("PIN\t\t: ")
        if pin != self.logged_in_user['password']:
            # Jika PIN salah, tampilkan pesan kesalahan.
            print("PIN salah. Tidak dapat melanjutkan penarikan saldo.")
            return

        if int(self.logged_in_user['saldo']) >= amount:
            # Jika saldo mencukupi, kurangi saldo pengguna dan perbarui di file CSV.
            self.logged_in_user['saldo'] = str(int(self.logged_in_user['saldo']) - amount)
            self.update_saldo_csv()
            print(f"Tarik saldo sebesar Rp{amount} berhasil. Saldo sekarang: Rp{self.logged_in_user['saldo']}")
        else:
            # Jika saldo tidak mencukupi, tampilkan pesan kesalahan.
            print("Saldo tidak mencukupi.")

    def logout(self):
        # Metode untuk logout dari akun yang sedang login.
        if self.logged_in_user:
            # Jika ada pengguna yang login, konfirmasi sebelum logout.
            konfirmasi = input("\nApakah Anda yakin untuk logout? Ketik 'YA' untuk konfirmasi: ").strip().upper()
            if konfirmasi == 'YA':
                # Jika pengguna mengonfirmasi, logout berhasil.
                print(f"Anda telah logout dari akun {self.logged_in_user['username']}.")
                self.logged_in_user = None
            else:
                # Jika pengguna membatalkan, tampilkan pesan.
                print("Logout dibatalkan.")
        else:
            # Jika belum ada pengguna yang login, tampilkan pesan.
            print("\nAnda belum login.")

    def cek_akun(self):
        # Metode untuk menampilkan informasi akun yang sedang login.
        if not self.logged_in_user:
            # Jika belum ada pengguna yang login, tampilkan pesan.
            print("\nAnda belum login. Silakan login terlebih dahulu.")
            return

        # Menampilkan informasi akun pengguna yang sedang login.
        print("\n|===================== INFORMASI AKUN =====================|")
        print(f"| Username\t: {self.logged_in_user['username']:<40} |")
        print(f"| Saldo MyPay\t: Rp{self.logged_in_user['saldo']:<38} |")
        print("|==========================================================|")

    def update_saldo_csv(self):
        # Metode untuk memperbarui saldo akun yang sedang login di file accounts.csv.
        if not self.logged_in_user:
            # Jika tidak ada akun yang login, tampilkan pesan kesalahan.
            print("\nTidak ada akun yang login. Tidak dapat memperbarui saldo.")
            return

        # Membaca semua data akun dari file CSV.
        with open('accounts.csv', mode='r') as csvfile:
            rows = list(csv.DictReader(csvfile))
        
        # Memperbarui saldo akun yang sedang login.
        for row in rows:
            if row['username'] == self.logged_in_user['username']:
                row['saldo'] = self.logged_in_user['saldo']
                break

        # Menulis ulang file CSV dengan saldo yang diperbarui.
        with open('accounts.csv', mode='w', newline='') as csvfile:
            fieldnames = ['username', 'password', 'saldo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

class MyVendingStatus:
    # Kelas untuk mengelola status MyVending, seperti suhu dan kelembapan.

    def __init__(self):
        # Konstruktor untuk menginisialisasi status awal MyVending.
        self.suhu = 5  # Inisialisasi suhu awal dalam derajat Celsius.
        self.kelembapan = 50  # Inisialisasi kelembapan awal dalam persentase.

    def display_status(self):
        # Metode untuk menampilkan status MyVending dalam format visual.
        print("\n==========================================")
        print("||==================||==================||")
        print(f"||                  || Suhu  || {self.suhu:5}°C ||")  # Menampilkan suhu saat ini.
        print(f"||     MyVending    || Waktu ||   {time.strftime('%H:%M')} ||")  # Menampilkan waktu saat ini.
        print(f"||                  || Mois  || {self.kelembapan:6}% ||")  # Menampilkan kelembapan saat ini.
        print("||==================||==================||")

        # Menentukan status berdasarkan kondisi suhu dan kelembapan.
        if self.suhu < 0:
            print("|| Status : Overfreeze                  ||")  # Status jika suhu terlalu rendah.
        elif self.suhu < 0 and self.kelembapan > 70:
            print("|| Status : Overfreeze, Hiperhumida     ||")  # Status jika suhu rendah dan kelembapan tinggi.
        elif self.suhu > 10:
            print("|| Status : Overheat                    ||")  # Status jika suhu terlalu tinggi.
        elif self.suhu > 10 and self.kelembapan > 70:
            print("|| Status : Overheat, Hiperhumida       ||")  # Status jika suhu tinggi dan kelembapan tinggi.
        else:
            print("|| Status : Normal                      ||")  # Status normal.
        print("==========================================")

    def set_suhu(self, perubahan):
        # Metode untuk mengatur suhu MyVending.
        lanjut = 'n'  # Variabel untuk mengontrol pengulangan.
        cek_suhu = self.suhu + perubahan  # Menghitung suhu baru berdasarkan perubahan.

        if 0 <= cek_suhu <= 10:
            # Jika suhu baru berada dalam batas aman, perbarui suhu.
            self.suhu += perubahan
            print(f"Suhu berhasil diubah menjadi {self.suhu}°C.")
        else:
            # Jika suhu baru berada di luar batas, tampilkan peringatan.
            while lanjut == 'n':
                if cek_suhu > 10:
                    print("\nPERINGATAN: \nSuhu terlalu tinggi, minuman akan tidak dingin.")
                elif cek_suhu < 0:
                    print("\nPERINGATAN: \nSuhu terlalu rendah, minuman akan beku.")
                
                # Meminta konfirmasi dari pengguna apakah ingin melanjutkan perubahan.
                lanjut = input("\nApakah Anda ingin melanjutkan?(y/n) ").lower()
                if lanjut == 'y':
                    # Jika pengguna mengonfirmasi, perbarui suhu.
                    self.suhu += perubahan
                    print(f"Suhu berhasil diubah menjadi {self.suhu}°C.")
                    break
                elif lanjut == 'n':
                    # Jika pengguna membatalkan, batalkan perubahan suhu.
                    print("Perubahan suhu dibatalkan!")
                    break

    def set_kelembapan(self, perubahan):
        # Metode untuk mengatur kelembapan MyVending.
        cek_kelembapan = self.kelembapan + perubahan  # Menghitung kelembapan baru berdasarkan perubahan.

        if 0 <= cek_kelembapan <= 70:
            # Jika kelembapan baru berada dalam batas aman, perbarui kelembapan.
            self.kelembapan += perubahan
            print(f"Kelembapan berhasil diubah menjadi {self.kelembapan}%.")
        elif cek_kelembapan < 0 or cek_kelembapan > 100:
            # Jika kelembapan baru di luar batas, tampilkan pesan kesalahan.
            print("Perubahan kelembapan melebihi batas. Perubahan tidak dapat dilakukan!")
        else:
            # Jika kelembapan tinggi, tampilkan peringatan.
            lanjut = 'n'  # Variabel untuk mengontrol pengulangan.
            while lanjut == 'n':
                if cek_kelembapan > 70:
                    print("\nPERINGATAN: \nKelembapan terlalu tinggi, ini akan mempercepat pertumbuhan jamur.")

                # Meminta konfirmasi dari pengguna apakah ingin melanjutkan perubahan.
                lanjut = input("\nApakah Anda ingin melanjutkan?(y/n) ").lower()
                if lanjut == 'y':
                    # Jika pengguna mengonfirmasi, perbarui kelembapan.
                    self.kelembapan += perubahan
                    print(f"Kelembapan berhasil diubah menjadi {self.kelembapan}%.")
                    break
                elif lanjut == 'n':
                    # Jika pengguna membatalkan, batalkan perubahan kelembapan.
                    print("Perubahan kelembapan dibatalkan!")
                    break

class SistemKembalian:
    # Kelas untuk mengelola sistem kembalian tunai di MyVending.

    def __init__(self, file_csv="kembalian.csv"):
        # Konstruktor untuk menginisialisasi data kembalian dari file CSV.
        self.file_csv = file_csv  # Nama file untuk menyimpan data kembalian.
        self.saldo = self._load_saldo()  # Memuat saldo kembalian dari file.

    def _load_saldo(self):
        # Metode untuk membaca saldo kembalian dari file CSV.
        saldo = {}  # Inisialisasi dictionary untuk menyimpan data nominal dan jumlah.
        try:
            with open(self.file_csv, mode='r') as file:
                reader = csv.DictReader(file)  # Membaca file CSV sebagai dictionary.
                for row in reader:
                    if "nominal" in row and "jumlah" in row:  # Validasi kolom CSV.
                        nominal = int(row["nominal"])  # Konversi nominal ke integer.
                        jumlah = int(row["jumlah"])  # Konversi jumlah ke integer.
                        saldo[nominal] = jumlah  # Simpan data ke dictionary.
                    else:
                        raise ValueError("Header CSV tidak valid. Diperlukan 'nominal' dan 'jumlah'.")
        except (FileNotFoundError, ValueError):
            # Jika file tidak ditemukan atau format tidak valid, buat file baru.
            print(f"File {self.file_csv} tidak ditemukan atau tidak valid. Membuat file baru...")
            self._initialize_csv()
            saldo = self._load_saldo()  # Reload data setelah inisialisasi file.
        return saldo

    def _initialize_csv(self):
        # Metode untuk membuat file CSV baru dengan format default.
        with open(self.file_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["nominal", "jumlah"])
            writer.writeheader()  # Tulis header file CSV.
            # Menulis data default untuk setiap nominal uang.
            for nominal in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
                writer.writerow({"nominal": nominal, "jumlah": 0})

    def cek_saldo_kembalian(self):
        # Metode untuk menampilkan saldo kembalian tunai secara visual.
        print("\n||  Saldo Kembalian Tunai  ||")
        print("||-------------------------||")
        total_saldo = 0  # Inisialisasi total saldo.
        for nominal, jumlah in sorted(self.saldo.items()):  # Iterasi data berdasarkan nominal.
            print(f"|| Rp{nominal:<7} | {jumlah:<4} lembar ||")  # Menampilkan nominal dan jumlah uang.
            total_saldo += nominal * jumlah  # Menghitung total saldo.
        print("||-------------------------||")
        print(f"|| Total Saldo: Rp{total_saldo:<8} ||")  # Menampilkan total saldo keseluruhan.
        print("||-------------------------||")

    def update_kembalian(self, nominal, jumlah):
        # Metode untuk memperbarui saldo kembalian berdasarkan nominal dan jumlah.
        if nominal in self.saldo:
            self.saldo[nominal] += jumlah  # Menambahkan jumlah kembalian untuk nominal tertentu.
        else:
            self.saldo[nominal] = jumlah  # Menambahkan nominal baru ke saldo.

        # Menyimpan perubahan ke file CSV.
        with open(self.file_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["nominal", "jumlah"])
            writer.writeheader()  # Tulis header file CSV.
            for nominal, jumlah in self.saldo.items():
                writer.writerow({"nominal": nominal, "jumlah": jumlah})

    def tambah_saldo(self, nominal, jumlah):
        # Metode untuk menambahkan saldo kembalian secara manual.
        print(f"Menambahkan Rp{nominal} x{jumlah} ke saldo kembalian.")
        self.update_kembalian(nominal, jumlah)  # Memperbarui data kembalian.

class Feedback:
    # Kelas untuk menangani penyimpanan dan penampilan feedback pengguna.

    def __init__(self, file_name="feedback.csv"):
        # Konstruktor untuk menginisialisasi objek Feedback.
        # Parameter:
        # - file_name: Nama file CSV tempat feedback disimpan.
        self.file_name = file_name

    def save_feedback(self, rating, feedback):
        # Metode untuk menyimpan feedback pengguna ke file CSV.
        # Parameter:
        # - rating: Penilaian pengguna dalam bentuk angka (1-5).
        # - feedback: Ulasan atau komentar pengguna dalam bentuk teks.
        with open(self.file_name, mode='a', newline='') as file:
            writer = csv.writer(file)  # Menggunakan csv.writer untuk menulis data ke file.
            writer.writerow([rating, feedback])  # Menulis baris baru berisi rating dan feedback ke file.
        print("Terima kasih atas feedback Anda!")  # Menampilkan pesan sukses.

    def display_feedback(self):
        # Metode untuk menampilkan semua feedback yang telah disimpan.
        try:
            # Membuka file CSV dan membaca feedback yang tersedia.
            with open(self.file_name, mode='r') as file:
                reader = csv.reader(file)  # Membaca data dari file dengan csv.reader.
                for idx, row in enumerate(reader, start=1):
                    # Menampilkan setiap feedback dengan format tertentu.
                    print(f"\nFeedback {idx} dari Anonim")
                    print(f"Rating\t\t: {row[0]} \nFeedback\t: {row[1]}\n")
        except FileNotFoundError:
            # Jika file tidak ditemukan, tampilkan pesan bahwa belum ada feedback.
            print("\nBelum ada feedback yang tersedia.")

def main():
    # Inisialisasi objek untuk berbagai kelas yang digunakan dalam program
    stok = StokBarang()  # Digunakan untuk mengelola stok produk
    log = LogAktivitas()  # Untuk mencatat dan menampilkan log aktivitas
    kembalian = SistemKembalian("kembalian.csv")  # Membaca dan mengelola saldo kembalian dari file CSV
    akun = Akun()  # Mengelola akun pengguna, seperti login dan saldo
    pembayaran = SistemPembayaran(kembalian, akun)  # Untuk mengatur berbagai metode pembayaran
    pesanan = PemrosesanPesanan(stok, log, pembayaran)  # Memproses transaksi, keranjang, dan checkout
    vending_status = MyVendingStatus()  # Untuk memantau status vending machine (suhu dan kelembapan)
    feedback_handler = Feedback()  # Menyimpan masukan feedback pengguna

    admin_password = "Admin#123"  # Password untuk akses menu admin

    while True:
        clear_screen()

        # Menampilkan header utama dengan sapaan selamat datang
        print("||=================================================||")
        print("||               SELAMAT DATANG DI MYVENDING       ||")
        print("||=================================================||")
        print("||                Selamat berbelanja!              ||")
        print("||=================================================||\n")
        
        # Menampilkan daftar produk yang tersedia
        stok.display_products()
        
        # Menampilkan menu utama untuk memilih fitur
        print("\n||=================================================||")
        print("||                    MENU UTAMA                   ||")
        print("||=================================================||")
        print("1. Belanja Produk")  # Opsi untuk belanja produk
        print("2. Login Akun")  # Opsi untuk login atau membuat akun baru
        print("3. Menu Admin")  # Akses khusus admin dengan password
        print("4. Lihat Feedback")  # Melihat feedback dari pengguna 
        print("5. Keluar")  # Keluar dari program
        print("----------------------------------------------------")
        
        pilihan_menu = int(input("Pilihan: "))  # Input untuk memilih menu utama

        if pilihan_menu == 1:  # Jika memilih belanja produk
            while True:  # Loop untuk menu belanja
                clear_screen()  # Membersihkan layar sebelum menampilkan daftar produk
                print("||=================================================||")
                print("||                    MY VENDING                   ||".center(49))
                print("||               Menu Belanja Produk               ||".center(49))
                print("||=================================================||\n")
                
                stok.display_products()  # Menampilkan daftar produk dari stok
                print("\n1. Tambahkan Produk ke Keranjang")  # Opsi untuk menambah produk ke keranjang
                print("2. Pembayaran")  # Opsi untuk melanjutkan ke proses pembayaran
                print("3. Cek Keranjang")  # Opsi untuk melihat isi keranjang belanja
                print("4. Kurangi produk dari Keranjang")  # Opsi untuk mengurangi produk dari keranjang
                print("5. Kembali ke Menu Utama")  # Opsi untuk kembali ke menu utama

                pilihan_menubelanja = int(input("Pilihan: "))  # Input pilihan menu belanja

                if pilihan_menubelanja == 1:  # Jika memilih menambah produk ke keranjang
                    ulang = "y"  # Variabel untuk mengulang proses penambahan produk
                    while ulang.lower() == "y":  # Selama pengguna menjawab "y", proses terus berjalan
                        clear_screen()  # Membersihkan layar sebelum menampilkan daftar produk
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||         Penambahan Produk ke Keranjang          ||".center(49))
                        print("||=================================================||\n")
                        stok.display_products()  # Menampilkan daftar produk yang tersedia
                        try:
                            kode_produk = int(input("\nKode produk\t\t: "))  # Input kode produk dari pengguna
                            if kode_produk in stok.products:  # Memastikan kode produk valid
                                kuantitas_produk = int(input("Kuantitas produk\t: "))  # Input jumlah produk yang ingin ditambahkan
                                if kuantitas_produk <= 0:  # Validasi jika jumlah kurang atau sama dengan nol
                                    print("Kuantitas produk tidak valid!")  # Pesan error untuk jumlah tidak valid
                                    continue  # Kembali ke awal loop
                                pesanan.tambah_ke_keranjang(kode_produk, kuantitas_produk)  # Tambahkan produk ke keranjang
                                ulang = input("Apakah Anda ingin menambahkan produk lainnya ke keranjang (y/n)? ").lower()  # Tanyakan apakah ingin menambahkan produk lain
                                while ulang not in ['y', 'n']:  # Validasi input harus "y" atau "n"
                                    print("Pilihan tidak valid. Harap jawab dengan 'y' atau 'n'.")  # Pesan error untuk input tidak valid
                                    ulang = input("Apakah Anda ingin menambahkan produk lainnya ke keranjang (y/n)? ").lower()  # Input ulang
                            else:
                                print("Kode produk tidak valid. Harap masukkan kode yang tersedia pada daftar.\n")  # Pesan error jika kode produk tidak ditemukan
                                break  # Kembali ke menu belanja
                        except ValueError:
                            print("Input tidak valid. Masukkan angka.")  # Pesan error jika input bukan angka

                elif pilihan_menubelanja == 2:  # Proses pembayaran
                    clear_screen()  # Membersihkan layar
                    print("||=================================================||")
                    print("||                    MY VENDING                   ||".center(49))
                    print("||                    Pembayaran                   ||".center(49))
                    print("||=================================================||")
                    while True:
                        if pesanan.cek_keranjang():  # Cek apakah keranjang tidak kosong
                            if pesanan.proses_checkout() == True:  # Jika proses checkout berhasil
                                ulang = "y"  # Variabel untuk menanyakan apakah ingin memberikan feedback
                                while ulang.lower() == "y":  # Selama pengguna menjawab "y"
                                    ulang = input("Apakah Anda ingin memberikan feedback untuk kami (y/n)? ")
                                    if ulang == "y":  # Jika pengguna ingin memberikan feedback
                                        while True:
                                            try:
                                                rating = int(input("\nSilakan beri rating (1-5): ").strip())  # Input rating pengguna
                                                if rating < 1 or rating > 5:  # Validasi rating harus dalam rentang 1-5
                                                    raise ValueError("Rating harus antara 1 hingga 5.")  # Pesan error jika tidak valid
                                                break
                                            except ValueError:
                                                print("Input tidak valid. Masukkan angka 1 sampai 5.")  # Pesan error jika bukan angka
                                                
                                        feedback = input("Silakan tuliskan feedback Anda: ").strip()  # Input feedback pengguna
                                        feedback_handler.save_feedback(rating, feedback)  # Simpan feedback ke file
                                        print("Feedback Anda telah tersimpan. Terima kasih telah berbelanja di MyVending. Sampai jumpa lagi!")
                                        break
                                    elif ulang == "n":  # Jika tidak ingin memberikan feedback
                                        print("Terima kasih telah berbelanja di MyVending. Sampai jumpa lagi!")
                                        break
                                    else:
                                        raise ValueError("Input tidak valid. Masukkan 'y' atau 'n'.")  # Pesan error untuk input tidak valid
                            break
                        else: 
                            break

                elif pilihan_menubelanja == 3:  # Cek isi keranjang
                    clear_screen()  # Membersihkan layar
                    print("||=================================================||")
                    print("||                   MY VENDING                    ||".center(49))
                    print("||                  Cek Keranjang                  ||".center(49))
                    print("||=================================================||")
                    if pesanan.cek_keranjang():  # Jika keranjang tidak kosong
                        pesanan.tampilkan_keranjang()  # Tampilkan isi keranjang

                elif pilihan_menubelanja == 4:  # Mengurangi produk dari keranjang
                    while True:
                        clear_screen()  # Membersihkan layar untuk memberikan tampilan yang lebih rapi
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||          Kurangi Produk dari Keranjang          ||".center(49))
                        print("||=================================================||")
                        
                        if not pesanan.cek_keranjang():  # Mengecek apakah keranjang kosong
                            break  # Jika keranjang kosong, keluar dari menu penghapusan
                        
                        try:
                            pesanan.tampilkan_keranjang()  # Menampilkan isi keranjang belanja kepada pengguna
                            kode_produk = int(input("Kode produk\t: "))  # Meminta input kode produk yang akan dikurangi
                            kuantitas = int(input("Masukkan kuantitas pengurangan : ").strip())  # Meminta input jumlah pengurangan produk
                            pesanan.kurangi_dari_keranjang(kode_produk, kuantitas)  # Memproses pengurangan produk dari keranjang
                        except ValueError:
                            print("Input tidak valid. Masukkan angka untuk kode produk dengan benar.")  # Pesan error jika input bukan angka
                            continue  # Kembali ke awal loop untuk input ulang
                        
                        ulang = input("Apakah Anda ingin mengurangi produk lainnya dari keranjang (y/n)? ").lower()  # Menanyakan apakah ingin mengurangi produk lain
                        while ulang not in ['y', 'n']:  # Validasi input harus berupa 'y' atau 'n'
                            print("Pilihan tidak valid. Harap jawab dengan 'y' atau 'n'.")  # Pesan error jika input tidak valid
                            ulang = input("Apakah Anda ingin mengurangi produk lainnya dari keranjang (y/n)? ").lower()  # Meminta input ulang
                        
                        if ulang == 'n':  # Jika pengguna memilih 'n', keluar dari loop
                            break

                elif pilihan_menubelanja == 5:  # Kembali ke menu utama
                    break  # Keluar dari menu belanja produk untuk kembali ke menu utama
                
                else:
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")  # Pesan error jika input tidak valid
                
                input("\nTekan Enter untuk melanjutkan...")  # Menunggu input dari pengguna untuk melanjutkan ke iterasi berikutnya
   
        elif pilihan_menu == 2:  # Jika memilih menu akun
            while True:
                clear_screen()  # Membersihkan layar untuk memberikan tampilan yang lebih rapi
                print("||=================================================||")
                print("||                    MY VENDING                   ||".center(49))
                print("||                    Menu Akun                    ||".center(49))
                print("||=================================================||")
                
                # Menampilkan opsi dalam menu akun
                print("\n1. Login")  # Login ke akun yang sudah ada
                print("2. Buat Akun Baru")  # Membuat akun baru
                print("3. Cek Akun")  # Melihat informasi akun yang sedang login
                print("4. Tambah Saldo MyPay")  # Menambahkan saldo ke akun MyPay
                print("5. Tarik Saldo MyPay")  # Menarik saldo dari akun MyPay
                print("6. Logout")  # Logout dari akun saat ini
                print("7. Kembali ke Menu Utama")  # Kembali ke menu utama

                pilihan_akun = int(input("Pilihan: "))  # Input pilihan untuk menu akun

                if pilihan_akun == 1:  # Jika memilih login
                    akun.login()  # Memanggil fungsi login dari kelas Akun untuk proses login pengguna

                elif pilihan_akun == 2:  # Jika memilih buat akun baru
                    akun.buat_akun_baru()  # Memanggil fungsi untuk membuat akun baru

                elif pilihan_akun == 3:  # Jika memilih cek akun
                    akun.cek_akun()  # Menampilkan informasi akun yang sedang login

                elif pilihan_akun == 4:  # Jika memilih tambah saldo
                    akun.tambah_saldo_mypay()  # Memanggil fungsi untuk menambah saldo MyPay

                elif pilihan_akun == 5:  # Jika memilih tarik saldo
                    akun.tarik_saldo_mypay()  # Memanggil fungsi untuk menarik saldo dari MyPay

                elif pilihan_akun == 6:  # Jika memilih logout
                    akun.logout()  # Memanggil fungsi logout untuk keluar dari akun saat ini

                elif pilihan_akun == 7:  # Jika memilih kembali ke menu utama
                    break  # Keluar dari loop menu akun untuk kembali ke menu utama

                else:  # Jika pilihan tidak valid
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-7!")  # Menampilkan pesan error untuk input yang salah
                
                input("Tekan Enter untuk melanjutkan...")  # Menunggu input untuk melanjutkan ke iterasi berikutnya
        elif pilihan_menu == 3:  # Jika memilih menu admin
            input_password = getpass.getpass("\nPassword (hide)\t: ")  # Input password admin (tersembunyi)

            if input_password == admin_password:  # Jika password yang dimasukkan benar
                while True:  # Menu admin
                    clear_screen()  # Membersihkan layar
                    print("||=================================================||")
                    print("||                    MY VENDING                   ||".center(49))
                    print("||                    Menu Admin                   ||".center(49))
                    print("||=================================================||")
                    
                    # Menampilkan opsi dalam menu admin
                    print("\n1. Tampilkan Riwayat Aktivitas")  # Menampilkan log aktivitas
                    print("2. Status MyVending")  # Menampilkan status vending machine (suhu & kelembapan)
                    print("3. Kelola Produk di MyVending")  # Kelola stok produk
                    print("4. Cek Saldo Kembalian Tunai")  # Menampilkan saldo kembalian tunai
                    print("5. Kembali ke Menu Utama")  # Kembali ke menu utama

                    pilihan_menuadmin = int(input("Pilihan: "))  # Input pilihan menu admin
                    
                    if pilihan_menuadmin == 1:  # Jika memilih riwayat aktivitas
                        clear_screen()  # Membersihkan layar
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||                Riwayat Aktivitas                ||".center(49))
                        print("||=================================================||")
                        log.show_history()  # Memanggil fungsi untuk menampilkan log aktivitas
                        input("\nTekan Enter untuk kembali ke Menu Admin...")  # Tunggu input untuk kembali

                    elif pilihan_menuadmin == 2:  # Jika memilih status vending
                        while True:
                            clear_screen()  # Membersihkan layar
                            print("||=================================================||")
                            print("||                    MY VENDING                   ||".center(49))
                            print("||                 Status MyVending                ||".center(49))
                            print("||=================================================||")
                            
                            vending_status.display_status()  # Menampilkan status vending machine
                            print("\n1. Atur Suhu")  # Mengatur suhu vending machine
                            print("2. Atur Kelembapan")  # Mengatur kelembapan vending machine
                            print("3. Kembali ke Menu Admin")  # Kembali ke menu admin

                            pilihan_status = int(input("Pilihan: "))  # Input pilihan untuk status vending
                            
                            if pilihan_status == 1:  # Jika memilih atur suhu
                                perubahan_suhu = int(input("\nPerubahan suhu (positif untuk tambah, negatif untuk kurangi): "))
                                vending_status.set_suhu(perubahan_suhu)  # Memanggil fungsi untuk mengatur suhu
                                input("\nTekan Enter untuk kembali ke status...")  # Tunggu input untuk kembali

                            elif pilihan_status == 2:  # Jika memilih atur kelembapan
                                perubahan_kelembapan = int(input("\nPerubahan kelembapan (positif untuk tambah, negatif untuk kurangi): "))
                                vending_status.set_kelembapan(perubahan_kelembapan)  # Memanggil fungsi untuk mengatur kelembapan
                                input("\nTekan Enter untuk kembali ke status...")  # Tunggu input untuk kembali

                            elif pilihan_status == 3:  # Jika memilih kembali ke menu admin
                                break  # Keluar dari loop menu status vending

                            else:  # Jika pilihan tidak valid
                                print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-3\n")

                    elif pilihan_menuadmin == 3:  # Jika memilih kelola produk
                        while True:  # Loop untuk menu kelola produk
                            clear_screen()  # Membersihkan layar
                            print("||=================================================||")
                            print("||                    MY VENDING                   ||".center(49))
                            print("||                  Kelola Produk                  ||".center(49))
                            print("||=================================================||")
                            
                            print("\n")
                            stok.display_products_admin()  # Menampilkan daftar produk
                            print("\n1. Tambah Stok Produk")  # Menambahkan stok produk
                            print("2. Kurangi Stok Produk")  # Mengurangi stok produk
                            print("3. Atur Expired Stok Produk")  # Mengatur tanggal expired stok produk
                            print("4. Kembali ke Menu Admin")  # Kembali ke menu admin

                            try:
                                pilihan_kelola_produk = int(input("Pilihan: "))  # Input pilihan kelola produk

                                if pilihan_kelola_produk == 1:  # Jika memilih tambah stok
                                    try:
                                        kode_produk = int(input("\nKode produk\t: "))  # Input kode produk
                                        if kode_produk in stok.products:  # Validasi kode produk
                                            jumlah_tambah = int(input("Kuantitas penambahan\t: "))  # Input jumlah stok
                                            stok.tambah_stok(kode_produk, jumlah_tambah, log)  # Menambahkan stok
                                        else:
                                            print("Kode produk tidak ditemukan.")  # Kode tidak valid
                                    except ValueError:
                                        print("Input tidak valid. Masukkan angka untuk kode produk dan jumlah stok.")  # Error handling
                                    input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

                                elif pilihan_kelola_produk == 2:  # Jika memilih kurangi stok
                                    try:
                                        kode_produk = int(input("\nKode produk\t: "))  # Input kode produk
                                        if kode_produk in stok.products:  # Validasi kode produk
                                            jumlah_kurang = int(input("Kuantitas pengurangan\t: "))  # Input jumlah stok
                                            stok.kurangi_stok(kode_produk, jumlah_kurang, log)  # Mengurangi stok
                                        else:
                                            print("Kode produk tidak ditemukan.")  # Kode tidak valid
                                    except ValueError:
                                        print("Input tidak valid. Masukkan angka untuk kode produk dan jumlah stok.")  # Error handling
                                    input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

                                elif pilihan_kelola_produk == 3:  # Jika memilih mengatur ulang expired stok
                                    try:
                                        kode_produk = int(input("\nKode produk\t: "))  # Input kode produk
                                        if kode_produk in stok.products:  # Validasi kode produk
                                            expired_baru = input("Expired baru (contoh: MM/YY, seperti 07/25)\t: ")  # Input expired baru
                                            stok.atur_expired(kode_produk, expired_baru, log)  # Memperbarui expired produk
                                        else:
                                            print("Kode produk tidak ditemukan.")  # Kode tidak valid
                                    except ValueError:
                                        print("Input tidak valid. Masukkan angka untuk kode produk.")  # Error handling
                                    input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

                                elif pilihan_kelola_produk == 4:  # Jika memilih kembali ke menu admin
                                    break  # Keluar dari loop kelola produk

                                else:  # Jika pilihan tidak valid
                                    print("Pilihan tidak valid. Masukkan angka antara 1-4.")  # Pesan kesalahan
                            except ValueError:
                                print("Input tidak valid. Masukkan angka untuk pilihan.")  # Error handling untuk input utama
                            input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

                    elif pilihan_menuadmin == 4:  # Jika memilih cek saldo kembalian
                        clear_screen()  # Membersihkan layar
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||               Cek Saldo Kembalian Tunai         ||".center(49))
                        print("||=================================================||")
                        kembalian.cek_saldo_kembalian()  # Menampilkan saldo kembalian
                        input("\nTekan Enter untuk kembali ke menu Admin...")  # Tunggu input untuk kembali

                    elif pilihan_menuadmin == 5:  # Jika memilih kembali ke menu utama
                        break  # Keluar dari loop menu admin

                    else:  # Jika pilihan tidak valid
                        print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-5!\n")

            else:
                # Jika password salah, cukup satu kali enter untuk kembali ke Menu Utama
                print("Password salah. Kembali ke Menu Utama.")
      
        elif pilihan_menu == 4:  # Jika memilih menampilkan feedback
            clear_screen()  # Membersihkan layar
            print("||=================================================||")
            print("||                    MY VENDING                   ||".center(49))
            print("||                  Lihat Feedback                 ||".center(49))
            print("||=================================================||")
            feedback_handler.display_feedback()  # Memanggil fungsi untuk menampilkan daftar feedback yang telah diberikan pengguna
                   
        elif pilihan_menu == 5:  # Jika memilih keluar dari aplikasi
            print("Terima kasih telah mengunjungi MyVending!")  # Menampilkan pesan perpisahan kepada pengguna
            exit()  # Menghentikan eksekusi program dan keluar

        else:  # Jika pilihan menu utama tidak valid
            print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-4!")  # Menampilkan pesan error jika input tidak sesuai dengan menu yang tersedia
            
        input("\nTekan Enter untuk melanjutkan...")  # Menunggu pengguna menekan Enter sebelum melanjutkan program

main()  # Memanggil fungsi utama untuk menjalankan keseluruhan alur program vending machine