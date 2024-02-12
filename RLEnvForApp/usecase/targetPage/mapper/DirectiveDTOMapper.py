from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.targetPage.AppEvent import AppEvent
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import \
    CodeCoverageDTOMapper
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.mapper import AppEventDTOMapper


def _mapping_code_coverage_dt_os_from(
        odeCoverages: [CodeCoverage]) -> [CodeCoverageDTO]:
    codeCoverageDTOs: [CodeCoverageDTO] = []
    for codeCoverage in odeCoverages:
        codeCoverageDTOs.append(
            CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                codeCoverage=codeCoverage))
    return codeCoverageDTOs


def _mapping_code_coverage_from(
        codeCoverageDTOs: [CodeCoverageDTO]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageDTO in codeCoverageDTOs:
        codeCoverages.append(
            CodeCoverageDTOMapper.mapping_code_coverage_from(
                codeCoverageDTO=codeCoverageDTO))
    return codeCoverages


def mapping_directive_from(directiveDTO: DirectiveDTO) -> Directive:
    appEvents: [AppEvent] = []
    for appEventDTO in directiveDTO.get_app_event_dt_os():
        appEvents.append(
            AppEventDTOMapper.mapping_app_event_from(
                appEventDTO=appEventDTO))

    return Directive(url=directiveDTO.get_url(), dom=directiveDTO.get_dom(), formXPath=directiveDTO.get_form_x_path(),
                     appEvents=appEvents, codeCoverages=_mapping_code_coverage_from(codeCoverageDTOs=directiveDTO.get_code_coverage_dt_os()))


def mapping_directive_dto_from(directive: Directive) -> DirectiveDTO:
    appEventDTOs: [AppEventDTO] = []
    for appEvent in directive.get_app_events():
        appEventDTOs.append(
            AppEventDTOMapper.mapping_app_event_dto_from(
                appEvent=appEvent))

    return DirectiveDTO(url=directive.get_url(), dom=directive.get_dom(), formXPath=directive.get_form_x_path(),
                        appEventDTOs=appEventDTOs, codeCoverageDTOs=_mapping_code_coverage_dt_os_from(directive.get_code_coverages()))
