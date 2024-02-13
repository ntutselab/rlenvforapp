from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.state.dto.stateDTO import StateDTO
from RLEnvForApp.usecase.environment.state.mapper import StateDTOMapper


def _mapping_state_dt_os_from(states: [State]) -> [StateDTO]:
    state_dt_os: [StateDTO] = []
    for state in states:
        state_dt_os.append(StateDTOMapper.mapping_state_dto_from(state=state))
    return state_dt_os


def mapping_episode_hanlder_dto_from(
        episode_handler: IEpisodeHandler) -> EpisodeHandlerDTO:
    return EpisodeHandlerDTO(id=episode_handler.get_id(),
                             episodeIndex=episode_handler.get_episode_index(),
                             episode_step=episode_handler.get_episode_step(),
                             state_dt_os=_mapping_state_dt_os_from(episode_handler.get_all_state()))
