import uuid

from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.mapper import (AppEventDTOMapper, DirectiveDTOMapper,
                                                   TargetPageEntityMapper)

from ...environment.autOperator.mapper import CodeCoverageDTOMapper
from . import CreateTargetPageInput, CreateTargetPageOutput


class CreateTargetPageUseCase:
    @inject
    def __init__(self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: CreateTargetPageInput.CreateTargetPageInput,
                output: CreateTargetPageOutput.CreateTargetPageOutput):
        appEvents: [AppEvent] = self._convertAppEventDTOsToAppEvents(input.getAppEventDTOs())
        codeCoverage: CodeCoverage = self._convertCodeCoverageDTOToCodeCoverage(
            input.getBasicCodeCoverage())
        directives: [Directive] = self._convertDirectiveDTOsToDirective(
            directiveDTOs=input.getDirectiveDTOs())
        targetPage = TargetPage(id=str(uuid.uuid4()),
                                targetUrl=input.getTargetPageUrl(),
                                rootUrl=input.getRootUrl(),
                                appEvents=appEvents,
                                taskID=input.getTaskID(),
                                formXPath=input.getFormXPath(),
                                basicCodeCoverage=codeCoverage,
                                directives=directives)
        targetPageEntity = TargetPageEntityMapper.mappingTargetPageEntityFrom(targetPage=targetPage)

        self._repository.add(targetPageEntity=targetPageEntity)
        output.setId(targetPage.getId())

    def _convertAppEventDTOsToAppEvents(self, appEventDTOs):
        appEvents: [AppEvent] = []

        for appEvent in appEventDTOs:
            appEvents.append(AppEventDTOMapper.mappingAppEventFrom(appEvent))

        return appEvents

    def _convertCodeCoverageDTOToCodeCoverage(self, codeCoverageDTO) -> CodeCoverage:
        if codeCoverageDTO is None:
            codeCoverage: CodeCoverage = CodeCoverage(
                codeCoverageType="null", codeCoverageVector=[])
        else:
            codeCoverage: CodeCoverage = CodeCoverageDTOMapper.mappingCodeCoverageFrom(
                codeCoverageDTO)
        return codeCoverage

    def _convertDirectiveDTOsToDirective(self, directiveDTOs) -> [Directive]:
        directives: [Directive] = []
        for directiveDTO in directiveDTOs:
            directives.append(DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO))
        return directives
