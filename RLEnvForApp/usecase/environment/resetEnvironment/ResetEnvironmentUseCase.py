import uuid

from dependency_injector.wiring import inject, Provide

from RLEnvForApp.domain.environment.state.State import State
from . import (ResetEnvironmentInput, ResetEnvironmentOutput)
from RLEnvForApp.domain.environment.actionCommand import (IActionCommand, InitiateToTargetActionCommand)
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import IObservationService
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.queueManager.ITargetPageQueueManagerService import ITargetPageQueueManagerService
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class ResetEnvironmentUseCase:
    @inject
    def __init__(self, operator: IAUTOperator,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[EnvironmentDIContainers.episodeHandlerRepository],
                 targetPageQueueManagerService: ITargetPageQueueManagerService = Provide[EnvironmentDIContainers.targetPageQueueManagerService],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService]):
        self._operator = operator
        self._episodeHandlerRepository = episodeHandlerRepository
        self._targetPageQueueManagerService = targetPageQueueManagerService
        self._observationService = observationSerivce

    def execute(self, input: ResetEnvironmentInput.ResetEnvironmentInput, output: ResetEnvironmentOutput.ResetEnvironmentOutput):
        targetPage = None
        episodeHandler = EpisodeHandlerFactory().createEpisodeHandler(id=str(uuid.uuid4()), episodeIndex=input.getEpisodeIndex())
        if not self._targetPageQueueManagerService.isEmpty():
            targetPage = self._targetPageQueueManagerService.dequeueTargetPage()
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                                                                            appEvents=targetPage.getAppEvents(),
                                                                            rootPath=targetPage.getRootUrl(),
                                                                            formXPath=targetPage.getFormXPath())
        else:
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                                                                            appEvents=[],
                                                                            rootPath="register.html",
                                                                            formXPath="")
        initiateToTargetActionCommand.execute(operator=self._operator)

        state: State = self._operator.getState()
        observation, originalObservation = self._observationService.getObservation(state=state)
        state.setOriginalObservation(originalObservation)

        episodeHandler.appendState(state)
        self._episodeHandlerRepository.add(EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler))

        url = ""
        formXPath = ""
        if targetPage is not None:
            url = targetPage.getTargetUrl()
            formXPath = targetPage.getFormXPath()

        output.setTargetPageUrl(url=url)
        output.setTargetPageId(targetPage.getId())
        output.setFormXPath(formXPath=formXPath)
        output.setEpisodeHandlerId(episodeHandler.getId())
        output.setObservation(observation)
        output.setOriginalObservation(originalObservation)
