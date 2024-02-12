from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class MaxCodeCoverageDirectiveRuleService(IDirectiveRuleService):
    def __init__(self):
        super().__init__()
        self._codeCoverageType = "statement coverage"

    def is_legal(self, targetPage: TargetPage,
                directive: Directive, lastDom="") -> bool:
        targetDirectiveCodeCoverage: CodeCoverage = directive.get_code_coverage_by_type(
            codeCoverageType=self._codeCoverageType)

        basicCodeCoverage = targetPage.get_basic_code_coverage()
        targetDirectiveImprovedCodeCoverage = targetDirectiveCodeCoverage.get_improved_code_coverage(
            originalCodeCovreage=basicCodeCoverage)
        if targetDirectiveImprovedCodeCoverage.get_covered_amount() == 0:
            return False

        for previousDirective in targetPage.get_directives():
            previousCodeCoverage: CodeCoverage = previousDirective.get_code_coverage_by_type(
                codeCoverageType=self._codeCoverageType)

            previousImprovedCodeCoverage = previousCodeCoverage.get_improved_code_coverage(
                originalCodeCovreage=basicCodeCoverage)

            isImproved = targetDirectiveImprovedCodeCoverage.get_covered_amount(
            ) > previousImprovedCodeCoverage.get_covered_amount()
            isSameCoverdNumber = targetDirectiveCodeCoverage.get_covered_amount(
            ) == previousCodeCoverage.get_covered_amount()
            isShorterAppEvents = len(
                directive.get_app_events()) < len(
                previousDirective.get_app_events())
            if not isImproved and not (
                    isSameCoverdNumber and isShorterAppEvents):
                return False
        return True
