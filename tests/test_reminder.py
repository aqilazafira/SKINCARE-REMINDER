from flask_login import login_user

from app.models import Reminder



def test_reminder_creation(auth_client, test_user):
    response = auth_client.patch(
        "/pengingat", json={"day": "SENIN", "hour": 8, "minute": 30, "skincareTypes": ["Cleanser", "Toner"]}
    )
    assert response.status_code == 201
    assert response.json["message"] == "Reminder added successfully"

    reminder = Reminder.query.filter_by(user_id=test_user.id).first()
    assert reminder is not None
    assert reminder.day == 0
    assert reminder.hour == 8
    assert reminder.minute == 30

    skincare_types = [skincare_type.skincare_type.title for skincare_type in reminder.skincare_types]
    assert "Cleanser" in skincare_types
    assert "Toner" in skincare_types


def test_reminder_page(auth_client, init_db, test_user):
    response = auth_client.get("/pengingat")
    assert response.status_code == 200
    assert b"SENIN" in response.data
    assert b"Set Skincare Routine" in response.data
    assert b"Cleanser" in response.data
    assert b"Toner" in response.data


def test_reminder_update(auth_client, init_db, test_user):
    response = auth_client.patch("/pengingat", json={"day": "SENIN", "hour": 9, "minute": 0, "skincareTypes": ["Serum"]})
    assert response.status_code == 201
    assert response.json["message"] == "Reminder added successfully"

    reminder = Reminder.query.filter_by(user_id=test_user.id).first()
    assert reminder is not None
    assert reminder.day == 0
    assert reminder.hour == 9
    assert reminder.minute == 0

    skincare_types = [skincare_type.skincare_type.title for skincare_type in reminder.skincare_types]
    assert "Serum" in skincare_types
