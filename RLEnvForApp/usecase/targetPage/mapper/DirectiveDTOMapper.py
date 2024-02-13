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
        code_coverages: [CodeCoverage]) -> [CodeCoverageDTO]:
    code_coverage_dt_os: [CodeCoverageDTO] = []
    for code_coverage in code_coverages:
        code_coverage_dt_os.append(
            CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                code_coverage=code_coverage))
    return code_coverage_dt_os


def _mapping_code_coverage_from(
        code_coverage_dt_os: [CodeCoverageDTO]) -> [CodeCoverage]:
    code_coverages: [CodeCoverage] = []
    for code_coverage_dto in code_coverage_dt_os:
        code_coverages.append(
            CodeCoverageDTOMapper.mapping_code_coverage_from(
                code_coverage_dto=code_coverage_dto))
    return code_coverages


def mapping_directive_from(directive_dto: DirectiveDTO) -> Directive:
    app_events: [AppEvent] = []
    for app_event_dto in directive_dto.get_app_event_dt_os():
        app_events.append(
            AppEventDTOMapper.mapping_app_event_from(
                app_event_dto=app_event_dto))

    return Directive(url=directive_dto.get_url(), dom=directive_dto.get_dom(), form_xpath=directive_dto.get_form_xpath(),
                     app_events=app_events, code_coverages=_mapping_code_coverage_from(code_coverage_dt_os=directive_dto.get_code_coverage_dt_os()))


def mapping_directive_dto_from(directive: Directive) -> DirectiveDTO:
    app_event_dt_os: [AppEventDTO] = []
    for app_event in directive.get_app_events():
        app_event_dt_os.append(
            AppEventDTOMapper.mapping_app_event_dto_from(
                app_event=app_event))

    return DirectiveDTO(url=directive.get_url(), dom=directive.get_dom(), form_xpath=directive.get_form_xpath(),
                        app_event_dt_os=app_event_dt_os, code_coverage_dt_os=_mapping_code_coverage_dt_os_from(directive.get_code_coverages()))
