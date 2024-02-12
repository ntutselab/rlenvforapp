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
        appElements: [AppElement] = state.get_all_selected_app_elements()

        path = state.get_url()
        folderPath, pageHTMLFileName = os.path.split(path)
        pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"
        jsonData = open(os.path.join(folderPath, pageJsonFileName), )
        pageLog = json.load(jsonData)
        jsonData.close()
        logAppEvents = pageLog["appEvent"]

        isInteractedElementSubmit = state.get_interacted_element().get_type() == "submit"
        isClick = state.get_action_type() == "click"

        if not (isInteractedElementSubmit and isClick):
            Logger().info("The last action is not clicking on the submit button.")
            return False

        for logAppEvent in logAppEvents:
            appElement = self._find_app_element_by_xpath(
                appElements=appElements, xpath=logAppEvent)
            if appElement is None:
                Logger().info(f"xpath in record not found: {logAppEvent}")
                return False
            if appElement.get_tag_name() == "input" and \
                    (appElement.get_type() == "button" or appElement.get_type() == "submit"):
                continue

            actionCategory = self._find_category_by_value(appElement.get_value())
            if actionCategory != logAppEvents[logAppEvent]['category']:
                Logger().info(f"Category not match, element xpath")
                return False

        Logger().info("All input field category match record")
        return True

    def _find_app_element_by_xpath(self, appElements: [AppElement], xpath):
        replaceXpath = xpath.replace("[1]", "")
        for appElement in appElements:
            appElementXpath = appElement.get_xpath().replace("[1]", "")
            if appElementXpath == replaceXpath:
                return appElement

    def _find_category_by_value(self, inputValue: str) -> str:
        inputValueIndex = -1
        if inputValue == '':
            return 'click'

        for i, values in enumerate(inputValues):
            if inputValue in values:
                inputValueIndex = i
                break

        if inputValueIndex == -1:
            return ''

        return inputTypes[inputValueIndex]
