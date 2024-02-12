import uuid

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.state import AppElement, State
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.mapper import \
    AppElementDTOMapper


class DefaultHtmlFileOperator(IAUTOperator):
    def __init__(self, crawler: ICrawler):
        super().__init__()
        self._crawler = crawler
        self._submitElement: AppElement = None
        self._selectedAppElements: [AppElement] = []
        self._interactedElementIndex: int = 0
        self._focusedAppElementIndex: int = 0
        self._appEventValue: str = ""

    def get_state(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focusedVector: [bool] = []
        for i in range(0, len(self._selectedAppElements)):
            focusedVector.append(i == self._focusedAppElementIndex)

        state.set_dom(self._crawler.get_dom())
        state.set_selected_app_elements(self._selectedAppElements)
        state.set_action_type(super().get_action_type())
        state.set_app_event_input_value(value=self._appEventValue)
        state.set_interacted_element(
            self._selectedAppElements[self._interactedElementIndex])
        state.set_focus_vector(focusedVector)
        return state

    def reset_crawler(self, path: str, formXPath: str = ""):
        self._crawler.reset(path=path, formXPath=formXPath)
        self._set_selected_app_element()
        self._focusedAppElementIndex = 0
        self._appEventValue = ""

    def go_to_root_page(self):
        self._crawler.go_to_root_page()

    def execute_app_event(self, xpath: str, value: str):
        self._interactedElementIndex = self._focusedAppElementIndex
        self._appEventValue = value
        if xpath == "" and value == "":
            self._click_submit_button()
        elif xpath == "" and value != "":
            self._input_value(
                xpath=self.get_focused_app_element().get_xpath(),
                value=value)
        else:
            self._input_value(xpath=xpath, value=value)

    def change_focus(self):
        numberOfSelectedAppElement = len(self._selectedAppElements)
        self._focusedAppElementIndex = (
            self._focusedAppElementIndex + 1) % numberOfSelectedAppElement

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selectedAppElements

    def get_focused_app_element(self) -> AppElement:
        return self._selectedAppElements[self._focusedAppElementIndex]

    def _set_selected_app_element(self):
        self._selectedAppElements: [AppElement] = []

        for appElementDTO in self._crawler.get_all_selected_app_elements_dt_os():
            appElement = AppElementDTOMapper.mapping_app_element_from(
                appElementDTO=appElementDTO)
            if appElement.get_tag_name() == "input":
                self._selectedAppElements.append(appElement)
            elif appElement.get_type() == "submit":
                self._submitElement = appElement

    def _click_submit_button(self):
        self._crawler.execute_app_event(self._submitElement.get_xpath(), "")

    def _input_value(self, xpath: str, value: str):
        self._crawler.execute_app_event(xpath=xpath, value=value)
        self._set_selected_app_element()
