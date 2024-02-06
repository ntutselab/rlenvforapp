import os
import unittest

from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager


class testFileManager(unittest.TestCase):
    def test_create_folder(self):
        fileManager = FileManager()
        fileManager.createFolder("htmlSet", "GUIDE_HTML_SET")


    def test_create_file(self):
        fileManager = FileManager()
        fileManager.createFolder("htmlSet", "GUIDE_HTML_SET")
        fileManager.createFile(path=os.path.join("htmlSet", "GUIDE_HTML_SET"), fileName="test.html", context="aabbcc")
