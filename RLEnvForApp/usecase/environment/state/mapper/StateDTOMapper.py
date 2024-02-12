from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import (
    AppElementDTOMapper, CodeCoverageDTOMapper)
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO


def _mapping_app_element_dt_os_from(appElements: [AppElement]):
    appElementDTOs: [AppElementDTO] = []
    for appElement in appElements:
        appElementDTOs.append(
            AppElementDTOMapper.mapping_app_element_dto_from(
                appElement=appElement))
    return appElementDTOs


def _mapping_code_coverage_dt_os_from(codeCoverages: [CodeCoverage]):
    codeCoverageDTOs: [CodeCoverageDTO] = []
    for codeCoverage in codeCoverages:
        codeCoverageDTOs.append(
            CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                codeCoverage=codeCoverage))
    return codeCoverageDTOs


def mapping_state_dto_from(state: State):
    stateDTO = StateDTO(id=state.get_id())
    stateDTO.set_dom(state.get_dom())
    stateDTO.set_url(state.get_url())
    stateDTO.set_screen_shot(state.get_screen_shot())
    stateDTO.set_interacted_element_dto(
        AppElementDTOMapper.mapping_app_element_dto_from(state.get_interacted_element()))
    stateDTO.set_selected_app_element_dt_os(
        _mapping_app_element_dt_os_from(
            state.get_all_selected_app_elements()))
    stateDTO.set_focus_vector(state.get_focus_vector())
    stateDTO.set_action_type(state.get_action_type())
    stateDTO.set_code_coverages(
        _mapping_code_coverage_dt_os_from(
            state.get_code_coverages()))
    stateDTO.set_app_event_value(state.get_app_event_input_value())
    return stateDTO
