import os
from datetime import datetime as dt

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Feedback, Timeline, User
from app.services.storage_service import allowed_file, upload_image

main_bp = Blueprint("main", __name__)

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__name__)) + "/app/static/timeline/"


@main_bp.route("/")
@login_required
def home():
    # Explicitly get a fresh user object from the database for the session
    user = db.session.get(User, current_user.id)
    return render_template("home.html", streak=user.streak)


# Halaman timeline
@main_bp.route("/timeline", methods=["GET", "POST"])
@login_required
def timeline():
    if request.method == "GET":
        timelines = Timeline.query.filter_by(user_id=current_user.id)
        user = db.session.get(User, current_user.id)
        return render_template("timeline.html", timelines=timelines, streak=user.streak)

    if "file" not in request.files:
        print("No file part")
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        print("No filename selected file")
        return redirect(request.url)

    dt_now = dt.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{current_user.id}_{dt_now}"

    if file and allowed_file(file.filename):
        image_bytes = file.read()
        if not upload_image(image_bytes=image_bytes, filename=filename, path="timeline"):
            return redirect(request.url)

    timeline = Timeline(image_url=filename + ".jpg", user_id=current_user.id)
    db.session.add(timeline)
    db.session.commit()

    # Re-fetch the user object from DB to get the updated streak from the trigger
    refreshed_user = db.session.get(User, current_user.id)

    # If streak just reached 3, flash a message
    if refreshed_user and refreshed_user.streak == 3:
        flash(f"Selamat! Anda telah mencapai streak {refreshed_user.streak} hari!", "success")

    return redirect(url_for("main.timeline"))


# Halaman feedback
@main_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "GET":
        return render_template("feedback.html")

    feedback_text = request.form.get("feedback")
    feedback = Feedback(content=feedback_text, user_id=current_user.id)
    db.session.add(feedback)
    db.session.commit()

    return redirect(url_for("main.home"))
