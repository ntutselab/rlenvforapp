from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity


class EpisodeHandlerEntity:
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        self._id = id
        self._episodeIndex = episodeIndex
        self._episodeStep = episodeStep
        self._stateEntities: [StateEntity] = []

    def get_id(self):
        return self._id

    def get_episode_index(self):
        return self._episodeIndex

    def get_episode_step(self):
        return self._episodeStep

    def set_all_state_entities(self, stateEntities: [StateEntity]):
        self._stateEntities = stateEntities

    def get_state_entities(self) -> [StateEntity]:
        return self._stateEntities
