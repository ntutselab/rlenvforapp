from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity


class DirectiveEntity:
    def __init__(self, url: str, dom: str, formXPath: str, appEventEntities: [
                 AppEventEntity], codeCoverageEntities: [CodeCoverageEntity]):
        self._url = url
        self._dom = dom
        self._formXPath = formXPath
        self._appEventEntities = appEventEntities
        self._codeCoverageEntities = codeCoverageEntities

    def get_url(self) -> str:
        return self._url

    def get_dom(self) -> str:
        return self._dom

    def get_form_x_path(self) -> str:
        return self._formXPath

    def get_app_event_entities(self) -> [AppEventEntity]:
        return self._appEventEntities

    def get_code_coverage_entities(self) -> [CodeCoverageEntity]:
        return self._codeCoverageEntities
