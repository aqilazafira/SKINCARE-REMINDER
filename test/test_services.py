import unittest
from unittest.mock import patch, MagicMock

from app.services import reminder_service, schedule_service, calender_service

# --- Test untuk reminder_service.py ---
class TestReminderService(unittest.TestCase):
    @patch("app.services.reminder_service.mail.send")
    def test_send_email_success(self, mock_mail_send):
        """
        Test fungsi send_email ketika pengiriman email berhasil.
        """
        # Simulasikan bahwa mail.send berjalan tanpa error
        mock_mail_send.return_value = None
        subject = "Test Subject"
        receiver = "test@example.com"
        message = "Test message"
        
        result = reminder_service.send_email(subject, receiver, message)
        self.assertEqual(result, "Email sent!")
        mock_mail_send.assert_called_once()

    @patch("app.services.reminder_service.mail.send")
    def test_send_email_failure(self, mock_mail_send):
        """
        Test fungsi send_email ketika terjadi error saat pengiriman email.
        """
        # Simulasikan error saat mail.send dipanggil
        mock_mail_send.side_effect = Exception("Failed to send")
        subject = "Test Subject"
        receiver = "test@example.com"
        message = "Test message"
        
        result = reminder_service.send_email(subject, receiver, message)
        self.assertIn("Error sending email", result)

# --- Test untuk schule_service.py ---
class TestSchuleService(unittest.TestCase):
    @patch("app.services.schule_service.scheduler")
    @patch("app.services.schule_service.current_app")
    def test_create_schedule(self, mock_current_app, mock_scheduler):
        """
        Test fungsi create_schedule untuk membuat schedule.
        """
        # Buat dummy job dengan id "job123"
        dummy_job = MagicMock()
        dummy_job.id = "job123"
        mock_scheduler.add_job.return_value = dummy_job
        # Setup dummy logger
        mock_logger = MagicMock()
        mock_current_app.logger = mock_logger

        from app.services.schedule_service import create_schedule
        dummy_action = lambda: None
        job_id = create_schedule(dummy_action, 1, 12, 0)
        self.assertEqual(job_id, "job123")
        mock_scheduler.add_job.assert_called_once()

    @patch("app.services.schule_service.scheduler")
    def test_delete_schedule(self, mock_scheduler):
        """
        Test fungsi delete_schedule untuk menghapus schedule.
        """
        from app.services.schedule_service import delete_schedule
        delete_schedule("job123")
        mock_scheduler.remove_job.assert_called_once_with("job123")

    @patch("app.services.schule_service.scheduler")
    def test_reschedule(self, mock_scheduler):
        """
        Test fungsi reschedule untuk mengubah jadwal.
        """
        from app.services.schedule_service import reschedule
        reschedule("job123", 2, 14, 30)
        mock_scheduler.reschedule_job.assert_called_once_with("job123", "cron", day_of_week=2, hour=14, minute=30)

# --- Test untuk calender_service.py ---
class TestCalenderService(unittest.TestCase):
    def test_get_next_weekday(self):
        """
        Test fungsi get_next_weekday yang merupakan fungsi murni (pure function).
        Pastikan tanggal yang dihasilkan adalah di masa depan.
        """
        from datetime import datetime
        from app.services.calender_service import get_next_weekday
        next_weekday = get_next_weekday(0)  # misal: mencari hari Senin (0)
        self.assertGreater(next_weekday, datetime.now())

    # Fungsi save_calendar_event, update_calendar_event, dan delete_calendar_event
    # bergantung pada Google Calendar API sehingga untuk pengujian lebih lanjut
    # sebaiknya menggunakan mocking yang lebih mendalam atau dites secara terpisah.
    # Di sini kita hanya akan mengetes fungsi murni atau melewati pengujian API.

if __name__ == "__main__":
    unittest.main()
