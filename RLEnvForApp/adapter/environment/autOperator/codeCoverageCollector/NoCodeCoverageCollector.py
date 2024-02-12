from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class NoCodeCoverageCollector(ICodeCoverageCollector):
    def __init__(self):
        super().__init__()

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        codeCoverageDTOs = []
        codeCoverageDTOs.append(
            CodeCoverageDTO(
                codeCoverageType="statement coverage",
                codeCoverageVector=[False]))
        return codeCoverageDTOs

    def reset_code_coverage(self):
        pass
