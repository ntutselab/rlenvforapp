from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.environment.state.mapper import StateDTOMapper


def _mapping_state_dt_os_from(states: [State]) -> [StateDTO]:
    stateDTOs: [StateDTO] = []
    for state in states:
        stateDTOs.append(StateDTOMapper.mapping_state_dto_from(state=state))
    return stateDTOs


def mapping_episode_hanlder_dto_from(
        episodeHandler: IEpisodeHandler) -> EpisodeHandlerDTO:
    return EpisodeHandlerDTO(id=episodeHandler.get_id(),
                             episodeIndex=episodeHandler.get_episode_index(),
                             episodeStep=episodeHandler.get_episode_step(),
                             stateDTOs=_mapping_state_dt_os_from(episodeHandler.get_all_state()))
