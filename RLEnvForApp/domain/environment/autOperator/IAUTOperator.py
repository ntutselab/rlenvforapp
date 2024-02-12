from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.State import State


class IAUTOperator:
    def __init__(self):
        self._actionType = ""
        self._actionNumber = None
        self._state: State = State(id="123456")

    def set_action_type(self, actionType: str):
        self._actionType = actionType

    def get_action_type(self):
        return self._actionType

    def set_action_number(self, actionNumber: int):
        self._actionNumber = actionNumber

    def get_action_number(self):
        return self._actionNumber

    def get_state(self) -> State:
        pass

    def reset_crawler(self, path: str, formXPath: str):
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
