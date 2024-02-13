
from dependency_injector.wiring import Provide

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository

from . import CreateEpisodeHandlerInput, CreateEpisodeHandlerOutput


class CreateEpisodeHandlerUseCase:
    def __init__(self, repository: EpisodeHandlerRepository):
        self._repository = repository

    def execute(self, input: CreateEpisodeHandlerInput.CreateEpisodeHandlerInput,
                output: CreateEpisodeHandlerOutput.CreateEpisodeHandlerOutput):
        episode_handler = Provide[EnvironmentDIContainers.episode_handler(
            episodeIndex=input.get_episode_index())]

        self._repository.add(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        output.set_id(episode_handler.get_id())
        output.set_index(episode_handler.get_index())
