import json
import os

from RLEnvForApp.domain.environment.inputSpace import inputTypes
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import IActionIndicationService
from RLEnvForApp.logger.logger import Logger


class CheckHTMLLogActionIndicationService(IActionIndicationService):
    def __init__(self):
        super().__init__()

    def isConform(self, state: State):
        interactedAppElement: AppElement = state.getInteractedElement()
        interactedAppElementXpath = interactedAppElement.getXpath().replace("[1]", "")

        path = state.getUrl()
        folderPath, pageHTMLFileName = os.path.split(path)
        pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"
        jsonData = open(os.path.join(folderPath, pageJsonFileName),)
        pageLog = json.load(jsonData)
        jsonData.close()
        pageLogAppEvents = pageLog["appEvent"]

        logAppEvents = {}
        for logAppEvent in pageLogAppEvents:
            logAppEvents[logAppEvent.replace("[1]", "")] = pageLogAppEvents[logAppEvent]

        if interactedAppElementXpath not in logAppEvents:
            Logger().info(f"Xpath not found in record: {interactedAppElementXpath}")
            return False

        actionCategory = inputTypes[state.getActionNumber()]
        if actionCategory != logAppEvents[interactedAppElementXpath]['category']:
            Logger().info(f"Category not match, element xpath")
            return False

        Logger().info("Input field category match record")
        return True
