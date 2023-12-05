from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import IDirectiveRuleService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class MaxCodeCoverageDirectiveRuleService(IDirectiveRuleService):
    def __init__(self):
        super().__init__()
        self._codeCoverageType = "statement coverage"

    def isLegal(self, targetPage: TargetPage, directive: Directive, lastDom="") -> bool:
        targetDirectiveCodeCoverage: CodeCoverage = directive.getCodeCoverageByType(codeCoverageType=self._codeCoverageType)

        basicCodeCoverage = targetPage.getBasicCodeCoverage()
        targetDirectiveImprovedCodeCoverage = targetDirectiveCodeCoverage.getImprovedCodeCoverage(originalCodeCovreage=basicCodeCoverage)
        if targetDirectiveImprovedCodeCoverage.getCoveredAmount() == 0:
            return False

        for previousDirective in targetPage.getDirectives():
            previousCodeCoverage: CodeCoverage = previousDirective.getCodeCoverageByType(codeCoverageType=self._codeCoverageType)

            previousImprovedCodeCoverage = previousCodeCoverage.getImprovedCodeCoverage(originalCodeCovreage=basicCodeCoverage)

            isImproved = targetDirectiveImprovedCodeCoverage.getCoveredAmount() > previousImprovedCodeCoverage.getCoveredAmount()
            isSameCoverdNumber = targetDirectiveCodeCoverage.getCoveredAmount() == previousCodeCoverage.getCoveredAmount()
            isShorterAppEvents = len(directive.getAppEvents()) < len(previousDirective.getAppEvents())
            if not isImproved and not (isSameCoverdNumber and isShorterAppEvents):
                return False
        return True
