from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.mapper import \
    CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import \
    DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper


def _mapping_code_coverage_entities_from(
        code_coverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    code_coverage_entities: [CodeCoverageEntity] = []
    for code_coverage in code_coverages:
        code_coverage_entities.append(
            CodeCoverageEntityMapper.mapping_code_coverage_entity_from(
                code_coverage=code_coverage))
    return code_coverage_entities


def _mapping_code_coverage_from(code_coverage_entities: [
                             CodeCoverageEntity]) -> [CodeCoverage]:
    code_coverages: [CodeCoverage] = []
    for code_coverage_entity in code_coverage_entities:
        code_coverages.append(
            CodeCoverageEntityMapper.mapping_code_coverage_from(
                code_coverage_entity=code_coverage_entity))
    return code_coverages


def mapping_directive_entity_from(directive: Directive) -> DirectiveEntity:
    app_event_entities: [AppEventEntity] = []
    for app_event in directive.get_app_events():
        app_event_entities.append(
            AppEventEntityMapper.mapping_app_event_entity_from(
                app_event=app_event))
    return DirectiveEntity(url=directive.get_url(), dom=directive.get_dom(), form_x_path=directive.get_form_x_path(
    ), app_event_entities=app_event_entities, code_coverage_entities=_mapping_code_coverage_entities_from(directive.get_code_coverages()))


def mapping_directive_from(directive_entity: DirectiveEntity) -> Directive:
    app_events: [AppEvent] = []
    for app_event_entity in directive_entity.get_app_event_entities():
        app_events.append(
            AppEventEntityMapper.mapping_app_event_from(
                app_event_entity=app_event_entity))
    return Directive(url=directive_entity.get_url(), dom=directive_entity.get_dom(), form_x_path=directive_entity.get_form_x_path(
    ), app_events=app_events, code_coverages=_mapping_code_coverage_from(directive_entity.get_code_coverage_entities()))
