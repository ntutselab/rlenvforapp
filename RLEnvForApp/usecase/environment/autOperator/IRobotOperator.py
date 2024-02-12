import uuid

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.state import AppElement, State
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import \
    AppElementDTOMapper


class IRobotOperator(IAUTOperator):
    def __init__(self, crawler: ICrawler,
                 codeCoverageCollector: ICodeCoverageCollector):
        super().__init__()
        self._crawler = crawler
        self._codeCoverageCollector = codeCoverageCollector
        self._activeUrl = ""
        self._selectedAppElements: [AppElement] = []
        self._interactedElement: AppElement = None
        self._focusedAppElementIndex: int = 0
        self._appEventValue: str = ""

    def get_state(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focusedVector: [bool] = []
        for i in range(0, len(self._selectedAppElements)):
            focusedVector.append(i == self._focusedAppElementIndex)
        state.set_focus_vector(focusedVector)
        state.set_interacted_element(self._interactedElement)
        state.set_selected_app_elements(self._selectedAppElements)
        state.set_url(self._crawler.get_url())
        state.set_dom(self._crawler.get_dom())
        state.set_code_coverages(
            self._mapping_code_coverage_form(codeCoverageDTOs=self._codeCoverageCollector.get_code_coverage_dt_os()))
        state.set_screen_shot(self._crawler.get_screen_shot())
        state.set_action_type(super().get_action_type())
        state.set_app_event_input_value(value=self._appEventValue)
        return state

    def reset_crawler(self, path: str, formXPath: str = ""):
        self._selectedAppElements: [AppElement] = []
        self._focusedAppElementIndex = 0
        self._interactedElement = None
        self._appEventValue = ""
        self._crawler.reset(path=path, formXPath=formXPath)
        self._activeUrl = self._crawler.get_url()
        self._update_all_selected_app_elements()

    def go_to_root_page(self):
        self._crawler.go_to_root_page()

    def execute_app_event(self, xpath: str, value: str):
        self._appEventValue = value
        if xpath == "":
            focusedAppElement = self.get_focused_app_element()
            if focusedAppElement is None:
                return
            xpath = focusedAppElement.get_xpath()
        self._crawler.execute_app_event(xpath=xpath, value=value)

        for i in self._selectedAppElements:
            if i.get_xpath() == xpath:
                self._interactedElement = i
                self._interactedElement.set_value(value)
        self._update_all_selected_app_elements()
        if not (self._activeUrl == self._crawler.get_url()):
            self._activeUrl = self._crawler.get_url()
            self._focusedAppElementIndex = 0

    def change_focus(self):
        if super().get_action_type() == "changeFocus":
            self._interactedElement = self._selectedAppElements[self._focusedAppElementIndex]
        numberOfSelectedAppElement = len(self._selectedAppElements)
        if numberOfSelectedAppElement != 0:
            self._focusedAppElementIndex = (
                self._focusedAppElementIndex + 1) % numberOfSelectedAppElement
        else:
            self._focusedAppElementIndex = 0

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selectedAppElements

    def get_focused_app_element(self) -> AppElement:
        if len(self._selectedAppElements) == 0:
            return None
        if len(self._selectedAppElements) <= self._focusedAppElementIndex:
            self._focusedAppElementIndex = 0

        return self._selectedAppElements[self._focusedAppElementIndex]

    def _update_all_selected_app_elements(self):
        self._selectedAppElements: [AppElement] = []

        inputAppElements: [AppElement] = []
        buttonAppElements: [AppElement] = []
        hyperlinkAppElements: [AppElement] = []
        otherAppElements: [AppElement] = []

        for appElementDTO in self._crawler.get_all_selected_app_elements_dt_os():
            appElement = AppElementDTOMapper.mapping_app_element_from(
                appElementDTO=appElementDTO)
            if "/input" in appElement.get_xpath().lower():
                inputAppElements.append(appElement)
            elif "/button" in appElement.get_xpath().lower():
                buttonAppElements.append(appElement)
            elif "/a" in appElement.get_xpath().lower():
                hyperlinkAppElements.append(appElement)
            else:
                otherAppElements.append(appElement)

        self._selectedAppElements.extend(inputAppElements)
        self._selectedAppElements.extend(buttonAppElements)
        self._selectedAppElements.extend(hyperlinkAppElements)
        self._selectedAppElements.extend(otherAppElements)

    def _mapping_code_coverage_form(self, codeCoverageDTOs: [
                                 CodeCoverageDTO]) -> [CodeCoverage]:
        codeCoverages = []
        for i in codeCoverageDTOs:
            codeCoverages.append(
                CodeCoverage(codeCoverageType=i.get_code_coverage_type(), codeCoverageVector=i.get_code_coverage_vector()))
        return codeCoverages
