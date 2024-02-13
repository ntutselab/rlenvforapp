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
        self._target_path: str = ""
        self._app_element_dt_os: [AppElementDTO] = []

    def go_to_root_page(self):
        folder_path, pageHTMLFileName = os.path.split(self._target_path)
        page_json_file_name = os.path.splitext(pageHTMLFileName)[0] + ".json"

        html_parser = etree.parse(
            os.path.join(
                folder_path,
                pageHTMLFileName),
            etree.HTMLParser())
        self._html = etree.tostring(html_parser).decode("utf-8")
        self._app_element_dt_os: [AppElementDTO] = []

        json_data = open(os.path.join(folder_path, page_json_file_name),)
        page_log = json.load(json_data)
        json_data.close()
        interactive_xpaths = page_log["interactive_appElement"]
        for xpath in interactive_xpaths:
            if xpath not in page_log["appEvent"]:
                continue
            element = html_parser.xpath(xpath)[0]
            self._app_element_dt_os.append(AppElementDTO(tag_name=element.tag,
                                                      name=self._get_html_tag_attribute(
                                                          element=element, attribute="name"),
                                                      type=self._get_html_tag_attribute(
                                                          element=element, attribute="type"),
                                                      xpath=html_parser.getpath(
                                                          element),
                                                      value=self._get_html_tag_attribute(element=element,
                                                                                      attribute="value")))
        random.shuffle(self._app_element_dt_os)

    def reset(self, rootPath: str, form_xpath: str = ""):
        if rootPath != "":
            self._target_path = rootPath
        self.go_to_root_page()

    def close(self):
        pass

    def execute_app_event(self, xpath: str, value: str):
        # if value == "":
        #     return
        # if "button" in xpath:
        #     return
        for element in self._app_element_dt_os:
            if element.get_xpath() is xpath:
                element._value = value

    def change_focus(self, xpath: str, value: str):
        for element in self._app_element_dt_os:
            if element.get_xpath() is xpath:
                element._value = value

    def get_screen_shot(self):
        pass

    def get_all_selected_app_elements_dt_os(self) -> [AppElementDTO]:
        return self._app_element_dt_os

    def get_dom(self) -> str:
        return self._html

    def get_url(self) -> str:
        return self._target_path

    def _get_html_tag_attribute(self, element, attribute):
        attribute_text = ""
        try:
            attribute_text = element.attrib[attribute]
        except BaseException:
            attribute_text = ""
        return attribute_text
