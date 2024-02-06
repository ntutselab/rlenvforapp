from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.entity.AppEventEntity import AppEventEntity
from RLEnvForApp.usecase.targetPage.entity.DirectiveEntity import DirectiveEntity
from RLEnvForApp.usecase.targetPage.mapper import AppEventEntityMapper


def _mappingCodeCoverageEntitiesFrom(odeCoverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    codeCoverageEntities: [CodeCoverageEntity] = []
    for codeCoverage in odeCoverages:
        codeCoverageEntities.append(
            CodeCoverageEntityMapper.mappingCodeCoverageEntityFrom(
                codeCoverage=codeCoverage))
    return codeCoverageEntities


def _mappingCodeCoverageFrom(codeCoverageEntities: [CodeCoverageEntity]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageEntity in codeCoverageEntities:
        codeCoverages.append(
            CodeCoverageEntityMapper.mappingCodeCoverageFrom(
                codeCoverageEntity=codeCoverageEntity))
    return codeCoverages


def mappingDirectiveEntityFrom(directive: Directive) -> DirectiveEntity:
    appEventEntities: [AppEventEntity] = []
    for appEvent in directive.getAppEvents():
        appEventEntities.append(AppEventEntityMapper.mappingAppEventEntityFrom(appEvent=appEvent))
    return DirectiveEntity(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(
    ), appEventEntities=appEventEntities, codeCoverageEntities=_mappingCodeCoverageEntitiesFrom(directive.getCodeCoverages()))


def mappingDirectiveFrom(directiveEntity: DirectiveEntity) -> Directive:
    appEvents: [AppEvent] = []
    for appEventEntity in directiveEntity.getAppEventEntities():
        appEvents.append(AppEventEntityMapper.mappingAppEventFrom(appEventEntity=appEventEntity))
    return Directive(url=directiveEntity.getUrl(), dom=directiveEntity.getDom(), formXPath=directiveEntity.getFormXPath(
    ), appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(directiveEntity.getCodeCoverageEntities()))
