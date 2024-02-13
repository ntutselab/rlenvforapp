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


class TestCrawlJaxGetImage(TestCase):
    def set_up(self) -> None:
        self._aut_repository = InMemoryApplicationUnderTestRepository()
        self._application_handler = DockerServerHandler(
            "RLEnvForApp/application/serverInstance")
        self._hirerarchy_initial = HirerarchyInitial(
            autRepository=self._aut_repository,
            applicationHandler=self._application_handler)
        self._hirerarchy_initial.start_aut_server(
            "timeoff_management_with_coverage")
        self._crawljax_crawler = IRobotCrawler(
            javaPort=40000,
            pythonPort=40001,
            crawlerPath="RLEnvForApp/application/crawler/irobot-crawler_screen_shot_v2.jar")
        # self._crawler = IRobotCrawler(javaPort=50000, pythonPort=50001, isJavaServerRunned=True)
        self._selenium_crawler = SeleniumCrawler(browser_name="Chrome")

    def tear_down(self) -> None:
        self._crawljax_crawler.close()
        self._selenium_crawler.close()
        for aut_entity in self._aut_repository.find_all():
            self._hirerarchy_initial.stop_aut_server(aut_entity.get_id())

    def test_crawl_get_image(self):
        crawljax_operator = IRobotOperator(
            self._crawljax_crawler,
            IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost",
                serverPort=3000))
        crawljax_operator.reset_crawler(path="http://localhost:3000")

        selenium_operator = IRobotOperator(
            self._selenium_crawler,
            IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost",
                serverPort=3000))
        selenium_operator.reset_crawler(path="http://localhost:3000")
        # self._crawler.reset("")

        crawljax_state = crawljax_operator.get_state()
        selenium_state = selenium_operator.get_state()

        crawljax_screen_shot = crawljax_state.get_screen_shot()
        selenium_screen_shot = selenium_state.get_screen_shot()
        print("crawljaxScreenShot", crawljax_screen_shot.shape)
        print("seleniumScreenShot", selenium_screen_shot.shape)
        # tf.keras.preprocessing.image.save_img("./crawljaxScreenShot.png", crawljaxScreenShot)
        # tf.keras.preprocessing.image.save_img("./seleniumScreenShot.png", seleniumScreenShot)
        self.assertEqual(len(crawljax_operator.get_all_selected_app_elements()),
                         len(selenium_operator.get_all_selected_app_elements()))

        for crawljaxAppElementDTO, seleniumAppElementDTO in zip(
                crawljax_operator.get_all_selected_app_elements(), selenium_operator.get_all_selected_app_elements()):
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
                crawljax_screen_shot,
                crawljax_screen_shot))
        self.assertTrue(
            numpy.array_equal(
                selenium_screen_shot,
                selenium_screen_shot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def test_crawl_get_image_after_do_action(self):

        self._crawljax_operator = IRobotOperator(
            self._crawljax_crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._crawljax_operator.reset_crawler(path="http://localhost:3000")
        self._go_to_canlandar(aut_operator=self._crawljax_operator)
        crawljax_state = self._crawljax_operator.get_state()

        for aut_entity in self._aut_repository.find_all():
            self._hirerarchy_initial.stop_aut_server(aut_entity.get_id())
        self._hirerarchy_initial.start_aut_server(
            "timeoff_management_with_coverage")

        self._selenium_operator = IRobotOperator(
            self._selenium_crawler, IstanbulMiddlewareCodeCoverageCollector(
                serverIp="localhost", serverPort=3000))
        self._selenium_operator.reset_crawler(path="http://localhost:3000")
        self._go_to_canlandar(aut_operator=self._selenium_operator)
        selenium_state = self._selenium_operator.get_state()

        self.assertEqual(crawljax_state.get_url(), selenium_state.get_url())
        self.assertEqual(len(crawljax_state.get_all_selected_app_elements()),
                         len(selenium_state.get_all_selected_app_elements()))

        crawljax_screen_shot = crawljax_state.get_screen_shot()
        selenium_screen_shot = selenium_state.get_screen_shot()
        tf.keras.preprocessing.image.save_img(
            "./crawljaxScreenShot.png", crawljax_screen_shot)
        tf.keras.preprocessing.image.save_img(
            "./seleniumScreenShot.png", selenium_screen_shot)
        self.assertTrue(
            numpy.array_equal(
                crawljax_screen_shot,
                crawljax_screen_shot))
        self.assertTrue(
            numpy.array_equal(
                selenium_screen_shot,
                selenium_screen_shot))
        # self.assertTrue(numpy.array_equal(crawljaxScreenShot, seleniumScreenShot))

    def _go_to_canlandar(self, aut_operator):
        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/form[1]/div[4]/div[2]/p[1]/a[2]", value="")
        aut_operator.get_state()

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[1]/div[1]/input[1]",
            value="Company name")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            1, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[2]/div[1]/input[1]",
            value="Kai")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            2, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[3]/div[1]/input[1]",
            value="Huang")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            3, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[4]/div[1]/input[1]",
            value="test@ntut.edu.tw")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            4, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[5]/div[1]/input[1]",
            value="123456")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            5, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[6]/div[1]/input[1]",
            value="123456")
        aut_operator.change_focus()
        aut_operator.get_focused_app_element()
        self.assertEqual(
            6, aut_operator.get_state().get_focus_vector().index(True))

        aut_operator.execute_app_event(
            xpath="/html[1]/body[1]/div[1]/div[3]/div[1]/form[1]/div[9]/div[1]/button[1]", value="")
        aut_operator.get_focused_app_element()
        # autOperator.executeAppEvent(xpath="", value="")
        # autOperator.getFocusedAppElement()
