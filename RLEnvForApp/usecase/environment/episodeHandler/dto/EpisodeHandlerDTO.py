from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO


class EpisodeHandlerDTO:
    def __init__(self, id: str, episodeIndex: int,
                 episode_step: int, state_dt_os: [StateDTO]):
        self._id = id
        self._episode_index = episodeIndex
        self._episode_step = episode_step
        self._state_dt_os: [StateDTO] = state_dt_os

    def get_id(self):
        return self._id

    def get_episode_index(self):
        return self._episode_index

    def get_episode_step(self):
        return self._episode_step

    def get_state_dt_os(self) -> [StateDTO]:
        return self._state_dt_os
