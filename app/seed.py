
from app import db
from app.models import Recommendation, SkincareType

def seed_data():
    recommendations = [
        "Berminyak",
        "Kering",
        "Kombinasi",
        "Normal",
        "Berjerawat",
    ]

    skincare_types = [
        "Cleanser",
        "Toner",
        "Serum",
        "Moisturizer",
        "Sunscreen",
        "Exfoliator",
        "Mask",
        "Eye Cream",
        "Face Oil"
    ]

    for title in recommendations:
        if not Recommendation.query.filter_by(title=title).first():
            db.session.add(Recommendation(title=title))

    for title in skincare_types:
        if not SkincareType.query.filter_by(title=title).first():
            db.session.add(SkincareType(title=title))

    db.session.commit()
    print("Seed data added successfully!")
