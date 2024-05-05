from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.logger.logger import Logger

from . import IActionCommand


class NosuchElementException(Exception):
    pass


class InitiateToTargetActionCommand(IActionCommand.IActionCommand):
    def __init__(self, appEvents: [AppEvent], rootPath: str, formXPath: str):
        super().__init__(actionNumber=-1, actionType="init")
        self._appEvents = appEvents
        self._rootPath = rootPath
        self._formXPath = formXPath

    def execute(self, operator: IAUTOperator):
        operator.setActionType(super().getActionType())
        isSuccess = False
        retry = 0
        while not isSuccess:
            try:
                Logger().info("Initialize the crawler to the target page")
                Logger().info(f"Root path: {self._rootPath}")
                Logger().info(f"Form XPath: {self._formXPath}")
                operator.resetCrawler(self._rootPath, self._formXPath)
                Logger().info("=====start the initial action=====")
                for appEvent in self._appEvents:
                    Logger().info(f"Xpath: {appEvent.getXpath()}, value: {appEvent.getValue()}")
                    operator.executeAppEvent(xpath=appEvent.getXpath(), value=appEvent.getValue())
                isSuccess = True
            except Exception as exception:
                Logger().info(f"InitiateToTargetActionCommand Exception, {exception}")
                retry += 1
            if retry >= 10:
                raise NosuchElementException("InitiateToTargetActionCommand Exception, retry 10 times")
