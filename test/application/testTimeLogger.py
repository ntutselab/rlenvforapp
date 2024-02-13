import os
import time
import unittest

from RLEnvForApp.application.timeLoggerService.TimeLoggerService import \
    TimeLoggerService


class TestTimeLogger(unittest.TestCase):
    def set_up(self) -> None:
        self.log_dir = "model/timeLoggerTest/"

        self.start_time_file_name = "startTime.log"
        start_time_log_path = os.path.join(self.log_dir, self.start_time_file_name)
        if os.path.exists(start_time_log_path):
            os.remove(start_time_log_path)

        self.stop_time_file_name = "stopTime.log"
        stop_time_log_path = os.path.join(self.log_dir, self.stop_time_file_name)
        if os.path.exists(stop_time_log_path):
            os.remove(stop_time_log_path)

        self.time_period_file_name = "timePeriod.log"
        time_period_log_path = os.path.join(self.log_dir, self.time_period_file_name)
        if os.path.exists(time_period_log_path):
            os.remove(time_period_log_path)

    def tear_down(self) -> None:
        pass

    def test_period_log(self):
        time_passed_seconds = 1

        start_time_seconds = TimeLoggerService().log_start(log_dir=self.log_dir)
        time.sleep(time_passed_seconds)
        stop_time_seconds = TimeLoggerService().log_stop(log_dir=self.log_dir)

        self.assertGreaterEqual(
            stop_time_seconds -
            start_time_seconds,
            time_passed_seconds)
        start_time_log_path = os.path.join(self.log_dir, self.start_time_file_name)
        stop_time_log_path = os.path.join(self.log_dir, self.stop_time_file_name)
        self.assertTrue(os.path.exists(start_time_log_path))
        self.assertTrue(os.path.exists(stop_time_log_path))

        time_period_log_path = os.path.join(self.log_dir, self.time_period_file_name)
        diff_seconds = TimeLoggerService().log_second_diff(start_time_seconds=start_time_seconds,
                                                        stop_time_seconds=stop_time_seconds, log_dir=self.log_dir)
        self.assertTrue(os.path.exists(time_period_log_path))

    def test_log_once(self):
        time_seconds = TimeLoggerService().log(log_dir=self.log_dir)
        time_log_path = os.path.join(self.log_dir, str(time_seconds) + ".log")
        self.assertTrue(os.path.exists(time_log_path))

    def test_log_second_diff(self):
        start_time_seconds = 100
        stop_time_seconds = 1000000
        diff_seconds = TimeLoggerService().log_second_diff(start_time_seconds=start_time_seconds,
                                                        stop_time_seconds=stop_time_seconds, log_dir=self.log_dir)
        self.assertEqual(stop_time_seconds - start_time_seconds, diff_seconds)
