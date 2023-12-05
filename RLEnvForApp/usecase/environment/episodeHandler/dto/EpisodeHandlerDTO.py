from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO


class EpisodeHandlerDTO:
    def __init__(self, id: str, episodeIndex: int, episodeStep: int, stateDTOs: [StateDTO]):
        self._id = id
        self._episodeIndex = episodeIndex
        self._episodeStep = episodeStep
        self._stateDTOs: [StateDTO] = stateDTOs

    def getId(self):
        return self._id

    def getEpisodeIndex(self):
        return self._episodeIndex

    def getEpisodeStep(self):
        return self._episodeStep

    def getStateDTOs(self) -> [StateDTO]:
        return self._stateDTOs
