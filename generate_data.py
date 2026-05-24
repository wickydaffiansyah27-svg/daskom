import json
import random
from db import nilai_ke_grade

FILE = "database.json"

# Daftar nama depan dan belakang untuk kombinasi 1000+ nama unik
NAMA_DEPAN = [
    "Wicky", "Jason", "Calvin", "Senku", "Albert",
    "Leclerc", "Max", "Arthur", "Intan", "Taylor",
    "Andi", "Budi", "Citra", "Dewi", "Eko",
    "Fajar", "Gita", "Hendra", "Indah", "Joko",
    "Kartika", "Lina", "Muhammad", "Nadia", "Omar",
    "Putri", "Qori", "Rudi", "Siti", "Tono",
    "Umar", "Vina", "Wawan", "Xavier", "Yuni",
    "Zaki", "Ahmad", "Bayu", "Clara", "Dimas",
    "Erwin", "Fitri", "Gunawan", "Hana", "Irfan",
    "Julia", "Kevin", "Lestari", "Mega", "Nico",
    "Olivia", "Panji", "Ratna", "Susanto", "Tari",
    "Usman", "Veronica", "Wisnu", "Xena", "Yoga",
    "Zoe", "Agus", "Bella", "Chandra", "Diana",
    "Edo", "Farah", "Gilang", "Hesti", "Imam",
    "Jessica", "Kurniawan", "Lulu", "Mario", "Novi",
    "Oscar", "Puspita", "Reza", "Sari", "Tommy",
    "Utami", "Vino", "Widya", "Yanto", "Zainal"
]

NAMA_BELAKANG = [
    "Pratama", "Saputra", "Wijaya", "Kusuma", "Putra",
    "Sari", "Ningsih", "Hidayat", "Ramadhan", "Setiawan",
    "Santoso", "Purnama", "Lestari", "Wibowo", "Nugroho",
    "Handayani", "Susanti", "Pradana", "Mahendra", "Permata",
    "Astuti", "Fauzi", "Harahap", "Simanjuntak", "Sitompul",
    "Nainggolan", "Siregar", "Hasibuan", "Damanik", "Limbong"
]

KURIKULUM = {
    1: [
        ("Pendidikan Agama Islam",     2),
        ("Pendidikan Pancasila",       2),
        ("Keterampilan Berbahasa Inggris",             3),
        ("Kalkulus",                   4),
        ("Computer Aided Design",                       3),
        ("Fisika",                                      4),
    ],
    2: [
        ("Pengukuran dan Instrumental Industri",        3),
        ("Pendidikan Kewarnegaraan",                    2),
        ("Dasar Komputer dan Pemrograman",              3),
        ("Rangkaian Listrik 1",                         3),
        ("Matematika Teknik",                           3),
        ("Pengantar Otomasi Industri dan Robotika",     4),
        ("Pendidikan Bahasa Indonesia",                 2),
    ],
    3: [
        ("Rangkaian Listrik 2",                         3),
        ("Medan Elektromagnetik",                       3),
        ("Praktikum Bengkel dan Dasar Elektro",         3),
        ("Kewirausahaan",                               2),
        ("Psikologi Pendidikan",                        2),
        ("Elektronika Dasar",                           3),
    ],
    4: [
        ("Pengelolaan Kelas",                           2),
        ("Kurikulum dan Pembelajaran",                  2),
        ("Praktikum Elektronika",                       3),
        ("Sistem Digital",                              3),
        ("Elektronika",                                 3),
        ("Sistem Kendali",                              3),
    ],
    5: [
        ("Mikrokontroler",                              3),
        ("PLC dan Otomasi",                             3),
        ("Sensor dan Aktuator",                         3),
        ("Metodologi Penelitian",                       2),
        ("Media Pembelajaran",                          2),
        ("Praktikum PLC",                               3),
    ],
    6: [
        ("IoT Industri",                                3),
        ("Robotika Lanjut",                             3), 
        ("Magang Industri",                             4),
        ("Seminar Proposal",                            2),
        ("Manajemen Proyek",                            2),
        ("Tugas Akhir Awal",                            3),
    ],
}

JUMLAH_MAHASISWA = 1000

def generate_nama_unik(index):
    """Generate nama unik dengan kombinasi nama depan dan belakang"""
    depan = NAMA_DEPAN[index % len(NAMA_DEPAN)]
    belakang = NAMA_BELAKANG[(index // len(NAMA_DEPAN)) % len(NAMA_BELAKANG)]

    # Tambahkan angka jika masih ada duplikasi
    if index >= len(NAMA_DEPAN) * len(NAMA_BELAKANG):
        return f"{depan} {belakang} {index}"
    return f"{depan} {belakang}"

def random_nilai():
    return random.randint(64, 100)

def generate():
    data = {
        "admin": {"username": "wicky", "password": "270506"},
        "mahasiswa": [],
        "riwayat": []
    }

    # Gunakan set untuk memastikan nama unik
    nama_digunakan = set()

    for i in range(1, JUMLAH_MAHASISWA + 1):
        nim = f"2024{i:05d}"

        # Generate nama unik
        while True:
            nama = generate_nama_unik(i)
            if nama not in nama_digunakan:
                nama_digunakan.add(nama)
                break
            i += 1  # Increment jika ada duplikasi

        mhs = {
            "nim": nim,
            "nama": nama,
            "semester": {}
        }

        for smt, matkul in KURIKULUM.items():
            records = []
            for mk, sks in matkul:
                nilai = random_nilai()
                grade, _ = nilai_ke_grade(nilai)
                records.append({
                    "nama": mk,
                    'sks': sks,
                    "nilai": nilai,
                    "grade": grade
                })
            mhs["semester"][str(smt)] = records

        data["mahasiswa"].append(mhs)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Data {JUMLAH_MAHASISWA} mahasiswa + nilai berhasil dibuat!")

if __name__ == "__main__":
    generate()