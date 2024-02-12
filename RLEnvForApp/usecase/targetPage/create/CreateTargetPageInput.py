from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class CreateTargetPageInput():
    def __init__(self, targetPageUrl: str, rootUrl: str, appEventDTOs: [AppEventDTO], taskID: str = "",
                 formXPath: str = "", basicCodeCoverage: CodeCoverageDTO = None, directiveDTOs: [DirectiveDTO] = []):
        self._targetPageUrl = targetPageUrl
        self._rootUrl = rootUrl
        self._appEventDTOs = appEventDTOs
        self._taskID = taskID
        self._formXPath = formXPath
        self._basicCodeCoverage = basicCodeCoverage
        self._directiveDTOs = directiveDTOs

    def getTargetPageUrl(self):
        return self._targetPageUrl

    def getRootUrl(self):
        return self._rootUrl

    def getAppEventDTOs(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def getTaskID(self):
        return self._taskID

    def getFormXPath(self):
        return self._formXPath

    def getBasicCodeCoverage(self):
        return self._basicCodeCoverage

    def getDirectiveDTOs(self) -> [DirectiveDTO]:
        return self._directiveDTOs
