from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity


class TargetPageEntity:
    def __init__(self, id: str, targetUrl: str, rootUrl: str, appEventEntities: [AppEventEntity], taskID: str,
                 formXPath: str, basicCodeCoverageEntity: CodeCoverageEntity, directiveEntities: [DirectiveEntity]):
        self._id = id
        self._targetUrl = targetUrl
        self._rootUrl = rootUrl
        self._appEventEntities = appEventEntities
        self._taskID = taskID
        self._formXPath = formXPath
        self._basicCodeCoverageEntity = basicCodeCoverageEntity
        self._directiveEntities = directiveEntities

    def getId(self):
        return self._id

    def getTargetUrl(self):
        return self._targetUrl

    def getRootUrl(self):
        return self._rootUrl

    def getAppEventEntities(self) -> AppEventEntity:
        return self._appEventEntities

    def getTaskID(self):
        return self._taskID

    def getFormXPath(self):
        return self._formXPath

    def getBasicCodeCoverageEntity(self) -> CodeCoverageEntity:
        return self._basicCodeCoverageEntity

    def getDirectiveEntities(self) -> [DirectiveEntity]:
        return self._directiveEntities
