from test.usecase.HirerarchyInitial import HirerarchyInitial
from unittest import TestCase

import numpy
import tensorflow as tf

from RLEnvForApp.adapter.applicationUnderTest.DockerServerHandler import \
    DockerServerHandler
from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
    IstanbulMiddlewareCodeCoverageCollector
from RLEnvForApp.adapter.environment.autOperator.crawler.IRobotCrawler import \
    IRobotCrawler
from RLEnvForApp.adapter.environment.autOperator.crawler.SeleniumCrawler import \
    SeleniumCrawler
from RLEnvForApp.adapter.repository.applicationUnderTest.InMemoryApplicationUnderTestRepository import \
    InMemoryApplicationUnderTestRepository
from RLEnvForApp.usecase.environment.autOperator.IRobotOperator import \
    IRobotOperator


class testCrawlJaxGetImage(TestCase):
    def set_up(self) -> None:
        self._autRepository = InMemoryApplicationUnderTestRepository()
        self._applicationHandler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchyInitial = HirerarchyInitial(
            autRepository=self._autRepository,
            applicationHandler=self._applicationHandler)
        self._hirerarchyInitial.start_aut_server(
            "timeoff_management_with_coverage")
        self._crawljaxCrawler = IRobotCrawler(
            javaPort=40000,
            pythonPort=40001,
            crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, isJavaServerRunned=True)
        self._seleniumCrawler = SeleniumCrawler(browserName="Chrome")

    def tear_down(self) -> None:
        self._crawljaxCrawler.close()
        self._seleniumCrawler.close()
        for autEntity in self._autRepository.find_all():
            self._hirerarchyInitial.stop_aut_server(autEntity.get_id())

    def test_crawl_get_image(self):
        crawljaxOperator = IRobotOperator(
            self._crawljaxCrawler,
            IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost",
                serverPort=3000))
        crawljaxOperator.reset_crawler(path="http://localhost:3000")

        seleniumOperator = IRobotOperator(
            self._seleniumCrawler,
            IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost",
                serverPort=3000))
        seleniumOperator.reset_crawler(path="http://localhost:3000")
        # self._crawler.reset("")

        crawljaxState = crawljaxOperator.get_state()
        seleniumState = seleniumOperator.get_state()

        crawljaxScreenShot = crawljaxState.get_screen_shot()
        seleniumScreenShot = seleniumState.get_screen_shot()
        print("crawljaxScreenShot", crawljaxScreenShot.shape)
        print("seleniumScreenShot", seleniumScreenShot.shape)
        # tf.keras.preprocessing.image.save_img("./crawljaxScreenShot.png", crawljaxScreenShot)
        # tf.keras.preprocessing.image.save_img("./seleniumScreenShot.png", seleniumScreenShot)
        self.assertEqual(len(crawljaxOperator.get_all_selected_app_elements()),
                         len(seleniumOperator.get_all_selected_app_elements()))

        for crawljaxAppElementDTO, seleniumAppElementDTO in zip(
                crawljaxOperator.get_all_selected_app_elements(), seleniumOperator.get_all_selected_app_elements()):
            self.assertEqual(
                crawljaxAppElementDTO.get_xpath(),
                seleniumAppElementDTO.get_xpath())
            self.assertEqual(
                crawljaxAppElementDTO.get_name(),
                seleniumAppElementDTO.get_name())
            self.assertEqual(
                crawljaxAppElementDTO.get_type(),
                seleniumAppElementDTO.get_type())
            self.assertEqual(
                crawljaxAppElementDTO.get_tag_name(),
                seleniumAppElementDTO.get_tag_name())

        self.assertTrue(
            numpy.array_equal(
                crawljaxScreenShot,
                crawljaxScreenShot))
        self.assertTrue(
            numpy.array_equal(
                seleniumScreenShot,
                seleniumScreenShot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def test_crawl_get_image_after_do_action(self):

        self._crawljaxOperator = IRobotOperator(
            self._crawljaxCrawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._crawljaxOperator.reset_crawler(path="http://localhost:3000")
        self._go_to_canlandar(autOperator=self._crawljaxOperator)
        crawljaxState = self._crawljaxOperator.get_state()

        for autEntity in self._autRepository.find_all():
            self._hirerarchyInitial.stop_aut_server(autEntity.get_id())
        self._hirerarchyInitial.start_aut_server(
            "timeoff_management_with_coverage")

        self._seleniumOperator = IRobotOperator(
            self._seleniumCrawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._seleniumOperator.reset_crawler(path="http://localhost:3000")
        self._go_to_canlandar(autOperator=self._seleniumOperator)
        seleniumState = self._seleniumOperator.get_state()

        self.assertEqual(crawljaxState.get_url(), seleniumState.get_url())
        self.assertEqual(len(crawljaxState.get_all_selected_app_elements()),
                         len(seleniumState.get_all_selected_app_elements()))

        crawljaxScreenShot = crawljaxState.get_screen_shot()
        seleniumScreenShot = seleniumState.get_screen_shot()
        tf.keras.preprocessing.image.save_img(
            "./crawljaxScreenShot.png", crawljaxScreenShot)
        tf.keras.preprocessing.image.save_img(
            "./seleniumScreenShot.png", seleniumScreenShot)
        self.assertTrue(
            numpy.array_equal(
                crawljaxScreenShot,
                crawljaxScreenShot))
        self.assertTrue(
            numpy.array_equal(
                seleniumScreenShot,
                seleniumScreenShot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def _go_to_canlandar(self, autOperator):
        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        autOperator.get_state()

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]",
            value="Company name")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            1, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]",
            value="Kai")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            2, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]",
            value="Huang")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            3, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]",
            value="test@ntut.edu.tw")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            4, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]",
            value="123456")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            5, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]",
            value="123456")
        autOperator.change_focus()
        autOperator.get_focused_app_element()
        self.assertEqual(
            6, autOperator.get_state().get_focus_vector().index(True))

        autOperator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        autOperator.get_focused_app_element()
        # autOperator.executeAppEvent(xpath="", value="")
        # autOperator.getFocusedAppElement()
