import os
import time


class TimeLoggerService:
    def __init__(self):
        pass

    def logStart(self, logDir):
        startTimeSeconds = time.time()
        timeStamp = time.ctime(startTimeSeconds)

        savePath = os.path.join(logDir, "startTime.log")
        savedContent = "Start Time: " + str(timeStamp) + \
            "\nStart Time(seconds): " + str(startTimeSeconds) + "\n"
        self._writeFile(path=savePath, content=savedContent)
        return startTimeSeconds

    def logStop(self, logDir):
        stopTimeSeconds = time.time()
        timeStamp = time.ctime(stopTimeSeconds)

        savePath = os.path.join(logDir, "stopTime.log")
        savedContent = "Stop Time: " + str(timeStamp) + \
            "\nStop Time(seconds): " + str(stopTimeSeconds) + "\n"
        self._writeFile(path=savePath, content=savedContent)
        return stopTimeSeconds

    def log(self, logDir):
        timeSeconds = time.time()
        timeStamp = time.ctime(timeSeconds)

        savePath = os.path.join(logDir, str(timeSeconds) + ".log")
        savedContent = "Log Time: " + str(timeStamp) + \
            "\nLog Time(seconds): " + str(timeSeconds) + "\n"
        self._writeFile(path=savePath, content=savedContent)
        return timeSeconds

    def logSecondDiff(self, startTimeSeconds, stopTimeSeconds, logDir):
        diffSeconds = stopTimeSeconds - startTimeSeconds
        startTime = time.localtime(startTimeSeconds)
        stopTime = time.localtime(stopTimeSeconds)

        savePath = os.path.join(logDir, "timePeriod.log")
        savedContent = "Start Time: " + str(startTime) + \
            "\nStop Time: " + str(stopTime) + "\nTime Period: "
        savedContent = savedContent + self._getFormatTime(diffSeconds)
        self._writeFile(path=savePath, content=savedContent)
        return diffSeconds

    def _writeFile(self, path: str, content: str):
        savedFile = open(path, "w")
        savedFile.write(content)
        savedFile.close()

    def _getFormatTime(self, timeSeconds):
        days = timeSeconds / 86400
        hours = (timeSeconds % 86400) / 3600
        minutes = (timeSeconds % 3600) / 60
        seconds = timeSeconds % 60
        return str(int(days)) + " day(s) " + str(int(hours)) + " hour(s) " + str(int(minutes)) + " min(s) " + str(int(seconds)) + " sec(s)"
