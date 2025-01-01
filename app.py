from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import String, Integer, DateTime
import re


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SECRET_KEY"] = "pusing"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column("user_id", Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(
        String(120), unique=True, nullable=True
    )
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.username}>"


@app.route("/")
@login_required
def home():
    return render_template("home.html")


# Halaman input
@app.route("/input")
@login_required
def input_page():
    return render_template("input.html")


# Halaman kulit berminyak
@app.route("/kulit_berminyak")
@login_required
def kulit_berminyak():
    return render_template("kulit_berminyak.html")


# Halaman kulit kering
@app.route("/kulit_kering")
@login_required
def kulit_kering():
    return render_template("kulit_kering.html")


# Halaman kulit kombinasi
@app.route("/kulit_kombinasi")
@login_required
def kulit_kombinasi():
    return render_template("kulit_kombinasi.html")


# Halaman kulit normal
@app.route("/kulit_normal")
@login_required
def kulit_normal():
    return render_template("kulit_normal.html")


# Halaman kulit berjerawat
@app.route("/kulit_berjerawat")
@login_required
def kulit_berjerawat():
    return render_template("kulit_berjerawat.html")


# Halaman login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password", "error")
            return redirect(url_for("login"))

        login_user(user)
        flash("Login successful", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return redirect(url_for("register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("An error occurred. Please try again.", "error")

    return render_template("register.html")


# Halaman pengingat
@app.route("/pengingat")
@login_required
def reminder_page():
    return render_template("pengingat.html")


# Halaman rekomendasi
@app.route("/rekomendasi")
@login_required
def rekomendasi():
    return render_template("rekomendasi.html")


# Halaman profil pengguna
@login_required
@app.route("/profile")
def profile():
    return render_template("profile.html")


# Halaman timeline
@app.route("/timeline")
@login_required
def timeline():
    return render_template("timeline.html")


# Halaman feedback
@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        # Tambahkan logika penyimpanan feedback di sini
        return redirect(url_for("home"))
    return render_template("feedback.html")


# Halaman feedback admin
@app.route("/feedback_admin")
@login_required
def feedback_admin():
    return render_template("feedback_admin.html")


# Halaman home_admin
@app.route("/home_admin")
@login_required
def home_admin():
    return render_template("admin/home_admin.html")


# Halaman kulit berjerawat admin
@app.route("/kulitberjerawat_admin")
@login_required
def kulitberjerawat_admin():
    return render_template("admin/kulitberjerawat_admin.html")


# Halaman kulit berminyak admin
@app.route("/kulitberminyak_admin")
@login_required
def kulitberminyak_admin():
    return render_template("admin/kulitberminyak_admin.html")


# Halaman kulit kering admin
@app.route("/kulitkering_admin")
@login_required
def kulitkering_admin():
    return render_template("admin/kulitkering_admin.html")


# Halaman kulit kombinasi admin
@app.route("/kulitkombinasi_admin")
@login_required
def kulitkombinasi_admin():
    return render_template("admin/kulitkombinasi_admin.html")


# Halaman kulit normal admin
@app.route("/kulitnormal_admin")
@login_required
def kulitnormal_admin():
    return render_template("admin/kulitnormal_admin.html")


# Halaman profile admin
@app.route("/profile_admin")
@login_required
def profile_admin():
    return render_template("admin/profile_admin.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Jalankan aplikasi
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
