import time
import uuid

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.state import AppElement, State
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import \
    AppElementDTOMapper


class AIGUIDEOperator(IAUTOperator):
    def __init__(self, crawler: ICrawler,
                 code_coverage_collector: ICodeCoverageCollector = ICodeCoverageCollector()):
        super().__init__()
        self._crawler = crawler
        self._code_coverage_collector = code_coverage_collector
        self._active_url = ""
        self._selected_app_elements: [AppElement] = []
        self._interacted_element: AppElement = None
        self._focused_app_element_index: int = 0
        self._app_event_value: str = ""

    def get_state(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focused_vector: [bool] = []
        for i in range(0, len(self._selected_app_elements)):
            focused_vector.append(i == self._focused_app_element_index)
        state.set_focus_vector(focused_vector)
        state.set_interacted_element(self.get_focused_app_element())
        state.set_selected_app_elements(self._selected_app_elements)
        state.set_url(self._crawler.get_url())
        state.set_dom(self._crawler.get_dom())
        state.set_code_coverages(
            self._mapping_code_coverage_form(code_coverage_dt_os=self._code_coverage_collector.get_code_coverage_dt_os()))
        state.set_screen_shot(self._crawler.get_screen_shot())
        return state

    def reset_crawler(self, rootPath: str, form_x_path: str):
        self._selected_app_elements: [AppElement] = []
        self._focused_app_element_index = 0
        self._interacted_element = None
        self._app_event_value = ""
        self._crawler.reset(rootPath=rootPath, form_x_path=form_x_path)
        self._active_url = self._crawler.get_url()
        self._update_all_selected_app_elements()

    def go_to_root_page(self):
        self._crawler.go_to_root_page()

    def execute_app_event(self, xpath: str, value: str):
        self._app_event_value = value
        if xpath == "":
            focused_app_element = self.get_focused_app_element()
            if focused_app_element is None:
                return
            xpath = focused_app_element.get_xpath()
        self._crawler.execute_app_event(xpath=xpath, value=value)

        for i in self._selected_app_elements:
            if i.get_xpath() == xpath:
                self._interacted_element = i
                self._interacted_element.set_value(value)
        self._update_all_selected_app_elements()
        if not (self._active_url == self._crawler.get_url()):
            self._active_url = self._crawler.get_url()
            self._focused_app_element_index = 0

    def change_focus(self):
        if super().get_action_type() == "changeFocus":
            focused_app_element: AppElement = self.get_focused_app_element()
            focused_app_element.set_value("")
            self._crawler.change_focus(focused_app_element.get_xpath(), "")
            self._interacted_element = self._selected_app_elements[self._focused_app_element_index]
        number_of_selected_app_element = len(self._selected_app_elements)
        if number_of_selected_app_element != 0:
            self._focused_app_element_index = (
                self._focused_app_element_index + 1) % number_of_selected_app_element
        else:
            self._focused_app_element_index = 0

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selected_app_elements

    def get_focused_app_element(self) -> AppElement:
        if len(self._selected_app_elements) == 0:
            return None
        if len(self._selected_app_elements) <= self._focused_app_element_index:
            self._focused_app_element_index = 0

        return self._selected_app_elements[self._focused_app_element_index]

    def _update_all_selected_app_elements(self):
        self._selected_app_elements: [AppElement] = []

        input_app_elements: [AppElement] = []
        button_app_elements: [AppElement] = []
        hyperlink_app_elements: [AppElement] = []
        other_app_elements: [AppElement] = []

        for app_element_dto in self._get_app_element_dt_os(retry=10):
            app_element = AppElementDTOMapper.mapping_app_element_from(
                app_element_dto=app_element_dto)
            if "/input" in app_element.get_xpath().lower():
                input_app_elements.append(app_element)
            elif "/button" in app_element.get_xpath().lower():
                button_app_elements.append(app_element)
            elif "/a" in app_element.get_xpath().lower():
                hyperlink_app_elements.append(app_element)
            else:
                other_app_elements.append(app_element)

        self._selected_app_elements.extend(input_app_elements)
        self._selected_app_elements.extend(hyperlink_app_elements)
        self._selected_app_elements.extend(other_app_elements)
        self._selected_app_elements.extend(button_app_elements)

    def _mapping_code_coverage_form(self, code_coverage_dt_os: [
                                 CodeCoverageDTO]) -> [CodeCoverage]:
        code_coverages = []
        for i in code_coverage_dt_os:
            code_coverages.append(
                CodeCoverage(code_coverage_type=i.get_code_coverage_type(), code_coverage_vector=i.get_code_coverage_vector()))
        return code_coverages

    def _get_app_element_dt_os(self, retry: int):
        app_element_dt_os: [AppElementDTO] = []
        is_retry = True
        retry_times = 0

        while (is_retry):
            try:
                app_element_dt_os = self._crawler.get_all_selected_app_elements_dt_os()
                is_retry = False
            except BaseException:
                time.sleep(1)
                retry_times += 1
                is_retry = retry_times < retry
        return app_element_dt_os
