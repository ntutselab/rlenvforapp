import io
import re
import time
from io import StringIO
from urllib.parse import urlparse

import numpy
from lxml import etree
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import AppElementDTO

# EVENT_WAITING_TIME = 1000 
# some page has some delay, so we need to wait for a while
EVENT_WAITING_TIME = 5000
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
    def goToRootPage(self):
        goToRootPageRetryCount = 1
        isGoToRootPageSuccess = False
        isTimeOut = False
        while not (isGoToRootPageSuccess or isTimeOut):
            goToRootPageRetryCount += 1
            try:
                self._driver.get(self._rootPath)
                isGoToRootPageSuccess = "http" in self.getUrl()
            except:
                isGoToRootPageSuccess = False
            isTimeOut = not goToRootPageRetryCount < CRAWLER_GOTO_ROOT_PAGE_TIMEOUT
            time.sleep(1)
        if not isGoToRootPageSuccess:
            Logger().info("SeleniumCrawler Warning: Crawler go to root page time out.")
        return isGoToRootPageSuccess

    def reset(self, rootPath: str, formXPath: str = ""):
        self.close()
        self._driver = self._getWebDriver()
        if rootPath != "":
            self._rootPath = rootPath
        else:
            Logger().info(
                f"SeleniumCrawler Warning: reset to '{rootPath}', go to root page '{self._rootPath}'")
        if formXPath != "":
            self._formXPath = formXPath
        else:
            self._formXPath = "//form"
        self.goToRootPage()

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def executeAppEvent(self, xpath: str, value: str):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
        except Exception as exception:
            Logger().info(f"SeleniumCrawlerWarning: No such element in xpath {xpath}")
            raise exception
        if element.tag_name == "select":
            try:
                select = Select(element)  # 創建 Select 物件
                select.select_by_value(value)  # 依 value 選擇 option
            except Exception as exception:
                Logger().info(f"SeleniumCrawler Warning: xpath: {xpath} can't select value {value}")
        elif value == "":
            try:
                element.click()
                time.sleep(EVENT_WAITING_TIME/1000)
            except Exception as exception:
                Logger().info(f"SeleniumCrawler Warning: xpath: {xpath} can't be clicked")
                # raise exception
        else:
            try:
                Logger().info(f"SeleniumCrawler: xpath: {xpath} is input with value: {value}")
                if element.get_attribute("type") == "checkbox":
                    # 只對 checkbox 根據 value 進行處理
                    if value.lower() == "true" and not element.is_selected():
                        element.click()  # 勾選
                    elif value.lower() == "false" and element.is_selected():
                        element.click()  # 取消勾選
                elif element.get_attribute("type") != "checkbox":
                    # 處理其他類型的輸入框
                    element.clear()
                    element.send_keys(value)
                else:
                    Logger().info(f"SeleniumCrawler Warning: xpath: {xpath} can't be input, The value is: {value}")

            except Exception as exception:
                Logger().info(f"SeleniumCrawler Warning: xpath: {xpath} can't be input, The exception is: {exception}")
                # raise exception

    def getScreenShot(self):
        PNGScreenShot = self._driver.get_screenshot_as_png()
        PILScreenShot = Image.open(io.BytesIO(PNGScreenShot))
        numpyScreenShot = numpy.array(PILScreenShot)
        return numpyScreenShot

    def getAllSelectedAppElementsDTOs(self) -> [AppElementDTO]:
        html_parser = etree.parse(StringIO(self.getDOM()), etree.HTMLParser())
        self._html = etree.tostring(html_parser).decode("utf-8")

        self._appElementDTOs: [AppElementDTO] = []
        # print(f"SeleniumCrawler: getAllSelectedAppElementsDTOs: _formXPath: {self._formXPath}")
        for element in html_parser.xpath(f"{self._formXPath}//input | {self._formXPath}//textarea | {self._formXPath}//button | {self._formXPath}//select"):
            elementXpath: str = html_parser.getpath(element)
            elementHref: str = self._getHtmlTagAttribute(element, "href")
            webElement = self._driver.find_element_by_xpath(elementXpath)
            if self._isInteractable(elementXpath) and not self._shouldHrefBeIgnored(elementHref):   
                options = None
                if element.tag == "select":
                # 抓取 select 下的 option
                    options = [opt.get_attribute("value") for opt in webElement.find_elements(By.TAG_NAME, "option")]

                self._appElementDTOs.append(AppElementDTO(tagName=element.tag,
                                                          name=self._getHtmlTagAttribute(
                                                              element=element, attribute="name"),
                                                          type=self._getHtmlTagAttribute(
                                                              element=element, attribute="type"),
                                                          placeholder=self._getHtmlTagAttribute(
                                                                element=element, attribute="placeholder"),
                                                          label=self._get_label_for_element(
                                                                html_parser=html_parser, element=element),
                                                          xpath=elementXpath,
                                                          value=webElement.get_attribute("value"),
                                                          options=options))
                

        return self._appElementDTOs

    def changeFocus(self, xpath: str, value: str):
        return

    def getDOM(self) -> str:
        return self._driver.page_source

    def getUrl(self) -> str:
        return self._driver.current_url

    def _getWebDriver(self):
        browserName = self._browserName
        driver = None
        retry = 0
        isStartBrowser = False
        while not isStartBrowser:
            try:
                if browserName is None:
                    pass
                elif browserName == "Chrome":
                    chrome_options = webdriver.chrome.options.Options()
                    # chrome_options.binary_location = "/home/selab/Downloads/chrome134.0.6998.165/chrome-linux64/chrome"
                    chrome_options.add_argument('--no-sandbox')  # root permission
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck,AccountConsistency,SafeBrowsingEnhancedProtection")
                    chrome_options.add_argument("--disable-default-apps")
                    # chrome_options.add_argument('--headless')  # no GUI display
                    driver = webdriver.Chrome(chrome_options=chrome_options)
                elif browserName == "Firefox":
                    firefox_options = webdriver.firefox.options.Options()
                    firefox_options.add_argument('--no-sandbox')  # root permission
                    firefox_options.add_argument('--disable-dev-shm-usage')
                    # firefox_options.add_argument('--headless')  # no GUI display
                    driver = webdriver.Firefox(firefox_options=firefox_options)
                isStartBrowser = True
            except:
                retry += 1
                if retry >= 10:
                    break
        driver.maximize_window()
        print(driver.capabilities["browserVersion"])
        return driver

    def _getHtmlTagAttribute(self, element, attribute):
        try:
            attributeText = element.attrib[attribute]
        except Exception:
            attributeText = ""
        return attributeText

    def _isAttributeInHtmlAttributes(self, element, attribute):
        try:
            elementAttributes = element.attrib
            print(f"_isAttributeInHtmlAttributes: ")
            print(f"Attributes: {elementAttributes}")
            if attribute in elementAttributes:
                return True
            else:
                return False
        except Exception:
            return False
    
    def is_disabled(self, element):
        return element.get_attribute("disabled") is not None

    def is_readonly(self, element):
        return element.get_attribute("readonly") is not None  # 通常 select 不會有這屬性
    

    def _get_label_for_element(self, html_parser, element):
        label = ""
        try:
            label_element = html_parser.xpath(f"//label[@for='{element.attrib['id']}']")[0]
            label = label_element.text
        except:
            label = ""
        return label

    def _isInteractable(self, xpath):
        try:
            element = self._driver.find_element_by_xpath(xpath=xpath)
            is_hidden = self._getHtmlTagAttribute(element=element, attribute="type") == "hidden"
            is_readonly = self.is_readonly(element)
            is_disabled = self.is_disabled(element)
            
            if is_hidden or is_disabled or is_readonly:
                print(f"SeleniumCrawler: _isInteractable: {xpath} is hidden, readonly or disable")
                return False
            return element.is_displayed() and element.is_enabled()
        except Exception as exception:
            Logger().info(f"SeleniumCrawlerException: {exception}")
            return False

    def _shouldHrefBeIgnored(self, href: str):
        isFileDownloading = re.match(".+\\.(?:pdf|ps|zip|mp3)(?:$|\\?.+)", href)
        isMailTo = href.startswith("mailto:")
        isWebCal = href.startswith("webcal:")
        isExternal = not urlparse(href).netloc == "" and not urlparse(
            href).netloc == urlparse(self._rootPath).netloc
        return isFileDownloading or isMailTo or isExternal or isWebCal