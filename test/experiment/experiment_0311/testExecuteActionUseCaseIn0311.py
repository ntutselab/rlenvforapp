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
        self._aut_operator = ClickForAllElementOperator(self._crawler)
        self._target_page_repository = InMemoryTargetPageRepository()
        self._episode_handler_repository = InMemoryEpisodeHandlerRepository()
        self._episode_handler_id = ""
        self._create_target_page()
        self._reset_env()

    def test_execute_click_action(self):
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

        self.assertEqual(900, len(execute_action_output.get_observation()))
        self.assertEqual(False, execute_action_output.get_is_done())
        self.assertEqual(-1, execute_action_output.get_reward())

    def test_execute_input_action(self):
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=7, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

        self.assertEqual(
            2, len(
                self._episode_handler_repository.find_by_id(
                    self._episode_handler_id).get_state_entities()))
        self.assertEqual(900, len(execute_action_output.get_observation()))
        self.assertEqual(False, execute_action_output.get_is_done())
        self.assertEqual(1, execute_action_output.get_reward())

    def test_execute_input_action_before_change_focus(self):
        self._execute_action(1)
        self._execute_action(1)
        self._execute_action(1)

        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=3, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)
        self.assertEqual(900, len(execute_action_output.get_observation()))
        self.assertEqual(False, execute_action_output.get_is_done())
        self.assertEqual(1, execute_action_output.get_reward())

    def test_execute_success_scenario(self):
        self._execute_action(6)
        self._execute_action(8)
        self._execute_action(9)
        self._execute_action(2)
        self._execute_action(11)
        self._execute_action(11)
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

        self.assertEqual(900, len(execute_action_output.get_observation()))
        self.assertTrue(execute_action_output.get_reward() > 100)
        self.assertEqual(True, execute_action_output.get_is_done())

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
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=0, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

        self.assertEqual(
            13, len(
                self._episode_handler_repository.find_by_id(
                    self._episode_handler_id).get_state_entities()))
        self.assertEqual(150, len(execute_action_output.get_observation()))
        self.assertEqual(-25, execute_action_output.get_reward())
        self.assertEqual(True, execute_action_output.get_is_done())

    def _execute_action(self, actionNumber: int):
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=self._aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

    def _create_target_page(self):
        target_page_url = "./register.html"
        root_url = "./"
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._target_page_repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(
            target_page_url=target_page_url, root_url=root_url, app_event_dt_os=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

    def _reset_env(self):
        reset_env_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator, episodeHandlerRepository=self._episode_handler_repository)
        reset_env_use_input = ResetEnvironmentInput.ResetEnvironmentIntput(
            episodeIndex=1)
        reset_env_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        reset_env_use_case.execute(
            input=reset_env_use_input,
            output=reset_env_use_output)

        self._episode_handler_id = reset_env_use_output.get_episode_handler_id()
