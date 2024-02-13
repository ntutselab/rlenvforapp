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
        target_page: TargetPage = TargetPageProcessingManagerSingleton.get_instance(
        ).get_be_processed_target_page()
        basic_code_coverage: CodeCoverage = target_page.get_basic_code_coverage()
        target_code_coverage: CodeCoverage = target_page.get_target_code_coverage()
        state_code_coverage: CodeCoverage = self._get_code_coverage_by_type(
            code_coverages=state.get_code_coverages(), type=target_code_coverage.get_code_coverage_type())

        target_improved_code_coverage = target_code_coverage.get_improved_code_coverage(
            originalCodeCovreage=basic_code_coverage)
        state_improved_code_coverage = state_code_coverage.get_improved_code_coverage(
            originalCodeCovreage=basic_code_coverage)

        if state_improved_code_coverage.get_covered_amount() == 0:
            return False

        if state_improved_code_coverage.get_covered_amount(
        ) >= target_improved_code_coverage.get_covered_amount():
            return True
        else:
            return False

    def _get_code_coverage_by_type(self, code_coverages: [CodeCoverage], type: str):
        for code_coverage in code_coverages:
            if code_coverage.get_code_coverage_type() == type:
                return code_coverage
