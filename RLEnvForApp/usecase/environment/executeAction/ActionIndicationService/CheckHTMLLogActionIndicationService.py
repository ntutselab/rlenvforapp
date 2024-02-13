import json
import os

from RLEnvForApp.domain.environment.inputSpace import inputTypes
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import \
    IActionIndicationService
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.logger.logger import Logger


class CheckHTMLLogActionIndicationService(IActionIndicationService):
    def __init__(self):
        super().__init__()

    def is_conform(self, state: State):
        interacted_app_element: AppElement = state.get_interacted_element()
        interacted_app_element_xpath = interacted_app_element.get_xpath().replace(
            "[1]", "")

        path = state.get_url()
        folder_path, pageHTMLFileName = os.path.split(path)
        page_json_file_name = os.path.splitext(pageHTMLFileName)[0] + ".json"
        json_data = open(os.path.join(folder_path, page_json_file_name),)
        page_log = json.load(json_data)
        json_data.close()
        page_log_app_events = page_log["appEvent"]

        log_app_events = {}
        for logAppEvent in page_log_app_events:
            log_app_events[logAppEvent.replace(
                "[1]", "")] = page_log_app_events[logAppEvent]

        if interacted_app_element_xpath not in log_app_events:
            Logger().info(
                f"Xpath not found in record: {interactedAppElementXpath}")
            return False

        action_category = inputTypes[state.get_action_number()]
        if action_category != log_app_events[interacted_app_element_xpath]['category']:
            Logger().info(f"Category not match, element xpath")
            return False

        Logger().info("Input field category match record")
        return True
