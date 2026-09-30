"""Modul backend autentikasi Flask dengan antarmuka web interaktif."""

import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "U6L2cJMgKERTtT1MQ4hmkj90PD338H_t"

def init_db():
    """Inisialisasi basis data dan membuat data pengguna awal."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)"
    )
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES ('admin', 'supersecret')"
    )
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Store username in session upon successful login
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            message = "Login Gagal! Kredensial tidak valid."
            status_class = "danger"

    return render_template("index.html", message=message, status_class=status_class)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Menampilkan formulir pendaftaran dan menyimpan pengguna baru ke database."""
    message = None
    status_class = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            message = "Username dan password wajib diisi!"
            status_class = "danger"
        else:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            try:
                # Parameterized query untuk menyimpan pengguna baru
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (username, password)
                )
                conn.commit()
                message = "Registrasi berhasil! Silakan kembali ke halaman utama untuk login."
                status_class = "success"
            except sqlite3.IntegrityError:
                message = "Username sudah digunakan. Silakan pilih username lain."
                status_class = "danger"
            finally:
                conn.close()

    return render_template(
        "register.html", message=message, status_class=status_class
    )

@app.route("/dashboard")
def dashboard():
    """Menampilkan halaman utama/dashboard area terproteksi sederhana."""
    return render_template("dashboard.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)  # nosemgrep
