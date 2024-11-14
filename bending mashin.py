import os
import time
import csv
import getpass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Display:
    def header_utama(self):
        print("||=================================================||")
        print("||           SELAMAT DATANG DI MYVENDING           ||".center(49))
        print("||=================================================||")
        print("||                Selamat berbelanja!              ||".center(49))
        print("||=================================================||")

    def header_myvending():
        print("||=================================================||")
        print("||                    MY VENDING                   ||".center(49))
        print("||=================================================||")
    
    def menu_utama(self):
        print("\n\n|----------------------------------------------------|")
        print("| MENU UTAMA                                         |".center(49))
        print("| 1. Belanja Produk                                  |".center(49))
        print("| 2. Login Akun                                      |".center(49))
        print("| 3. Menu Admin                                      |".center(49))
        print("| 4. Keluar                                          |".center(49))
        print("|----------------------------------------------------|")

class StokBarang:
    def __init__(self):
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
        print("\n\n  DAFTAR PRODUK                  ")
        print("|--------------------------------------------------|")
        print("| Kode | Produk           | Harga      | Stok      |")
        print("|--------------------------------------------------|")
        for code, product in self.products.items():
            print(f"| {code:<4} | {product['name']:<16} | Rp{product['price']:<8} | {product['stock']:<7}   |")
        print("|--------------------------------------------------|")
    
    def check_stock_and_update(self, product_code, quantity):
        if product_code in self.products:
            product = self.products[product_code]
            if product["stock"] >= quantity:
                # Kurangi stok produk
                product["stock"] -= quantity
                return True
            else:
                print(f"Stok tidak cukup untuk {product['name']}!")
                return False
        return False

class LogAktivitas:
    def __init__(self):
        self.history = []

    def add_log(self, action, detail):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.history.append({"timestamp": timestamp, "action": action, "detail": detail})

    def show_history(self):
        print("\n|-------------------------------------------------|")
        if not self.history:
            print("|           Belum ada riwayat aktivitas           |".center(49))
        else:
            for entry in self.history:
                print(f"|| [{entry['timestamp']}] {entry['action']} - {entry['detail']}                  ||")
        print("|-------------------------------------------------|")

class SistemPembayaran:
    def __init__(self):
        self.nomor_tujuan = "089656054453"
        self.wallet = 0

    def top_up_wallet(self, amount):
        self.wallet += amount
        print(f"Dompet berhasil di-top up sebesar Rp{amount}. Total dompet: Rp{self.wallet}.")
        return amount

    def pilih_metode_pembayaran(self, total):
        print("\n||=================================================||")
        print("||              PILIH METODE PEMBAYARAN            ||".center(49))
        print("||=================================================||")
        print("|| 1. GoPay                                        ||".center(49))
        print("|| 2. DANA                                         ||".center(49))
        print("|| 3. OVO                                          ||".center(49))
        print("|| 4. Tunai                                        ||".center(49))
        print("||=================================================||")
        
        metode = input("Masukkan pilihan metode pembayaran (1-4): ")
        if metode == "1":
            metode_pembayaran = "GoPay"
        elif metode == "2":
            metode_pembayaran = "DANA"
        elif metode == "3":
            metode_pembayaran = "OVO"
        elif metode == "4":
            metode_pembayaran = "Tunai"
        else:
            print("Metode pembayaran tidak valid. Pembayaran dibatalkan.")
            return False
        
        if metode_pembayaran == "Tunai":
            print(f"\nSilakan bayar Rp{total}.")
            cash_received = int(input("Masukkan jumlah uang yang diberikan: "))
            if cash_received < total:
                print("Uang yang diberikan tidak cukup. Pembayaran dibatalkan.")
                return False
            else:
                change = cash_received - total
                if change > 0:
                    self.wallet += change
                    print(f"Kembalian Rp{change} telah ditambahkan ke dompet Anda.")
                print("Pembayaran Diverifikasi, Pesanan Akan Segera Dibuat.\n")
                return True
        else:
            print(f"\nSilakan transfer Rp{total} ke nomor {self.nomor_tujuan} menggunakan {metode_pembayaran}.")
            konfirmasi = input("Apakah Anda sudah melakukan pembayaran? (ya/tidak): ").lower()
            if konfirmasi == "ya":
                print("Pembayaran Diverifikasi, Pesanan Akan Segera Dibuat.\n")
                return True
            else:
                print("Pembayaran belum dikonfirmasi. Silakan lakukan pembayaran terlebih dahulu.\n")
                return False

class PemrosesanPesanan:
    def __init__(self, stok, log, pembayaran):
        self.stok = stok
        self.log = log
        self.pembayaran = pembayaran
        self.cart = []
        self.total_harga = 0

    def tambah_ke_keranjang(self, product_code, quantity):
        if self.stok.check_stock_and_update(product_code, quantity):
            produk = self.stok.products[product_code]
            self.cart.append({"code": product_code, "name": produk["name"], "quantity": quantity, "price": produk["price"] * quantity})
            self.total_harga += produk["price"] * quantity
            print(f"\n{quantity} {produk['name']} telah ditambahkan ke keranjang. \nTotal sementara: Rp{self.total_harga}\n")
        else:
            print("\nStok tidak mencukupi! Produk gagal ditambahkan.\n")

    def hapus_dari_keranjang(self, product_code):
        for item in self.cart:
            if item["code"] == product_code:
                self.cart.remove(item)
                self.total_harga -= item["price"]
                print(f"{item['name']} x{item['quantity']} telah dihapus dari keranjang. Total sementara: Rp{self.total_harga}\n")
                return
        print("Item tidak ditemukan di keranjang.\n")

    def cek_keranjang(self):
        if not self.cart:
            print("\n" + "Keranjang Anda kosong.\n".center(55))
            return False

        print("\n|---------------------------------------------------|")
        print("|                   KERANJANG BELANJA               |".center(49))
        print("|---------------------------------------------------|")
        for item in self.cart:
            print(f"| {item['name']:<25} | {'x' + str(item['quantity']):^6} | Rp{item['price']:<10} |")
        print("|---------------------------------------------------|")
        print(f"| Total Harga: {' ':<22} {' Rp' + str(self.total_harga):<13} |")
        print("|---------------------------------------------------|\n")


    def proses_checkout(self):
        if not self.cart:
            print("Keranjang Anda kosong. Tambahkan produk terlebih dahulu.\n")
            return
        
        self.cek_keranjang()

        if self.pembayaran.pilih_metode_pembayaran(self.total_harga):
            for item in self.cart:
                self.log.add_log("Pembelian", f"{item['name']} x{item['quantity']} - Rp{item['price']}")
            print("Transaksi selesai, terima kasih telah berbelanja di MYVENDING!\n")
            self.cart = []
            self.total_harga = 0

class Akun:
    def __init__(self):
        self.logged_in_user = None  # Menyimpan user yang sedang login

    def login(self):
        if self.logged_in_user:
            print("Anda sudah login. Silakan logout terlebih dahulu untuk login dengan akun lain.")
            return
        
        username = input("Masukkan username: ")
        password = getpass.getpass("Masukkan password: ")  # Sembunyikan password dengan getpass
        
        with open('accounts.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    self.logged_in_user = row  # Simpan data akun yang login
                    print("Login berhasil!")
                    print(f"Saldo saat ini: Rp{row['saldo']}")
                    return True
            print("Username atau password salah.")
            return False

    def buat_akun_baru(self):
        if self.logged_in_user:
            print("Anda sudah login. Silakan logout terlebih dahulu untuk membuat akun baru.")
            return
        
        username = input("Masukkan username baru: ")
        
        # Cek apakah username sudah ada
        with open('accounts.csv', mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['username'] == username:
                    print("Username sudah digunakan. Silakan pilih yang lain.")
                    return
        
        password = input("Masukkan password baru: ")
        saldo = 0  # Set saldo awal ke Rp0

        with open('accounts.csv', mode='a', newline='') as csvfile:
            fieldnames = ['username', 'password', 'saldo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Jika file kosong, tulis header
            csvfile.seek(0, os.SEEK_END)
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerow({'username': username, 'password': password, 'saldo': saldo})
        
        print("Akun berhasil dibuat dengan saldo Rp0. Tambahkan saldo melalui menu Tambah Saldo MyPay.")

    def tambah_saldo_mypay(self):
        if not self.logged_in_user:
            print("Anda harus login terlebih dahulu untuk menambah saldo.")
            return

        metode = input("Pilih metode tambah saldo (Gopay/Ovo/Dana/QRIS): ").strip().lower()
        amount = int(input("Masukkan jumlah saldo yang ingin ditambahkan: "))

        # Konfirmasi dengan PIN setelah memilih metode
        pin = getpass.getpass("Masukkan PIN untuk konfirmasi: ")
        if pin != self.logged_in_user['password']:
            print("PIN salah. Tidak dapat melanjutkan penambahan saldo.")
            return

        # Nomor virtual untuk pembayaran
        nomor_virtual = "089656054453"
        if metode in ['gopay', 'ovo', 'dana', 'qris']:
            print(f"Silakan transfer Rp{amount} ke nomor {nomor_virtual} melalui {metode.capitalize()}.")
            konfirmasi = input("Ketik 'YA' jika sudah melakukan pembayaran: ").strip().upper()
            if konfirmasi == 'YA':
                # Update saldo pengguna yang sedang login
                self.logged_in_user['saldo'] = int(self.logged_in_user['saldo']) + amount
                print(f"Saldo sebesar Rp{amount} berhasil ditambahkan.")

                # Perbarui saldo di file CSV
                with open('accounts.csv', mode='r') as csvfile:
                    rows = list(csv.DictReader(csvfile))
                
                for row in rows:
                    if row['username'] == self.logged_in_user['username']:
                        row['saldo'] = self.logged_in_user['saldo']
                        break
                
                with open('accounts.csv', mode='w', newline='') as csvfile:
                    fieldnames = ['username', 'password', 'saldo']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
            else:
                print("Pembayaran belum dikonfirmasi.")
        else:
            print("Metode tidak valid. Silakan pilih kembali.")

    def tarik_saldo_mypay(self):
        if not self.logged_in_user:
            print("Anda harus login terlebih dahulu untuk menarik saldo.")
            return

        amount = int(input("Masukkan jumlah saldo yang ingin ditarik: "))

        # Konfirmasi dengan PIN sebelum tarik saldo
        pin = getpass.getpass("Masukkan PIN untuk konfirmasi: ")
        if pin != self.logged_in_user['password']:
            print("PIN salah. Tidak dapat melanjutkan penarikan saldo.")
            return

        if int(self.logged_in_user['saldo']) >= amount:
            # Kurangi saldo pengguna yang sedang login
            self.logged_in_user['saldo'] = int(self.logged_in_user['saldo']) - amount
            print(f"Tarik saldo sebesar Rp{amount} berhasil. Saldo sekarang: Rp{self.logged_in_user['saldo']}")

            # Perbarui saldo di file CSV
            with open('accounts.csv', mode='r') as csvfile:
                rows = list(csv.DictReader(csvfile))
            
            for row in rows:
                if row['username'] == self.logged_in_user['username']:
                    row['saldo'] = self.logged_in_user['saldo']
                    break
            
            with open('accounts.csv', mode='w', newline='') as csvfile:
                fieldnames = ['username', 'password', 'saldo']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            print("Saldo tidak mencukupi.")

    def logout(self):
        if self.logged_in_user:
            konfirmasi = input("Apakah Anda yakin untuk logout? Ketik 'YA' untuk konfirmasi: ").strip().upper()
            if konfirmasi == 'YA':
                print(f"Anda telah logout dari akun {self.logged_in_user['username']}.")
                self.logged_in_user = None
            else:
                print("Logout dibatalkan.")
        else:
            print("Anda belum login.")

class MyVendingStatus:
    def __init__(self):
        self.suhu = 5  # Suhu awal, misalnya dalam °C
        self.kelembapan = 50  # Kelembapan awal, misalnya dalam persentase (%)
    
    def display_status(self):
        # Menampilkan status MyVending dengan format khusus
        print("======================================")
        print("||==================||==============||")
        print(f"||                  || Suhu || {self.suhu:3}°C ||||")
        print(f"||     MyVending    || Waktu || {time.strftime('%H:%M')} ||||")
        print(f"||                  || Mois  || {self.kelembapan:3}% ||||")
        print("||==================||==============||")
        print("======================================\n")
    
    def set_suhu(self, perubahan):
        # Mengubah suhu berdasarkan input perubahan
        self.suhu += perubahan
        print(f"Suhu berhasil diubah menjadi {self.suhu}°C.")
        
        # Memberikan peringatan jika suhu berada di luar batas normal
        if self.suhu > 10:
            print("Peringatan: Suhu terlalu tinggi, minuman akan tidak dingin.")
        elif self.suhu < 0:
            print("Peringatan: Suhu terlalu rendah, minuman akan beku.")
    
    def set_kelembapan(self, perubahan):
        # Mengubah kelembapan dengan batas minimum 0% dan maksimum 100%
        self.kelembapan = max(0, min(100, self.kelembapan + perubahan))
        print(f"Kelembapan berhasil diubah menjadi {self.kelembapan}%.")

        # Memberikan peringatan jika kelembapan terlalu tinggi
        if self.kelembapan > 70:
            print("Peringatan: Kelembapan terlalu tinggi, ini akan mempercepat pertumbuhan jamur.")

def main():
    stok = StokBarang()
    log = LogAktivitas()
    pembayaran = SistemPembayaran()
    display = Display()
    pesanan = PemrosesanPesanan(stok, log, pembayaran)
    akun = Akun()  # Mengelola data akun
    vending_status = MyVendingStatus()  # Status suhu dan kelembapan MyVending

    admin_password = "Admin#123"  # Password baru untuk akses ke Menu Admin

    while True:
        clear_screen()
        
        # Menampilkan Header Utama
        print("||=================================================||")
        print("||               SELAMAT DATANG DI MYVENDING       ||")
        print("||=================================================||")
        print("||                Selamat berbelanja!              ||")
        print("||=================================================||\n")
        
        # Menampilkan Daftar Produk di Awal
        stok.display_products()
        
        # Tampilkan menu utama
        print("\n||=================================================||")
        print("||                    MENU UTAMA                   ||")
        print("||=================================================||")
        print("1. Belanja Produk")
        print("2. Login Akun")
        print("3. Menu Admin")
        print("4. Keluar")
        print("----------------------------------------------------")
        
        pilihan_menu = int(input("Pilihan: "))

        if pilihan_menu == 1:
            # Menu Belanja Produk
            while True: 
                clear_screen()
                print("||=================================================||")
                print("||                    MY VENDING                   ||".center(49))
                print("||               Menu Belanja Produk               ||".center(49))
                print("||=================================================||")
                
                stok.display_products()  # Menampilkan daftar produk
                print("\n1. Tambahkan Produk ke Keranjang")
                print("2. Pembayaran")
                print("3. Cek Keranjang")
                print("4. Hapus Produk dari Keranjang")
                print("5. Kembali ke Menu Utama")

                pilihan_menubelanja = int(input("Pilihan: "))
                
                if pilihan_menubelanja == 1:
                    # Menambahkan produk ke keranjang
                    ulang = "ya"
                    while ulang.lower() == "ya":  
                        clear_screen()
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||         Penambahan Produk ke Keranjang          ||".center(49))
                        print("||=================================================||")
                        stok.display_products()
                        kode_produk = int(input("\nKode produk\t\t: "))
                        kuantitas_produk = int(input("Kuantitas produk\t: "))
                        pesanan.tambah_ke_keranjang(kode_produk, kuantitas_produk)  
                        ulang = input("Apakah Anda ingin menambahkan produk lainnya ke keranjang(ya/tidak)? ").lower()
                        if ulang not in ["ya", "tidak"]:  
                            print("Pilihan tidak valid. Harap jawab dengan 'ya' atau 'tidak'.")
                            ulang = "tidak"

                elif pilihan_menubelanja == 2:
                    # Proses pembayaran
                    clear_screen()
                    print("||=================================================||")
                    print("||                    MY VENDING                   ||".center(49))
                    print("||                    Pembayaran                   ||".center(49))
                    print("||=================================================||")
                    pesanan.cek_keranjang()
                    pesanan.proses_checkout()
                    break

                elif pilihan_menubelanja == 3:
                    # Cek keranjang
                    clear_screen()
                    print("||=================================================||")
                    print("||                   MY VENDING                    ||".center(49))
                    print("||                  Cek Keranjang                  ||".center(49))
                    print("||=================================================||")
                    pesanan.cek_keranjang()

                elif pilihan_menubelanja == 4:
                    # Hapus produk dari keranjang
                    ulang = "ya"
                    while ulang.lower() == "ya":  
                        clear_screen()
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||           Hapus Produk dari Keranjang           ||".center(49))
                        print("||=================================================||")
                        if pesanan.cek_keranjang() == True:
                            kode_produk = int(input("Masukkan kode produk: "))
                            pesanan.hapus_dari_keranjang(kode_produk)
                        else:
                            print("\n" + "Keranjang Anda kosong.".center(55))
                        ulang = input("Apakah Anda ingin menghapus produk lainnya dari keranjang(ya/tidak)? ").lower()
                        if ulang not in ["ya", "tidak"]:  
                            print("Pilihan tidak valid. Harap jawab dengan 'ya' atau 'tidak'.")
                            ulang = "tidak"

                elif pilihan_menubelanja == 5: 
                    break  # Kembali ke menu utama
                
                else:
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                
                input("\nTekan Enter untuk melanjutkan...")
        
        elif pilihan_menu == 2:
            # Menu Akun
            while True:
                clear_screen()
                print("||=================================================||")
                print("||                    MY VENDING                   ||".center(49))
                print("||                    Menu Akun                    ||".center(49))
                print("||=================================================||")
                
                print("\n1. Login")
                print("2. Buat Akun Baru")
                print("3. Tambah Saldo MyPay")
                print("4. Tarik Saldo MyPay")
                print("5. Logout")
                print("6. Kembali ke Menu Utama")

                pilihan_akun = int(input("Pilihan: "))

                if pilihan_akun == 1:
                    akun.login()  # Fungsi login di kelas Akun
                elif pilihan_akun == 2:
                    akun.buat_akun_baru()  # Fungsi buat akun baru
                elif pilihan_akun == 3:
                    akun.tambah_saldo_mypay()  # Fungsi tambah saldo MyPay
                elif pilihan_akun == 4:
                    akun.tarik_saldo_mypay()  # Fungsi tarik saldo MyPay
                elif pilihan_akun == 5:
                    akun.logout()  # Fungsi logout
                elif pilihan_akun == 6:
                    break  # Kembali ke Menu Utama
                else:
                    print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!")
                
                input("Tekan Enter untuk melanjutkan...")

        elif pilihan_menu == 3:
            # Meminta Password untuk Mengakses Menu Admin
            input_password = getpass.getpass("Masukkan password untuk akses Menu Admin: ")  # Menggunakan getpass untuk menyembunyikan input password
            
            if input_password == admin_password:
                # Jika password benar, akses Menu Admin
                while True:
                    clear_screen()
                    print("||=================================================||")
                    print("||                    MY VENDING                   ||".center(49))
                    print("||                    Menu Admin                   ||".center(49))
                    print("||=================================================||")
                    print("\n1. Tampilkan Riwayat Aktivitas")
                    print("2. Status MyVending")
                    print("3. Ubah Produk di MyVending")
                    print("4. Kembali ke Menu Utama")

                    pilihan_menuadmin = int(input("Pilihan: "))
                    
                    if pilihan_menuadmin == 1:
                        clear_screen()
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||                Riwayat Aktivitas                ||".center(49))
                        print("||=================================================||")
                        log.show_history()
                        print()

                    elif pilihan_menuadmin == 2:
                        # Menampilkan Status MyVending
                        while True:
                            clear_screen()
                            print("||=================================================||")
                            print("||                    MY VENDING                   ||".center(49))
                            print("||                 Status MyVending                ||".center(49))
                            print("||=================================================||")
                            
                            vending_status.display_status()  # Menampilkan status suhu dan kelembapan
                            print("\n1. Atur Suhu")
                            print("2. Atur Kelembapan")
                            print("3. Kembali ke Menu Admin")

                            pilihan_status = int(input("Pilihan: "))
                            
                            if pilihan_status == 1:
                                perubahan_suhu = int(input("Masukkan perubahan suhu (positif untuk tambah, negatif untuk kurangi): "))
                                vending_status.set_suhu(perubahan_suhu)
                                input("\nTekan Enter untuk kembali ke status...")  # Kembali ke status setelah atur suhu
                            elif pilihan_status == 2:
                                perubahan_kelembapan = int(input("Masukkan perubahan kelembapan (positif untuk tambah, negatif untuk kurangi): "))
                                vending_status.set_kelembapan(perubahan_kelembapan)
                                input("\nTekan Enter untuk kembali ke status...")  # Kembali ke status setelah atur kelembapan
                            elif pilihan_status == 3:
                                break
                            else:
                                print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                    
                    elif pilihan_menuadmin == 3:
                        # Ubah Produk di MyVending (Tidak diubah)
                        pass
                    elif pilihan_menuadmin == 4:
                        break
                    else:
                        print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                    
                    input("Tekan Enter untuk melanjutkan...")
            else:
                # Jika password salah, cukup satu kali enter untuk kembali ke Menu Utama
                print("Password salah. Kembali ke Menu Utama.")

        elif pilihan_menu == 4:
            print("Terima kasih telah mengunjungi MyVending!")
            exit()
        else:
            print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!")
            
        input("\nTekan Enter untuk melanjutkan...")  # Satu kali enter setelah semua kondisi

main()