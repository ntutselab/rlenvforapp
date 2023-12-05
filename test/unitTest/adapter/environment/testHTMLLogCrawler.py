import unittest

from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import HTMLLogCrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self._crawler = HTMLLogCrawler()
        self._filePath = "htmlSet/GUIDE_HTML_SET/timeoff__login_.html"

    def test_crawler_reset(self):
        self._crawler.reset(path=self._filePath)
        self.assertEqual(self._filePath, self._crawler.getUrl())
        self.assertEqual(3, len(self._crawler.getAllSelectedAppElementsDTOs()))

    def test_crawler_execute_action(self):
        self._crawler.reset(path=self._filePath)
        self.assertEqual(self._filePath, self._crawler.getUrl())
        self.assertEqual(3, len(self._crawler.getAllSelectedAppElementsDTOs()))
        passwoardAppElementDTO: AppElementDTO = None
        for appElementDTO in self._crawler.getAllSelectedAppElementsDTOs():
            if appElementDTO.getName() == "password":
                passwoardAppElementDTO = appElementDTO
        self.assertEqual("", passwoardAppElementDTO.getValue())
        self._crawler.executeAppEvent(xpath=passwoardAppElementDTO.getXpath(), value="testPassword")
        for appElementDTO in self._crawler.getAllSelectedAppElementsDTOs():
            if appElementDTO.getName() == "password":
                passwoardAppElementDTO = appElementDTO
        self.assertEqual("testPassword", passwoardAppElementDTO.getValue())

if __name__ == '__main__':
    unittest.main()
