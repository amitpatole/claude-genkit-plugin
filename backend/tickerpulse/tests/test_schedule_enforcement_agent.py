from typing import Any
import unittest
from unittest.mock import patch, MagicMock
from backend.tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent, get_db_connection

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch('backend.tickerpulse.schedule_enforcement_agent.get_db_connection')
    def test_enforce_schedule_in_development_hours(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = {'user_id': 1, 'schedule': 'Development'}
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_connection

        agent = ScheduleEnforcementAgent()
        result = agent.enforce_schedule(1)
        self.assertEqual(result, {'user_id': 1, 'schedule': 'Development'})

    @patch('backend.tickerpulse.schedule_enforcement_agent.get_db_connection')
    def test_enforce_schedule_outside_development_hours(self, mock_get_db_connection):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connection.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value = mock_connection

        agent = ScheduleEnforcementAgent()
        result = agent.enforce_schedule(1)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()