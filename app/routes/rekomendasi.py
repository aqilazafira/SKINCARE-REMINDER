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


# Halaman kulit berjerawat admin
@rekomendasi_bp.route("/kulitberjerawat_admin")
@login_required
def kulitberjerawat_admin():
    return render_template("admin/kulitberjerawat_admin.html")


# Halaman kulit berminyak admin
@rekomendasi_bp.route("/kulitberminyak_admin")
@login_required
def kulitberminyak_admin():
    return render_template("admin/kulitberminyak_admin.html")


# Halaman kulit kering admin
@rekomendasi_bp.route("/kulitkering_admin")
@login_required
def kulitkering_admin():
    return render_template("admin/kulitkering_admin.html")


# Halaman kulit kombinasi admin
@rekomendasi_bp.route("/kulitkombinasi_admin")
@login_required
def kulitkombinasi_admin():
    return render_template("admin/kulitkombinasi_admin.html")


# Halaman kulit normal admin
@rekomendasi_bp.route("/kulitnormal_admin")
@login_required
def kulitnormal_admin():
    return render_template("admin/kulitnormal_admin.html")
