import unittest

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.DirectiveRuleService.MaxCodeCoverageDirectiveRuleService import \
    MaxCodeCoverageDirectiveRuleService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class TestMaxCodeCoverageDirectiveRuleService(unittest.TestCase):
    def set_up(self) -> None:
        self._directive_rule_service = MaxCodeCoverageDirectiveRuleService()
        self._code_coverage_type = "statement coverage"

    def test_no_improved_code_coverage_with_baseline(self):
        basic_code_coverage = self._create_code_coverage([1, 1, 1, 1, 1])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        directive = Directive(app_events=[], code_coverages=[code_coverage])

        self.assertFalse(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def test_improved_code_coverage_with_baseline(self):
        basic_code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([1, 1, 1, 1, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])

        self.assertTrue(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def test_improved_code_coverage_with_older_directive(self):
        basic_code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        target_page.append_directive(directive=directive)

        code_coverage = self._create_code_coverage([0, 0, 0, 1, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        self.assertTrue(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive(self):
        basic_code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([0, 0, 0, 1, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        target_page.append_directive(directive=directive)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        self.assertFalse(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive_but_shorter_app_events(
            self):
        basic_code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(
            app_events=[
                AppEvent(
                    xpath="",
                    value="")],
            code_coverages=[code_coverage])
        target_page.append_directive(directive=directive)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        self.assertTrue(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def test_no_improved_code_coverage_with_older_directive_but_no_shorter_app_events(
            self):
        basic_code_coverage = self._create_code_coverage([0, 0, 0, 0, 0])
        target_page = self._create_target_page(
            basic_code_coverage=basic_code_coverage)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(app_events=[], code_coverages=[code_coverage])
        target_page.append_directive(directive=directive)

        code_coverage = self._create_code_coverage([0, 0, 0, 0, 1])
        directive = Directive(
            app_events=[
                AppEvent(
                    xpath="",
                    value="")],
            code_coverages=[code_coverage])
        self.assertFalse(
            self._directive_rule_service.is_legal(
                target_page=target_page,
                directive=directive))

    def _create_target_page(self, basic_code_coverage: CodeCoverage) -> TargetPage:
        return TargetPage(id="123",
                          targetUrl="/",
                          root_url="/",
                          app_events="",
                          task_id="456",
                          basic_code_coverage=basic_code_coverage,
                          directives=[])

    def _create_code_coverage(self, code_coverage_vector: [bool]) -> CodeCoverage:
        return CodeCoverage(code_coverage_type=self._code_coverage_type,
                            code_coverage_vector=code_coverage_vector)
