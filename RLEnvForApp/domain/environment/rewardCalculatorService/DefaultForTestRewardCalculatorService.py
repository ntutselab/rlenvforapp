from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.rewardCalculatorService.IRewardCalculatorService import \
    IRewardCalculatorService
from RLEnvForApp.domain.environment.state import AppElement, State


class DefaultForTestRewardCalculatorService(IRewardCalculatorService):
    def __init__(self):
        super().__init__()
        self._episode_done_reward_coefficient: float = 50
        self._change_focus_reward_coefficient: float = -1

        self._input_reward_coefficient: float = 3.5
        self._input_reward_base_line: float = -3

    def calculate_reward(self, episode_handler: IEpisodeHandler):
        reward = 0.0
        number_of_state = episode_handler.get_number_of_state()
        last_state = episode_handler.get_state(number_of_state - 1)

        if self._is_input_action(last_state=last_state):
            reward = self._get_input_value_reward(
                elementTagName=last_state.get_interacted_element().get_name(),
                inputValue=last_state.get_app_event_input_value())

        if self._is_change_focus_action(last_state=last_state):
            reward = self._get_change_focus_reward()

        if self._is_click_action(last_state=last_state):
            reward = self._get_click_reward()

        if episode_handler.is_done():
            reward = self._get_episode_done_reward(
                app_elements=last_state.get_all_selected_app_elements())

        return reward

    def _is_input_action(self, last_state: State):
        return last_state.get_action_type() == "input"

    def _is_change_focus_action(self, last_state: State):
        return last_state.get_action_type() == "changeFocus"

    def _is_click_action(self, last_state: State):
        return last_state.get_action_type() == "click"

    def _get_input_value_reward(self, elementTagName: str, inputValue: str):
        reward_revise = 0
        if "name" in elementTagName:
            if inputValue == "Michael Chen":
                reward_revise = self._input_reward_coefficient * 1.0
            elif inputValue == "sgfsdg":
                reward_revise = self._input_reward_coefficient * 0.5
            else:
                reward_revise = self._input_reward_coefficient * 0.25

        if "email" in elementTagName:
            if inputValue == "abc@gmail.com":
                reward_revise = self._input_reward_coefficient * 1.0
            else:
                reward_revise = self._input_reward_coefficient * 0

        if "password" in elementTagName:
            if (inputValue == "2020/05/29") or (inputValue ==
                                                "0984000000") or (inputValue == "Michael Chen"):
                reward_revise = self._input_reward_coefficient * 1

            if (inputValue == "sgfsdg") or (inputValue == "10"):
                reward_revise = self._input_reward_coefficient * 0.5

            if inputValue == "abc@gmail.com":
                reward_revise = self._input_reward_coefficient * 0.25

        return self._input_reward_base_line + reward_revise

    def _get_change_focus_reward(self):
        return self._change_focus_reward_coefficient

    def _get_click_reward(self):
        return self._input_reward_base_line

    def _get_episode_done_reward(self, app_elements: [AppElement]):
        is_successed = True
        password = ""
        for app_element in app_elements:
            if app_element.get_value() == "":
                is_successed = False
            if "email" in app_element.get_name():
                if app_element.get_value() != "abc@gmail.com":
                    is_successed = False
            if "password" in app_element.get_name():
                if password is "":
                    password = app_element.get_value()
                elif password != app_element.get_value():
                    is_successed = False

        if is_successed:
            return self._episode_done_reward_coefficient
        else:
            return self._episode_done_reward_coefficient * -0.5
