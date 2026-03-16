from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule, get_db_connection
import pytest

@patch('backend.tickerpulse.schedule_enforcement_agent.get_db_connection')
def test_enforce_schedule(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('user1', datetime(2023, 10, 1, 9, 0), datetime(2023, 10, 1, 17, 0)),
        ('user2', datetime(2023, 10, 1, 10, 0), datetime(2023, 10, 1, 18, 0))
    ]
    mock_get_db_connection.return_value = mock_conn

    with patch('backend.tickerpulse.schedule_enforcement_agent.datetime') as mock_datetime:
        mock_now = datetime(2023, 10, 1, 11, 0)
        mock_datetime.now.return_value = mock_now

        enforce_schedule()

        mock_cursor.execute.assert_called_once_with("SELECT user_id, start_time, end_time FROM work_schedule WHERE status = 'active'")
        mock_cursor.fetchall.assert_called_once()
        mock_conn.close.assert_called_once()