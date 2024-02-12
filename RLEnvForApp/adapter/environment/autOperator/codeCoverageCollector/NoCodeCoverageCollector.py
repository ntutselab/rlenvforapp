from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class NoCodeCoverageCollector(ICodeCoverageCollector):
    def __init__(self):
        super().__init__()

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        codeCoverageDTOs = []
        codeCoverageDTOs.append(
            CodeCoverageDTO(
                codeCoverageType="statement coverage",
                codeCoverageVector=[False]))
        return codeCoverageDTOs

    def resetCodeCoverage(self):
        pass
