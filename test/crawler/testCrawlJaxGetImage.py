from test.usecase.HirerarchyInitial import HirerarchyInitial
from unittest import TestCase

import numpy
import tensorflow as tf

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import DockerServerHandler
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.IRobotCrawler import IRobotCrawler
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import SeleniumCrawler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.usecase.environment.autOperator.IRobotOperator import IRobotOperator


class testCrawlJaxGetImage(TestCase):
    def setUp(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._applicationHandler = DockerServerHandler("RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository, applicationHandler=self._applicationHandler)
        self._hirerarchyInitial.startAUTServer("timeoff_management_with_coverage")
        self._crawljaxCrawler = IRobotCrawler(
            javaPort=40000, pythonPort=40001, crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, isJavaServerRunned=True)
        self._seleniumCrawler = SeleniumCrawler(browserName="Chrome")

    def tearDown(self) -> None:
        self._crawljaxCrawler.close()
        self._seleniumCrawler.close()
        for autEntity in self._autRepository.findAll():
            self._hirerarchyInitial.stopAUTServer(autEntity.getId())

    def test_crawl_get_image(self):
        crawljaxOperator = IRobotOperator(self._crawljaxCrawler, IstanbulMiddlewareCodeCoverageCollector(
            serverIp="localhost", serverPort=3000))
        crawljaxOperator.resetCrawler(path="http://localhost:3000")

        seleniumOperator = IRobotOperator(self._seleniumCrawler, IstanbulMiddlewareCodeCoverageCollector(
            serverIp="localhost", serverPort=3000))
        seleniumOperator.resetCrawler(path="http://localhost:3000")
        # self._crawler.reset("")

        crawljaxState = crawljaxOperator.getState()
        seleniumState = seleniumOperator.getState()

        crawljaxScreenShot = crawljaxState.getScreenShot()
        seleniumScreenShot = seleniumState.getScreenShot()
        print("crawljaxScreenShot", crawljaxScreenShot.shape)
        print("seleniumScreenShot", seleniumScreenShot.shape)
        # tf.keras.preprocessing.image.save_img("./crawljaxScreenShot.png", crawljaxScreenShot)
        # tf.keras.preprocessing.image.save_img("./seleniumScreenShot.png", seleniumScreenShot)
        self.assertEqual(len(crawljaxOperator.getAllSelectedAppElements()),
                         len(seleniumOperator.getAllSelectedAppElements()))

        for crawljaxAppElementDTO, seleniumAppElementDTO in zip(crawljaxOperator.getAllSelectedAppElements(), seleniumOperator.getAllSelectedAppElements()):
            self.assertEqual(crawljaxAppElementDTO.getXpath(), seleniumAppElementDTO.getXpath())
            self.assertEqual(crawljaxAppElementDTO.getName(), seleniumAppElementDTO.getName())
            self.assertEqual(crawljaxAppElementDTO.getType(), seleniumAppElementDTO.getType())
            self.assertEqual(crawljaxAppElementDTO.getTagName(), seleniumAppElementDTO.getTagName())

        self.assertTrue(numpy.array_equal(crawljaxScreenShot, crawljaxScreenShot))
        self.assertTrue(numpy.array_equal(seleniumScreenShot, seleniumScreenShot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def test_crawl_get_image_after_do_action(self):

        self._crawljaxOperator = IRobotOperator(
            self._crawljaxCrawler, IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000))
        self._crawljaxOperator.resetCrawler(path="http://localhost:3000")
        self._goToCanlandar(autOperator=self._crawljaxOperator)
        crawljaxState = self._crawljaxOperator.getState()

        for autEntity in self._autRepository.findAll():
            self._hirerarchyInitial.stopAUTServer(autEntity.getId())
        self._hirerarchyInitial.startAUTServer("timeoff_management_with_coverage")

        self._seleniumOperator = IRobotOperator(
            self._seleniumCrawler, IstanbulMiddlewareCodeCoverageCollector(serverIp="localhost", serverPort=3000))
        self._seleniumOperator.resetCrawler(path="http://localhost:3000")
        self._goToCanlandar(autOperator=self._seleniumOperator)
        seleniumState = self._seleniumOperator.getState()

        self.assertEqual(crawljaxState.getUrl(), seleniumState.getUrl())
        self.assertEqual(len(crawljaxState.getAllSelectedAppElements()),
                         len(seleniumState.getAllSelectedAppElements()))

        crawljaxScreenShot = crawljaxState.getScreenShot()
        seleniumScreenShot = seleniumState.getScreenShot()
        tf.keras.preprocessing.image.save_img("./crawljaxScreenShot.png", crawljaxScreenShot)
        tf.keras.preprocessing.image.save_img("./seleniumScreenShot.png", seleniumScreenShot)
        self.assertTrue(numpy.array_equal(crawljaxScreenShot, crawljaxScreenShot))
        self.assertTrue(numpy.array_equal(seleniumScreenShot, seleniumScreenShot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def _goToCanlandar(self, autOperator):
        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        autOperator.getState()

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]", value="Company name")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(1, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]", value="Kai")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(2, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]", value="Huang")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(3, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]", value="test@ntut.edu.tw")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(4, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]", value="123456")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(5, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]", value="123456")
        autOperator.changeFocus()
        autOperator.getFocusedAppElement()
        self.assertEqual(6, autOperator.getState().getFocusVector().index(True))

        autOperator.executeAppEvent(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        autOperator.getFocusedAppElement()
        # autOperator.executeAppEvent(xpath="", value="")
        # autOperator.getFocusedAppElement()
