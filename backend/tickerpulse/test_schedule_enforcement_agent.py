import unittest
from unittest.mock import patch
from backend.tickerpulse.schedule_enforcement_agent import enforce_schedule

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch('backend.tickerpulse.schedule_enforcement_agent.current_app.config')
    def test_enforce_schedule(self, mock_config):
        mock_config['CURRENT_TIME'] = 16:00
        mock_config['DATABASE_PATH'] = 'tickerpulse.db'
        mock_config['non_dev_hours'] = [(15:00, 17:00)]

        with patch('backend.tickerpulse.schedule_enforcement_agent.get_db_connection') as mock_get_db:
            mock_cursor = mock_get_db.return_value.cursor.return_value
            mock_cursor.fetchall.return_value = [(15:00, 17:00)]

            enforce_schedule()
            mock_get_db.assert_called_once_with()
            mock_cursor.fetchall.assert_called_once()

if __:  # pragma: no cover
    unittest.main()