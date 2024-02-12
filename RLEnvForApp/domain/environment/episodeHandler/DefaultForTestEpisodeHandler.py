from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state import State


class DefaultForTestEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def isDone(self) -> bool:
        lastState: State = self.getState(super().getNumberOfState() - 1)
        if super().getEpisodeStep() != - \
                1 and super().getEpisodeStep() <= len(super().getAllState()):
            return True
        if lastState.getActionType() == "click":
            return True
        return False
