from RLEnvForApp.adapter.environment.autOperator.autCache.DOMCache import \
    DOMCache
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class AUTCacheHandler(ICrawler, ICodeCoverageCollector):
    def __init__(self, crawler: ICrawler,
                 codeCoverageCollector: ICodeCoverageCollector):
        super().__init__()
        self._crawler = crawler
        self._codeCoverageCollector = codeCoverageCollector

        self._appEventSequence: [AppEventDTO] = []
        self._DOMCaches: [DOMCache] = []
        self.isHit = False

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        return self._codeCoverageCollector.get_code_coverage_dt_os()

    def reset_code_coverage(self):
        return self._codeCoverageCollector.reset_code_coverage()

    def go_to_root_page(self):
        return self._crawler.go_to_root_page()

    def reset(self, rootPath: str, formXPath: str = ""):
        self.isHit = False
        return self._crawler.reset(rootPath=rootPath, formXPath=formXPath)

    def close(self):
        return self._crawler.close()

    def execute_app_event(self, xpath: str, value: str):
        self._appEventSequence.append(
            AppEventDTO(
                xpath=xpath,
                value=value,
                category=""))
        self._crawler.execute_app_event(xpath=xpath, value=value)
        domCache = DOMCache
        domCache.dom = self._crawler.get_dom()

    def get_screen_shot(self):
        return self._crawler.get_screen_shot()

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        return self._crawler.get_all_selected_app_elements_dt_os()

    def get_dom(self) -> str:
        return self._crawler.get_dom()

    def get_url(self) -> str:
        return self._crawler.get_url()
