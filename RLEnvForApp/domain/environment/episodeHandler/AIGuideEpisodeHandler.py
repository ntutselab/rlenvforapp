from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State


class AIGuideEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def isDone(self) -> bool:
        initState: State = self._states[0]
        initURL = initState.getUrl()
        initCoverages: [CodeCoverage] = initState.getCodeCoverages()

        lastState: State = self.getState(super().getNumberOfState() - 1)
        lastUrl = lastState.getUrl()
        lastCoverages: [CodeCoverage] = lastState.getCodeCoverages()

        if initURL != lastUrl:
            return True

        if len(lastState.getFocusVector()) == 0:
            return True

        if super().getEpisodeStep() != -1 and super().getEpisodeStep() <= len(super().getAllState()) - 1:
            return True

        for lastCoverage in lastCoverages:
            initCoverage: CodeCoverage = self._getCodeCoverageByType(type=lastCoverage.getCodeCoverageType(), codeCoverages=initCoverages)
            improvedCoverage: CodeCoverage = lastCoverage.getImprovedCodeCoverage(originalCodeCovreage=initCoverage)
            if improvedCoverage.getCoveredAmount() != 0:
                return True

        return False

    def _getCodeCoverageByType(self, type: str, codeCoverages: [CodeCoverage]):
        for codeCoverage in codeCoverages:
            if codeCoverage.getCodeCoverageType() == type:
                return codeCoverage
