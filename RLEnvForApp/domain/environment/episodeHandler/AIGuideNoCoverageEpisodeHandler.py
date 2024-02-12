from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.logger.logger import Logger


class AIGuideNoCoverageEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def is_done(self) -> bool:
        initState: State = self._states[0]
        initURL = initState.get_url()

        currentState: State = self._states[-1]
        previousState: State = self._states[-2]

        if initURL != currentState.get_url():
            Logger().info("Episode is done because the URL has changed.")
            return True

        if len(currentState.get_focus_vector()) == 0:
            Logger().info("Episode is done because the state has no focus vector.")
            return True

        if super().get_episode_step() != - \
                1 and super().get_episode_step() + 1 <= len(self._states):
            Logger().info("Episode is done because the episode step exceeded.")
            return True

        if previousState.get_interacted_element() and previousState.get_interacted_element().get_type() == "submit" and \
                previousState.get_action_type() == "click" and \
                self._is_all_input_tag_has_value(previousState.get_all_selected_app_elements()):
            Logger().info("Episode is done because click on submit button, and all input has value.")
            return True
        return False

    def _is_all_input_tag_has_value(self, appElements: [AppElement]):
        for i in appElements:
            if i.get_tag_name() == "input" and (
                    i.get_type() != "button" and i.get_type() != "submit"):
                if i.get_value() == "":
                    return False
        return True
