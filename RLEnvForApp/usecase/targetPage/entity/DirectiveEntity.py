from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


class DirectiveEntity:
    def __init__(self, url: str, dom: str, form_xpath: str, app_event_entities: [
                 AppEventEntity], code_coverage_entities: [CodeCoverageEntity]):
        self._url = url
        self._dom = dom
        self._form_xpath = form_xpath
        self._app_event_entities = app_event_entities
        self._code_coverage_entities = code_coverage_entities

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_xpath(self) -> str:
        return self._form_xpath

    def get_app_event_entities(self) -> [AppEventEntity]:
        return self._app_event_entities

    def get_code_coverage_entities(self) -> [CodeCoverageEntity]:
        return self._code_coverage_entities
