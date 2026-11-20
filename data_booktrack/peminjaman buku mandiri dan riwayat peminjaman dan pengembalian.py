import csv
import os
from datetime import datetime, timedelta

# ==================================================
# BOOK TRACK - MODUL PEMINJAMAN MANDIRI & RIWAYAT
# Isi: peminjaman mandiri, riwayat peminjaman,
#      riwayat pengembalian
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "data_booktrack")

DENDA_PER_HARI = 1000
LAMA_PINJAM = 7
MAKS_PINJAMAN_AKTIF = 3   # batas buku yang boleh dipinjam bersamaan

FILES = {
    "buku": os.path.join(FOLDER, "buku.csv"),
    "anggota": os.path.join(FOLDER, "anggota.csv"),
    "akun": os.path.join(FOLDER, "akun.csv"),
    "peminjaman": os.path.join(FOLDER, "peminjaman.csv"),
    "perpanjangan": os.path.join(FOLDER, "perpanjangan.csv"),
    "riwayat": os.path.join(FOLDER, "riwayat.csv"),
}

KOLOM = {
    "buku": ["id_buku", "judul", "penulis", "kategori", "stok"],
    "anggota": ["id_anggota", "nama", "kelas"],
    "akun": ["username", "password", "role", "id_anggota"],
    "peminjaman": [
        "id_pinjam", "id_anggota", "id_buku", "judul",
        "tanggal_pinjam", "jatuh_tempo",
        "tanggal_kembali", "status", "denda", "status_denda",
    ],
    "perpanjangan": [
        "id_perpanjangan", "id_pinjam", "tanggal_pengajuan", "status",
    ],
    "riwayat": ["tanggal", "username", "aktivitas"],
}


# ==================================================
# 1. FUNGSI DASAR CSV
# ==================================================

def baca_csv(jenis):
    with open(FILES[jenis], "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def simpan_csv(jenis, data):
    with open(FILES[jenis], "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=KOLOM[jenis])
        writer.writeheader()
        writer.writerows(data)


def tambah_csv(jenis, data):
    with open(FILES[jenis], "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=KOLOM[jenis])
        writer.writerow(data)


def persiapan_data():
    """Membuat folder, file CSV kosong, dan data contoh jika belum ada."""
    os.makedirs(FOLDER, exist_ok=True)

    for jenis in FILES:
        if not os.path.exists(FILES[jenis]):
            simpan_csv(jenis, [])

    if not baca_csv("buku"):
        simpan_csv("buku", [
            {"id_buku": "B001", "judul": "Laskar Pelangi", "penulis": "Andrea Hirata", "kategori": "Novel", "stok": "5"},
            {"id_buku": "B002", "judul": "Bumi", "penulis": "Tere Liye", "kategori": "Fiksi", "stok": "4"},
            {"id_buku": "B003", "judul": "Atomic Habits", "penulis": "James Clear", "kategori": "Pengembangan Diri", "stok": "3"},
        ])

    if not baca_csv("anggota"):
        tambah_csv("anggota", {
            "id_anggota": "A001", "nama": "Peminjam Contoh", "kelas": "Sistem Informasi",
        })

    if not baca_csv("akun"):
        tambah_csv("akun", {
            "username": "peminjam", "password": "pinjam123",
            "role": "peminjam", "id_anggota": "A001",
        })


# ==================================================
# 2. FUNGSI UMUM
# ==================================================

def garis():
    print("=" * 65)


def judul(teks):
    print()
    garis()
    print(teks.center(65))
    garis()


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


def hari_ini():
    return datetime.now().date()


def tanggal_tampil(tanggal):
    if not tanggal:
        return "-"
    return datetime.strptime(tanggal, "%Y-%m-%d").strftime("%d-%m-%Y")


def rupiah(angka):
    return "Rp {:,}".format(int(angka)).replace(",", ".")


def buat_id(jenis, kolom, awalan):
    nomor_terbesar = 0
    for item in baca_csv(jenis):
        try:
            nomor = int(item[kolom][len(awalan):])
            nomor_terbesar = max(nomor_terbesar, nomor)
        except ValueError:
            continue
    return awalan + str(nomor_terbesar + 1).zfill(3)


def catat_riwayat(username, aktivitas):
    tambah_csv("riwayat", {
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "username": username,
        "aktivitas": aktivitas,
    })


def tampilkan_buku():
    judul("KATALOG BUKU")
    buku = baca_csv("buku")

    if not buku:
        print("Belum ada data buku.")
        return

    print(f"{'ID':<8} {'JUDUL':<25} {'PENULIS':<20} {'STOK':<6}")
    garis()
    for b in buku:
        print(
            f"{b['id_buku']:<8} "
            f"{b['judul'][:24]:<25} "
            f"{b['penulis'][:19]:<20} "
            f"{b['stok']:<6}"
        )


# ==================================================
# 3. PEMINJAMAN BUKU MANDIRI
# ==================================================

def ajukan_peminjaman(user):
    judul("PEMINJAMAN BUKU MANDIRI")

    peminjaman = baca_csv("peminjaman")
    milik_user = [p for p in peminjaman if p["id_anggota"] == user["id_anggota"]]

    # Cek 1: denda yang belum lunas
    if any(int(p["denda"]) > 0 and p["status_denda"] != "Lunas" for p in milik_user):
        print("Kamu masih memiliki denda yang belum lunas!")
        print("Selesaikan pembayaran denda ke petugas terlebih dahulu.")
        return

    # Cek 2: batas jumlah pinjaman aktif
    aktif = [p for p in milik_user if p["status"] == "Dipinjam"]
    if len(aktif) >= MAKS_PINJAMAN_AKTIF:
        print(f"Batas peminjaman tercapai (maksimal {MAKS_PINJAMAN_AKTIF} buku).")
        return

    tampilkan_buku()

    id_buku = input("\nMasukkan ID buku: ").strip().upper()
    buku = baca_csv("buku")
    buku_dipilih = next((b for b in buku if b["id_buku"] == id_buku), None)

    if buku_dipilih is None:
        print("Buku tidak ditemukan!")
        return

    if int(buku_dipilih["stok"]) <= 0:
        print("Stok buku sedang habis!")
        return

    # Cek 3: buku yang sama masih dipinjam
    if any(p["id_buku"] == id_buku for p in aktif):
        print("Kamu masih meminjam buku ini!")
        return

    # Tanggal pinjam otomatis = hari ini (peminjaman mandiri)
    tanggal_pinjam = hari_ini()
    jatuh_tempo = tanggal_pinjam + timedelta(days=LAMA_PINJAM)

    print("\nBuku dipilih       :", buku_dipilih["judul"])
    print("Tanggal peminjaman :", tanggal_tampil(tanggal_pinjam.isoformat()))
    print("Batas pengembalian :", tanggal_tampil(jatuh_tempo.isoformat()))
    print("Denda keterlambatan:", rupiah(DENDA_PER_HARI), "/ hari")

    if input("\nLanjutkan peminjaman? (y/n): ").strip().lower() != "y":
        print("Peminjaman dibatalkan.")
        return

    id_pinjam = buat_id("peminjaman", "id_pinjam", "P")

    tambah_csv("peminjaman", {
        "id_pinjam": id_pinjam,
        "id_anggota": user["id_anggota"],
        "id_buku": id_buku,
        "judul": buku_dipilih["judul"],
        "tanggal_pinjam": tanggal_pinjam.isoformat(),
        "jatuh_tempo": jatuh_tempo.isoformat(),
        "tanggal_kembali": "",
        "status": "Dipinjam",
        "denda": "0",
        "status_denda": "Tidak Ada",
    })

    # Kurangi stok
    buku_dipilih["stok"] = str(int(buku_dipilih["stok"]) - 1)
    simpan_csv("buku", buku)

    catat_riwayat(user["username"], "Meminjam buku " + buku_dipilih["judul"])

    print("\nPEMINJAMAN BERHASIL!")
    print("ID Peminjaman     :", id_pinjam)
    print("Judul Buku        :", buku_dipilih["judul"])
    print("Tanggal Pinjam    :", tanggal_tampil(tanggal_pinjam.isoformat()))
    print("Batas Pengembalian:", tanggal_tampil(jatuh_tempo.isoformat()))
    print("Status            : Dipinjam")


# ==================================================
# 4. RIWAYAT PEMINJAMAN
# ==================================================

def riwayat_peminjaman(user):
    judul("RIWAYAT PEMINJAMAN")

    data_user = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
    ]

    if not data_user:
        print("Belum ada riwayat peminjaman.")
        return

    # Terbaru di atas
    data_user.sort(key=lambda p: p["tanggal_pinjam"], reverse=True)

    print(f"{'ID':<7} {'JUDUL':<24} {'PINJAM':<11} {'TEMPO':<11} {'STATUS':<13}")
    garis()

    for p in data_user:
        print(
            f"{p['id_pinjam']:<7} "
            f"{p['judul'][:23]:<24} "
            f"{tanggal_tampil(p['tanggal_pinjam']):<11} "
            f"{tanggal_tampil(p['jatuh_tempo']):<11} "
            f"{p['status']:<13}"
        )

        if p["status"] == "Dipinjam":
            jatuh_tempo = datetime.strptime(p["jatuh_tempo"], "%Y-%m-%d").date()
            sisa = (jatuh_tempo - hari_ini()).days

            if sisa > 0:
                print(f"        -> Sisa waktu {sisa} hari")
            elif sisa == 0:
                print("        -> Hari terakhir pengembalian!")
            else:
                telat = abs(sisa)
                print(
                    f"        -> TERLAMBAT {telat} hari "
                    f"(estimasi denda {rupiah(telat * DENDA_PER_HARI)})"
                )

    aktif = sum(1 for p in data_user if p["status"] == "Dipinjam")
    print()
    garis()
    print(f"Total transaksi: {len(data_user)} | Sedang dipinjam: {aktif}")


# ==================================================
# 5. RIWAYAT PENGEMBALIAN
# ==================================================

def riwayat_pengembalian(user):
    judul("RIWAYAT PENGEMBALIAN")

    data_kembali = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
        and p["status"] == "Dikembalikan"
    ]

    if not data_kembali:
        print("Belum ada buku yang dikembalikan.")
        return

    data_kembali.sort(key=lambda p: p["tanggal_kembali"], reverse=True)

    total_denda = 0
    belum_lunas = 0

    for p in data_kembali:
        jatuh_tempo = datetime.strptime(p["jatuh_tempo"], "%Y-%m-%d").date()
        kembali = datetime.strptime(p["tanggal_kembali"], "%Y-%m-%d").date()
        telat = max(0, (kembali - jatuh_tempo).days)
        denda = int(p["denda"])

        total_denda += denda
        if p["status_denda"] == "Belum Lunas":
            belum_lunas += denda

        print("\nID Peminjaman   :", p["id_pinjam"])
        print("Judul Buku      :", p["judul"])
        print("Tanggal Pinjam  :", tanggal_tampil(p["tanggal_pinjam"]))
        print("Jatuh Tempo     :", tanggal_tampil(p["jatuh_tempo"]))
        print("Tanggal Kembali :", tanggal_tampil(p["tanggal_kembali"]))
        print("Keterlambatan   :", telat, "hari" if telat else "(tepat waktu)")
        print("Denda           :", rupiah(denda))
        print("Status Denda    :", p["status_denda"])

    print()
    garis()
    print("Total buku dikembalikan :", len(data_kembali))
    print("Total denda keseluruhan :", rupiah(total_denda))
    print("Denda belum lunas       :", rupiah(belum_lunas))


# ==================================================
# 6. MENU UJI COBA (opsional, untuk dijalankan terpisah)
# ==================================================

def login():
    judul("LOGIN")
    username = input("Username : ").strip()
    password = input("Password : ").strip()

    for akun in baca_csv("akun"):
        if akun["username"] == username and akun["password"] == password:
            if akun["role"] != "peminjam":
                print("Modul ini hanya untuk peminjam.")
                return None
            catat_riwayat(username, "Login ke sistem")
            return akun

    print("Username atau password salah!")
    return None


def menu_peminjam(user):
    while True:
        judul("MENU PEMINJAM")
        print("1. Pinjam buku (mandiri)")
        print("2. Riwayat peminjaman")
        print("3. Riwayat pengembalian")
        print("4. Logout")

        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "1":
            ajukan_peminjaman(user)
        elif pilihan == "2":
            riwayat_peminjaman(user)
        elif pilihan == "3":
            riwayat_pengembalian(user)
        elif pilihan == "4":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break
        else:
            print("Pilihan tidak valid!")

        jeda()


def main():
    persiapan_data()
    user = login()
    if user:
        menu_peminjam(user)


if __name__ == "__main__":
    main()
