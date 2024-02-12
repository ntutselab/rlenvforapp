from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage
from RLEnvForApp.usecase.environment.autOperator.mapper import \
    CodeCoverageDTOMapper
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO
from RLEnvForApp.usecase.targetPage.mapper import (AppEventDTOMapper,
                                                   DirectiveDTOMapper)


def mappingTargetPageDTOFrom(targetPage: TargetPage):
    appEventDTOs: [AppEventDTO] = []
    for appEvent in targetPage.getAppEvents():
        appEventDTOs.append(AppEventDTOMapper.mappingAppEventDTOFrom(appEvent=appEvent))

    directiveDTOs: [DirectiveDTO] = []
    for directive in targetPage.getDirectives():
        directiveDTOs.append(DirectiveDTOMapper.mappingDirectiveDTOFrom(directive))

    return TargetPageDTO(id=targetPage.getId(),
                         targetUrl=targetPage.getTargetUrl(),
                         rootUrl=targetPage.getRootUrl(),
                         appEventDTOs=appEventDTOs,
                         taskID=targetPage.getTaskID(),
                         formXPath=targetPage.getFormXPath(),
                         basicCodeCoverageDTO=CodeCoverageDTOMapper.mappingCodeCoverageDTOFrom(
                             targetPage.getBasicCodeCoverage()),
                         directiveDTOs=directiveDTOs)


def mappingTargetPageFrom(targetPageDTO: TargetPageDTO):
    appEvents: [AppEvent] = []
    for appEventDTO in targetPageDTO.getAppEventDTOs():
        appEvents.append(AppEventDTOMapper.mappingAppEventFrom(appEventDTO=appEventDTO))

    directives: [Directive] = []
    for directiveDTO in targetPageDTO.getDirectiveDTOs():
        directives.append(DirectiveDTOMapper.mappingDirectiveFrom(directiveDTO=directiveDTO))
    return TargetPage(id=targetPageDTO.getId(),
                      targetUrl=targetPageDTO.getTargetUrl(),
                      rootUrl=targetPageDTO.getRootUrl(),
                      appEvents=appEvents,
                      taskID=targetPageDTO.getTaskID(),
                      formXPath=targetPageDTO.getFormXPath(),
                      basicCodeCoverage=CodeCoverageDTOMapper.mappingCodeCoverageFrom(
                          targetPageDTO.getBasicCodeCoverageDTO()),
                      directives=directives)
