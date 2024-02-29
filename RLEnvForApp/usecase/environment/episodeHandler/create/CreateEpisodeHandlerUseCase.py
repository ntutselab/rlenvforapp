
from dependency_injector.wiring import Provide

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository

from . import CreateEpisodeHandlerInput, CreateEpisodeHandlerOutput


class CreateEpisodeHandlerUseCase:
    def __init__(self, repository: EpisodeHandlerRepository):
        self._repository = repository

    def execute(self, input: CreateEpisodeHandlerInput.CreateEpisodeHandlerInput, output: CreateEpisodeHandlerOutput.CreateEpisodeHandlerOutput):
        episodeHandler = Provide[EnvironmentDIContainers.episodeHandler(
            episodeIndex=input.getEpisodeIndex())]

        self._repository.add(EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(
            episodeHandler=episodeHandler))

        output.setId(episodeHandler.getId())
        output.setIndex(episodeHandler.getIndex())
