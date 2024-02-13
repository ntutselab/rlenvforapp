from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.logger.logger import Logger

from . import IActionCommand


class InitiateToTargetActionCommand(IActionCommand.IActionCommand):
    def __init__(self, app_events: [AppEvent], rootPath: str, form_xpath: str):
        super().__init__(actionNumber=-1, action_type="init")
        self._app_events = app_events
        self._root_path = rootPath
        self._form_xpath = form_xpath

    def execute(self, operator: IAUTOperator):
        operator.set_action_type(super().get_action_type())
        is_success = False
        retry = 0
        while not is_success:
            try:
                Logger().info("Initialize the crawler to the target page")
                Logger().info(f"Root path: {self._rootPath}")
                Logger().info(f"Form XPath: {self._formXPath}")
                operator.reset_crawler(self._root_path, self._form_xpath)
                Logger().info("=====start the initial action=====")
                for app_event in self._app_events:
                    Logger().info(
                        f"Xpath: {appEvent.getXpath()}, value: {appEvent.getValue()}")
                    operator.execute_app_event(
                        xpath=app_event.get_xpath(), value=app_event.get_value())
                is_success = True
            except Exception as e:
                Logger().info(f"InitiateToTargetActionCommand Exception, {e}")
                retry += 1
            if retry >= 10:
                raise RuntimeError
