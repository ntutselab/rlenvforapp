from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state import State
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.logger.logger import Logger


class AIGuideHTMLLogEpisodeHandler(IEpisodeHandler):
    def __init__(self, id: str, episodeIndex: int, episodeStep: int):
        super().__init__(id, episodeIndex, episodeStep)
        self._states: [State] = []

    def is_done(self) -> bool:
        previousState: State = self._states[-2]
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
