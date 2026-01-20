from flask import render_template, url_for
from flask_mail import Message

from app import mail, scheduler


def send_email(subject: str, receiver: str, message: str):
    with scheduler.app.app_context():
        reminder_url = url_for('reminder.reminder_page', _external=True)
        
        msg = Message(
            subject=subject,
            recipients=[receiver],
        )

        msg.body = message
        msg.html = render_template("mail.html", reminder_url=reminder_url)

        print(f"Sending email to {receiver}")

        try:
            mail.send(msg)
            return "Email sent!"
        except Exception as e:
            return f"Error sending email: {str(e)}"
