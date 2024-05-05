import uuid

from dependency_injector.wiring import Provide, inject
from selenium.common.exceptions import NoSuchElementException

from RLEnvForApp.domain.environment.actionCommand.InitiateToTargetActionCommand import NosuchElementException
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.actionCommand import (IActionCommand,
                                                          InitiateToTargetActionCommand)
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.observationService.IObservationService import \
    IObservationService
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.usecase.environment.episodeHandler.factory.EpisodeHandlerFactory import \
    EpisodeHandlerFactory
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.queueManager.ITargetPageQueueManagerService import \
    ITargetPageQueueManagerService

from . import ResetEnvironmentInput, ResetEnvironmentOutput
from ...targetPage.remove.RemoveTargetPageInput import RemoveTargetPageInput
from ...targetPage.remove.RemoveTargetPageOutput import RemoveTargetPageOutput
from ...targetPage.remove.RemoveTargetPageUseCase import RemoveTargetPageUseCase


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

    def execute(self, input: ResetEnvironmentInput.ResetEnvironmentInput, output: ResetEnvironmentOutput.ResetEnvironmentOutput):
        target_page = None
        episodeHandler = EpisodeHandlerFactory().createEpisodeHandler(
            id=str(uuid.uuid4()), episodeIndex=input.getEpisodeIndex())

        # Execute initiateToTargetActionCommand when the target page is not empty
        if not self._targetPageQueueManagerService.isEmpty():
            target_page = self._targetPageQueueManagerService.dequeueTargetPage()
            initiate_to_target_action_command: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                appEvents=target_page.getAppEvents(),
                rootPath=target_page.getRootUrl(),
                formXPath=target_page.getFormXPath())
        else:
            initiate_to_target_action_command: IActionCommand.IActionCommand = InitiateToTargetActionCommand.InitiateToTargetActionCommand(
                appEvents=[],
                rootPath="register.html",
                formXPath="")
        try:
            initiate_to_target_action_command.execute(operator=self._operator)
        except NosuchElementException:
            remove_target_page_use_case = RemoveTargetPageUseCase()
            remove_target_page_input = RemoveTargetPageInput(targetPageId=target_page.getId())
            remove_target_page_output = RemoveTargetPageOutput()
            remove_target_page_use_case.execute(input=remove_target_page_input, output=remove_target_page_output)
            raise NoSuchElementException("NoSuchElementException, remove target page")

        state: State = self._operator.getState()
        observation = self._observationService.getObservation(state=state)
        # state.setOriginalObservation(original_observation)

        episodeHandler.appendState(state)
        self._episodeHandlerRepository.add(
            EpisodeHandlerEntityMapper.mappingEpisodeHandlerEntityForm(episodeHandler=episodeHandler))

        url = ""
        formXPath = ""
        if target_page is not None:
            url = target_page.getTargetUrl()
            formXPath = target_page.getFormXPath()

        output.setTargetPageUrl(url=url)
        output.setTargetPageId(target_page.getId())
        output.setFormXPath(formXPath=formXPath)
        output.setEpisodeHandlerId(episodeHandler.getId())
        output.setObservation(observation)
        # output.setOriginalObservation(original_observation)
