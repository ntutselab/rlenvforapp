from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity


def mapping_code_coverage_entity_from(
        codeCoverage: CodeCoverage) -> CodeCoverageEntity:
    return CodeCoverageEntity(codeCoverageType=codeCoverage.get_code_coverage_type(),
                              codeCoverageVector=codeCoverage.get_code_coverage_vector())


def mapping_code_coverage_from(
        codeCoverageEntity: CodeCoverageEntity) -> CodeCoverage:
    return CodeCoverage(codeCoverageType=codeCoverageEntity.get_code_coverage_type(),
                        codeCoverageVector=codeCoverageEntity.get_code_coverage_vector())
