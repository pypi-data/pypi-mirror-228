import unittest
from quickbelog import Log
from quickbeutils import time_to_string


class StringUtilsTestCase(unittest.TestCase):

    def test_time_to_string(self):
        sec = 1000000
        sec_text = time_to_string(value=sec)
        Log.debug(sec_text)
        self.assertEqual(sec_text, time_to_string(sec*1000, units='msec'))

    def test_periods(self):
        test_cases = {
            61: 'minutes',
            3601: 'hours',
            int(3600*24+1): '1 days',
            int(3600*24*31+1): '31 days',
            int(3600*24*365+1+8120): '365 days',
            int(3600*24*2+3600*3+245): '2 days',
        }
        for sec, token in test_cases.items():
            sec_text = time_to_string(value=sec)
            Log.debug(sec_text)
            self.assertIn(token, sec_text)


if __name__ == '__main__':
    unittest.main()
