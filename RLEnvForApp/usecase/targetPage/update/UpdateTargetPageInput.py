from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class UpdateTargetPageInput:
    def __init__(self, target_page_id: str, target_page_url: str = None, root_url: str = None, app_event_dt_os: [AppEventDTO] = None,
                 task_id: str = None, basic_code_coverage_dto: CodeCoverageDTO = None, directive_dt_os: [DirectiveDTO] = None):
        self._target_page_id = target_page_id
        self._target_page_url = target_page_url
        self._root_url = root_url
        self._app_event_dt_os = app_event_dt_os
        self._task_id = task_id
        self._basic_code_coverage_dto = basic_code_coverage_dto
        self._directive_dt_os = directive_dt_os

    def get_target_page_id(self):
        return self._target_page_id

    def get_target_page_url(self):
        return self._target_page_url

    def get_root_url(self):
        return self._root_url

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._app_event_dt_os

    def get_task_id(self):
        return self._task_id

    def get_basic_code_coverage_dto(self) -> CodeCoverageDTO:
        return self._basic_code_coverage_dto

    def get_directive_dt_os(self) -> [DirectiveDTO]:
        return self._directive_dt_os
