
import json
import os
from datetime import datetime

from app import db
from app.models import (
    Recommendation,
    SkincareStep,
    SkincareType,
    SkinRecommendation,
)


def seed_data():
    seed_recommendations_and_types()
    seed_skincare_routines()
    print("Seed data added successfully!")


def seed_recommendations_and_types():
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
        "Face Oil",
    ]

    for title in recommendations:
        if not Recommendation.query.filter_by(title=title).first():
            db.session.add(Recommendation(title=title))

    for title in skincare_types:
        if not SkincareType.query.filter_by(title=title).first():
            db.session.add(SkincareType(title=title))

    db.session.commit()


def seed_skincare_routines():
    # Clear existing data
    db.session.query(SkinRecommendation).delete()
    db.session.query(SkincareStep).delete()
    db.session.commit()

    # Load data from JSON
    steps_path = os.path.join(os.path.dirname(__file__), "static/data/skincare_steps.json")
    recs_path = os.path.join(os.path.dirname(__file__), "static/data/recommendations_by_skin.json")

    with open(steps_path) as f:
        steps_data = json.load(f)
    with open(recs_path) as f:
        recs_data = json.load(f)

    # --- Create SkincareStep objects ---
    created_steps = {}  # To keep track of created steps: {step_name: step_object}
    step_order_counter = {"Morning": 0, "Night": 0}

    # First pass: from skincare_steps.json to get order and time
    for routine_type, steps in steps_data.items():
        for step_info in steps:
            step_name = step_info["step"]
            if step_name not in created_steps:
                step_time = datetime.strptime(step_info["time"], "%H:%M").time()
                step = SkincareStep(
                    name=step_name,
                    routine_type=routine_type.capitalize(),
                    default_time=step_time,
                    step_order=step_order_counter[routine_type.capitalize()],
                )
                db.session.add(step)
                created_steps[step_name] = step
                step_order_counter[routine_type.capitalize()] += 1

    # Second pass: from recommendations_by_skin.json to catch any unique steps
    for skin_type, routines in recs_data.items():
        for routine_type, steps in routines.items():
            for step_info in steps:
                step_name = step_info["step"]
                if step_name not in created_steps:
                    # For steps not in the primary list, default time/order is needed
                    step = SkincareStep(
                        name=step_name,
                        routine_type=routine_type.capitalize(),
                        default_time=datetime.strptime("00:00", "%H:%M").time(),
                        step_order=99,  # Put at the end
                    )
                    db.session.add(step)
                    created_steps[step_name] = step
    
    db.session.commit() # Commit steps to get IDs

    # --- Create SkinRecommendation objects ---
    for skin_type, routines in recs_data.items():
        for routine_type, steps in routines.items():
            for step_info in steps:
                step_name = step_info["step"]
                step_detail = step_info["detail"]
                
                # Find the corresponding step object from our created_steps dict
                step_object = created_steps.get(step_name)

                if step_object:
                    recommendation = SkinRecommendation(
                        skin_type=skin_type,
                        step_id=step_object.id,
                        detail=step_detail,
                    )
                    db.session.add(recommendation)

    db.session.commit()
