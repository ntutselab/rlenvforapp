from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity


class EpisodeHandlerEntity:
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        self._id = id
        self._episodeIndex = episodeIndex
        self._episodeStep = episodeStep
        self._stateEntities: [StateEntity] = []

    def getId(self):
        return self._id

    def getEpisodeIndex(self):
        return self._episodeIndex

    def getEpisodeStep(self):
        return self._episodeStep

    def setAllStateEntities(self, stateEntities: [StateEntity]):
        self._stateEntities = stateEntities

    def getStateEntities(self) -> [StateEntity]:
        return self._stateEntities
