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

    def get_target_page_url(self):
        return self._targetPageUrl

    def get_root_url(self):
        return self._rootUrl

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def get_task_id(self):
        return self._taskID

    def get_form_x_path(self):
        return self._formXPath

    def get_basic_code_coverage(self):
        return self._basicCodeCoverage

    def get_directive_dt_os(self) -> [DirectiveDTO]:
        return self._directiveDTOs
