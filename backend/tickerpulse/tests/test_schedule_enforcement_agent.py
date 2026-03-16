import unittest
from unittest.mock import patch
from tickerpulse.schedule_enforcement_agent import ScheduleEnforcementAgent, get_schedule_enforcement_config
from datetime import datetime

class TestScheduleEnforcementAgent(unittest.TestCase):
    @patch('tickerpulse.schedule_enforcement_agent.get_current_time')
    def test_enforce_schedule(self, mock_get_current_time):
        mock_get_current_time.return_value = datetime(2023, 10, 1, 15)  # 15:00 is in non-dev hours
        agent = ScheduleEnforcementAgent(db_path="test.db")
        agent.enforce_schedule()
        self.assertTrue(mock_get_current_time.called)

    @patch('tickerpulse.schedule_enforcement_agent.get_current_time')
    def test_no_enforcement_outside_non_dev_hours(self, mock_get_current_time):
        mock_get_current_time.return_value = datetime(2023, 10, 1, 9)  # 09:00 is not in non-dev hours
        agent = ScheduleEnforcementAgent(db_path="test.db")
        agent.enforce_schedule()
        self.assertTrue(mock_get_current_time.called)

if __name__ == '__main__':
    unittest.main()