from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive


class TargetPage:
    def __init__(self, id: str, targetUrl: str, rootUrl: str, appEvents: [AppEvent], taskID: str,
                 formXPath: str, basicCodeCoverage: CodeCoverage, directives: [Directive]):
        self._id = id
        self._targetUrl = targetUrl
        self._rootUrl = rootUrl
        self._appEvents = appEvents
        self._taskID = taskID
        self._formXPath = formXPath
        self._basicCodeCoverage = basicCodeCoverage
        self._directives: [] = directives

    def get_id(self):
        return self._id

    def get_target_url(self):
        return self._targetUrl

    def set_target_url(self, targetUrl: str):
        self._targetUrl = targetUrl

    def get_root_url(self):
        return self._rootUrl

    def set_root_url(self, rootUrl: str):
        self._rootUrl = rootUrl

    def get_app_events(self) -> [AppEvent]:
        return self._appEvents

    def set_app_events(self, appEvents: [AppEvent]):
        self._appEvents = appEvents

    def get_task_id(self) -> str:
        return self._taskID

    def set_task_id(self, taskID: str):
        self._taskID = taskID

    def get_form_x_path(self):
        return self._formXPath

    def set_form_x_path(self, formXPath: str):
        self._formXPath = formXPath

    def get_basic_code_coverage(self) -> [bool]:
        return self._basicCodeCoverage

    def set_basic_code_coverage(self, basicCodeCoverage: [bool]):
        self._basicCodeCoverage = basicCodeCoverage

    def get_directives(self) -> [Directive]:
        return self._directives

    def set_directives(self, directives: [Directive]):
        self._directives = directives

    def append_directive(self, directive: Directive):
        self._directives.append(directive)

    def get_target_code_coverage(self) -> CodeCoverage:
        codeCoverageType = self._basicCodeCoverage.get_code_coverage_type()
        if len(self._directives) == 0:
            return self._basicCodeCoverage
        else:
            targetDirective: Directive = None
            for directive in self._directives:
                if targetDirective is None:
                    targetDirective = directive
                    continue
                targetCodeCoverage: CodeCoverage = targetDirective.get_code_coverage_by_type(
                    codeCoverageType=codeCoverageType)
                directiveCodeCoverage: CodeCoverage = directive.get_code_coverage_by_type(
                    codeCoverageType=codeCoverageType)

                if targetDirective is None:
                    targetDirective = directive
                if targetCodeCoverage.get_covered_amount() < directiveCodeCoverage.get_covered_amount():
                    targetDirective = directive
            return targetDirective.get_code_coverage_by_type(
                codeCoverageType=codeCoverageType)
