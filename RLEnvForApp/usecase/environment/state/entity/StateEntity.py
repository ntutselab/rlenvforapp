
from . import AppElementEntity
from .CodeCoverageEntity import CodeCoverageEntity


class StateEntity:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [bool] = [False]
        self._focusVector: [bool] = None
        self._actionType = ""
        self._inputValue = ""
        self._interactedElement = None
        self._selectedAppElementEntities: [AppElementEntity] = []
        self._actionNumber = None
        self._originalObservation = {}

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
        self._screenShot = screenShot

    def get_screen_shot(self):
        return self._screenShot

    def set_code_coverages(self, codeCoverages: [CodeCoverageEntity]):
        self._codeCoverages = codeCoverages

    def get_code_coverages(self) -> [CodeCoverageEntity]:
        return self._codeCoverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def get_focus_vector(self) -> [bool]:
        return self._focusVector

    def set_action_type(self, actionType: str):
        self._actionType = actionType

    def get_action_type(self):
        return self._actionType

    def set_input_value(self, inputValue: str):
        self._inputValue = inputValue

    def get_input_value(self) -> str:
        return self._inputValue

    def set_interacted_element_entity(self, interactedElement: AppElementEntity):
        self._interactedElement = interactedElement

    def get_inter_acted_element_entity(self) -> AppElementEntity:
        return self._interactedElement

    def set_selected_app_element_entities(
            self, selectedAppElementEntities: [AppElementEntity]):
        self._selectedAppElementEntities = selectedAppElementEntities

    def get_selected_app_element_entities(self) -> [AppElementEntity]:
        return self._selectedAppElementEntities

    def set_action_number(self, actionNumber: int):
        self._actionNumber = actionNumber

    def get_action_number(self) -> int:
        return self._actionNumber

    def set_original_observation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def get_original_observation(self) -> dict:
        return self._originalObservation
