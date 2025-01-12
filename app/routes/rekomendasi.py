from flask import Blueprint, render_template
from flask_login import login_required

rekomendasi_bp = Blueprint("rekomendasi", __name__)


@rekomendasi_bp.route("/rekomendasi")
@login_required
def rekomendasi():
    return render_template("rekomendasi.html")

# Halaman kulit berminyak
@rekomendasi_bp.route("/kulit_berminyak")
def kulit_berminyak():
    return render_template("kulit_berminyak.html")


# Halaman kulit kering
@rekomendasi_bp.route("/kulit_kering")
def kulit_kering():
    return render_template("kulit_kering.html")


# Halaman kulit kombinasi
@rekomendasi_bp.route("/kulit_kombinasi")
def kulit_kombinasi():
    return render_template("kulit_kombinasi.html")


# Halaman kulit normal
@rekomendasi_bp.route("/kulit_normal")
def kulit_normal():
    return render_template("kulit_normal.html")


# Halaman kulit berjerawat
@rekomendasi_bp.route("/kulit_berjerawat")
def kulit_berjerawat():
    return render_template("kulit_berjerawat.html")
