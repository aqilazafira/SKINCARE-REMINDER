from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Product, Recommendation

rekomendasi_bp = Blueprint("rekomendasi", __name__)


@rekomendasi_bp.route("/rekomendasi")
@login_required
def rekomendasi():
    return render_template("rekomendasi.html")


# Halaman kulit berminyak
@rekomendasi_bp.route("/kulit_berminyak")
def kulit_berminyak():
    recommendation = Recommendation.query.filter_by(title="Berminyak").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title)


# Halaman kulit kering
@rekomendasi_bp.route("/kulit_kering")
def kulit_kering():
    recommendation = Recommendation.query.filter_by(title="Kering").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title)


# Halaman kulit kombinasi
@rekomendasi_bp.route("/kulit_kombinasi")
def kulit_kombinasi():
    recommendation = Recommendation.query.filter_by(title="Kombinasi").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title)


# Halaman kulit normal
@rekomendasi_bp.route("/kulit_normal")
def kulit_normal():
    recommendation = Recommendation.query.filter_by(title="Normal").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title)


# Halaman kulit berjerawat
@rekomendasi_bp.route("/kulit_berjerawat")
def kulit_berjerawat():
    recommendation = Recommendation.query.filter_by(title="Berjerawat").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title)
