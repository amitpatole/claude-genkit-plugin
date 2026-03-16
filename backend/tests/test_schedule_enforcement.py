from unittest.mock import patch, MagicMock
from schedule_enforcement.schedule_enforcement import enforce_schedule, is_within_allowed_hours, log_violation, notify_user
from datetime import datetime, time

def test_enforcement() -> None:
    with patch('schedule_enforcement.schedule_enforcement.is_within_allowed_hours', return_value=False) as mock_within_hours:
        mock_within_hours.return_value = False
        with patch('schedule_enforcement.schedule_enforcement.log_violation') as mock_log_violation:
            with patch('schedule_enforcement.schedule_enforcement.notify_user') as mock_notify_user:
                enforce_schedule(12345, 67890)
                mock_log_violation.assert_called_once_with(12345, 67890)
                mock_notify_user.assert_called_once_with(12345, 67890)

def test_within_hours() -> None:
    with patch('schedule_enforcement.schedule_enforcement.is_within_allowed_hours', return_value=True) as mock_within_hours:
        mock_within_hours.return_value = True
        enforce_schedule(12345, 67890)
        assert not mock_log_violation.called
        assert not mock_notify_user.called

def test_is_within_allowed_hours() -> None:
    with patch('schedule_enforcement.schedule_enforcement.datetime') as mock_datetime:
        mock_datetime.now.return_value.time.return_value = time(23)  # 11 PM
        assert is_within_allowed_hours() is False

        mock_datetime.now.return_value.time.return_value = time(7)  # 7 AM
        assert is_within_allowed_hours() is False

        mock_datetime.now.return_value.time.return_value = time(10)  # 10 AM
        assert is_within_allowed_hours() is True