import uuid

from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.mapper import (AppEventDTOMapper,
                                                   DirectiveDTOMapper,
                                                   TargetPageEntityMapper)

from ...environment.autOperator.mapper import CodeCoverageDTOMapper
from . import CreateTargetPageInput, CreateTargetPageOutput


class CreateTargetPageUseCase:
    @inject
    def __init__(
            self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: CreateTargetPageInput.CreateTargetPageInput,
                output: CreateTargetPageOutput.CreateTargetPageOutput):
        app_events: [AppEvent] = self._convert_app_event_dt_os_to_app_events(
            input.get_app_event_dt_os())
        code_coverage: CodeCoverage = self._convert_code_coverage_dto_to_code_coverage(
            input.get_basic_code_coverage())
        directives: [Directive] = self._convert_directive_dt_os_to_directive(
            directive_dt_os=input.get_directive_dt_os())
        target_page = TargetPage(id=str(uuid.uuid4()),
                                targetUrl=input.get_target_page_url(),
                                root_url=input.get_root_url(),
                                app_events=app_events,
                                task_id=input.get_task_id(),
                                form_xpath=input.get_form_xpath(),
                                basic_code_coverage=code_coverage,
                                directives=directives)
        target_page_entity = TargetPageEntityMapper.mapping_target_page_entity_from(
            target_page=target_page)

        self._repository.add(target_page_entity=target_page_entity)
        output.set_id(target_page.get_id())

    def _convert_app_event_dt_os_to_app_events(self, app_event_dt_os):
        app_events: [AppEvent] = []

        for app_event in app_event_dt_os:
            app_events.append(AppEventDTOMapper.mapping_app_event_from(app_event))

        return app_events

    def _convert_code_coverage_dto_to_code_coverage(
            self, code_coverage_dto) -> CodeCoverage:
        if code_coverage_dto is None:
            code_coverage: CodeCoverage = CodeCoverage(
                code_coverage_type="null", code_coverage_vector=[])
        else:
            code_coverage: CodeCoverage = CodeCoverageDTOMapper.mapping_code_coverage_from(
                code_coverage_dto)
        return code_coverage

    def _convert_directive_dt_os_to_directive(self, directive_dt_os) -> [Directive]:
        directives: [Directive] = []
        for directive_dto in directive_dt_os:
            directives.append(
                DirectiveDTOMapper.mapping_directive_from(
                    directive_dto=directive_dto))
        return directives
