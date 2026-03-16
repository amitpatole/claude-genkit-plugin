import unittest
from unittest.mock import patch
from datetime import datetime
from backend.tickerpulse.schedule_enforcement_agent import (get_current_hour, is_non_dev_hour, enforce_schedule, enforce_schedule_async, check_and_log_schedule_enforcement)

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch('backend.tickerpulse.schedule_enforcement_agent.datetime')
    def test_is_non_dev_hour(self, mock_datetime):
        mock_datetime.now.return_value.hour = 21
        self.assertTrue(is_non_dev_hour(mock_datetime.now.return_value.hour))

        mock_datetime.now.return_value.hour = 7
        self.assertFalse(is_non_dev_hour(mock_datetime.now.return_value.hour))

    @patch('backend.tickerpulse.schedule_enforcement_agent.datetime')
    def test_enforce_schedule(self, mock_datetime):
        mock_datetime.now.return_value.hour = 21
        self.assertFalse(enforce_schedule(mock_datetime.now.return_value.hour))

        mock_datetime.now.return_value.hour = 7
        self.assertTrue(enforce_schedule(mock_datetime.now.return_value.hour))

    @patch('backend.tickerpulse.schedule_enforcement_agent.datetime')
    def test_check_and_log_schedule_enforcement(self, mock_datetime):
        mock_datetime.now.return_value.hour = 21
        with patch('backend.tickerpulse.schedule_enforcement_agent.logging') as mock_logging:
            check_and_log_schedule_enforcement()
            mock_logging.info.assert_called_with("Schedule Enforcement: Enforced: False")

        mock_datetime.now.return_value.hour = 7
        with patch('backend.tickerpulse.schedule_enforcement_agent.logging') as mock_logging:
            check_and_log_schedule_enforcement()
            mock_logging.info.assert_called_with("Schedule Enforcement: Enforced: True")

if __name__ == '__main__':
    unittest.main()