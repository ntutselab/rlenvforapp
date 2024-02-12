import time
from unittest import TestCase

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import DockerServerHandler
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.IRobotCrawler import IRobotCrawler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.adapter.repository.episodeHandler.InMemoryEpisodeHandlerRepository import \
    InMemoryEpisodeHandlerRepository
from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import InMemoryTargetPageRepository

from RLEnvForApp.domain.environment.autOperator.IAUTOperator import IAUTOperator
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import IEpisodeHandler
from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage

from RLEnvForApp.usecase.environment.autOperator.IRobotOperator import IRobotOperator
from RLEnvForApp.usecase.environment.episodeHandler.mapper import EpisodeHandlerEntityMapper
from RLEnvForApp.usecase.environment.state.mapper import CodeCoverageEntityMapper
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionUseCase, ExecuteActionInput, ExecuteActionOutput
from RLEnvForApp.usecase.environment.resetEnvironment import ResetEnvironmentUseCase, ResetEnvironmentInput, ResetEnvironmentOutput
from RLEnvForApp.usecase.targetPage.create import CreateTargetPageUseCase, CreateTargetPageInput, CreateTargetPageOutput
from RLEnvForApp.usecase.targetPage.queueManager.HtmlFileTargetPageQueueManagerService import \
    HtmlFileTargetPageQueueManagerService

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from test.usecase.HirerarchyInitial import HirerarchyInitial


class testWebCrawlerGetCoverage(TestCase):
    def setUp(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._targetPageRepository = InMemoryTargetPageRepository()
        self._episodeHandlerRepository = InMemoryEpisodeHandlerRepository()
        self._applicationHandler = DockerServerHandler("RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(autRepository=self._autRepository, applicationHandler=self._applicationHandler)
        self._hirerarchyInitial.startAUTServer("timeoff_management_with_coverage")
        self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        time.sleep(5)

    def tearDown(self) -> None:
        self._crawler.close()
        for autEntity in self._autRepository.findAll():
            self._hirerarchyInitial.stopAUTServer(autEntity.getId())


    def test_crawljax_get_coverage(self):
        self._crawler.reset(path="http://localhost:3000")
        time.sleep(5)
        url = self._crawler.getUrl()

        codeCoverageCollector = IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000)
        codeCoverages: [CodeCoverage] = codeCoverageCollector.getCodeCoverageDTOs()
        statementCoverageLength = 0
        branchCoverageLength = 0
        statementCoveragedAmount = 0
        branchCoveragedAmount = 0
        for i in codeCoverages:
            codeCoverage: CodeCoverage = CodeCoverageEntityMapper.mappingCodeCoverageFrom(i)
            if i.getCodeCoverageType() == "statement coverage":
                statementCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                statementCoveragedAmount = codeCoverage.getCoveredAmount()
            if i.getCodeCoverageType() == "branch coverage":
                branchCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                branchCoveragedAmount = codeCoverage.getCoveredAmount()

        self.assertEqual("http://localhost:3000", url)
        self.assertEqual(1036, branchCoverageLength)
        self.assertEqual(2698, statementCoverageLength)

        self.assertEqual(31, branchCoveragedAmount)
        self.assertEqual(472, statementCoveragedAmount)

    def test_crawljax_goto_register_get_coverage(self):
        statementCoverageLength = 0
        branchCoverageLength = 0
        statementCoveragedAmount = 0
        branchCoveragedAmount = 0

        self._crawler.reset(path="http://localhost:3000")
        time.sleep(5)
        self._crawler.executeAppEvent(xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        time.sleep(5)
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

        self.assertEqual("http://localhost:3000/register/", self._crawler.getUrl())
        self.assertEqual(1036, branchCoverageLength)
        self.assertEqual(2698, statementCoverageLength)

        self.assertEqual(34, branchCoveragedAmount)
        self.assertEqual(476, statementCoveragedAmount)

    def test_crawljax_execute_usecase_get_coverage(self):
        container = EnvironmentDIContainers()
        container.config.from_ini("configuration/config/default.ini")
        container.wire(modules=[ExecuteActionUseCase, ResetEnvironmentUseCase])

        self._autOperator = IRobotOperator(self._crawler, IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000))
        self._episodeHandlerId = ""
        self._createTargetPage()
        self._resetEnv(autOperator=self._autOperator)

        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        self._executeAction(autOperator=self._autOperator, actionNumber=2)
        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        self._executeAction(autOperator=self._autOperator, actionNumber=2)
        self._executeAction(autOperator=self._autOperator, actionNumber=1)
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=self._autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=0, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

        episodeHandlerEntities = self._episodeHandlerRepository.findAll()
        lastEpisodeHandler: IEpisodeHandler = EpisodeHandlerEntityMapper.mappingEpisodeHandlerForm(episodeHandlerEntities.pop())

        statementCoverageLength = 0
        branchCoverageLength = 0
        statementCoveredAmount = 0
        branchCoveredAmount = 0
        for codeCoverage in lastEpisodeHandler.getAllState().pop().getCodeCoverages():
            if codeCoverage.getCodeCoverageType() == "statement coverage":
                statementCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                statementCoveredAmount = codeCoverage.getCoveredAmount()
            if codeCoverage.getCodeCoverageType() == "branch coverage":
                branchCoverageLength = codeCoverage.getCodeCoverageVectorLength()
                branchCoveredAmount = codeCoverage.getCoveredAmount()

        self.assertEqual(1036, branchCoverageLength)
        self.assertEqual(2698, statementCoverageLength)

        self.assertEqual(31, branchCoveredAmount)
        self.assertEqual(472, statementCoveredAmount)

    def _executeAction(self, autOperator: IAUTOperator, actionNumber: int):
        executeActionUseCase = ExecuteActionUseCase.ExecuteActionUseCase(autOperator=autOperator,
                                                                         episodeHandlerRepository=self._episodeHandlerRepository)
        executeActionInput = ExecuteActionInput.ExecuteActionInput(actionNumber=actionNumber, epsisodeHandlerId=self._episodeHandlerId)
        executeActionOutput = ExecuteActionOutput.ExecuteActionOutput()
        executeActionUseCase.execute(input=executeActionInput, output=executeActionOutput)

    def _createTargetPage(self):
        createTargetPageUseCase = CreateTargetPageUseCase.CreateTargetPageUseCase(repository=self._targetPageRepository)
        createTargetPageInput = CreateTargetPageInput.CreateTargetPageInput(targetPageUrl="http://localhost:3000", rootUrl="http://localhost:3000", appEventDTOs=[])
        createTargetPageOutput = CreateTargetPageOutput.CreateTargetPageOutput()
        createTargetPageUseCase.execute(createTargetPageInput, createTargetPageOutput)

    def _resetEnv(self, autOperator: IAUTOperator):
        resetEnvironmentUseCase = ResetEnvironmentUseCase.ResetEnvironmentUseCase(operator=autOperator,
                                                                          episodeHandlerRepository=self._episodeHandlerRepository,
                                                                          targetPageQueueManagerService=HtmlFileTargetPageQueueManagerService(repository=self._targetPageRepository))
        resetEnvironmentUseInput = ResetEnvironmentInput.ResetEnvironmentInput(episodeIndex=1)
        resetEnvironmentUseOutput = ResetEnvironmentOutput.ResetEnvironmentOutput()
        resetEnvironmentUseCase.execute(input=resetEnvironmentUseInput, output=resetEnvironmentUseOutput)

        self._episodeHandlerId = resetEnvironmentUseOutput.getEpisodeHandlerId()
