import csv
import os
from datetime import datetime, timedelta

# ==================================================
# BOOK TRACK
# Hanya berisi fitur milik pengunjung (peminjam buku).
# Akun admin TIDAK bisa masuk lewat program ini.
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.join(BASE_DIR, "data_booktrackbaru")

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

# Akun contoh pengunjung (hanya dibuat saat akun.csv masih kosong)
# username, password, role, nama anggota, kelas
AKUN_AWAL = [
    ("pengunjung", "pinjam123", "pengunjung",
     "Pengunjung Contoh", "Sistem Informasi"),
    ("pengunjung2", "pinjam456", "pengunjung",
     "Siti Aminah", "Sistem Informasi"),
    ("pengunjung3", "pinjam789", "pengunjung",
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

    if role == "pengunjung":
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



def migrasi_role():
    """Menyesuaikan data lama: peminjam -> pengunjung."""
    akun = baca_csv("akun")
    berubah = False

    for a in akun:
        if a["role"] == "peminjam":
            a["role"] = "pengunjung"
            berubah = True

    if berubah:
        simpan_csv("akun", akun)


def persiapan_data():
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    for jenis in FILES:
        if not os.path.exists(FILES[jenis]):
            simpan_csv(jenis, [])

    migrasi_role()

    # Data buku awal
    if len(baca_csv("buku")) == 0:
        data_buku = [
            {"id_buku": "B001", "judul": "Laskar Pelangi",
             "penulis": "Andrea Hirata", "kategori": "Novel", "stok": "5"},
            {"id_buku": "B002", "judul": "Bumi",
             "penulis": "Tere Liye", "kategori": "Fiksi", "stok": "4"},
            {"id_buku": "B003", "judul": "Atomic Habits",
             "penulis": "James Clear", "kategori": "Pengembangan Diri",
             "stok": "3"},
            {"id_buku": "B004", "judul": "Algoritma dan Pemrograman",
             "penulis": "Rinaldi Munir", "kategori": "Pendidikan",
             "stok": "6"},
            {"id_buku": "B005", "judul": "Filosofi Teras",
             "penulis": "Henry Manampiring", "kategori": "Filsafat",
             "stok": "4"},
        ]

        simpan_csv("buku", data_buku)

    # Akun contoh pengunjung (hanya jika belum ada akun sama sekali)
    if len(baca_csv("akun")) == 0:
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


def label(teks):
    """Label dengan titik dua sejajar, untuk prompt input."""
    return f"{teks:<{LEBAR_LABEL}} : "


def tanya(teks):
    return input(label(teks)).strip()


def tanya_id(teks):
    """Input ID tidak peka huruf besar/kecil (b001 sama dengan B001)."""
    return tanya(teks).lower()


def sama_id(id_data, id_input):
    """Bandingkan ID di data dengan ID yang diketik (sudah huruf kecil)."""
    return str(id_data).lower() == id_input


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


def keterangan_waktu(jatuh_tempo_iso):
    jatuh_tempo = datetime.strptime(jatuh_tempo_iso, "%Y-%m-%d").date()
    sisa = (jatuh_tempo - hari_ini()).days

    if sisa > 0:
        return f"Sisa {sisa} hari"

    if sisa == 0:
        return "Hari terakhir"

    return f"Terlambat {abs(sisa)} hari"


def teks_denda(p):
    """Ringkas: '-' jika tidak ada denda, atau 'Rp 5.000 (Belum)'."""
    if int(p["denda"]) == 0:
        return "-"

    status = "Lunas" if p["status_denda"] == "Lunas" else "Belum"
    return f"{rupiah(p['denda'])} ({status})"


# ==================================================
# 3. LOGIN DAN REGISTRASI
# ==================================================

def login():
    """Login khusus pengunjung. Akun admin ditolak di program ini."""
    judul("LOGIN PENGUNJUNG")

    username = tanya("Username")
    password = tanya("Password")

    for akun in baca_csv("akun"):
        if akun["username"] == username and akun["password"] == password:

            if akun["role"] != "pengunjung":
                print("\nAkun ini bukan akun pengunjung!")
                return None

            print("\nLogin berhasil!")
            print("Selamat datang,", username)

            catat_riwayat(username, "Login ke sistem")
            return akun

    print("\nUsername atau password salah!")
    return None


def registrasi():
    """Daftar akun baru (disimpan ke akun.csv). Role otomatis pengunjung.
    Jika berhasil, langsung mengembalikan akun agar langsung masuk."""
    judul("REGISTRASI PENGUNJUNG")

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
        "role": "pengunjung",
        "id_anggota": id_anggota
    }

    tambah_csv("akun", akun_baru)
    catat_riwayat(username, "Registrasi akun baru")

    print("\nRegistrasi berhasil! Kamu langsung masuk ke akun.")
    cetak_detail([
        ("Username", username),
        ("ID Anggota", id_anggota),
        ("Role", "Pengunjung")
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
# 5. PEMINJAMAN LANGSUNG
# ==================================================

def ajukan_peminjaman(user):
    judul("PEMINJAMAN BUKU")

    tampilkan_buku()

    print()
    id_input = tanya_id("ID buku")
    buku = baca_csv("buku")

    buku_dipilih = None

    for data in buku:
        if sama_id(data["id_buku"], id_input):
            buku_dipilih = data
            break

    if buku_dipilih is None:
        print("Buku tidak ditemukan!")
        return

    id_buku = buku_dipilih["id_buku"]

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

    print("Tekan ENTER saja untuk memakai tanggal hari ini.")
    tanggal_input = tanya("Tgl (ENTER=hari ini)")

    if tanggal_input == "":
        tanggal_pinjam = hari_ini()

    else:
        try:
            tanggal_pinjam = datetime.strptime(
                tanggal_input, "%d-%m-%Y"
            ).date()

            if tanggal_pinjam != hari_ini():
                print("Tanggal peminjaman harus sesuai tanggal hari ini!")
                return

        except ValueError:
            print("Format tanggal tidak valid! Gunakan DD-MM-YYYY.")
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
# 6. STATUS, RIWAYAT, DAN DENDA
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
# 7. PERPANJANGAN
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
    id_input = tanya_id("ID peminjaman")

    dipilih = next(
        (p for p in aktif if sama_id(p["id_pinjam"], id_input)), None
    )

    if dipilih is None:
        print("Data peminjaman tidak ditemukan!")
        return

    id_pinjam = dipilih["id_pinjam"]

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


# ==================================================
# 8. MENU PENGUNJUNG
# ==================================================

def menu_pengunjung(user):
    while True:
        judul("MENU PENGUNJUNG BOOK TRACK")

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
# 9. PROGRAM UTAMA
# ==================================================

def main():
    persiapan_data()

    while True:
        judul("BOOK TRACK")
        print("VERSI PENGUNJUNG".center(LEBAR_GARIS))

        print("\n1. Login")
        print("2. Registrasi pengunjung")
        print("3. Keluar")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            akun = login()

            if akun is not None:
                menu_pengunjung(akun)

        elif pilihan == "2":
            akun = registrasi()

            if akun is not None:
                menu_pengunjung(akun)
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
