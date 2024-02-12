import unittest

from RLEnvForApp.adapter.environment.autOperator.crawler.HtmlFileCrawler import HtmlFileCrawler
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.DefaultHtmlFileOperator import DefaultHtmlFileOperator
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionUseCase, ExecuteActionInput, ExecuteActionOutput
from RLEnvForApp.usecase.environment.resetEnvironment import ResetEnvironmentUseCase, ResetEnvironmentInput, ResetEnvironmentOutput
from RLEnvForApp.usecase.targetPage.create import CreateTargetPageUseCase, CreateTargetPageInput, CreateTargetPageOutput
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers


class testExecuteActionUseCaseTest(unittest.TestCase):
    def setUp(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(modules=[ExecuteActionUseCase, ResetEnvironmentUseCase])

        self._crawler = HtmlFileCrawler()
        self._autOperator = DefaultHtmlFileOperator(self._crawler)
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

        self.assertEqual(150, len(executeActionOutput.getObservation()))
        self.assertEqual(True, executeActionOutput.getIsDone())
        self.assertEqual(-25, executeActionOutput.getReward())
        self.assertEqual(300, executeActionOutput.getObservation()[0])

    def test_execute_input_action(self):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=7, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(2, len(self._episodeHandlerRepository.findById(self._episodeHandlerId).getStateEntities()))
        self.assertEqual(150, len(executeActionOutput.getObservation()))
        self.assertEqual(300, executeActionOutput.getObservation()[0])
        self.assertEqual(False, executeActionOutput.getIsDone())
        self.assertEqual(0.5, executeActionOutput.getReward())

    def test_execute_input_action_before_change_focus(self):
        self._executeAction(1)
        self._executeAction(1)
        self._executeAction(1)

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=3, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)
        self.assertEqual(150, len(executeActionOutput.getObservation()))
        self.assertEqual(300, executeActionOutput.getObservation()[3])
        self.assertEqual(False, executeActionOutput.getIsDone())
        self.assertEqual(-3, executeActionOutput.getReward())

    def test_execute_success_scenario(self):
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
        self._executeAction(6)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        self.assertEqual(150, len(executeActionOutput.getObservation()))
        self.assertEqual(50, executeActionOutput.getReward())
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
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput, output=resetEnvironmentUseOutput)

        self._episodeHandlerId = resetEnvironmentUseOutput.getEpisodeHandlerId()
