from unittest.mock import patch
from app.services.reminder_service import send_email
from app.services.schedule_service import create_schedule, delete_schedule, reschedule

@patch('app.services.reminder_service.mail.send')
def test_send_email(mock_mail_send, app):
    with app.app_context():
        response = send_email("Test Subject", "test@example.com", "Test Message")
        assert response == "Email sent!"
        mock_mail_send.assert_called_once()

@patch('app.services.schedule_service.scheduler.add_job')
def test_create_schedule(mock_add_job, app):
    with app.app_context():
        mock_add_job.return_value.id = 'test_job_id'
        job_id = create_schedule(lambda: print("Test Action"), day=2, hour=8, minute=30)
        assert job_id == 'test_job_id'
        mock_add_job.assert_called_once()

@patch('app.services.schedule_service.scheduler.remove_job')
def test_delete_schedule(mock_remove_job, app):
    with app.app_context():
        job_id = create_schedule(lambda: print("Test Action"), day=2, hour=8, minute=30)
        delete_schedule(job_id)
        mock_remove_job.assert_called_once_with(job_id)

