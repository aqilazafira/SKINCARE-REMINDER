import uuid

from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, url_for, request, flash
from flask_login import login_required
from flask_login.utils import request

from app import db
from app.helper.decorators import admin_required
from app.models import Feedback, Product, ProductRecommendation, ProductSkincareType, Recommendation, SkincareType, User, SkincareStep, SkinRecommendation
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
        # Product data fetching (existing logic)
        products_record = Product.query.all()
        products_recommendations = [
            [recommendation.recommendation.title for recommendation in product.recommendations] for product in products_record
        ]
        products_skincare_types = [
            [skincare_type.skincare_type.title for skincare_type in product.skincare_types] for product in products_record
        ]
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

        # Routine data fetching and structuring with name mapping
        all_steps = db.session.query(SkincareStep, SkinRecommendation).join(SkinRecommendation, SkincareStep.id == SkinRecommendation.step_id).order_by(SkincareStep.routine_type, SkincareStep.step_order).all()
        
        # Map database skin_type values to user-facing titles
        skin_type_map = {
            "berminyak": "Berminyak",
            "kering": "Kering",
            "kombinasi": "Kombinasi",
            "normal": "Normal",
            "sensitif": "Berjerawat",
            "berjerawat": "Berjerawat"
        }

        routines_by_title = {}
        for step, rec in all_steps:
            # Use the map to get the display title, fallback to capitalizing the skin_type
            title = skin_type_map.get(rec.skin_type, rec.skin_type.capitalize())
            
            if title not in routines_by_title:
                routines_by_title[title] = {'morning': [], 'night': []}
            
            if step.routine_type == 'Morning':
                routines_by_title[title]['morning'].append((step, rec))
            else:
                routines_by_title[title]['night'].append((step, rec))

        return render_template(
            "admin/rekomendasi_admin.html",
            recommendations=recommendations,
            skincare_types=skincare_types,
            products=products,
            routines_by_skin_type=routines_by_title
        )

    # ... (rest of the POST logic for product creation remains the same) ...
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


@admin_bp.route("/admin/routines/step/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_step():
    skin_type_map = {
        "berminyak": "Berminyak",
        "kering": "Kering",
        "kombinasi": "Kombinasi",
        "normal": "Normal",
        "sensitif": "Berjerawat",
        "berjerawat": "Berjerawat"
    }
    skin_types_from_db = [st[0] for st in db.session.query(SkinRecommendation.skin_type).distinct().all()]

    if request.method == "POST":
        name = request.form.get("name")
        routine_type = request.form.get("routine_type")
        default_time_str = request.form.get("default_time")
        step_order = request.form.get("step_order")
        detail = request.form.get("detail")
        selected_skin_types = request.form.getlist("skin_types")

        if not all([name, routine_type, default_time_str, step_order, detail]):
            flash("Mohon isi semua kolom.", "error")
            return redirect(url_for("admin.add_step"))

        if not selected_skin_types:
            flash("Mohon pilih setidaknya satu jenis kulit.", "error")
            # Re-populate form for rendering
            display_skin_types = {st: skin_type_map.get(st, st.capitalize()) for st in skin_types_from_db}
            return render_template("admin/add_step.html", skin_types=display_skin_types, form_data=request.form)

        # Check if a step with the same name, routine_type, and step_order already exists to avoid duplicates
        existing_step = SkincareStep.query.filter_by(name=name, routine_type=routine_type, step_order=int(step_order)).first()
        if existing_step:
            step_to_use = existing_step
        else:
            new_step = SkincareStep(
                name=name,
                routine_type=routine_type,
                default_time=datetime.strptime(default_time_str, "%H:%M").time(),
                step_order=int(step_order),
            )
            db.session.add(new_step)
            db.session.flush()
            step_to_use = new_step

        for skin_type in selected_skin_types:
            # Prevent adding a duplicate SkinRecommendation
            existing_rec = SkinRecommendation.query.filter_by(step_id=step_to_use.id, skin_type=skin_type).first()
            if not existing_rec:
                new_rec = SkinRecommendation(
                    skin_type=skin_type,
                    step_id=step_to_use.id,
                    detail=detail
                )
                db.session.add(new_rec)
        
        db.session.commit()
        flash(f"Langkah '{name}' berhasil ditambahkan untuk jenis kulit yang dipilih.", "success")
        return redirect(url_for("admin.rekomendasi_admin"))

    # For GET request
    display_skin_types = {st: skin_type_map.get(st, st.capitalize()) for st in skin_types_from_db}
    return render_template("admin/add_step.html", skin_types=display_skin_types)


@admin_bp.route("/admin/routines/recommendation/edit/<int:rec_id>", methods=["POST"])
@login_required
@admin_required
def edit_recommendation(rec_id):
    recommendation = SkinRecommendation.query.get_or_404(rec_id)
    new_detail = request.form.get("detail")
    
    if new_detail:
        recommendation.detail = new_detail
        db.session.commit()
        flash("Recommendation detail updated successfully!", "success")
    else:
        flash("Detail cannot be empty.", "error")

    return redirect(url_for("admin.rekomendasi_admin"))


@admin_bp.route("/admin/routines/step/delete/<int:step_id>", methods=["POST"])
@login_required
@admin_required
def delete_step(step_id):
    step = SkincareStep.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    flash(f"Step '{step.name}' has been deleted from all routines.", "success")
    return redirect(url_for("admin.rekomendasi_admin"))


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

    
@admin_bp.route("/admin/users", methods=["GET", "PUT"])
@login_required
@admin_required
def users_page():
    if request.method == "PUT":
        id = request.form.get("id")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.username = username
        user.email = email
        user.set_password(password)

        db.session.commit()
        return jsonify({"message": "User updated"})


    User_record = User.query.all()

    return render_template(
        "admin/User.html",
        users = User_record
    )


@admin_bp.route("/admin/users/<int:user_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)

    db.session.commit()
    return jsonify({"message": "User deleted!"})