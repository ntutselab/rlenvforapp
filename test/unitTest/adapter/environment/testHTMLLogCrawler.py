import unittest

from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import \
    HTMLLogCrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


class MyTestCase(unittest.TestCase):

    def set_up(self) -> None:
        self._crawler = HTMLLogCrawler()
        self._file_path = "htmlSet/GUIDE_HTML_SET/timeoff__login_.html"

    def test_crawler_reset(self):
        self._crawler.reset(rootPath=self._file_path)
        self.assertEqual(self._file_path, self._crawler.get_url())
        self.assertEqual(3, len(self._crawler.get_all_selected_app_elements_dt_os()))

    def test_crawler_execute_action(self):
        self._crawler.reset(rootPath=self._file_path)
        self.assertEqual(self._file_path, self._crawler.get_url())
        self.assertEqual(3, len(self._crawler.get_all_selected_app_elements_dt_os()))
        passwoard_app_element_dto: AppElementDTO = None
        for app_element_dto in self._crawler.get_all_selected_app_elements_dt_os():
            if app_element_dto.get_name() == "password":
                passwoard_app_element_dto = app_element_dto
        self.assertEqual("", passwoard_app_element_dto.get_value())
        self._crawler.execute_app_event(
            xpath=passwoard_app_element_dto.get_xpath(),
            value="testPassword")
        for app_element_dto in self._crawler.get_all_selected_app_elements_dt_os():
            if app_element_dto.get_name() == "password":
                passwoard_app_element_dto = app_element_dto
        self.assertEqual("testPassword", passwoard_app_element_dto.get_value())


if __name__ == '__main__':
    unittest.main()
