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
        code_coverage = CodeCoverage.CodeCoverage(
            code_coverage_type="branch coverage", code_coverage_vector=[3, 2, 1, 0])
        code_coverage_vector = code_coverage.get_code_coverage_vector()

        list_code_coverage_feature = CodeCoverageVectorConverter().convert(
            state_element=code_coverage_vector)

        self.assertNotEqual([3, 2, 1, 0], list_code_coverage_feature)
        self.assertEqual([1, 1, 1, 0], list_code_coverage_feature)
