import os
import unittest

from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager


class testFileManager(unittest.TestCase):
    def test_create_folder(self):
        file_manager = FileManager()
        file_manager.create_folder("htmlSet", "GUIDE_HTML_SET")

    def test_create_file(self):
        file_manager = FileManager()
        file_manager.create_folder("htmlSet", "GUIDE_HTML_SET")
        file_manager.create_file(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            file_name="test.html",
            context="aabbcc")
