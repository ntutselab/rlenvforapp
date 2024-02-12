from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


def mapping_code_coverage_from(codeCoverageDTO: CodeCoverageDTO) -> CodeCoverage:
    return CodeCoverage(codeCoverageType=codeCoverageDTO.get_code_coverage_type(),
                        codeCoverageVector=codeCoverageDTO.get_code_coverage_vector())


def mapping_code_coverage_dto_from(codeCoverage: CodeCoverage) -> CodeCoverageDTO:
    return CodeCoverageDTO(codeCoverageType=codeCoverage.get_code_coverage_type(),
                           codeCoverageVector=codeCoverage.get_code_coverage_vector())
