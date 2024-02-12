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

    def get_target_page_id(self):
        return self._targetPageId

    def get_target_page_url(self):
        return self._targetPageUrl

    def get_root_url(self):
        return self._rootUrl

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def get_task_id(self):
        return self._taskID

    def get_basic_code_coverage_dto(self) -> CodeCoverageDTO:
        return self._basicCodeCoverageDTO

    def get_directive_dt_os(self) -> [DirectiveDTO]:
        return self._directiveDTOs
