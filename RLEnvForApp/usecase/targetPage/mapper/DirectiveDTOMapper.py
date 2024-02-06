from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import CodeCoverageDTOMapper
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.mapper import AppEventDTOMapper


def _mappingCodeCoverageDTOsFrom(odeCoverages: [CodeCoverage]) -> [CodeCoverageDTO]:
    codeCoverageDTOs: [CodeCoverageDTO] = []
    for codeCoverage in odeCoverages:
        codeCoverageDTOs.append(
            CodeCoverageDTOMapper.mappingCodeCoverageDTOFrom(
                codeCoverage=codeCoverage))
    return codeCoverageDTOs


def _mappingCodeCoverageFrom(codeCoverageDTOs: [CodeCoverageDTO]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageDTO in codeCoverageDTOs:
        codeCoverages.append(
            CodeCoverageDTOMapper.mappingCodeCoverageFrom(
                codeCoverageDTO=codeCoverageDTO))
    return codeCoverages


def mappingDirectiveFrom(directiveDTO: DirectiveDTO) -> Directive:
    appEvents: [AppEvent] = []
    for appEventDTO in directiveDTO.getAppEventDTOs():
        appEvents.append(AppEventDTOMapper.mappingAppEventFrom(appEventDTO=appEventDTO))

    return Directive(url=directiveDTO.getUrl(), dom=directiveDTO.getDom(), formXPath=directiveDTO.getFormXPath(),
                     appEvents=appEvents, codeCoverages=_mappingCodeCoverageFrom(codeCoverageDTOs=directiveDTO.getCodeCoverageDTOs()))


def mappingDirectiveDTOFrom(directive: Directive) -> DirectiveDTO:
    appEventDTOs: [AppEventDTO] = []
    for appEvent in directive.getAppEvents():
        appEventDTOs.append(AppEventDTOMapper.mappingAppEventDTOFrom(appEvent=appEvent))

    return DirectiveDTO(url=directive.getUrl(), dom=directive.getDom(), formXPath=directive.getFormXPath(),
                        appEventDTOs=appEventDTOs, codeCoverageDTOs=_mappingCodeCoverageDTOsFrom(directive.getCodeCoverages()))
