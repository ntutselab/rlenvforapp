import re
import unittest

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class TestCodeCoverage(unittest.TestCase):
    def test_get_improved_code_coverage(self):
        origin_code_coverage_vector = [1, 1, 0, 0]
        code_coverage_vector = [1, 0, 1, 0]
        origin_code_coverage = CodeCoverage(
            code_coverage_type="statement",
            code_coverage_vector=origin_code_coverage_vector)
        code_coverage = CodeCoverage(
            code_coverage_type="statement",
            code_coverage_vector=code_coverage_vector)

        improved_code_coverage = code_coverage.get_improved_code_coverage(
            originalCodeCovreage=origin_code_coverage)
        self.assertEqual(
            improved_code_coverage.get_code_coverage_type(),
            "Improved: statement")
        self.assertEqual(
            improved_code_coverage.get_code_coverage_vector(), [
                0, 0, 1, 0])

    def test_test(self):
        xpath = "/html/body/div/form/div[2]/div/input".upper()
        new_xpath = ""
        for path in xpath.split("/"):
            if not re.match(".*\\[\\d*\\]", path) and not path == "":
                path += "[1]/"
            else:
                path += "/"
            new_xpath += path
        print(new_xpath[:len(new_xpath) - 1])
