from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.IDirectiveRuleService import \
    IDirectiveRuleService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class MaxCodeCoverageDirectiveRuleService(IDirectiveRuleService):
    def __init__(self):
        super().__init__()
        self._code_coverage_type = "statement coverage"

    def is_legal(self, target_page: TargetPage,
                directive: Directive, lastDom="") -> bool:
        target_directive_code_coverage: CodeCoverage = directive.get_code_coverage_by_type(
            code_coverage_type=self._code_coverage_type)

        basic_code_coverage = target_page.get_basic_code_coverage()
        target_directive_improved_code_coverage = target_directive_code_coverage.get_improved_code_coverage(
            originalCodeCovreage=basic_code_coverage)
        if target_directive_improved_code_coverage.get_covered_amount() == 0:
            return False

        for previousDirective in target_page.get_directives():
            previousCodeCoverage: CodeCoverage = previousDirective.get_code_coverage_by_type(
                code_coverage_type=self._code_coverage_type)

            previousImprovedCodeCoverage = previousCodeCoverage.get_improved_code_coverage(
                originalCodeCovreage=basic_code_coverage)

            isImproved = target_directive_improved_code_coverage.get_covered_amount(
            ) > previousImprovedCodeCoverage.get_covered_amount()
            isSameCoverdNumber = target_directive_code_coverage.get_covered_amount(
            ) == previousCodeCoverage.get_covered_amount()
            isShorterAppEvents = len(
                directive.get_app_events()) < len(
                previousDirective.get_app_events())
            if not isImproved and not (
                    isSameCoverdNumber and isShorterAppEvents):
                return False
        return True
