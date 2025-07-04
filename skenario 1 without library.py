# Fungsi validasi tahun kabisat
def is_kabisat(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False

# Fungsi validasi tanggal secara manual
def validate_date(date_str):
    # Memisahkan input menjadi hari, bulan, dan tahun
    try:
        day, month, year = map(int, date_str.split('/'))
    except ValueError:
        return False

    # Validasi panjang tahun
    if len(str(year)) != 4:
        return False

    # Daftar jumlah hari per bulan
    days_in_month = [31, 29 if is_kabisat(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Validasi bulan dan hari
    if 1 <= month <= 12 and 1 <= day <= days_in_month[month - 1]:
        return True
    return False

# Data film dan kapasitas tiket menggunakan dictionary
films = {
    "Film A": {"genre": "Action", "times": {"16:00": 100, "18:30": 100, "21:00": 100}},
    "Film B": {"genre": "Slice of Life", "times": {"17:00": 50, "20:00": 50}},
    "Film C": {"genre": "Action", "times": {"15:00": 75, "19:00": 75}},
    "Film D": {"genre": "Thriller", "times": {"16:00": 120, "20:00": 120}},
    "Film E": {"genre": "Action", "times": {"14:00": 90, "18:00": 90}},
}

# List untuk menyimpan data pemesanan
bookings = []
# List untuk menyimpan data antrian
waiting_list = []

def display_films():
    """Menampilkan daftar film dan waktu tayang dengan kapasitas yang tersedia."""
    for film, details in films.items():
        print(f"\n{film} ({details['genre']})")
        for time, capacity in details['times'].items():
            status = "Tiket habis" if capacity == 0 else f"Tiket tersedia: {capacity}"
            print(f"  Waktu: {time} - {status}")

import random

def generate_booking_code():
    """Menghasilkan kode booking."""
    return "BOOK-" + str(random.randint(100000, 999999))

def generate_payment_code():
    """Menghasilkan kode pembayaran."""
    return "PAY-" + str(random.randint(100000, 999999))

def make_booking():
    """Proses pemesanan tiket."""
    name = input("Masukkan nama Anda: ")
    display_films()

    while True:
        selected_film = input("Pilih film atau ketik 'keluar' untuk batal: ")
        if selected_film.lower() == "keluar":
            print("Pemesanan dibatalkan.")
            return
        if selected_film in films:
            break
        print("Film tidak tersedia. Silakan pilih film lain.")

    while True:
        selected_time = input(f"Pilih waktu tayang untuk {selected_film}: ")
        if selected_time in films[selected_film]['times']:
            if films[selected_film]['times'][selected_time] > 0:
                break
            else:
                print(f"Tiket habis untuk jam {selected_time}. Pilih waktu lain.")
                continue
        print("Waktu tayang tidak tersedia. Silakan pilih waktu lain.")

    while True:
        try:
            ticket_count = int(input("Masukkan jumlah tiket: "))
            available_tickets = films[selected_film]['times'][selected_time]

            if ticket_count <= available_tickets:
                # Kurangi jumlah tiket yang tersedia
                films[selected_film]['times'][selected_time] -= ticket_count
                # Simpan data pemesanan
                bookings.append({
                    "name": name,
                    "film": selected_film,
                    "time": selected_time,
                    "tickets": ticket_count
                })
                print(f"Pemesanan berhasil! Anda memesan {ticket_count} tiket untuk {selected_film} pada {selected_time}.")

                # Menambahkan fitur pembayaran
                payment_choice = input("Apakah Anda ingin membayar sekarang atau nanti? (ketik 'sekarang' atau 'nanti'): ").lower()
                while True:
                    if payment_choice == 'sekarang':
                        booking_code = generate_booking_code()
                        print(f"Pembayaran berhasil! Kode booking Anda adalah {booking_code}.")
                        bookings[-1]["booking_code"] = booking_code
                        break
                    elif payment_choice == 'nanti':
                        payment_code = generate_payment_code()
                        print(f"Anda memilih untuk membayar nanti. Kode pembayaran Anda adalah {payment_code}. Gunakan kode ini untuk membayar di kasir bioskop.")
                        bookings[-1]["payment_code"] = payment_code
                        break
                    else:
                        print("Pilihan tidak valid!")
                        payment_choice = input("Silakan pilih 'sekarang' atau 'nanti': ").lower()
                break
            else:
                print(f"Tiket tidak cukup! Tiket tersisa untuk waktu {selected_time}: {available_tickets}")
                print("Pilih opsi berikut:")
                print("1. Masukkan jumlah tiket baru yang sesuai dengan sisa tiket")
                print("2. Pilih jam tayang lain")
                print("3. Pilih film lain")
                print("4. Ketik 'keluar' untuk batal memesan")

                choice = input("Pilih opsi (1/2/3/4): ").strip()

                if choice == "1":
                    print(f"Masukkan jumlah tiket yang ingin dipesan kembali (Maksimal: {available_tickets}).")
                elif choice == "2":
                    display_films()
                    selected_time = input(f"Pilih waktu tayang baru untuk {selected_film}: ")
                    if selected_time not in films[selected_film]['times']:
                        print("Waktu tayang tidak tersedia. Silakan pilih waktu lain.")
                        continue
                elif choice == "3":
                    display_films()
                    selected_film = input("Pilih film lain: ")
                    if selected_film not in films:
                        print("Film tidak tersedia. Silakan pilih film lain.")
                        continue
                    selected_time = input(f"Pilih waktu tayang untuk {selected_film}: ")
                    if selected_time not in films[selected_film]['times']:
                        print("Waktu tayang tidak tersedia. Silakan pilih waktu lain.")
                        continue
                elif choice.lower() == "keluar":
                    print("Pemesanan dibatalkan.")
                    return
                else:
                    print("Pilihan tidak valid. Silakan pilih opsi yang benar.")
        except ValueError:
            print("Jumlah tiket tidak valid. Masukkan angka.")

def view_bookings():
    """Menampilkan daftar pemesanan yang telah dibuat."""
    if bookings:
        print("\nDaftar Pemesanan:")
        for booking in bookings:
            print(f"{booking['name']} memesan {booking['tickets']} tiket untuk {booking['film']} pada {booking['time']}")
    else:
        print("Belum ada pemesanan yang dibuat.")

def cancel_booking():
    """Pembatalan pemesanan tiket dengan syarat maksimal 30 menit sebelum penayangan."""

    # Meminta input waktu sekarang dari pengguna
    current_time_input = input("Masukkan waktu sekarang (HH:MM): ")
    try:
        current_time_hour, current_time_minute = map(int, current_time_input.split(':'))
    except ValueError:
        print("Format waktu tidak valid. Harap masukkan dalam format HH:MM.")
        return

    name = input("Masukkan nama Anda untuk membatalkan pesanan: ")
    user_bookings = [booking for booking in bookings if booking['name'] == name]

    if not user_bookings:
        print("Tidak ada pesanan yang ditemukan atas nama Anda.")
        return

    # Menampilkan daftar pesanan yang dimiliki pengguna
    print("\nDaftar pesanan Anda:")
    for i, booking in enumerate(user_bookings, start=1):
        print(f"{i}. {booking['tickets']} tiket untuk {booking['film']} pada {booking['time']}")

    # Meminta pengguna memilih pesanan yang ingin dibatalkan
    while True:
        try:
            choice = int(input(f"Pilih nomor pesanan yang ingin dibatalkan (1-{len(user_bookings)}), atau ketik 0 untuk batal: "))
            if choice == 0:
                print("Pembatalan pesanan dibatalkan.")
                return
            elif 1 <= choice <= len(user_bookings):
                booking_to_cancel = user_bookings[choice - 1]
                selected_time = booking_to_cancel['time']

                # Memecah waktu tayang ke dalam jam dan menit
                booking_hour, booking_minute = map(int, selected_time.split(':'))

                # Menghitung selisih waktu secara manual
                time_diff = (booking_hour * 60 + booking_minute) - (current_time_hour * 60 + current_time_minute)

                if time_diff < 30:
                    print("Pembatalan hanya bisa dilakukan maksimal 30 menit sebelum penayangan.")
                    return

                # Jika sudah melakukan pembayaran
                if "booking_code" in booking_to_cancel:
                    print(f"Pesanan {booking_to_cancel['tickets']} tiket untuk {booking_to_cancel['film']} pada {booking_to_cancel['time']} telah dibayar.")
                    print("Pembatalan berhasil, dana akan dikembalikan melalui metode pembayaran yang sama.")
                else:
                    print(f"Pesanan {booking_to_cancel['tickets']} tiket untuk {booking_to_cancel['film']} pada {booking_to_cancel['time']} berhasil dibatalkan.")

                # Mengembalikan tiket yang dibatalkan ke kapasitas film yang sesuai
                films[booking_to_cancel['film']]['times'][booking_to_cancel['time']] += booking_to_cancel['tickets']

                # Menghapus pemesanan dari daftar
                bookings.remove(booking_to_cancel)

                print("Tiket berhasil dibatalkan.")
                return
            else:
                print(f"Masukkan nomor yang valid antara 1 dan {len(user_bookings)}.")
        except ValueError:
            print("Masukkan nomor yang valid.")

def search_film():
    """Pencarian film berdasarkan judul atau genre."""
    search_input = input("Cari film berdasarkan judul atau kategori: ")
    found = False
    for film, details in films.items():
        if search_input.lower() in film.lower() or search_input.lower() in details['genre'].lower():
            print(f"{film} (Genre: {details['genre']})")
            found = True
            for time, capacity in details['times'].items():
                status = "Tiket habis" if capacity == 0 else f"Tiket tersedia: {capacity}"
                print(f"  Waktu: {time} - {status}")
    if not found:
        print("Film tidak ditemukan.")

def menu():
    """Menu utama untuk pemesanan tiket bioskop."""
    while True:
        print("\nMenu:")
        print("1. Pesan tiket")
        print("2. Lihat daftar pesanan")
        print("3. Batalkan pesanan")
        print("4. Lihat daftar film")
        print("5. Cari film")
        print("6. Keluar")
        choice = input("Pilih opsi (1-6): ")

        if choice == "1":
            make_booking()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            display_films()
        elif choice == "5":
            search_film()
        elif choice == "6":
            print("Terima kasih telah menggunakan sistem pemesanan tiket CineMax.")
            break
        else:
            print("Pilihan tidak valid, silakan pilih opsi lain.")

# Memulai program
menu()
