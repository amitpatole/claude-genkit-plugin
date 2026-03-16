import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule, get_schedule_enforcement_db

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch('backend.tickerpulse.schedule_enforcement_agent.datetime')
    def test_enforce_schedule(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 10, 15, 0, 0)
        with patch('backend.tickerpulse.schedule_enforcement_agent.sqlite3.connect') as mock_connect:
            mock_cursor = MagicMock()
            mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [{"task_id": 123}]
            enforce_schedule()
            mock_cursor.execute.assert_called_once_with("SELECT * FROM schedule WHERE time >= ?", (datetime(2023, 10, 10, 15, 0, 0),))
            mock_cursor.fetchall.assert_called_once()
            mock_cursor.close.assert_called_once()
            mock_connect.assert_called_once_with(get_db_path("schedule_enforcement.db"), detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

if __name__ == '__main__':
    unittest.main()