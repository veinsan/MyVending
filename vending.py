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
        print("\n||==================================================||")
        print("||          PILIH PRODUK YANG INGIN DIBELI          ||")
        print("||==================================================||")
        print("|| Kode | Produk           | Harga      | Stok      ||")
        print("||--------------------------------------------------||")
        for code, product in self.products.items():
            print(f"|| {code:<4} | {product['name']:<15} | Rp{product['price']:<7} | {product['stock']:<5}   ||")
        print("||==================================================||")

    def add_stock(self, product_code, quantity):
        if product_code in self.products:
            self.products[product_code]["stock"] += quantity
            print(f"Stok untuk {self.products[product_code]['name']} berhasil ditambahkan sebanyak {quantity}.")
        else:
            print("Produk tidak ada.")

    def check_stock_and_update(self, product_code, quantity):
        if product_code in self.products and self.products[product_code]["stock"] >= quantity:
            self.products[product_code]["stock"] -= quantity
            return True
        else:
            print("Stok barang habis atau produk tidak ditemukan.")
            return False

class LogAktivitas:
    def __init__(self):
        self.history = []

    def add_log(self, product_name, quantity, price):
        self.history.append({"name": product_name, "quantity": quantity, "price": price})

    def show_history(self):
        print("\n||=================================================||")
        print("||                RIWAYAT PEMBELIAN                ||".center(49))
        print("||=================================================||")
        if not self.history:
            print("||          Belum ada riwayat pembelian            ||".center(49))
        else:
            for entry in self.history:
                print(f"|| {entry['name']} x{entry['quantity']} - Rp{entry['price']:<7}                  ||")
        print("||=================================================||")

class SistemPembayaran:
    def __init__(self):
        self.nomor_tujuan = "089656054453"

    def pilih_metode_pembayaran(self, total):
        print("\n||=================================================||")
        print("||              PILIH METODE PEMBAYARAN            ||".center(49))
        print("||=================================================||")
        print("|| 1. GoPay                                        ||".center(49))
        print("|| 2. DANA                                         ||".center(49))
        print("|| 3. OVO                                          ||".center(49))
        print("||=================================================||")
        
        metode = input("Masukkan pilihan metode pembayaran (1-3): ")
        if metode == "1":
            metode_pembayaran = "GoPay"
        elif metode == "2":
            metode_pembayaran = "DANA"
        elif metode == "3":
            metode_pembayaran = "OVO"
        else:
            print("Metode pembayaran tidak valid. Pembayaran dibatalkan.")
            return False
        
        print(f"\nSilakan transfer Rp{total} ke nomor {self.nomor_tujuan} menggunakan {metode_pembayaran}.")
        konfirmasi = input("Apakah Anda sudah melakukan pembayaran? (ya/tidak): ").lower()
        if konfirmasi == "ya":
            print("Pembayaran Diverifikasi, Pesanan Akan Segera Dibuat.\n")
            return True
        else:
            print("Pembayaran belum dikonfirmasi. Silakan lakukan pembayaran terlebih dahulu.\n")
            return False

class Display:
    def header_utama(self):
        print("||=================================================||")
        print("||           SELAMAT DATANG DI MYVENDING           ||".center(49))
        print("||=================================================||")
        print("||                Selamat berbelanja!              ||".center(49))
        print("||=================================================||")

    def menu_utama(self):
        print("||=================================================||")
        print("||                   SILAHKAN PILIH MENU           ||".center(49))
        print("||=================================================||")
        print("|| 1. Pilihan Produk                               ||".center(49))
        print("|| 2. Pilihan Bahasa dan Pengaturan                ||".center(49))
        print("|| 3. Menu Admin                                   ||".center(49))
        print("|| 4. Keluar                                       ||".center(49))
        print("||=================================================||")

    def menu_bahasa_pengaturan(self):
        print("\n||=================================================||")
        print("||                 MENU PENGATURAN                 ||".center(49))
        print("||=================================================||")
        print("|| 1. Pilihan Bahasa (Indonesia, Inggris)          ||".center(49))
        print("|| 2. Bantuan dan Informasi Panduan                ||".center(49))
        print("|| 3. Kembali ke Menu Utama                        ||".center(49))
        print("||=================================================||")

    def menu_admin(self):
        print("\n||=================================================||")
        print("||                    MENU ADMIN                   ||".center(49))
        print("||=================================================||")
        print("|| 1. Lihat Log History                            ||".center(49))
        print("|| 2. Tambah Stok Produk                           ||".center(49))
        print("|| 3. Kembali ke Menu Utama                        ||".center(49))
        print("||=================================================||")

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
            self.cart.append({"name": produk["name"], "quantity": quantity, "price": produk["price"] * quantity})
            self.total_harga += produk["price"] * quantity
            print(f"{quantity} {produk['name']} telah ditambahkan ke keranjang. Total sementara: Rp{self.total_harga}\n")
        else:
            print("Gagal menambahkan ke keranjang. Stok tidak mencukupi.\n")

    def proses_checkout(self):
        if not self.cart:
            print("Keranjang Anda kosong. Tambahkan produk terlebih dahulu.\n")
            return
        
        print("\n||=================================================||")
        print("||                  REVIEW PEMBELIAN               ||".center(49))
        print("||=================================================||")
        for item in self.cart:
            print(f"|| {item['name']} x{item['quantity']} - Rp{item['price']:<7}                   ||")
        print(f"|| Total Harga: Rp{self.total_harga:<7}                           ||")
        print("||=================================================||")

        if self.pembayaran.pilih_metode_pembayaran(self.total_harga):
            for item in self.cart:
                self.log.add_log(item["name"], item["quantity"], item["price"])
            print("Transaksi selesai, terima kasih telah berbelanja di MYVENDING!\n")
            self.cart = []
            self.total_harga = 0


def main():
    stok = StokBarang()
    log = LogAktivitas()
    pembayaran = SistemPembayaran()
    display = Display()
    pesanan = PemrosesanPesanan(stok, log, pembayaran)

    while True:
        display.header_utama()
        display.menu_utama()
        
        try:
            pilihan = int(input("Masukkan pilihan: "))
            print()  # Menambahkan spasi setelah input pilihan
        except ValueError:
            print("Masukkan pilihan yang valid.\n")
            continue

        if pilihan == 1:
            # Menu Pilihan Produk
            while True:
                stok.display_products()
                print("\n1. Tambah Produk ke Keranjang")
                print("2. Lanjutkan ke Pembayaran")
                print("3. Kembali ke Menu Utama")
                
                pilihan_produk = input("Masukkan pilihan: ")
                print()  # Menambahkan spasi setelah input pilihan

                if pilihan_produk == "1":
                    kode_produk = int(input("Masukkan kode produk yang ingin dibeli: "))
                    jumlah = int(input("Masukkan jumlah barang yang ingin dibeli: "))
                    pesanan.tambah_ke_keranjang(kode_produk, jumlah)
                elif pilihan_produk == "2":
                    pesanan.proses_checkout()
                    break
                elif pilihan_produk == "3":
                    print("Kembali ke Menu Utama.\n")
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.\n")

        elif pilihan == 2:
            # Menampilkan menu pengaturan bahasa dan pengaturan lain
            while True:
                display.menu_bahasa_pengaturan()
                pilihan_pengaturan = input("Masukkan pilihan pengaturan: ")
                print()  # Menambahkan spasi setelah input pilihan
                if pilihan_pengaturan == "1":
                    print("Bahasa saat ini: Indonesia. (Bahasa Inggris dapat ditambahkan)\n")
                elif pilihan_pengaturan == "2":
                    print("Panduan: Gunakan menu ini untuk berbelanja produk dengan mudah.\n")
                elif pilihan_pengaturan == "3":
                    print("Kembali ke Menu Utama.\n")
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.\n")

        elif pilihan == 3:
            # Menu admin
            while True:
                display.menu_admin()
                pilihan_admin = input("Masukkan pilihan admin: ")
                print()  # Menambahkan spasi setelah input pilihan
                if pilihan_admin == "1":
                    # Menampilkan log history
                    log.show_history()
                    print()  # Spasi tambahan setelah log history
                elif pilihan_admin == "2":
                    # Menambah stok produk
                    stok.display_products()
                    kode_produk = int(input("Masukkan kode produk untuk menambah stok: "))
                    jumlah = int(input("Masukkan jumlah stok yang ingin ditambahkan: "))
                    stok.add_stock(kode_produk, jumlah)
                    print()  # Spasi tambahan setelah stok ditambahkan
                elif pilihan_admin == "3":
                    print("Kembali ke Menu Utama.\n")
                    break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.\n")
                
        elif pilihan == 4:
            print("Terima kasih telah menggunakan MYVENDING!\n")
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.\n")

main()