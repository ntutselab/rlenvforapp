import itertools

from RLEnvForApp.logger.logger import Logger


class CodeCoverage:
    def __init__(self, codeCoverageType: str, codeCoverageVector: [bool]):
        self._codeCoverageType = codeCoverageType
        self._codeCoverageVector = codeCoverageVector

    def getCodeCoverageType(self):
        return self._codeCoverageType

    def getCodeCoverageVector(self):
        return self._codeCoverageVector

    def getCodeCoverageVectorLength(self):
        return len(self._codeCoverageVector)

    def getCoveredAmount(self):
        coveredAmount = 0
        for i in self._codeCoverageVector:
            if i:
                coveredAmount += 1
        return coveredAmount

    def getRatio(self):
        return self.getCoveredAmount() / self.getCodeCoverageVectorLength()

    def getImprovedCodeCoverage(self, originalCodeCovreage):
        if self.getCodeCoverageVectorLength() != originalCodeCovreage.getCodeCoverageVectorLength():
            Logger().info(
                f"Warning: Origin code coverage size is {originalCodeCovreage.getCodeCoverageVectorLength()}, New code coverage size is {self.getCodeCoverageVectorLength()}")
        originCodeCoverageVector = originalCodeCovreage.getCodeCoverageVector()
        improvedCodeCoverageVector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(self._codeCoverageVector, originCodeCoverageVector):
            improvedCodeCoverageVector.append(bool(not originalCovered and covered))
        return CodeCoverage(codeCoverageType="Improved: " + self._codeCoverageType, codeCoverageVector=improvedCodeCoverageVector)

    def merge(self, codeCoverage):
        if self.getCodeCoverageType() != codeCoverage.getCodeCoverageType():
            raise Exception("Differenet type of code coverage")
        codeCoverageVector = codeCoverage.getCodeCoverageVector()
        newCodeCoverageVector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(self._codeCoverageVector, codeCoverageVector):
            newCodeCoverageVector.append(bool(originalCovered or covered))
        self._codeCoverageVector = newCodeCoverageVector
