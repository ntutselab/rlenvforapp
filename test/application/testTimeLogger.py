import os
import time
import unittest

from RLEnvForApp.application.timeLoggerService.TimeLoggerService import \
    TimeLoggerService


class testTimeLogger(unittest.TestCase):
    def setUp(self) -> None:
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

    def tearDown(self) -> None:
        pass

    def testPeriodLog(self):
        timePassedSeconds = 1

        startTimeSeconds = TimeLoggerService().logStart(logDir=self.logDir)
        time.sleep(timePassedSeconds)
        stopTimeSeconds = TimeLoggerService().logStop(logDir=self.logDir)

        self.assertGreaterEqual(stopTimeSeconds - startTimeSeconds, timePassedSeconds)
        startTimeLogPath = os.path.join(self.logDir, self.startTimeFileName)
        stopTimeLogPath = os.path.join(self.logDir, self.stopTimeFileName)
        self.assertTrue(os.path.exists(startTimeLogPath))
        self.assertTrue(os.path.exists(stopTimeLogPath))

        timePeriodLogPath = os.path.join(self.logDir, self.timePeriodFileName)
        diffSeconds = TimeLoggerService().logSecondDiff(startTimeSeconds=startTimeSeconds,
                                                        stopTimeSeconds=stopTimeSeconds, logDir=self.logDir)
        self.assertTrue(os.path.exists(timePeriodLogPath))

    def testLogOnce(self):
        timeSeconds = TimeLoggerService().log(logDir=self.logDir)
        timeLogPath = os.path.join(self.logDir, str(timeSeconds) + ".log")
        self.assertTrue(os.path.exists(timeLogPath))

    def testLogSecondDiff(self):
        startTimeSeconds = 100
        stopTimeSeconds = 1000000
        diffSeconds = TimeLoggerService().logSecondDiff(startTimeSeconds=startTimeSeconds,
                                                        stopTimeSeconds=stopTimeSeconds, logDir=self.logDir)
        self.assertEqual(stopTimeSeconds - startTimeSeconds, diffSeconds)
