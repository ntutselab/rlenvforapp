import io
import re
import time
from io import StringIO
from urllib.parse import urlparse

import numpy
from lxml import etree
from PIL import Image
from selenium import webdriver

from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO

EVENT_WAITING_TIME = 1000
PAGE_WAITING_TIME = 1000
CRAWLER_GOTO_ROOT_PAGE_TIMEOUT = 10


class SeleniumCrawler(ICrawler):
    def __init__(self, browserName: str):
        super().__init__()
        self._browserName = browserName
        self._rootPath = ""
        self._driver = None
        self._appElementDTOs: [AppElementDTO] = []
        self._formXPath = "//form"

    def go_to_root_page(self):
        goToRootPageRetryCount = 1
        isGoToRootPageSuccess = False
        isTimeOut = False
        while not (isGoToRootPageSuccess or isTimeOut):
            goToRootPageRetryCount += 1
            try:
                self._driver.get(self._rootPath)
                isGoToRootPageSuccess = "http" in self.get_url()
            except BaseException:
                isGoToRootPageSuccess = False
            isTimeOut = not (goToRootPageRetryCount <
                             CRAWLER_GOTO_ROOT_PAGE_TIMEOUT)
            time.sleep(1)
        if not isGoToRootPageSuccess:
            Logger().info("SeleniumCrawler Warning: Crawler go to root page time out.")
        return isGoToRootPageSuccess

    def reset(self, rootPath: str, formXPath: str = ""):
        self.close()
        self._driver = self._get_web_driver()
        if rootPath != "":
            self._rootPath = rootPath
        else:
            Logger().info(
                f"SeleniumCrawler Warning: reset to '{rootPath}', go to root page '{self._rootPath}'")
        if formXPath != "":
            self._formXPath = formXPath
        else:
            self._formXPath = "//form"
        self.go_to_root_page()

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def execute_app_event(self, xpath: str, value: str):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
        except Exception as e:
            Logger().info(
                f"SeleniumCrawlerWarning: No such element in xpath {xpath}")
            raise e

        if value == "":
            try:
                element.click()
                time.sleep(EVENT_WAITING_TIME / 1000)
            except Exception as e:
                Logger().info(
                    f"SeleniumCrawler Warning: xpath: {xpath} can't be clicked")
                # raise e
        else:
            try:
                element.clear()
                element.send_keys(value)
            except Exception as e:
                Logger().info(
                    f"SeleniumCrawler Warning: xpath: {xpath} can't be input")
                # raise e

    def get_screen_shot(self):
        PNGScreenShot = self._driver.get_screenshot_as_png()
        PILScreenShot = Image.open(io.BytesIO(PNGScreenShot))
        numpyScreenShot = numpy.array(PILScreenShot)
        return numpyScreenShot

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        htmlParser = etree.parse(StringIO(self.get_dom()), etree.HTMLParser())
        self._html = etree.tostring(htmlParser).decode("utf-8")
        self._appElementDTOs: [AppElementDTO] = []
        for element in htmlParser.xpath(
                f"{self._formXPath}//input | {self._formXPath}//textarea | {self._formXPath}//button"):
            elementXpath: str = htmlParser.getpath(element)
            elementHref: str = self._get_html_tag_attribute(element, "href")
            webElement = self._driver.find_element_by_xpath(elementXpath)
            if self._is_interactable(
                    elementXpath) and not self._should_href_be_ignored(elementHref):
                self._appElementDTOs.append(AppElementDTO(tagName=element.tag,
                                                          name=self._get_html_tag_attribute(
                                                              element=element, attribute="name"),
                                                          type=self._get_html_tag_attribute(
                                                              element=element, attribute="type"),
                                                          xpath=elementXpath,
                                                          value=webElement.get_attribute("value")))

        return self._appElementDTOs

    def change_focus(self, xpath: str, value: str):
        return

    def get_dom(self) -> str:
        return self._driver.page_source

    def get_url(self) -> str:
        return self._driver.current_url

    def _get_web_driver(self):
        browserName = self._browserName
        driver = None
        retry = 0
        isStartBrowser = False
        while (not isStartBrowser):
            try:
                if browserName is "Chrome":
                    chrome_options = webdriver.chrome.options.Options()
                    chrome_options.add_argument(
                        '--no-sandbox')  # root permission
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    # chrome_options.add_argument('--headless')  # no GUI
                    # display
                    driver = webdriver.Chrome(chrome_options=chrome_options)
                elif browserName is "Firefox":
                    firefox_options = webdriver.firefox.options.Options()
                    firefox_options.add_argument(
                        '--no-sandbox')  # root permission
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    # firefox_options.add_argument('--headless')  # no GUI
                    # display
                    driver = webdriver.Firefox(firefox_options=firefox_options)
                isStartBrowser = True
            except BaseException:
                retry += 1
                if retry >= 10:
                    break
        driver.maximize_window()
        return driver

    def _get_html_tag_attribute(self, element, attribute):
        try:
            attributeText = element.attrib[attribute]
        except BaseException:
            attributeText = ""
        return attributeText

    def _is_interactable(self, xpath):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
            if self._get_html_tag_attribute(element=element, attribute="input") == "input" and self._get_html_tag_attribute(
                    element=element, attribute="type") == "hidden":
                return False
            return element.is_displayed() and element.is_enabled()
        except Exception as e:
            Logger().info(f"SeleniumCrawlerException: {e}")
            return False

    def _should_href_be_ignored(self, href: str):
        isFileDownloading = re.match(
            ".+\\.(?:pdf|ps|zip|mp3)(?:$|\\?.+)", href)
        isMailTo = href.startswith("mailto:")
        isExternal = not (urlparse(href).netloc == "") and \
            not (urlparse(href).netloc == urlparse(self._rootPath).netloc)
        return isFileDownloading or isMailTo or isExternal
