import csv
import os
from datetime import datetime, timedelta

# ==================================================
# BOOK TRACK - SISTEM PENGELOLAAN BUKU PERPUSTAKAAN
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "data_booktrack")

DENDA_PER_HARI = 5000
LAMA_PINJAM = 7
LAMA_PERPANJANGAN = 7

LEBAR_GARIS = 65
LEBAR_LABEL = 20

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

# username, password, role, nama anggota, kelas
# (nama & kelas hanya dipakai untuk role peminjam)
AKUN_AWAL = [
    ("admin", "admin321", "admin", "", ""),
    ("petugas", "admin123", "petugas", "", ""),
    ("petugas2", "petugas123", "petugas", "", ""),
    ("peminjam", "pinjam123", "peminjam",
     "Peminjam Contoh", "Sistem Informasi"),
    ("peminjam2", "pinjam456", "peminjam",
     "Siti Aminah", "Sistem Informasi"),
    ("peminjam3", "pinjam789", "peminjam",
     "Rizky Pratama", "Teknik Informatika"),
]


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


def buat_akun_awal(username, password, role, nama, kelas):
    """Membuat akun contoh jika username belum ada."""
    if any(a["username"] == username for a in baca_csv("akun")):
        return

    id_anggota = ""

    if role == "peminjam":
        id_anggota = buat_id("anggota", "id_anggota", "A")

        tambah_csv("anggota", {
            "id_anggota": id_anggota,
            "nama": nama,
            "kelas": kelas
        })

    tambah_csv("akun", {
        "username": username,
        "password": password,
        "role": role,
        "id_anggota": id_anggota
    })


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

    # Akun awal: admin, petugas, dan peminjam
    for username, password, role, nama, kelas in AKUN_AWAL:
        buat_akun_awal(username, password, role, nama, kelas)


# ==================================================
# 2. FUNGSI UMUM
# ==================================================

def garis(panjang=LEBAR_GARIS):
    print("=" * panjang)


def judul(teks):
    print()
    garis()
    print(teks.center(LEBAR_GARIS))
    garis()


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


def hari_ini():
    return datetime.now().date()


def tanggal_tampil(tanggal):
    if tanggal == "":
        return "-"

    return datetime.strptime(tanggal, "%Y-%m-%d").strftime("%d-%m-%Y")


def rupiah(angka):
    return "Rp " + f"{int(angka):,}".replace(",", ".")


def potong(teks, panjang):
    teks = str(teks)

    if len(teks) <= panjang:
        return teks

    return teks[:panjang - 3] + "..."


# ---------- Tampilan rapi (titik dua sejajar & tabel) ----------

def label(teks):
    """Label dengan titik dua sejajar, untuk prompt input."""
    return f"{teks:<{LEBAR_LABEL}} : "


def tanya(teks):
    return input(label(teks)).strip()


def cetak_detail(daftar):
    """Mencetak pasangan (label, nilai) dengan titik dua sejajar."""
    for nama, nilai in daftar:
        print(label(nama) + str(nilai))


def cetak_tabel(kolom, baris):
    """Mencetak tabel otomatis dengan nomor urut dan lebar menyesuaikan."""
    kolom = ["No"] + list(kolom)
    baris = [[i + 1] + list(b) for i, b in enumerate(baris)]

    lebar = [len(str(k)) for k in kolom]

    for b in baris:
        for i, nilai in enumerate(b):
            lebar[i] = max(lebar[i], len(str(nilai)))

    pemisah = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def teks_baris(isi):
        return "| " + " | ".join(
            f"{str(v):<{lebar[i]}}" for i, v in enumerate(isi)
        ) + " |"

    print(pemisah)
    print(teks_baris(kolom))
    print(pemisah)

    for b in baris:
        print(teks_baris(b))

    print(pemisah)


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


def nama_anggota(id_anggota):
    anggota = cari_anggota(id_anggota)
    return anggota["nama"] if anggota else "-"


def keterangan_waktu(jatuh_tempo_iso):
    jatuh_tempo = datetime.strptime(jatuh_tempo_iso, "%Y-%m-%d").date()
    sisa = (jatuh_tempo - hari_ini()).days

    if sisa > 0:
        return f"Sisa {sisa} hari"

    if sisa == 0:
        return "Hari terakhir"

    return f"Terlambat {abs(sisa)} hari"


def teks_denda(p):
    """Ringkas: '-' jika tidak ada denda, atau 'Rp 3.000 (Belum)'."""
    if int(p["denda"]) == 0:
        return "-"

    status = "Lunas" if p["status_denda"] == "Lunas" else "Belum"
    return f"{rupiah(p['denda'])} ({status})"


# ==================================================
# 3. LOGIN DAN REGISTRASI
# ==================================================

def login():
    judul("LOGIN BOOK TRACK")

    username = tanya("Username")
    password = tanya("Password")

    for akun in baca_csv("akun"):
        if akun["username"] == username and akun["password"] == password:
            print("\nLogin berhasil!")
            print("Selamat datang,", username, f"({akun['role']})")

            catat_riwayat(username, "Login ke sistem")
            return akun

    print("\nUsername atau password salah!")
    return None


def registrasi():
    """Daftar akun baru. Role otomatis peminjam (anggota).
    Jika berhasil, langsung mengembalikan akun agar langsung masuk."""
    judul("REGISTRASI PEMINJAM")

    username = tanya("Username")

    if username == "":
        print("Username tidak boleh kosong!")
        return None

    for akun in baca_csv("akun"):
        if akun["username"] == username:
            print("Username sudah digunakan!")
            return None

    password = tanya("Password")
    nama = tanya("Nama anggota")
    kelas = tanya("Kelas / Prodi")

    if not password or not nama or not kelas:
        print("Semua data wajib diisi!")
        return None

    id_anggota = buat_id("anggota", "id_anggota", "A")

    tambah_csv("anggota", {
        "id_anggota": id_anggota,
        "nama": nama,
        "kelas": kelas
    })

    akun_baru = {
        "username": username,
        "password": password,
        "role": "peminjam",
        "id_anggota": id_anggota
    }

    tambah_csv("akun", akun_baru)
    catat_riwayat(username, "Registrasi akun baru")

    print("\nRegistrasi berhasil! Kamu langsung masuk ke akun.")
    cetak_detail([
        ("Username", username),
        ("ID Anggota", id_anggota),
        ("Role", "Peminjam (Anggota)")
    ])

    return akun_baru


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

    kata = tanya("Judul / penulis").lower()

    if not kata:
        print("Kata pencarian tidak boleh kosong!")
        return

    ditemukan = False

    for buku in baca_csv("buku"):
        if kata in buku["judul"].lower() or kata in buku["penulis"].lower():
            print()
            cetak_detail([
                ("ID", buku["id_buku"]),
                ("Judul", buku["judul"]),
                ("Penulis", buku["penulis"]),
                ("Kategori", buku["kategori"]),
                ("Stok", buku["stok"])
            ])
            ditemukan = True

    if not ditemukan:
        print("Buku tidak ditemukan.")


# ==================================================
# 5. KELOLA DATA BUKU - PETUGAS & ADMIN
#    (tambah, ubah, hapus dijadikan satu menu)
# ==================================================

def tambah_buku():
    judul("TAMBAH BUKU")

    nama = tanya("Judul buku")
    penulis = tanya("Penulis")
    kategori = tanya("Kategori")
    stok = input_angka(label("Jumlah stok"))

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
    cetak_detail([("ID Buku", id_buku)])


def ubah_buku():
    tampilkan_buku()

    print()
    id_buku = tanya("ID buku").upper()
    buku = baca_csv("buku")

    for data in buku:
        if data["id_buku"] == id_buku:

            print("\nKosongkan jika tidak ingin mengubah data.")

            nama = tanya("Judul baru")
            penulis = tanya("Penulis baru")
            kategori = tanya("Kategori baru")
            stok = tanya("Stok baru")

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

    print()
    id_buku = tanya("ID buku").upper()
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

            konfirmasi = tanya("Hapus buku? (y/n)").lower()

            if konfirmasi == "y":
                buku.remove(data)
                simpan_csv("buku", buku)
                print("Buku berhasil dihapus!")

            return

    print("Buku tidak ditemukan.")


def menu_kelola_buku():
    while True:
        judul("KELOLA DATA BUKU")

        print("1. Tambah buku")
        print("2. Ubah data buku")
        print("3. Hapus buku")
        print("4. Kembali")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            tambah_buku()
            jeda()

        elif pilihan == "2":
            ubah_buku()
            jeda()

        elif pilihan == "3":
            hapus_buku()
            jeda()

        elif pilihan == "4":
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 6. DATA ANGGOTA - PETUGAS & ADMIN
#    (lihat, tambah, ubah, hapus ada di satu menu)
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

    nama = tanya("Nama anggota")
    kelas = tanya("Kelas / Prodi")

    if not nama or not kelas:
        print("Data tidak boleh kosong!")
        return

    id_anggota = buat_id("anggota", "id_anggota", "A")

    tambah_csv("anggota", {
        "id_anggota": id_anggota,
        "nama": nama,
        "kelas": kelas
    })

    print("\nAnggota berhasil ditambahkan!")
    cetak_detail([("ID Anggota", id_anggota)])


def ubah_anggota():
    tampilkan_anggota()

    print()
    id_anggota = tanya("ID anggota").upper()
    anggota = baca_csv("anggota")

    for data in anggota:
        if data["id_anggota"] == id_anggota:

            print("\nKosongkan jika tidak ingin mengubah data.")

            nama = tanya("Nama baru")
            kelas = tanya("Kelas baru")

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

    print()
    id_anggota = tanya("ID anggota").upper()
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

            konfirmasi = tanya("Hapus? (y/n)").lower()

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


def menu_data_anggota():
    while True:
        judul("MENU DATA ANGGOTA")

        print("1. Lihat data anggota")
        print("2. Tambah anggota")
        print("3. Ubah data anggota")
        print("4. Hapus anggota")
        print("5. Kembali")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            tampilkan_anggota()
            jeda()

        elif pilihan == "2":
            tambah_anggota()
            jeda()

        elif pilihan == "3":
            ubah_anggota()
            jeda()

        elif pilihan == "4":
            hapus_anggota()
            jeda()

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 7. KELOLA AKUN - ADMIN
# ==================================================

def lihat_akun():
    judul("DAFTAR AKUN")

    akun = baca_csv("akun")

    if not akun:
        print("Belum ada akun.")
        return

    baris = []

    for a in akun:
        nama = nama_anggota(a["id_anggota"]) if a["id_anggota"] else "-"

        baris.append([
            a["username"],
            "*" * len(a["password"]),
            a["role"],
            a["id_anggota"] or "-",
            nama
        ])

    cetak_tabel(
        ["Username", "Password", "Role", "ID Anggota", "Nama Anggota"],
        baris
    )


def tambah_akun_petugas(user):
    judul("TAMBAH AKUN PETUGAS")

    username = tanya("Username")

    if username == "":
        print("Username tidak boleh kosong!")
        return

    if any(a["username"] == username for a in baca_csv("akun")):
        print("Username sudah digunakan!")
        return

    password = tanya("Password")

    if not password:
        print("Password tidak boleh kosong!")
        return

    tambah_csv("akun", {
        "username": username,
        "password": password,
        "role": "petugas",
        "id_anggota": ""
    })

    catat_riwayat(user["username"], "Menambah akun petugas " + username)

    print("\nAkun petugas berhasil dibuat!")
    cetak_detail([("Username", username), ("Role", "petugas")])


def ubah_password_akun(user):
    lihat_akun()

    print()
    username = tanya("Username")
    akun = baca_csv("akun")

    for a in akun:
        if a["username"] == username:
            password_baru = tanya("Password baru")

            if not password_baru:
                print("Password tidak boleh kosong!")
                return

            a["password"] = password_baru
            simpan_csv("akun", akun)

            catat_riwayat(
                user["username"],
                "Mengubah password akun " + username
            )

            print("Password berhasil diubah!")
            return

    print("Akun tidak ditemukan.")


def hapus_akun_petugas(user):
    judul("HAPUS AKUN PETUGAS")

    petugas = [a for a in baca_csv("akun") if a["role"] == "petugas"]

    if not petugas:
        print("Belum ada akun petugas.")
        return

    cetak_tabel(["Username", "Role"], [[a["username"], a["role"]] for a in petugas])

    print()
    username = tanya("Username")

    if not any(a["username"] == username for a in petugas):
        print("Akun petugas tidak ditemukan.")
        return

    if username == user["username"]:
        print("Tidak bisa menghapus akun yang sedang dipakai!")
        return

    if tanya("Hapus akun? (y/n)").lower() == "y":
        akun = [a for a in baca_csv("akun") if a["username"] != username]
        simpan_csv("akun", akun)

        catat_riwayat(user["username"], "Menghapus akun petugas " + username)
        print("Akun petugas berhasil dihapus!")


def menu_kelola_akun(user):
    while True:
        judul("KELOLA AKUN")

        print("1. Lihat semua akun")
        print("2. Tambah akun petugas")
        print("3. Ubah password akun")
        print("4. Hapus akun petugas")
        print("5. Kembali")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            lihat_akun()
            jeda()

        elif pilihan == "2":
            tambah_akun_petugas(user)
            jeda()

        elif pilihan == "3":
            ubah_password_akun(user)
            jeda()

        elif pilihan == "4":
            hapus_akun_petugas(user)
            jeda()

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 8. PEMINJAMAN LANGSUNG - PEMINJAM
# ==================================================

def ajukan_peminjaman(user):
    judul("PEMINJAMAN BUKU")

    tampilkan_buku()

    print()
    id_buku = tanya("ID buku").upper()
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

    print()
    cetak_detail([("Buku dipilih", buku_dipilih["judul"])])

    tanggal_input = tanya("Tanggal (DD-MM-YYYY)")

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

    print()
    cetak_detail([
        ("Tanggal peminjaman", tanggal_tampil(tanggal_pinjam.isoformat())),
        ("Batas pengembalian", tanggal_tampil(jatuh_tempo.isoformat()))
    ])

    konfirmasi = tanya("Lanjutkan? (y/n)").lower()

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
    cetak_detail([
        ("ID Peminjaman", id_pinjam),
        ("Judul Buku", buku_dipilih["judul"]),
        ("Tanggal Pinjam", tanggal_tampil(tanggal_pinjam.isoformat())),
        ("Batas Pengembalian", tanggal_tampil(jatuh_tempo.isoformat())),
        ("Status", "Dipinjam")
    ])


# ==================================================
# 9. STATUS, RIWAYAT, DAN DENDA - PEMINJAM
# ==================================================

def status_peminjaman(user):
    judul("STATUS PEMINJAMAN")

    aktif = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
        and p["status"] == "Dipinjam"
    ]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    baris = [
        [
            p["id_pinjam"],
            potong(p["judul"], 24),
            tanggal_tampil(p["tanggal_pinjam"]),
            tanggal_tampil(p["jatuh_tempo"]),
            keterangan_waktu(p["jatuh_tempo"])
        ]
        for p in aktif
    ]

    cetak_tabel(
        ["ID", "Judul", "Tgl Pinjam", "Jatuh Tempo", "Keterangan"],
        baris
    )


def riwayat_peminjam(user):
    judul("RIWAYAT PEMINJAMAN")

    data_user = [
        p for p in baca_csv("peminjaman")
        if p["id_anggota"] == user["id_anggota"]
    ]

    if not data_user:
        print("Belum ada riwayat peminjaman.")
        return

    baris = [
        [
            p["id_pinjam"],
            potong(p["judul"], 24),
            tanggal_tampil(p["tanggal_pinjam"]),
            tanggal_tampil(p["jatuh_tempo"]),
            tanggal_tampil(p["tanggal_kembali"]),
            p["status"],
            teks_denda(p)
        ]
        for p in data_user
    ]

    cetak_tabel(
        ["ID", "Judul", "Tgl Pinjam", "Jatuh Tempo",
         "Tgl Kembali", "Status", "Denda"],
        baris
    )


def informasi_denda(user):
    judul("INFORMASI DENDA")

    baris = []
    total_belum_lunas = 0

    for p in baca_csv("peminjaman"):
        if p["id_anggota"] != user["id_anggota"]:
            continue

        if p["status"] == "Dipinjam":
            jatuh_tempo = datetime.strptime(
                p["jatuh_tempo"], "%Y-%m-%d"
            ).date()

            telat = (hari_ini() - jatuh_tempo).days

            if telat > 0:
                estimasi = telat * DENDA_PER_HARI
                total_belum_lunas += estimasi

                baris.append([
                    p["id_pinjam"], potong(p["judul"], 24),
                    rupiah(estimasi), "Berjalan (estimasi)"
                ])

        elif int(p["denda"]) > 0:
            if p["status_denda"] != "Lunas":
                total_belum_lunas += int(p["denda"])

            baris.append([
                p["id_pinjam"], potong(p["judul"], 24),
                rupiah(p["denda"]), p["status_denda"]
            ])

    if not baris:
        print("Kamu tidak memiliki denda.")
        return

    cetak_tabel(["ID", "Judul", "Denda", "Status"], baris)

    print()
    cetak_detail([
        ("Denda per hari", rupiah(DENDA_PER_HARI)),
        ("Total belum lunas", rupiah(total_belum_lunas))
    ])


# ==================================================
# 10. PERPANJANGAN - PEMINJAM
#     Hasil langsung diketahui (disetujui / ditolak),
#     dan statusnya bisa dicek lagi di menu status.
#     Data perpanjangan otomatis dihapus saat buku dikembalikan.
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

    baris = []

    for p in aktif:
        sudah = any(
            r["id_pinjam"] == p["id_pinjam"]
            and r["status"] == "Disetujui"
            for r in perpanjangan
        )

        baris.append([
            p["id_pinjam"],
            potong(p["judul"], 24),
            tanggal_tampil(p["jatuh_tempo"]),
            "Sudah diperpanjang" if sudah else "Belum"
        ])

    cetak_tabel(["ID", "Judul", "Jatuh Tempo", "Perpanjangan"], baris)

    print()
    id_pinjam = tanya("ID peminjaman").upper()

    dipilih = next(
        (p for p in aktif if p["id_pinjam"] == id_pinjam), None
    )

    if dipilih is None:
        print("Data peminjaman tidak ditemukan!")
        return

    if any(
        r["id_pinjam"] == id_pinjam and r["status"] == "Disetujui"
        for r in perpanjangan
    ):
        print("Buku ini sudah pernah diperpanjang!")
        return

    jatuh_tempo = datetime.strptime(
        dipilih["jatuh_tempo"], "%Y-%m-%d"
    ).date()

    id_perpanjangan = buat_id(
        "perpanjangan", "id_perpanjangan", "R"
    )

    # Ditolak: pengajuan dilakukan pada/setelah jatuh tempo
    if hari_ini() >= jatuh_tempo:
        sudah_dicatat = any(
            r["id_pinjam"] == id_pinjam and r["status"] == "Ditolak"
            for r in perpanjangan
        )

        if not sudah_dicatat:
            tambah_csv("perpanjangan", {
                "id_perpanjangan": id_perpanjangan,
                "id_pinjam": id_pinjam,
                "tanggal_pengajuan": hari_ini().isoformat(),
                "status": "Ditolak"
            })

        catat_riwayat(
            user["username"],
            "Perpanjangan ditolak " + id_pinjam
        )

        print("\nPERPANJANGAN DITOLAK!")
        print("Pengajuan harus dilakukan sebelum jatuh tempo.")
        return

    # Disetujui langsung
    jatuh_tempo_baru = jatuh_tempo + timedelta(days=LAMA_PERPANJANGAN)

    dipilih["jatuh_tempo"] = jatuh_tempo_baru.isoformat()
    simpan_csv("peminjaman", peminjaman)

    tambah_csv("perpanjangan", {
        "id_perpanjangan": id_perpanjangan,
        "id_pinjam": id_pinjam,
        "tanggal_pengajuan": hari_ini().isoformat(),
        "status": "Disetujui"
    })

    catat_riwayat(
        user["username"],
        "Perpanjangan disetujui " + id_pinjam
    )

    print("\nPERPANJANGAN DISETUJUI!")
    cetak_detail([
        ("ID Pengajuan", id_perpanjangan),
        ("Buku", dipilih["judul"]),
        ("Jatuh tempo lama", tanggal_tampil(jatuh_tempo.isoformat())),
        ("Jatuh tempo baru", tanggal_tampil(jatuh_tempo_baru.isoformat())),
        ("Status", "Disetujui")
    ])


def status_perpanjangan(user):
    judul("STATUS PERPANJANGAN")

    peminjaman = {p["id_pinjam"]: p for p in baca_csv("peminjaman")}

    baris = []

    for r in baca_csv("perpanjangan"):
        p = peminjaman.get(r["id_pinjam"])

        if p and p["id_anggota"] == user["id_anggota"]:
            baris.append([
                r["id_perpanjangan"],
                potong(p["judul"], 24),
                tanggal_tampil(r["tanggal_pengajuan"]),
                tanggal_tampil(p["jatuh_tempo"]),
                r["status"]
            ])

    if not baris:
        print("Belum ada pengajuan perpanjangan.")
        return

    cetak_tabel(
        ["ID", "Judul", "Tgl Pengajuan", "Jatuh Tempo", "Status"],
        baris
    )


def data_perpanjangan():
    """Seluruh data perpanjangan (petugas & admin) dalam bentuk tabel."""
    judul("DATA PERPANJANGAN")

    perpanjangan = baca_csv("perpanjangan")

    if not perpanjangan:
        print("Belum ada data perpanjangan.")
        return

    peminjaman = {p["id_pinjam"]: p for p in baca_csv("peminjaman")}

    baris = []

    for r in perpanjangan:
        p = peminjaman.get(r["id_pinjam"])

        if p is None:
            continue

        baris.append([
            r["id_perpanjangan"],
            r["id_pinjam"],
            potong(nama_anggota(p["id_anggota"]), 16),
            potong(p["judul"], 20),
            tanggal_tampil(r["tanggal_pengajuan"]),
            tanggal_tampil(p["jatuh_tempo"]),
            r["status"]
        ])

    cetak_tabel(
        ["ID", "ID Pinjam", "Peminjam", "Judul",
         "Tgl Pengajuan", "Jatuh Tempo", "Status"],
        baris
    )


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

    baris = [
        [
            p["id_pinjam"],
            potong(nama_anggota(p["id_anggota"]), 16),
            potong(p["judul"], 24),
            tanggal_tampil(p["jatuh_tempo"]),
            keterangan_waktu(p["jatuh_tempo"])
        ]
        for p in aktif
    ]

    cetak_tabel(
        ["ID", "Peminjam", "Judul", "Jatuh Tempo", "Keterangan"],
        baris
    )

    print()
    id_pinjam = tanya("ID peminjaman").upper()

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

            # Data perpanjangan buku ini otomatis dihapus
            perpanjangan = baca_csv("perpanjangan")
            sisa = [r for r in perpanjangan if r["id_pinjam"] != id_pinjam]
            ada_perpanjangan = len(sisa) != len(perpanjangan)

            if ada_perpanjangan:
                simpan_csv("perpanjangan", sisa)

            print("\nPengembalian berhasil dicatat!")
            cetak_detail([
                ("Tanggal Kembali", tanggal_tampil(p["tanggal_kembali"])),
                ("Terlambat", f"{max(0, keterlambatan)} hari"),
                ("Total Denda", rupiah(denda))
            ])

            if ada_perpanjangan:
                print("Data perpanjangan buku ini otomatis dihapus.")

            catat_riwayat(
                user["username"],
                "Mencatat pengembalian " + id_pinjam
            )

            return

    print("Data peminjaman tidak ditemukan!")


# ==================================================
# 12. PENGELOLAAN DENDA - PETUGAS & ADMIN
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

    baris = [
        [
            p["id_pinjam"],
            potong(nama_anggota(p["id_anggota"]), 16),
            potong(p["judul"], 24),
            rupiah(p["denda"]),
            p["status_denda"]
        ]
        for p in data_denda
    ]

    cetak_tabel(["ID", "Peminjam", "Judul", "Denda", "Status"], baris)

    print()
    id_pinjam = tanya("ID peminjaman").upper()

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

            print()
            cetak_detail([("Total dibayar", rupiah(p["denda"]))])
            konfirmasi = tanya("Bayar? (y/n)").lower()

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
# 13. SELURUH RIWAYAT - PETUGAS & ADMIN (TABEL)
# ==================================================

def seluruh_riwayat():
    judul("SELURUH RIWAYAT PEMINJAMAN")

    peminjaman = baca_csv("peminjaman")

    if not peminjaman:
        print("Belum ada transaksi.")
        return

    baris = [
        [
            p["id_pinjam"],
            potong(nama_anggota(p["id_anggota"]), 12),
            potong(p["judul"], 16),
            tanggal_tampil(p["tanggal_pinjam"]),
            tanggal_tampil(p["jatuh_tempo"]),
            tanggal_tampil(p["tanggal_kembali"]),
            p["status"],
            teks_denda(p)
        ]
        for p in peminjaman
    ]

    cetak_tabel(
        ["ID", "Peminjam", "Judul", "Tgl Pinjam", "Jatuh Tempo",
         "Tgl Kembali", "Status", "Denda"],
        baris
    )


def lihat_riwayat_aktivitas():
    judul("RIWAYAT AKTIVITAS SISTEM")

    data = baca_csv("riwayat")

    if not data:
        print("Belum ada aktivitas.")
        return

    baris = [
        [item["tanggal"], item["username"], item["aktivitas"]]
        for item in data
    ]

    cetak_tabel(["Tanggal", "Username", "Aktivitas"], baris)


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

        pilihan = input("\nPilih menu : ").strip()

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
            informasi_denda(user)
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
        print("2. Kelola data buku (tambah/ubah/hapus)")
        print("3. Data anggota (lihat/tambah/ubah/hapus)")
        print("4. Proses pengembalian")
        print("5. Data perpanjangan")
        print("6. Kelola pembayaran denda")
        print("7. Seluruh riwayat peminjaman")
        print("8. Riwayat aktivitas sistem")
        print("9. Logout")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            tampilkan_buku()
            jeda()

        elif pilihan == "2":
            menu_kelola_buku()

        elif pilihan == "3":
            menu_data_anggota()

        elif pilihan == "4":
            pengembalian_buku(user)
            jeda()

        elif pilihan == "5":
            data_perpanjangan()
            jeda()

        elif pilihan == "6":
            kelola_denda(user)
            jeda()

        elif pilihan == "7":
            seluruh_riwayat()
            jeda()

        elif pilihan == "8":
            lihat_riwayat_aktivitas()
            jeda()

        elif pilihan == "9":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 16. MENU ADMIN
# ==================================================

def menu_admin(user):
    while True:
        judul("MENU ADMIN BOOK TRACK")

        print("1. Lihat katalog buku")
        print("2. Kelola data buku (tambah/ubah/hapus)")
        print("3. Data anggota (lihat/tambah/ubah/hapus)")
        print("4. Kelola akun (petugas & peminjam)")
        print("5. Seluruh riwayat peminjaman")
        print("6. Data perpanjangan")
        print("7. Kelola pembayaran denda")
        print("8. Riwayat aktivitas sistem")
        print("9. Logout")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            tampilkan_buku()
            jeda()

        elif pilihan == "2":
            menu_kelola_buku()

        elif pilihan == "3":
            menu_data_anggota()

        elif pilihan == "4":
            menu_kelola_akun(user)

        elif pilihan == "5":
            seluruh_riwayat()
            jeda()

        elif pilihan == "6":
            data_perpanjangan()
            jeda()

        elif pilihan == "7":
            kelola_denda(user)
            jeda()

        elif pilihan == "8":
            lihat_riwayat_aktivitas()
            jeda()

        elif pilihan == "9":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 17. PROGRAM UTAMA
# ==================================================

def masuk_menu(akun):
    """Langsung masuk ke menu sesuai role akun."""
    if akun["role"] == "admin":
        menu_admin(akun)

    elif akun["role"] == "petugas":
        menu_petugas(akun)

    elif akun["role"] == "peminjam":
        menu_peminjam(akun)


def main():
    persiapan_data()

    while True:
        judul("BOOK TRACK")
        print("SISTEM PENGELOLAAN BUKU PERPUSTAKAAN".center(LEBAR_GARIS))

        print("\n1. Login")
        print("2. Registrasi peminjam")
        print("3. Keluar")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            akun = login()

            if akun is not None:
                masuk_menu(akun)

        elif pilihan == "2":
            akun = registrasi()

            if akun is not None:
                masuk_menu(akun)
            else:
                jeda()

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan Book Track!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


if __name__ == "__main__":
    main()