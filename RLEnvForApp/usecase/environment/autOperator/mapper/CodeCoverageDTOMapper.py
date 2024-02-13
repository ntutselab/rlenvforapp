from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


def mapping_code_coverage_from(code_coverage_dto: CodeCoverageDTO) -> CodeCoverage:
    return CodeCoverage(code_coverage_type=code_coverage_dto.get_code_coverage_type(),
                        code_coverage_vector=code_coverage_dto.get_code_coverage_vector())


def mapping_code_coverage_dto_from(code_coverage: CodeCoverage) -> CodeCoverageDTO:
    return CodeCoverageDTO(code_coverage_type=code_coverage.get_code_coverage_type(),
                           code_coverage_vector=code_coverage.get_code_coverage_vector())
