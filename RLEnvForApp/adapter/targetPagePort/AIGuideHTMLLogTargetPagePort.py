import json
import os

from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput, CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class AIGuideHTMLLogTargetPagePort(ITargetPagePort):
    def __init__(self, folderPath: str):
        super().__init__()
        self._folder_path = folderPath

    def connect(self):
        pass

    def close(self):
        pass

    def waitForTargetPage(self):
        target_page_paths = self._getAllFilePathInFolder(self._folder_path)
        for path in target_page_paths:
            if ".html" in path:
                folder_path, page_html_file_name = os.path.split(path)
                page_json_file_name = os.path.splitext(page_html_file_name)[0] + ".json"
                json_data = open(os.path.join(folder_path, page_json_file_name),)
                page_log = json.load(json_data)
                json_data.close()
                self._add_target_page(target_page_url=path, root_url=path,
                                      form_xpath=page_log["formXPath"],
                                      appEventDTOs=[])

    @staticmethod
    def _add_target_page(target_page_url: str, root_url: str, form_xpath: str, appEventDTOs: [AppEventDTO]):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase()
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=target_page_url,
                                                                               rootUrl=root_url,
                                                                               formXPath=form_xpath,
                                                                               appEventDTOs=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(create_target_page_input, create_target_page_output)

    @staticmethod
    def _getAllFilePathInFolder(target_folder_path: str):
        files_path = []
        for dir_path, dir_names, file_names in os.walk(target_folder_path):
            for file in file_names:
                files_path.append(dir_path + "/" + file)
        return files_path
