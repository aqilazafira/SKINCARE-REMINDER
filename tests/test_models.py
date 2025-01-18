from app import db
from app.models import (
    Feedback,
    Product,
    ProductRecommendation,
    ProductSkincareType,
    Recommendation,
    Reminder,
    ReminderSkincare,
    SkincareType,
    Timeline,
    User,
)


def test_user_model(init_db):
    user = User(username="testuser", email="testuser@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    assert user.check_password("password")
    assert not user.check_password("wrongpassword")


def test_product_model(init_db):
    product = Product(brand="Test Brand", description="Test Description", image_url="test.jpg")
    db.session.add(product)
    db.session.commit()

    assert product.brand == "Test Brand"
    assert product.description == "Test Description"


def test_recommendation_model(init_db):
    recommendation = Recommendation(title="Berminyak")
    db.session.add(recommendation)
    db.session.commit()

    assert recommendation.title == "Berminyak"


def test_skincare_type_model(init_db):
    skincare_type = SkincareType(title="Cleanser")
    db.session.add(skincare_type)
    db.session.commit()

    assert skincare_type.title == "Cleanser"


def test_feedback_model(init_db):
    user = User.query.first()
    feedback = Feedback(content="Great app!", user_id=user.id)
    db.session.add(feedback)
    db.session.commit()

    assert feedback.content == "Great app!"
    assert feedback.user_id == user.id


def test_timeline_model(init_db):
    user = User.query.first()
    timeline = Timeline(image_url="test.jpg", user_id=user.id)
    db.session.add(timeline)
    db.session.commit()

    assert timeline.image_url == "test.jpg"
    assert timeline.user_id == user.id


def test_reminder_model(init_db):
    user = User.query.first()
    reminder = Reminder(id=1, day=0, hour=8, minute=30, user_id=user.id)
    db.session.add(reminder)
    db.session.commit()

    assert reminder.day == 0
    assert reminder.hour == 8
    assert reminder.minute == 30
    assert reminder.user_id == user.id


def test_product_recommendation_model(init_db):
    product = Product.query.first()
    recommendation = Recommendation.query.first()
    product_recommendation = ProductRecommendation(product_id=product.id, recommendation_id=recommendation.id)
    db.session.add(product_recommendation)
    db.session.commit()

    assert product_recommendation.product_id == product.id
    assert product_recommendation.recommendation_id == recommendation.id


def test_product_skincare_type_model(init_db):
    product = Product.query.first()
    skincare_type = SkincareType.query.first()
    product_skincare_type = ProductSkincareType(product_id=product.id, skincare_type_id=skincare_type.id)
    db.session.add(product_skincare_type)
    db.session.commit()

    assert product_skincare_type.product_id == product.id
    assert product_skincare_type.skincare_type_id == skincare_type.id


# def test_reminder_skincare_model(init_db):
#     reminder = Reminder.query.first()
#     skincare_type = SkincareType.query.first()
#     reminder_skincare = ReminderSkincare(reminder_id=reminder.id, skincare_type_id=skincare_type.id)
#     db.session.add(reminder_skincare)
#     db.session.commit()

#     assert reminder_skincare.reminder_id == reminder.id
#     assert reminder_skincare.skincare_type_id == skincare_type.id
