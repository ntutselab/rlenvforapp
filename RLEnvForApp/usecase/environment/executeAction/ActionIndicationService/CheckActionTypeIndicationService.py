from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State


class CheckActionTypeIndicationService(IActionIndicationService):
    def __init__(self):
        super().__init__()

    def is_conform(self, state: State):
        action_type = state.get_action_type()
        interacted_app_element = state.get_interacted_element()

        if action_type == "input":
            return self._is_valid_input_action(app_element=interacted_app_element)
        if action_type == "click":
            return self._is_valid_click_action(app_element=interacted_app_element)
        if action_type == "changeFocus":
            return self._is_valid_change_focus_action(
                app_element=interacted_app_element)

        return False

    def _is_valid_input_action(self, app_element: AppElement):
        if app_element and app_element.get_tag_name(
        ) and app_element.get_tag_name().lower() == "input":
            return True
        else:
            return False

    def _is_valid_click_action(self, app_element: AppElement):
        if app_element and app_element.get_type() and app_element.get_type().lower() == "submit":
            return True
        else:
            return False

    def _is_valid_change_focus_action(self, app_element: AppElement):
        is_valid_input_action = self._is_valid_input_action(app_element=app_element)
        is_valid_click_action = self._is_valid_click_action(app_element=app_element)
        return not (is_valid_click_action or is_valid_input_action)
