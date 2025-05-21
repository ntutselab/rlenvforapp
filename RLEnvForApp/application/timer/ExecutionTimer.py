import time

class ExecutionTimer:
    _instance = None

    def __init__(self):
        if ExecutionTimer._instance is not None:
            raise Exception("Use get_instance() instead of instantiating directly")
        self.total_time = 0
        self.start_time = None
        self.durations = []
        ExecutionTimer._instance = self

    @classmethod
    def init_instance(cls):
        """用於首次初始化（只在爬行開始時調用）"""
        if cls._instance is None:
            cls._instance = ExecutionTimer()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise Exception("ExecutionTimer has not been initialized. Call init_instance() first.")
        return cls._instance

    def start(self):
        self.start_time = time.time()

    def stop_and_accumulate(self):
        if self.start_time is None:
            raise Exception("Timer not started")
        duration = time.time() - self.start_time
        self.durations.append(duration)
        self.total_time += duration
        self.start_time = None
        return duration

    def get_total_time(self):
        return self.total_time
    
    def get_summary(self):
        return {
            "total_time": self.total_time,
            "count": len(self.durations),
            "avg": self.total_time / len(self.durations) if self.durations else 0
        }