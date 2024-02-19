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

    def getId(self):
        return self._id

    def getTargetUrl(self):
        return self._targetUrl

    def setTargetUrl(self, targetUrl: str):
        self._targetUrl = targetUrl

    def getRootUrl(self):
        return self._rootUrl

    def setRootUrl(self, rootUrl: str):
        self._rootUrl = rootUrl

    def getAppEvents(self) -> [AppEvent]:
        return self._appEvents

    def setAppEvents(self, appEvents: [AppEvent]):
        self._appEvents = appEvents

    def getTaskID(self) -> str:
        return self._taskID

    def setTaskID(self, taskID: str):
        self._taskID = taskID

    def getFormXPath(self):
        return self._formXPath

    def setFormXPath(self, formXPath: str):
        self._formXPath = formXPath

    def getBasicCodeCoverage(self) -> [bool]:
        return self._basicCodeCoverage

    def setBasicCodeCoverage(self, basicCodeCoverage: [bool]):
        self._basicCodeCoverage = basicCodeCoverage

    def getDirectives(self) -> [Directive]:
        return self._directives

    def setDirectives(self, directives: [Directive]):
        self._directives = directives

    def appendDirective(self, directive: Directive):
        self._directives.append(directive)

    def getTargetCodeCoverage(self) -> CodeCoverage:
        codeCoverageType = self._basicCodeCoverage.getCodeCoverageType()
        if len(self._directives) == 0:
            return self._basicCodeCoverage
        else:
            targetDirective: Directive = None
            for directive in self._directives:
                if targetDirective is None:
                    targetDirective = directive
                    continue
                targetCodeCoverage: CodeCoverage = targetDirective.getCodeCoverageByType(
                    codeCoverageType=codeCoverageType)
                directiveCodeCoverage: CodeCoverage = directive.getCodeCoverageByType(
                    codeCoverageType=codeCoverageType)

                if targetDirective is None:
                    targetDirective = directive
                if targetCodeCoverage.getCoveredAmount() < directiveCodeCoverage.getCoveredAmount():
                    targetDirective = directive
            return targetDirective.getCodeCoverageByType(codeCoverageType=codeCoverageType)
