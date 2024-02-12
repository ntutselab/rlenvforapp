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
        appEvents: [AppEvent] = self._convert_app_event_dt_os_to_app_events(
            input.get_app_event_dt_os())
        codeCoverage: CodeCoverage = self._convert_code_coverage_dto_to_code_coverage(
            input.get_basic_code_coverage())
        directives: [Directive] = self._convert_directive_dt_os_to_directive(
            directiveDTOs=input.get_directive_dt_os())
        targetPage = TargetPage(id=str(uuid.uuid4()),
                                targetUrl=input.get_target_page_url(),
                                rootUrl=input.get_root_url(),
                                appEvents=appEvents,
                                taskID=input.get_task_id(),
                                formXPath=input.get_form_x_path(),
                                basicCodeCoverage=codeCoverage,
                                directives=directives)
        targetPageEntity = TargetPageEntityMapper.mapping_target_page_entity_from(
            targetPage=targetPage)

        self._repository.add(targetPageEntity=targetPageEntity)
        output.set_id(targetPage.get_id())

    def _convert_app_event_dt_os_to_app_events(self, appEventDTOs):
        appEvents: [AppEvent] = []

        for appEvent in appEventDTOs:
            appEvents.append(AppEventDTOMapper.mapping_app_event_from(appEvent))

        return appEvents

    def _convert_code_coverage_dto_to_code_coverage(
            self, codeCoverageDTO) -> CodeCoverage:
        if codeCoverageDTO is None:
            codeCoverage: CodeCoverage = CodeCoverage(
                codeCoverageType="null", codeCoverageVector=[])
        else:
            codeCoverage: CodeCoverage = CodeCoverageDTOMapper.mapping_code_coverage_from(
                codeCoverageDTO)
        return codeCoverage

    def _convert_directive_dt_os_to_directive(self, directiveDTOs) -> [Directive]:
        directives: [Directive] = []
        for directiveDTO in directiveDTOs:
            directives.append(
                DirectiveDTOMapper.mapping_directive_from(
                    directiveDTO=directiveDTO))
        return directives
