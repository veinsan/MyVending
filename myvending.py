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
# display : Objek dari kelas Display untuk menampilkan antarmuka ke pengguna
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

# ALGORITMA
import os
# Modul `os` digunakan untuk berinteraksi dengan sistem operasi, seperti membersihkan layar terminal.

import time
# Modul `time` digunakan untuk menangani operasi terkait waktu, seperti mencatat waktu transaksi.

import csv
# Modul `csv` digunakan untuk membaca dan menulis file dalam format CSV, seperti data akun atau saldo.

import getpass
# Modul `getpass` digunakan untuk mengambil input password secara aman (input tidak terlihat saat diketik).

def clear_screen():
    # Fungsi untuk membersihkan layar terminal agar tampilan menu lebih rapi setiap kali di-refresh.
    # `os.system` akan memanggil perintah bawaan sistem operasi:
    # - 'cls' untuk Windows
    # - 'clear' untuk sistem berbasis UNIX (Linux, macOS)
    os.system('cls' if os.name == 'nt' else 'clear')

class Display:
    # Kelas Display bertanggung jawab untuk menampilkan berbagai tampilan, header, dan menu pada vending machine.

    def header_utama(self):
        # Menampilkan header utama yang menyambut pengguna saat aplikasi dimulai.
        print("||=================================================||")
        print("||           SELAMAT DATANG DI MYVENDING           ||".center(49))
        print("||=================================================||")
        print("||                Selamat berbelanja!              ||".center(49))
        print("||=================================================||")

    def header_myvending():
        # Menampilkan header utama dengan label "MY VENDING".
        print("||=================================================||")
        print("||                    MY VENDING                   ||".center(49))
        print("||=================================================||")
    
    def menu_admin(self):
        # Menampilkan menu pilihan yang tersedia untuk administrator.
        print("\n\n|----------------------------------------------------|")
        print("| MENU ADMIN                                        |".center(49))
        print("| 1. Tampilkan Riwayat Aktivitas                    |".center(49))
        print("| 2. Status MyVending                               |".center(49))
        print("| 3. Kelola Produk di MyVending                     |".center(49))
        print("| 4. Cek Saldo Kembalian Tunai                      |".center(49))
        print("| 5. Kembali ke Menu Utama                          |".center(49))
        print("|----------------------------------------------------|")

class StokBarang:
    # Kelas untuk mengelola stok barang dalam vending machine, termasuk menampilkan daftar produk,
    # mengecek ketersediaan stok, dan menambah stok produk.

    def __init__(self):
        # Konstruktor untuk inisialisasi data produk.
        # Data produk disimpan dalam dictionary dengan format:
        # {kode_produk: {"name": nama_produk, "price": harga, "stock": jumlah_stok}}
        self.products = {
            1: {"name": "Aqua", "price": 4000, "stock": 10},
            2: {"name": "Pocari Sweat", "price": 8000, "stock": 10},
            3: {"name": "Teh Pucuk", "price": 5000, "stock": 10},
            4: {"name": "Lime", "price": 5000, "stock": 10},
            5: {"name": "Coca cola", "price": 5000, "stock": 10},
            6: {"name": "Cap Kaki Tiga", "price": 9000, "stock": 10},
            7: {"name": "Floridina", "price": 5000, "stock": 10}
        }

    def display_products(self):
        # Fungsi untuk menampilkan daftar produk yang tersedia dalam vending machine.
        print("                    DAFTAR PRODUK                    ")
        print("|---------------------------------------------------|")
        print("| Kode | Produk           | Harga      | Stok       |")
        print("|---------------------------------------------------|")
        for code, product in self.products.items():
            # Menampilkan informasi setiap produk: kode, nama, harga, dan jumlah stok.
            print(f"| {code:<4} | {product['name']:<16} | Rp{product['price']:<8} | {product['stock']:<8}   |")
        print("|---------------------------------------------------|")
    
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
                log.add_log("Tambah Stok", f"{self.products[product_code]['name']} - Tambah {tambahan} (Total: {self.products[product_code]['stock']})")
                print(f"\nStok {self.products[product_code]['name']} berhasil ditambahkan sebanyak {tambahan}. \nTotal stok {self.products[product_code]['name']}: {self.products[product_code]['stock']}.")
                return True
        else:
            # Jika kode produk tidak valid, tampilkan pesan kesalahan.
            print("Kode produk tidak valid.")
            return False

class LogAktivitas:
    # Kelas untuk mencatat dan menampilkan riwayat aktivitas yang dilakukan dalam sistem vending machine.

    def __init__(self):
        # Konstruktor untuk inisialisasi atribut history, yang menyimpan riwayat aktivitas.
        self.history = [] #Riwayat aktivitas disimpan dalam bentuk list.

    def add_log(self, action, detail):
        # Fungsi untuk menambahkan entri log ke dalam riwayat aktivitas.
        # Parameter:
        # - action: Deskripsi singkat tentang jenis aktivitas (misalnya, "Pembelian" atau "Tambah Stok").
        # - detail: Informasi tambahan tentang aktivitas (misalnya, produk yang dibeli atau jumlah stok yang ditambahkan).
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Mendapatkan waktu saat aktivitas dilakukan.
        self.history.append({"timestamp": timestamp, "action": action, "detail": detail}) # Menyimpan entri log sebagai dictionary.

    def show_history(self):
        # Fungsi untuk menampilkan semua riwayat aktivitas yang tercatat.
        print("\n|-------------------------------------------------|")
        if not self.history:
            # Jika tidak ada aktivitas yang tercatat, tampilkan pesan bahwa riwayat masih kosong.
            print("|           Belum ada riwayat aktivitas           |".center(49))
        else:
            # Jika ada aktivitas, tampilkan setiap entri dalam format yang rapi.
            for entry in self.history:
                print(f"|| [{entry['timestamp']}] {entry['action']} - {entry['detail']}                  ||")
        print("|-------------------------------------------------|")

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
            # Perbarui saldo pengguna di file CSV.
            self.akun.update_saldo_csv()
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

    def bayar_dengan_tunai(self, total_harga):
        # Metode untuk memproses pembayaran menggunakan uang tunai.
        # Parameter:
        # - total_harga: Jumlah total harga yang harus dibayar.
        print("\nMasukkan nominal uang yang digunakan untuk membayar (gunakan pecahan Rp1000, Rp2000, Rp5000, Rp10000, Rp20000, Rp50000, Rp100000).")
        sisa_pembayaran = total_harga
        while sisa_pembayaran > 0:
            # Loop untuk meminta input uang dari pengguna hingga total pembayaran terpenuhi.
            nominal = int(input(f"Sisa pembayaran\t\t: Rp{sisa_pembayaran}. \nNominal\t\t\t: Rp"))
            jumlah = int(input(f"Banyak lembar Rp{nominal}\t: "))
            total_input = nominal * jumlah

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
            link_qris = "https://youtu.be/dQw4w9WgXcQ?si=SgIGQBGfMir4h7VY"  # Contoh link QRIS.
            print("\nPembayaran melalui QRIS sedang diproses...")
            self.generate_qris_ascii(link_qris)
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

    def __init__(self, stok, log, pembayaran):
        # Konstruktor untuk menginisialisasi objek PemrosesanPesanan.
        # Parameter:
        # - stok: Objek dari kelas StokBarang untuk mengatur ketersediaan barang.
        # - log: Objek dari kelas LogAktivitas untuk mencatat aktivitas pengguna.
        # - pembayaran: Objek dari kelas SistemPembayaran untuk memproses pembayaran.
        self.stok = stok  # Referensi ke stok barang.
        self.log = log  # Referensi ke log aktivitas.
        self.pembayaran = pembayaran  # Referensi ke sistem pembayaran.
        self.cart = []  # Keranjang belanja pengguna, berupa daftar produk.
        self.total_harga = 0  # Total harga awal, diatur ke nol.

    def tambah_ke_keranjang(self, product_code, quantity):
        # Metode untuk menambahkan produk ke keranjang belanja.
        # Parameter:
        # - product_code: Kode produk yang ingin ditambahkan.
        # - quantity: Jumlah produk yang ingin ditambahkan.
        if self.stok.check_stock_and_update(product_code, quantity):
            # Jika stok produk mencukupi, tambahkan produk ke keranjang.
            produk = self.stok.products[product_code]
            self.cart.append({
                "code": product_code, 
                "name": produk["name"], 
                "quantity": quantity, 
                "price": produk["price"] * quantity
            })
            self.total_harga += produk["price"] * quantity  # Tambahkan harga produk ke total harga.
            print(f"\n{quantity} {produk['name']} telah ditambahkan ke keranjang. \nTotal sementara: Rp{self.total_harga}\n")
        else:
            # Jika stok tidak mencukupi, tampilkan pesan kesalahan.
            print("\nStok tidak mencukupi! Produk gagal ditambahkan.\n")

    def hapus_dari_keranjang(self, product_code):
        # Metode untuk menghapus produk dari keranjang belanja.
        # Parameter:
        # - product_code: Kode produk yang ingin dihapus dari keranjang.
        for item in self.cart:
            if item["code"] == product_code:
                # Jika produk ditemukan dalam keranjang, hapus produk tersebut.
                self.cart.remove(item)
                self.total_harga -= item["price"]  # Kurangi harga produk dari total harga.
                self.stok.products[product_code]['stock'] += item["quantity"]  # Tambahkan kembali stok produk.
                print(f"\n{item['name']} x{item['quantity']} telah dihapus dari keranjang. Stok {item['name']} dikembalikan.")
                print(f"Total sementara: Rp{self.total_harga}\n")
                return
        # Jika produk tidak ditemukan dalam keranjang, tampilkan pesan kesalahan.
        print("Item tidak ditemukan di keranjang.\n")

    def cek_keranjang(self):
        # Metode untuk memeriksa apakah keranjang belanja kosong.
        # Mengembalikan True jika keranjang tidak kosong, False jika kosong.
        if not self.cart:
            print("\n" + "Keranjang Anda kosong.\n".center(55))
            return False
        else:
            return True

    def tampilkan_keranjang(self):
        # Metode untuk menampilkan isi keranjang belanja.
        print("\n|---------------------------------------------------|")
        print("|                   KERANJANG BELANJA               |".center(49))
        print("|---------------------------------------------------|")
        print("| Kode | Nama Produk           | Jumlah | Harga     |")
        print("|---------------------------------------------------|")
        for item in self.cart:
            # Tampilkan setiap item dalam keranjang.
            print(f"| {item['code']:<4} | {item['name']:<21} | {'x' + str(item['quantity']):^6} | Rp{item['price']:<7} |")
        print("|---------------------------------------------------|")
        print(f"| Total Harga: {' ':<25} {' Rp' + str(self.total_harga):<10} |")
        print("|---------------------------------------------------|\n")

    def proses_checkout(self):
        # Metode untuk memproses checkout dan pembayaran.
        if not self.cart:
            # Jika keranjang kosong, tampilkan pesan dan batalkan checkout.
            print("Keranjang Anda kosong. Tambahkan produk terlebih dahulu.\n")
            return

        # Menampilkan isi keranjang sebelum memproses pembayaran.
        self.tampilkan_keranjang()

        # Proses pembayaran melalui sistem pembayaran.
        if self.pembayaran.proses_checkout(self.total_harga):
            # Jika pembayaran berhasil, catat pembelian ke log dan cetak struk.
            for item in self.cart:
                self.log.add_log("Pembelian", f"{item['name']} x{item['quantity']} - Rp{item['price']}")
            self.cetak_struk()  # Cetak struk pembayaran.
            print("\nTransaksi berhasil!")
            self.cart = []  # Kosongkan keranjang setelah checkout.
            self.total_harga = 0  # Reset total harga setelah transaksi selesai.
        else:
            # Jika pembayaran gagal, tampilkan pesan kesalahan.
            print("Pembayaran gagal. Silakan coba lagi.")
        
    def cetak_struk(self):
        # Metode untuk mencetak struk pembayaran setelah checkout berhasil.
        print("\n|================= STRUK PEMBAYARAN ================|")
        print(f"| Waktu Transaksi:              {time.strftime('%Y-%m-%d %H:%M:%S')} |")
        print("|---------------------------------------------------|")
        print("| Produk               | Jumlah | Harga Total       |")
        print("|---------------------------------------------------|")
        for item in self.cart:
            # Tampilkan informasi setiap produk dalam struk.
            print(f"| {item['name']:<20} | {item['quantity']:<6} | Rp{item['price']:<15} |")
        print("|---------------------------------------------------|")
        print(f"| Total Harga: {' ':<18} Rp{self.total_harga:<15} |")
        print("|---------------------------------------------------|")
        print("|    Terima kasih telah berbelanja di MYVENDING!    |")
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

def main():
    # Inisialisasi objek untuk berbagai kelas yang digunakan dalam program
    stok = StokBarang()  # Digunakan untuk mengelola stok produk
    log = LogAktivitas()  # Untuk mencatat dan menampilkan log aktivitas
    kembalian = SistemKembalian("kembalian.csv")  # Membaca dan mengelola saldo kembalian dari file CSV
    akun = Akun()  # Mengelola akun pengguna, seperti login dan saldo
    pembayaran = SistemPembayaran(kembalian, akun)  # Untuk mengatur berbagai metode pembayaran
    display = Display()  # Menampilkan header dan antarmuka program
    pesanan = PemrosesanPesanan(stok, log, pembayaran)  # Memproses transaksi, keranjang, dan checkout
    vending_status = MyVendingStatus()  # Untuk memantau status vending machine (suhu dan kelembapan)

    admin_password = "Admin#123"  # Password untuk akses menu admin

    while True:  # Loop utama program
        clear_screen()  # Membersihkan layar sebelum menampilkan menu utama

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
        print("4. Keluar")  # Keluar dari program
        print("----------------------------------------------------")
        
        pilihan_menu = int(input("Pilihan: "))  # Input untuk memilih menu utama

        if pilihan_menu == 1:  # Jika memilih belanja produk
            while True:  # Loop untuk menu belanja
                clear_screen()  # Membersihkan layar sebelum menampilkan daftar produk
                print("||=================================================||")
                print("||                    MY VENDING                   ||".center(49))
                print("||               Menu Belanja Produk               ||".center(49))
                print("||=================================================||\n")
                
                stok.display_products()  # Menampilkan daftar produk
                print("\n1. Tambahkan Produk ke Keranjang")  # Tambahkan produk ke keranjang
                print("2. Pembayaran")  # Lanjutkan ke proses pembayaran
                print("3. Cek Keranjang")  # Lihat isi keranjang belanja
                print("4. Hapus Produk dari Keranjang")  # Menghapus item dari keranjang
                print("5. Kembali ke Menu Utama")  # Kembali ke menu utama

                pilihan_menubelanja = int(input("Pilihan: "))  # Input untuk memilih opsi belanja
                
                if pilihan_menubelanja == 1:  # Menambah produk ke keranjang
                    ulang = "y"  # Menanyakan apakah pengguna ingin mengulangi penambahan
                    while ulang.lower() == "y":  
                        clear_screen()  # Membersihkan layar
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||         Penambahan Produk ke Keranjang          ||".center(49))
                        print("||=================================================||\n")
                        stok.display_products()  # Menampilkan daftar produk
                        try:
                            kode_produk = int(input("\nKode produk\t\t: "))  # Input kode produk
                            if kode_produk in stok.products:  # Cek apakah produk ada dalam stok
                                kuantitas_produk = int(input("Kuantitas produk\t: "))  # Input kuantitas
                                if kuantitas_produk <= 0:  # Validasi kuantitas harus > 0
                                    print("Kuantitas produk tidak valid!")
                                    continue  
                                pesanan.tambah_ke_keranjang(kode_produk, kuantitas_produk)  # Tambahkan ke keranjang
                                ulang = input("Apakah Anda ingin menambahkan produk lainnya ke keranjang (y/n)? ").lower()
                                while ulang not in ['y', 'n']:  # Validasi input y/n
                                    print("Pilihan tidak valid. Harap jawab dengan 'y' atau 'n'.")
                                    ulang = input("Apakah Anda ingin menambahkan produk lainnya ke keranjang (y/n)? ").lower()
                            else:
                                print("Kode produk tidak valid. Harap masukkan kode yang tersedia pada daftar.\n")
                                break
                        except ValueError:
                            print("Input tidak valid. Masukkan angka.")  # Handling jika input bukan angka

                elif pilihan_menubelanja == 2:  # Proses pembayaran
                    clear_screen()  # Membersihkan layar
                    print("||=================================================||")
                    print("||                    MY VENDING                   ||".center(49))
                    print("||                    Pembayaran                   ||".center(49))
                    print("||=================================================||")
                    while True:
                        if pesanan.cek_keranjang():  # Cek apakah keranjang tidak kosong
                            pesanan.tampilkan_keranjang()  # Menampilkan isi keranjang
                            pesanan.proses_checkout()  # Lanjutkan ke checkout
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

                elif pilihan_menubelanja == 4:  # Hapus produk dari keranjang
                    while True:
                        clear_screen()  # Membersihkan layar
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||           Hapus Produk dari Keranjang           ||".center(49))
                        print("||=================================================||")
                        
                        if not pesanan.cek_keranjang():  # Jika keranjang kosong
                            break  # Keluar dari menu penghapusan
                        
                        try:
                            pesanan.tampilkan_keranjang()  # Tampilkan isi keranjang
                            kode_produk = int(input("Kode produk\t: "))  # Input kode produk
                            pesanan.hapus_dari_keranjang(kode_produk)  # Hapus produk dari keranjang
                        except ValueError:
                            print("Input tidak valid. Masukkan angka untuk kode produk dengan benar.")  # Handling error
                            continue
                        
                        ulang = input("Apakah Anda ingin menghapus produk lainnya dari keranjang (y/n)? ").lower()  # Tanyakan ulang
                        while ulang not in ['y', 'n']:  # Validasi input
                            print("Pilihan tidak valid. Harap jawab dengan 'y' atau 'n'.")
                            ulang = input("Apakah Anda ingin menghapus produk lainnya dari keranjang (y/n)? ").lower()
                        
                        if ulang == 'n':  # Jika tidak ingin menghapus lagi, keluar dari loop
                            break

                elif pilihan_menubelanja == 5:  # Kembali ke menu utama
                    break
                
                else:
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                
                input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

        elif pilihan_menu == 2:  # Jika memilih menu akun
            while True:
                clear_screen()  # Membersihkan layar
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
                    akun.login()  # Memanggil fungsi login dari kelas Akun

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
                    break  # Keluar dari loop menu akun

                else:  # Jika pilihan tidak valid
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-7!")
                
                input("Tekan Enter untuk melanjutkan...")  # Menunggu input untuk melanjutkan

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
                                pilihan_status = int(input("Pilihan: "))

                    elif pilihan_menuadmin == 3:  # Jika memilih kelola produk
                        while True:  # Loop untuk menu kelola produk
                            clear_screen()  # Membersihkan layar
                            print("||=================================================||")
                            print("||                    MY VENDING                   ||".center(49))
                            print("||                  Kelola Produk                  ||".center(49))
                            print("||=================================================||")
                            
                            stok.display_products()  # Menampilkan daftar produk
                            print("\n1. Tambah Stok Produk")  # Menambahkan stok produk
                            print("2. Kembali ke Menu Admin")  # Kembali ke menu admin

                            try:
                                pilihan_kelola_produk = int(input("Pilihan: "))  # Input pilihan kelola produk

                                if pilihan_kelola_produk == 1:  # Jika memilih tambah stok
                                    try:
                                        kode_produk = int(input("\nKode produk\t: "))  # Input kode produk
                                        if kode_produk in stok.products:  # Validasi kode produk
                                            jumlah_tambah = int(input("Stok penambahan\t: "))  # Input jumlah stok
                                            
                                            stok.tambah_stok(kode_produk, jumlah_tambah, log)  # Menambahkan stok
                                        else:
                                            print("Kode produk tidak ditemukan.")  # Kode tidak valid
                                    except ValueError:
                                        print("Input tidak valid. Masukkan angka untuk kode produk dan jumlah stok.")  # Error handling
                                    input("\nTekan Enter untuk melanjutkan...")  # Tunggu input untuk melanjutkan

                                elif pilihan_kelola_produk == 2:  # Jika memilih kembali ke menu admin
                                    break  # Keluar dari loop kelola produk

                                else:  # Jika pilihan tidak valid
                                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan 1 atau 2!")
                                    input("\nTekan Enter untuk melanjutkan...")

                            except ValueError:
                                print("Input tidak valid. Masukkan angka untuk pilihan.")  # Error handling
                                input("\nTekan Enter untuk melanjutkan...")

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

        elif pilihan_menu == 4:  # Jika memilih keluar dari aplikasi
            print("Terima kasih telah mengunjungi MyVending!")  # Menampilkan pesan perpisahan
            exit()  # Menghentikan program

        else:  # Jika pilihan menu utama tidak valid
            print("Pilihan tidak valid. Silakan masukkan kembali pilihan antara 1-4!")  # Menampilkan pesan error
            
        input("\nTekan Enter untuk melanjutkan...")  # Menunggu pengguna menekan Enter sebelum melanjutkan

main()  # Memanggil fungsi utama program untuk menjalankan alur vending machine.