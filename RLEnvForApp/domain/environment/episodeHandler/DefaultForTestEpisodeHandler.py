from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state import State


class DefaultForTestEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episode_step: int):
        super().__init__(id, episodeIndex, episode_step)
        self._states: [State] = []

    def is_done(self) -> bool:
        last_state: State = self.get_state(super().get_number_of_state() - 1)
        if super().get_episode_step() != - \
                1 and super().get_episode_step() <= len(super().get_all_state()):
            return True
        if last_state.get_action_type() == "click":
            return True
        return False
