import itertools

from RLEnvForApp.logger.logger import Logger


class CodeCoverage:
    def __init__(self, codeCoverageType: str, codeCoverageVector: [bool]):
        self._codeCoverageType = codeCoverageType
        self._codeCoverageVector = codeCoverageVector

    def get_code_coverage_type(self):
        return self._codeCoverageType

    def get_code_coverage_vector(self):
        return self._codeCoverageVector

    def get_code_coverage_vector_length(self):
        return len(self._codeCoverageVector)

    def get_covered_amount(self):
        coveredAmount = 0
        for i in self._codeCoverageVector:
            if i:
                coveredAmount += 1
        return coveredAmount

    def get_ratio(self):
        return self.get_covered_amount() / self.get_code_coverage_vector_length()

    def get_improved_code_coverage(self, originalCodeCovreage):
        if self.get_code_coverage_vector_length(
        ) != originalCodeCovreage.get_code_coverage_vector_length():
            Logger().info(
                f"Warning: Origin code coverage size is {originalCodeCovreage.getCodeCoverageVectorLength()}, New code coverage size is {self.getCodeCoverageVectorLength()}")
        originCodeCoverageVector = originalCodeCovreage.get_code_coverage_vector()
        improvedCodeCoverageVector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(
                self._codeCoverageVector, originCodeCoverageVector):
            improvedCodeCoverageVector.append(
                bool(not originalCovered and covered))
        return CodeCoverage(codeCoverageType="Improved: " + self._codeCoverageType,
                            codeCoverageVector=improvedCodeCoverageVector)

    def merge(self, codeCoverage):
        if self.get_code_coverage_type() != codeCoverage.get_code_coverage_type():
            raise Exception("Differenet type of code coverage")
        codeCoverageVector = codeCoverage.get_code_coverage_vector()
        newCodeCoverageVector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(
                self._codeCoverageVector, codeCoverageVector):
            newCodeCoverageVector.append(bool(originalCovered or covered))
        self._codeCoverageVector = newCodeCoverageVector
