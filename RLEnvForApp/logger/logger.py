import logging
import os
import sys


class Logger:
    _instance = None

    def __new__(cls, fileName="AIGuideEnv.log"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # ✅ 確保資料夾存在
            log_dir = "./executionSummary"
            os.makedirs(log_dir, exist_ok=True)

            # ✅ 處理空檔名
            if not fileName or fileName == ".log":
                fileName = "default.log"
            aiGuideLogger = logging.getLogger(fileName)

            logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,
                                datefmt='%Y-%m-%d %H:%M:%S')

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))

            fileHandler = logging.FileHandler(mode='a', filename=f"./executionSummary/{fileName}", encoding="utf-8")
            fileHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
            fileHandler.setLevel(logging.INFO)

            # sys.stdout.reconfigure(encoding='utf-8')

            aiGuideLogger.addHandler(console)
            aiGuideLogger.addHandler(fileHandler)

            cls._instance.logger = aiGuideLogger
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def info(self, message):
        self.logger.info(message)

    def exception(self, message):
        self.logger.exception(message)
