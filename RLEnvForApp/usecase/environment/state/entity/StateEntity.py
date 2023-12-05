from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from . import AppElementEntity
from .CodeCoverageEntity import CodeCoverageEntity


class StateEntity:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [bool] = [False]
        self._focusVector: [bool] = None
        self._actionType = ""
        self._inputValue = ""
        self._interactedElement = None
        self._selectedAppElementEntities: [AppElementEntity] = []
        self._actionNumber = None
        self._originalObservation = {}

    def getId(self):
        return self._id

    def setDom(self, dom: str):
        self._dom = dom

    def getDom(self) -> str:
        return self._dom

    def setUrl(self, url: str):
        self._url = url

    def getUrl(self) -> str:
        return self._url

    def setScreenShot(self, screenShot):
        self._screenShot = screenShot

    def getScreenShot(self):
        return self._screenShot

    def setCodeCoverages(self, codeCoverages: [CodeCoverageEntity]):
        self._codeCoverages = codeCoverages

    def getCodeCoverages(self) -> [CodeCoverageEntity]:
        return self._codeCoverages

    def setFocusVector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def getFocusVector(self) -> [bool]:
        return self._focusVector

    def setActionType(self, actionType: str):
        self._actionType = actionType

    def getActionType(self):
        return self._actionType

    def setInputValue(self, inputValue: str):
        self._inputValue = inputValue

    def getInputValue(self) -> str:
        return self._inputValue

    def setInteractedElementEntity(self, interactedElement: AppElementEntity):
        self._interactedElement = interactedElement

    def getInterActedElementEntity(self) -> AppElementEntity:
        return self._interactedElement

    def setSelectedAppElementEntities(self, selectedAppElementEntities: [AppElementEntity]):
        self._selectedAppElementEntities = selectedAppElementEntities

    def getSelectedAppElementEntities(self) -> [AppElementEntity]:
        return self._selectedAppElementEntities

    def setActionNumber(self, actionNumber: int):
        self._actionNumber = actionNumber

    def getActionNumber(self) -> int:
        return self._actionNumber

    def setOriginalObservation(self, originalObservation: dict):
        self._originalObservation = originalObservation

    def getOriginalObservation(self) -> dict:
        return self._originalObservation
