# ==================================================
# BOOK TRACK - VERSI ADMIN
# Admin mengelola SEMUA data, termasuk data pengunjung
# (anggota, akun, peminjaman, perpanjangan, denda).
# Memakai data dan fungsi dasar dari booktrack_pengunjung.py,
# jadi kedua file harus berada di folder yang sama.
# Hanya akun role admin yang bisa masuk lewat program ini.
# ==================================================

from booktrack_pengunjung import (
    DENDA_PER_HARI, LEBAR_GARIS,
    baca_csv, simpan_csv, tambah_csv, buat_akun_awal, persiapan_data,
    garis, judul, jeda, hari_ini, tanggal_tampil, rupiah, potong,
    label, tanya, tanya_id, sama_id, cetak_detail, cetak_tabel,
    buat_id, catat_riwayat, keterangan_waktu, teks_denda,
    tampilkan_buku, cari_buku
)
from datetime import datetime


# ==================================================
# 1. PERSIAPAN DATA ADMIN
# ==================================================

def migrasi_admin():
    """Menyesuaikan data lama: petugas -> admin."""
    akun = baca_csv("akun")
    berubah = False

    for a in akun:
        if a["role"] == "petugas":
            a["role"] = "admin"
            berubah = True

    if berubah:
        simpan_csv("akun", akun)


def persiapan_admin():
    persiapan_data()
    migrasi_admin()

    # Pastikan selalu ada minimal satu akun admin
    if not any(a["role"] == "admin" for a in baca_csv("akun")):
        buat_akun_awal("admin", "admin321", "admin", "", "")


# ==================================================
# 2. FUNGSI KHUSUS ADMIN
# ==================================================

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


def cari_anggota(id_anggota):
    for anggota in baca_csv("anggota"):
        if anggota["id_anggota"] == id_anggota:
            return anggota

    return None


def nama_anggota(id_anggota):
    anggota = cari_anggota(id_anggota)
    return anggota["nama"] if anggota else "-"


# ==================================================
# 3. LOGIN ADMIN
# ==================================================

def login():
    """Login khusus admin. Akun pengunjung ditolak di program ini."""
    judul("LOGIN ADMIN")

    username = tanya("Username")
    password = tanya("Password")

    for akun in baca_csv("akun"):
        if akun["username"] == username and akun["password"] == password:

            if akun["role"] != "admin":
                print("\nAkun ini bukan akun admin!")
                return None

            print("\nLogin berhasil!")
            print("Selamat datang,", username, "(admin)")

            catat_riwayat(username, "Login ke sistem (admin)")
            return akun

    print("\nUsername atau password salah!")
    return None


# ==================================================
# 4. KATALOG ADMIN (lihat + cari + tambah + ubah + hapus)
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
    print()
    id_input = tanya_id("ID buku")
    buku = baca_csv("buku")

    for data in buku:
        if sama_id(data["id_buku"], id_input):

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
                        if p["id_buku"] == data["id_buku"]
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
    print()
    id_input = tanya_id("ID buku")
    buku = baca_csv("buku")

    for data in buku:
        if sama_id(data["id_buku"], id_input):

            aktif = any(
                p["id_buku"] == data["id_buku"]
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


def menu_katalog_admin():
    """Katalog selalu tampil di atas, dengan menu cari/tambah/ubah/hapus."""
    while True:
        tampilkan_buku()

        print("\n1. Cari buku")
        print("2. Tambah buku")
        print("3. Ubah data buku")
        print("4. Hapus buku")
        print("5. Kembali")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            cari_buku()
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
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 5. DATA ANGGOTA
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
    """Menambah anggota sekaligus akunnya (tersimpan ke akun.csv)."""
    judul("TAMBAH ANGGOTA")

    nama = tanya("Nama anggota")
    kelas = tanya("Kelas / Prodi")
    username = tanya("Username akun")
    password = tanya("Password akun")

    if not nama or not kelas or not username or not password:
        print("Data tidak boleh kosong!")
        return

    if any(a["username"] == username for a in baca_csv("akun")):
        print("Username sudah digunakan!")
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
        "role": "pengunjung",
        "id_anggota": id_anggota
    })

    print("\nAnggota dan akun berhasil ditambahkan!")
    cetak_detail([
        ("ID Anggota", id_anggota),
        ("Username", username),
        ("Role", "Pengunjung")
    ])


def ubah_anggota():
    tampilkan_anggota()

    print()
    id_input = tanya_id("ID anggota")
    anggota = baca_csv("anggota")

    for data in anggota:
        if sama_id(data["id_anggota"], id_input):

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
    id_input = tanya_id("ID anggota")
    anggota = baca_csv("anggota")

    for data in anggota:
        if sama_id(data["id_anggota"], id_input):

            aktif = any(
                p["id_anggota"] == data["id_anggota"]
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
                    if a["id_anggota"] != data["id_anggota"]
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
# 6. KELOLA AKUN
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


def tambah_akun_admin(user):
    judul("TAMBAH AKUN ADMIN")

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
        "role": "admin",
        "id_anggota": ""
    })

    catat_riwayat(user["username"], "Menambah akun admin " + username)

    print("\nAkun admin berhasil dibuat!")
    cetak_detail([("Username", username), ("Role", "admin")])


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


def hapus_akun_admin(user):
    """Menghapus akun admin lain. Akun pengunjung dihapus lewat Data Anggota."""
    judul("HAPUS AKUN ADMIN")

    daftar_admin = [a for a in baca_csv("akun") if a["role"] == "admin"]

    cetak_tabel(
        ["Username", "Role"],
        [[a["username"], a["role"]] for a in daftar_admin]
    )

    print()
    username = tanya("Username")

    if not any(a["username"] == username for a in daftar_admin):
        print("Akun admin tidak ditemukan.")
        return

    if username == user["username"]:
        print("Tidak bisa menghapus akun yang sedang dipakai!")
        return

    if tanya("Hapus akun? (y/n)").lower() == "y":
        akun = [a for a in baca_csv("akun") if a["username"] != username]
        simpan_csv("akun", akun)

        catat_riwayat(user["username"], "Menghapus akun admin " + username)
        print("Akun admin berhasil dihapus!")


def menu_kelola_akun(user):
    while True:
        judul("KELOLA AKUN")

        print("1. Lihat semua akun")
        print("2. Tambah akun admin")
        print("3. Ubah password akun")
        print("4. Hapus akun admin")
        print("5. Kembali")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            lihat_akun()
            jeda()

        elif pilihan == "2":
            tambah_akun_admin(user)
            jeda()

        elif pilihan == "3":
            ubah_password_akun(user)
            jeda()

        elif pilihan == "4":
            hapus_akun_admin(user)
            jeda()

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 7. DATA PERPANJANGAN, PENGEMBALIAN, DAN DENDA
# ==================================================

def data_perpanjangan():
    """Seluruh data perpanjangan (admin) dalam bentuk tabel."""
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
    id_input = tanya_id("ID peminjaman")

    for p in peminjaman:
        if sama_id(p["id_pinjam"], id_input) and p["status"] == "Dipinjam":

            id_pinjam = p["id_pinjam"]
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
    id_input = tanya_id("ID peminjaman")

    for p in peminjaman:
        if sama_id(p["id_pinjam"], id_input):

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
                    "Memperbarui pembayaran denda " + p["id_pinjam"]
                )

                print("Pembayaran berhasil dicatat!")

            return

    print("Transaksi tidak ditemukan.")


# ==================================================
# 8. RIWAYAT
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
# 9. MENU ADMIN
# ==================================================

def menu_admin(user):
    while True:
        judul("MENU ADMIN BOOK TRACK")

        print("1. Katalog buku (lihat/cari/tambah/ubah/hapus)")
        print("2. Data anggota (lihat/tambah/ubah/hapus)")
        print("3. Proses pengembalian")
        print("4. Data perpanjangan")
        print("5. Kelola pembayaran denda")
        print("6. Seluruh riwayat peminjaman")
        print("7. Riwayat aktivitas sistem")
        print("8. Kelola akun")
        print("9. Logout")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            menu_katalog_admin()

        elif pilihan == "2":
            menu_data_anggota()

        elif pilihan == "3":
            pengembalian_buku(user)
            jeda()

        elif pilihan == "4":
            data_perpanjangan()
            jeda()

        elif pilihan == "5":
            kelola_denda(user)
            jeda()

        elif pilihan == "6":
            seluruh_riwayat()
            jeda()

        elif pilihan == "7":
            lihat_riwayat_aktivitas()
            jeda()

        elif pilihan == "8":
            menu_kelola_akun(user)

        elif pilihan == "9":
            catat_riwayat(user["username"], "Logout dari sistem")
            print("Berhasil logout!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# 10. PROGRAM UTAMA
# ==================================================

def main():
    persiapan_admin()

    while True:
        judul("BOOK TRACK")
        print("VERSI ADMIN".center(LEBAR_GARIS))

        print("\n1. Login admin")
        print("2. Keluar")

        pilihan = input("\nPilih menu : ").strip()

        if pilihan == "1":
            akun = login()

            if akun is not None:
                menu_admin(akun)

        elif pilihan == "2":
            print("\nTerima kasih telah menggunakan Book Track!")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


if __name__ == "__main__":
    main()