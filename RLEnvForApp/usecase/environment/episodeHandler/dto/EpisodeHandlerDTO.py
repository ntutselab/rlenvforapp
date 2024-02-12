from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO


class EpisodeHandlerDTO:
    def __init__(self, id: str, episodeIndex: int,
                 episodeStep: int, stateDTOs: [StateDTO]):
        self._id = id
        self._episodeIndex = episodeIndex
        self._episodeStep = episodeStep
        self._stateDTOs: [StateDTO] = stateDTOs

    def get_id(self):
        return self._id

    def get_episode_index(self):
        return self._episodeIndex

    def get_episode_step(self):
        return self._episodeStep

    def get_state_dt_os(self) -> [StateDTO]:
        return self._stateDTOs
