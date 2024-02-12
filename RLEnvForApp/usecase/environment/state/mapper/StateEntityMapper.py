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


def _mapping_app_element_entities_from(appElements: [AppElement]):
    appElementEntities: [AppElementEntity] = []
    for appElement in appElements:
        appElementEntities.append(
            AppElementEntityMapper.mapping_app_element_entity_from(appElement))
    return appElementEntities


def _mapping_app_element_from(appElementEntities: [AppElementEntity]):
    appElements: [AppElement] = []
    for appElementEntity in appElementEntities:
        appElements.append(
            AppElementEntityMapper.mapping_app_element_entity_from(appElementEntity))
    return appElements


def _mapping_code_coverage_entities_from(
        codeCoverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    codeCoverageEntityList: [CodeCoverageEntity] = []
    for codeCoverage in codeCoverages:
        codeCoverageEntityList.append(
            CodeCoverageEntityMapper.mapping_code_coverage_entity_from(codeCoverage))
    return codeCoverageEntityList


def _mapping_code_coverages_from(
        codeCoverageEntities: [CodeCoverageEntity]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageEntity in codeCoverageEntities:
        codeCoverages.append(
            CodeCoverageEntityMapper.mapping_code_coverage_from(
                codeCoverageEntity=codeCoverageEntity))
    return codeCoverages


def mapping_state_entiy_from(state: State) -> StateEntity:
    stateEntity = StateEntity(id=state.get_id())
    stateEntity.set_dom(state.get_dom())
    stateEntity.set_url(state.get_url())
    stateEntity.set_screen_shot(state.get_screen_shot())
    stateEntity.set_interacted_element_entity(
        AppElementEntityMapper.mapping_app_element_entity_from(
            state.get_interacted_element()))
    stateEntity.set_selected_app_element_entities(
        _mapping_app_element_entities_from(
            state.get_all_selected_app_elements()))
    stateEntity.set_focus_vector(state.get_focus_vector())
    stateEntity.set_action_type(state.get_action_type())
    stateEntity.set_code_coverages(
        _mapping_code_coverage_entities_from(
            state.get_code_coverages()))
    stateEntity.set_input_value(state.get_app_event_input_value())
    stateEntity.set_action_number(state.get_action_number())
    stateEntity.set_original_observation(state.get_original_observation())
    return stateEntity


def mapping_state_from(stateEntity: StateEntity):
    state = State(id=stateEntity.get_id())
    state.set_dom(stateEntity.get_dom())
    state.set_url(stateEntity.get_url())
    state.set_screen_shot(stateEntity.get_screen_shot())
    state.set_interacted_element(
        AppElementEntityMapper.mapping_app_element_from(stateEntity.get_inter_acted_element_entity()))
    state.set_selected_app_elements(_mapping_app_element_from(
        stateEntity.get_selected_app_element_entities()))
    state.set_focus_vector(stateEntity.get_focus_vector())
    state.set_action_type(stateEntity.get_action_type())
    state.set_code_coverages(
        _mapping_code_coverages_from(
            stateEntity.get_code_coverages()))
    state.set_app_event_input_value(stateEntity.get_input_value())
    state.set_action_number(stateEntity.get_action_number())
    state.set_original_observation(stateEntity.get_original_observation())
    return state
