from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class StateDTO:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screen_shot = None
        self._code_coverages: [bool] = [False]
        self._focus_vector: [bool] = None
        self._action_type = ""
        self._value = ""
        self._interacted_element = None
        self._selected_app_element_dt_os: [AppElementDTO] = []

    def get_id(self):
        return self._id

    def set_dom(self, dom: str):
        self._dom = dom

    def get_dom(self) -> str:
        return self._dom

    def set_url(self, url: str):
        self._url = url

    def get_url(self) -> str:
        return self._url

    def set_screen_shot(self, screenShot):
        self._screen_shot = screenShot

    def get_screen_shot(self):
        return self._screen_shot

    def set_code_coverages(self, code_coverages: [CodeCoverageDTO]):
        self._code_coverages = code_coverages

    def get_code_coverages(self) -> [CodeCoverageDTO]:
        return self._code_coverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focus_vector = focusVector

    def get_focus_vector(self) -> [bool]:
        return self._focus_vector

    def set_action_type(self, action_type: str):
        self._action_type = action_type

    def get_action_type(self):
        return self._action_type

    def set_app_event_value(self, value: str):
        self._value = value

    def get_app_event_value(self) -> str:
        return self._value

    def set_interacted_element_dto(self, interactedElement: AppElementDTO):
        self._interacted_element = interactedElement

    def get_inter_acted_element_dto(self) -> AppElementDTO:
        return self._interacted_element

    def set_selected_app_element_dt_os(
            self, selectedAppElementEntities: [AppElementDTO]):
        self._selected_app_element_dt_os = selectedAppElementEntities

    def get_selected_app_element_dt_os(self) -> [AppElementDTO]:
        return self._selected_app_element_dt_os
