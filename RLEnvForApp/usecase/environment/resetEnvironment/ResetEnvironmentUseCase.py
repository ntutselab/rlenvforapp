import uuid

from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommand import (
    IActionCommand, InitiateToTargetActionCommand)
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import \
    EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.queueManager.ITargetPageQueueManagerService import \
    ITargetPageQueueManagerService

from . import ResetEnvironmentInput, ResetEnvironmentOutput


class ResetEnvironmentUseCase:
    @inject
    def __init__(self, operator: IAUTOperator,
                 episodeHandlerRepository: EpisodeHandlerRepository = Provide[
                     EnvironmentDIContainers.episodeHandlerRepository],
                 targetPageQueueManagerService: ITargetPageQueueManagerService = Provide[
                     EnvironmentDIContainers.targetPageQueueManagerService],
                 observationSerivce: IObservationService = Provide[EnvironmentDIContainers.observationService]):
        self._operator = operator
        self._episodeHandlerRepository = episodeHandlerRepository
        self._targetPageQueueManagerService = targetPageQueueManagerService
        self._observationService = observationSerivce

    def execute(self, input: ResetEnvironmentInput.ResetEnvironmentInput,
                output: ResetEnvironmentOutput.ResetEnvironmentOutput):
        targetPage = None
        episodeHandler = EpisodeHandlerFactory().create_episode_handler(
            id=str(uuid.uuid4()), episodeIndex=input.get_episode_index())
        if not self._targetPageQueueManagerService.is_empty():
            targetPage = self._targetPageQueueManagerService.dequeue_target_page()
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                appEvents=targetPage.get_app_events(),
                rootPath=targetPage.get_root_url(),
                formXPath=targetPage.get_form_x_path())
        else:
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                appEvents=[],
                rootPath="register.html",
                formXPath="")
        initiateToTargetActionCommand.execute(operator=self._operator)

        state: State = self._operator.get_state()
        observation, originalObservation = self._observationService.get_observation(
            state=state)
        state.set_original_observation(originalObservation)

        episodeHandler.append_state(state)
        self._episodeHandlerRepository.add(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episodeHandler=episodeHandler))

        url = ""
        formXPath = ""
        if targetPage is not None:
            url = targetPage.get_target_url()
            formXPath = targetPage.get_form_x_path()

        output.set_target_page_url(url=url)
        output.set_target_page_id(targetPage.get_id())
        output.set_form_x_path(formXPath=formXPath)
        output.set_episode_handler_id(episodeHandler.get_id())
        output.set_observation(observation)
        output.set_original_observation(originalObservation)
