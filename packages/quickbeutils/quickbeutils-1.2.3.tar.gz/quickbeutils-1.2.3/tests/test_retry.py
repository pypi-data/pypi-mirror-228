import inspect
import unittest
from quickbelog import Log
from quickbeutils import retry


def _get_method_name() -> str:
    this_stack = inspect.stack()
    name = this_stack[1][3]
    return name.replace('_', ' ')


def always_fail(a1: str, a2: int):
    msg = f'{a1} {a2}'
    Log.debug(msg)
    raise AssertionError('This is always fails.')


class RetryTestCase(unittest.TestCase):

    def test_until_fails(self):
        try:
            retry(always_fail, "This is a test", 123)
        except TimeoutError:
            Log.exception('Exception expected :-)')
            self.assertEqual(True, True)

    def test_succeed_after_number_of_sec(self):

        def return_after_x_seconds(sw_id: str, seconds: int):
            sec = Log.stopwatch_seconds(stopwatch_id=sw_id)
            if sec > seconds:
                return sec
            else:
                raise ValueError(f'Too early, passed {sec}, waiting for {seconds}')
        x = 5
        n = retry(
            return_after_x_seconds, Log.start_stopwatch(_get_method_name()),
            x, retries=5, delay=1
        )
        self.assertGreaterEqual(n, x)

    def test_random_delay(self):
        max_time = 5.0
        sw_id = Log.start_stopwatch(_get_method_name())

        try:
            retry(always_fail, "This is a test", 123, retries=10, time_limit=max_time, delay_pattern='random')
        except TimeoutError:
            Log.exception('Exception expected :-)')
            self.assertGreaterEqual(Log.stopwatch_seconds(stopwatch_id=sw_id), max_time)

    def test_retry_loop_fixed_delay_pattern(self):
        max_time = 6.5

        sw_id = Log.start_stopwatch(_get_method_name())
        try:
            retry(
                always_fail, "This is a test", 123,
                retries=5, delay=1.5, time_limit=max_time, delay_pattern='fixed'
            )
            self.assertLessEqual(Log.stopwatch_seconds(stopwatch_id=sw_id), max_time)
        except TimeoutError:
            Log.exception('')

        sw_id = Log.start_stopwatch(_get_method_name())
        try:
            retry(
                always_fail, "This is a test", 123,
                retries=6, delay=1.5, time_limit=max_time, delay_pattern='fixed'
            )
        except TimeoutError:
            Log.exception('')
            Log.exception('Exception expected :-)')
            self.assertGreaterEqual(Log.stopwatch_seconds(stopwatch_id=sw_id), max_time)

    def test_time_limit_exceeded(self):
        max_time = 5
        sw_id = Log.start_stopwatch(_get_method_name())

        try:
            retry(always_fail, "This is a test", 123, retries=3, time_limit=max_time)
        except TimeoutError:
            Log.exception('Exception expected :-)')
            self.assertLessEqual(Log.stopwatch_seconds(stopwatch_id=sw_id), max_time * 1.5)
            self.assertGreaterEqual(Log.stopwatch_seconds(stopwatch_id=sw_id), max_time)


if __name__ == '__main__':
    unittest.main()
