from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO


class StateDTO:
    def __init__(self, id: str):
        self._id = id
        self._dom: str = ""
        self._url = None
        self._screenShot = None
        self._codeCoverages: [bool] = [False]
        self._focusVector: [bool] = None
        self._actionType = ""
        self._value = ""
        self._interactedElement = None
        self._selectedAppElementDTOs: [AppElementDTO] = []

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

    def setCodeCoverages(self, codeCoverages: [CodeCoverageDTO]):
        self._codeCoverages = codeCoverages

    def getCodeCoverages(self) -> [CodeCoverageDTO]:
        return self._codeCoverages

    def setFocusVector(self, focusVector: [bool]):
        self._focusVector = focusVector

    def getFocusVector(self) -> [bool]:
        return self._focusVector

    def setActionType(self, actionType: str):
        self._actionType = actionType

    def getActionType(self):
        return self._actionType

    def setAppEventValue(self, value: str):
        self._value = value

    def getAppEventValue(self) -> str:
        return self._value

    def setInteractedElementDTO(self, interactedElement: AppElementDTO):
        self._interactedElement = interactedElement

    def getInterActedElementDTO(self) -> AppElementDTO:
        return self._interactedElement

    def setSelectedAppElementDTOs(self, selectedAppElementEntities: [AppElementDTO]):
        self._selectedAppElementDTOs = selectedAppElementEntities

    def getSelectedAppElementDTOs(self) -> [AppElementDTO]:
        return self._selectedAppElementDTOs
