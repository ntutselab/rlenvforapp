import json
import os
import re
import time
from urllib.parse import urlparse

from dependency_injector.wiring import inject
from py4j.java_gateway import (CallbackServerParameters, GatewayParameters,
                               JavaGateway)

from RLEnvForApp.adapter.targetPagePort.FileManager import FileManager
from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.domain.environment.inputSpace import (ValueWeightSingleton,
                                                       inputTypes, inputValues)
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.episodeHandler.get import (
    GetEpisodeHandlerInput, GetEpisodeHandlerOutput, GetEpisodeHandlerUseCase)
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveInput,
                                                   CreateDirectiveOutput,
                                                   CreateDirectiveUseCase,
                                                   CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get import (GetAllTargetPageInput,
                                                GetAllTargetPageOutput,
                                                GetAllTargetPageUseCase,
                                                GetTargetPageInput,
                                                GetTargetPageOutput,
                                                GetTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.remove import (RemoveTargetPageInput,
                                                   RemoveTargetPageOutput,
                                                   RemoveTargetPageUseCase)


class AIGuideTargetPagePort(ITargetPagePort):
    @inject
    def __init__(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int,
                 serverName: str, root_url: str = "127.0.0.1", code_coverage_type: str = "coverage"):
        super().__init__()
        self._java_ip = javaIp
        self._python_ip = pythonIp
        self._java_port = javaPort
        self._python_port = pythonPort
        self._root_url = root_url
        self._code_coverage_type = code_coverage_type
        self._java_object_py4_j_learning_pool = None
        self._java_object_learning_task_dt_os = []
        self._server_name = serverName
        self._is_training = True

    def connect(self):
        gateway_parameters = GatewayParameters(
            address=self._java_ip, port=self._java_port)
        callback_server_parameters = CallbackServerParameters(
            address=self._python_ip, port=self._python_port)
        self._java_object_py4_j_learning_pool = JavaGateway(gateway_parameters=gateway_parameters,
                                                       callback_server_parameters=callback_server_parameters)

    def close(self):
        self._java_object_py4_j_learning_pool.setAgentDone(True)
        self._java_object_py4_j_learning_pool.shutdown()

    def wait_for_target_page(self):
        Logger().info("Waiting for target page")
        while (self._java_object_py4_j_learning_pool.isLearningTaskDTOQueueEmpty()):
            time.sleep(1)
        self.pull_target_page()

    def pull_target_page(self):
        is_first = True
        while len(self._get_all_target_page_dto()) == 0 or is_first:
            while not (
                    self._java_object_py4_j_learning_pool.isLearningTaskDTOQueueEmpty()):
                java_object_learning_task_dto = self._java_object_py4_j_learning_pool.deQueueLearningTaskDTO()
                url = java_object_learning_task_dto.getTargetURL()
                stateID = java_object_learning_task_dto.getStateID()
                formXPaths = java_object_learning_task_dto.getFormXPaths()

                app_event_dt_os = []
                for javaObjectHighLevelActionDTO in java_object_learning_task_dto.getHighLevelActionDTOList():
                    for javaObjectActionDTO in javaObjectHighLevelActionDTO.getActionDTOList():
                        app_event_dto = AppEventDTO(
                            xpath=javaObjectActionDTO.get_xpath(),
                            value=javaObjectActionDTO.get_value(),
                            category="")
                        app_event_dt_os.append(app_event_dto)

                code_coverage_vector = []
                for i in java_object_learning_task_dto.get_code_coverage_vector():
                    code_coverage_vector.append(i)
                code_coverage_dto = self._create_code_coverage_dto(
                    code_coverage_type=self._code_coverage_type,
                    code_coverage_vector=java_object_learning_task_dto.get_code_coverage_vector())
                if not self._have_same_task_id(task_id=stateID):
                    # support for filling out multiple forms
                    for form_x_path in formXPaths:
                        self._add_target_page(
                            target_page_url=url,
                            root_url=self._root_url,
                            app_event_dt_os=app_event_dt_os,
                            stateID=stateID,
                            form_x_path=form_x_path,
                            code_coverage_vector=code_coverage_dto)
                    # support for filling in single form
                    # self._addTargetPage(targetPageUrl=url, rootUrl=self._rootUrl, appEventDTOs=appEventDTOs,
                    # stateID=stateID, formXPath="//form",
                    # codeCoverageVector=codeCoverageDTO)
                    self._java_object_learning_task_dt_os.append(
                        java_object_learning_task_dto)
            is_first = False

    def push_target_page(self, target_page_id: str, episode_handler_id: str):
        directive_dto = self._create_directive(
            target_page_id=target_page_id,
            episode_handler_id=episode_handler_id)
        target_page_dto: TargetPageDTO = self._get_target_page(
            target_page_id=target_page_id)

        self._java_object_py4_j_learning_pool.enQueueLearningResultDTO(
            self._create_java_object_learning_result_dto(
                taskId=target_page_dto.get_task_id(), directive_dto=directive_dto))
        self._save_target_page_to_html_set(
            episode_handler_id=episode_handler_id,
            directive_dto=directive_dto)
        if not self._is_training:
            self._remove_target_page(target_page_id=target_page_id)

    def get_pause_agent(self):
        return self._java_object_py4_j_learning_pool.get_pause_agent()

    def set_pause_agent(self, isPauseAgent: bool):
        self._java_object_py4_j_learning_pool.set_pause_agent(isPauseAgent)

    def _add_target_page(self, target_page_url: str, root_url: str, app_event_dt_os: [AppEventDTO], stateID: str = "",
                       form_x_path: str = "", code_coverage_vector: CodeCoverageDTO = None):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase()
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            app_event_dt_os=app_event_dt_os,
                                                                            task_id=stateID,
                                                                            form_x_path=form_x_path,
                                                                            basic_code_coverage=code_coverage_vector)
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

    def _get_all_target_page_dto(self) -> [TargetPageDTO]:
        get_all_target_page_use_case = GetAllTargetPageUseCase.GetAllTargetPageUseCase()
        get_all_target_page_input = GetAllTargetPageInput.GetAllTargetPageInput()
        get_all_target_page_output = GetAllTargetPageOutput.GetAllTargetPageOutput()

        get_all_target_page_use_case.execute(
            input=get_all_target_page_input,
            output=get_all_target_page_output)
        return get_all_target_page_output.get_target_page_dt_os()

    def _remove_target_page(self, target_page_id: str):
        remove_target_page_use_case = RemoveTargetPageUseCase.RemoveTargetPageUseCase()
        remove_target_page_input = RemoveTargetPageInput.RemoveTargetPageInput(
            target_page_id=target_page_id)
        remove_target_page_output = RemoveTargetPageOutput.RemoveTargetPageOutput()

        remove_target_page_use_case.execute(
            input=remove_target_page_input,
            output=remove_target_page_output)

    def _create_code_coverage_dto(
            self, code_coverage_type: str, code_coverage_vector: [bool]):
        return CodeCoverageDTO(code_coverage_type=code_coverage_type,
                               code_coverage_vector=code_coverage_vector)

    def _get_target_page(self, target_page_id: str):
        get_target_page_use_case = GetTargetPageUseCase.GetTargetPageUseCase()
        get_target_page_input = GetTargetPageInput.GetTargetPageInput(
            target_page_id=target_page_id)
        get_target_page_output = GetTargetPageOutput.GetTargetPageOutput()

        get_target_page_use_case.execute(
            input=get_target_page_input,
            output=get_target_page_output)
        return get_target_page_output.get_target_page_dto()

    def _create_directive(self, target_page_id: str, episode_handler_id: str):
        create_directive_use_case = CreateDirectiveUseCase.CreateDirectiveUseCase()
        create_directive_input = CreateDirectiveInput.CreateDirectiveInput(
            target_page_id=target_page_id, episode_handler_id=episode_handler_id)
        create_directive_output = CreateDirectiveOutput.CreateDirectiveOutput()
        create_directive_use_case.execute(
            create_directive_input, create_directive_output)

        return create_directive_output.get_directive_dto()

    def _get_episode_handler_dto(
            self, episode_handler_id: str) -> EpisodeHandlerDTO:
        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase()
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(
            episode_handler_id=episode_handler_id)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        return output.get_episode_handler_dto()

    def _find_java_object_learning_task_dto_by_task_id(self, stateID: str):
        for java_object_learning_task_dto in self._java_object_learning_task_dt_os:
            if java_object_learning_task_dto.getStateID() == stateID:
                return java_object_learning_task_dto

    def _create_java_object_high_level_actions(self, app_event_dt_os: [AppEventDTO]):
        high_level_action_dt_os = []
        high_level_action_dt_os.append([])
        for app_event in app_event_dt_os:
            if app_event.get_value() == "":
                high_level_action_dt_os.append([app_event])
                high_level_action_dt_os.append([])
            else:
                high_level_action_dt_os[len(
                    high_level_action_dt_os) - 1].append(app_event)

        java_object_high_level_action_dt_os = []
        for highLevelActionDTO in high_level_action_dt_os:
            if len(highLevelActionDTO) == 0:
                continue
            java_object_high_level_action_dto_builder = self._getjava_object_high_level_action_dto_builder()
            for app_event in highLevelActionDTO:
                java_object_high_level_action_dto_builder.appendActionDTO(self._get_crawljax_xpath(xpath=app_event.get_xpath()),
                                                                    app_event.get_value())
            java_object_high_level_action_dt_os.append(
                java_object_high_level_action_dto_builder.build())

        return java_object_high_level_action_dt_os

    def _getjava_object_high_level_action_dto_builder(self):
        java_object_high_level_action_dto_builder = self._java_object_py4_j_learning_pool.getHighLevelActionDTOBuilder()
        java_object_high_level_action_dto_builder.setActionDTOList()
        return java_object_high_level_action_dto_builder

    def _get_code_coverage_dto_by_type(self, code_coverage_dt_os: [
                                  CodeCoverageDTO], type: str):
        for code_coverage_dto in code_coverage_dt_os:
            if code_coverage_dto.get_code_coverage_type() == type:
                return code_coverage_dto

    def _get_crawljax_xpath(self, xpath: str):
        crawljax_xpath = ""
        for i in xpath.upper().split("/"):
            if not re.match(".*\\[\\d*\\]", i) and not i == "":
                i += "[1]/"
            else:
                i += "/"

            crawljax_xpath += i
        return crawljax_xpath[:len(crawljax_xpath) - 1]

    def _create_java_object_learning_result_dto(
            self, taskId: str, directive_dto: DirectiveDTO):
        java_object_learning_task_dto = self._find_java_object_learning_task_dto_by_task_id(
            taskId)
        java_object_high_level_action_dt_os = self._create_java_object_high_level_actions(
            app_event_dt_os=directive_dto.get_app_event_dt_os())

        # build learning result
        java_object_learning_result_dto_builder = self._java_object_py4_j_learning_pool.getLearnResultDTOBuilder()
        # set high level action
        java_object_learning_result_dto_builder.setHighLevelActionDTOList()
        for javaObjectHighLevelActionDTO in java_object_high_level_action_dt_os:
            java_object_learning_result_dto_builder.appendHighLevelActionDTOList(
                javaObjectHighLevelActionDTO)
        # set task id
        java_object_learning_result_dto_builder.set_task_id(
            java_object_learning_task_dto.getStateID())
        java_object_learning_result_dto_builder.set_form_x_path(
            directive_dto.get_form_x_path())
        # set code coverage
        code_coverage_dto = self._get_code_coverage_dto_by_type(code_coverage_dt_os=directive_dto.get_code_coverage_dt_os(),
                                                         type="statement coverage")
        code_coverage_vector = code_coverage_dto.get_code_coverage_vector()
        code_coverage_vector_size = len(code_coverage_vector)
        java_object_array = self._java_object_py4_j_learning_pool.new_array(
            self._java_object_py4_j_learning_pool.jvm.boolean, code_coverage_vector_size)
        for i in range(0, code_coverage_vector_size):
            java_object_array[i] = code_coverage_vector[i]
        java_object_learning_result_dto_builder.setCodeCoverageVector(
            java_object_array)
        # set original code coverage
        java_object_learning_result_dto_builder.setOriginalCodeCoverageVector(
            java_object_learning_task_dto.get_code_coverage_vector())
        java_object_learning_result_dto_builder.setDone(False)
        return java_object_learning_result_dto_builder.build()

    def _save_target_page_to_html_set(
            self, episode_handler_id: str, directive_dto: DirectiveDTO):
        file_name = f"{self._serverName}_{urlparse( directiveDTO.getUrl()).path.replace( '/', '_')}_{directiveDTO.getFormXPath().replace( '/', '_')}"
        initial_state_dto: StateDTO = self._get_episode_handler_dto(
            episode_handler_id=episode_handler_id).get_state_dt_os()[0]

        interactive_app_element_dictionary = []
        directive_dictionary = {}
        for app_event_dto in directive_dto.get_app_event_dt_os():
            directive_dictionary[app_event_dto.get_xpath()] = {
                "value": app_event_dto.get_value(), "category": app_event_dto.get_category()}
        for app_element_dto in initial_state_dto.get_selected_app_element_dt_os():
            interactive_app_element_dictionary.append(app_element_dto.get_xpath())
        form_x_path = directive_dto.get_form_x_path()
        directive_log_json = json.dumps(
            {
                "interactive_appElement": interactive_app_element_dictionary,
                "appEvent": directive_dictionary,
                "formXPath": form_x_path})

        self._update_input_value_weights(directive_dictionary)

        Logger().info(
            f"Save html set:\n{fileName}\n{formXPath}\n{directiveDictionary}")

        file_manager = FileManager()
        file_manager.create_folder("htmlSet", "GUIDE_HTML_SET")
        file_manager.create_file(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            file_name=file_name + ".html",
            context=directive_dto.get_dom())
        file_manager.create_file(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            file_name=file_name + ".json",
            context=directive_log_json)

    def _have_same_url(self, url: str):
        target_page_dt_os = self._get_all_target_page_dto()
        for target_page_dto in target_page_dt_os:
            if target_page_dto.get_target_url() == url:
                return True
        return False

    def _have_same_task_id(self, task_id: str):
        target_page_dt_os = self._get_all_target_page_dto()
        for target_page_dto in target_page_dt_os:
            if target_page_dto.get_task_id() == task_id:
                return True
        return False

    def _update_input_value_weights(self, app_event):
        input_value_weights = ValueWeightSingleton.get_instance().get_value_weights()

        for xpath, event in app_event.items():
            category = event["category"]
            value = event["value"]
            categoryIndex = inputTypes.index(category)
            if value in inputValues[categoryIndex]:
                indexOfValue = inputValues[categoryIndex].index(value)
                input_value_weights[category][indexOfValue] *= 10
                Logger().info(
                    f"Update inputValueWeight: {category} [{value}] {inputValueWeights[category][indexOfValue]}")
                input_value_weights[category] = [float(weight) / sum(input_value_weights[category]) for weight
                                               in input_value_weights[category]]

        ValueWeightSingleton.get_instance().set_value_weights(input_value_weights)
