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
        gateway_parameters = GatewayParameters(address=self._javaIp, port=self._javaPort)
        callback_server_parameters = CallbackServerParameters(
            address=self._pythonIp, port=self._pythonPort)
        self._javaObjectPy4JLearningPool = JavaGateway(gateway_parameters=gateway_parameters,
                                                       callback_server_parameters=callback_server_parameters)

    def close(self):
        self._javaObjectPy4JLearningPool.setAgentDone(True)
        self._javaObjectPy4JLearningPool.shutdown()

    def waitForTargetPage(self):
        Logger().info("Waiting for target page")
        while (self._javaObjectPy4JLearningPool.isLearningTaskDTOQueueEmpty()):
            time.sleep(1)
        self.pullTargetPage()

    def pullTargetPage(self):
        isFirst = True
        while len(self._getAllTargetPageDTO()) == 0 or isFirst:
            while not (self._javaObjectPy4JLearningPool.isLearningTaskDTOQueueEmpty()):
                javaObjectLearningTaskDTO = self._javaObjectPy4JLearningPool.deQueueLearningTaskDTO()
                url = javaObjectLearningTaskDTO.getTargetURL()
                stateID = javaObjectLearningTaskDTO.getStateID()
                formXPaths = javaObjectLearningTaskDTO.getFormXPaths()

                appEventDTOs = []
                for javaObjectHighLevelActionDTO in javaObjectLearningTaskDTO.getHighLevelActionDTOList():
                    for javaObjectActionDTO in javaObjectHighLevelActionDTO.getActionDTOList():
                        appEventDTO = AppEventDTO(
                            xpath=javaObjectActionDTO.getXpath(),
                            value=javaObjectActionDTO.getValue(),
                            category="")
                        appEventDTOs.append(appEventDTO)

                codeCoverageVector = []
                for i in javaObjectLearningTaskDTO.getCodeCoverageVector():
                    codeCoverageVector.append(i)
                codeCoverageDTO = self._createCodeCoverageDTO(
                    codeCoverageType=self._codeCoverageType,
                    codeCoverageVector=javaObjectLearningTaskDTO.getCodeCoverageVector())
                if not self._haveSameTaskID(taskID=stateID):
                    # support for filling out multiple forms
                    for formXPath in formXPaths:
                        self._addTargetPage(
                            targetPageUrl=url,
                            rootUrl=self._rootUrl,
                            appEventDTOs=appEventDTOs,
                            stateID=stateID,
                            formXPath=formXPath,
                            codeCoverageVector=codeCoverageDTO)
                    # support for filling in single form
                    # self._addTargetPage(targetPageUrl=url, rootUrl=self._rootUrl, appEventDTOs=appEventDTOs,
                    # stateID=stateID, formXPath="//form", codeCoverageVector=codeCoverageDTO)
                    self._javaObjectLearningTaskDTOs.append(javaObjectLearningTaskDTO)
            isFirst = False

    def pushTargetPage(self, targetPageId: str, episodeHandlerId: str):
        directiveDTO = self._createDirective(
            targetPageId=targetPageId,
            episodeHandlerId=episodeHandlerId)
        targetPageDTO: TargetPageDTO = self._getTargetPage(targetPageId=targetPageId)

        self._javaObjectPy4JLearningPool.enQueueLearningResultDTO(
            self._createJavaObjectLearningResultDTO(
                taskId=targetPageDTO.getTaskID(), directiveDTO=directiveDTO))
        self._saveTargetPageToHtmlSet(episodeHandlerId=episodeHandlerId, directiveDTO=directiveDTO)
        if not self._isTraining:
            self._removeTargetPage(targetPageId=targetPageId)

    def getPauseAgent(self):
        return self._javaObjectPy4JLearningPool.getPauseAgent()

    def setPauseAgent(self, isPauseAgent: bool):
        self._javaObjectPy4JLearningPool.setPauseAgent(isPauseAgent)

    def _addTargetPage(self, targetPageUrl: str, rootUrl: str, appEventDTOs: [AppEventDTO], stateID: str = "",
                       formXPath: str = "", codeCoverageVector: CodeCoverageDTO = None):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase()
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            appEventDTOs=appEventDTOs,
                                                                            taskID=stateID,
                                                                            formXPath=formXPath,
                                                                            basicCodeCoverage=codeCoverageVector)
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

    def _getAllTargetPageDTO(self) -> [TargetPageDTO]:
        getAllTargetPageUseCase = GetAllTargetPageUseCase.GetAllTargetPageUseCase()
        getAllTargetPageInput = GetAllTargetPageInput.GetAllTargetPageInput()
        getAllTargetPageOutput = GetAllTargetPageOutput.GetAllTargetPageOutput()

        getAllTargetPageUseCase.execute(input=getAllTargetPageInput, output=getAllTargetPageOutput)
        return getAllTargetPageOutput.getTargetPageDTOs()

    def _removeTargetPage(self, targetPageId: str):
        removeTargetPageUseCase = RemoveTargetPageUseCase.RemoveTargetPageUseCase()
        removeTargetPageInput = RemoveTargetPageInput.RemoveTargetPageInput(
            targetPageId=targetPageId)
        removeTargetPageOutput = RemoveTargetPageOutput.RemoveTargetPageOutput()

        removeTargetPageUseCase.execute(input=removeTargetPageInput, output=removeTargetPageOutput)

    def _createCodeCoverageDTO(self, codeCoverageType: str, codeCoverageVector: [bool]):
        return CodeCoverageDTO(codeCoverageType=codeCoverageType,
                               codeCoverageVector=codeCoverageVector)

    def _getTargetPage(self, targetPageId: str):
        getTargetPageUseCase = GetTargetPageUseCase.GetTargetPageUseCase()
        getTargetPageInput = GetTargetPageInput.GetTargetPageInput(targetPageId=targetPageId)
        getTargetPageOutput = GetTargetPageOutput.GetTargetPageOutput()

        getTargetPageUseCase.execute(input=getTargetPageInput, output=getTargetPageOutput)
        return getTargetPageOutput.getTargetPageDTO()

    def _createDirective(self, targetPageId: str, episodeHandlerId: str):
        createDirectiveUseCase = CreateDirectiveUseCase.CreateDirectiveUseCase()
        createDirectiveInput = CreateDirectiveInput.CreateDirectiveInput(
            targetPageId=targetPageId, episodeHandlerId=episodeHandlerId)
        createDirectiveOutput = CreateDirectiveOutput.CreateDirectiveOutput()
        createDirectiveUseCase.execute(createDirectiveInput, createDirectiveOutput)

        return createDirectiveOutput.getDirectiveDTO()

    def _getEpisodeHandlerDTO(self, episodeHandlerId: str) -> EpisodeHandlerDTO:
        usecase = GetEpisodeHandlerUseCase.GetEpisodeHandlerUseCase()
        input = GetEpisodeHandlerInput.GetEpisodeHandlerInput(episodeHandlerId=episodeHandlerId)
        output = GetEpisodeHandlerOutput.GetEpisodeHandlerOutput()

        usecase.execute(input=input, output=output)
        return output.getEpisodeHandlerDTO()

    def _findJavaObjectLearningTaskDTOByTaskID(self, stateID: str):
        for javaObjectLearningTaskDTO in self._javaObjectLearningTaskDTOs:
            if javaObjectLearningTaskDTO.getStateID() == stateID:
                return javaObjectLearningTaskDTO

    def _createJavaObjectHighLevelActions(self, appEventDTOs: [AppEventDTO]):
        highLevelActionDTOs = []
        highLevelActionDTOs.append([])
        for appEvent in appEventDTOs:
            if appEvent.getValue() == "":
                highLevelActionDTOs.append([appEvent])
                highLevelActionDTOs.append([])
            else:
                highLevelActionDTOs[len(highLevelActionDTOs) - 1].append(appEvent)

        javaObjectHighLevelActionDTOs = []
        for highLevelActionDTO in highLevelActionDTOs:
            if len(highLevelActionDTO) == 0:
                continue
            javaObjectHighLevelActionDTOBuilder = self._getjavaObjectHighLevelActionDTOBuilder()
            for appEvent in highLevelActionDTO:
                javaObjectHighLevelActionDTOBuilder.appendActionDTO(self._getCrawljaxXpath(xpath=appEvent.getXpath()),
                                                                    appEvent.getValue())
            javaObjectHighLevelActionDTOs.append(javaObjectHighLevelActionDTOBuilder.build())

        return javaObjectHighLevelActionDTOs

    def _getjavaObjectHighLevelActionDTOBuilder(self):
        javaObjectHighLevelActionDTOBuilder = self._javaObjectPy4JLearningPool.getHighLevelActionDTOBuilder()
        javaObjectHighLevelActionDTOBuilder.setActionDTOList()
        return javaObjectHighLevelActionDTOBuilder

    def _getCodeCoverageDTOByType(self, codeCoverageDTOs: [CodeCoverageDTO], type: str):
        for codeCoverageDTO in codeCoverageDTOs:
            if codeCoverageDTO.getCodeCoverageType() == type:
                return codeCoverageDTO

    def _getCrawljaxXpath(self, xpath: str):
        crawljaxXpath = ""
        for i in xpath.upper().split("/"):
            if not re.match(".*\\[\\d*\\]", i) and not i == "":
                i += "[1]/"
            else:
                i += "/"

            crawljaxXpath += i
        return crawljaxXpath[:len(crawljaxXpath) - 1]

    def _createJavaObjectLearningResultDTO(self, taskId: str, directiveDTO: DirectiveDTO):
        javaObjectLearningTaskDTO = self._findJavaObjectLearningTaskDTOByTaskID(taskId)
        javaObjectHighLevelActionDTOs = self._createJavaObjectHighLevelActions(
            appEventDTOs=directiveDTO.getAppEventDTOs())

        # build learning result
        javaObjectLearningResultDTOBuilder = self._javaObjectPy4JLearningPool.getLearnResultDTOBuilder()
        # set high level action
        javaObjectLearningResultDTOBuilder.setHighLevelActionDTOList()
        for javaObjectHighLevelActionDTO in javaObjectHighLevelActionDTOs:
            javaObjectLearningResultDTOBuilder.appendHighLevelActionDTOList(
                javaObjectHighLevelActionDTO)
        # set task id
        javaObjectLearningResultDTOBuilder.setTaskID(javaObjectLearningTaskDTO.getStateID())
        javaObjectLearningResultDTOBuilder.setFormXPath(directiveDTO.getFormXPath())
        # set code coverage
        codeCoverageDTO = self._getCodeCoverageDTOByType(codeCoverageDTOs=directiveDTO.getCodeCoverageDTOs(),
                                                         type="statement coverage")
        codeCoverageVector = codeCoverageDTO.getCodeCoverageVector()
        codeCoverageVectorSize = len(codeCoverageVector)
        javaObjectArray = self._javaObjectPy4JLearningPool.new_array(
            self._javaObjectPy4JLearningPool.jvm.boolean, codeCoverageVectorSize)
        for i in range(0, codeCoverageVectorSize):
            javaObjectArray[i] = codeCoverageVector[i]
        javaObjectLearningResultDTOBuilder.setCodeCoverageVector(javaObjectArray)
        # set original code coverage
        javaObjectLearningResultDTOBuilder.setOriginalCodeCoverageVector(
            javaObjectLearningTaskDTO.getCodeCoverageVector())
        javaObjectLearningResultDTOBuilder.setDone(False)
        return javaObjectLearningResultDTOBuilder.build()

    def _saveTargetPageToHtmlSet(self, episodeHandlerId: str, directiveDTO: DirectiveDTO):
        fileName = "{serverName}_{url}_{formXPath}".format(
            serverName=self._serverName,
            url=urlparse(
                directiveDTO.getUrl()).path.replace(
                "/",
                "_"),
            formXPath=directiveDTO.getFormXPath().replace(
                "/",
                "_"))
        initialStateDTO: StateDTO = self._getEpisodeHandlerDTO(
            episodeHandlerId=episodeHandlerId).getStateDTOs()[0]

        interactiveAppElementDictionary = []
        directiveDictionary = {}
        for appEventDTO in directiveDTO.getAppEventDTOs():
            directiveDictionary[appEventDTO.getXpath()] = {
                "value": appEventDTO.getValue(), "category": appEventDTO.getCategory()}
        for appElementDTO in initialStateDTO.getSelectedAppElementDTOs():
            interactiveAppElementDictionary.append(appElementDTO.getXpath())
        formXPath = directiveDTO.getFormXPath()
        directiveLogJson = json.dumps(
            {
                "interactive_appElement": interactiveAppElementDictionary,
                "appEvent": directiveDictionary,
                "formXPath": formXPath})

        self._updateInputValueWeights(directiveDictionary)

        Logger().info(f"Save html set:\n{fileName}\n{formXPath}\n{directiveDictionary}")

        fileManager = FileManager()
        fileManager.createFolder("htmlSet", "GUIDE_HTML_SET")
        fileManager.createFile(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            fileName=fileName + ".html",
            context=directiveDTO.getDom())
        fileManager.createFile(
            path=os.path.join(
                "htmlSet",
                "GUIDE_HTML_SET"),
            fileName=fileName + ".json",
            context=directiveLogJson)

    def _haveSameURL(self, url: str):
        targetPageDTOs = self._getAllTargetPageDTO()
        for targetPageDTO in targetPageDTOs:
            if targetPageDTO.getTargetUrl() == url:
                return True
        return False

    def _haveSameTaskID(self, taskID: str):
        targetPageDTOs = self._getAllTargetPageDTO()
        for targetPageDTO in targetPageDTOs:
            if targetPageDTO.getTaskID() == taskID:
                return True
        return False

    def _updateInputValueWeights(self, appEvent):
        inputValueWeights = ValueWeightSingleton.getInstance().getValueWeights()

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

        ValueWeightSingleton.getInstance().setValueWeights(inputValueWeights)
