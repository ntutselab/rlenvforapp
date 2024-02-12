from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State


class AIGuideEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def is_done(self) -> bool:
        initState: State = self._states[0]
        initURL = initState.get_url()
        initCoverages: [CodeCoverage] = initState.get_code_coverages()

        lastState: State = self.get_state(super().get_number_of_state() - 1)
        lastUrl = lastState.get_url()
        lastCoverages: [CodeCoverage] = lastState.get_code_coverages()

        if initURL != lastUrl:
            return True

        if len(lastState.get_focus_vector()) == 0:
            return True

        if super().get_episode_step() != - \
                1 and super().get_episode_step() <= len(super().get_all_state()) - 1:
            return True

        for lastCoverage in lastCoverages:
            initCoverage: CodeCoverage = self._get_code_coverage_by_type(
                type=lastCoverage.get_code_coverage_type(), codeCoverages=initCoverages)
            improvedCoverage: CodeCoverage = lastCoverage.get_improved_code_coverage(
                originalCodeCovreage=initCoverage)
            if improvedCoverage.get_covered_amount() != 0:
                return True

        return False

    def _get_code_coverage_by_type(self, type: str, codeCoverages: [CodeCoverage]):
        for codeCoverage in codeCoverages:
            if codeCoverage.get_code_coverage_type() == type:
                return codeCoverage
