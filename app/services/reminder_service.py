from flask import current_app
from flask_mail import Message

from app import mail

def send_email(subject: str, receiver: str, message: str):
    with current_app.app_context():
        msg = Message(
            subject=subject,
            recipients=[receiver],
        )

        msg.body = message
        print(f"Sending email to {receiver}")

        try:
            mail.send(msg)
            return "Email sent!"
        except Exception as e:
            return f"Error sending email: {str(e)}"
