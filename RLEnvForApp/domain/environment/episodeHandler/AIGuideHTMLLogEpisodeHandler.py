from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state import State
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.logger.logger import Logger


class AIGuideHTMLLogEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def isDone(self) -> bool:
        previousState: State = self._states[-2]
        if super().getEpisodeStep() != - \
                1 and super().getEpisodeStep() + 1 <= len(self._states):
            Logger().info("Episode is done because the episode step exceeded.")
            return True
        if previousState.getInteractedElement() and previousState.getInteractedElement().getType() == "submit" and \
                previousState.getActionType() == "click" and \
                self._isAllInputTagHasValue(previousState.getAllSelectedAppElements()):
            Logger().info("Episode is done because click on submit button, and all input has value.")
            return True
        return False

    def _isAllInputTagHasValue(self, appElements: [AppElement]):
        for i in appElements:
            if i.getTagName() == "input" and (
                    i.getType() != "button" and i.getType() != "submit"):
                if i.getValue() == "":
                    return False
        return True
