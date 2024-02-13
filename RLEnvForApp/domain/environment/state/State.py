from RLEnvForApp.domain.environment.observationService.htmlExtractor.HtmlExtractor import \
    HtmlExtractor
from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class State:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screen_shot = None
        self._code_coverages: [CodeCoverage] = []
        self._focus_vector: [bool] = None
        self._action_type = ""
        self._input_value = ""
        self._interacted_element = None
        self._selected_app_elements: [AppElement] = []
        self._action_number = None
        self._original_observation = {}

    def get_id(self):
        return self._id

    def set_dom(self, DOM: str):
        self._dom = DOM

    def get_dom(self):
        return self._dom

    def set_url(self, url: str):
        self._url = url

    def get_url(self):
        return self._url

    def set_screen_shot(self, screenShot):
        self._screen_shot = screenShot

    def get_screen_shot(self):
        return self._screen_shot

    def set_code_coverages(self, code_coverages: [CodeCoverage]):
        self._code_coverages = code_coverages

    def get_code_coverages(self) -> [CodeCoverage]:
        return self._code_coverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focus_vector = focusVector

    def get_focus_vector(self):
        return self._focus_vector

    def set_action_type(self, action_type: str):
        self._action_type = action_type

    def get_action_type(self):
        return self._action_type

    def set_app_event_input_value(self, value: str):
        self._input_value = value

    def get_app_event_input_value(self):
        return self._input_value

    def set_interacted_element(self, interactedElement: AppElement):
        self._interacted_element = interactedElement

    def get_interacted_element(self) -> AppElement:
        return self._interacted_element

    def get_interacted_element_label(self) -> str:
        return HtmlExtractor().get_label_name(self._dom, self._interacted_element.get_xpath())

    def get_interacted_element_placeholder(self) -> str:
        return HtmlExtractor().get_placeholder(
            self._dom, self._interacted_element.get_xpath())

    def set_selected_app_elements(self, app_elements: [AppElement]):
        self._selected_app_elements = app_elements

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selected_app_elements

    def set_action_number(self, actionNumber: int):
        self._action_number = actionNumber

    def get_action_number(self) -> int:
        return self._action_number

    def set_original_observation(self, originalObservation: dict):
        self._original_observation = originalObservation

    def get_original_observation(self) -> dict:
        return self._original_observation

    def is_selected_app_elements_empty(self) -> bool:
        return len(self._selected_app_elements) == 0
