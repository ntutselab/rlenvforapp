from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO


class CreateTargetPageInput():
    def __init__(self, target_page_url: str, root_url: str, app_event_dt_os: [AppEventDTO], task_id: str = "",
                 form_x_path: str = "", basic_code_coverage: CodeCoverageDTO = None, directive_dt_os: [DirectiveDTO] = []):
        self._target_page_url = target_page_url
        self._root_url = root_url
        self._app_event_dt_os = app_event_dt_os
        self._task_id = task_id
        self._form_x_path = form_x_path
        self._basic_code_coverage = basic_code_coverage
        self._directive_dt_os = directive_dt_os

    def get_target_page_url(self):
        return self._target_page_url

    def get_root_url(self):
        return self._root_url

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._app_event_dt_os

    def get_task_id(self):
        return self._task_id

    def get_form_x_path(self):
        return self._form_x_path

    def get_basic_code_coverage(self):
        return self._basic_code_coverage

    def get_directive_dt_os(self) -> [DirectiveDTO]:
        return self._directive_dt_os
