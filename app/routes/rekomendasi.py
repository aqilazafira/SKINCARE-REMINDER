from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required
from datetime import datetime
from pytz import timezone, utc

from app import db
from app.models import Product, Recommendation, SkincareStep, SkinRecommendation

rekomendasi_bp = Blueprint("rekomendasi", __name__)

def get_routine_from_db(skin_type):
    """Fetches and formats skincare routine from the database."""
    morning_steps_db = (
        db.session.query(SkincareStep, SkinRecommendation)
        .join(SkinRecommendation, SkincareStep.id == SkinRecommendation.step_id)
        .filter(
            SkinRecommendation.skin_type == skin_type,
            SkincareStep.routine_type == "Morning",
        )
        .order_by(SkincareStep.step_order)
        .all()
    )

    night_steps_db = (
        db.session.query(SkincareStep, SkinRecommendation)
        .join(SkinRecommendation, SkincareStep.id == SkinRecommendation.step_id)
        .filter(
            SkinRecommendation.skin_type == skin_type,
            SkincareStep.routine_type == "Night",
        )
        .order_by(SkincareStep.step_order)
        .all()
    )

    formatted_routine = {
        "morning": [{"step": step.name, "detail": rec.detail} for step, rec in morning_steps_db],
        "night": [{"step": step.name, "detail": rec.detail} for step, rec in night_steps_db],
    }
    return formatted_routine

@rekomendasi_bp.route("/rekomendasi")
@login_required
def rekomendasi():
    return render_template("rekomendasi.html")

# Halaman kulit berminyak
@rekomendasi_bp.route("/kulit_berminyak")
def kulit_berminyak():
    skin_type = "berminyak"
    recommendation = Recommendation.query.filter_by(title="Berminyak").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    skin_type_recs = get_routine_from_db(skin_type)
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title, skin_type=skin_type, recommendations=skin_type_recs)

# Halaman kulit kering
@rekomendasi_bp.route("/kulit_kering")
def kulit_kering():
    skin_type = "kering"
    recommendation = Recommendation.query.filter_by(title="Kering").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    skin_type_recs = get_routine_from_db(skin_type)
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title, skin_type=skin_type, recommendations=skin_type_recs)

# Halaman kulit kombinasi
@rekomendasi_bp.route("/kulit_kombinasi")
def kulit_kombinasi():
    skin_type = "kombinasi"
    recommendation = Recommendation.query.filter_by(title="Kombinasi").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    skin_type_recs = get_routine_from_db(skin_type)
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title, skin_type=skin_type, recommendations=skin_type_recs)

# Halaman kulit normal
@rekomendasi_bp.route("/kulit_normal")
def kulit_normal():
    skin_type = "normal"
    recommendation = Recommendation.query.filter_by(title="Normal").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    skin_type_recs = get_routine_from_db(skin_type)
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title, skin_type=skin_type, recommendations=skin_type_recs)

# Halaman kulit berjerawat
@rekomendasi_bp.route("/kulit_berjerawat")
def kulit_berjerawat():
    skin_type = "sensitif"  # Assuming berjerawat maps to sensitif
    recommendation = Recommendation.query.filter_by(title="Berjerawat").first()
    products = Product.query.join(Product.recommendations).filter_by(recommendation_id=recommendation.id).all()
    skin_type_recs = get_routine_from_db(skin_type)
    return render_template("rekomendasi_page.html", products=products, recommendation_title=recommendation.title, skin_type=skin_type, recommendations=skin_type_recs)

# Placeholder for utility functions
def create_google_event_for_user(user_id, title, start_datetime_iso, description=None):
    """Placeholder: Creates a Google Calendar event for the user."""
    print(f"Event Created: User({user_id}), Title({title}), Start({start_datetime_iso}), Desc({description})")
    return f"evt_{user_id}_{title.replace(' ', '_')}_{start_datetime_iso}"

def send_email_to_user(user_id, subject, html_body):
    """Placeholder: Sends an email to the user."""
    print(f"Email Sent: User({user_id}), Subject({subject})")
    pass

@rekomendasi_bp.route('/rekomendasi/<skin_type>/generate', methods=['POST'])
def generate_routine(skin_type):
    """Generates calendar events and sends a confirmation email for a skincare routine."""
    data = request.get_json()
    user_id = data.get('user_id')
    date_str = data.get('date')
    user_tz_str = data.get('user_timezone', 'UTC')

    if not all([user_id, date_str, user_tz_str]):
        return jsonify({"error": "Missing required fields: user_id, date, user_timezone"}), 400

    try:
        user_timezone = timezone(user_tz_str)
        routine_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        steps_to_schedule = db.session.query(SkincareStep, SkinRecommendation).join(SkinRecommendation, SkincareStep.id == SkinRecommendation.step_id).filter(SkinRecommendation.skin_type == skin_type).order_by(SkincareStep.routine_type, SkincareStep.step_order).all()

        if not steps_to_schedule:
            return jsonify({"error": "Invalid skin type or no routine found"}), 404

        created_events = []
        email_summary = f"<h1>Your Skincare Routine for {routine_date.strftime('%A, %B %d, %Y')}</h1>"
        
        morning_html = "<h2>Morning Routine</h2><ul>"
        night_html = "<h2>Night Routine</h2><ul>"

        for step, recommendation in steps_to_schedule:
            step_time = step.default_time
            local_dt = user_timezone.localize(datetime.combine(routine_date, step_time))
            utc_dt_iso = local_dt.astimezone(utc).isoformat()
            event_title = f"Skincare: {step.name}"
            event_description = recommendation.detail

            try:
                event_id = create_google_event_for_user(
                    user_id=user_id,
                    title=event_title,
                    start_datetime_iso=utc_dt_iso,
                    description=event_description
                )
                created_events.append({"step": step.name, "event_id": event_id})
                
                item_html = f"<li><b>{step_time.strftime('%H:%M')}</b> - {step.name}: {event_description}</li>"
                if step.routine_type == "Morning":
                    morning_html += item_html
                else:
                    night_html += item_html

            except Exception as e:
                current_app.logger.error(f"Failed to create calendar event for {step.name}: {e}")
                return jsonify({"error": f"Failed to create event for {step.name}", "details": str(e)}), 500
        
        morning_html += "</ul>"
        night_html += "</ul>"
        email_summary += morning_html + night_html

        send_email_to_user(
            user_id=user_id,
            subject=f"Your Skincare Schedule for {routine_date.strftime('%Y-%m-%d')}",
            html_body=email_summary
        )

    except Exception as e:
        current_app.logger.error(f"An error occurred during routine generation: {e}")
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500

    return jsonify({"status": "ok", "created_events": created_events})
