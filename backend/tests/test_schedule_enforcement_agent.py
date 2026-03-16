from unittest.mock import patch, MagicMock
from backend.schedule_enforcement_agent import get_non_dev_hours, is_within_non_dev_hours, enforce_schedule

def test_get_non_dev_hours():
    assert get_non_dev_hours() == (time(18, 0), time(8, 0))

@patch('backend.schedule_enforcement_agent.datetime')
def test_is_within_non_dev_hours(mock_datetime):
    mock_now = datetime.now()
    mock_now.time.return_value = time(17, 30)
    assert not is_within_non_dev_hours(mock_now.time())

    mock_now.time.return_value = time(18, 0)
    assert is_within_non_dev_hours(mock_now.time())

    mock_now.time.return_value = time(23, 0)
    assert not is_within_non_dev_hours(mock_now.time())

@patch('backend.schedule_enforcement_agent.logging')
def test_enforce_schedule(mock_logging):
    enforce_schedule(1)
    mock_logging.warning.assert_called_once_with("User 1 is active during non-development hours.")