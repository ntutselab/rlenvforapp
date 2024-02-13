import os
import time


class TimeLoggerService:
    def __init__(self):
        pass

    def log_start(self, log_dir):
        start_time_seconds = time.time()
        time_stamp = time.ctime(start_time_seconds)

        save_path = os.path.join(log_dir, "startTime.log")
        saved_content = "Start Time: " + str(time_stamp) + \
            "\nStart Time(seconds): " + str(start_time_seconds) + "\n"
        self._write_file(path=save_path, content=saved_content)
        return start_time_seconds

    def log_stop(self, log_dir):
        stop_time_seconds = time.time()
        time_stamp = time.ctime(stop_time_seconds)

        save_path = os.path.join(log_dir, "stopTime.log")
        saved_content = "Stop Time: " + str(time_stamp) + \
            "\nStop Time(seconds): " + str(stop_time_seconds) + "\n"
        self._write_file(path=save_path, content=saved_content)
        return stop_time_seconds

    def log(self, log_dir):
        time_seconds = time.time()
        time_stamp = time.ctime(time_seconds)

        save_path = os.path.join(log_dir, str(time_seconds) + ".log")
        saved_content = "Log Time: " + str(time_stamp) + \
            "\nLog Time(seconds): " + str(time_seconds) + "\n"
        self._write_file(path=save_path, content=saved_content)
        return time_seconds

    def log_second_diff(self, start_time_seconds, stop_time_seconds, log_dir):
        diff_seconds = stop_time_seconds - start_time_seconds
        start_time = time.localtime(start_time_seconds)
        stop_time = time.localtime(stop_time_seconds)

        save_path = os.path.join(log_dir, "timePeriod.log")
        saved_content = "Start Time: " + str(start_time) + \
            "\nStop Time: " + str(stop_time) + "\nTime Period: "
        saved_content = saved_content + self._get_format_time(diff_seconds)
        self._write_file(path=save_path, content=saved_content)
        return diff_seconds

    def _write_file(self, path: str, content: str):
        saved_file = open(path, "w")
        saved_file.write(content)
        saved_file.close()

    def _get_format_time(self, time_seconds):
        days = time_seconds / 86400
        hours = (time_seconds % 86400) / 3600
        minutes = (time_seconds % 3600) / 60
        seconds = time_seconds % 60
        return str(int(days)) + " day(s) " + str(int(hours)) + " hour(s) " + \
            str(int(minutes)) + " min(s) " + str(int(seconds)) + " sec(s)"
