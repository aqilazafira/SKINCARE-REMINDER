import uuid

from flask import Blueprint, jsonify, redirect, render_template, url_for
from flask_login import login_required
from flask_login.utils import request

from app import db
from app.helper.decorators import admin_required
from app.models import Feedback, Product, ProductRecommendation, ProductSkincareType, Recommendation, SkincareType
from app.services.storage_service import allowed_file, delete_image, upload_image

admin_bp = Blueprint("admin", __name__)


# Halaman home_admin
@admin_bp.route("/admin")
@login_required
@admin_required
def home_admin():
    return render_template("admin/home_admin.html")


# Halaman feedback admin
@admin_bp.route("/admin/feedback")
@login_required
@admin_required
def feedback_admin():
    feedbacks = Feedback.query.all()
    return render_template("admin/feedback_admin.html", feedbacks=feedbacks)

@admin_bp.route("/admin/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return jsonify({"message": "success"})


# Halaman feedback admin
@admin_bp.route("/admin/timeline")
@login_required
@admin_required
def timeline_admin():
    return render_template("admin/timeline_admin.html")


@admin_bp.route("/admin/rekomendasi", methods=["GET", "POST"])
@login_required
@admin_required
def rekomendasi_admin():
    if request.method == "GET":
        products_record = Product.query.all()

        # convert the recommendations and skincare_types to list of titles
        products_recommendations = [
            [recommendation.recommendation.title for recommendation in product.recommendations] for product in products_record
        ]
        products_skincare_types = [
            [skincare_type.skincare_type.title for skincare_type in product.skincare_types] for product in products_record
        ]

        # update the products n recommendations and skincare_types
        # to be list of titles
        products = []
        for product, recommendations, skincare_types in zip(products_record, products_recommendations, products_skincare_types):
            products.append(
                {
                    "id": product.id,
                    "brand": product.brand,
                    "description": product.description,
                    "image_url": product.image_url,
                    "recommendations": recommendations,
                    "skincare_types": skincare_types,
                }
            )

        recommendations = Recommendation.query.all()
        skincare_types = SkincareType.query.all()

        return render_template(
            "admin/rekomendasi_admin.html",
            recommendations=recommendations,
            skincare_types=skincare_types,
            products=products,
        )

    if "file" not in request.files:
        print("No file part")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        print("No filename selected file")
        return redirect(request.url)

    filename = uuid.uuid4().hex

    if file and allowed_file(file.filename):
        image_bytes = file.read()
        if not upload_image(image_bytes=image_bytes, filename=filename, path="products"):
            return redirect(request.url)

    brand = request.form.get("brand")
    description = request.form.get("description")
    recommendations = request.form.get("recommendations").split(",")
    skincare_types = request.form.get("skincareTypes").split(",")

    new_product = Product(brand=brand, image_url=filename + ".jpg", description=description)
    db.session.add(new_product)
    db.session.commit()

    for recommendation_title in recommendations:
        recommendation = Recommendation.query.filter_by(title=recommendation_title).first()
        if recommendation:
            product_recommendation = ProductRecommendation(
                product_id=new_product.id, recommendation_id=recommendation.id
            )
            db.session.add(product_recommendation)

    for skincare_type_title in skincare_types:
        skincare_type = SkincareType.query.filter_by(title=skincare_type_title).first()
        if skincare_type:
            product_skincare_type = ProductSkincareType(product_id=new_product.id, skincare_type_id=skincare_type.id)
            db.session.add(product_skincare_type)

    db.session.commit()

    return jsonify(request.form)


@admin_bp.route("/admin/rekomendasi/<int:product_id>", methods=["PUT"])
@login_required
@admin_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    brand = request.form.get("brand")
    description = request.form.get("description")
    recommendations = request.form.get("recommendations").split(",")
    skincare_types = request.form.get("skincareTypes").split(",")

    if "file" in request.files:
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = uuid.uuid4().hex
            image_bytes = file.read()
            if upload_image(image_bytes=image_bytes, filename=filename, path="products"):
                # Delete the old image file from the server
                delete_image(product.image_url, "products")
                product.image_url = filename + ".jpg"

    product.brand = brand
    product.description = description

    # Clear existing recommendations and skincare types
    ProductRecommendation.query.filter_by(product_id=product_id).delete()
    ProductSkincareType.query.filter_by(product_id=product_id).delete()

    for recommendation_title in recommendations:
        recommendation = Recommendation.query.filter_by(title=recommendation_title).first()
        if recommendation:
            product_recommendation = ProductRecommendation(
                product_id=product.id, recommendation_id=recommendation.id
            )
            db.session.add(product_recommendation)

    for skincare_type_title in skincare_types:
        skincare_type = SkincareType.query.filter_by(title=skincare_type_title).first()
        if skincare_type:
            product_skincare_type = ProductSkincareType(product_id=product.id, skincare_type_id=skincare_type.id)
            db.session.add(product_skincare_type)

    db.session.commit()

    return jsonify({"message": "Product updated successfully"})

@admin_bp.route("/admin/rekomendasi/<int:product_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        # Delete the image file from the server
        delete_image(product.image_url, "products")

        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})
    return jsonify({"message": "Product not found"}), 404

# Halaman kulit berjerawat admin
@admin_bp.route("/admin/kulitberjerawat")
@login_required
@admin_required
def kulitberjerawat_admin():
    return render_template("admin/kulitberjerawat_admin.html")


# Halaman kulit berminyak admin
@admin_bp.route("/admin/kulitberminyak")
@login_required
@admin_required
def kulitberminyak_admin():
    return render_template("admin/kulitberminyak_admin.html")


# Halaman kulit kering admin
@admin_bp.route("/admin/kulitkering")
@login_required
@admin_required
def kulitkering_admin():
    return render_template("admin/kulitkering_admin.html")


# Halaman kulit kombinasi admin
@admin_bp.route("/admin/kulitkombinasi")
@login_required
@admin_required
def kulitkombinasi_admin():
    return render_template("admin/kulitkombinasi_admin.html")


# Halaman kulit normal admin
@admin_bp.route("/admin/kulitnormal")
@login_required
@admin_required
def kulitnormal_admin():
    return render_template("admin/kulitnormal_admin.html")


# Halaman profile admin
@admin_bp.route("/admin/profile")
@login_required
@admin_required
def profile_admin():
    return render_template("admin/profile_admin.html")
