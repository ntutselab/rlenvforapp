from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state import State


class DefaultForTestEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def is_done(self) -> bool:
        lastState: State = self.get_state(super().get_number_of_state() - 1)
        if super().get_episode_step() != - \
                1 and super().get_episode_step() <= len(super().get_all_state()):
            return True
        if lastState.get_action_type() == "click":
            return True
        return False
