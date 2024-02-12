import unittest

from RLEnvForApp.domain.environment.observationService.converter.CodeCoverageVectorConverter import \
    CodeCoverageVectorConverter
from RLEnvForApp.domain.environment.state import CodeCoverage


class testCodeCoverageVectorConverter(unittest.TestCase):
    def set_up(self) -> None:
        pass

    def tear_down(self) -> None:
        pass

    def test_convert(self):
        codeCoverage = CodeCoverage.CodeCoverage(
            codeCoverageType="branch coverage", codeCoverageVector=[3, 2, 1, 0])
        codeCoverageVector = codeCoverage.get_code_coverage_vector()

        listCodeCoverageFeature = CodeCoverageVectorConverter().convert(
            stateElement=codeCoverageVector)

        self.assertNotEqual([3, 2, 1, 0], listCodeCoverageFeature)
        self.assertEqual([1, 1, 1, 0], listCodeCoverageFeature)
