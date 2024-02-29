import logging


class Logger:
    _instance = None

    def __new__(cls, fileName="AIGuideEnv.log"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            aiGuideLogger = logging.getLogger(fileName)

            logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG,
                                datefmt='%Y-%m-%d %H:%M:%S')

            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            console.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))

            fileHandler = logging.FileHandler(mode='w', filename=fileName)
            fileHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
            fileHandler.setLevel(logging.INFO)

            aiGuideLogger.addHandler(console)
            aiGuideLogger.addHandler(fileHandler)

            cls._instance.logger = aiGuideLogger
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance

    def info(self, message):
        self.get_instance().info(message)

    def exception(self, message):
        self.get_instance().exception(message)
