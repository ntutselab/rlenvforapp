from test.usecase.HirerarchyInitial import HirerarchyInitial
from unittest import TestCase

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import \
    DockerServerHandler
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
# from RLEnvForApp.adapter.environment.autOperator.crawler.IRobotCrawler import IRobotCrawler
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import \
    SeleniumCrawler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.domain.environment.actionCommandFactoryService.DefaultForTestActionCommandFactoryService import \
    DefaultForTestActionCommandFactoryService
from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator
from RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService import \
    DefaultForTestObservationService
from RLEnvForApp.domain.environment.rewardCalculatorService.DefaultForTestRewardCalculatorService import \
    DefaultForTestRewardCalculatorService
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.usecase.environment.autOperator.IRobotOperator import \
    IRobotOperator
from RLEnvForApp.usecase.environment.executeAction import (
    ExecuteActionInput, ExecuteActionOutput, ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (
    ResetEnvironmentInput, ResetEnvironmentOutput, ResetEnvironmentUseCase)
from RLEnvForApp.usecase.environment.state.mapper import \
    CodeCoverageEntityMapper
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.queueManager.HtmlFileTargetPageQueueManagerService import \
    HtmlFileTargetPageQueueManagerService


class testCrawlerExecuteActionUseCaseTest(TestCase):
    def set_up(self) -> None:
        self._aut_repository = InMemoryApplicationUnderTestRepository()
        self._target_page_repository = InMemoryTargetPageRepository()
        self._episode_handler_repository = InMemoryEpisodeHandlerRepository()
        self._application_handler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchy_initial = HirerarchyInitial(
            autRepository=self._aut_repository,
            applicationHandler=self._application_handler)
        self._hirerarchy_initial.start_aut_server(
            "timeoff_management_with_coverage")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        self._crawler = SeleniumCrawler(browser_name="Chrome")

    def tear_down(self) -> None:
        print("Crawler closed")
        self._crawler.close()
        for aut_entity in self._aut_repository.find_all():
            self._hirerarchy_initial.stop_aut_server(aut_entity.get_id())

    def test_crawljax_goto_root_page_error(self):
        self.assertFalse(self._crawler.reset(path="", form_xpath=""))

    def test_crawljax_goto_register_get_coverage(self):
        statement_coverage_length = 0
        branch_coverage_length = 0
        statement_coveraged_amount = 0
        branch_coveraged_amount = 0

        self._aut_operator = IRobotOperator(
            self._crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))

        self._aut_operator.reset_crawler(path="http://localhost:3000")
        self._aut_operator.get_state()

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        self._aut_operator.get_state()

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]",
            value="Company name")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            1, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]", value="Kai")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            2, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]",
            value="Huang")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            3, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]",
            value="test@ntut.edu.tw")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            4, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]",
            value="123456")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            5, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]",
            value="123456")
        self._aut_operator.change_focus()
        self._aut_operator.get_focused_app_element()
        self.assertEqual(
            6, self._aut_operator.get_state().get_focus_vector().index(True))

        self._aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        self._aut_operator.get_focused_app_element()
        self._aut_operator.execute_app_event(xpath="", value="")
        state = self._aut_operator.get_state()
        self._aut_operator.get_focused_app_element()

        self.assertEqual("http://localhost:3000/calendar/", state.get_url())
        if len(state.get_focus_vector()) == 0:
            self.assertEqual(0, len(state.get_focus_vector()))
            self.assertTrue(state.is_selected_app_elements_empty())
            self.assertEqual(None, state.get_interacted_element())
        else:
            self.assertEqual(0, state.get_focus_vector().index(True))

        code_coverage_collector = IstanbulMiddlewareCodeCoverageCollector(
            serverIp="localhost", serverPort=3000)
        code_coverages: [
            CodeCoverage] = code_coverage_collector.get_code_coverage_dt_os()
        for i in code_coverages:
            code_coverage: CodeCoverage = CodeCoverageEntityMapper.mapping_code_coverage_from(
                i)
            if i.get_code_coverage_type() == "statement coverage":
                statement_coverage_length = code_coverage.get_code_coverage_vector_length()
                statement_coveraged_amount = code_coverage.get_covered_amount()
            if i.get_code_coverage_type() == "branch coverage":
                branch_coverage_length = code_coverage.get_code_coverage_vector_length()
                branch_coveraged_amount = code_coverage.get_covered_amount()

        self.assertEqual(1036, branch_coverage_length)
        self.assertEqual(2698, statement_coverage_length)
        self.assertEqual(170, branch_coveraged_amount)
        self.assertEqual(814, statement_coveraged_amount)

    def test_change_focus_command(self):
        self._aut_operator = IRobotOperator(
            self._crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._create_target_page()
        self._reset_env(aut_operator=self._aut_operator)
        state = self._aut_operator.get_state()
        self.assertEqual(
            0, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(aut_operator=self._aut_operator, actionNumber=1)
        state = self._aut_operator.get_state()
        self.assertEqual(
            0, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(aut_operator=self._aut_operator, actionNumber=1)
        state = self._aut_operator.get_state()
        self.assertEqual(
            1, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(aut_operator=self._aut_operator, actionNumber=1)
        state = self._aut_operator.get_state()
        self.assertEqual(
            2, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

    def _execute_action(self, aut_operator: IAUTOperator, actionNumber: int):
        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(aut_operator=aut_operator,
                                                                         episodeHandlerRepository=self._episode_handler_repository,
                                                                         rewardCalculatorService=DefaultForTestRewardCalculatorService(),
                                                                         actionCommandFactory=DefaultForTestActionCommandFactoryService(),
                                                                         observationSerivce=DefaultForTestObservationService())
        execute_action_input = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(
            input=execute_action_input,
            output=execute_action_output)
        return execute_action_output

    def _create_target_page(self):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._target_page_repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(
            target_page_url="http://localhost:3000", root_url="http://localhost:3000", app_event_dt_os=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

    def _reset_env(self, aut_operator: IAUTOperator):
        reset_environment_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=aut_operator,
                                                                                  episodeHandlerRepository=self._episode_handler_repository,
                                                                                  targetPageQueueManagerService=HtmlFileTargetPageQueueManagerService(
                                                                                      repository=self._target_page_repository),
                                                                                  observationSerivce=DefaultForTestObservationService())
        reset_environment_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        reset_environment_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        reset_environment_use_case.execute(
            input=reset_environment_use_input,
            output=reset_environment_use_output)

        self._episode_handler_id = reset_environment_use_output.get_episode_handler_id()
        return reset_environment_use_output
