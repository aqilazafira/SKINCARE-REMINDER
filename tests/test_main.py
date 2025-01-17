from app import create_app, db
from app.models import Feedback, User


def test_feedback_creation(auth_client, init_db):
    response = auth_client.post("/feedback", data=dict(feedback='Great app!'), follow_redirects=True)
