import json
import os

from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class AIGuideHTMLLogTargetPagePort(ITargetPagePort):
    def __init__(self, folder_path: str):
        super().__init__()
        self._folder_path = folder_path

    def connect(self):
        pass

    def close(self):
        pass

    def wait_for_target_page(self):
        target_page_paths = self._get_all_file_path_in_folder(self._folder_path)
        for path in target_page_paths:
            if ".html" in path:
                folder_path, pageHTMLFileName = os.path.split(path)
                page_json_file_name = os.path.splitext(
                    pageHTMLFileName)[0] + ".json"
                json_data = open(os.path.join(folder_path, page_json_file_name),)
                page_log = json.load(json_data)
                json_data.close()
                self._add_target_page(
                    target_page_url=path,
                    root_url=path,
                    form_xpath=page_log["formXPath"],
                    app_event_dt_os=[])

    def _add_target_page(self, target_page_url: str, root_url: str,
                       form_xpath: str, app_event_dt_os: [AppEventDTO]):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase()
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            form_xpath=form_xpath,
                                                                            app_event_dt_os=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

    def _get_all_file_path_in_folder(self, targetFolderPath: str):
        files_path = []
        for dir_path, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                files_path.append(dir_path + "/" + file)
        return files_path
