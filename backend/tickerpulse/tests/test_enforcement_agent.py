from unittest.mock import patch
from backend.tickerpulse.enforcement_agent import enforce_schedule
from datetime import datetime

def test_enforce_schedule_non_dev_hours():
    with patch('backend.tickerpulse.enforcement_agent.get_db_connection') as mock_conn:
        mock_cursor = mock_conn().__enter__().cursor
        mock_cursor.fetchone.return_value = {'non_dev_hours': ['17:00-18:00']}
        
        result = enforce_schedule(1, '17:30')
        assert result is True

def test_enforce_schedule_dev_hours():
    with patch('backend.tickerpulse.enforcement_agent.get_db_connection') as mock_conn:
        mock_cursor = mock_conn().__enter__().cursor
        mock_cursor.fetchone.return_value = {'non_dev_hours': ['18:00-19:00']}
        
        result = enforce_schedule(1, '18:00')
        assert result is False