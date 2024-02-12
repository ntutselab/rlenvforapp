from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
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

    def get_id(self):
        return self._id

    def get_target_url(self):
        return self._targetUrl

    def get_root_url(self):
        return self._rootUrl

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def get_task_id(self):
        return self._taskID

    def get_form_x_path(self):
        return self._formXPath

    def get_basic_code_coverage_dto(self) -> CodeCoverageDTO:
        return self._basicCodeCoverageDTO

    def get_directive_dt_os(self) -> [DirectiveDTO]:
        return self._directiveDTOs
