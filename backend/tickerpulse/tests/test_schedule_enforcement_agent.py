from unittest.mock import patch
from datetime import datetime
import pytest
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule

@patch('backend.tickerpulse.schedule_enforcement_agent.datetime')
def test_enforce_schedule(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 10, 10, 15, 30)
    with patch('backend.tickerpulse.schedule_enforcement_agent.get_db_conn') as mock_get_db_conn:
        mock_cursor = mock_get_db_conn().__aenter__.return_value
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'time': datetime(2023, 10, 10, 15, 30)}
        ]
        enforce_schedule()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM schedule WHERE active = 1", ())
        mock_cursor.fetchall.assert_called_once()
        mock_get_db_conn().__aenter__.assert_called_once()
        mock_get_db_conn().__exit__.assert_called_once()