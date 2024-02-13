from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository

from ...environment.autOperator.mapper import CodeCoverageDTOMapper
from ..entity.TargetPageEntity import TargetPageEntity
from ..mapper import (AppEventDTOMapper, DirectiveDTOMapper,
                      TargetPageEntityMapper)
from ..queueManager.TargetPageProcessingManagerSingleton import \
    TargetPageProcessingManagerSingleton
from . import UpdateTargetPageInput, UpdateTargetPageOutput


class UpdateTargetPageUseCase:
    @inject
    def __init__(
            self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: UpdateTargetPageInput.UpdateTargetPageInput,
                output: UpdateTargetPageOutput.UpdateTargetPageOutput):
        target_page_entity: TargetPageEntity = self._repository.find_by_id(
            input.get_target_page_id())
        target_page: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)

        target_page_url = input.get_target_page_url()
        if target_page_url is not None:
            target_page.set_target_url(targetUrl=target_page_url)

        root_url = input.get_root_url()
        if root_url is not None:
            target_page.set_root_url(root_url=root_url)

        app_event_dt_os = input.get_app_event_dt_os()
        if app_event_dt_os is not None:
            app_events: [AppEvent] = []
            for app_event_dto in app_event_dt_os:
                app_events.append(
                    AppEventDTOMapper.mapping_app_event_from(
                        app_event_dto=app_event_dto))
            target_page.set_app_events(app_events=app_events)

        task_id = input.get_task_id()
        if task_id is not None:
            target_page.set_task_id(task_id=task_id)

        basic_code_coverage_dto = input.get_basic_code_coverage_dto()
        if basic_code_coverage_dto is not None:
            newBasicCodeCoverage = CodeCoverageDTOMapper.mapping_code_coverage_from(
                code_coverage_dto=basic_code_coverage_dto)
            basic_code_coverage = target_page.get_basic_code_coverage()
            if newBasicCodeCoverage.get_code_coverage_type(
            ) == basic_code_coverage.get_code_coverage_type():
                newBasicCodeCoverage.merge(basic_code_coverage)
            target_page.set_basic_code_coverage(
                basic_code_coverage=newBasicCodeCoverage)

        directive_dt_os = input.get_directive_dt_os()
        if directive_dt_os is not None:
            directives: [Directive] = []
            for directive_dto in directive_dt_os:
                directives.append(
                    DirectiveDTOMapper.mapping_directive_from(
                        directive_dto=directive_dto))
            target_page.set_directives(directives=directives)

        target_page_entity = TargetPageEntityMapper.mapping_target_page_entity_from(
            target_page=target_page)
        self._repository.update(target_page_entity=target_page_entity)

        TargetPageProcessingManagerSingleton.get_instance(
        ).set_be_processed_target_page(target_page=target_page)
        output.set_id(target_page.get_id())
