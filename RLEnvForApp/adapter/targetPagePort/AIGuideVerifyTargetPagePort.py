import os
import json

from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageUseCase, CreateTargetPageOutput, CreateTargetPageInput)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.get import GetAllTargetPageUseCase, GetAllTargetPageInput, GetAllTargetPageOutput


class AIGuideVerifyTargetPagePort(ITargetPagePort):
    def __init__(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str, rootUrl: str = "127.0.0.1", codeCoverageType: str = "coverage"):
        super().__init__()
        self._folderPath = "htmlSet/LEARNING_TASK"
        self._javaIp = javaIp
        self._pythonIp = pythonIp
        self._javaPort = javaPort
        self._pythonPort = pythonPort
        self._rootUrl = rootUrl
        self._codeCoverageType = codeCoverageType
        self._javaObjectPy4JLearningPool = None
        self._javaObjectLearningTaskDTOs = []
        self._serverName = serverName

    def connect(self):
        pass

    def close(self):
        pass

    def waitForTargetPage(self):
        self.pullTargetPage()

    def pullTargetPage(self):
        while len(self._getAllTargetPageDTO()) == 0:
            targetPagePaths = self._getAllFilePathInFolder(self._folderPath)
            for path in targetPagePaths:
                if ".json" in path:
                    folderPath, pageHTMLFileName = os.path.split(path)
                    pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"
                    jsonData = open(os.path.join(folderPath, pageJsonFileName), )
                    pageLog = json.load(jsonData)
                    jsonData.close()
                    pageLog = pageLog[0]
                    formXpath = pageLog["formXPaths"][0]
                    appEventDTOs = []
                    for actionSequence in pageLog["actionSequence"]:
                        for appEvent in actionSequence:
                            appEventDTO = AppEventDTO(xpath=appEvent["xpath"],
                                                      value=appEvent["value"], category="")
                            appEventDTOs.append(appEventDTO)

                    self._addTargetPage(targetPageUrl=pageLog["targetURL"], rootUrl=self._rootUrl, formXPath=formXpath,
                                        appEventDTOs=appEventDTOs, stateID=pageLog["stateID"],
                                        codeCoverageVector=None)

    def _getAllTargetPageDTO(self) -> [TargetPageDTO]:
        getAllTargetPageUseCase = GetAllTargetPageUseCase.GetAllTargetPageUseCase()
        getAllTargetPageInput = GetAllTargetPageInput.GetAllTargetPageInput()
        getAllTargetPageOutput = GetAllTargetPageOutput.GetAllTargetPageOutput()

        getAllTargetPageUseCase.execute(input=getAllTargetPageInput, output=getAllTargetPageOutput)
        return getAllTargetPageOutput.getTargetPageDTOs()

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

    def _getAllFilePathInFolder(self, targetFolderPath: str):
        filesPath = []
        for dirPath, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                filesPath.append(dirPath + "/" + file)
        return filesPath
