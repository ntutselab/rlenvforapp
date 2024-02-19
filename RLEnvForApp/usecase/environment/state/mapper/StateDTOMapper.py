from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO
from RLEnvForApp.usecase.environment.autOperator.mapper import (AppElementDTOMapper,
                                                                CodeCoverageDTOMapper)
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO


def _mappingAppElementDTOsFrom(appElements: [AppElement]):
    appElementDTOs: [AppElementDTO] = []
    for appElement in appElements:
        appElementDTOs.append(AppElementDTOMapper.mappingAppElementDTOFrom(appElement=appElement))
    return appElementDTOs

def _mappingCodeCoverageDTOsFrom(codeCoverages: [CodeCoverage]):
    codeCoverageDTOs: [CodeCoverageDTO] = []
    for codeCoverage in codeCoverages:
        codeCoverageDTOs.append(CodeCoverageDTOMapper.mappingCodeCoverageDTOFrom(codeCoverage=codeCoverage))
    return codeCoverageDTOs

def mappingStateDTOFrom(state: State):
    stateDTO = StateDTO(id=state.getId())
    stateDTO.setDom(state.getDOM())
    stateDTO.setUrl(state.getUrl())
    stateDTO.setScreenShot(state.getScreenShot())
    stateDTO.setInteractedElementDTO(
        AppElementDTOMapper.mappingAppElementDTOFrom(state.getInteractedElement()))
    stateDTO.setSelectedAppElementDTOs(_mappingAppElementDTOsFrom(state.getAllSelectedAppElements()))
    stateDTO.setFocusVector(state.getFocusVector())
    stateDTO.setActionType(state.getActionType())
    stateDTO.setCodeCoverages(_mappingCodeCoverageDTOsFrom(state.getCodeCoverages()))
    stateDTO.setAppEventValue(state.getAppEventInputValue())
    return stateDTO
