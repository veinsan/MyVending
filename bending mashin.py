import os
import time
import csv
import getpass
import qrcode

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
    
    def menu_admin(self):
        print("\n\n|----------------------------------------------------|")
        print("| MENU ADMIN                                        |".center(49))
        print("| 1. Tampilkan Riwayat Aktivitas                    |".center(49))
        print("| 2. Status MyVending                               |".center(49))
        print("| 3. Kelola Produk di MyVending                     |".center(49))
        print("| 4. Cek Saldo Kembalian Tunai                      |".center(49))
        print("| 5. Kembali ke Menu Utama                          |".center(49))
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
    
    def tambah_stok(self, product_code, tambahan, log):
        if product_code in self.products:
            current_stock = self.products[product_code]["stock"]
            if current_stock + tambahan > 25:
                print("Stok akan overload! Stok maksimal adalah 25.")
                return False
            else:
                self.products[product_code]["stock"] += tambahan
                log.add_log("Tambah Stok", f"{self.products[product_code]['name']} - Tambah {tambahan} (Total: {self.products[product_code]['stock']})")
                print(f"Stok {self.products[product_code]['name']} berhasil ditambahkan sebanyak {tambahan}. Total stok: {self.products[product_code]['stock']}.")
                input("\nTekan Enter untuk melanjutkan...")
                return True
        else:
            print("Kode produk tidak valid.")
            input("\nTekan Enter untuk melanjutkan...")
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
    def __init__(self, kembalian):
        self.saldo = 0  # Inisialisasi saldo MyPay
        self.kembalian = kembalian  # Menggunakan class SistemKembalian untuk mengelola kembalian

    def bayar_dengan_tunai(self, total_harga):
        print("Masukkan nominal uang yang digunakan untuk membayar (gunakan pecahan Rp1000, Rp2000, Rp5000, Rp10000, Rp20000, Rp50000, Rp100000).")
        sisa_pembayaran = total_harga
        while sisa_pembayaran > 0:
            nominal = int(input(f"Sisa pembayaran: Rp{sisa_pembayaran}. Masukkan nominal: Rp"))
            jumlah = int(input(f"Berapa lembar Rp{nominal}? "))
            total_input = nominal * jumlah

            if total_input > sisa_pembayaran:
                kembalian = total_input - sisa_pembayaran
                print(f"Kembalian: Rp{kembalian}")
                self.kembalian.update_kembalian(nominal, jumlah)  # Update saldo kembalian
                return True
            elif total_input == sisa_pembayaran:
                print("Pembayaran berhasil. Tidak ada kembalian.")
                self.kembalian.update_kembalian(nominal, jumlah)
                return True
            else:
                sisa_pembayaran -= total_input
                self.kembalian.update_kembalian(nominal, jumlah)
        return True

    def proses_checkout(self, total_harga):
        print("\nPilih metode pembayaran:")
        print("1. MyPay (Saldo)")
        print("2. QRIS")
        print("3. Tunai")

        pilihan_pembayaran = int(input("Pilihan: "))
        if pilihan_pembayaran == 1:
            return self.bayar_dengan_saldo(total_harga)
        elif pilihan_pembayaran == 2:
            link_qris = "https://example.com/qris-payment?transaction_id=123456789"
            print("\nPembayaran melalui QRIS sedang diproses...")
            self.generate_qris_ascii(link_qris)
            input("Tekan Enter setelah melakukan pembayaran.")
            print("Pembayaran dengan QRIS berhasil.")
            return True
        elif pilihan_pembayaran == 3:
            return self.bayar_dengan_tunai(total_harga)
        else:
            print("Metode pembayaran tidak valid. Kembali ke menu pembayaran.")
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
        if not self.cart:
            print("\nKeranjang Anda kosong. Tidak ada produk yang dapat dihapus.\n")
            return

        for item in self.cart:
            print(f"Kode: {item['code']}, Nama: {item['name']}, Jumlah: {item['quantity']}, Harga: Rp{item['price']}")
        print("|---------------------------------------------------|")
        print("")

        kode_hapus = int(input("Masukkan kode produk yang ingin dihapus dari keranjang: "))
        for item in self.cart:
            if item["code"] == kode_hapus:
                self.cart.remove(item)
                self.total_harga -= item["price"]
                print(f"{item['name']} telah dihapus dari keranjang.")
                return
        print(f"Produk dengan kode {kode_hapus} tidak ditemukan di keranjang.\n")

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
        return True

    def proses_checkout(self, total_harga):
        print("\nPilih metode pembayaran:")
        print("1. MyPay (Saldo)")
        print("2. QRIS")
        print("3. Tunai")
        print("4. GoPay")
        print("5. OVO")
        print("6. Dana")

        pilihan_pembayaran = int(input("Pilihan: "))
        if pilihan_pembayaran == 1:
            return self.bayar_dengan_saldo(total_harga)
        elif pilihan_pembayaran == 2:
            link_qris = "https://example.com/qris-payment?transaction_id=123456789"
            print("\nPembayaran melalui QRIS sedang diproses...")
            self.generate_qris_ascii(link_qris)
            input("Tekan Enter setelah melakukan pembayaran.")
            print("Pembayaran dengan QRIS berhasil.")
            return True
        elif pilihan_pembayaran == 3:
            return self.bayar_dengan_tunai(total_harga)
        elif pilihan_pembayaran in [4, 5, 6]:
            metode = {4: "GoPay", 5: "OVO", 6: "Dana"}
            print(f"\nSilakan transfer Rp{total_harga} ke nomor '089656054453' melalui {metode[pilihan_pembayaran]}.")
            input("Tekan Enter setelah melakukan pembayaran.")
            print(f"Pembayaran dengan {metode[pilihan_pembayaran]} berhasil.")
            return True
        else:
            print("Metode pembayaran tidak valid. Kembali ke menu pembayaran.")
            return False


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

class SistemKembalian:
    def __init__(self, file_csv="kembalian.csv"):
        self.file_csv = file_csv
        self.saldo = self._load_saldo()

    def _load_saldo(self):
        saldo = {}
        try:
            with open(self.file_csv, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "nominal" in row and "jumlah" in row:  # Periksa apakah kolom sesuai
                        nominal = int(row["nominal"])
                        jumlah = int(row["jumlah"])
                        saldo[nominal] = jumlah
                    else:
                        raise ValueError("Header CSV tidak valid. Diperlukan 'nominal' dan 'jumlah'.")
        except (FileNotFoundError, ValueError):
            print(f"File {self.file_csv} tidak ditemukan atau tidak valid. Membuat file baru...")
            self._initialize_csv()
            saldo = self._load_saldo()  # Reload setelah inisialisasi
        return saldo

    def _initialize_csv(self):
        with open(self.file_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["nominal", "jumlah"])
            writer.writeheader()
            for nominal in [1000, 2000, 5000, 10000, 20000, 50000, 100000]:
                writer.writerow({"nominal": nominal, "jumlah": 0})

    def cek_saldo_kembalian(self):
        print("\n|| Saldo Kembalian Tunai ||")
        print("||------------------------||")
        total_saldo = 0
        for nominal, jumlah in sorted(self.saldo.items()):
            print(f"|| Rp{nominal:<7} | {jumlah:<4} lembar ||")
            total_saldo += nominal * jumlah
        print("||------------------------||")
        print(f"|| Total Saldo: Rp{total_saldo:<15} ||")
        print("||------------------------||")

    def update_kembalian(self, nominal, jumlah):
        if nominal in self.saldo:
            self.saldo[nominal] += jumlah
        else:
            self.saldo[nominal] = jumlah

        with open(self.file_csv, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["nominal", "jumlah"])
            writer.writeheader()
            for nominal, jumlah in self.saldo.items():
                writer.writerow({"nominal": nominal, "jumlah": jumlah})

    def tambah_saldo(self, nominal, jumlah):
        print(f"Menambahkan Rp{nominal} x{jumlah} ke saldo kembalian.")
        self.update_kembalian(nominal, jumlah)

def main():
    stok = StokBarang()
    log = LogAktivitas()
    kembalian = SistemKembalian("kembalian.csv")  # Hubungkan dengan CSV
    pembayaran = SistemPembayaran(kembalian)  # Hubungkan SistemKembalian dengan SistemPembayaran
    display = Display()
    pesanan = PemrosesanPesanan(stok, log, pembayaran)
    akun = Akun()
    vending_status = MyVendingStatus()

    admin_password = "Admin#123"

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
                    print("3. Kelola Produk di MyVending")
                    print("4. Cek Saldo Kembalian Tunai")
                    print("5. Kembali ke Menu Utama")

                    pilihan_menuadmin = int(input("Pilihan: "))
                    
                    if pilihan_menuadmin == 1:
                        clear_screen()
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||                Riwayat Aktivitas                ||".center(49))
                        print("||=================================================||")
                        log.show_history()
                        input("\nTekan Enter untuk kembali ke Menu Admin...")

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
                        # Kelola Produk di MyVending
                        while True:
                            clear_screen()
                            print("||=================================================||")
                            print("||                    MY VENDING                   ||".center(49))
                            print("||                  Kelola Produk                  ||".center(49))
                            print("||=================================================||")
                            
                            stok.display_products()  # Menampilkan daftar produk
                            print("\n1. Tambah Stok Produk")
                            print("2. Kembali ke Menu Admin")

                            pilihan_kelola_produk = int(input("Pilihan: "))

                            if pilihan_kelola_produk == 1:
                                kode_produk = int(input("Masukkan kode produk yang ingin ditambah stok: "))
                                jumlah_tambah = int(input("Masukkan jumlah stok yang ingin ditambahkan: "))
                                
                                if kode_produk in stok.products:
                                    produk = stok.products[kode_produk]
                                    if produk["stock"] + jumlah_tambah > 25:
                                        print("Stok melebihi kapasitas maksimal (25). Tidak bisa menambah stok.")
                                    else:
                                        produk["stock"] += jumlah_tambah
                                        print(f"Stok {produk['name']} berhasil ditambah menjadi {produk['stock']}.")
                                        log.add_log("Tambah Stok", f"{produk['name']} +{jumlah_tambah}")
                                        input("\nTekan Enter untuk melanjutkan...")
                                else:
                                    print("Kode produk tidak ditemukan.")
                                    input("\nTekan Enter untuk melanjutkan...")

                            elif pilihan_kelola_produk == 2:
                                break  # Kembali ke Menu Admin
                            else:
                                print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                    
                    elif pilihan_menuadmin == 4:
                        # Cek Saldo Kembalian Tunai
                        clear_screen()
                        print("||=================================================||")
                        print("||                    MY VENDING                   ||".center(49))
                        print("||               Cek Saldo Kembalian Tunai         ||".center(49))
                        print("||=================================================||")
                        kembalian.cek_saldo_kembalian()
                        input("\nTekan Enter untuk kembali ke menu Admin...")  # Cukup 1 kali Enter untuk keluar

                    elif pilihan_menuadmin == 5:
                        break  # Kembali ke Menu Utama

                    else:
                        print("Pilihan tidak valid. Silakan masukkan kembali pilihan yang valid!\n")
                    
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
