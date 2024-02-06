from RLEnvForApp.domain.environment.state import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.observationService.htmlExtractor.HtmlExtractor import HtmlExtractor


class State:
    def __init__(self, id: str):
        self._id = id
        self._DOM: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [CodeCoverage] = []
        self._focusVector: [bool] = None
        self._actionType = ""
        self._inputValue = ""
        self._interactedElement = None
        self._selectedAppElements: [AppElement] = []
        self._actionNumber = None
        self._originalObservation = {}

    def getId(self):
        return self._id

    def setDOM(self, DOM: str):
        self._DOM = DOM

    def getDOM(self):
        return self._DOM

    def setUrl(self, url: str):
        self._url = url

    def getUrl(self):
        return self._url

    def setScreenShot(self, screenShot):
        self._screenShot = screenShot

    def getScreenShot(self):
        return self._screenShot

    def setCodeCoverages(self, codeCoverages: [CodeCoverage]):
        self._codeCoverages = codeCoverages

    def getCodeCoverages(self) -> [CodeCoverage]:
        return self._codeCoverages

    def setFocusVector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def getFocusVector(self):
        return self._focusVector

    def setActionType(self, actionType: str):
        self._actionType = actionType

    def getActionType(self):
        return self._actionType

    def setAppEventInputValue(self, value: str):
        self._inputValue = value

    def getAppEventInputValue(self):
        return self._inputValue

    def setInteractedElement(self, interactedElement: AppElement):
        self._interactedElement = interactedElement

    def getInteractedElement(self) -> AppElement:
        return self._interactedElement

    def getInteractedElementLabel(self) -> str:
        return HtmlExtractor().getLabelName(self._DOM, self._interactedElement.getXpath())

    def getInteractedElementPlaceholder(self) -> str:
        return HtmlExtractor().getPlaceholder(self._DOM, self._interactedElement.getXpath())

    def setSelectedAppElements(self, appElements: [AppElement]):
        self._selectedAppElements = appElements

    def getAllSelectedAppElements(self) -> [AppElement]:
        return self._selectedAppElements

    def setActionNumber(self, actionNumber: int):
        self._actionNumber = actionNumber
    
    def getActionNumber(self) -> int:
        return self._actionNumber

    def setOriginalObservation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def getOriginalObservation(self) -> dict:
        return self._originalObservation

    def isSelectedAppElementsEmpty(self) -> bool:
        return len(self._selectedAppElements) == 0
