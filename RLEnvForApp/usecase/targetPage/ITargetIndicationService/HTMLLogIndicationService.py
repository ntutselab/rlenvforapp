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

    def isConform(self, state: State) -> bool:
        appElements: [AppElement] = state.getAllSelectedAppElements()

        path = state.getUrl()
        folderPath, pageHTMLFileName = os.path.split(path)
        pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"
        jsonData = open(os.path.join(folderPath, pageJsonFileName), )
        pageLog = json.load(jsonData)
        jsonData.close()
        logAppEvents = pageLog["appEvent"]

        isInteractedElementSubmit = state.getInteractedElement().getType() == "submit"
        isClick = state.getActionType() == "click"

        if not (isInteractedElementSubmit and isClick):
            Logger().info("The last action is not clicking on the submit button.")
            return False

        for logAppEvent in logAppEvents:
            appElement = self._findAppElementByXpath(
                appElements=appElements, xpath=logAppEvent)
            if appElement is None:
                Logger().info(f"xpath in record not found: {logAppEvent}")
                return False
            if appElement.getTagName() == "input" and \
                    (appElement.getType() == "button" or appElement.getType() == "submit"):
                continue

            actionCategory = self._findCategoryByValue(appElement.getValue())
            if actionCategory != logAppEvents[logAppEvent]['category']:
                Logger().info(f"Category not match, element xpath")
                return False

        Logger().info("All input field category match record")
        return True

    def _findAppElementByXpath(self, appElements: [AppElement], xpath):
        replaceXpath = xpath.replace("[1]", "")
        for appElement in appElements:
            appElementXpath = appElement.getXpath().replace("[1]", "")
            if appElementXpath == replaceXpath:
                return appElement

    def _findCategoryByValue(self, inputValue: str) -> str:
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
