import unittest

from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import \
    HTMLLogCrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


class MyTestCase(unittest.TestCase):

    def set_up(self) -> None:
        self._crawler = HTMLLogCrawler()
        self._filePath = "htmlSet/GUIDE_HTML_SET/timeoff__login_.html"

    def test_crawler_reset(self):
        self._crawler.reset(rootPath=self._filePath)
        self.assertEqual(self._filePath, self._crawler.get_url())
        self.assertEqual(3, len(self._crawler.get_all_selected_app_elements_dt_os()))

    def test_crawler_execute_action(self):
        self._crawler.reset(rootPath=self._filePath)
        self.assertEqual(self._filePath, self._crawler.get_url())
        self.assertEqual(3, len(self._crawler.get_all_selected_app_elements_dt_os()))
        passwoardAppElementDTO: AppElementDTO = None
        for appElementDTO in self._crawler.get_all_selected_app_elements_dt_os():
            if appElementDTO.get_name() == "password":
                passwoardAppElementDTO = appElementDTO
        self.assertEqual("", passwoardAppElementDTO.get_value())
        self._crawler.execute_app_event(
            xpath=passwoardAppElementDTO.get_xpath(),
            value="testPassword")
        for appElementDTO in self._crawler.get_all_selected_app_elements_dt_os():
            if appElementDTO.get_name() == "password":
                passwoardAppElementDTO = appElementDTO
        self.assertEqual("testPassword", passwoardAppElementDTO.get_value())


if __name__ == '__main__':
    unittest.main()
