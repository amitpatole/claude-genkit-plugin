from unittest.mock import patch, MagicMock
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule
from datetime import datetime

def test_enforce_schedule(caplog):
    with patch('backend.tickerpulse.schedule_enforcement_agent.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 10, 12, 0, 0)
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [1, 2, 3]
        with patch('backend.tickerpulse.schedule_enforcement_agent.get_db_connection') as mock_get_db_connection:
            mock_conn = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_get_db_connection.return_value = mock_conn
            enforce_schedule()
            assert "Enforcing schedule" in caplog.text