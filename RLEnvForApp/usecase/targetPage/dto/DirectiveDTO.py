from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class DirectiveDTO:
    def __init__(self, url: str, dom: str, formXPath: str, appEventDTOs: [
                 AppEventDTO], codeCoverageDTOs: [CodeCoverageDTO]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEventDTOs = appEventDTOs
        self._codeCoverageDTOs = codeCoverageDTOs

    def getUrl(self) -> str:
        return self._url

    def getDom(self) -> str:
        return self._dom

    def getFormXPath(self) -> str:
        return self._formXPath

    def getAppEventDTOs(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        return self._codeCoverageDTOs
