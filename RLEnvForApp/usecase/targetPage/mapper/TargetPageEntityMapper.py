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


def mapping_target_page_entity_from(target_page: TargetPage.TargetPage):
    app_event_entities: [AppEventEntity.AppEventEntity] = []
    for app_event in target_page.get_app_events():
        app_event_entities.append(
            AppEventEntityMapper.mapping_app_event_entity_from(app_event))

    directive_entities: [DirectiveEntity] = []
    for directive in target_page.get_directives():
        directive_entities.append(
            DirectiveEntityMapper.mapping_directive_entity_from(
                directive=directive))
    return TargetPageEntity.TargetPageEntity(id=target_page.get_id(),
                                             targetUrl=target_page.get_target_url(),
                                             root_url=target_page.get_root_url(),
                                             app_event_entities=app_event_entities,
                                             task_id=target_page.get_task_id(),
                                             form_x_path=target_page.get_form_x_path(),
                                             basicCodeCoverageEntity=CodeCoverageEntityMapper.mapping_code_coverage_entity_from(
                                                 target_page.get_basic_code_coverage()),
                                             directive_entities=directive_entities)


def mapping_target_page_from(target_page_entity: TargetPageEntity):
    app_events: [AppEvent] = []
    for app_event_entity in target_page_entity.get_app_event_entities():
        app_events.append(
            AppEventEntityMapper.mapping_app_event_from(
                app_event_entity=app_event_entity))

    directives: [Directive] = []
    for directive_entity in target_page_entity.get_directive_entities():
        directives.append(
            DirectiveEntityMapper.mapping_directive_from(
                directive_entity=directive_entity))
    return TargetPage.TargetPage(id=target_page_entity.get_id(),
                                 targetUrl=target_page_entity.get_target_url(),
                                 root_url=target_page_entity._root_url,
                                 app_events=app_events,
                                 task_id=target_page_entity.get_task_id(),
                                 form_x_path=target_page_entity.get_form_x_path(),
                                 basic_code_coverage=CodeCoverageEntityMapper.mapping_code_coverage_from(
                                     target_page_entity.get_basic_code_coverage_entity()),
                                 directives=directives)
