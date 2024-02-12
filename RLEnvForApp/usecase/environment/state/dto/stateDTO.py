from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class StateDTO:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [bool] = [False]
        self._focusVector: [bool] = None
        self._actionType = ""
        self._value = ""
        self._interactedElement = None
        self._selectedAppElementDTOs: [AppElementDTO] = []

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

    def set_code_coverages(self, codeCoverages: [CodeCoverageDTO]):
        self._codeCoverages = codeCoverages

    def get_code_coverages(self) -> [CodeCoverageDTO]:
        return self._codeCoverages

    def set_focus_vector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def get_focus_vector(self) -> [bool]:
        return self._focusVector

    def set_action_type(self, actionType: str):
        self._actionType = actionType

    def get_action_type(self):
        return self._actionType

    def set_app_event_value(self, value: str):
        self._value = value

    def get_app_event_value(self) -> str:
        return self._value

    def set_interacted_element_dto(self, interactedElement: AppElementDTO):
        self._interactedElement = interactedElement

    def get_inter_acted_element_dto(self) -> AppElementDTO:
        return self._interactedElement

    def set_selected_app_element_dt_os(
            self, selectedAppElementEntities: [AppElementDTO]):
        self._selectedAppElementDTOs = selectedAppElementEntities

    def get_selected_app_element_dt_os(self) -> [AppElementDTO]:
        return self._selectedAppElementDTOs
