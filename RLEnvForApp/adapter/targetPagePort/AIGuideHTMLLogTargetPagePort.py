import json
import os

from RLEnvForApp.adapter.targetPagePort.ITargetPagePort import ITargetPagePort
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class AIGuideHTMLLogTargetPagePort(ITargetPagePort):
    def __init__(self, folderPath: str):
        super().__init__()
        self._folderPath = folderPath

    def connect(self):
        pass

    def close(self):
        pass

    def waitForTargetPage(self):
        targetPagePaths = self._getAllFilePathInFolder(self._folderPath)
        for path in targetPagePaths:
            if ".html" in path:
                folderPath, pageHTMLFileName = os.path.split(path)
                pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"
                jsonData = open(os.path.join(folderPath, pageJsonFileName),)
                pageLog = json.load(jsonData)
                jsonData.close()
                self._addTargetPage(
                    targetPageUrl=path,
                    rootUrl=path,
                    formXPath=pageLog["formXPath"],
                    appEventDTOs=[])

    def _addTargetPage(self, targetPageUrl: str, rootUrl: str,
                       formXPath: str, appEventDTOs: [AppEventDTO]):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase()
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl,
                                                                            formXPath=formXPath,
                                                                            appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

    def _getAllFilePathInFolder(self, targetFolderPath: str):
        filesPath = []
        for dirPath, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                filesPath.append(dirPath + "/" + file)
        return filesPath
