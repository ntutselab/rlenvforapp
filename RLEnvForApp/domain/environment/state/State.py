from RLEnvForApp.domain.environment.observationService.htmlExtractor.HtmlExtractor import \
    HtmlExtractor
from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class State:
    def __init__(self, id: str):
        self._id = id
        self._DOM: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [CodeCoverage] = []
        self._focusVector: [bool] = None
        self._actionType = ""
        self._inputValue = ""
        self._interactedElement = None
        self._selectedAppElements: [AppElement] = []
        self._actionNumber = None
        self._originalObservation = {}

    def get_id(self):
        return self._id

    def set_dom(self, DOM: str):
        self._DOM = DOM

    def get_dom(self):
        return self._DOM

    def set_url(self, url: str):
        self._url = url

    def get_url(self):
        return self._url

    def set_screen_shot(self, screenShot):
        self._screenShot = screenShot

    def get_screen_shot(self):
        return self._screenShot

    def set_code_coverages(self, codeCoverages: [CodeCoverage]):
        self._codeCoverages = codeCoverages

    def get_code_coverages(self) -> [CodeCoverage]:
        return self._codeCoverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def get_focus_vector(self):
        return self._focusVector

    def set_action_type(self, actionType: str):
        self._actionType = actionType

    def get_action_type(self):
        return self._actionType

    def set_app_event_input_value(self, value: str):
        self._inputValue = value

    def get_app_event_input_value(self):
        return self._inputValue

    def set_interacted_element(self, interactedElement: AppElement):
        self._interactedElement = interactedElement

    def get_interacted_element(self) -> AppElement:
        return self._interactedElement

    def get_interacted_element_label(self) -> str:
        return HtmlExtractor().get_label_name(self._DOM, self._interactedElement.get_xpath())

    def get_interacted_element_placeholder(self) -> str:
        return HtmlExtractor().get_placeholder(
            self._DOM, self._interactedElement.get_xpath())

    def set_selected_app_elements(self, appElements: [AppElement]):
        self._selectedAppElements = appElements

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selectedAppElements

    def set_action_number(self, actionNumber: int):
        self._actionNumber = actionNumber

    def get_action_number(self) -> int:
        return self._actionNumber

    def set_original_observation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def get_original_observation(self) -> dict:
        return self._originalObservation

    def is_selected_app_elements_empty(self) -> bool:
        return len(self._selectedAppElements) == 0
