from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import AppElement, State


class DefaultForTestRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._episodeDoneRewardCoefficient: float = 50
        self._changeFocusRewardCoefficient: float = -1

        self._inputRewardCoefficient: float = 3.5
        self._inputRewardBaseLine: float = -3

    def calculate_reward(self, episodeHandler: IEpisodeHandler):
        reward = 0.0
        numberOfState = episodeHandler.get_number_of_state()
        lastState = episodeHandler.get_state(numberOfState - 1)

        if self._is_input_action(lastState=lastState):
            reward = self._get_input_value_reward(
                elementTagName=lastState.get_interacted_element().get_name(),
                inputValue=lastState.get_app_event_input_value())

        if self._is_change_focus_action(lastState=lastState):
            reward = self._get_change_focus_reward()

        if self._is_click_action(lastState=lastState):
            reward = self._get_click_reward()

        if episodeHandler.is_done():
            reward = self._get_episode_done_reward(
                appElements=lastState.get_all_selected_app_elements())

        return reward

    def _is_input_action(self, lastState: State):
        return lastState.get_action_type() == "input"

    def _is_change_focus_action(self, lastState: State):
        return lastState.get_action_type() == "changeFocus"

    def _is_click_action(self, lastState: State):
        return lastState.get_action_type() == "click"

    def _get_input_value_reward(self, elementTagName: str, inputValue: str):
        rewardRevise = 0
        if "name" in elementTagName:
            if inputValue == "Michael Chen":
                rewardRevise = self._inputRewardCoefficient * 1.0
            elif inputValue == "sgfsdg":
                rewardRevise = self._inputRewardCoefficient * 0.5
            else:
                rewardRevise = self._inputRewardCoefficient * 0.25

        if "email" in elementTagName:
            if inputValue == "abc@gmail.com":
                rewardRevise = self._inputRewardCoefficient * 1.0
            else:
                rewardRevise = self._inputRewardCoefficient * 0

        if "password" in elementTagName:
            if (inputValue == "2020/05/29") or (inputValue ==
                                                "0984000000") or (inputValue == "Michael Chen"):
                rewardRevise = self._inputRewardCoefficient * 1

            if (inputValue == "sgfsdg") or (inputValue == "10"):
                rewardRevise = self._inputRewardCoefficient * 0.5

            if inputValue == "abc@gmail.com":
                rewardRevise = self._inputRewardCoefficient * 0.25

        return self._inputRewardBaseLine + rewardRevise

    def _get_change_focus_reward(self):
        return self._changeFocusRewardCoefficient

    def _get_click_reward(self):
        return self._inputRewardBaseLine

    def _get_episode_done_reward(self, appElements: [AppElement]):
        isSuccessed = True
        password = ""
        for appElement in appElements:
            if appElement.get_value() == "":
                isSuccessed = False
            if "email" in appElement.get_name():
                if appElement.get_value() != "abc@gmail.com":
                    isSuccessed = False
            if "password" in appElement.get_name():
                if password is "":
                    password = appElement.get_value()
                elif password != appElement.get_value():
                    isSuccessed = False

        if isSuccessed:
            return self._episodeDoneRewardCoefficient
        else:
            return self._episodeDoneRewardCoefficient * -0.5
