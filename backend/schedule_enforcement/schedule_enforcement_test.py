from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.schedule_enforcement import is_within_non_dev_hours, get_non_dev_hours
from backend.app import app

def test_get_non_dev_hours():
    assert get_non_dev_hours() == {"start": "18:00", "end": "08:00", "timezone": "UTC"}

@patch('backend.schedule_enforcement.datetime')
def test_is_within_non_dev_hours(mock_datetime):
    mock_now = datetime(2023, 10, 1, 19, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now
    assert is_within_non_dev_hours(mock_now) == True

    mock_now = datetime(2023, 10, 1, 7, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now
    assert is_within_non_dev_hours(mock_now) == False