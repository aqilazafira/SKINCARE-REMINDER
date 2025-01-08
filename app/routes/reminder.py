from datetime import datetime, timedelta

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from flask_mail import Message

from app import mail

reminder_bp = Blueprint("reminder", __name__)


@reminder_bp.route("/save_schedule", methods=["POST"])
@login_required
def save_schedule():
    schedule_type = request.form["schedule"]
    hours = int(request.form["hours"])
    minutes = int(request.form["minutes"])
    period = request.form["period"]

    # Convert to 24-hour format
    if period == "PM" and hours != 12:
        hours += 12
    elif period == "AM" and hours == 12:
        hours = 0

    time = f"{hours:02d}:{minutes:02d}"

    # # schedules = load_schedules()
    # schedules[schedule_type] = time
    # save_schedules(schedules)

    flash("Schedule saved successfully!", "success")
    return redirect(url_for("reminder.reminder_page"))


@reminder_bp.route("/pengingat")
@login_required
def reminder_page():
    # schedules = load_schedules()
    return render_template("pengingat.html")


@reminder_bp.route("/get_reminders")
@login_required
def get_reminders():
    # schedules = load_schedules()
    current_time = datetime.now()
    reminders = []

    for schedule_type, time in schedules.items():
        reminder_time = datetime.strptime(time, "%H:%M").replace(
            year=current_time.year, month=current_time.month, day=current_time.day
        )

        if reminder_time < current_time:
            reminder_time += timedelta(days=1)

        if (reminder_time - current_time).total_seconds() <= 60:  # Check if within the next minute
            reminders.append({"type": schedule_type, "time": time})

    return jsonify(reminders)


@reminder_bp.route("/mail")
def handle_email():
    msg = Message(
        subject="Love letter",
        recipients=["gearykeaton@gmail.com"],
    )
    msg.body = "I love you!"

    try:
        mail.send(msg)
        return "Email sent!"
    except Exception as e:
        return f"Error sending email: {str(e)}"
