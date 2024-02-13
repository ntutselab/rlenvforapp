from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class NoCodeCoverageCollector(ICodeCoverageCollector):
    def __init__(self):
        super().__init__()

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        code_coverage_dt_os = []
        code_coverage_dt_os.append(
            CodeCoverageDTO(
                code_coverage_type="statement coverage",
                code_coverage_vector=[False]))
        return code_coverage_dt_os

    def reset_code_coverage(self):
        pass
