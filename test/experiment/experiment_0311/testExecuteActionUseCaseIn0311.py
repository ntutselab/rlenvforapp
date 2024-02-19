import unittest

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.environment.autOperator.crawler.HtmlFileCrawler import HtmlFileCrawler
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.ClickForAllElementOperator import \
    ClickForAllElementOperator
from RLEnvForApp.usecase.environment.executeAction import (ExecuteActionInput, ExecuteActionOutput,
                                                           ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (ResetEnvironmentInput,
                                                              ResetEnvironmentOutput,
                                                              ResetEnvironmentUseCase)
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput, CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)


class testExecuteActionUseCaseIn0311(unittest.TestCase):
    def setUp(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/20210311_word_2_vec_more_pages_experiment.ini")
        container.wire(modules=[ExecuteActionUseCase, ResetEnvironmentUseCase])

        self._crawler = HtmlFileCrawler()
        self._autOperator = ClickForAllElementOperator(self._crawler)
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._episodeHandlerId = ""
        self._create_target_page()
        self._resetEnv()



    def test_execute_click_action(self):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(900, len(executeActionOutput.getObservation()))
        self.assertEqual(False, executeActionOutput.getIsDone())
        self.assertEqual(-1, executeActionOutput.getReward())

    def test_execute_input_action(self):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=7, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(2, len(self._episodeHandlerRepository.findById(self._episodeHandlerId).getStateEntities()))
        self.assertEqual(900, len(executeActionOutput.getObservation()))
        self.assertEqual(False, executeActionOutput.getIsDone())
        self.assertEqual(1, executeActionOutput.getReward())

    def test_execute_input_action_before_change_focus(self):
        self._executeAction(1)
        self._executeAction(1)
        self._executeAction(1)

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=3, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)
        self.assertEqual(900, len(executeActionOutput.getObservation()))
        self.assertEqual(False, executeActionOutput.getIsDone())
        self.assertEqual(1, executeActionOutput.getReward())

    def test_execute_success_scenario(self):
        self._executeAction(6)
        self._executeAction(8)
        self._executeAction(9)
        self._executeAction(2)
        self._executeAction(11)
        self._executeAction(11)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(900, len(executeActionOutput.getObservation()))
        self.assertTrue(executeActionOutput.getReward() > 100)
        self.assertEqual(True, executeActionOutput.getIsDone())

    def test_execute_passward_false_scenario(self):
        self._executeAction(5)

        self._executeAction(1)
        self._executeAction(7)

        self._executeAction(1)
        self._executeAction(7)

        self._executeAction(1)
        self._executeAction(2)

        self._executeAction(1)
        self._executeAction(6)

        self._executeAction(1)
        self._executeAction(5)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(13, len(self._episodeHandlerRepository.findById(self._episodeHandlerId).getStateEntities()))
        self.assertEqual(150, len(executeActionOutput.getObservation()))
        self.assertEqual(-25, executeActionOutput.getReward())
        self.assertEqual(True, executeActionOutput.getIsDone())

    def _executeAction(self, actionNumber: int):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=actionNumber, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

    def _create_target_page(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

    def _resetEnv(self):
        resetEnvUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvUseInput = ResetEnvironmentInput.ResetEnvironmentIntput(episodeIndex=1)
        resetEnvUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvUseCase.execute(input=resetEnvUseInput, output=resetEnvUseOutput)

        self._episodeHandlerId = resetEnvUseOutput.getEpisodeHandlerId()
