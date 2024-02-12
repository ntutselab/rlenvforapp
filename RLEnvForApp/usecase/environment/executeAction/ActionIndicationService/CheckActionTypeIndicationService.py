from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State


class CheckActionTypeIndicationService(IActionIndicationService):
    def __init__(self):
        super().__init__()

    def is_conform(self, state: State):
        actionType = state.get_action_type()
        interactedAppElement = state.get_interacted_element()

        if actionType == "input":
            return self._is_valid_input_action(appElement=interactedAppElement)
        if actionType == "click":
            return self._is_valid_click_action(appElement=interactedAppElement)
        if actionType == "changeFocus":
            return self._is_valid_change_focus_action(
                appElement=interactedAppElement)

        return False

    def _is_valid_input_action(self, appElement: AppElement):
        if appElement and appElement.get_tag_name(
        ) and appElement.get_tag_name().lower() == "input":
            return True
        else:
            return False

    def _is_valid_click_action(self, appElement: AppElement):
        if appElement and appElement.get_type() and appElement.get_type().lower() == "submit":
            return True
        else:
            return False

    def _is_valid_change_focus_action(self, appElement: AppElement):
        isValidInputAction = self._is_valid_input_action(appElement=appElement)
        isValidClickAction = self._is_valid_click_action(appElement=appElement)
        return not (isValidClickAction or isValidInputAction)
