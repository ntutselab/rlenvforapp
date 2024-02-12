import os
import time
import unittest

from RLEnvForApp.application.timeLoggerService.TimeLoggerService import \
    TimeLoggerService


class testTimeLogger(unittest.TestCase):
    def set_up(self) -> None:
        self.logDir = "model/timeLoggerTest/"

        self.startTimeFileName = "startTime.log"
        startTimeLogPath = os.path.join(self.logDir, self.startTimeFileName)
        if os.path.exists(startTimeLogPath):
            os.remove(startTimeLogPath)

        self.stopTimeFileName = "stopTime.log"
        stopTimeLogPath = os.path.join(self.logDir, self.stopTimeFileName)
        if os.path.exists(stopTimeLogPath):
            os.remove(stopTimeLogPath)

        self.timePeriodFileName = "timePeriod.log"
        timePeriodLogPath = os.path.join(self.logDir, self.timePeriodFileName)
        if os.path.exists(timePeriodLogPath):
            os.remove(timePeriodLogPath)

    def tear_down(self) -> None:
        pass

    def test_period_log(self):
        timePassedSeconds = 1

        startTimeSeconds = TimeLoggerService().log_start(logDir=self.logDir)
        time.sleep(timePassedSeconds)
        stopTimeSeconds = TimeLoggerService().log_stop(logDir=self.logDir)

        self.assertGreaterEqual(
            stopTimeSeconds -
            startTimeSeconds,
            timePassedSeconds)
        startTimeLogPath = os.path.join(self.logDir, self.startTimeFileName)
        stopTimeLogPath = os.path.join(self.logDir, self.stopTimeFileName)
        self.assertTrue(os.path.exists(startTimeLogPath))
        self.assertTrue(os.path.exists(stopTimeLogPath))

        timePeriodLogPath = os.path.join(self.logDir, self.timePeriodFileName)
        diffSeconds = TimeLoggerService().log_second_diff(startTimeSeconds=startTimeSeconds,
                                                        stopTimeSeconds=stopTimeSeconds, logDir=self.logDir)
        self.assertTrue(os.path.exists(timePeriodLogPath))

    def test_log_once(self):
        timeSeconds = TimeLoggerService().log(logDir=self.logDir)
        timeLogPath = os.path.join(self.logDir, str(timeSeconds) + ".log")
        self.assertTrue(os.path.exists(timeLogPath))

    def test_log_second_diff(self):
        startTimeSeconds = 100
        stopTimeSeconds = 1000000
        diffSeconds = TimeLoggerService().log_second_diff(startTimeSeconds=startTimeSeconds,
                                                        stopTimeSeconds=stopTimeSeconds, logDir=self.logDir)
        self.assertEqual(stopTimeSeconds - startTimeSeconds, diffSeconds)
