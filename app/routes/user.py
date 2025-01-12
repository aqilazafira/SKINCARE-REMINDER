import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models import User

user_bp = Blueprint("user", __name__)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password", "error")
            return redirect(url_for("user.login"))

        login_user(user, remember=True)
        flash("Login successful", "success")
        return redirect(url_for("main.home"))

    return render_template("login.html")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address", "error")
            return redirect(url_for("user.register"))

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("user.register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
            return redirect(url_for("user.register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "error")
            return redirect(url_for("user.register"))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("user.login"))
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("An error occurred. Please try again.", "error")

    return render_template("register.html")


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))


# Halaman profil pengguna
@user_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
