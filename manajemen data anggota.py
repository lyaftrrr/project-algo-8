def data_anggota():
    nim = input("Masukkan NIM: ")

    for data in anggota:
        if data["nim"] == nim:
            print("NIM sudah terdaftar!")
            return

    nama = input("Masukkan Nama: ")

    anggota.append({
        "nim": nim,
        "nama": nama
    })

    simpan_data()
    print("Anggota berhasil ditambahkan!")


# 3. PEMINJAMAN BUKU
def peminjaman():
    nim = input("Masukkan NIM: ")
    id_buku = input("Masukkan ID Buku: ")

    anggota_ada = False
    buku_ada = False

    for data in anggota:
        if data["nim"] == nim:
            anggota_ada = True

    for data in buku:
        if data["id_buku"] == id_buku:
            buku_ada = True

    if anggota_ada and buku_ada:
        for data in buku:
            if data["id_buku"] == id_buku:

                if data["stok"] > 0:
                    data["stok"] -= 1

                    id_pinjam = "P" + str(len(riwayat) + 1)

                    riwayat.append({
                        "id_pinjam": id_pinjam,
                        "nim": nim,
                        "id_buku": id_buku,
                        "status": "Dipinjam",
                        "denda": "0"
                    })

                    simpan_data()
                    print("Peminjaman berhasil!")
                    print("ID Peminjaman:", id_pinjam)

                else:
                    print("Stok buku habis!")
    else:
        print("NIM atau ID buku tidak ditemukan!")
