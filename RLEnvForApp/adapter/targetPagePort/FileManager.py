import os

from RLEnvForApp.logger.logger import Logger


class FileManager:
    def __init__(self):
        pass

    def create_folder(self, folder_path, folderName):
        path = os.path.join(folder_path, folderName)
        if os.path.isdir(path):
            Logger().info("%s directory already exist" % path)
            return
        try:
            os.makedirs(path)
        except OSError:
            Logger().info("Creation of the directory %s failed" % path)
        else:
            Logger().info("Successfully created the directory %s " % path)

    def create_file(self, path: str, file_name: str, context: str):
        file_path = os.path.join(path, file_name)
        file = open(file_path, "w", encoding='utf-8')
        file.write(str(context))
        file.close()
