from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app import db
from app.models import Reminder, ReminderSkincare, SkincareType, User
from app.services.calender_service import delete_calendar_event, save_calendar_event, update_calendar_event
from app.services.reminder_service import send_email
from app.services.schedule_service import create_schedule, delete_schedule, reschedule

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

    # Convert day from string to integer
    day = DAYS.index(day.upper())

    receiver = current_user.email
    reminder_action = lambda: send_email(
        subject="Reminder",
        receiver=receiver,
        message="Don't forget to do your skincare routine!",
    )

    reminder = Reminder.query.filter_by(user_id=current_user.id, day=day).first()
    if reminder:
        reminder.hour = hour
        reminder.minute = minute
        db.session.commit()
        ReminderSkincare.query.filter_by(reminder_id=reminder.id).delete()
        db.session.commit()
        reschedule(reminder.id, day=day, hour=hour, minute=minute)
        update_calendar_event(reminder.id, day, f"{hour}:{minute}", receiver)
    else:
        job_id = create_schedule(action=reminder_action, day=day, hour=hour, minute=minute)
        reminder = Reminder(id=job_id, user_id=current_user.id, day=day, hour=hour, minute=minute)
        db.session.add(reminder)
        db.session.commit()
        save_calendar_event(day, f"{hour}:{minute}", receiver)

    for skincare_type in skincare_types:
        skincare_type = skincare_type
        skincare_type_id = SkincareType.query.filter_by(title=skincare_type).first().id

        new_reminder_skincare = ReminderSkincare(reminder_id=reminder.id, skincare_type_id=skincare_type_id)
        db.session.add(new_reminder_skincare)

    db.session.commit()
    return jsonify({"message": "Reminder added successfully"}), 201


@reminder_bp.route("/pengingat", methods=["DELETE"])
@login_required
def delete_reminder():
    data = request.get_json()
    day = data.get("day")

    # Convert day from string to integer
    day_of_week = DAYS.index(day.upper())

    reminder = Reminder.query.filter_by(user_id=current_user.id, day=day_of_week).first()

    try:
        delete_schedule(reminder.id)
        delete_calendar_event(reminder.id)
    except Exception:
        pass

    if reminder:
        ReminderSkincare.query.filter_by(reminder_id=reminder.id).delete()
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({"message": "Reminder deleted successfully"}), 200
    return jsonify({"message": "Reminder not found"}), 404
