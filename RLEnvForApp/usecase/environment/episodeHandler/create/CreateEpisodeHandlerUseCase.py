
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
        episodeHandler = Provide[EnvironmentDIContainers.episodeHandler(
            episodeIndex=input.get_episode_index())]

        self._repository.add(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        output.set_id(episodeHandler.get_id())
        output.set_index(episodeHandler.get_index())
