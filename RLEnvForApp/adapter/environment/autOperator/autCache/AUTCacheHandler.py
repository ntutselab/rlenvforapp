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
                 code_coverage_collector: ICodeCoverageCollector):
        super().__init__()
        self._crawler = crawler
        self._code_coverage_collector = code_coverage_collector

        self._app_event_sequence: [AppEventDTO] = []
        self._dom_caches: [DOMCache] = []
        self.is_hit = False

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        return self._code_coverage_collector.get_code_coverage_dt_os()

    def reset_code_coverage(self):
        return self._code_coverage_collector.reset_code_coverage()

    def go_to_root_page(self):
        return self._crawler.go_to_root_page()

    def reset(self, rootPath: str, form_xpath: str = ""):
        self.is_hit = False
        return self._crawler.reset(rootPath=rootPath, form_xpath=form_xpath)

    def close(self):
        return self._crawler.close()

    def execute_app_event(self, xpath: str, value: str):
        self._app_event_sequence.append(
            AppEventDTO(
                xpath=xpath,
                value=value,
                category=""))
        self._crawler.execute_app_event(xpath=xpath, value=value)
        dom_cache = DOMCache
        dom_cache.dom = self._crawler.get_dom()

    def get_screen_shot(self):
        return self._crawler.get_screen_shot()

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        return self._crawler.get_all_selected_app_elements_dt_os()

    def get_dom(self) -> str:
        return self._crawler.get_dom()

    def get_url(self) -> str:
        return self._crawler.get_url()
