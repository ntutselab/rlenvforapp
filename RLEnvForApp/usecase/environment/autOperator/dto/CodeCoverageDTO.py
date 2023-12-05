# CodeCoverageDTO

class CodeCoverageDTO:
    def __init__(self, codeCoverageType: str, codeCoverageVector: [bool]):
        self._codeCoverageType = codeCoverageType
        self._codeCoverageVector = codeCoverageVector

    def getCodeCoverageType(self):
        return self._codeCoverageType

    def getCodeCoverageVector(self):
        return self._codeCoverageVector