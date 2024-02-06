from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


class DirectiveEntity:
    def __init__(self, url: str, dom: str, formXPath: str, appEventEntities: [
                 AppEventEntity], codeCoverageEntities: [CodeCoverageEntity]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEventEntities = appEventEntities
        self._codeCoverageEntities = codeCoverageEntities

    def getUrl(self) -> str:
        return self._url

    def getDom(self) -> str:
        return self._dom

    def getFormXPath(self) -> str:
        return self._formXPath

    def getAppEventEntities(self) -> [AppEventEntity]:
        return self._appEventEntities

    def getCodeCoverageEntities(self) -> [CodeCoverageEntity]:
        return self._codeCoverageEntities
