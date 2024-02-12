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
        odeCoverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    codeCoverageEntities: [CodeCoverageEntity] = []
    for codeCoverage in odeCoverages:
        codeCoverageEntities.append(
            CodeCoverageEntityMapper.mapping_code_coverage_entity_from(
                codeCoverage=codeCoverage))
    return codeCoverageEntities


def _mapping_code_coverage_from(codeCoverageEntities: [
                             CodeCoverageEntity]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageEntity in codeCoverageEntities:
        codeCoverages.append(
            CodeCoverageEntityMapper.mapping_code_coverage_from(
                codeCoverageEntity=codeCoverageEntity))
    return codeCoverages


def mapping_directive_entity_from(directive: Directive) -> DirectiveEntity:
    appEventEntities: [AppEventEntity] = []
    for appEvent in directive.get_app_events():
        appEventEntities.append(
            AppEventEntityMapper.mapping_app_event_entity_from(
                appEvent=appEvent))
    return DirectiveEntity(url=directive.get_url(), dom=directive.get_dom(), formXPath=directive.get_form_x_path(
    ), appEventEntities=appEventEntities, codeCoverageEntities=_mapping_code_coverage_entities_from(directive.get_code_coverages()))


def mapping_directive_from(directiveEntity: DirectiveEntity) -> Directive:
    appEvents: [AppEvent] = []
    for appEventEntity in directiveEntity.get_app_event_entities():
        appEvents.append(
            AppEventEntityMapper.mapping_app_event_from(
                appEventEntity=appEventEntity))
    return Directive(url=directiveEntity.get_url(), dom=directiveEntity.get_dom(), formXPath=directiveEntity.get_form_x_path(
    ), appEvents=appEvents, codeCoverages=_mapping_code_coverage_from(directiveEntity.get_code_coverage_entities()))
