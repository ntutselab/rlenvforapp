from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.State import State


class IAUTOperator:
    def __init__(self):
        self._actionType = ""
        self._actionNumber = None
        self._state: State = State(id="123456")

    def setActionType(self, actionType: str):
        self._actionType = actionType

    def getActionType(self):
        return self._actionType

    def setActionNumber(self, actionNumber: int):
        self._actionNumber = actionNumber

    def getActionNumber(self):
        return self._actionNumber

    def getState(self) -> State:
        pass

    def resetCrawler(self, path: str, formXPath: str):
        pass

    def goToRootPage(self):
        pass

    def executeAppEvent(self, xpath: str, value: str):
        pass

    def changeFocus(self):
        pass

    def getAllSelectedElements(self) -> [AppElement]:
        pass

    def getFocusedAppElement(self) -> AppElement:
        pass
