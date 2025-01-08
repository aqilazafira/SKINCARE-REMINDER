from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def home():
    return render_template("home.html")


# Halaman feedback admin
@main_bp.route("/feedback_admin")
@login_required
def feedback_admin():
    return render_template("feedback_admin.html")


# Halaman home_admin
@main_bp.route("/home_admin")
@login_required
def home_admin():
    return render_template("admin/home_admin.html")


# Halaman timeline
@main_bp.route("/timeline")
@login_required
def timeline():
    return render_template("timeline.html")


# Halaman feedback
@main_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        # Tambahkan logika penyimpanan feedback di sini
        return redirect(url_for("main.home"))
    return render_template("feedback.html")
