import unittest

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.MaxCodeCoverageDirectiveRuleService import \
    MaxCodeCoverageDirectiveRuleService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class testMaxCodeCoverageDirectiveRuleService(unittest.TestCase):
    def set_up(self) -> None:
        self._directiveRuleService = MaxCodeCoverageDirectiveRuleService()
        self._codeCoverageType = "statement coverage"

    def test_no_improved_code_coverage_with_baseline(self):
        basicCodeCoverage = self._create_code_coverage([1, 1, 1, 1, 1])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])

        self.assertFalse(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def test_improved_code_coverage_with_baseline(self):
        basicCodeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([1, 1, 1, 1, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])

        self.assertTrue(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def test_improved_code_coverage_with_older_directive(self):
        basicCodeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        targetPage.append_directive(directive=directive)

        codeCoverage = self._create_code_coverage([0, 0, 0, 1, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        self.assertTrue(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive(self):
        basicCodeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([0, 0, 0, 1, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        targetPage.append_directive(directive=directive)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        self.assertFalse(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive_but_shorter_app_events(
            self):
        basicCodeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(
            appEvents=[
                AppEvent(
                    xpath="",
                    value="")],
            codeCoverages=[codeCoverage])
        targetPage.append_directive(directive=directive)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        self.assertTrue(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive_but_no_shorter_app_events(
            self):
        basicCodeCoverage = self._create_code_coverage([0, 0, 0, 0, 0])
        targetPage = self._create_target_page(
            basicCodeCoverage=basicCodeCoverage)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(appEvents=[], codeCoverages=[codeCoverage])
        targetPage.append_directive(directive=directive)

        codeCoverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(
            appEvents=[
                AppEvent(
                    xpath="",
                    value="")],
            codeCoverages=[codeCoverage])
        self.assertFalse(
            self._directiveRuleService.is_legal(
                targetPage=targetPage,
                directive=directive))

    def _create_target_page(self, basicCodeCoverage: CodeCoverage) -> TargetPage:
        return TargetPage(id="123",
                          targetUrl="/",
                          rootUrl="/",
                          appEvents="",
                          taskID="456",
                          basicCodeCoverage=basicCodeCoverage,
                          directives=[])

    def _create_code_coverage(self, codeCoverageVector: [bool]) -> CodeCoverage:
        return CodeCoverage(codeCoverageType=self._codeCoverageType,
                            codeCoverageVector=codeCoverageVector)
