from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler
from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO
from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.environment.episodeHandler.get import (
    GetEpisodeHandlerInput, GetEpisodeHandlerOutput)
from RLEnvForApp.usecase.environment.episodeHandler.mapper import (
    EpisodeHandlerDTOMapper, EpisodeHandlerEntityMapper)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository


class GetEpisodeHandlerUseCase:
    @inject
    def __init__(
            self, episodeHandlerRepository: EpisodeHandlerRepository = Provide[EnvironmentDIContainers.episodeHandlerRepository]):
        self._episode_handler_repository = episodeHandlerRepository

    def execute(self, input: GetEpisodeHandlerInput.GetEpisodeHandlerInput,
                output: GetEpisodeHandlerOutput.GetEpisodeHandlerOutput):
        episode_handler_entity: [EpisodeHandlerEntity] = self._episode_handler_repository.find_by_id(
            input.get_episode_handler_id())
        episode_handler: IEpisodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episode_handler_entity=episode_handler_entity)
        episode_handler_dto: EpisodeHandlerDTO = EpisodeHandlerDTOMapper.mapping_episode_hanlder_dto_from(
            episode_handler=episode_handler)
        output.set_episode_handler_dto(episode_handler_dto=episode_handler_dto)
