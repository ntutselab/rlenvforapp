from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import \
    DirectiveEntity


class TargetPageEntity:
    def __init__(self, id: str, targetUrl: str, root_url: str, app_event_entities: [AppEventEntity], task_id: str,
                 form_x_path: str, basicCodeCoverageEntity: CodeCoverageEntity, directive_entities: [DirectiveEntity]):
        self._id = id
        self._target_url = targetUrl
        self._root_url = root_url
        self._app_event_entities = app_event_entities
        self._task_id = task_id
        self._form_x_path = form_x_path
        self._basic_code_coverage_entity = basicCodeCoverageEntity
        self._directive_entities = directive_entities

    def get_id(self):
        return self._id

    def get_target_url(self):
        return self._target_url

    def get_root_url(self):
        return self._root_url

    def get_app_event_entities(self) -> AppEventEntity:
        return self._app_event_entities

    def get_task_id(self):
        return self._task_id

    def get_form_x_path(self):
        return self._form_x_path

    def get_basic_code_coverage_entity(self) -> CodeCoverageEntity:
        return self._basic_code_coverage_entity

    def get_directive_entities(self) -> [DirectiveEntity]:
        return self._directive_entities
