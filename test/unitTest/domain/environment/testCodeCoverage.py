import re
import unittest

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class testCodeCoverage(unittest.TestCase):
    def test_get_improved_code_coverage(self):
        originCodeCoverageVector = [1, 1, 0, 0]
        codeCoverageVector = [1, 0, 1, 0]
        originCodeCoverage = CodeCoverage(
            codeCoverageType="statement",
            codeCoverageVector=originCodeCoverageVector)
        codeCoverage = CodeCoverage(
            codeCoverageType="statement",
            codeCoverageVector=codeCoverageVector)

        improvedCodeCoverage = codeCoverage.get_improved_code_coverage(
            originalCodeCovreage=originCodeCoverage)
        self.assertEqual(
            improvedCodeCoverage.get_code_coverage_type(),
            "Improved: statement")
        self.assertEqual(
            improvedCodeCoverage.get_code_coverage_vector(), [
                0, 0, 1, 0])

    def test_test(self):
        xpath = "/html/body/div/form/div[2]/div/input".upper()
        newXpath = ""
        for path in xpath.split("/"):
            if not re.match(".*\\[\\d*\\]", path) and not path == "":
                path += "[1]/"
            else:
                path += "/"
            newXpath += path
        print(newXpath[:len(newXpath) - 1])
