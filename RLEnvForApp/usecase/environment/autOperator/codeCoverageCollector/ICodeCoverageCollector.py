from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO


class ICodeCoverageCollector:
    def __init__(self):
        pass

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        return []

    def resetCodeCoverage(self):
        pass
