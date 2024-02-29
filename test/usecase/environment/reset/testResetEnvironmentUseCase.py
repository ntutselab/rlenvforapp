import unittest

from configuration.di.EnvironmentDIContainers import (EnvironmentDIContainers,
                                                      InMemoryEpisodeHandlerRepository)
from RLEnvForApp.adapter.environment.autOperator.crawler.HtmlFileCrawler import HtmlFileCrawler
from RLEnvForApp.usecase.environment.autOperator.ExperimentalHtmlFileOperator import \
    ExperimentalHtmlFileOperator
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.executeAction import (ExecuteActionInput, ExecuteActionOutput,
                                                           ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (ResetEnvironmentInput,
                                                              ResetEnvironmentOutput,
                                                              ResetEnvironmentUseCase)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput, CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)


class testResetEnvironmentUseCase(unittest.TestCase):
    def setUp(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(modules=[ExecuteActionUseCase,
                       ResetEnvironmentUseCase, CreateTargetPageUseCase])

        self._crawler = HtmlFileCrawler()
        self._autOperator = ExperimentalHtmlFileOperator(self._crawler)
        self._episodeHandlerRepository: EpisodeHandlerRepository = InMemoryEpisodeHandlerRepository.InMemoryEpisodeHandlerRepository(
            sizeLimit=1)

        self._createTargetPage()
        self._autOperator.resetCrawler("./register.html")

    def test_first_reset_environment(self):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()

        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput,
                                        output=resetEnvironmentUseOutput)

        episodeHandlerEntity = self._episodeHandlerRepository.findAll()[0]
        episodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(
            episodeHandlerEntity=episodeHandlerEntity)

        self.assertEqual(resetEnvironmentUseOutput.getEpisodeHandlerId(), episodeHandler.getId())

    def test_reset_environment(self):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput,
                                        output=resetEnvironmentUseOutput)

        self._executeAction(5, resetEnvironmentUseOutput.getEpisodeHandlerId())

        self._executeAction(1, resetEnvironmentUseOutput.getEpisodeHandlerId())
        self._executeAction(7, resetEnvironmentUseOutput.getEpisodeHandlerId())

        self._executeAction(1, resetEnvironmentUseOutput.getEpisodeHandlerId())
        self._executeAction(7, resetEnvironmentUseOutput.getEpisodeHandlerId())

        self._executeAction(1, resetEnvironmentUseOutput.getEpisodeHandlerId())
        self._executeAction(2, resetEnvironmentUseOutput.getEpisodeHandlerId())

        self._executeAction(1, resetEnvironmentUseOutput.getEpisodeHandlerId())
        self._executeAction(6, resetEnvironmentUseOutput.getEpisodeHandlerId())

        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput,
                                        output=resetEnvironmentUseOutput)

        self.assertEqual(1, len(self._episodeHandlerRepository.findAll()[0].getStateEntities()))

    def _executeAction(self, actionNumber: int, epsisodeHandlerId: str):
        self._executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=epsisodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()

        self._executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

    def _createTargetPage(self):
        targetPageUrl = "./register.html"
        rootUrl = "./register.html"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase()
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl,
                                                                            rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()

        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)
