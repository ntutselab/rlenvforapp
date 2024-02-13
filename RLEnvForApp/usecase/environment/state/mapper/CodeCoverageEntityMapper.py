from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity


def mapping_code_coverage_entity_from(
        code_coverage: CodeCoverage) -> CodeCoverageEntity:
    return CodeCoverageEntity(code_coverage_type=code_coverage.get_code_coverage_type(),
                              code_coverage_vector=code_coverage.get_code_coverage_vector())


def mapping_code_coverage_from(
        code_coverage_entity: CodeCoverageEntity) -> CodeCoverage:
    return CodeCoverage(code_coverage_type=code_coverage_entity.get_code_coverage_type(),
                        code_coverage_vector=code_coverage_entity.get_code_coverage_vector())
