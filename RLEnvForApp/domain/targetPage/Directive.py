from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent


class Directive:
    def __init__(self, url: str, dom: str, formXPath: str, appEvents: [
                 AppEvent], codeCoverages: [CodeCoverage]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEvents = appEvents
        self._codeCoverages = codeCoverages

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_x_path(self) -> str:
        return self._formXPath

    def get_app_events(self) -> [AppEvent]:
        return self._appEvents

    def get_code_coverages(self) -> [CodeCoverage]:
        return self._codeCoverages

    def get_code_coverage_by_type(self, codeCoverageType: str) -> CodeCoverage:
        for codeCoverage in self._codeCoverages:
            if codeCoverage.get_code_coverage_type() == codeCoverageType:
                return codeCoverage
