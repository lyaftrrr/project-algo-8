
import csv
import os
from datetime import datetime, timedelta

# ==================================================
# BOOK TRACK - SISTEM PENGELOLAAN BUKU PERPUSTAKAAN
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "data_booktrack")

DENDA_PER_HARI = 1000
LAMA_PINJAM = 7
LAMA_PERPANJANGAN = 7

FILES = {
    "buku": os.path.join(FOLDER, "buku.csv"),
    "anggota": os.path.join(FOLDER, "anggota.csv"),
    "akun": os.path.join(FOLDER, "akun.csv"),
    "peminjaman": os.path.join(FOLDER, "peminjaman.csv"),
    "perpanjangan": os.path.join(FOLDER, "perpanjangan.csv"),
    "riwayat": os.path.join(FOLDER, "riwayat.csv")
}

KOLOM = {
    "buku": [
        "id_buku", "judul", "penulis", "kategori", "stok"
    ],
    "anggota": [
        "id_anggota", "nama", "kelas"
    ],
    "akun": [
        "username", "password", "role", "id_anggota"
    ],
    "peminjaman": [
        "id_pinjam", "id_anggota", "id_buku", "judul",
        "tanggal_pinjam", "jatuh_tempo",
        "tanggal_kembali", "status", "denda", "status_denda"
    ],
    "perpanjangan": [
        "id_perpanjangan", "id_pinjam",
        "tanggal_pengajuan", "status"
    ],
    "riwayat": [
        "tanggal", "username", "aktivitas"
    ]
}


# ==================================================
# 1. PERSIAPAN DATA DAN CSV
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
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    for jenis in FILES:
        if not os.path.exists(FILES[jenis]):
            simpan_csv(jenis, [])

    # Data buku awal
    if len(baca_csv("buku")) == 0:
        data_buku = [
            {
                "id_buku": "B001",
                "judul": "Laskar Pelangi",
                "penulis": "Andrea Hirata",
                "kategori": "Novel",
                "stok": "5"
            },
            {
                "id_buku": "B002",
                "judul": "Bumi",
                "penulis": "Tere Liye",
                "kategori": "Fiksi",
                "stok": "4"
            },
            {
                "id_buku": "B003",
                "judul": "Atomic Habits",
                "penulis": "James Clear",
                "kategori": "Pengembangan Diri",
                "stok": "3"
            },
            {
                "id_buku": "B004",
                "judul": "Algoritma dan Pemrograman",
                "penulis": "Rinaldi Munir",
                "kategori": "Pendidikan",
                "stok": "6"
            },
            {
                "id_buku": "B005",
                "judul": "Filosofi Teras",
                "penulis": "Henry Manampiring",
                "kategori": "Filsafat",
                "stok": "4"
            }
        ]

        simpan_csv("buku", data_buku)

    # Akun petugas awal
    akun = baca_csv("akun")

    if not any(a["username"] == "petugas" for a in akun):
        tambah_csv("akun", {
            "username": "petugas",
            "password": "admin123",
            "role": "petugas",
            "id_anggota": ""
        })

    # Akun peminjam contoh
    akun = baca_csv("akun")

    if not any(a["username"] == "peminjam" for a in akun):
        if not any(a["id_anggota"] == "A001" for a in baca_csv("anggota")):
            tambah_csv("anggota", {
                "id_anggota": "A001",
                "nama": "Peminjam Contoh",
                "kelas": "Sistem Informasi"
            })

        tambah_csv("akun", {
            "username": "peminjam",
            "password": "pinjam123",
            "role": "peminjam",
            "id_anggota": "A001"
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
    if tanggal == "":
        return "-"

    return datetime.strptime(tanggal, "%Y-%m-%d").strftime("%d-%m-%Y")


def input_angka(pesan):
    while True:
        try:
            angka = int(input(pesan))

            if angka < 0:
                print("Angka tidak boleh negatif!")
                continue

            return angka

        except ValueError:
            print("Masukkan angka yang benar!")


def buat_id(jenis, kolom, awalan):
    data = baca_csv(jenis)
    nomor_terbesar = 0

    for item in data:
        try:
            nomor = int(item[kolom][len(awalan):])

            if nomor > nomor_terbesar:
                nomor_terbesar = nomor

        except ValueError:
            continue

    return awalan + str(nomor_terbesar + 1).zfill(3)


def catat_riwayat(username, aktivitas):
    tambah_csv("riwayat", {
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "username": username,
        "aktivitas": aktivitas
    })


def cari_anggota(id_anggota):
    for anggota in baca_csv("anggota"):
        if anggota["id_anggota"] == id_anggota:
            return anggota

    return None


def cari_buku_id(id_buku):
    for buku in baca_csv("buku"):
        if buku["id_buku"] == id_buku:
            return buku

    return None


def cari_pinjam(id_pinjam):
    for pinjam in baca_csv("peminjaman"):
        if pinjam["id_pinjam"] == id_pinjam:
            return pinjam

    return None


# ==================================================
# 3. LOGIN DAN REGISTRASI
# ==================================================

def login():
    judul("LOGIN BOOK TRACK")

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    for akun in baca_csv("akun"):
        if akun["username"] == username and akun["password"] == password:
            print("\nLogin berhasil!")
            print("Selamat datang,", username)

            catat_riwayat(username, "Login ke sistem")
            return akun

    print("\nUsername atau password salah!")
    return None


def registrasi():
    judul("REGISTRASI PEMINJAM")

    username = input("Buat username: ").strip()

    if username == "":
        print("Username tidak boleh kosong!")
        return

    for akun in baca_csv("akun"):
        if akun["username"] == username:
            print("Username sudah digunakan!")
            return

    password = input("Buat password: ").strip()
    nama = input("Nama lengkap: ").strip()
    kelas = input("Kelas / Program Studi: ").strip()

    if not password or not nama or not kelas:
        print("Semua data wajib diisi!")
        return

    id_anggota = buat_id("anggota", "id_anggota", "A")

    tambah_csv("anggota", {
        "id_anggota": id_anggota,
        "nama": nama,
        "kelas": kelas
    })

    tambah_csv("akun", {
        "username": username,
        "password": password,
        "role": "peminjam",
        "id_anggota": id_anggota
    })

    print("\nRegistrasi berhasil!")
    print("ID Anggota:", id_anggota)
    print("Silakan login menggunakan akun yang telah dibuat.")


# ==================================================
# 4. KATALOG DAN PENCARIAN BUKU
# ==================================================

def tampilkan_buku():
    judul("KATALOG BUKU")

    buku = baca_csv("buku")

    if not buku:
        print("Belum ada data buku.")
        return

    print(f"{'ID':<8} {'JUDUL':<25} {'PENULIS':<20} {'STOK':<6}")
    garis()

    for data in buku:
        print(
            f"{data['id_buku']:<8} "
            f"{data['judul'][:24]:<25} "
            f"{data['penulis'][:19]:<20} "
            f"{data['stok']:<6}"
        )


def cari_buku():
    judul("CARI BUKU")

    kata = input("Masukkan judul atau penulis: ").strip().lower()

    if not kata:
        print("Kata pencarian tidak boleh kosong!")
        return

    ditemukan = False

    for buku in baca_csv("buku"):
        if kata in buku["judul"].lower() or kata in buku["penulis"].lower():
            print("\nID       :", buku["id_buku"])
            print("Judul    :", buku["judul"])
            print("Penulis  :", buku["penulis"])
            print("Kategori :", buku["kategori"])
            print("Stok     :", buku["stok"])
            ditemukan = True

    if not ditemukan:
        print("Buku tidak ditemukan.")


# ==================================================
# 5. CRUD BUKU - PETUGAS
# ==================================================

def tambah_buku():
    judul("TAMBAH BUKU")

    nama = input("Judul buku: ").strip()
    penulis = input("Penulis: ").strip()
    kategori = input("Kategori: ").strip()
    stok = input_angka("Jumlah stok: ")

    if not nama or not penulis or not kategori:
        print("Data tidak boleh kosong!")
        return

    id_buku = buat_id("buku", "id_buku", "B")

    tambah_csv("buku", {
        "id_buku": id_buku,
        "judul": nama,
        "penulis": penulis,
        "kategori": kategori,
        "stok": str(stok)
    })

    print("\nBuku berhasil ditambahkan!")
    print("ID Buku:", id_buku)


def ubah_buku():
    tampilkan_buku()

    id_buku = input("\nMasukkan ID buku: ").strip()
    buku = baca_csv("buku")

    for data in buku:
        if data["id_buku"] == id_buku:

            print("\nKosongkan jika tidak ingin mengubah data.")

            nama = input("Judul baru: ").strip()
            penulis = input("Penulis baru: ").strip()
            kategori = input("Kategori baru: ").strip()
            stok = input("Stok baru: ").strip()

            if nama:
                data["judul"] = nama

            if penulis:
                data["penulis"] = penulis

            if kategori:
                data["kategori"] = kategori

            if stok:
                try:
                    stok_baru = int(stok)

                    if stok_baru < 0:
                        print("Stok tidak boleh negatif!")
                        return

                    stok_sedang_dipinjam = sum(
                        1 for p in baca_csv("peminjaman")
                        if p["id_buku"] == id_buku
                        and p["status"] == "Dipinjam"
                    )

                    if stok_baru < stok_sedang_dipinjam:
                        print("Stok tidak boleh lebih kecil dari jumlah buku yang sedang dipinjam!")
                        return

                    data["stok"] = str(stok_baru)

                except ValueError:
                    print("Stok harus berupa angka!")
                    return

            simpan_csv("buku", buku)
            print("Data buku berhasil diperbarui!")
            return

    print("Buku tidak ditemukan.")


def hapus_buku():
    tampilkan_buku()

    id_buku = input("\nMasukkan ID buku: ").strip()
    buku = baca_csv("buku")

    for data in buku:
        if data["id_buku"] == id_buku:

            aktif = any(
                p["id_buku"] == id_buku
                and p["status"] == "Dipinjam"
                for p in baca_csv("peminjaman")
            )

            if aktif:
                print("Buku masih sedang dipinjam!")
                return

            konfirmasi = input("Yakin menghapus buku? (y/n): ").lower()

            if konfirmasi == "y":
                buku.remove(data)
                simpan_csv("buku", buku)
                print("Buku berhasil dihapus!")

            return

    print("Buku tidak ditemukan.")


# ==================================================
# 6. CRUD ANGGOTA - PETUGAS
# ==================================================

def tampilkan_anggota():
    judul("DATA ANGGOTA")

    anggota = baca_csv("anggota")

    if not anggota:
        print("Belum ada anggota.")
        return

    print(f"{'ID':<12} {'NAMA':<30} {'KELAS':<20}")
    garis()

    for data in anggota:
        print(
            f"{data['id_anggota']:<12} "
            f"{data['nama']:<30} "
            f"{data['kelas']:<20}"
        )


def tambah_anggota():
    judul("TAMBAH ANGGOTA")

    nama = input("Nama anggota: ").strip()
    kelas = input("Kelas / Program Studi: ").strip()

    if not nama or not kelas:
        print("Data tidak boleh kosong!")
        return

    id_anggota = buat_id("anggota", "id_anggota", "A")

    tambah_csv("anggota", {
        "id_anggota": id_anggota,
        "nama": nama,
        "kelas": kelas
    })

    print("Anggota berhasil ditambahkan!")
    print("ID Anggota:", id_anggota)


def ubah_anggota():
    tampilkan_anggota()

    id_anggota = input("\nMasukkan ID anggota: ").strip()
    anggota = baca_csv("anggota")

    for data in anggota:
        if data["id_anggota"] == id_anggota:

            nama = input("Nama baru (kosongkan jika tetap): ").strip()
            kelas = input("Kelas baru (kosongkan jika tetap): ").strip()

            if nama:
                data["nama"] = nama

            if kelas:
                data["kelas"] = kelas

            simpan_csv("anggota", anggota)
            print("Data anggota berhasil diperbarui!")
            return

    print("Anggota tidak ditemukan.")


def hapus_anggota():
    tampilkan_anggota()

    id_anggota = input("\nMasukkan ID anggota: ").strip()
    anggota = baca_csv("anggota")

    for data in anggota:
        if data["id_anggota"] == id_anggota:

            aktif = any(
                p["id_anggota"] == id_anggota
                and p["status"] == "Dipinjam"
                for p in baca_csv("peminjaman")
            )

            if aktif:
                print("Anggota masih memiliki pinjaman aktif!")
                return

            konfirmasi = input("Hapus anggota dan akunnya? (y/n): ").lower()

            if konfirmasi == "y":
                anggota.remove(data)
                simpan_csv("anggota", anggota)

                akun = [
                    a for a in baca_csv("akun")
                    if a["id_anggota"] != id_anggota
                ]

                simpan_csv("akun", akun)
                print("Anggota dan akun berhasil dihapus!")

            return

    print("Anggota tidak ditemukan.")


# ==================================================
# 7. PEMINJAMAN LANGSUNG - PEMINJAM
# ==================================================

def ajukan_peminjaman(user):
    judul("PEMINJAMAN BUKU")

    tampilkan_buku()

    id_buku = input("\nMasukkan ID buku: ").strip()
    buku = baca_csv("buku")

    buku_dipilih = None

    for data in buku:
        if data["id_buku"] == id_buku:
            buku_dipilih = data
            break

    if buku_dipilih is None:
        print("Buku tidak ditemukan!")
        return

    if int(buku_dipilih["stok"]) <= 0:
        print("Stok buku sedang habis!")
        return

    peminjaman = baca_csv("peminjaman")

    for data in peminjaman:
        if (
            data["id_anggota"] == user["id_anggota"]
            and data["id_buku"] == id_buku
            and data["status"] == "Dipinjam"
        ):
            print("Kamu masih meminjam buku ini!")
            return

    print("\nBuku dipilih:", buku_dipilih["judul"])

    tanggal_input = input(
        "Tanggal peminjaman (DD-MM-YYYY): "
    ).strip()

    try:
        tanggal_pinjam = datetime.strptime(
            tanggal_input, "%d-%m-%Y"
        ).date()

        if tanggal_pinjam != hari_ini():
            print("Tanggal peminjaman harus sesuai tanggal hari ini!")
            return

    except ValueError:
        print("Format tanggal tidak valid!")
        return

    jatuh_tempo = tanggal_pinjam + timedelta(days=LAMA_PINJAM)

    print("\nTanggal peminjaman :", tanggal_tampil(tanggal_pinjam.isoformat()))
    print("Batas pengembalian :", tanggal_tampil(jatuh_tempo.isoformat()))

    konfirmasi = input("\nLanjutkan peminjaman? (y/n): ").lower()

    if konfirmasi != "y":
        print("Peminjaman dibatalkan.")
        return

    id_pinjam = buat_id("peminjaman", "id_pinjam", "P")

    transaksi = {
        "id_pinjam": id_pinjam,
        "id_anggota": user["id_anggota"],
        "id_buku": id_buku,
        "judul": buku_dipilih["judul"],
        "tanggal_pinjam": tanggal_pinjam.isoformat(),
        "jatuh_tempo": jatuh_tempo.isoformat(),
        "tanggal_kembali": "",
        "status": "Dipinjam",
        "denda": "0",
        "status_denda": "Tidak Ada"
    }

    # Menyimpan transaksi ke CSV
    tambah_csv("peminjaman", transaksi)

    # Mengurangi stok buku
    buku_dipilih["stok"] = str(
        int(buku_dipilih["stok"]) - 1
    )

    simpan_csv("buku", buku)

    catat_riwayat(
        user["username"],
        "Meminjam buku " + buku_dipilih["judul"]
    )

    print("\nPEMINJAMAN BERHASIL!")
    print("ID Peminjaman:", id_pinjam)
    print("Judul Buku:", buku_dipilih["judul"])
    print("Tanggal Pinjam:", tanggal_tampil(tanggal_pinjam.isoformat()))
    print("Batas Pengembalian:", tanggal_tampil(jatuh_tempo.isoformat()))
    print("Status: Dipinjam")


# ==================================================
# 8. STATUS DAN RIWAYAT PEMINJAMAN
# ==================================================

def status_peminjaman(user):
    judul("STATUS PEMINJAMAN")

    data_user = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
    ]

    if not data_user:
        print("Belum ada transaksi peminjaman.")
        return

    for p in data_user:
        print("\nID Peminjaman :", p["id_pinjam"])
        print("Judul Buku    :", p["judul"])
        print("Tanggal Pinjam:", tanggal_tampil(p["tanggal_pinjam"]))
        print("Jatuh Tempo   :", tanggal_tampil(p["jatuh_tempo"]))
        print("Tanggal Kembali:", tanggal_tampil(p["tanggal_kembali"]))
        print("Status        :", p["status"])
        print("Denda         : Rp", p["denda"])
        print("Status Denda  :", p["status_denda"])

        if p["status"] == "Dipinjam":
            jatuh_tempo = datetime.strptime(
                p["jatuh_tempo"], "%Y-%m-%d"
            ).date()

            sisa = (jatuh_tempo - hari_ini()).days

            if sisa > 0:
                print("Sisa waktu:", sisa, "hari")
            elif sisa == 0:
                print("Keterangan: Hari terakhir pengembalian")
            else:
                print("Keterangan: Terlambat", abs(sisa), "hari")


def riwayat_peminjam(user):
    judul("RIWAYAT PEMINJAMAN")

    data_user = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
    ]

    if not data_user:
        print("Belum ada riwayat peminjaman.")
        return

    for p in data_user:
        print("\nID:", p["id_pinjam"])
        print("Buku:", p["judul"])
        print("Tanggal Pinjam:", tanggal_tampil(p["tanggal_pinjam"]))
        print("Jatuh Tempo:", tanggal_tampil(p["jatuh_tempo"]))
        print("Tanggal Kembali:", tanggal_tampil(p["tanggal_kembali"]))
        print("Status:", p["status"])
        print("Denda: Rp", p["denda"])
        print("Status Denda:", p["status_denda"])


# ==================================================
# 9. PERPANJANGAN - PEMINJAM
# ==================================================

def ajukan_perpanjangan(user):
    judul("PENGAJUAN PERPANJANGAN")

    peminjaman = baca_csv("peminjaman")
    perpanjangan = baca_csv("perpanjangan")

    aktif = [
        p for p in peminjaman
        if p["id_anggota"] == user["id_anggota"]
        and p["status"] == "Dipinjam"
    ]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    for p in aktif:
        print(
            "\nID:", p["id_pinjam"],
            "| Buku:", p["judul"],
            "| Jatuh tempo:", tanggal_tampil(p["jatuh_tempo"])
        )

    id_pinjam = input("\nMasukkan ID peminjaman: ").strip()

    dipilih = None

    for p in aktif:
        if p["id_pinjam"] == id_pinjam:
            dipilih = p
            break

    if dipilih is None:
        print("Data peminjaman tidak ditemukan!")
        return

    jatuh_tempo = datetime.strptime(
        dipilih["jatuh_tempo"], "%Y-%m-%d"
    ).date()

    if hari_ini() >= jatuh_tempo:
        print("Pengajuan harus dilakukan sebelum jatuh tempo!")
        return

    for p in perpanjangan:
        if p["id_pinjam"] == id_pinjam:
            if p["status"] == "Menunggu":
                print("Pengajuan masih menunggu petugas!")
                return

            if p["status"] == "Disetujui":
                print("Buku ini sudah pernah diperpanjang!")
                return

    id_perpanjangan = buat_id(
        "perpanjangan", "id_perpanjangan", "R"
    )

    tambah_csv("perpanjangan", {
        "id_perpanjangan": id_perpanjangan,
        "id_pinjam": id_pinjam,
        "tanggal_pengajuan": hari_ini().isoformat(),
        "status": "Menunggu"
    })

    catat_riwayat(
        user["username"],
        "Mengajukan perpanjangan " + id_pinjam
    )

    print("\nPengajuan berhasil disimpan!")
    print("ID Pengajuan:", id_perpanjangan)
    print("Status: Menunggu persetujuan petugas.")


def status_perpanjangan(user):
    judul("STATUS PERPANJANGAN")

    peminjaman = baca_csv("peminjaman")
    perpanjangan = baca_csv("perpanjangan")

    ditemukan = False

    for r in perpanjangan:
        for p in peminjaman:
            if (
                p["id_pinjam"] == r["id_pinjam"]
                and p["id_anggota"] == user["id_anggota"]
            ):
                ditemukan = True
                print("\nID Pengajuan:", r["id_perpanjangan"])
                print("Buku:", p["judul"])
                print("Tanggal Pengajuan:", tanggal_tampil(r["tanggal_pengajuan"]))
                print("Status:", r["status"])

    if not ditemukan:
        print("Belum ada pengajuan perpanjangan.")


# ==================================================
# 10. PERSETUJUAN PERPANJANGAN - PETUGAS
# ==================================================

def kelola_perpanjangan(user):
    judul("PENGELOLAAN PERPANJANGAN")

    perpanjangan = baca_csv("perpanjangan")
    peminjaman = baca_csv("peminjaman")

    menunggu = [
        r for r in perpanjangan
        if r["status"] == "Menunggu"
    ]

    if not menunggu:
        print("Tidak ada pengajuan yang menunggu.")
        return

    for r in menunggu:
        p = cari_pinjam(r["id_pinjam"])

        if p:
            anggota = cari_anggota(p["id_anggota"])
            nama = anggota["nama"] if anggota else "-"

            print("\nID Perpanjangan:", r["id_perpanjangan"])
            print("Peminjam:", nama)
            print("Buku:", p["judul"])
            print("Jatuh Tempo Lama:", tanggal_tampil(p["jatuh_tempo"]))

    id_perpanjangan = input(
        "\nMasukkan ID perpanjangan: "
    ).strip()

    for r in perpanjangan:
        if (
            r["id_perpanjangan"] == id_perpanjangan
            and r["status"] == "Menunggu"
        ):
            p = cari_pinjam(r["id_pinjam"])

            if p is None or p["status"] != "Dipinjam":
                print("Transaksi peminjaman tidak aktif!")
                return

            print("\n1. Setujui")
            print("2. Tolak")

            pilihan = input("Pilih: ")

            if pilihan == "1":
                jatuh_tempo = datetime.strptime(
                    p["jatuh_tempo"], "%Y-%m-%d"
                ).date()

                tanggal_pengajuan = datetime.strptime(
                    r["tanggal_pengajuan"], "%Y-%m-%d"
                ).date()

                if tanggal_pengajuan >= jatuh_tempo:
                    print("Pengajuan sudah melewati batas waktu!")
                    return

                jatuh_tempo_baru = jatuh_tempo + timedelta(
                    days=LAMA_PERPANJANGAN
                )

                p["jatuh_tempo"] = jatuh_tempo_baru.isoformat()
                r["status"] = "Disetujui"

                print("Perpanjangan berhasil disetujui!")
                print("Jatuh tempo baru:", tanggal_tampil(p["jatuh_tempo"]))

            elif pilihan == "2":
                r["status"] = "Ditolak"
                print("Perpanjangan ditolak.")

            else:
                print("Pilihan tidak valid!")
                return

            simpan_csv("peminjaman", peminjaman)
            simpan_csv("perpanjangan", perpanjangan)

            catat_riwayat(
                user["username"],
                "Memproses perpanjangan " + id_perpanjangan
            )

            return

    print("Pengajuan tidak ditemukan.")


# ==================================================
# 11. PENGEMBALIAN BUKU - PETUGAS
# ==================================================

def pengembalian_buku(user):
    judul("PENGEMBALIAN BUKU")

    peminjaman = baca_csv("peminjaman")

    aktif = [
        p for p in peminjaman
        if p["status"] == "Dipinjam"
    ]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    for p in aktif:
        anggota = cari_anggota(p["id_anggota"])
        nama = anggota["nama"] if anggota else "-"

        print("\nID Peminjaman:", p["id_pinjam"])
        print("Peminjam:", nama)
        print("Buku:", p["judul"])
        print("Jatuh Tempo:", tanggal_tampil(p["jatuh_tempo"]))

    id_pinjam = input("\nMasukkan ID peminjaman: ").strip()

    for p in peminjaman:
        if p["id_pinjam"] == id_pinjam and p["status"] == "Dipinjam":

            tanggal_kembali = hari_ini()

            jatuh_tempo = datetime.strptime(
                p["jatuh_tempo"], "%Y-%m-%d"
            ).date()

            keterlambatan = (tanggal_kembali - jatuh_tempo).days

            if keterlambatan > 0:
                denda = keterlambatan * DENDA_PER_HARI
                status_denda = "Belum Lunas"
            else:
                denda = 0
                status_denda = "Tidak Ada"

            p["tanggal_kembali"] = tanggal_kembali.isoformat()
            p["status"] = "Dikembalikan"
            p["denda"] = str(denda)
            p["status_denda"] = status_denda

            buku = baca_csv("buku")

            for b in buku:
                if b["id_buku"] == p["id_buku"]:
                    b["stok"] = str(int(b["stok"]) + 1)
                    break

            simpan_csv("buku", buku)
            simpan_csv("peminjaman", peminjaman)

            print("\nPengembalian berhasil dicatat!")
            print("Tanggal Kembali:", tanggal_tampil(p["tanggal_kembali"]))
            print("Terlambat:", max(0, keterlambatan), "hari")
            print("Total Denda: Rp", denda)

            catat_riwayat(
                user["username"],
                "Mencatat pengembalian " + id_pinjam
            )

            return

    print("Data peminjaman tidak ditemukan!")


# ==================================================
# 12. PENGELOLAAN DENDA - PETUGAS
# ==================================================

def kelola_denda(user):
    judul("PENGELOLAAN DENDA")

    peminjaman = baca_csv("peminjaman")

    data_denda = [
        p for p in peminjaman
        if int(p["denda"]) > 0
    ]

    if not data_denda:
        print("Belum ada data denda.")
        return

    for p in data_denda:
        anggota = cari_anggota(p["id_anggota"])
        nama = anggota["nama"] if anggota else "-"

        print("\nID Peminjaman:", p["id_pinjam"])
        print("Peminjam:", nama)
        print("Buku:", p["judul"])
        print("Denda: Rp", p["denda"])
        print("Status:", p["status_denda"])

    id_pinjam = input("\nMasukkan ID peminjaman: ").strip()

    for p in peminjaman:
        if p["id_pinjam"] == id_pinjam:

            if int(p["denda"]) <= 0:
                print("Tidak ada denda untuk transaksi ini.")
                return

            if p["status"] != "Dikembalikan":
                print("Buku harus dikembalikan terlebih dahulu!")
                return

            if p["status_denda"] == "Lunas":
                print("Denda sudah lunas!")
                return

            print("\nTotal yang harus dibayar: Rp", p["denda"])
            konfirmasi = input("Konfirmasi pembayaran? (y/n): ").lower()

            if konfirmasi == "y":
                p["status_denda"] = "Lunas"
                simpan_csv("peminjaman", peminjaman)

                catat_riwayat(
                    user["username"],
                    "Memperbarui pembayaran denda " + id_pinjam
                )

                print("Pembayaran berhasil dicatat!")

            return

    print("Transaksi tidak ditemukan.")


# ==================================================
# 13. SELURUH RIWAYAT - PETUGAS
# ==================================================

def seluruh_riwayat():
    judul("SELURUH RIWAYAT PEMINJAMAN")

    peminjaman = baca_csv("peminjaman")

    if not peminjaman:
        print("Belum ada transaksi.")
        return

    for p in peminjaman:
        anggota = cari_anggota(p["id_anggota"])
        nama = anggota["nama"] if anggota else "-"

        print("\nID Peminjaman:", p["id_pinjam"])
        print("Nama Peminjam:", nama)
        print("Judul Buku:", p["judul"])
        print("Tanggal Pinjam:", tanggal_tampil(p["tanggal_pinjam"]))
        print("Jatuh Tempo:", tanggal_tampil(p["jatuh_tempo"]))
        print("Tanggal Kembali:", tanggal_tampil(p["tanggal_kembali"]))
        print("Status:", p["status"])
        print("Denda: Rp", p["denda"])
        print("Status Denda:", p["status_denda"])


def lihat_riwayat_aktivitas():
    judul("RIWAYAT AKTIVITAS SISTEM")

    data = baca_csv("riwayat")

    if not data:
        print("Belum ada aktivitas.")
        return

    for item in data:
        print("\nTanggal:", item["tanggal"])
        print("Username:", item["username"])
        print("Aktivitas:", item["aktivitas"])


# ==================================================
# 14. MENU PEMINJAM
# ==================================================

def menu_peminjam(user):
    while True:
        judul("MENU PEMINJAM BOOK TRACK")

        print("1. Lihat katalog buku")
        print("2. Cari buku")
        print("3. Pinjam buku")
        print("4. Lihat status peminjaman")
        print("5. Ajukan perpanjangan")
        print("6. Lihat status perpanjangan")
        print("7. Riwayat peminjaman")
        print("8. Informasi denda")
        print("9. Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            tampilkan_buku()
            jeda()

        elif pilihan == "2":
            cari_buku()
            jeda()

        elif pilihan == "3":
            ajukan_peminjaman(user)
            jeda()

        elif pilihan == "4":
            status_peminjaman(user)
            jeda()

        elif pilihan == "5":
            ajukan_perpanjangan(user)
            jeda()

        elif pilihan == "6":
            status_perpanjangan(user)
            jeda()

        elif pilihan == "7":
            riwayat_peminjam(user)
            jeda()

        elif pilihan == "8":
            status_peminjaman(user)
            jeda()

        elif pilihan == "9":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 15. MENU PETUGAS
# ==================================================

def menu_petugas(user):
    while True:
        judul("MENU PETUGAS BOOK TRACK")

        print("1. Lihat katalog buku")
        print("2. Tambah buku")
        print("3. Ubah data buku")
        print("4. Hapus buku")
        print("5. Lihat data anggota")
        print("6. Tambah anggota")
        print("7. Ubah data anggota")
        print("8. Hapus anggota")
        print("9. Proses pengembalian")
        print("10. Kelola perpanjangan")
        print("11. Kelola pembayaran denda")
        print("12. Seluruh riwayat peminjaman")
        print("13. Riwayat aktivitas sistem")
        print("14. Logout")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            tampilkan_buku()
            jeda()

        elif pilihan == "2":
            tambah_buku()
            jeda()

        elif pilihan == "3":
            ubah_buku()
            jeda()

        elif pilihan == "4":
            hapus_buku()
            jeda()

        elif pilihan == "5":
            tampilkan_anggota()
            jeda()

        elif pilihan == "6":
            tambah_anggota()
            jeda()

        elif pilihan == "7":
            ubah_anggota()
            jeda()

        elif pilihan == "8":
            hapus_anggota()
            jeda()

        elif pilihan == "9":
            pengembalian_buku(user)
            jeda()

        elif pilihan == "10":
            kelola_perpanjangan(user)
            jeda()

        elif pilihan == "11":
            kelola_denda(user)
            jeda()

        elif pilihan == "12":
            seluruh_riwayat()
            jeda()

        elif pilihan == "13":
            lihat_riwayat_aktivitas()
            jeda()

        elif pilihan == "14":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 16. PROGRAM UTAMA
# ==================================================

def main():
    persiapan_data()

    while True:
        judul("BOOK TRACK")
        print("SISTEM PENGELOLAAN BUKU PERPUSTAKAAN")

        print("\n1. Login")
        print("2. Registrasi peminjam")
        print("3. Keluar")

        pilihan = input("\nPilih menu: ")

        if pilihan == "1":
            user = login()

            if user is not None:
                if user["role"] == "petugas":
                    menu_petugas(user)

                elif user["role"] == "peminjam":
                    menu_peminjam(user)

        elif pilihan == "2":
            registrasi()
            jeda()

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan Book Track!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()
            
if __name__ == "__main__":
    main()
