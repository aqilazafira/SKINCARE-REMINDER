import io

from PIL import Image
from werkzeug.datastructures import FileStorage

from app.models import Feedback, Timeline

def create_test_image():
    img = Image.new("RGB", (100, 100), color=(73, 109, 137))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_byte_arr.seek(0)
    return img_byte_arr


def test_feedback_creation(auth_client, init_db):
    response = auth_client.post("/feedback", data=dict(feedback="Great app!"), follow_redirects=True)
    assert response.status_code == 200
    feedback = Feedback.query.filter_by(content="Great app!").first()
    assert feedback is not None


def test_timeline_creation(auth_client, init_db):
    file_storage = FileStorage(stream=create_test_image(), filename="test.jpg", content_type="image/jpeg")
    response = auth_client.post("/timeline", data={"file": file_storage}, follow_redirects=True)
    assert response.status_code == 200
    timeline = Timeline.query.filter_by(user_id=1).first()
    assert timeline is not None
