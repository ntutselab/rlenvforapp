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


def mapping_target_page_dto_from(target_page: TargetPage):
    app_event_dt_os: [AppEventDTO] = []
    for app_event in target_page.get_app_events():
        app_event_dt_os.append(
            AppEventDTOMapper.mapping_app_event_dto_from(
                app_event=app_event))

    directive_dt_os: [DirectiveDTO] = []
    for directive in target_page.get_directives():
        directive_dt_os.append(
            DirectiveDTOMapper.mapping_directive_dto_from(directive))

    return TargetPageDTO(id=target_page.get_id(),
                         targetUrl=target_page.get_target_url(),
                         root_url=target_page.get_root_url(),
                         app_event_dt_os=app_event_dt_os,
                         task_id=target_page.get_task_id(),
                         form_x_path=target_page.get_form_x_path(),
                         basic_code_coverage_dto=CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                             target_page.get_basic_code_coverage()),
                         directive_dt_os=directive_dt_os)


def mapping_target_page_from(target_page_dto: TargetPageDTO):
    app_events: [AppEvent] = []
    for app_event_dto in target_page_dto.get_app_event_dt_os():
        app_events.append(
            AppEventDTOMapper.mapping_app_event_from(
                app_event_dto=app_event_dto))

    directives: [Directive] = []
    for directive_dto in target_page_dto.get_directive_dt_os():
        directives.append(
            DirectiveDTOMapper.mapping_directive_from(
                directive_dto=directive_dto))
    return TargetPage(id=target_page_dto.get_id(),
                      targetUrl=target_page_dto.get_target_url(),
                      root_url=target_page_dto.get_root_url(),
                      app_events=app_events,
                      task_id=target_page_dto.get_task_id(),
                      form_x_path=target_page_dto.get_form_x_path(),
                      basic_code_coverage=CodeCoverageDTOMapper.mapping_code_coverage_from(
                          target_page_dto.get_basic_code_coverage_dto()),
                      directives=directives)
