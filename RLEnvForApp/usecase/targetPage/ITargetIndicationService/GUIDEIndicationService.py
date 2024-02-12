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

    def is_conform(self, state: State) -> bool:
        targetPage: TargetPage = TargetPageProcessingManagerSingleton.get_instance(
        ).get_be_processed_target_page()
        basicCodeCoverage: CodeCoverage = targetPage.get_basic_code_coverage()
        targetCodeCoverage: CodeCoverage = targetPage.get_target_code_coverage()
        stateCodeCoverage: CodeCoverage = self._get_code_coverage_by_type(
            codeCoverages=state.get_code_coverages(), type=targetCodeCoverage.get_code_coverage_type())

        targetImprovedCodeCoverage = targetCodeCoverage.get_improved_code_coverage(
            originalCodeCovreage=basicCodeCoverage)
        stateImprovedCodeCoverage = stateCodeCoverage.get_improved_code_coverage(
            originalCodeCovreage=basicCodeCoverage)

        if stateImprovedCodeCoverage.get_covered_amount() == 0:
            return False

        if stateImprovedCodeCoverage.get_covered_amount(
        ) >= targetImprovedCodeCoverage.get_covered_amount():
            return True
        else:
            return False

    def _get_code_coverage_by_type(self, codeCoverages: [CodeCoverage], type: str):
        for codeCoverage in codeCoverages:
            if codeCoverage.get_code_coverage_type() == type:
                return codeCoverage
