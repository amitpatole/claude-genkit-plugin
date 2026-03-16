from unittest.mock import patch, MagicMock
from backend.schedule_enforcement.schedule_enforcement import is_allowed_time, log_violation, notify_user, enforce_schedule
import pytest

def test_is_allowed_time():
    with patch("backend.schedule_enforcement.schedule_enforcement.datetime") as mock_datetime:
        mock_datetime.now.return_value.astimezone.return_value.hour = 23
        assert is_allowed_time() == True

        mock_datetime.now.return_value.astimezone.return_value.hour = 8
        assert is_allowed_time() == False

def test_log_violation():
    with patch("backend.schedule_enforcement.schedule_enforcement.sqlite3.connect") as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_connect.return_value.commit.return_value = None
        mock_connect.return_value.close.return_value = None
        log_violation("user123", datetime(2023, 10, 1, 9, 0, 0, tzinfo=timezone.utc), "Test violation")

def test_notify_user():
    with patch("backend.schedule_enforcement.schedule_enforcement.current_app") as mock_current_app:
        mock_logger = mock_current_app.logger
        notify_user("user123", datetime(2023, 10, 1, 9, 0, 0, tzinfo=timezone.utc), "Test violation")
        mock_logger.info.assert_called_once()

def test_enforce_schedule():
    with patch("backend.schedule_enforcement.schedule_enforcement.is_allowed_time") as mock_is_allowed_time:
        mock_is_allowed_time.return_value = False
        enforce_schedule("user123", datetime(2023, 10, 1, 9, 0, 0, tzinfo=timezone.utc), "Test violation")
        assert mock_is_allowed_time.call_count == 1
        assert log_violation.call_count == 1
        assert notify_user.call_count == 1

if __name__ == "__main__":
    pytest.main()