from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import \
    EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.state.entity.StateEntity import StateEntity
from RLEnvForApp.usecase.environment.state.mapper import StateEntityMapper


def mappingEpisodeHandlerEntityForm(episodeHandler: IEpisodeHandler):
    episodeHandlerEntity = EpisodeHandlerEntity(id=episodeHandler.getId(
    ), episodeIndex=episodeHandler.getEpisodeIndex(), episodeStep=episodeHandler.getEpisodeStep())

    stateEntities: [StateEntity] = []
    for state in episodeHandler.getAllState():
        stateEntities.append(StateEntityMapper.mappingStateEntiyFrom(state))
    episodeHandlerEntity.setAllStateEntities(stateEntities)
    return episodeHandlerEntity


def mappingEpisodeHandlerForm(episodeHandlerEntity: EpisodeHandlerEntity):
    episodeHandler = EpisodeHandlerFactory().createEpisodeHandler(id=episodeHandlerEntity.getId(),
                                                                  episodeIndex=episodeHandlerEntity.getEpisodeIndex())
    for stateEntity in episodeHandlerEntity.getStateEntities():
        episodeHandler.appendState(
            state=StateEntityMapper.mappingStateFrom(stateEntity=stateEntity))
    return episodeHandler
