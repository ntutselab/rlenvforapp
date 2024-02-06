from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from . import (UpdateTargetPageOutput, UpdateTargetPageInput)
from RLEnvForApp.usecase.repository.TargetPageRepository import TargetPageRepository
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from dependency_injector.wiring import inject, Provide

from ..entity.TargetPageEntity import TargetPageEntity
from ..mapper import TargetPageEntityMapper, AppEventDTOMapper, DirectiveDTOMapper
from ..queueManager.TargetPageProcessingManagerSingleton import TargetPageProcessingManagerSingleton
from ...environment.autOperator.mapper import CodeCoverageDTOMapper


class UpdateTargetPageUseCase:
    @inject
    def __init__(self, repository: TargetPageRepository = Provide[EnvironmentDIContainers.targetPageRepository]):
        self._repository = repository

    def execute(self, input: UpdateTargetPageInput.UpdateTargetPageInput,
                output: UpdateTargetPageOutput.UpdateTargetPageOutput):
        targetPageEntity: TargetPageEntity = self._repository.findById(input.getTargetPageId())
        targetPage: TargetPage = TargetPageEntityMapper.mappingTargetPageFrom(targetPageEntity=targetPageEntity)

        targetPageUrl = input.getTargetPageUrl()
        if targetPageUrl is not None:
            targetPage.setTargetUrl(targetUrl=targetPageUrl)

        rootUrl = input.getRootUrl()
        if rootUrl != None:
            targetPage.setRootUrl(rootUrl=rootUrl)

        appEventDTOs = input.getAppEventDTOs()
        if appEventDTOs != None:
            appEvents: [AppEvent] = []
            for appEventDTO in appEventDTOs:
                appEvents.append(AppEventDTOMapper.mappingAppEventFrom(appEventDTO=appEventDTO))
            targetPage.setAppEvents(appEvents=appEvents)

        taskID = input.getTaskID()
        if taskID != None:
            targetPage.setTaskID(taskID=taskID)

        basicCodeCoverageDTO = input.getBasicCodeCoverageDTO()
        if basicCodeCoverageDTO != None:
            newBasicCodeCoverage = CodeCoverageDTOMapper.mappingCodeCoverageFrom(codeCoverageDTO=basicCodeCoverageDTO)
            basicCodeCoverage = targetPage.getBasicCodeCoverage()
            if newBasicCodeCoverage.getCodeCoverageType() == basicCodeCoverage.getCodeCoverageType():
                newBasicCodeCoverage.merge(basicCodeCoverage)
            targetPage.setBasicCodeCoverage(basicCodeCoverage=newBasicCodeCoverage)

        directiveDTOs = input.getDirectiveDTOs()
        if directiveDTOs != None:
            directives: [Directive] = []
            for directiveDTO in directiveDTOs:
                directives.append(DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO))
            targetPage.setDirectives(directives=directives)

        targetPageEntity = TargetPageEntityMapper.mappingTargetPageEntityFrom(targetPage=targetPage)
        self._repository.update(targetPageEntity=targetPageEntity)

        TargetPageProcessingManagerSingleton.getInstance().setBeProcessedTargetPage(targetPage=targetPage)
        output.setId(targetPage.getId())
