from RLEnvForApp.domain.targetPage import TargetPage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.mapper import \
    CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity import (AppEventEntity,
                                                   TargetPageEntity)
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import \
    DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import (AppEventEntityMapper,
                                                   DirectiveEntityMapper)


def mapping_target_page_entity_from(targetPage: TargetPage.TargetPage):
    appEventEntities: [AppEventEntity.AppEventEntity] = []
    for appEvent in targetPage.get_app_events():
        appEventEntities.append(
            AppEventEntityMapper.mapping_app_event_entity_from(appEvent))

    directiveEntities: [DirectiveEntity] = []
    for directive in targetPage.get_directives():
        directiveEntities.append(
            DirectiveEntityMapper.mapping_directive_entity_from(
                directive=directive))
    return TargetPageEntity.TargetPageEntity(id=targetPage.get_id(),
                                             targetUrl=targetPage.get_target_url(),
                                             rootUrl=targetPage.get_root_url(),
                                             appEventEntities=appEventEntities,
                                             taskID=targetPage.get_task_id(),
                                             formXPath=targetPage.get_form_x_path(),
                                             basicCodeCoverageEntity=CodeCoverageEntityMapper.mapping_code_coverage_entity_from(
                                                 targetPage.get_basic_code_coverage()),
                                             directiveEntities=directiveEntities)


def mapping_target_page_from(targetPageEntity: TargetPageEntity):
    appEvents: [AppEvent] = []
    for appEventEntity in targetPageEntity.get_app_event_entities():
        appEvents.append(
            AppEventEntityMapper.mapping_app_event_from(
                appEventEntity=appEventEntity))

    directives: [Directive] = []
    for directiveEntity in targetPageEntity.get_directive_entities():
        directives.append(
            DirectiveEntityMapper.mapping_directive_from(
                directiveEntity=directiveEntity))
    return TargetPage.TargetPage(id=targetPageEntity.get_id(),
                                 targetUrl=targetPageEntity.get_target_url(),
                                 rootUrl=targetPageEntity._rootUrl,
                                 appEvents=appEvents,
                                 taskID=targetPageEntity.get_task_id(),
                                 formXPath=targetPageEntity.get_form_x_path(),
                                 basicCodeCoverage=CodeCoverageEntityMapper.mapping_code_coverage_from(
                                     targetPageEntity.get_basic_code_coverage_entity()),
                                 directives=directives)
