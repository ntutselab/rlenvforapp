import uuid

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.state import State, AppElement
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import ICrawler
from RLEnvForApp.usecase.environment.autOperator.mapper import AppElementDTOMapper


class DefaultHtmlFileOperator(IAUTOperator):
    def __init__(self, crawler: ICrawler):
        super().__init__()
        self._crawler = crawler
        self._submitElement: AppElement = None
        self._selectedAppElements: [AppElement] = []
        self._interactedElementIndex: int = 0
        self._focusedAppElementIndex: int = 0
        self._appEventValue: str = ""

    def getState(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focusedVector: [bool] = []
        for i in range(0, len(self._selectedAppElements)):
            focusedVector.append(i == self._focusedAppElementIndex)

        state.setDOM(self._crawler.getDOM())
        state.setSelectedAppElements(self._selectedAppElements)
        state.setActionType(super().getActionType())
        state.setAppEventInputValue(value=self._appEventValue)
        state.setInteractedElement(self._selectedAppElements[self._interactedElementIndex])
        state.setFocusVector(focusedVector)
        return state

    def resetCrawler(self, path: str, formXPath: str = ""):
        self._crawler.reset(path=path, formXPath=formXPath)
        self._setSelectedAppElement()
        self._focusedAppElementIndex = 0
        self._appEventValue = ""

    def goToRootPage(self):
        self._crawler.goToRootPage()

    def executeAppEvent(self, xpath: str, value: str):
        self._interactedElementIndex = self._focusedAppElementIndex
        self._appEventValue = value
        if xpath == "" and value == "":
            self._clickSubmitButton()
        elif xpath == "" and value != "":
            self._inputValue(xpath=self.getFocusedAppElement().getXpath(), value=value)
        else:
            self._inputValue(xpath=xpath, value=value)

    def changeFocus(self):
        numberOfSelectedAppElement = len(self._selectedAppElements)
        self._focusedAppElementIndex = (
            self._focusedAppElementIndex + 1) % numberOfSelectedAppElement

    def getAllSelectedAppElements(self) -> [AppElement]:
        return self._selectedAppElements

    def getFocusedAppElement(self) -> AppElement:
        return self._selectedAppElements[self._focusedAppElementIndex]

    def _setSelectedAppElement(self):
        self._selectedAppElements: [AppElement] = []

        for appElementDTO in self._crawler.getAllSelectedAppElementsDTOs():
            appElement = AppElementDTOMapper.mappingAppElementFrom(appElementDTO=appElementDTO)
            if appElement.getTagName() == "input":
                self._selectedAppElements.append(appElement)
            elif appElement.getType() == "submit":
                self._submitElement = appElement

    def _clickSubmitButton(self):
        self._crawler.executeAppEvent(self._submitElement.getXpath(), "")

    def _inputValue(self, xpath: str, value: str):
        self._crawler.executeAppEvent(xpath=xpath, value=value)
        self._setSelectedAppElement()
