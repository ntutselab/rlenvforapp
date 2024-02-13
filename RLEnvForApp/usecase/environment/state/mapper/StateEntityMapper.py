from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.state.entity.AppElementEntity import \
    AppElementEntity
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import \
    CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity
from RLEnvForApp.usecase.environment.state.mapper import (
    AppElementEntityMapper, CodeCoverageEntityMapper)


def _mapping_app_element_entities_from(app_elements: [AppElement]):
    app_element_entities: [AppElementEntity] = []
    for app_element in app_elements:
        app_element_entities.append(
            AppElementEntityMapper.mapping_app_element_entity_from(app_element))
    return app_element_entities


def _mapping_app_element_from(app_element_entities: [AppElementEntity]):
    app_elements: [AppElement] = []
    for app_element_entity in app_element_entities:
        app_elements.append(
            AppElementEntityMapper.mapping_app_element_entity_from(app_element_entity))
    return app_elements


def _mapping_code_coverage_entities_from(
        code_coverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    code_coverage_entity_list: [CodeCoverageEntity] = []
    for code_coverage in code_coverages:
        code_coverage_entity_list.append(
            CodeCoverageEntityMapper.mapping_code_coverage_entity_from(code_coverage))
    return code_coverage_entity_list


def _mapping_code_coverages_from(
        code_coverage_entities: [CodeCoverageEntity]) -> [CodeCoverage]:
    code_coverages: [CodeCoverage] = []
    for code_coverage_entity in code_coverage_entities:
        code_coverages.append(
            CodeCoverageEntityMapper.mapping_code_coverage_from(
                code_coverage_entity=code_coverage_entity))
    return code_coverages


def mapping_state_entiy_from(state: State) -> StateEntity:
    state_entity = StateEntity(id=state.get_id())
    state_entity.set_dom(state.get_dom())
    state_entity.set_url(state.get_url())
    state_entity.set_screen_shot(state.get_screen_shot())
    state_entity.set_interacted_element_entity(
        AppElementEntityMapper.mapping_app_element_entity_from(
            state.get_interacted_element()))
    state_entity.set_selected_app_element_entities(
        _mapping_app_element_entities_from(
            state.get_all_selected_app_elements()))
    state_entity.set_focus_vector(state.get_focus_vector())
    state_entity.set_action_type(state.get_action_type())
    state_entity.set_code_coverages(
        _mapping_code_coverage_entities_from(
            state.get_code_coverages()))
    state_entity.set_input_value(state.get_app_event_input_value())
    state_entity.set_action_number(state.get_action_number())
    state_entity.set_original_observation(state.get_original_observation())
    return state_entity


def mapping_state_from(state_entity: StateEntity):
    state = State(id=state_entity.get_id())
    state.set_dom(state_entity.get_dom())
    state.set_url(state_entity.get_url())
    state.set_screen_shot(state_entity.get_screen_shot())
    state.set_interacted_element(
        AppElementEntityMapper.mapping_app_element_from(state_entity.get_inter_acted_element_entity()))
    state.set_selected_app_elements(_mapping_app_element_from(
        state_entity.get_selected_app_element_entities()))
    state.set_focus_vector(state_entity.get_focus_vector())
    state.set_action_type(state_entity.get_action_type())
    state.set_code_coverages(
        _mapping_code_coverages_from(
            state_entity.get_code_coverages()))
    state.set_app_event_input_value(state_entity.get_input_value())
    state.set_action_number(state_entity.get_action_number())
    state.set_original_observation(state_entity.get_original_observation())
    return state
