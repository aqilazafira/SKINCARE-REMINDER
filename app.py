from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Halaman utama
@app.route("/")
def home():
    return render_template("home.html")

# Halaman input
@app.route("/input")
def input_page():
    return render_template("input.html")

# Halaman kulit berminyak
@app.route("/kulit_berminyak")
def kulit_berminyak():
    return render_template("kulit_berminyak.html")

# Halaman kulit kering
@app.route("/kulit_kering")
def kulit_kering():
    return render_template("kulit_kering.html")

# Halaman kulit kombinasi
@app.route("/kulit_kombinasi")
def kulit_kombinasi():
    return render_template("kulit_kombinasi.html")

# Halaman kulit normal
@app.route("/kulit_normal")
def kulit_normal():
    return render_template("kulit_normal.html")

# Halaman kulit berjerawat
@app.route("/kulit_berjerawat")
def kulit_berjerawat():
    return render_template("kulit_berjerawat.html")

# Halaman login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Tambahkan logika autentikasi di sini
        return redirect(url_for("home"))
    return render_template("login.html")

# Halaman register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Tambahkan logika registrasi di sini
        return redirect(url_for("login"))
    return render_template("register.html")

# Halaman pengingat
@app.route("/pengingat")
def reminder_page():
    return render_template("pengingat.html")

# Halaman rekomendasi
@app.route("/rekomendasi")
def rekomendasi():
    return render_template("rekomendasi.html")

# Halaman profil pengguna
@app.route("/profile")
def profile():
    return render_template("profile.html")

# Halaman timeline
@app.route("/timeline")
def timeline():
    return render_template("timeline.html")

# Halaman feedback
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        # Tambahkan logika penyimpanan feedback di sini
        return redirect(url_for("home"))
    return render_template("feedback.html")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

# Jalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
