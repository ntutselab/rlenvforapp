from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class TargetPageDTO:
    def __init__(self, id: str, targetUrl: str, rootUrl: str, appEventDTOs: [AppEventDTO], taskID: str,
                 formXPath: str, basicCodeCoverageDTO: CodeCoverageDTO, directiveDTOs: [DirectiveDTO]):
        self._id = id
        self._targetUrl = targetUrl
        self._rootUrl = rootUrl
        self._appEventDTOs = appEventDTOs
        self._taskID = taskID
        self._formXPath = formXPath
        self._basicCodeCoverageDTO = basicCodeCoverageDTO
        self._directiveDTOs = directiveDTOs

    def getId(self):
        return self._id

    def getTargetUrl(self):
        return self._targetUrl

    def getRootUrl(self):
        return self._rootUrl

    def getAppEventDTOs(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def getTaskID(self):
        return self._taskID

    def getFormXPath(self):
        return self._formXPath

    def getBasicCodeCoverageDTO(self) -> CodeCoverageDTO:
        return self._basicCodeCoverageDTO

    def getDirectiveDTOs(self) -> [DirectiveDTO]:
        return self._directiveDTOs
