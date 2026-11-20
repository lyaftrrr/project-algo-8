import csv
import os

NAMA_FILE = 'data_buku.csv'


def baca_data_buku():
    """Membuat file CSV beserta header jika belum ada."""
    if not os.path.exists(NAMA_FILE):
        with open(NAMA_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Judul', 'Penulis', 'Tahun Terbit', 'status'])
        print(f"[INFO] File '{NAMA_FILE}' berhasil dibuat.")


def tampilkan_menu():
    print("\n=== SISTEM PENGELOLAAN BUKU PERPUSTAKAAN ===")
    print("1. Tambah Buku")
    print("2. Cari Buku")
    print("3. Pinjam Buku")
    print("4. Kembalikan Buku")
    print("5. Tampilkan Semua Buku")
    print("6. Keluar")
    print("===========================================")


def tambah_buku():
    print("\n=== TAMBAH BUKU BARU ===")
    judul = input("Masukkan Judul Buku: ").strip()
    penulis = input("Masukkan Nama Penulis: ").strip()
    tahun = input("Masukkan Tahun Terbit: ").strip()

    if not judul or not penulis or not tahun:
        print("[GAGAL] Semua data wajib diisi.")
        return

    with open(NAMA_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([judul, penulis, tahun, "TERSEDIA"])
    print(f"[SUKSES] Buku '{judul}' berhasil ditambahkan.")


def cari_buku():
    print("\n=== CARI BUKU ===")
    kata_kunci = input("Masukkan judul atau penulis yang dicari: ").strip().lower()

    if not kata_kunci:
        print("[GAGAL] Kata pencarian tidak boleh kosong.")
        return

    ditemukan = False

    try:
        with open(NAMA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # lewati header

            print(f"{'Judul':<20} {'Penulis':<20} {'Tahun':<10} {'Status'}")
            print("-" * 60)

            for row in reader:
                if len(row) < 4:
                    continue

                judul, penulis, tahun, status = row
                if kata_kunci in judul.lower() or kata_kunci in penulis.lower():
                    print(f"{judul:<20} {penulis:<20} {tahun:<10} {status}")
                    ditemukan = True

        if not ditemukan:
            print("[INFO] Buku tidak ditemukan.")

    except FileNotFoundError:
        print("[ERROR] Data belum ada. Silakan tambahkan buku terlebih dahulu.")


def ubah_status_buku(judul_cari, status_baru, pesan_sukses):
    """Mengubah kolom status satu buku saja, tanpa menduplikasi data di CSV."""
    baris_data = []      # dibuat baru setiap fungsi dipanggil
    ditemukan = False

    try:
        with open(NAMA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header is None:
                print("[INFO] Belum ada data buku.")
                return
            baris_data.append(header)

            for row in reader:
                if len(row) < 4:
                    continue

                if row[0].lower() == judul_cari.strip().lower():
                    ditemukan = True

                    if status_baru == "DIPINJAM" and row[3] == "DIPINJAM":
                        print(f"[GAGAL] Buku '{row[0]}' sedang dipinjam.")
                        return

                    elif status_baru == "TERSEDIA" and row[3] == "TERSEDIA":
                        print(f"[INFO] Buku '{row[0]}' memang sudah tersedia.")
                        return

                    row[3] = status_baru
                    print(pesan_sukses.format(row[0]))

                baris_data.append(row)

        if ditemukan:
            with open(NAMA_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(baris_data)
        else:
            print("[INFO] Buku tidak ditemukan dalam sistem.")

    except FileNotFoundError:
        print("[ERROR] File data tidak ditemukan.")


def pinjam_buku():
    print("\n=== PINJAM BUKU ===")
    judul_cari = input("Masukkan Judul Buku yang ingin dipinjam: ")
    ubah_status_buku(judul_cari, "DIPINJAM", "[SUKSES] Buku '{}' berhasil dipinjam.")


def kembalikan_buku():
    print("\n=== KEMBALIKAN BUKU ===")
    judul_cari = input("Masukkan Judul Buku yang ingin dikembalikan: ")
    ubah_status_buku(judul_cari, "TERSEDIA", "[SUKSES] Buku '{}' berhasil dikembalikan.")


def tampilkan_semua_buku():
    print("\n=== DAFTAR SEMUA BUKU ===")
    try:
        with open(NAMA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)

            if header is None:
                print("[INFO] Belum ada data buku.")
                return

            print(f"{header[0]:<20} {header[1]:<20} {header[2]:<10} {header[3]}")
            print("-" * 60)

            ada_data = False
            for row in reader:
                if len(row) < 4:
                    continue
                print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10} {row[3]}")
                ada_data = True

            if not ada_data:
                print("[INFO] Belum ada data buku.")

    except FileNotFoundError:
        print("[INFO] Belum ada data buku.")


if __name__ == "__main__":
    baca_data_buku()

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-6): ").strip()

        if pilihan == '1':
            tambah_buku()
        elif pilihan == '2':
            cari_buku()
        elif pilihan == '3':
            pinjam_buku()
        elif pilihan == '4':
            kembalikan_buku()
        elif pilihan == '5':
            tampilkan_semua_buku()
        elif pilihan == '6':
            print("Terima kasih telah menggunakan sistem ini.")
            break
        else:
            print("[ERROR] Pilihan tidak valid. Silakan coba lagi.")
