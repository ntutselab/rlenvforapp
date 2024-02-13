
from . import AppElementEntity
from .CodeCoverageEntity import CodeCoverageEntity


class StateEntity:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screen_shot = None
        self._code_coverages: [bool] = [False]
        self._focus_vector: [bool] = None
        self._action_type = ""
        self._input_value = ""
        self._interacted_element = None
        self._selected_app_element_entities: [AppElementEntity] = []
        self._action_number = None
        self._original_observation = {}

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

    def set_code_coverages(self, code_coverages: [CodeCoverageEntity]):
        self._code_coverages = code_coverages

    def get_code_coverages(self) -> [CodeCoverageEntity]:
        return self._code_coverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focus_vector = focusVector

    def get_focus_vector(self) -> [bool]:
        return self._focus_vector

    def set_action_type(self, action_type: str):
        self._action_type = action_type

    def get_action_type(self):
        return self._action_type

    def set_input_value(self, inputValue: str):
        self._input_value = inputValue

    def get_input_value(self) -> str:
        return self._input_value

    def set_interacted_element_entity(self, interactedElement: AppElementEntity):
        self._interacted_element = interactedElement

    def get_inter_acted_element_entity(self) -> AppElementEntity:
        return self._interacted_element

    def set_selected_app_element_entities(
            self, selectedAppElementEntities: [AppElementEntity]):
        self._selected_app_element_entities = selectedAppElementEntities

    def get_selected_app_element_entities(self) -> [AppElementEntity]:
        return self._selected_app_element_entities

    def set_action_number(self, actionNumber: int):
        self._action_number = actionNumber

    def get_action_number(self) -> int:
        return self._action_number

    def set_original_observation(self, originalObservation: dict):
        self._original_observation = originalObservation

    def get_original_observation(self) -> dict:
        return self._original_observation
