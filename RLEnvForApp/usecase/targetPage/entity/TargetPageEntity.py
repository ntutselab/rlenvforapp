from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import \
    DirectiveEntity


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

    def get_id(self):
        return self._id

    def get_target_url(self):
        return self._targetUrl

    def get_root_url(self):
        return self._rootUrl

    def get_app_event_entities(self) -> AppEventEntity:
        return self._appEventEntities

    def get_task_id(self):
        return self._taskID

    def get_form_x_path(self):
        return self._formXPath

    def get_basic_code_coverage_entity(self) -> CodeCoverageEntity:
        return self._basicCodeCoverageEntity

    def get_directive_entities(self) -> [DirectiveEntity]:
        return self._directiveEntities
