import csv
import os
from datetime import datetime, timedelta

# BOOK TRACK - SISTEM PENGELOLAAN BUKU PERPUSTAKAAN
# Pengunjung : Login / Registrasi di beranda
# Admin      : beranda pilihan 4, dengan kata kunci khusus

KATA_KUNCI_ADMIN = "admin321"   # ganti sesuai keinginan, hanya diketahui admin
DENDA_PER_HARI = 5000
LAMA_PINJAM = 7
LAMA_PERPANJANGAN = 7
STOK_MENIPIS = 2

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_booktrack")

KOLOM = {
    "buku": ["id_buku", "judul", "penulis", "kategori", "stok"],
    "anggota": ["id_anggota", "nama", "kelas"],
    "akun": ["username", "password", "role", "id_anggota"],
    "peminjaman": [
        "id_pinjam", "id_anggota", "id_buku", "judul", "tanggal_pinjam",
        "jatuh_tempo", "tanggal_kembali", "status", "denda", "status_denda"
    ],
    "perpanjangan": ["id_perpanjangan", "id_pinjam", "tanggal_pengajuan", "status"],
    "riwayat": ["tanggal", "username", "aktivitas"]
}

FILES = {nama: os.path.join(FOLDER, nama + ".csv") for nama in KOLOM}


#1. PENYIMPANAN DATA (CSV)

def baca(jenis):
    with open(FILES[jenis], "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def simpan(jenis, data):
    with open(FILES[jenis], "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=KOLOM[jenis])
        writer.writeheader()
        writer.writerows(data)


def tambah(jenis, data):
    with open(FILES[jenis], "a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=KOLOM[jenis]).writerow(data)


def persiapan():
    os.makedirs(FOLDER, exist_ok=True)

    for nama in KOLOM:
        if not os.path.exists(FILES[nama]):
            simpan(nama, [])

    # Buku contoh
    if not baca("buku"):
        buku_awal = [
            ("Laskar Pelangi", "Andrea Hirata", "Novel", 5),
            ("Bumi", "Tere Liye", "Fiksi", 4),
            ("Atomic Habits", "James Clear", "Pengembangan Diri", 3),
            ("Algoritma dan Pemrograman", "Rinaldi Munir", "Pendidikan", 6),
            ("Filosofi Teras", "Henry Manampiring", "Filsafat", 4),
        ]

        simpan("buku", [
            {"id_buku": f"B{i:03d}", "judul": j, "penulis": p,
             "kategori": k, "stok": str(s)}
            for i, (j, p, k, s) in enumerate(buku_awal, 1)
        ])

    # Akun pengunjung contoh
    if not baca("akun"):
        contoh = [
            ("pengunjung", "pinjam123", "Pengunjung Contoh", "Sistem Informasi"),
            ("pengunjung2", "pinjam456", "Siti Aminah", "Sistem Informasi"),
            ("pengunjung3", "pinjam789", "Rizky Pratama", "Teknik Informatika"),
        ]

        for i, (username, password, nama, kelas) in enumerate(contoh, 1):
            id_anggota = f"A{i:03d}"
            tambah("anggota", {"id_anggota": id_anggota, "nama": nama, "kelas": kelas})
            tambah("akun", {"username": username, "password": password,
                            "role": "pengunjung", "id_anggota": id_anggota})


#2. FUNGSI UMUM

def judul(teks):
    print("\n" + "=" * 65)
    print(teks.center(65))
    print("=" * 65)


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


def hari_ini():
    return datetime.now().date()


def ke_tanggal(teks):
    return datetime.strptime(teks, "%Y-%m-%d").date()


def tgl(teks):
    """Tampilan tanggal DD-MM-YYYY ('-' jika kosong)."""
    return ke_tanggal(teks).strftime("%d-%m-%Y") if teks else "-"


def rupiah(angka):
    return "Rp " + f"{int(angka):,}".replace(",", ".")


def tanya(teks):
    """Input dengan titik dua yang rapi."""
    if teks.startswith("\n"):
        print()
        teks = teks[1:]

    return input(f"{teks:<20} : ").strip()


def tampil(pasangan):
    """Cetak (label, nilai) dengan titik dua sejajar."""
    for nama, nilai in pasangan:
        print(f"{nama:<20} : {nilai}")


def input_angka(teks):
    while True:
        isi = tanya(teks)

        if isi.isdigit():
            return int(isi)

        print("Masukkan angka yang benar!")


def tabel(kolom, baris):
    """Cetak tabel dengan nomor urut."""
    kolom = ["No"] + kolom
    baris = [[i + 1] + b for i, b in enumerate(baris)]
    lebar = [max(len(str(x)) for x in k) for k in zip(*([kolom] + baris))]
    pemisah = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def cetak(isi):
        print("| " + " | ".join(str(x).ljust(w) for x, w in zip(isi, lebar)) + " |")

    print(pemisah)
    cetak(kolom)
    print(pemisah)

    for b in baris:
        cetak(b)

    print(pemisah)


def buat_id(jenis, kolom, awalan):
    nomor = [
        int(d[kolom][len(awalan):]) for d in baca(jenis)
        if d[kolom][len(awalan):].isdigit()
    ]

    return awalan + str(max(nomor, default=0) + 1).zfill(3)


def cari(daftar, kolom, nilai):
    """Cari data berdasarkan ID tanpa peduli huruf besar/kecil (b001 = B001)."""
    for d in daftar:
        if d[kolom].upper() == nilai.strip().upper():
            return d

    return None


def catat(username, aktivitas):
    tambah("riwayat", {
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "username": username,
        "aktivitas": aktivitas
    })


def nama_anggota(id_anggota):
    a = cari(baca("anggota"), "id_anggota", id_anggota)
    return a["nama"] if a else "-"


def keterangan(jatuh_tempo):
    sisa = (ke_tanggal(jatuh_tempo) - hari_ini()).days

    if sisa > 0:
        return f"Sisa {sisa} hari"

    if sisa == 0:
        return "Hari terakhir"

    return f"Terlambat {-sisa} hari"


#3. KATALOG BUKU (dipakai pengunjung dan admin)

def lihat_buku():
    judul("KATALOG BUKU")
    buku = baca("buku")

    if not buku:
        print("Belum ada data buku.")
        return

    tabel(["ID", "Judul", "Penulis", "Kategori", "Stok"],
          [[b["id_buku"], b["judul"], b["penulis"], b["kategori"], b["stok"]]
           for b in buku])


def cari_buku():
    judul("CARI BUKU")
    kata = tanya("Judul / penulis").lower()

    hasil = [b for b in baca("buku")
             if kata and (kata in b["judul"].lower() or kata in b["penulis"].lower())]

    if not hasil:
        print("Buku tidak ditemukan.")
        return

    tabel(["ID", "Judul", "Penulis", "Kategori", "Stok"],
          [[b["id_buku"], b["judul"], b["penulis"], b["kategori"], b["stok"]]
           for b in hasil])


# ==================================================
# 4. LOGIN DAN REGISTRASI PENGUNJUNG
# ==================================================

def login():
    judul("LOGIN PENGUNJUNG")
    username = tanya("Username")
    password = tanya("Password")

    for akun in baca("akun"):
        if akun["username"] == username and akun["password"] == password:
            if akun["id_anggota"] == "":
                print("\nBukan akun pengunjung! Admin masuk lewat menu 4 di beranda.")
                return None

            print("\nLogin berhasil! Selamat datang,", username)
            catat(username, "Login ke sistem")
            return akun

    print("\nUsername atau password salah!")
    return None


def registrasi():
    judul("REGISTRASI PENGUNJUNG")
    username = tanya("Username")

    if username == "" or any(a["username"] == username for a in baca("akun")):
        print("Username kosong atau sudah digunakan!")
        return None

    password = tanya("Password")
    nama = tanya("Nama anggota")
    kelas = tanya("Kelas / Prodi")

    if not password or not nama or not kelas:
        print("Semua data wajib diisi!")
        return None

    id_anggota = buat_id("anggota", "id_anggota", "A")
    akun = {"username": username, "password": password,
            "role": "pengunjung", "id_anggota": id_anggota}

    tambah("anggota", {"id_anggota": id_anggota, "nama": nama, "kelas": kelas})
    tambah("akun", akun)
    catat(username, "Registrasi akun baru")

    print("\nRegistrasi berhasil! Kamu langsung masuk ke akun.")
    tampil([("ID Anggota", id_anggota), ("Role", "Pengunjung")])
    return akun


#5. FITUR PENGUNJUNG

def pinjam_buku(user):
    judul("PEMINJAMAN BUKU")
    lihat_buku()

    daftar_buku = baca("buku")
    buku = cari(daftar_buku, "id_buku", tanya("\nID buku"))

    if buku is None:
        print("Buku tidak ditemukan!")
        return

    if int(buku["stok"]) <= 0:
        print("Stok buku sedang habis!")
        return

    if any(p["id_anggota"] == user["id_anggota"] and p["id_buku"] == buku["id_buku"]
           and p["status"] == "Dipinjam" for p in baca("peminjaman")):
        print("Kamu masih meminjam buku ini!")
        return

    print("Tekan ENTER saja untuk memakai tanggal hari ini.")
    isi = tanya("Tgl (ENTER=hari ini)")

    if isi == "":
        tanggal_pinjam = hari_ini()
    else:
        try:
            tanggal_pinjam = datetime.strptime(isi, "%d-%m-%Y").date()
        except ValueError:
            print("Format tanggal salah! Gunakan DD-MM-YYYY.")
            return

        if tanggal_pinjam != hari_ini():
            print("Tanggal peminjaman harus tanggal hari ini!")
            return

    jatuh_tempo = tanggal_pinjam + timedelta(days=LAMA_PINJAM)

    print()
    tampil([("Buku", buku["judul"]),
            ("Tanggal pinjam", tanggal_pinjam.strftime("%d-%m-%Y")),
            ("Batas pengembalian", jatuh_tempo.strftime("%d-%m-%Y"))])

    if tanya("Lanjutkan? (y/n)").lower() != "y":
        print("Peminjaman dibatalkan.")
        return

    id_pinjam = buat_id("peminjaman", "id_pinjam", "P")

    tambah("peminjaman", {
        "id_pinjam": id_pinjam, "id_anggota": user["id_anggota"],
        "id_buku": buku["id_buku"], "judul": buku["judul"],
        "tanggal_pinjam": tanggal_pinjam.isoformat(),
        "jatuh_tempo": jatuh_tempo.isoformat(), "tanggal_kembali": "",
        "status": "Dipinjam", "denda": "0", "status_denda": "Tidak Ada"
    })

    buku["stok"] = str(int(buku["stok"]) - 1)
    simpan("buku", daftar_buku)
    catat(user["username"], "Meminjam buku " + buku["judul"])

    print("\nPEMINJAMAN BERHASIL!")
    tampil([("ID Peminjaman", id_pinjam), ("Status", "Dipinjam")])


def status_pinjam(user):
    judul("STATUS PEMINJAMAN")

    aktif = [p for p in baca("peminjaman")
             if p["id_anggota"] == user["id_anggota"] and p["status"] == "Dipinjam"]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    tabel(["ID", "Judul", "Tgl Pinjam", "Jatuh Tempo", "Keterangan"],
          [[p["id_pinjam"], p["judul"], tgl(p["tanggal_pinjam"]),
            tgl(p["jatuh_tempo"]), keterangan(p["jatuh_tempo"])] for p in aktif])


def riwayat_pinjam(user):
    judul("RIWAYAT PEMINJAMAN")

    milik = [p for p in baca("peminjaman") if p["id_anggota"] == user["id_anggota"]]

    if not milik:
        print("Belum ada riwayat peminjaman.")
        return

    tabel(["ID", "Judul", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali", "Status", "Denda"],
          [[p["id_pinjam"], p["judul"], tgl(p["tanggal_pinjam"]), tgl(p["jatuh_tempo"]),
            tgl(p["tanggal_kembali"]), p["status"], rupiah(p["denda"])] for p in milik])


def info_denda(user):
    judul("INFORMASI DENDA")
    baris = []
    total = 0

    for p in baca("peminjaman"):
        if p["id_anggota"] != user["id_anggota"]:
            continue

        telat = (hari_ini() - ke_tanggal(p["jatuh_tempo"])).days

        if p["status"] == "Dipinjam" and telat > 0:
            denda, status = telat * DENDA_PER_HARI, "Berjalan (estimasi)"
        elif int(p["denda"]) > 0:
            denda, status = int(p["denda"]), p["status_denda"]
        else:
            continue

        if status != "Lunas":
            total += denda

        baris.append([p["id_pinjam"], p["judul"], rupiah(denda), status])

    if not baris:
        print("Kamu tidak memiliki denda.")
        return

    tabel(["ID", "Judul", "Denda", "Status"], baris)
    print()
    tampil([("Denda per hari", rupiah(DENDA_PER_HARI)),
            ("Total belum lunas", rupiah(total))])


def ajukan_perpanjangan(user):
    """Hasil langsung diketahui: disetujui (+7 hari) atau ditolak."""
    judul("PENGAJUAN PERPANJANGAN")

    pinjaman = baca("peminjaman")
    aktif = [p for p in pinjaman
             if p["id_anggota"] == user["id_anggota"] and p["status"] == "Dipinjam"]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    tabel(["ID", "Judul", "Jatuh Tempo"],
          [[p["id_pinjam"], p["judul"], tgl(p["jatuh_tempo"])] for p in aktif])

    p = cari(aktif, "id_pinjam", tanya("\nID peminjaman"))

    if p is None:
        print("Data peminjaman tidak ditemukan!")
        return

    perpanjangan = baca("perpanjangan")

    if any(r["id_pinjam"] == p["id_pinjam"] and r["status"] == "Disetujui"
           for r in perpanjangan):
        print("Buku ini sudah pernah diperpanjang!")
        return

    jatuh_tempo = ke_tanggal(p["jatuh_tempo"])
    data = {"id_perpanjangan": buat_id("perpanjangan", "id_perpanjangan", "R"),
            "id_pinjam": p["id_pinjam"], "tanggal_pengajuan": hari_ini().isoformat()}

    if hari_ini() >= jatuh_tempo:
        data["status"] = "Ditolak"
        tambah("perpanjangan", data)
        print("\nPERPANJANGAN DITOLAK! Pengajuan harus sebelum jatuh tempo.")
        return

    baru = jatuh_tempo + timedelta(days=LAMA_PERPANJANGAN)
    p["jatuh_tempo"] = baru.isoformat()
    simpan("peminjaman", pinjaman)

    data["status"] = "Disetujui"
    tambah("perpanjangan", data)
    catat(user["username"], "Perpanjangan disetujui " + p["id_pinjam"])

    print("\nPERPANJANGAN DISETUJUI!")
    tampil([("Jatuh tempo lama", jatuh_tempo.strftime("%d-%m-%Y")),
            ("Jatuh tempo baru", baru.strftime("%d-%m-%Y"))])


def status_perpanjangan(user):
    judul("STATUS PERPANJANGAN")
    pinjaman = {p["id_pinjam"]: p for p in baca("peminjaman")}

    baris = [[r["id_perpanjangan"], pinjaman[r["id_pinjam"]]["judul"],
              tgl(r["tanggal_pengajuan"]), tgl(pinjaman[r["id_pinjam"]]["jatuh_tempo"]),
              r["status"]]
             for r in baca("perpanjangan")
             if r["id_pinjam"] in pinjaman
             and pinjaman[r["id_pinjam"]]["id_anggota"] == user["id_anggota"]]

    if not baris:
        print("Belum ada pengajuan perpanjangan.")
        return

    tabel(["ID", "Judul", "Tgl Pengajuan", "Jatuh Tempo", "Status"], baris)


def menu_pengunjung(user):
    menu = [
        ("Lihat katalog buku", lambda: lihat_buku()),
        ("Cari buku", lambda: cari_buku()),
        ("Pinjam buku", lambda: pinjam_buku(user)),
        ("Lihat status peminjaman", lambda: status_pinjam(user)),
        ("Ajukan perpanjangan", lambda: ajukan_perpanjangan(user)),
        ("Lihat status perpanjangan", lambda: status_perpanjangan(user)),
        ("Riwayat peminjaman", lambda: riwayat_pinjam(user)),
        ("Informasi denda", lambda: info_denda(user)),
    ]

    jalankan_menu("MENU PENGUNJUNG BOOK TRACK", menu, "Logout", user)


def jalankan_menu(judul_menu, menu, teks_keluar, user=None):
    """Tampilkan menu berulang sampai memilih pilihan terakhir (keluar)."""
    while True:
        judul(judul_menu)

        for i, (nama, _) in enumerate(menu, 1):
            print(f"{i}. {nama}")

        print(f"{len(menu) + 1}. {teks_keluar}")
        pilihan = input("\nPilih menu : ").strip()

        if pilihan == str(len(menu) + 1):
            if user:
                catat(user["username"], teks_keluar)

            return True

        if pilihan.isdigit() and 1 <= int(pilihan) <= len(menu):
            # Submenu mengembalikan True, jadi tidak perlu jeda lagi
            if not menu[int(pilihan) - 1][1]():
                jeda()
        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 6. ADMIN - KATA KUNCI DAN PEMANTAUAN
# ==================================================

def masuk_admin():
    """Admin hanya bisa masuk dengan kata kunci yang benar (3 kali percobaan)."""
    judul("AKSES ADMIN")

    for sisa in (2, 1, 0):
        if tanya("Kata kunci") == KATA_KUNCI_ADMIN:
            catat("admin", "Masuk ke mode admin")
            return True

        if sisa > 0:
            print(f"Kata kunci salah! Sisa percobaan: {sisa}")

    print("Kata kunci salah. Akses admin DITOLAK.")
    catat("-", "Percobaan akses admin gagal")
    return False


def pantau():
    judul("PEMANTAUAN SISTEM")
    buku = baca("buku")
    aktif = [p for p in baca("peminjaman") if p["status"] == "Dipinjam"]
    terlambat = [p for p in aktif if ke_tanggal(p["jatuh_tempo"]) < hari_ini()]

    tampil([("Jumlah judul buku", len(buku)),
            ("Total stok tersedia", sum(int(b["stok"]) for b in buku)),
            ("Sedang dipinjam", len(aktif)),
            ("Terlambat", len(terlambat)),
            ("Jumlah pengunjung", len(baca("anggota")))])

    menipis = [b for b in buku if int(b["stok"]) <= STOK_MENIPIS]
    print(f"\nSTOK MENIPIS (<= {STOK_MENIPIS})")

    if menipis:
        tabel(["ID", "Judul", "Stok"], [[b["id_buku"], b["judul"], b["stok"]] for b in menipis])
    else:
        print("Tidak ada buku dengan stok menipis.")


#7. ADMIN - KATALOG BUKU (tambah, ubah, kurangi stok, hapus)

def tambah_buku():
    judul("TAMBAH BUKU")
    nama = tanya("Judul buku")
    penulis = tanya("Penulis")
    kategori = tanya("Kategori")
    stok = input_angka("Jumlah stok")

    if not nama or not penulis or not kategori:
        print("Data tidak boleh kosong!")
        return

    id_buku = buat_id("buku", "id_buku", "B")
    tambah("buku", {"id_buku": id_buku, "judul": nama, "penulis": penulis,
                    "kategori": kategori, "stok": str(stok)})
    print("\nBuku berhasil ditambahkan! ID Buku:", id_buku)


def ubah_buku():
    daftar = baca("buku")
    buku = cari(daftar, "id_buku", tanya("\nID buku"))

    if buku is None:
        print("Buku tidak ditemukan.")
        return

    print("Kosongkan jika tidak ingin mengubah.")
    buku["judul"] = tanya("Judul baru") or buku["judul"]
    buku["penulis"] = tanya("Penulis baru") or buku["penulis"]
    buku["kategori"] = tanya("Kategori baru") or buku["kategori"]
    simpan("buku", daftar)
    print("Data buku berhasil diperbarui!")


def ubah_stok(user):
    daftar = baca("buku")
    buku = cari(daftar, "id_buku", tanya("\nID buku"))

    if buku is None:
        print("Buku tidak ditemukan.")
        return

    print()
    tampil([("Buku", buku["judul"]), ("Stok sekarang", buku["stok"])])
    print("\n1. Tambah stok\n2. Kurangi stok")
    pilihan = tanya("Pilih")

    if pilihan not in ("1", "2"):
        print("Pilihan tidak valid!")
        return

    jumlah = input_angka("Jumlah")
    lama = int(buku["stok"])
    baru = lama + jumlah if pilihan == "1" else lama - jumlah

    if baru < 0:
        print("Stok tidak boleh kurang dari 0!")
        return

    buku["stok"] = str(baru)
    simpan("buku", daftar)
    catat(user["username"], f"Stok {buku['judul']} {lama} -> {baru}")
    print(f"Stok berhasil diperbarui: {lama} -> {baru}")

def hapus_buku():
    daftar = baca("buku")
    buku = cari(daftar, "id_buku", tanya("\nID buku"))

    if buku is None:
        print("Buku tidak ditemukan.")
        return

    if any(p["id_buku"] == buku["id_buku"] and p["status"] == "Dipinjam"
           for p in baca("peminjaman")):
        print("Buku masih sedang dipinjam!")
        return

    if tanya("Hapus buku? (y/n)").lower() == "y":
        daftar.remove(buku)
        simpan("buku", daftar)
        print("Buku berhasil dihapus!")


def menu_katalog_admin(user):
    """Katalog tampil di atas, menu kelola di bawahnya."""
    while True:
        lihat_buku()
        print("\n1. Cari buku\n2. Tambah buku\n3. Ubah data buku")
        print("4. Tambah / kurangi stok\n5. Hapus buku\n6. Kembali")
        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "6":
            return True

        aksi = {"1": cari_buku, "2": tambah_buku, "3": ubah_buku,
                "4": lambda: ubah_stok(user), "5": hapus_buku}.get(pilihan)

        if aksi:
            aksi()
        else:
            print("Pilihan tidak valid!")

        jeda()


#8. ADMIN - DATA PENGUNJUNG

def lihat_pengunjung():
    judul("DATA PENGUNJUNG")
    anggota = baca("anggota")

    if not anggota:
        print("Belum ada pengunjung.")
        return

    username = {a["id_anggota"]: a["username"] for a in baca("akun")}
    pinjaman = baca("peminjaman")

    tabel(["ID", "Nama", "Kelas", "Username", "Dipinjam"],
          [[a["id_anggota"], a["nama"], a["kelas"], username.get(a["id_anggota"], "-"),
            sum(1 for p in pinjaman
                if p["id_anggota"] == a["id_anggota"] and p["status"] == "Dipinjam")]
           for a in anggota])


def tambah_pengunjung():
    judul("TAMBAH PENGUNJUNG")
    nama = tanya("Nama anggota")
    kelas = tanya("Kelas / Prodi")
    username = tanya("Username akun")
    password = tanya("Password akun")

    if not (nama and kelas and username and password):
        print("Data tidak boleh kosong!")
        return

    if any(a["username"] == username for a in baca("akun")):
        print("Username sudah digunakan!")
        return

    id_anggota = buat_id("anggota", "id_anggota", "A")
    tambah("anggota", {"id_anggota": id_anggota, "nama": nama, "kelas": kelas})
    tambah("akun", {"username": username, "password": password,
                    "role": "pengunjung", "id_anggota": id_anggota})
    print("\nPengunjung dan akun berhasil ditambahkan! ID:", id_anggota)


def ubah_pengunjung():
    lihat_pengunjung()
    daftar = baca("anggota")
    anggota = cari(daftar, "id_anggota", tanya("\nID anggota"))

    if anggota is None:
        print("Anggota tidak ditemukan.")
        return

    print("Kosongkan jika tidak ingin mengubah.")
    anggota["nama"] = tanya("Nama baru") or anggota["nama"]
    anggota["kelas"] = tanya("Kelas baru") or anggota["kelas"]
    password = tanya("Password baru")
    simpan("anggota", daftar)

    if password:
        akun = baca("akun")

        for a in akun:
            if a["id_anggota"] == anggota["id_anggota"]:
                a["password"] = password

        simpan("akun", akun)

    print("Data pengunjung berhasil diperbarui!")


def hapus_pengunjung():
    lihat_pengunjung()
    daftar = baca("anggota")
    anggota = cari(daftar, "id_anggota", tanya("\nID anggota"))

    if anggota is None:
        print("Anggota tidak ditemukan.")
        return

    if any(p["id_anggota"] == anggota["id_anggota"] and p["status"] == "Dipinjam"
           for p in baca("peminjaman")):
        print("Anggota masih memiliki pinjaman aktif!")
        return

    if tanya("Hapus? (y/n)").lower() == "y":
        daftar.remove(anggota)
        simpan("anggota", daftar)
        simpan("akun", [a for a in baca("akun") if a["id_anggota"] != anggota["id_anggota"]])
        print("Anggota dan akun berhasil dihapus!")


def menu_data_pengunjung():
    menu = [
        ("Lihat data pengunjung", lihat_pengunjung),
        ("Tambah pengunjung", tambah_pengunjung),
        ("Ubah data pengunjung", ubah_pengunjung),
        ("Hapus pengunjung", hapus_pengunjung),
    ]

    return jalankan_menu("MENU DATA PENGUNJUNG", menu, "Kembali")


#9. ADMIN - PENGEMBALIAN, PERPANJANGAN, DENDA, RIWAYAT

def pengembalian(user):
    judul("PENGEMBALIAN BUKU")
    pinjaman = baca("peminjaman")
    aktif = [p for p in pinjaman if p["status"] == "Dipinjam"]

    if not aktif:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    tabel(["ID", "Peminjam", "Judul", "Jatuh Tempo", "Keterangan"],
          [[p["id_pinjam"], nama_anggota(p["id_anggota"]), p["judul"],
            tgl(p["jatuh_tempo"]), keterangan(p["jatuh_tempo"])] for p in aktif])

    p = cari(aktif, "id_pinjam", tanya("\nID peminjaman"))

    if p is None:
        print("Data peminjaman tidak ditemukan!")
        return

    telat = max(0, (hari_ini() - ke_tanggal(p["jatuh_tempo"])).days)
    denda = telat * DENDA_PER_HARI

    p["tanggal_kembali"] = hari_ini().isoformat()
    p["status"] = "Dikembalikan"
    p["denda"] = str(denda)
    p["status_denda"] = "Belum Lunas" if denda > 0 else "Tidak Ada"
    simpan("peminjaman", pinjaman)

    # stok bertambah kembali
    buku = baca("buku")

    for b in buku:
        if b["id_buku"] == p["id_buku"]:
            b["stok"] = str(int(b["stok"]) + 1)

    simpan("buku", buku)

    # data perpanjangan buku ini otomatis dihapus
    simpan("perpanjangan", [r for r in baca("perpanjangan") if r["id_pinjam"] != p["id_pinjam"]])
    catat(user["username"], "Mencatat pengembalian " + p["id_pinjam"])

    print("\nPengembalian berhasil dicatat!")
    tampil([("Tanggal kembali", tgl(p["tanggal_kembali"])),
            ("Terlambat", f"{telat} hari"),
            ("Total denda", rupiah(denda))])


def data_perpanjangan():
    judul("DATA PERPANJANGAN")
    pinjaman = {p["id_pinjam"]: p for p in baca("peminjaman")}

    baris = [[r["id_perpanjangan"], r["id_pinjam"],
              nama_anggota(pinjaman[r["id_pinjam"]]["id_anggota"]),
              pinjaman[r["id_pinjam"]]["judul"], tgl(r["tanggal_pengajuan"]),
              tgl(pinjaman[r["id_pinjam"]]["jatuh_tempo"]), r["status"]]
             for r in baca("perpanjangan") if r["id_pinjam"] in pinjaman]

    if not baris:
        print("Belum ada data perpanjangan.")
        return

    tabel(["ID", "ID Pinjam", "Peminjam", "Judul", "Tgl Pengajuan", "Jatuh Tempo", "Status"], baris)


def kelola_denda(user):
    judul("PENGELOLAAN DENDA")
    pinjaman = baca("peminjaman")
    ada_denda = [p for p in pinjaman if int(p["denda"]) > 0]

    if not ada_denda:
        print("Belum ada data denda.")
        return

    tabel(["ID", "Peminjam", "Judul", "Denda", "Status"],
          [[p["id_pinjam"], nama_anggota(p["id_anggota"]), p["judul"],
            rupiah(p["denda"]), p["status_denda"]] for p in ada_denda])

    p = cari(ada_denda, "id_pinjam", tanya("\nID peminjaman"))

    if p is None:
        print("Transaksi denda tidak ditemukan.")
        return

    if p["status_denda"] == "Lunas":
        print("Denda sudah lunas!")
        return

    print()
    tampil([("Total dibayar", rupiah(p["denda"]))])

    if tanya("Bayar? (y/n)").lower() == "y":
        p["status_denda"] = "Lunas"
        simpan("peminjaman", pinjaman)
        catat(user["username"], "Pembayaran denda " + p["id_pinjam"])
        print("Pembayaran berhasil dicatat!")


def seluruh_riwayat():
    judul("SELURUH RIWAYAT PEMINJAMAN")
    pinjaman = baca("peminjaman")

    if not pinjaman:
        print("Belum ada transaksi.")
        return

    tabel(["ID", "Peminjam", "Judul", "Tgl Pinjam", "Jatuh Tempo", "Tgl Kembali", "Status", "Denda"],
          [[p["id_pinjam"], nama_anggota(p["id_anggota"]), p["judul"], tgl(p["tanggal_pinjam"]),
            tgl(p["jatuh_tempo"]), tgl(p["tanggal_kembali"]), p["status"], rupiah(p["denda"])]
           for p in pinjaman])


def riwayat_aktivitas():
    judul("RIWAYAT AKTIVITAS SISTEM")
    data = baca("riwayat")

    if not data:
        print("Belum ada aktivitas.")
        return

    tabel(["Tanggal", "Username", "Aktivitas"],
          [[d["tanggal"], d["username"], d["aktivitas"]] for d in data])

def menu_admin():
    user = {"username": "admin"}

    menu = [
        ("Pemantauan sistem", pantau),
        ("Katalog buku (cari/tambah/ubah/stok/hapus)", lambda: menu_katalog_admin(user)),
        ("Data pengunjung", menu_data_pengunjung),
        ("Proses pengembalian", lambda: pengembalian(user)),
        ("Data perpanjangan", data_perpanjangan),
        ("Kelola pembayaran denda", lambda: kelola_denda(user)),
        ("Seluruh riwayat peminjaman", seluruh_riwayat),
        ("Riwayat aktivitas sistem", riwayat_aktivitas),
    ]

    jalankan_menu("MENU ADMIN BOOK TRACK", menu, "Keluar dari mode admin", user)

#10. PROGRAM UTAMA

def main():
    persiapan()

    while True:
        judul("BOOK TRACK")
        print("SISTEM PENGELOLAAN BUKU PERPUSTAKAAN".center(65))
        print("\n1. Login\n2. Registrasi pengunjung\n3. Keluar\n4. Admin")
        pilihan = input("\nPilih menu : ").strip()

        if pilihan in ("1", "2"):
            akun = login() if pilihan == "1" else registrasi()

            if akun:
                menu_pengunjung(akun)
            else:
                jeda()

        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan Book Track!")
            break

        elif pilihan == "4":
            if masuk_admin():
                menu_admin()
            else:
                jeda()

        else:
            print("Pilihan tidak valid!")
            jeda()

if __name__ == "__main__":
    main()