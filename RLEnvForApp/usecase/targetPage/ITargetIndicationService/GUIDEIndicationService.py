from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import \
    ITargetIndicationService
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.targetPage.queueManager.TargetPageProcessingManagerSingleton import \
    TargetPageProcessingManagerSingleton


class GUIDEIndicationService(ITargetIndicationService):
    def __init__(self):
        super().__init__()

    def isConform(self, state: State) -> bool:
        targetPage: TargetPage = TargetPageProcessingManagerSingleton.getInstance().getBeProcessedTargetPage()
        basicCodeCoverage: CodeCoverage = targetPage.getBasicCodeCoverage()
        targetCodeCoverage: CodeCoverage = targetPage.getTargetCodeCoverage()
        stateCodeCoverage: CodeCoverage = self._getCodeCoverageByType(
            codeCoverages=state.getCodeCoverages(), type=targetCodeCoverage.getCodeCoverageType())

        targetImprovedCodeCoverage = targetCodeCoverage.getImprovedCodeCoverage(
            originalCodeCovreage=basicCodeCoverage)
        stateImprovedCodeCoverage = stateCodeCoverage.getImprovedCodeCoverage(
            originalCodeCovreage=basicCodeCoverage)

        if stateImprovedCodeCoverage.getCoveredAmount() == 0:
            return False

        if stateImprovedCodeCoverage.getCoveredAmount() >= targetImprovedCodeCoverage.getCoveredAmount():
            return True
        else:
            return False

    def _getCodeCoverageByType(self, codeCoverages: [CodeCoverage], type: str):
        for codeCoverage in codeCoverages:
            if codeCoverage.getCodeCoverageType() == type:
                return codeCoverage
