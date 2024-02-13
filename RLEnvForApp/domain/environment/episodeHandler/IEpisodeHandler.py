from RLEnvForApp.domain.environment.state import State


class IEpisodeHandler:
    def __init__(self, id: str, episodeIndex: int, episode_step: int):
        self._id = id
        self._episode_index = episodeIndex
        self._episode_step = episode_step
        self._states: [State] = []

    def get_id(self):
        return self._id

    def get_episode_index(self) -> int:
        return self._episode_index

    def get_episode_step(self):
        return self._episode_step

    def append_state(self, state: State):
        self._states.append(state)

    def get_state(self, index: int) -> State:
        return self._states[index]

    def set_all_state(self, state: State):
        self._states = state

    def get_all_state(self) -> [State]:
        return self._states

    def is_done(self) -> bool:
        pass

    def get_number_of_state(self) -> int:
        return len(self._states)

    def reset(self):
        self._states = []
