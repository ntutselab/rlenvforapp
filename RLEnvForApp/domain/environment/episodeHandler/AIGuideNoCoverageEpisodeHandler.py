from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.logger.logger import Logger


class AIGuideNoCoverageEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def isDone(self) -> bool:
        initState: State = self._states[0]
        initURL = initState.getUrl()

        currentState: State = self._states[-1]
        previousState: State = self._states[-2]

        if initURL != currentState.getUrl():
            Logger().info("Episode is done because the URL has changed.")
            return True

        if len(currentState.getFocusVector()) == 0:
            Logger().info("Episode is done because the state has no focus vector.")
            return True

        if super().getEpisodeStep() != -1 and super().getEpisodeStep() + 1 <= len(self._states):
            Logger().info("Episode is done because the episode step exceeded.")
            return True

        if previousState.getInteractedElement() and previousState.getInteractedElement().getType() == "submit" and \
                previousState.getActionType() == "click" and \
                self._is_all_input_tag_has_value(previousState.getAllSelectedAppElements()):
            Logger().info("Episode is done because click on submit button, and all input has value.")
            return True

        # return True if the states has more than 10 changeFocus action
        if self._is_more_than_ten_change_focus_action():
            Logger().info("Episode is done because the states has more than 10 changeFocus action.")
            return True

        return False

    def _is_all_input_tag_has_value(self, appElements: [AppElement]):
        for i in appElements:
            if i.getTagName() == "input" and (i.getType() != "button" and i.getType() != "submit"):
                if i.getValue() == "":
                    return False
        return True

    def _is_more_than_ten_change_focus_action(self):
        count = 0
        for state in self._states:
            if state.getActionType() == "changeFocus":
                count += 1
        return count > 10
