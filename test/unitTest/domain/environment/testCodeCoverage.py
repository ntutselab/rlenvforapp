import re
import unittest

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class testCodeCoverage(unittest.TestCase):
    def testGetImprovedCodeCoverage(self):
        originCodeCoverageVector = [1,1,0,0]
        codeCoverageVector = [1,0,1,0]
        originCodeCoverage = CodeCoverage(codeCoverageType="statement", codeCoverageVector=originCodeCoverageVector)
        codeCoverage = CodeCoverage(codeCoverageType="statement", codeCoverageVector=codeCoverageVector)

        improvedCodeCoverage = codeCoverage.getImprovedCodeCoverage(originalCodeCovreage=originCodeCoverage)
        self.assertEqual(improvedCodeCoverage.getCodeCoverageType(), "Improved: statement")
        self.assertEqual(improvedCodeCoverage.getCodeCoverageVector(), [0, 0, 1, 0])

    def testTest(self):
        xpath = "/html/body/div/form/div[2]/div/input".upper()
        newXpath = ""
        for path in xpath.split("/"):
            if not re.match(".*\[\d*\]", path) and not path == "":
                path += "[1]/"
            else:
                path += "/"
            newXpath += path
        print(newXpath[:len(newXpath)-1])
