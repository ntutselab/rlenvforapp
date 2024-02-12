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
                 serverName: str, rootUrl: str = "127.0.0.1", codeCoverageType: str = "coverage"):
        super().__init__()
        self._javaIp = javaIp
        self._pythonIp = pythonIp
        self._javaPort = javaPort
        self._pythonPort = pythonPort
        self._rootUrl = rootUrl
        self._codeCoverageType = codeCoverageType
        self._javaObjectPy4JLearningPool = None
        self._javaObjectLearningTaskDTOs = []
        self._serverName = serverName
        self._isTraining = True

    def connect(self):
        gateway_parameters = GatewayParameters(
            address=self._javaIp, port=self._javaPort)
        callback_server_parameters = CallbackServerParameters(
            address=self._pythonIp, port=self._pythonPort)
        self._javaObjectPy4JLearningPool = JavaGateway(gateway_parameters=gateway_parameters,
                                                       callback_server_parameters=callback_server_parameters)

    def close(self):
        self._javaObjectPy4JLearningPool.setAgentDone(True)
        self._javaObjectPy4JLearningPool.shutdown()

    def wait_for_target_page(self):
        Logger().info("Waiting for target page")
        while (self._javaObjectPy4JLearningPool.isLearningTaskDTOQueueEmpty()):
            time.sleep(1)
        self.pull_target_page()

    def pull_target_page(self):
        isFirst = True
        while len(self._get_all_target_page_dto()) == 0 or isFirst:
            while not (
                    self._javaObjectPy4JLearningPool.isLearningTaskDTOQueueEmpty()):
                javaObjectLearningTaskDTO = self._javaObjectPy4JLearningPool.deQueueLearningTaskDTO()
                url = javaObjectLearningTaskDTO.getTargetURL()
                stateID = javaObjectLearningTaskDTO.getStateID()
                formXPaths = javaObjectLearningTaskDTO.getFormXPaths()

                appEventDTOs = []
                for javaObjectHighLevelActionDTO in javaObjectLearningTaskDTO.getHighLevelActionDTOList():
                    for javaObjectActionDTO in javaObjectHighLevelActionDTO.getActionDTOList():
                        appEventDTO = AppEventDTO(
                            xpath=javaObjectActionDTO.get_xpath(),
                            value=javaObjectActionDTO.get_value(),
                            category="")
                        appEventDTOs.append(appEventDTO)

                codeCoverageVector = []
                for i in javaObjectLearningTaskDTO.get_code_coverage_vector():
                    codeCoverageVector.append(i)
                codeCoverageDTO = self._create_code_coverage_dto(
                    codeCoverageType=self._codeCoverageType,
                    codeCoverageVector=javaObjectLearningTaskDTO.get_code_coverage_vector())
                if not self._have_same_task_id(taskID=stateID):
                    # support for filling out multiple forms
                    for formXPath in formXPaths:
                        self._add_target_page(
                            targetPageUrl=url,
                            rootUrl=self._rootUrl,
                            appEventDTOs=appEventDTOs,
                            stateID=stateID,
                            formXPath=formXPath,
                            codeCoverageVector=codeCoverageDTO)
                    # support for filling in single form
                    # self._addTargetPage(targetPageUrl=url, rootUrl=self._rootUrl, appEventDTOs=appEventDTOs,
                    # stateID=stateID, formXPath="//form",
                    # codeCoverageVector=codeCoverageDTO)
                    self._javaObjectLearningTaskDTOs.append(
                        javaObjectLearningTaskDTO)
            isFirst = False

    def push_target_page(self, targetPageId: str, episodeHandlerId: str):
        directiveDTO = self._create_directive(
            targetPageId=targetPageId,
            episodeHandlerId=episodeHandlerId)
        targetPageDTO: TargetPageDTO = self._get_target_page(
            targetPageId=targetPageId)

        self._javaObjectPy4JLearningPool.enQueueLearningResultDTO(
            self._create_java_object_learning_result_dto(
                taskId=targetPageDTO.get_task_id(), directiveDTO=directiveDTO))
        self._save_target_page_to_html_set(
            episodeHandlerId=episodeHandlerId,
            directiveDTO=directiveDTO)
        if not self._isTraining:
            self._remove_target_page(targetPageId=targetPageId)

    def get_pause_agent(self):
        return self._javaObjectPy4JLearningPool.get_pause_agent()

    def set_pause_agent(self, isPauseAgent: bool):
        self._javaObjectPy4JLearningPool.set_pause_agent(isPauseAgent)

    def _add_target_page(self, targetPageUrl: str, rootUrl: str, appEventDTOs: [AppEventDTO], stateID: str = "",
                       formXPath: str = "", codeCoverageVector: CodeCoverageDTO = None):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase()
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=appEventDTOs,
                                                                            taskID=stateID,
                                                                            formXPath=formXPath,
                                                                            basicCodeCoverage=codeCoverageVector)
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

    def _get_all_target_page_dto(self) -> [TargetPageDTO]:
        getAllTargetPageUseCase = GetAllTargetPageUseCase.GetAllTargetPageUseCase()
        getAllTargetPageInput = GetAllTargetPageInput.GetAllTargetPageInput()
        getAllTargetPageOutput = GetAllTargetPageOutput.GetAllTargetPageOutput()

        getAllTargetPageUseCase.execute(
            input=getAllTargetPageInput,
            output=getAllTargetPageOutput)
        return getAllTargetPageOutput.get_target_page_dt_os()

    def _remove_target_page(self, targetPageId: str):
        removeTargetPageUseCase = RemoveTargetPageUseCase.RemoveTargetPageUseCase()
        removeTargetPageInput = RemoveTargetPageInput.RemoveTargetPageInput(
            targetPageId=targetPageId)
        removeTargetPageOutput = RemoveTargetPageOutput.RemoveTargetPageOutput()

        removeTargetPageUseCase.execute(
            input=removeTargetPageInput,
            output=removeTargetPageOutput)

    def _create_code_coverage_dto(
            self, codeCoverageType: str, codeCoverageVector: [bool]):
        return CodeCoverageDTO(codeCoverageType=codeCoverageType,
                               codeCoverageVector=codeCoverageVector)

    def _get_target_page(self, targetPageId: str):
        getTargetPageUseCase = GetTargetPageUseCase.GetTargetPageUseCase()
        getTargetPageInput = GetTargetPageInput.GetTargetPageInput(
            targetPageId=targetPageId)
        getTargetPageOutput = GetTargetPageOutput.GetTargetPageOutput()

        getTargetPageUseCase.execute(
            input=getTargetPageInput,
            output=getTargetPageOutput)
        return getTargetPageOutput.get_target_page_dto()

    def _create_directive(self, targetPageId: str, episodeHandlerId: str):
        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase()
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=targetPageId, episodeHandlerId=episodeHandlerId)
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(
            createDirectiveInput, createDirectiveOutput)

        return createDirectiveOutput.get_directive_dto()

    def _get_episode_handler_dto(
            self, episodeHandlerId: str) -> EpisodeHandlerDTO:
        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase()
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(
            episodeHandlerId=episodeHandlerId)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        return output.get_episode_handler_dto()

    def _find_java_object_learning_task_dto_by_task_id(self, stateID: str):
        for javaObjectLearningTaskDTO in self._javaObjectLearningTaskDTOs:
            if javaObjectLearningTaskDTO.getStateID() == stateID:
                return javaObjectLearningTaskDTO

    def _create_java_object_high_level_actions(self, appEventDTOs: [AppEventDTO]):
        highLevelActionDTOs = []
        highLevelActionDTOs.append([])
        for appEvent in appEventDTOs:
            if appEvent.get_value() == "":
                highLevelActionDTOs.append([appEvent])
                highLevelActionDTOs.append([])
            else:
                highLevelActionDTOs[len(
                    highLevelActionDTOs) - 1].append(appEvent)

        javaObjectHighLevelActionDTOs = []
        for highLevelActionDTO in highLevelActionDTOs:
            if len(highLevelActionDTO) == 0:
                continue
            javaObjectHighLevelActionDTOBuilder = self._getjava_object_high_level_action_dto_builder()
            for appEvent in highLevelActionDTO:
                javaObjectHighLevelActionDTOBuilder.appendActionDTO(self._get_crawljax_xpath(xpath=appEvent.get_xpath()),
                                                                    appEvent.get_value())
            javaObjectHighLevelActionDTOs.append(
                javaObjectHighLevelActionDTOBuilder.build())

        return javaObjectHighLevelActionDTOs

    def _getjava_object_high_level_action_dto_builder(self):
        javaObjectHighLevelActionDTOBuilder = self._javaObjectPy4JLearningPool.getHighLevelActionDTOBuilder()
        javaObjectHighLevelActionDTOBuilder.setActionDTOList()
        return javaObjectHighLevelActionDTOBuilder

    def _get_code_coverage_dto_by_type(self, codeCoverageDTOs: [
                                  CodeCoverageDTO], type: str):
        for codeCoverageDTO in codeCoverageDTOs:
            if codeCoverageDTO.get_code_coverage_type() == type:
                return codeCoverageDTO

    def _get_crawljax_xpath(self, xpath: str):
        crawljaxXpath = ""
        for i in xpath.upper().split("/"):
            if not re.match(".*\\[\\d*\\]", i) and not i == "":
                i += "[1]/"
            else:
                i += "/"

            crawljaxXpath += i
        return crawljaxXpath[:len(crawljaxXpath) - 1]

    def _create_java_object_learning_result_dto(
            self, taskId: str, directiveDTO: DirectiveDTO):
        javaObjectLearningTaskDTO = self._find_java_object_learning_task_dto_by_task_id(
            taskId)
        javaObjectHighLevelActionDTOs = self._create_java_object_high_level_actions(
            appEventDTOs=directiveDTO.get_app_event_dt_os())

        # build learning result
        javaObjectLearningResultDTOBuilder = self._javaObjectPy4JLearningPool.getLearnResultDTOBuilder()
        # set high level action
        javaObjectLearningResultDTOBuilder.setHighLevelActionDTOList()
        for javaObjectHighLevelActionDTO in javaObjectHighLevelActionDTOs:
            javaObjectLearningResultDTOBuilder.appendHighLevelActionDTOList(
                javaObjectHighLevelActionDTO)
        # set task id
        javaObjectLearningResultDTOBuilder.set_task_id(
            javaObjectLearningTaskDTO.getStateID())
        javaObjectLearningResultDTOBuilder.set_form_x_path(
            directiveDTO.get_form_x_path())
        # set code coverage
        codeCoverageDTO = self._get_code_coverage_dto_by_type(codeCoverageDTOs=directiveDTO.get_code_coverage_dt_os(),
                                                         type="statement coverage")
        codeCoverageVector = codeCoverageDTO.get_code_coverage_vector()
        codeCoverageVectorSize = len(codeCoverageVector)
        javaObjectArray = self._javaObjectPy4JLearningPool.new_array(
            self._javaObjectPy4JLearningPool.jvm.boolean, codeCoverageVectorSize)
        for i in range(0, codeCoverageVectorSize):
            javaObjectArray[i] = codeCoverageVector[i]
        javaObjectLearningResultDTOBuilder.setCodeCoverageVector(
            javaObjectArray)
        # set original code coverage
        javaObjectLearningResultDTOBuilder.setOriginalCodeCoverageVector(
            javaObjectLearningTaskDTO.get_code_coverage_vector())
        javaObjectLearningResultDTOBuilder.setDone(False)
        return javaObjectLearningResultDTOBuilder.build()

    def _save_target_page_to_html_set(
            self, episodeHandlerId: str, directiveDTO: DirectiveDTO):
        fileName = f"{self._serverName}_{urlparse( directiveDTO.getUrl()).path.replace( '/', '_')}_{directiveDTO.getFormXPath().replace( '/', '_')}"
        initialStateDTO: StateDTO = self._get_episode_handler_dto(
            episodeHandlerId=episodeHandlerId).get_state_dt_os()[0]

        interactiveAppElementDictionary = []
        directiveDictionary = {}
        for appEventDTO in directiveDTO.get_app_event_dt_os():
            directiveDictionary[appEventDTO.get_xpath()] = {
                "value": appEventDTO.get_value(), "category": appEventDTO.get_category()}
        for appElementDTO in initialStateDTO.get_selected_app_element_dt_os():
            interactiveAppElementDictionary.append(appElementDTO.get_xpath())
        formXPath = directiveDTO.get_form_x_path()
        directiveLogJson = json.dumps(
            {
                "interactive_appElement": interactiveAppElementDictionary,
                "appEvent": directiveDictionary,
                "formXPath": formXPath})

        self._update_input_value_weights(directiveDictionary)

        Logger().info(
            f"Save html set:\n{fileName}\n{formXPath}\n{directiveDictionary}")

        fileManager = FileManager()
        fileManager.create_folder("htmlSet", "GUIDE_HTML_SET")
        fileManager.create_file(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            fileName=fileName + ".html",
            context=directiveDTO.get_dom())
        fileManager.create_file(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            fileName=fileName + ".json",
            context=directiveLogJson)

    def _have_same_url(self, url: str):
        targetPageDTOs = self._get_all_target_page_dto()
        for targetPageDTO in targetPageDTOs:
            if targetPageDTO.get_target_url() == url:
                return True
        return False

    def _have_same_task_id(self, taskID: str):
        targetPageDTOs = self._get_all_target_page_dto()
        for targetPageDTO in targetPageDTOs:
            if targetPageDTO.get_task_id() == taskID:
                return True
        return False

    def _update_input_value_weights(self, appEvent):
        inputValueWeights = ValueWeightSingleton.get_instance().get_value_weights()

        for xpath, event in appEvent.items():
            category = event["category"]
            value = event["value"]
            categoryIndex = inputTypes.index(category)
            if value in inputValues[categoryIndex]:
                indexOfValue = inputValues[categoryIndex].index(value)
                inputValueWeights[category][indexOfValue] *= 10
                Logger().info(
                    f"Update inputValueWeight: {category} [{value}] {inputValueWeights[category][indexOfValue]}")
                inputValueWeights[category] = [float(weight) / sum(inputValueWeights[category]) for weight
                                               in inputValueWeights[category]]

        ValueWeightSingleton.get_instance().set_value_weights(inputValueWeights)
