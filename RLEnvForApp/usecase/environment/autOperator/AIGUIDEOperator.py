import time
import uuid

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.state import State, AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import AppElementDTOMapper
import random


class AIGUIDEOperator(IAUTOperator):
    def __init__(self, crawler: ICrawler,
                 codeCoverageCollector: ICodeCoverageCollector = ICodeCoverageCollector()):
        super().__init__()
        self._crawler = crawler
        self._codeCoverageCollector = codeCoverageCollector
        self._activeUrl = ""
        self._selectedAppElements: [AppElement] = []
        self._interactedElement: AppElement = None
        self._focusedAppElementIndex: int = 0
        self._appEventValue: str = ""

    def getState(self) -> State:
        state = State.State(id=str(uuid.uuid4()))
        focusedVector: [bool] = []
        for i in range(0, len(self._selectedAppElements)):
            focusedVector.append(i == self._focusedAppElementIndex)
        state.setFocusVector(focusedVector)
        state.setInteractedElement(self.getFocusedAppElement())
        state.setSelectedAppElements(self._selectedAppElements)
        state.setUrl(self._crawler.getUrl())
        state.setDOM(self._crawler.getDOM())
        state.setCodeCoverages(
            self._mappingCodeCoverageForm(codeCoverageDTOs=self._codeCoverageCollector.getCodeCoverageDTOs()))
        state.setScreenShot(self._crawler.getScreenShot())
        return state

    def resetCrawler(self, rootPath: str, formXPath: str):
        self._selectedAppElements: [AppElement] = []
        self._focusedAppElementIndex = 0
        self._interactedElement = None
        self._appEventValue = ""
        self._crawler.reset(rootPath=rootPath, formXPath=formXPath)
        self._activeUrl = self._crawler.getUrl()
        self._updateAllSelectedAppElements()

    def goToRootPage(self):
        self._crawler.goToRootPage()

    def executeAppEvent(self, xpath: str, value: str):
        self._appEventValue = value
        if xpath == "":
            focusedAppElement = self.getFocusedAppElement()
            if focusedAppElement is None:
                return
            xpath = focusedAppElement.getXpath()
        self._crawler.executeAppEvent(xpath=xpath, value=value)

        for i in self._selectedAppElements:
            if i.getXpath() == xpath:
                self._interactedElement = i
                self._interactedElement.setValue(value)
        self._updateAllSelectedAppElements()
        if not (self._activeUrl == self._crawler.getUrl()):
            self._activeUrl = self._crawler.getUrl()
            self._focusedAppElementIndex = 0

    def changeFocus(self):
        if super().getActionType() == "changeFocus":
            focusedAppElement: AppElement = self.getFocusedAppElement()
            focusedAppElement.setValue("")
            self._crawler.changeFocus(focusedAppElement.getXpath(), "")
            self._interactedElement = self._selectedAppElements[self._focusedAppElementIndex]
        numberOfSelectedAppElement = len(self._selectedAppElements)
        if numberOfSelectedAppElement != 0:
            self._focusedAppElementIndex = (
                self._focusedAppElementIndex + 1) % numberOfSelectedAppElement
        else:
            self._focusedAppElementIndex = 0

    def getAllSelectedAppElements(self) -> [AppElement]:
        return self._selectedAppElements

    def getFocusedAppElement(self) -> AppElement:
        if len(self._selectedAppElements) == 0:
            return None
        if len(self._selectedAppElements) <= self._focusedAppElementIndex:
            self._focusedAppElementIndex = 0

        return self._selectedAppElements[self._focusedAppElementIndex]

    def _updateAllSelectedAppElements(self):
        self._selectedAppElements: [AppElement] = []

        inputAppElements: [AppElement] = []
        buttonAppElements: [AppElement] = []
        hyperlinkAppElements: [AppElement] = []
        otherAppElements: [AppElement] = []

        for appElementDTO in self._getAppElementDTOs(retry=10):
            appElement = AppElementDTOMapper.mappingAppElementFrom(appElementDTO=appElementDTO)
            if "/input" in appElement.getXpath().lower():
                inputAppElements.append(appElement)
            elif "/button" in appElement.getXpath().lower():
                buttonAppElements.append(appElement)
            elif "/a" in appElement.getXpath().lower():
                hyperlinkAppElements.append(appElement)
            else:
                otherAppElements.append(appElement)

        self._selectedAppElements.extend(inputAppElements)
        self._selectedAppElements.extend(hyperlinkAppElements)
        self._selectedAppElements.extend(otherAppElements)
        self._selectedAppElements.extend(buttonAppElements)

    def _mappingCodeCoverageForm(self, codeCoverageDTOs: [CodeCoverageDTO]) -> [CodeCoverage]:
        codeCoverages = []
        for i in codeCoverageDTOs:
            codeCoverages.append(
                CodeCoverage(codeCoverageType=i.getCodeCoverageType(), codeCoverageVector=i.getCodeCoverageVector()))
        return codeCoverages

    def _getAppElementDTOs(self, retry: int):
        appElementDTOs: [AppElementDTO] = []
        isRetry = True
        retryTimes = 0

        while (isRetry):
            try:
                appElementDTOs = self._crawler.getAllSelectedAppElementsDTOs()
                isRetry = False
            except BaseException:
                time.sleep(1)
                retryTimes += 1
                isRetry = retryTimes < retry
        return appElementDTOs
