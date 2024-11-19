import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database 'nilai_siswa.db'
    cursor = conn.cursor()  # Membuat cursor untuk menjalankan perintah SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil data dari tabel 'nilai_siswa'
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute("SELECT * FROM nilai_siswa")  # Menjalankan query untuk mengambil semua data dari tabel
    rows = cursor.fetchall()  # Mengambil semua hasil query
    conn.close()  # Menutup koneksi ke database
    return rows  # Mengembalikan hasil query

# Fungsi untuk menyimpan data ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Mengirim data yang dimasukkan ke query
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk memperbarui data yang sudah ada di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Mengirim data yang diperbarui ke query
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghapus data dari database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat cursor
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi paling tinggi
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:  # Jika nilai fisika paling tinggi
        return "Teknik"
    elif inggris > biologi and inggris > fisika:  # Jika nilai inggris paling tinggi
        return "Bahasa"
    else:  # Jika ada nilai yang sama atau tidak ada yang tertinggi
        return "Tidak Diketahui"

# Fungsi untuk menangani tombol 'Add' (submit data)
def submit():
    try:
        nama = nama_var.get()  # Mengambil nilai nama dari input
        biologi = int(biologi_var.get())  # Mengambil nilai biologi dan mengonversinya ke integer
        fisika = int(fisika_var.get())  # Mengambil nilai fisika dan mengonversinya ke integer
        inggris = int(inggris_var.get())  # Mengambil nilai inggris dan mengonversinya ke integer

        if not nama:  # Jika nama kosong, munculkan error
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input setelah submit
        populate_table()  # Memperbarui tampilan tabel
    except ValueError as e:  # Menangani error jika input bukan angka
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk menangani tombol 'Update' (perbarui data)
def update():
    try:
        if not selected_record_id.get():  # Jika tidak ada ID yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID yang dipilih
        nama = nama_var.get()  # Mengambil nama
        biologi = int(biologi_var.get())  # Mengambil nilai biologi
        fisika = int(fisika_var.get())  # Mengambil nilai fisika
        inggris = int(inggris_var.get())  # Mengambil nilai inggris

        if not nama:  # Jika nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input setelah update
        populate_table()  # Memperbarui tampilan tabel
    except ValueError as e:  # Menangani error jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani tombol 'Delete' (hapus data)
def delete():
    try:
        if not selected_record_id.get():  # Jika tidak ada ID yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID yang dipilih
        delete_database(record_id)  # Menghapus data berdasarkan ID

        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input setelah delete
        populate_table()  # Memperbarui tampilan tabel
    except ValueError as e:  # Menangani error jika input tidak valid
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan semua input form
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama
    biologi_var.set("")  # Mengosongkan input biologi
    fisika_var.set("")  # Mengosongkan input fisika
    inggris_var.set("")  # Mengosongkan input inggris
    selected_record_id.set("")  # Mengosongkan ID yang dipilih

# Fungsi untuk menampilkan data di tabel
def populate_table():
    for row in tree.get_children():  # Menghapus semua data lama dari tabel
        tree.delete(row)
    for row in fetch_data():  # Menambahkan data baru ke tabel
        tree.insert('', 'end', values=row)  # Menampilkan setiap baris data

# Fungsi untuk mengisi input berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil item yang dipilih
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari item yang dipilih

        selected_record_id.set(selected_row[0])  # Mengisi ID ke variabel
        nama_var.set(selected_row[1])  # Mengisi nama ke variabel
        biologi_var.set(selected_row[2])  # Mengisi nilai biologi ke variabel
        fisika_var.set(selected_row[3])  # Mengisi nilai fisika ke variabel
        inggris_var.set(selected_row[4])  # Mengisi nilai inggris ke variabel
    except IndexError:  # Menangani jika tidak ada data yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()   # Memanggil fungsi untuk membuat database

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")  # Memberikan judul pada window GUI

# Variabel tkinter untuk menyimpan input pengguna
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat elemen-elemen GUI (label, entry, button, dll)
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)  # Label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)  # Entry untuk nama siswa

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)  # Label untuk nilai biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)  # Entry untuk nilai biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)  # Label untuk nilai fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)  # Entry untuk nilai fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)  # Label untuk nilai inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)  # Entry untuk nilai inggris

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)  # Tombol untuk menambahkan data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)  # Tombol untuk memperbarui data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)  # Tombol untuk menghapus data

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel dengan header

# Mengatur posisi dan tampilan isi tabel
for col in columns:
    tree.heading(col, text=col.capitalize())  # Memberikan nama header kolom
    tree.column(col, anchor='center')  # Mengatur posisi isi kolom di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menampilkan tabel di window

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Mengatur event ketika baris tabel dipilih

populate_table()  # Mengisi tabel dengan data yang ada

root.mainloop()  # Menjalankan GUI
