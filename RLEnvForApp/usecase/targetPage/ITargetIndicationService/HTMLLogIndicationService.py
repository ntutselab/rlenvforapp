import json
import os

from RLEnvForApp.domain.environment.inputSpace import inputTypes, inputValues
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.targetPage.TargetIndicationService.ITargetIndicationService import \
    ITargetIndicationService
from RLEnvForApp.logger.logger import Logger


class HTMLLogIndicationService(ITargetIndicationService):
    def __init__(self):
        super().__init__()

    def is_conform(self, state: State) -> bool:
        app_elements: [AppElement] = state.get_all_selected_app_elements()

        path = state.get_url()
        folder_path, pageHTMLFileName = os.path.split(path)
        page_json_file_name = os.path.splitext(pageHTMLFileName)[0] + ".json"
        json_data = open(os.path.join(folder_path, page_json_file_name), )
        page_log = json.load(json_data)
        json_data.close()
        log_app_events = page_log["appEvent"]

        is_interacted_element_submit = state.get_interacted_element().get_type() == "submit"
        is_click = state.get_action_type() == "click"

        if not (is_interacted_element_submit and is_click):
            Logger().info("The last action is not clicking on the submit button.")
            return False

        for logAppEvent in log_app_events:
            app_element = self._find_app_element_by_xpath(
                app_elements=app_elements, xpath=logAppEvent)
            if app_element is None:
                Logger().info(f"xpath in record not found: {logAppEvent}")
                return False
            if app_element.get_tag_name() == "input" and \
                    (app_element.get_type() == "button" or app_element.get_type() == "submit"):
                continue

            action_category = self._find_category_by_value(app_element.get_value())
            if action_category != log_app_events[logAppEvent]['category']:
                Logger().info(f"Category not match, element xpath")
                return False

        Logger().info("All input field category match record")
        return True

    def _find_app_element_by_xpath(self, app_elements: [AppElement], xpath):
        replace_xpath = xpath.replace("[1]", "")
        for app_element in app_elements:
            appElementXpath = app_element.get_xpath().replace("[1]", "")
            if appElementXpath == replace_xpath:
                return app_element

    def _find_category_by_value(self, inputValue: str) -> str:
        input_value_index = -1
        if inputValue == '':
            return 'click'

        for i, values in enumerate(inputValues):
            if inputValue in values:
                input_value_index = i
                break

        if input_value_index == -1:
            return ''

        return inputTypes[input_value_index]
