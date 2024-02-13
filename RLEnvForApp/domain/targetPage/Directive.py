from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent


class Directive:
    def __init__(self, url: str, dom: str, form_xpath: str, app_events: [
                 AppEvent], code_coverages: [CodeCoverage]):
        self._url = url
        self._dom = dom
        self._form_xpath = form_xpath
        self._app_events = app_events
        self._code_coverages = code_coverages

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_xpath(self) -> str:
        return self._form_xpath

    def get_app_events(self) -> [AppEvent]:
        return self._app_events

    def get_code_coverages(self) -> [CodeCoverage]:
        return self._code_coverages

    def get_code_coverage_by_type(self, code_coverage_type: str) -> CodeCoverage:
        for code_coverage in self._code_coverages:
            if code_coverage.get_code_coverage_type() == code_coverage_type:
                return code_coverage
