import unittest

from configuration.di.EnvironmentDIContainers import (
    EnvironmentDIContainers, InMemoryEpisodeHandlerRepository)
from RLEnvForApp.adapter.environment.autOperator.crawler.HtmlFileCrawler import \
    HtmlFileCrawler
from RLEnvForApp.usecase.environment.autOperator.ExperimentalHtmlFileOperator import \
    ExperimentalHtmlFileOperator
from RLEnvForApp.usecase.environment.episodeHandler.mapper import \
    EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import (
    ExecuteActionInput, ExecuteActionOutput, ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (
    ResetEnvironmentInput, ResetEnvironmentOutput, ResetEnvironmentUseCase)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)


class testResetEnvironmentUseCase(unittest.TestCase):
    def set_up(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(
            modules=[
                ExecuteActionUseCase,
                ResetEnvironmentUseCase,
                CreateTargetPageUseCase])

        self._crawler = HtmlFileCrawler()
        self._autOperator = ExperimentalHtmlFileOperator(self._crawler)
        self._episodeHandlerRepository: EpisodeHandlerRepository = InMemoryEpisodeHandlerRepository.InMemoryEpisodeHandlerRepository(
            sizeLimit=1)

        self._create_target_page()
        self._autOperator.reset_crawler("./register.html")

    def test_first_reset_environment(self):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()

        resetEnvironmentUseCase.execute(
            input=resetEnvironmentUseInput,
            output=resetEnvironmentUseOutput)

        episodeHandlerEntity = self._episodeHandlerRepository.find_all()[0]
        episodeHandler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episodeHandlerEntity=episodeHandlerEntity)

        self.assertEqual(
            resetEnvironmentUseOutput.get_episode_handler_id(),
            episodeHandler.get_id())

    def test_reset_environment(self):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(
            input=resetEnvironmentUseInput,
            output=resetEnvironmentUseOutput)

        self._execute_action(5, resetEnvironmentUseOutput.get_episode_handler_id())

        self._execute_action(1, resetEnvironmentUseOutput.get_episode_handler_id())
        self._execute_action(7, resetEnvironmentUseOutput.get_episode_handler_id())

        self._execute_action(1, resetEnvironmentUseOutput.get_episode_handler_id())
        self._execute_action(7, resetEnvironmentUseOutput.get_episode_handler_id())

        self._execute_action(1, resetEnvironmentUseOutput.get_episode_handler_id())
        self._execute_action(2, resetEnvironmentUseOutput.get_episode_handler_id())

        self._execute_action(1, resetEnvironmentUseOutput.get_episode_handler_id())
        self._execute_action(6, resetEnvironmentUseOutput.get_episode_handler_id())

        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(
            input=resetEnvironmentUseInput,
            output=resetEnvironmentUseOutput)

        self.assertEqual(
            1, len(
                self._episodeHandlerRepository.find_all()[0].get_state_entities()))

    def _execute_action(self, actionNumber: int, epsisodeHandlerId: str):
        self._executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=epsisodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()

        self._executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

    def _create_target_page(self):
        targetPageUrl = "./register.html"
        rootUrl = "./register.html"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase()
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()

        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)
