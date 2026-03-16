from unittest.mock import patch
from datetime import datetime
from backend.tickerpulse.schedule_enforcement import is_non_dev_hour, enforce_schedule

def test_is_non_dev_hour():
    """Test the is_non_dev_hour function."""
    # Mock time outside development hours
    with patch('backend.tickerpulse.schedule_enforcement.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1, 6, 0)  # 6 AM
        assert is_non_dev_hour(mock_datetime.now().time()) == True

    # Mock time within development hours
    with patch('backend.tickerpulse.schedule_enforcement.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1, 15, 0)  # 3 PM
        assert is_non_dev_hour(mock_datetime.now().time()) == False

def test_enforce_schedule():
    """Test the enforce_schedule function."""
    # Mock time outside development hours
    with patch('backend.tickerpulse.schedule_enforcement.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1, 6, 0)  # 6 AM
        assert enforce_schedule(mock_datetime.now().time()) == True

    # Mock time within development hours
    with patch('backend.tickerpulse.schedule_enforcement.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1, 15, 0)  # 3 PM
        assert enforce_schedule(mock_datetime.now().time()) == False