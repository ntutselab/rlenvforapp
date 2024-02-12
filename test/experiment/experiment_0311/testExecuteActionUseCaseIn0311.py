import unittest

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.environment.autOperator.crawler.HtmlFileCrawler import \
    HtmlFileCrawler
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.ClickForAllElementOperator import \
    ClickForAllElementOperator
from RLEnvForApp.usecase.environment.executeAction import (
    ExecuteActionInput, ExecuteActionOutput, ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (
    ResetEnvironmentInput, ResetEnvironmentOutput, ResetEnvironmentUseCase)
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)


class testExecuteActionUseCaseIn0311(unittest.TestCase):
    def set_up(self) -> None:
        container = EnvironmentDIContainers()
        container.config.from_ini(
            "configuration/config/20210311_word_2_vec_more_pages_experiment.ini")
        container.wire(modules=[ExecuteActionUseCase, ResetEnvironmentUseCase])

        self._crawler = HtmlFileCrawler()
        self._autOperator = ClickForAllElementOperator(self._crawler)
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._episodeHandlerId = ""
        self._create_target_page()
        self._reset_env()

    def test_execute_click_action(self):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

        self.assertEqual(900, len(executeActionOutput.get_observation()))
        self.assertEqual(False, executeActionOutput.get_is_done())
        self.assertEqual(-1, executeActionOutput.get_reward())

    def test_execute_input_action(self):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=7, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

        self.assertEqual(
            2, len(
                self._episodeHandlerRepository.find_by_id(
                    self._episodeHandlerId).get_state_entities()))
        self.assertEqual(900, len(executeActionOutput.get_observation()))
        self.assertEqual(False, executeActionOutput.get_is_done())
        self.assertEqual(1, executeActionOutput.get_reward())

    def test_execute_input_action_before_change_focus(self):
        self._execute_action(1)
        self._execute_action(1)
        self._execute_action(1)

        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=3, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)
        self.assertEqual(900, len(executeActionOutput.get_observation()))
        self.assertEqual(False, executeActionOutput.get_is_done())
        self.assertEqual(1, executeActionOutput.get_reward())

    def test_execute_success_scenario(self):
        self._execute_action(6)
        self._execute_action(8)
        self._execute_action(9)
        self._execute_action(2)
        self._execute_action(11)
        self._execute_action(11)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

        self.assertEqual(900, len(executeActionOutput.get_observation()))
        self.assertTrue(executeActionOutput.get_reward() > 100)
        self.assertEqual(True, executeActionOutput.get_is_done())

    def test_execute_passward_false_scenario(self):
        self._execute_action(5)

        self._execute_action(1)
        self._execute_action(7)

        self._execute_action(1)
        self._execute_action(7)

        self._execute_action(1)
        self._execute_action(2)

        self._execute_action(1)
        self._execute_action(6)

        self._execute_action(1)
        self._execute_action(5)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

        self.assertEqual(
            13, len(
                self._episodeHandlerRepository.find_by_id(
                    self._episodeHandlerId).get_state_entities()))
        self.assertEqual(150, len(executeActionOutput.get_observation()))
        self.assertEqual(-25, executeActionOutput.get_reward())
        self.assertEqual(True, executeActionOutput.get_is_done())

    def _execute_action(self, actionNumber: int):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)

    def _create_target_page(self):
        targetPageUrl = "./register.html"
        rootUrl = "./"
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(
            targetPageUrl=targetPageUrl, rootUrl=rootUrl, appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

    def _reset_env(self):
        resetEnvUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._autOperator, episodeHandlerRepository=self._episodeHandlerRepository)
        resetEnvUseInput = ResetEnvironmentInput.ResetEnvironmentIntput(
            episodeIndex=1)
        resetEnvUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvUseCase.execute(
            input=resetEnvUseInput,
            output=resetEnvUseOutput)

        self._episodeHandlerId = resetEnvUseOutput.get_episode_handler_id()
