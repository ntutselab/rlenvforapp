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
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._applicationHandler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository,
            applicationHandler=self._applicationHandler)
        self._hirerarchyInitial.start_aut_server(
            "timeoff_management_with_coverage")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        self._crawler = SeleniumCrawler(browserName="Chrome")

    def tear_down(self) -> None:
        print("Crawler closed")
        self._crawler.close()
        for autEntity in self._autRepository.find_all():
            self._hirerarchyInitial.stop_aut_server(autEntity.get_id())

    def test_crawljax_goto_root_page_error(self):
        self.assertFalse(self._crawler.reset(path="", formXPath=""))

    def test_crawljax_goto_register_get_coverage(self):
        statementCoverageLength = 0
        branchCoverageLength = 0
        statementCoveragedAmount = 0
        branchCoveragedAmount = 0

        self._autOperator = IRobotOperator(
            self._crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))

        self._autOperator.reset_crawler(path="http://localhost:3000")
        self._autOperator.get_state()

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        self._autOperator.get_state()

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]",
            value="Company name")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            1, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]", value="Kai")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            2, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]",
            value="Huang")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            3, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]",
            value="test@ntut.edu.tw")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            4, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]",
            value="123456")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            5, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]",
            value="123456")
        self._autOperator.change_focus()
        self._autOperator.get_focused_app_element()
        self.assertEqual(
            6, self._autOperator.get_state().get_focus_vector().index(True))

        self._autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        self._autOperator.get_focused_app_element()
        self._autOperator.execute_app_event(xpath="", value="")
        state = self._autOperator.get_state()
        self._autOperator.get_focused_app_element()

        self.assertEqual("http://localhost:3000/calendar/", state.get_url())
        if len(state.get_focus_vector()) == 0:
            self.assertEqual(0, len(state.get_focus_vector()))
            self.assertTrue(state.is_selected_app_elements_empty())
            self.assertEqual(None, state.get_interacted_element())
        else:
            self.assertEqual(0, state.get_focus_vector().index(True))

        codeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(
            serverIp="localhost", serverPort=3000)
        codeCoverages: [
            CodeCoverage] = codeCoverageCollector.get_code_coverage_dt_os()
        for i in codeCoverages:
            codeCoverage: CodeCoverage = CodeCoverageEntityMapper.mapping_code_coverage_from(
                i)
            if i.get_code_coverage_type() == "statement coverage":
                statementCoverageLength = codeCoverage.get_code_coverage_vector_length()
                statementCoveragedAmount = codeCoverage.get_covered_amount()
            if i.get_code_coverage_type() == "branch coverage":
                branchCoverageLength = codeCoverage.get_code_coverage_vector_length()
                branchCoveragedAmount = codeCoverage.get_covered_amount()

        self.assertEqual(1036, branchCoverageLength)
        self.assertEqual(2698, statementCoverageLength)
        self.assertEqual(170, branchCoveragedAmount)
        self.assertEqual(814, statementCoveragedAmount)

    def test_change_focus_command(self):
        self._autOperator = IRobotOperator(
            self._crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._create_target_page()
        self._reset_env(autOperator=self._autOperator)
        state = self._autOperator.get_state()
        self.assertEqual(
            0, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.get_state()
        self.assertEqual(
            0, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.get_state()
        self.assertEqual(
            1, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

        self._execute_action(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.get_state()
        self.assertEqual(
            2, state.get_all_selected_app_elements().index(
                state.get_interacted_element()))

    def _execute_action(self, autOperator: IAUTOperator, actionNumber: int):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository,
                                                                         rewardCalculatorService=DefaultForTestRewardCalculatorService(),
                                                                         actionCommandFactory=DefaultForTestActionCommandFactoryService(),
                                                                         observationSerivce=DefaultForTestObservationService())
        executeActionInput = ExecuteActionInput.ExecuteActionInput(
            actionNumber=actionNumber, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(
            input=executeActionInput,
            output=executeActionOutput)
        return executeActionOutput

    def _create_target_page(self):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(
            targetPageUrl="http://localhost:3000", rootUrl="http://localhost:3000", appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(
            createTargetPageInput, createTargetPageOutput)

    def _reset_env(self, autOperator: IAUTOperator):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=autOperator,
                                                                                  episodeHandlerRepository=self._episodeHandlerRepository,
                                                                                  targetPageQueueManagerService=HtmlFileTargetPageQueueManagerService(
                                                                                      repository=self._targetPageRepository),
                                                                                  observationSerivce=DefaultForTestObservationService())
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(
            input=resetEnvironmentUseInput,
            output=resetEnvironmentUseOutput)

        self._episodeHandlerId = resetEnvironmentUseOutput.get_episode_handler_id()
        return resetEnvironmentUseOutput
