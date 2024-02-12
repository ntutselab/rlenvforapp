import json
import os
import random

from lxml import etree

from RLEnvForApp.usecase.environment.autOperator.crawler.ICrawler import \
    ICrawler
from RLEnvForApp.usecase.environment.autOperator.dto.AppElementDTO import \
    AppElementDTO


class HTMLLogCrawler(ICrawler):
    def __init__(self):
        super().__init__()
        self._html: str = ""
        self._targetPath: str = ""
        self._appElementDTOs: [AppElementDTO] = []

    def go_to_root_page(self):
        folderPath, pageHTMLFileName = os.path.split(self._targetPath)
        pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"

        htmlParser = etree.parse(
            os.path.join(
                folderPath,
                pageHTMLFileName),
            etree.HTMLParser())
        self._html = etree.tostring(htmlParser).decode("utf-8")
        self._appElementDTOs: [AppElementDTO] = []

        jsonData = open(os.path.join(folderPath, pageJsonFileName),)
        pageLog = json.load(jsonData)
        jsonData.close()
        interactiveXpaths = pageLog["interactive_appElement"]
        for xpath in interactiveXpaths:
            if xpath not in pageLog["appEvent"]:
                continue
            element = htmlParser.xpath(xpath)[0]
            self._appElementDTOs.append(AppElementDTO(tagName=element.tag,
                                                      name=self._get_html_tag_attribute(
                                                          element=element, attribute="name"),
                                                      type=self._get_html_tag_attribute(
                                                          element=element, attribute="type"),
                                                      xpath=htmlParser.getpath(
                                                          element),
                                                      value=self._get_html_tag_attribute(element=element,
                                                                                      attribute="value")))
        random.shuffle(self._appElementDTOs)

    def reset(self, rootPath: str, formXPath: str = ""):
        if rootPath != "":
            self._targetPath = rootPath
        self.go_to_root_page()

    def close(self):
        pass

    def execute_app_event(self, xpath: str, value: str):
        # if value == "":
        #     return
        # if "button" in xpath:
        #     return
        for element in self._appElementDTOs:
            if element.get_xpath() is xpath:
                element._value = value

    def change_focus(self, xpath: str, value: str):
        for element in self._appElementDTOs:
            if element.get_xpath() is xpath:
                element._value = value

    def get_screen_shot(self):
        pass

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        return self._appElementDTOs

    def get_dom(self) -> str:
        return self._html

    def get_url(self) -> str:
        return self._targetPath

    def _get_html_tag_attribute(self, element, attribute):
        attributeText = ""
        try:
            attributeText = element.attrib[attribute]
        except BaseException:
            attributeText = ""
        return attributeText
