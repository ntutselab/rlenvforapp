from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class ICodeCoverageCollector:
    def __init__(self):
        pass

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        return []

    def reset_code_coverage(self):
        pass
