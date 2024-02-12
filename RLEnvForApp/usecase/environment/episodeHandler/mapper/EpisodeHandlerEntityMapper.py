from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import \
    EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity
from RLEnvForApp.usecase.environment.state.mapper import StateEntityMapper


def mapping_episode_handler_entity_form(episodeHandler: IEpisodeHandler):
    episodeHandlerEntity = EpisodeHandlerEntity(
        id=episodeHandler.get_id(),
        episodeIndex=episodeHandler.get_episode_index(),
        episodeStep=episodeHandler.get_episode_step())

    stateEntities: [StateEntity] = []
    for state in episodeHandler.get_all_state():
        stateEntities.append(StateEntityMapper.mapping_state_entiy_from(state))
    episodeHandlerEntity.set_all_state_entities(stateEntities)
    return episodeHandlerEntity


def mapping_episode_handler_form(episodeHandlerEntity: EpisodeHandlerEntity):
    episodeHandler = EpisodeHandlerFactory().create_episode_handler(
        id=episodeHandlerEntity.get_id(), episodeIndex=episodeHandlerEntity.get_episode_index())
    for stateEntity in episodeHandlerEntity.get_state_entities():
        episodeHandler.append_state(
            state=StateEntityMapper.mapping_state_from(
                stateEntity=stateEntity))
    return episodeHandler
