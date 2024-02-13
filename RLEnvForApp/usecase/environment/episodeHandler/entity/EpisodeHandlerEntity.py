from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity


class EpisodeHandlerEntity:
    def __init__(self, id: str, episodeIndex: int, episode_step: int):
        self._id = id
        self._episode_index = episodeIndex
        self._episode_step = episode_step
        self._state_entities: [StateEntity] = []

    def get_id(self):
        return self._id

    def get_episode_index(self):
        return self._episode_index

    def get_episode_step(self):
        return self._episode_step

    def set_all_state_entities(self, state_entities: [StateEntity]):
        self._state_entities = state_entities

    def get_state_entities(self) -> [StateEntity]:
        return self._state_entities
