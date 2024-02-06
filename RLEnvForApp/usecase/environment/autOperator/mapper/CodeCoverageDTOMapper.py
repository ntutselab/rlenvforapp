from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO


def mappingCodeCoverageFrom(codeCoverageDTO: CodeCoverageDTO) -> CodeCoverage:
    return CodeCoverage(codeCoverageType=codeCoverageDTO.getCodeCoverageType(),
                        codeCoverageVector=codeCoverageDTO.getCodeCoverageVector())


def mappingCodeCoverageDTOFrom(codeCoverage: CodeCoverage) -> CodeCoverageDTO:
    return CodeCoverageDTO(codeCoverageType=codeCoverage.getCodeCoverageType(),
                           codeCoverageVector=codeCoverage.getCodeCoverageVector())
