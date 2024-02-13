import itertools

from RLEnvForApp.logger.logger import Logger


class CodeCoverage:
    def __init__(self, code_coverage_type: str, code_coverage_vector: [bool]):
        self._code_coverage_type = code_coverage_type
        self._code_coverage_vector = code_coverage_vector

    def get_code_coverage_type(self):
        return self._code_coverage_type

    def get_code_coverage_vector(self):
        return self._code_coverage_vector

    def get_code_coverage_vector_length(self):
        return len(self._code_coverage_vector)

    def get_covered_amount(self):
        covered_amount = 0
        for i in self._code_coverage_vector:
            if i:
                covered_amount += 1
        return covered_amount

    def get_ratio(self):
        return self.get_covered_amount() / self.get_code_coverage_vector_length()

    def get_improved_code_coverage(self, originalCodeCovreage):
        if self.get_code_coverage_vector_length(
        ) != originalCodeCovreage.get_code_coverage_vector_length():
            Logger().info(
                f"Warning: Origin code coverage size is {originalCodeCovreage.getCodeCoverageVectorLength()}, New code coverage size is {self.getCodeCoverageVectorLength()}")
        origin_code_coverage_vector = originalCodeCovreage.get_code_coverage_vector()
        improved_code_coverage_vector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(
                self._code_coverage_vector, origin_code_coverage_vector):
            improved_code_coverage_vector.append(
                bool(not originalCovered and covered))
        return CodeCoverage(code_coverage_type="Improved: " + self._code_coverage_type,
                            code_coverage_vector=improved_code_coverage_vector)

    def merge(self, code_coverage):
        if self.get_code_coverage_type() != code_coverage.get_code_coverage_type():
            raise Exception("Differenet type of code coverage")
        code_coverage_vector = code_coverage.get_code_coverage_vector()
        new_code_coverage_vector: [bool] = []
        for covered, originalCovered in itertools.zip_longest(
                self._code_coverage_vector, code_coverage_vector):
            new_code_coverage_vector.append(bool(originalCovered or covered))
        self._code_coverage_vector = new_code_coverage_vector
