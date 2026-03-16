from typing import Any
import unittest
from unittest.mock import patch
from backend.tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch("backend.utils.db.get_db_connection")
    def test_enforce_schedule(self, mock_get_db_connection):
        agent = ScheduleEnforcementAgent()
        mock_cursor = mock_get_db_connection.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = {"is_scheduled": True}

        result = agent.enforce_schedule(123)
        self.assertTrue(result)

        mock_cursor.fetchone.return_value = {"is_scheduled": False}
        result = agent.enforce_schedule(123)
        self.assertFalse(result)

        mock_cursor.fetchone.return_value = None
        result = agent.enforce_schedule(123)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()