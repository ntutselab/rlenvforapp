from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import \
    EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.state.entity.StateEntity import \
    StateEntity
from RLEnvForApp.usecase.environment.state.mapper import StateEntityMapper


def mapping_episode_handler_entity_form(episode_handler: IEpisodeHandler):
    episode_handler_entity = EpisodeHandlerEntity(
        id=episode_handler.get_id(),
        episodeIndex=episode_handler.get_episode_index(),
        episode_step=episode_handler.get_episode_step())

    state_entities: [StateEntity] = []
    for state in episode_handler.get_all_state():
        state_entities.append(StateEntityMapper.mapping_state_entiy_from(state))
    episode_handler_entity.set_all_state_entities(state_entities)
    return episode_handler_entity


def mapping_episode_handler_form(episode_handler_entity: EpisodeHandlerEntity):
    episode_handler = EpisodeHandlerFactory().create_episode_handler(
        id=episode_handler_entity.get_id(), episodeIndex=episode_handler_entity.get_episode_index())
    for state_entity in episode_handler_entity.get_state_entities():
        episode_handler.append_state(
            state=StateEntityMapper.mapping_state_from(
                state_entity=state_entity))
    return episode_handler
