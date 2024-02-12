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

    def goToRootPage(self):
        folderPath, pageHTMLFileName = os.path.split(self._targetPath)
        pageJsonFileName = os.path.splitext(pageHTMLFileName)[0] + ".json"

        htmlParser = etree.parse(os.path.join(folderPath, pageHTMLFileName), etree.HTMLParser())
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
                                                      name=self._getHtmlTagAttribute(
                                                          element=element, attribute="name"),
                                                      type=self._getHtmlTagAttribute(
                                                          element=element, attribute="type"),
                                                      xpath=htmlParser.getpath(element),
                                                      value=self._getHtmlTagAttribute(element=element,
                                                                                      attribute="value")))
        random.shuffle(self._appElementDTOs)

    def reset(self, rootPath: str, formXPath: str = ""):
        if rootPath != "":
            self._targetPath = rootPath
        self.goToRootPage()

    def close(self):
        pass

    def executeAppEvent(self, xpath: str, value: str):
        # if value == "":
        #     return
        # if "button" in xpath:
        #     return
        for element in self._appElementDTOs:
            if element.getXpath() is xpath:
                element._value = value

    def changeFocus(self, xpath: str, value: str):
        for element in self._appElementDTOs:
            if element.getXpath() is xpath:
                element._value = value

    def getScreenShot(self):
        pass

    def getAllSelectedAppElementsDTOs(self) -> [AppElementDTO]:
        return self._appElementDTOs

    def getDOM(self) -> str:
        return self._html

    def getUrl(self) -> str:
        return self._targetPath

    def _getHtmlTagAttribute(self, element, attribute):
        attributeText = ""
        try:
            attributeText = element.attrib[attribute]
        except BaseException:
            attributeText = ""
        return attributeText
