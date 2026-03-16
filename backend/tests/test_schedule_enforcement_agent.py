from unittest.mock import patch, MagicMock
from backend.schedule_enforcement_agent import get_current_time, is_non_dev_hour, get_non_dev_hours_schedule, enforce_schedule
from datetime import datetime

def test_get_current_time() -> None:
    with patch('backend.schedule_enforcement_agent.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 10, 17, 30, 0)
        assert get_current_time() == time(17, 30, 0)

def test_is_non_dev_hour() -> None:
    assert is_non_dev_hour(time(17, 30, 0)) == True
    assert is_non_dev_hour(time(8, 30, 0)) == False

def test_get_non_dev_hours_schedule() -> None:
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {'task_name': 'task1', 'start_time': datetime(2023, 10, 10, 18, 0, 0), 'end_time': datetime(2023, 10, 10, 19, 0, 0)},
        {'task_name': 'task2', 'start_time': datetime(2023, 10, 10, 19, 0, 0), 'end_time': datetime(2023, 10, 10, 20, 0, 0)}
    ]
    with patch('backend.schedule_enforcement_agent.sqlite3.connect') as mock_connect:
        mock_connect.return_value = mock_cursor
        schedule = get_non_dev_hours_schedule()
        assert schedule == {'task1': time(18, 0, 0), 'task2': time(19, 0, 0)}

def test_enforce_schedule() -> None:
    with patch('backend.schedule_enforcement_agent.get_non_dev_hours_schedule') as mock_get_schedule:
        mock_get_schedule.return_value = {'task1': time(18, 0, 0)}
        with patch('backend.schedule_enforcement_agent.logging') as mock_logging:
            enforce_schedule()
            mock_logging.info.assert_called_with("Task task1 is scheduled for 18:00:00 during non-dev hours.")