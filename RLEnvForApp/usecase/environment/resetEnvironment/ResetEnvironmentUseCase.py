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
        self._episode_handler_repository = episodeHandlerRepository
        self._target_page_queue_manager_service = targetPageQueueManagerService
        self._observation_service = observationSerivce

    def execute(self, input: ResetEnvironmentInput.ResetEnvironmentInput,
                output: ResetEnvironmentOutput.ResetEnvironmentOutput):
        target_page = None
        episode_handler = EpisodeHandlerFactory().create_episode_handler(
            id=str(uuid.uuid4()), episodeIndex=input.get_episode_index())
        if not self._target_page_queue_manager_service.is_empty():
            target_page = self._target_page_queue_manager_service.dequeue_target_page()
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                app_events=target_page.get_app_events(),
                rootPath=target_page.get_root_url(),
                form_x_path=target_page.get_form_x_path())
        else:
            initiateToTargetActionCommand: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                app_events=[],
                rootPath="register.html",
                form_x_path="")
        initiateToTargetActionCommand.execute(operator=self._operator)

        state: State = self._operator.get_state()
        observation, originalObservation = self._observation_service.get_observation(
            state=state)
        state.set_original_observation(originalObservation)

        episode_handler.append_state(state)
        self._episode_handler_repository.add(
            EpisodeHandlerEntityMapper.mapping_episode_handler_entity_form(
                episode_handler=episode_handler))

        url = ""
        form_x_path = ""
        if target_page is not None:
            url = target_page.get_target_url()
            form_x_path = target_page.get_form_x_path()

        output.set_target_page_url(url=url)
        output.set_target_page_id(target_page.get_id())
        output.set_form_x_path(form_x_path=form_x_path)
        output.set_episode_handler_id(episode_handler.get_id())
        output.set_observation(observation)
        output.set_original_observation(originalObservation)
