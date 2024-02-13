from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State


class AIGuideEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episode_step: int):
        super().__init__(id, episodeIndex, episode_step)
        self._states: [State] = []

    def is_done(self) -> bool:
        init_state: State = self._states[0]
        init_url = init_state.get_url()
        init_coverages: [CodeCoverage] = init_state.get_code_coverages()

        last_state: State = self.get_state(super().get_number_of_state() - 1)
        last_url = last_state.get_url()
        last_coverages: [CodeCoverage] = last_state.get_code_coverages()

        if init_url != last_url:
            return True

        if len(last_state.get_focus_vector()) == 0:
            return True

        if super().get_episode_step() != - \
                1 and super().get_episode_step() <= len(super().get_all_state()) - 1:
            return True

        for lastCoverage in last_coverages:
            initCoverage: CodeCoverage = self._get_code_coverage_by_type(
                type=lastCoverage.get_code_coverage_type(), code_coverages=init_coverages)
            improvedCoverage: CodeCoverage = lastCoverage.get_improved_code_coverage(
                originalCodeCovreage=initCoverage)
            if improvedCoverage.get_covered_amount() != 0:
                return True

        return False

    def _get_code_coverage_by_type(self, type: str, code_coverages: [CodeCoverage]):
        for code_coverage in code_coverages:
            if code_coverage.get_code_coverage_type() == type:
                return code_coverage
