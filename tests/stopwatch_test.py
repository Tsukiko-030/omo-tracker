import unittest
import time
from stopwatch import *

class TestStopwatch(unittest.TestCase):
    def test_start_stop(self):
        sw = Stopwatch()
        sw.start_stopwatch()
        time.sleep(2)
        sw.stop_stopwatch()
        elapsed = sw.get_elapsed_time()
        self.assertTrue(1 <= elapsed <= 3)

    def test_pause_resume(self):
        sw = Stopwatch()
        sw.start_stopwatch()
        time.sleep(1)
        sw.pause_stopwatch()
        elapsed_after_pause = sw.get_elapsed_time()
        time.sleep(1)
        sw.resume_stopwatch()
        time.sleep(1)
        sw.stop_stopwatch()
        total_elapsed = sw.get_elapsed_time()
        self.assertTrue(2 <= total_elapsed <= 4)
        self.assertEqual(elapsed_after_pause, 1)

    def test_reset(self):
        sw = Stopwatch()
        sw.start_stopwatch()
        time.sleep(1)
        sw.reset_stopwatch()
        self.assertEqual(sw.get_elapsed_time(), 0)
        self.assertFalse(sw.is_running())

    def test_exceptions(self):
        sw = Stopwatch()
        with self.assertRaises(StopwatchError):
            sw.stop_stopwatch()
        with self.assertRaises(StopwatchError):
            sw.pause_stopwatch()
        sw.start_stopwatch()
        with self.assertRaises(StopwatchError):
            sw.start_stopwatch()
        sw.stop_stopwatch()
        with self.assertRaises(StopwatchError):
            sw.resume_stopwatch()

if __name__ == '__main__':
    unittest.main()
