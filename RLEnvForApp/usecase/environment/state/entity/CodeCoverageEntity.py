class CodeCoverageEntity:
    def __init__(self, code_coverage_type: str, code_coverage_vector: [bool]):
        self._code_coverage_type = code_coverage_type
        self._code_coverage_vector = code_coverage_vector

    def get_code_coverage_type(self):
        return self._code_coverage_type

    def get_code_coverage_vector(self):
        return self._code_coverage_vector
