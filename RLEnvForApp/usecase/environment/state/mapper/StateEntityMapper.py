from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.state.entity.AppElementEntity import AppElementEntity
from RLEnvForApp.usecase.environment.state.entity.CodeCoverageEntity import CodeCoverageEntity
from RLEnvForApp.usecase.environment.state.entity.StateEntity import StateEntity
from RLEnvForApp.usecase.environment.state.mapper import (AppElementEntityMapper,
                                                          CodeCoverageEntityMapper)


def _mappingAppElementEntitiesFrom(appElements: [AppElement]):
    appElementEntities: [AppElementEntity] = []
    for appElement in appElements:
        appElementEntities.append(AppElementEntityMapper.mappingAppElementEntityFrom(appElement))
    return appElementEntities

def _mappingAppElementFrom(appElementEntities: [AppElementEntity]):
    appElements: [AppElement] = []
    for appElementEntity in appElementEntities:
        appElements.append(AppElementEntityMapper.mappingAppElementEntityFrom(appElementEntity))
    return appElements

def _mappingCodeCoverageEntitiesFrom(codeCoverages: [CodeCoverage]) -> [CodeCoverageEntity]:
    codeCoverageEntityList: [CodeCoverageEntity] = []
    for codeCoverage in codeCoverages:
        codeCoverageEntityList.append(CodeCoverageEntityMapper.mappingCodeCoverageEntityFrom(codeCoverage))
    return codeCoverageEntityList

def _mappingCodeCoveragesFrom(codeCoverageEntities: [CodeCoverageEntity]) -> [CodeCoverage]:
    codeCoverages: [CodeCoverage] = []
    for codeCoverageEntity in codeCoverageEntities:
        codeCoverages.append(CodeCoverageEntityMapper.mappingCodeCoverageFrom(codeCoverageEntity=codeCoverageEntity))
    return codeCoverages

def mappingStateEntiyFrom(state: State) -> StateEntity:
    stateEntity = StateEntity(id=state.getId())
    stateEntity.setDom(state.getDOM())
    stateEntity.setUrl(state.getUrl())
    stateEntity.setScreenShot(state.getScreenShot())
    stateEntity.setInteractedElementEntity(AppElementEntityMapper.mappingAppElementEntityFrom(state.getInteractedElement()))
    stateEntity.setSelectedAppElementEntities(_mappingAppElementEntitiesFrom(state.getAllSelectedAppElements()))
    stateEntity.setFocusVector(state.getFocusVector())
    stateEntity.setActionType(state.getActionType())
    stateEntity.setCodeCoverages(_mappingCodeCoverageEntitiesFrom(state.getCodeCoverages()))
    stateEntity.setInputValue(state.getAppEventInputValue())
    stateEntity.setActionNumber(state.getActionNumber())
    stateEntity.setOriginalObservation(state.getOriginalObservation())
    return stateEntity

def mappingStateFrom(stateEntity: StateEntity):
    state = State(id=stateEntity.getId())
    state.setDOM(stateEntity.getDom())
    state.setUrl(stateEntity.getUrl())
    state.setScreenShot(stateEntity.getScreenShot())
    state.setInteractedElement(
        AppElementEntityMapper.mappingAppElementFrom(stateEntity.getInterActedElementEntity()))
    state.setSelectedAppElements(_mappingAppElementFrom(stateEntity.getSelectedAppElementEntities()))
    state.setFocusVector(stateEntity.getFocusVector())
    state.setActionType(stateEntity.getActionType())
    state.setCodeCoverages(_mappingCodeCoveragesFrom(stateEntity.getCodeCoverages()))
    state.setAppEventInputValue(stateEntity.getInputValue())
    state.setActionNumber(stateEntity.getActionNumber())
    state.setOriginalObservation(stateEntity.getOriginalObservation())
    return state
