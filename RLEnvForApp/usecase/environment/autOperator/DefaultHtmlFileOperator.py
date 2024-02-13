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
        self._submit_element: AppElement = None
        self._selected_app_elements: [AppElement] = []
        self._interacted_element_index: int = 0
        self._focused_app_element_index: int = 0
        self._app_event_value: str = ""

    def get_state(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focused_vector: [bool] = []
        for i in range(0, len(self._selected_app_elements)):
            focused_vector.append(i == self._focused_app_element_index)

        state.set_dom(self._crawler.get_dom())
        state.set_selected_app_elements(self._selected_app_elements)
        state.set_action_type(super().get_action_type())
        state.set_app_event_input_value(value=self._app_event_value)
        state.set_interacted_element(
            self._selected_app_elements[self._interacted_element_index])
        state.set_focus_vector(focused_vector)
        return state

    def reset_crawler(self, path: str, form_x_path: str = ""):
        self._crawler.reset(path=path, form_x_path=form_x_path)
        self._set_selected_app_element()
        self._focused_app_element_index = 0
        self._app_event_value = ""

    def go_to_root_page(self):
        self._crawler.go_to_root_page()

    def execute_app_event(self, xpath: str, value: str):
        self._interacted_element_index = self._focused_app_element_index
        self._app_event_value = value
        if xpath == "" and value == "":
            self._click_submit_button()
        elif xpath == "" and value != "":
            self._input_value(
                xpath=self.get_focused_app_element().get_xpath(),
                value=value)
        else:
            self._input_value(xpath=xpath, value=value)

    def change_focus(self):
        number_of_selected_app_element = len(self._selected_app_elements)
        self._focused_app_element_index = (
            self._focused_app_element_index + 1) % number_of_selected_app_element

    def get_all_selected_app_elements(self) -> [AppElement]:
        return self._selected_app_elements

    def get_focused_app_element(self) -> AppElement:
        return self._selected_app_elements[self._focused_app_element_index]

    def _set_selected_app_element(self):
        self._selected_app_elements: [AppElement] = []

        for app_element_dto in self._crawler.get_all_selected_app_elements_dt_os():
            app_element = AppElementDTOMapper.mapping_app_element_from(
                app_element_dto=app_element_dto)
            if app_element.get_tag_name() == "input":
                self._selected_app_elements.append(app_element)
            elif app_element.get_type() == "submit":
                self._submit_element = app_element

    def _click_submit_button(self):
        self._crawler.execute_app_event(self._submit_element.get_xpath(), "")

    def _input_value(self, xpath: str, value: str):
        self._crawler.execute_app_event(xpath=xpath, value=value)
        self._set_selected_app_element()
