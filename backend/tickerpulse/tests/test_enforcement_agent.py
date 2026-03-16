import unittest
from unittest.mock import patch
from datetime import datetime, time
from tickerpulse.enforcement_agent import enforce_schedule

class TestEnforcementAgent(unittest.TestCase):
    @patch('tickerpulse.enforcement_agent.datetime')
    def test_enforce_schedule(self, mock_datetime):
        mock_datetime.now.return_value.time.return_value = time(17, 30)
        enforce_schedule()
        mock_datetime.now.return_value.time.return_value = time(8, 30)
        enforce_schedule()

if __name__ == '__main__':
    unittest.main()