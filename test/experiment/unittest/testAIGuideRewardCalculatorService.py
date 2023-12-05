import unittest

from RLEnvForApp.domain.environment.rewardCalculatorService.AIGuideRewardCalculatorService import \
    AIGuideRewardCalculatorService
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive


class testAIGuideRewardCalculatorService(unittest.TestCase):
    def test_coverage_is_better(self):
        rewardCalculater = AIGuideRewardCalculatorService()
        directiveA = Directive(appEvents=None,
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 0, 0, 0, 0])])
        directiveB = Directive(appEvents=None,
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 1, 0, 0, 0])])
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveA, directiveB=directiveB), directiveB)
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveB, directiveB=directiveA), directiveB)

    def test_more_coverage_is_better(self):
        rewardCalculater = AIGuideRewardCalculatorService()
        directiveA = Directive(appEvents=None,
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 0, 0, 0, 0]),
                                              self.createCodeCoverage(type="statement",
                                                                      coverageVector=[1, 1, 0, 0, 0])])
        directiveB = Directive(appEvents=None,
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 1, 0, 0, 0])])
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveA, directiveB=directiveB), directiveB)
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveB, directiveB=directiveA), directiveB)

    def test_same_coverage_but_appEvent_is_better(self):
        rewardCalculater = AIGuideRewardCalculatorService()
        directiveA = Directive(appEvents=[self.createAppEvent(), self.createAppEvent()],
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 0, 0, 0, 0]),
                                              self.createCodeCoverage(type="statement",
                                                                      coverageVector=[1, 1, 0, 0, 0])])
        directiveB = Directive(appEvents=[self.createAppEvent()],
                               codeCoverages=[self.createCodeCoverage(type="branch", coverageVector=[1, 0, 0, 0, 0])])
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveA, directiveB=directiveB), directiveB)
        self.assertEqual(rewardCalculater.getBetterDirective(directiveA=directiveB, directiveB=directiveA), directiveB)

    def createCodeCoverage(self, type: str, coverageVector: [bool]):
        return CodeCoverage(codeCoverageType=type, codeCoverageVector=coverageVector)

    def createAppEvent(self, xpath: str = "", value: str = ""):
        return AppEvent(xpath=xpath, value=value)
