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
        self._episodeHandlerRepository = episodeHandlerRepository

    def execute(self, input: GetEpisodeHandlerInput.GetEpisodeHandlerInput,
                output: GetEpisodeHandlerOutput.GetEpisodeHandlerOutput):
        episodeHandlerEntity: [EpisodeHandlerEntity] = self._episodeHandlerRepository.find_by_id(
            input.get_episode_handler_id())
        episodeHandler: IEpisodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episodeHandlerEntity=episodeHandlerEntity)
        episodeHandlerDTO: EpisodeHandlerDTO = EpisodeHandlerDTOMapper.mapping_episode_hanlder_dto_from(
            episodeHandler=episodeHandler)
        output.set_episode_handler_dto(episodeHandlerDTO=episodeHandlerDTO)
