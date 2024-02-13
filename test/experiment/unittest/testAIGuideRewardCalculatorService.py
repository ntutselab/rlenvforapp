import unittest

from RLEnvForApp.domain.environment.rewardCalculatorService.AIGuideRewardCalculatorService import \
    AIGuideRewardCalculatorService
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive


class testAIGuideRewardCalculatorService(unittest.TestCase):
    def test_coverage_is_better(self):
        reward_calculater = AIGuideRewardCalculatorService()
        directive_a = Directive(app_events=None,
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 0, 0, 0, 0])])
        directive_b = Directive(app_events=None,
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 1, 0, 0, 0])])
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_a,
                directive_b=directive_b),
            directive_b)
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_b,
                directive_b=directive_a),
            directive_b)

    def test_more_coverage_is_better(self):
        reward_calculater = AIGuideRewardCalculatorService()
        directive_a = Directive(app_events=None,
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 0, 0, 0, 0]),
                                              self.create_code_coverage(type="statement",
                                                                      coverageVector=[1, 1, 0, 0, 0])])
        directive_b = Directive(app_events=None,
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 1, 0, 0, 0])])
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_a,
                directive_b=directive_b),
            directive_b)
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_b,
                directive_b=directive_a),
            directive_b)

    def test_same_coverage_but_app_event_is_better(self):
        reward_calculater = AIGuideRewardCalculatorService()
        directive_a = Directive(app_events=[self.create_app_event(), self.create_app_event()],
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 0, 0, 0, 0]),
                                              self.create_code_coverage(type="statement",
                                                                      coverageVector=[1, 1, 0, 0, 0])])
        directive_b = Directive(app_events=[self.create_app_event()],
                               code_coverages=[self.create_code_coverage(type="branch", coverageVector=[1, 0, 0, 0, 0])])
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_a,
                directive_b=directive_b),
            directive_b)
        self.assertEqual(
            reward_calculater.getBetterDirective(
                directive_a=directive_b,
                directive_b=directive_a),
            directive_b)

    def create_code_coverage(self, type: str, coverageVector: [bool]):
        return CodeCoverage(code_coverage_type=type,
                            code_coverage_vector=coverageVector)

    def create_app_event(self, xpath: str = "", value: str = ""):
        return AppEvent(xpath=xpath, value=value)
