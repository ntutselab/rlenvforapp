import uuid

from dependency_injector.wiring import Provide

from . import (CreateEpisodeHandlerInput, CreateEpisodeHandlerOutput)
from RLEnvForApp.domain.environment.episodeHandler.DefaultForTestEpisodeHandler import DefaultForTestEpisodeHandler
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class CreateEpisodeHandlerUseCase:
    def __init__(self, repository: EpisodeHandlerRepository):
        self._repository = repository

    def execute(self, input: CreateEpisodeHandlerInput.CreateEpisodeHandlerInput, output: CreateEpisodeHandlerOutput.CreateEpisodeHandlerOutput):
        episodeHandler = Provide[EnvironmentDIContainers.episodeHandler(episodeIndex=input.getEpisodeIndex())]

        self._repository.add(EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler))

        output.setId(episodeHandler.getId())
        output.setIndex(episodeHandler.getIndex())
