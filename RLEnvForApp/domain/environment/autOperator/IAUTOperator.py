from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.State import State


class IAUTOperator:
    def __init__(self):
        self._action_type = ""
        self._action_number = None
        self._state: State = State(id="123456")

    def set_action_type(self, action_type: str):
        self._action_type = action_type

    def get_action_type(self):
        return self._action_type

    def set_action_number(self, actionNumber: int):
        self._action_number = actionNumber

    def get_action_number(self):
        return self._action_number

    def get_state(self) -> State:
        pass

    def reset_crawler(self, path: str, form_xpath: str):
        pass

    def go_to_root_page(self):
        pass

    def execute_app_event(self, xpath: str, value: str):
        pass

    def change_focus(self):
        pass

    def get_all_selected_elements(self) -> [AppElement]:
        pass

    def get_focused_app_element(self) -> AppElement:
        pass
