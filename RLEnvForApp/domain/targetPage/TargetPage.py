from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive


class TargetPage:
    def __init__(self, id: str, targetUrl: str, root_url: str, app_events: [AppEvent], task_id: str,
                 form_xpath: str, basic_code_coverage: CodeCoverage, directives: [Directive]):
        self._id = id
        self._target_url = targetUrl
        self._root_url = root_url
        self._app_events = app_events
        self._task_id = task_id
        self._form_xpath = form_xpath
        self._basic_code_coverage = basic_code_coverage
        self._directives: [] = directives

    def get_id(self):
        return self._id

    def get_target_url(self):
        return self._target_url

    def set_target_url(self, targetUrl: str):
        self._target_url = targetUrl

    def get_root_url(self):
        return self._root_url

    def set_root_url(self, root_url: str):
        self._root_url = root_url

    def get_app_events(self) -> [AppEvent]:
        return self._app_events

    def set_app_events(self, app_events: [AppEvent]):
        self._app_events = app_events

    def get_task_id(self) -> str:
        return self._task_id

    def set_task_id(self, task_id: str):
        self._task_id = task_id

    def get_form_xpath(self):
        return self._form_xpath

    def set_form_xpath(self, form_xpath: str):
        self._form_xpath = form_xpath

    def get_basic_code_coverage(self) -> [bool]:
        return self._basic_code_coverage

    def set_basic_code_coverage(self, basic_code_coverage: [bool]):
        self._basic_code_coverage = basic_code_coverage

    def get_directives(self) -> [Directive]:
        return self._directives

    def set_directives(self, directives: [Directive]):
        self._directives = directives

    def append_directive(self, directive: Directive):
        self._directives.append(directive)

    def get_target_code_coverage(self) -> CodeCoverage:
        code_coverage_type = self._basic_code_coverage.get_code_coverage_type()
        if len(self._directives) == 0:
            return self._basic_code_coverage
        else:
            targetDirective: Directive = None
            for directive in self._directives:
                if targetDirective is None:
                    targetDirective = directive
                    continue
                target_code_coverage: CodeCoverage = targetDirective.get_code_coverage_by_type(
                    code_coverage_type=code_coverage_type)
                directiveCodeCoverage: CodeCoverage = directive.get_code_coverage_by_type(
                    code_coverage_type=code_coverage_type)

                if targetDirective is None:
                    targetDirective = directive
                if target_code_coverage.get_covered_amount() < directiveCodeCoverage.get_covered_amount():
                    targetDirective = directive
            return targetDirective.get_code_coverage_by_type(
                code_coverage_type=code_coverage_type)
