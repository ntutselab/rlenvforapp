import unittest

from RLEnvForApp.domain.environment.observationService.converter.CodeCoverageVectorConverter import \
    CodeCoverageVectorConverter
from RLEnvForApp.domain.environment.state import CodeCoverage


class testCodeCoverageVectorConverter(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testConvert(self):
        codeCoverage = CodeCoverage.CodeCoverage(
            codeCoverageType="branch coverage", codeCoverageVector=[3, 2, 1, 0])
        codeCoverageVector = codeCoverage.getCodeCoverageVector()

        listCodeCoverageFeature = CodeCoverageVectorConverter().convert(
            stateElement=codeCoverageVector)

        self.assertNotEqual([3, 2, 1, 0], listCodeCoverageFeature)
        self.assertEqual([1, 1, 1, 0], listCodeCoverageFeature)
