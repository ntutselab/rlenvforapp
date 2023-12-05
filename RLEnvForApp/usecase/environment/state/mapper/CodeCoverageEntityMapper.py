from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity


def mappingCodeCoverageEntityFrom(codeCoverage: CodeCoverage) -> CodeCoverageEntity:
    return CodeCoverageEntity(codeCoverageType= codeCoverage.getCodeCoverageType(), codeCoverageVector=codeCoverage.getCodeCoverageVector())

def mappingCodeCoverageFrom(codeCoverageEntity: CodeCoverageEntity) -> CodeCoverage:
    return CodeCoverage(codeCoverageType=codeCoverageEntity.getCodeCoverageType(), codeCoverageVector=codeCoverageEntity.getCodeCoverageVector())