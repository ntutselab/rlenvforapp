import os

from RLEnvForApp.logger.logger import Logger


class FileManager:
    def __init__(self):
        pass

    def create_folder(self, folderPath, folderName):
        path = os.path.join(folderPath, folderName)
        if os.path.isdir(path):
            Logger().info("%s directory already exist" % path)
            return
        try:
            os.makedirs(path)
        except OSError:
            Logger().info("Creation of the directory %s failed" % path)
        else:
            Logger().info("Successfully created the directory %s " % path)

    def create_file(self, path: str, fileName: str, context: str):
        filePath = os.path.join(path, fileName)
        f = open(filePath, "w", encoding='utf-8')
        f.write(str(context))
        f.close()
