import os

from RLEnvForApp.logger.logger import Logger


class FileManager:
    def __init__(self):
        pass

    def createFolder(self, folderPath, folderName):
        path = os.path.join(folderPath, folderName)
        if os.path.isdir(path):
            Logger().info(f"{path} directory already exist")
            return
        try:
            os.makedirs(path)
        except OSError:
            Logger().info(f"Creation of the directory {path} failed")
        else:
            Logger().info(f"Successfully created the directory {path} ")

    def createFile(self, path: str, fileName: str, context: str):
        filePath = os.path.join(path, fileName)
        file = open(filePath, "w", encoding='utf-8')
        file.write(str(context))
        file.close()
