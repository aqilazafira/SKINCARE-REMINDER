import re
import secrets

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from app import db, mail
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



@user_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            token = secrets.token_urlsafe(16)
            try:
                user.reset_token = token
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)

            reset_url = url_for("user.reset_password", token=token, _external=True)
            msg = Message(
                subject="Password Reset Request",
                recipients=[email],
                body=f"To reset your password, click the following link: {reset_url}",
            )
            mail.send(msg)
            flash("Password reset email sent. Please check your inbox.", "success")
        else:
            flash("Email address not found.", "error")

    return render_template("forgot_password.html")


@user_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("user.reset_password", token=token))

        user = User.query.filter_by(reset_token=token).first()

        if user:
            user.set_password(password)
            user.reset_token = None
            db.session.commit()
            flash("Password reset successful. Please log in.", "success")
            return redirect(url_for("user.login"))
        else:
            flash("Invalid or expired token.", "error")

    return render_template("reset_password.html", token=token)
