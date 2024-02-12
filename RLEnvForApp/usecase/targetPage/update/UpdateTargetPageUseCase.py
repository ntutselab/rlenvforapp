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
        targetPageEntity: TargetPageEntity = self._repository.find_by_id(
            input.get_target_page_id())
        targetPage: TargetPage = TargetPageEntityMapper.mapping_target_page_from(
            targetPageEntity=targetPageEntity)

        targetPageUrl = input.get_target_page_url()
        if targetPageUrl is not None:
            targetPage.set_target_url(targetUrl=targetPageUrl)

        rootUrl = input.get_root_url()
        if rootUrl is not None:
            targetPage.set_root_url(rootUrl=rootUrl)

        appEventDTOs = input.get_app_event_dt_os()
        if appEventDTOs is not None:
            appEvents: [AppEvent] = []
            for appEventDTO in appEventDTOs:
                appEvents.append(
                    AppEventDTOMapper.mapping_app_event_from(
                        appEventDTO=appEventDTO))
            targetPage.set_app_events(appEvents=appEvents)

        taskID = input.get_task_id()
        if taskID is not None:
            targetPage.set_task_id(taskID=taskID)

        basicCodeCoverageDTO = input.get_basic_code_coverage_dto()
        if basicCodeCoverageDTO is not None:
            newBasicCodeCoverage = CodeCoverageDTOMapper.mapping_code_coverage_from(
                codeCoverageDTO=basicCodeCoverageDTO)
            basicCodeCoverage = targetPage.get_basic_code_coverage()
            if newBasicCodeCoverage.get_code_coverage_type(
            ) == basicCodeCoverage.get_code_coverage_type():
                newBasicCodeCoverage.merge(basicCodeCoverage)
            targetPage.set_basic_code_coverage(
                basicCodeCoverage=newBasicCodeCoverage)

        directiveDTOs = input.get_directive_dt_os()
        if directiveDTOs is not None:
            directives: [Directive] = []
            for directiveDTO in directiveDTOs:
                directives.append(
                    DirectiveDTOMapper.mapping_directive_from(
                        directiveDTO=directiveDTO))
            targetPage.set_directives(directives=directives)

        targetPageEntity = TargetPageEntityMapper.mapping_target_page_entity_from(
            targetPage=targetPage)
        self._repository.update(targetPageEntity=targetPageEntity)

        TargetPageProcessingManagerSingleton.get_instance(
        ).set_be_processed_target_page(targetPage=targetPage)
        output.set_id(targetPage.get_id())
