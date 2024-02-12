from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class DirectiveDTO:
    def __init__(self, url: str, dom: str, formXPath: str, appEventDTOs: [
                 AppEventDTO], codeCoverageDTOs: [CodeCoverageDTO]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEventDTOs = appEventDTOs
        self._codeCoverageDTOs = codeCoverageDTOs

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_x_path(self) -> str:
        return self._formXPath

    def get_app_event_dt_os(self) -> [AppEventDTO]:
        return self._appEventDTOs

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        return self._codeCoverageDTOs
