import json
import os

from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get import (GetAllTargetPageInput,
                                                GetAllTargetPageOutput,
                                                GetAllTargetPageUseCase)


class AIGuideVerifyTargetPagePort(ITargetPagePort):
    def __init__(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int,
                 serverName: str, root_url: str = "127.0.0.1", code_coverage_type: str = "coverage"):
        super().__init__()
        self._folder_path = "htmlSet/LEARNING_TASK"
        self._java_ip = javaIp
        self._python_ip = pythonIp
        self._java_port = javaPort
        self._python_port = pythonPort
        self._root_url = root_url
        self._code_coverage_type = code_coverage_type
        self._java_object_py4_j_learning_pool = None
        self._java_object_learning_task_dt_os = []
        self._server_name = serverName

    def connect(self):
        pass

    def close(self):
        pass

    def wait_for_target_page(self):
        self.pull_target_page()

    def pull_target_page(self):
        while len(self._get_all_target_page_dto()) == 0:
            target_page_paths = self._get_all_file_path_in_folder(self._folder_path)
            for path in target_page_paths:
                if ".json" in path:
                    folder_path, pageHTMLFileName = os.path.split(path)
                    page_json_file_name = os.path.splitext(
                        pageHTMLFileName)[0] + ".json"
                    json_data = open(
                        os.path.join(
                            folder_path,
                            page_json_file_name),
                    )
                    page_log = json.load(json_data)
                    json_data.close()
                    page_log = page_log[0]
                    formXpath = page_log["formXPaths"][0]
                    app_event_dt_os = []
                    for actionSequence in page_log["actionSequence"]:
                        for app_event in actionSequence:
                            app_event_dto = AppEventDTO(xpath=app_event["xpath"],
                                                      value=app_event["value"], category="")
                            app_event_dt_os.append(app_event_dto)

                    self._add_target_page(target_page_url=page_log["targetURL"], root_url=self._root_url, form_xpath=formXpath,
                                        app_event_dt_os=app_event_dt_os, stateID=page_log["stateID"],
                                        code_coverage_vector=None)

    def _get_all_target_page_dto(self) -> [TargetPageDTO]:
        get_all_target_page_use_case = GetAllTargetPageUseCase.GetAllTargetPageUseCase()
        get_all_target_page_input = GetAllTargetPageInput.GetAllTargetPageInput()
        get_all_target_page_output = GetAllTargetPageOutput.GetAllTargetPageOutput()

        get_all_target_page_use_case.execute(
            input=get_all_target_page_input,
            output=get_all_target_page_output)
        return get_all_target_page_output.get_target_page_dt_os()

    def _add_target_page(self, target_page_url: str, root_url: str, app_event_dt_os: [AppEventDTO], stateID: str = "",
                       form_xpath: str = "", code_coverage_vector: CodeCoverageDTO = None):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase()
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            app_event_dt_os=app_event_dt_os,
                                                                            task_id=stateID,
                                                                            form_xpath=form_xpath,
                                                                            basic_code_coverage=code_coverage_vector)
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

    def _get_all_file_path_in_folder(self, targetFolderPath: str):
        files_path = []
        for dir_path, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                files_path.append(dir_path + "/" + file)
        return files_path
