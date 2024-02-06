from RLEnvForApp.adapter.environment.autOperator.autCache.DOMCache import DOMCache
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class AUTCacheHandler(ICrawler, ICodeCoverageCollector):
    def __init__(self, crawler: ICrawler, codeCoverageCollector: ICodeCoverageCollector):
        super().__init__()
        self._crawler = crawler
        self._codeCoverageCollector = codeCoverageCollector

        self._appEventSequence: [AppEventDTO] = []
        self._DOMCaches: [DOMCache] = []
        self.isHit = False

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        return self._codeCoverageCollector.getCodeCoverageDTOs()

    def resetCodeCoverage(self):
        return self._codeCoverageCollector.resetCodeCoverage()

    def goToRootPage(self):
        return self._crawler.goToRootPage()

    def reset(self, rootPath: str, formXPath: str = ""):
        self.isHit = False
        return self._crawler.reset(rootPath=rootPath, formXPath=formXPath)

    def close(self):
        return self._crawler.close()

    def executeAppEvent(self, xpath: str, value: str):
        self._appEventSequence.append(AppEventDTO(xpath=xpath, value=value, category=""))
        self._crawler.executeAppEvent(xpath=xpath, value=value)
        domCache = DOMCache
        domCache.dom = self._crawler.getDOM()

    def getScreenShot(self):
        return self._crawler.getScreenShot()

    def getAllSelectedAppElementsDTOs(self) -> [AppElementDTO]:
        return self._crawler.getAllSelectedAppElementsDTOs()

    def getDOM(self) -> str:
        return self._crawler.getDOM()

    def getUrl(self) -> str:
        return self._crawler.getUrl()
