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


def _mapping_app_element_dt_os_from(app_elements: [AppElement]):
    app_element_dt_os: [AppElementDTO] = []
    for app_element in app_elements:
        app_element_dt_os.append(
            AppElementDTOMapper.mapping_app_element_dto_from(
                app_element=app_element))
    return app_element_dt_os


def _mapping_code_coverage_dt_os_from(code_coverages: [CodeCoverage]):
    code_coverage_dt_os: [CodeCoverageDTO] = []
    for code_coverage in code_coverages:
        code_coverage_dt_os.append(
            CodeCoverageDTOMapper.mapping_code_coverage_dto_from(
                code_coverage=code_coverage))
    return code_coverage_dt_os


def mapping_state_dto_from(state: State):
    state_dto = StateDTO(id=state.get_id())
    state_dto.set_dom(state.get_dom())
    state_dto.set_url(state.get_url())
    state_dto.set_screen_shot(state.get_screen_shot())
    state_dto.set_interacted_element_dto(
        AppElementDTOMapper.mapping_app_element_dto_from(state.get_interacted_element()))
    state_dto.set_selected_app_element_dt_os(
        _mapping_app_element_dt_os_from(
            state.get_all_selected_app_elements()))
    state_dto.set_focus_vector(state.get_focus_vector())
    state_dto.set_action_type(state.get_action_type())
    state_dto.set_code_coverages(
        _mapping_code_coverage_dt_os_from(
            state.get_code_coverages()))
    state_dto.set_app_event_value(state.get_app_event_input_value())
    return state_dto
