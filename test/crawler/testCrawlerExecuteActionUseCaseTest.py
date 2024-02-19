from unittest import TestCase

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import DockerServerHandler
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import SeleniumCrawler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository
from RLEnvForApp.domain.environment.actionCommandFactoryService.DefaultForTestActionCommandFactoryService import \
    DefaultForTestActionCommandFactoryService

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.rewardCalculatorService.DefaultForTestRewardCalculatorService import \
    DefaultForTestRewardCalculatorService
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage
from RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService import \
    DefaultForTestObservationService

from RLEnvForApp.usecase.environment.autOperator.IRobotOperator import IRobotOperator
from RLEnvForApp.domain.environment.observationService.DefaultForTestObservationService import \
    DefaultForTestObservationService
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.environment.executeAction import *
from RLEnvForApp.usecase.environment.resetEnvironment import *
from RLEnvForApp.usecase.targetPage.create import *
from RLEnvForApp.usecase.targetPage.queueManager.HtmlFileTargetPageQueueManagerService import \
    HtmlFileTargetPageQueueManagerService
from test.usecase.HirerarchyInitial import HirerarchyInitial


class testCrawlerExecuteActionUseCaseTest(TestCase):
    def setUp(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._applicationHandler = DockerServerHandler("RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(autRepository=self._autRepository, applicationHandler=self._applicationHandler)
        self._hirerarchyInitial.startAUTServer("timeoff_management_with_coverage")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        self._crawler = SeleniumCrawler(browserName="Chrome")

    def tearDown(self) -> None:
        print("Crawler closed")
        self._crawler.close()
        for autEntity in self._autRepository.findAll():
            self._hirerarchyInitial.stopAUTServer(autEntity.getId())

    def test_crawljax_goto_root_page_error(self):
        self.assertFalse(self._crawler.reset(path="", formXPath=""))


    def test_crawljax_goto_register_get_coverage(self):
        statementCoverageLength = 0
        branchCoverageLength = 0
        statementCoveragedAmount = 0
        branchCoveragedAmount = 0

        self._autOperator = IRobotOperator(self._crawler, IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000))

        self._autOperator.resetCrawler(path="http://localhost:3000")
        self._autOperator.getState()

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        self._autOperator.getState()


        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]", value="Company name")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(1, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]", value="Kai")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(2, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]", value="Huang")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(3, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]", value="test@ntut.edu.tw")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(4, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]", value="123456")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(5, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]", value="123456")
        self._autOperator.changeFocus()
        self._autOperator.getFocusedAppElement()
        self.assertEqual(6, self._autOperator.getState().getFocusVector().index(True))

        self._autOperator.executeAppEvent(xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        self._autOperator.getFocusedAppElement()
        self._autOperator.executeAppEvent(xpath="", value="")
        state = self._autOperator.getState()
        self._autOperator.getFocusedAppElement()

        self.assertEqual("http://localhost:3000/calendar/", state.getUrl())
        if len(state.getFocusVector()) == 0:
            self.assertEqual(0, len(state.getFocusVector()))
            self.assertTrue(state.isSelectedAppElementsEmpty())
            self.assertEqual(None, state.getInteractedElement())
        else:
            self.assertEqual(0, state.getFocusVector().index(True))

        codeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000)
        codeCoverages: [CodeCoverage] = codeCoverageCollector.getCodeCoverageDTOs()
        for i in codeCoverages:
            codeCoverage: CodeCoverage = CodeCoverageEntityMapper.mappingCodeCoverageFrom(i)
            if i.getCodeCoverageType() == "statement coverage":
                statementCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                statementCoveragedAmount = codeCoverage.getCoveredAmount()
            if i.getCodeCoverageType() == "branch coverage":
                branchCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                branchCoveragedAmount = codeCoverage.getCoveredAmount()

        self.assertEqual(1036, branchCoverageLength)
        self.assertEqual(2698, statementCoverageLength)
        self.assertEqual(170, branchCoveragedAmount)
        self.assertEqual(814, statementCoveragedAmount)

    def test_change_focus_command(self):
        self._autOperator = IRobotOperator(self._crawler, IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000))
        self._createTargetPage()
        self._resetEnv(autOperator=self._autOperator)
        state = self._autOperator.getState()
        self.assertEqual(0, state.getAllSelectedAppElements().index(state.getInteractedElement()))


        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.getState()
        self.assertEqual(0, state.getAllSelectedAppElements().index(state.getInteractedElement()))

        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.getState()
        self.assertEqual(1, state.getAllSelectedAppElements().index(state.getInteractedElement()))

        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        state = self._autOperator.getState()
        self.assertEqual(2, state.getAllSelectedAppElements().index(state.getInteractedElement()))

    def _executeAction(self, autOperator: IAUTOperator, actionNumber: int):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository,
                                                                         rewardCalculatorService=DefaultForTestRewardCalculatorService(),
                                                                         actionCommandFactory=DefaultForTestActionCommandFactoryService(),
                                                                          observationSerivce=DefaultForTestObservationService())
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=actionNumber, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)
        return executeActionOutput

    def _createTargetPage(self):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl="http://localhost:3000", rootUrl="http://localhost:3000", appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

    def _resetEnv(self, autOperator: IAUTOperator):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=autOperator,
                                                                          episodeHandlerRepository=self._episodeHandlerRepository,
                                                                          targetPageQueueManagerService=HtmlFileTargetPageQueueManagerService(repository=self._targetPageRepository),
                                                                          observationSerivce=DefaultForTestObservationService())
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput, output=resetEnvironmentUseOutput)

        self._episodeHandlerId = resetEnvironmentUseOutput.getEpisodeHandlerId()
        return resetEnvironmentUseOutput
