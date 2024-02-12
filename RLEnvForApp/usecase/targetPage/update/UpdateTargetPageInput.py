from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class UpdateTargetPageInput:
    def __init__(self, targetPageId: str, targetPageUrl: str = None, rootUrl: str = None, appEventDTOs: [AppEventDTO] = None,
                 taskID: str = None, basicCodeCoverageDTO: CodeCoverageDTO = None, directiveDTOs: [DirectiveDTO] = None):
        self._targetPageId = targetPageId
        self._targetPageUrl = targetPageUrl
        self._rootUrl = rootUrl
        self._appEventDTOs = appEventDTOs
        self._taskID = taskID
        self._basicCodeCoverageDTO = basicCodeCoverageDTO
        self._directiveDTOs = directiveDTOs

    def getTargetPageId(self):
        return self._targetPageId

    def getTargetPageUrl(self):
        return self._targetPageUrl

    def getRootUrl(self):
        return self._rootUrl

    def getAppEventDTOs(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def getTaskID(self):
        return self._taskID

    def getBasicCodeCoverageDTO(self) -> CodeCoverageDTO:
        return self._basicCodeCoverageDTO

    def getDirectiveDTOs(self) -> [DirectiveDTO]:
        return self._directiveDTOs
