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


def mapping_target_page_dto_from(targetPage: TargetPage):
    appEventDTOs: [AppEventDTO] = []
    for appEvent in targetPage.get_app_events():
        appEventDTOs.append(
            AppEventDTOMapper.mapping_app_event_dto_from(
                appEvent=appEvent))

    directiveDTOs: [DirectiveDTO] = []
    for directive in targetPage.get_directives():
        directiveDTOs.append(
            DirectiveDTOMapper.mapping_directive_dto_from(directive))

    return TargetPageDTO(id=targetPage.get_id(),
                         targetUrl=targetPage.get_target_url(),
                         rootUrl=targetPage.get_root_url(),
                         appEventDTOs=appEventDTOs,
                         taskID=targetPage.get_task_id(),
                         formXPath=targetPage.get_form_x_path(),
                         basicCodeCoverageDTO=CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                             targetPage.get_basic_code_coverage()),
                         directiveDTOs=directiveDTOs)


def mapping_target_page_from(targetPageDTO: TargetPageDTO):
    appEvents: [AppEvent] = []
    for appEventDTO in targetPageDTO.get_app_event_dt_os():
        appEvents.append(
            AppEventDTOMapper.mapping_app_event_from(
                appEventDTO=appEventDTO))

    directives: [Directive] = []
    for directiveDTO in targetPageDTO.get_directive_dt_os():
        directives.append(
            DirectiveDTOMapper.mapping_directive_from(
                directiveDTO=directiveDTO))
    return TargetPage(id=targetPageDTO.get_id(),
                      targetUrl=targetPageDTO.get_target_url(),
                      rootUrl=targetPageDTO.get_root_url(),
                      appEvents=appEvents,
                      taskID=targetPageDTO.get_task_id(),
                      formXPath=targetPageDTO.get_form_x_path(),
                      basicCodeCoverage=CodeCoverageDTOMapper.mapping_code_coverage_from(
                          targetPageDTO.get_basic_code_coverage_dto()),
                      directives=directives)
