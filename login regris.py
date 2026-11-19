import csv
import os

# BOOK TRACK - LOGIN DAN REGISTRASI 

# File akun.csv disimpan di folder yang sama dengan file .py ini
folder = os.path.dirname(os.path.abspath(__file__))
file_akun = os.path.join(folder, "akun.csv")


# Menyiapkan file CSV
def siapkan_file():
    # Kalau akun.csv belum ada, buat dulu beserta 2 akun contoh
    if not os.path.exists(file_akun):
        with open(file_akun, "w", newline="", encoding="utf-8") as f:
            tulis = csv.writer(f)
            tulis.writerow(["username", "password", "role", "nama", "kelas"])
            tulis.writerow(["petugas", "admin123", "petugas", "Petugas", "-"])
            tulis.writerow(["peminjam", "pinjam123", "peminjam", "Peminjam Contoh", "Sistem Informasi"])


def baca_akun():
    # Mengambil semua akun dari CSV
    with open(file_akun, "r", newline="", encoding="utf-8") as f:
        baca = csv.reader(f)
        next(baca)  # lewati baris judul
        return list(baca)

# Login
def login():
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    for akun in baca_akun():
        if akun[0] == username and akun[1] == password:
            print("Login berhasil! Selamat datang,", akun[3])
            return akun

    print("Username atau password salah!")
    return None


# Registrasi
def registrasi():
    print("\n=== REGISTRASI ===")
    username = input("Buat username: ")

    if username == "":
        print("Username tidak boleh kosong!")
        return

    # Ceuntuk ck username sudah dipakai atau belum
    for akun in baca_akun():
        if akun[0] == username:
            print("Username sudah dipakai!")
            return

    password = input("Buat password: ")
    nama = input("Nama lengkap: ")
    kelas = input("Program Studi: ")

    if password == "" or nama == "" or kelas == "":
        print("Semua data harus diisi!")
        return

    # Simpan akun baru ke CSV (role otomatis peminjam)
    with open(file_akun, "a", newline="", encoding="utf-8") as f:
        tulis = csv.writer(f)
        tulis.writerow([username, password, "peminjam", nama, kelas])

    print("Registrasi berhasil! Silakan login.")


# Menu setelah login (sementara)
def menu_user(akun):
    role = akun[2]

    while True:
        print("\n=== MENU ===")
        print("1. Logout")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            print("Berhasil logout!")
            break
        else:
            print("Pilihan tidak valid!")


# Program utama
def main():
    siapkan_file()

    while True:
        print("\n=== BOOK TRACK ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih: ")

        if pilihan == "1":
            akun = login()
            if akun is not None:
                menu_user(akun)

        elif pilihan == "2":
            registrasi()

        elif pilihan == "3":
            print("Terima kasih! SYDAH MAMPIR")
            break

        else:
            print("Pilihan tidak valid!")


main()