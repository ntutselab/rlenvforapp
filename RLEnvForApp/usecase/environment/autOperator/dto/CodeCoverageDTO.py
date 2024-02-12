# CodeCoverageDTO

class CodeCoverageDTO:
    def __init__(self, codeCoverageType: str, codeCoverageVector: [bool]):
        self._codeCoverageType = codeCoverageType
        self._codeCoverageVector = codeCoverageVector

    def get_code_coverage_type(self):
        return self._codeCoverageType

    def get_code_coverage_vector(self):
        return self._codeCoverageVector
