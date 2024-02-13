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
        self._aut_operator = ExperimentalHtmlFileOperator(self._crawler)
        self._episode_handler_repository: EpisodeHandlerRepository = InMemoryEpisodeHandlerRepository.InMemoryEpisodeHandlerRepository(
            sizeLimit=1)

        self._create_target_page()
        self._aut_operator.reset_crawler("./register.html")

    def test_first_reset_environment(self):
        reset_environment_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator, episodeHandlerRepository=self._episode_handler_repository)
        reset_environment_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        reset_environment_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()

        reset_environment_use_case.execute(
            input=reset_environment_use_input,
            output=reset_environment_use_output)

        episode_handler_entity = self._episode_handler_repository.find_all()[0]
        episode_handler = EpisodeHandlerEntityMapper.mapping_episode_handler_form(
            episode_handler_entity=episode_handler_entity)

        self.assertEqual(
            reset_environment_use_output.get_episode_handler_id(),
            episode_handler.get_id())

    def test_reset_environment(self):
        reset_environment_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator, episodeHandlerRepository=self._episode_handler_repository)
        reset_environment_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        reset_environment_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        reset_environment_use_case.execute(
            input=reset_environment_use_input,
            output=reset_environment_use_output)

        self._execute_action(5, reset_environment_use_output.get_episode_handler_id())

        self._execute_action(1, reset_environment_use_output.get_episode_handler_id())
        self._execute_action(7, reset_environment_use_output.get_episode_handler_id())

        self._execute_action(1, reset_environment_use_output.get_episode_handler_id())
        self._execute_action(7, reset_environment_use_output.get_episode_handler_id())

        self._execute_action(1, reset_environment_use_output.get_episode_handler_id())
        self._execute_action(2, reset_environment_use_output.get_episode_handler_id())

        self._execute_action(1, reset_environment_use_output.get_episode_handler_id())
        self._execute_action(6, reset_environment_use_output.get_episode_handler_id())

        reset_environment_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator, episodeHandlerRepository=self._episode_handler_repository)
        reset_environment_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        reset_environment_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        reset_environment_use_case.execute(
            input=reset_environment_use_input,
            output=reset_environment_use_output)

        self.assertEqual(
            1, len(
                self._episode_handler_repository.find_all()[0].get_state_entities()))

    def _execute_action(self, actionNumber: int, epsisodeHandlerId: str):
        self._execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(
            aut_operator=self._aut_operator, episodeHandlerRepository=self._episode_handler_repository)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=epsisodeHandlerId)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()

        self._execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)

    def _create_target_page(self):
        target_page_url = "./register.html"
        root_url = "./register.html"
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase()
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url, app_event_dt_os=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()

        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)
