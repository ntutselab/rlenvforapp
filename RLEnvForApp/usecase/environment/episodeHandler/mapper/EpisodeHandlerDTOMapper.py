from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.environment.state.mapper import StateDTOMapper


def _mappingStateDTOsFrom(states: [State]) -> [StateDTO]:
    stateDTOs: [StateDTO] = []
    for state in states:
        stateDTOs.append(StateDTOMapper.mappingStateDTOFrom(state=state))
    return stateDTOs


def mappingEpisodeHanlderDTOFrom(episodeHandler: IEpisodeHandler) -> EpisodeHandlerDTO:
    return EpisodeHandlerDTO(id=episodeHandler.getId(),
                             episodeIndex=episodeHandler.getEpisodeIndex(),
                             episodeStep=episodeHandler.getEpisodeStep(),
                             stateDTOs=_mappingStateDTOsFrom(episodeHandler.getAllState()))
