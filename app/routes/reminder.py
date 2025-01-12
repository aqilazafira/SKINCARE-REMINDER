from datetime import datetime, timedelta
from random import randint

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from flask_mail import Message
from sqlalchemy.sql.functions import random

from app import db
from app.models import Reminder, ReminderSkincare, SkincareType, User
from app.services.reminder_service import send_email
from app.services.schedule_service import create_schedule, reschedule

reminder_bp = Blueprint("reminder", __name__)

DAYS = ["SENIN", "SELASA", "RABU", "KAMIS", "JUMAT", "SABTU", "MINGGU"]

@reminder_bp.route("/pengingat", methods=["GET"])
@login_required
def reminder_page():
    user = User.query.filter_by(id=current_user.id).first()
    user_reminders = []

    for reminder in user.reminders:
        skincare_types = []

        for skincare_type in reminder.skincare_types:
            type = SkincareType.query.filter_by(id=skincare_type.skincare_type_id).first()
            skincare_types.append(type.title)

        skincare_types = ", ".join(skincare_types)

        reminder = {
            "id": reminder.id,
            "day": DAYS[reminder.day],
            "hour": reminder.hour,
            "minute": reminder.minute,
            "skincare_types": skincare_types,
        }

        user_reminders.append(reminder)

    return render_template("pengingat.html", user_reminders=user_reminders)

@reminder_bp.route("/pengingat", methods=["PATCH"])
@login_required
def save_schedule():
    data = request.get_json()
    day = data.get("day")
    hour = int(data.get("hour"))
    minute = int(data.get("minute"))
    skincare_types = data.get("skincareTypes")

    print(data)

    # Convert day from string to integer
    day = DAYS.index(day.upper())

    reminder_action = lambda: send_email("714230044@ulbi.ac.id", "Reminder", "Don't forget to do your skincare routine!")

    reminder = Reminder.query.filter_by(user_id=current_user.id, day=day).first()
    if reminder:
        reminder.hour = hour
        reminder.minute = minute
        db.session.commit()
        ReminderSkincare.query.filter_by(reminder_id=reminder.id).delete()
        db.session.commit()
        reschedule(reminder.id, hour=hour, minute=minute)
    else:
        job_id = create_schedule(action=reminder_action, hour=hour, minute=minute)
        reminder = Reminder(id=job_id, user_id=current_user.id, day=day, hour=hour, minute=minute)
        db.session.add(reminder)
        db.session.commit()

    for skincare_type in skincare_types:
        skincare_type = skincare_type.upper()
        skincare_type_id = SkincareType.query.filter_by(title=skincare_type).first().id

        new_reminder_skincare = ReminderSkincare(reminder_id=reminder.id, skincare_type_id=skincare_type_id)
        db.session.add(new_reminder_skincare)

    db.session.commit()
    return jsonify({"message": "Reminder added successfully"}), 201
