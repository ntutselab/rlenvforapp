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
    def __init__(self, browser_name: str):
        super().__init__()
        self._browser_name = browser_name
        self._root_path = ""
        self._driver = None
        self._app_element_dt_os: [AppElementDTO] = []
        self._form_xpath = "//form"

    def go_to_root_page(self):
        go_to_root_page_retry_count = 1
        is_go_to_root_page_success = False
        is_time_out = False
        while not (is_go_to_root_page_success or is_time_out):
            go_to_root_page_retry_count += 1
            try:
                self._driver.get(self._root_path)
                is_go_to_root_page_success = "http" in self.get_url()
            except BaseException:
                is_go_to_root_page_success = False
            is_time_out = not (go_to_root_page_retry_count <
                             CRAWLER_GOTO_ROOT_PAGE_TIMEOUT)
            time.sleep(1)
        if not is_go_to_root_page_success:
            Logger().info("SeleniumCrawler Warning: Crawler go to root page time out.")
        return is_go_to_root_page_success

    def reset(self, rootPath: str, form_xpath: str = ""):
        self.close()
        self._driver = self._get_web_driver()
        if rootPath != "":
            self._root_path = rootPath
        else:
            Logger().info(
                f"SeleniumCrawler Warning: reset to '{rootPath}', go to root page '{self._rootPath}'")
        if form_xpath != "":
            self._form_xpath = form_xpath
        else:
            self._form_xpath = "//form"
        self.go_to_root_page()

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def execute_app_event(self, xpath: str, value: str):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
        except Exception as exception:
            Logger().info(
                f"SeleniumCrawlerWarning: No such element in xpath {xpath}")
            raise exception

        if value == "":
            try:
                element.click()
                time.sleep(EVENT_WAITING_TIME / 1000)
            except Exception as exception:
                Logger().info(
                    f"SeleniumCrawler Warning: xpath: {xpath} can't be clicked")
                # raise exception
        else:
            try:
                element.clear()
                element.send_keys(value)
            except Exception as exception:
                Logger().info(
                    f"SeleniumCrawler Warning: xpath: {xpath} can't be input")
                # raise exception

    def get_screen_shot(self):
        png_screen_shot = self._driver.get_screenshot_as_png()
        pil_screen_shot = Image.open(io.BytesIO(png_screen_shot))
        numpy_screen_shot = numpy.array(pil_screen_shot)
        return numpy_screen_shot

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        html_parser = etree.parse(StringIO(self.get_dom()), etree.HTMLParser())
        self._html = etree.tostring(html_parser).decode("utf-8")
        self._app_element_dt_os: [AppElementDTO] = []
        for element in html_parser.xpath(
                f"{self._formXPath}//input | {self._formXPath}//textarea | {self._formXPath}//button"):
            elementXpath: str = html_parser.getpath(element)
            elementHref: str = self._get_html_tag_attribute(element, "href")
            webElement = self._driver.find_element_by_xpath(elementXpath)
            if self._is_interactable(
                    elementXpath) and not self._should_href_be_ignored(elementHref):
                self._app_element_dt_os.append(AppElementDTO(tag_name=element.tag,
                                                          name=self._get_html_tag_attribute(
                                                              element=element, attribute="name"),
                                                          type=self._get_html_tag_attribute(
                                                              element=element, attribute="type"),
                                                          xpath=elementXpath,
                                                          value=webElement.get_attribute("value")))

        return self._app_element_dt_os

    def change_focus(self, xpath: str, value: str):
        return

    def get_dom(self) -> str:
        return self._driver.page_source

    def get_url(self) -> str:
        return self._driver.current_url

    def _get_web_driver(self):
        browser_name = self._browser_name
        driver = None
        retry = 0
        is_start_browser = False
        while (not is_start_browser):
            try:
                if browser_name is "Chrome":
                    chrome_options = webdriver.chrome.options.Options()
                    chrome_options.add_argument(
                        '--no-sandbox')  # root permission
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    # chrome_options.add_argument('--headless')  # no GUI
                    # display
                    driver = webdriver.Chrome(chrome_options=chrome_options)
                elif browser_name is "Firefox":
                    firefox_options = webdriver.firefox.options.Options()
                    firefox_options.add_argument(
                        '--no-sandbox')  # root permission
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    # firefox_options.add_argument('--headless')  # no GUI
                    # display
                    driver = webdriver.Firefox(firefox_options=firefox_options)
                is_start_browser = True
            except BaseException:
                retry += 1
                if retry >= 10:
                    break
        driver.maximize_window()
        return driver

    def _get_html_tag_attribute(self, element, attribute):
        try:
            attribute_text = element.attrib[attribute]
        except BaseException:
            attribute_text = ""
        return attribute_text

    def _is_interactable(self, xpath):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
            if self._get_html_tag_attribute(element=element, attribute="input") == "input" and self._get_html_tag_attribute(
                    element=element, attribute="type") == "hidden":
                return False
            return element.is_displayed() and element.is_enabled()
        except Exception as exception:
            Logger().info(f"SeleniumCrawlerException: {exception}")
            return False

    def _should_href_be_ignored(self, href: str):
        is_file_downloading = re.match(
            ".+\\.(?:pdf|ps|zip|mp3)(?:$|\\?.+)", href)
        is_mail_to = href.startswith("mailto:")
        is_external = not (urlparse(href).netloc == "") and \
            not (urlparse(href).netloc == urlparse(self._root_path).netloc)
        return is_file_downloading or is_mail_to or is_external
