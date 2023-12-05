import json
import os
import re

from RLEnvForApp.logger.logger import Logger


class FormSubmitCriteriaSingleton:
    _instance = None

    @staticmethod
    def getInstance():
        if not FormSubmitCriteriaSingleton._instance:
            FormSubmitCriteriaSingleton()
        return FormSubmitCriteriaSingleton._instance

    def __init__(self):
        if FormSubmitCriteriaSingleton._instance:
            raise Exception('only one instance can exist')
        else:
            if os.path.exists('form_submit_criteria.json'):
                with open('form_submit_criteria.json', encoding='utf-8') as jsonfile:
                    data = json.load(jsonfile)
                self._OriginFormSubmitCriteria: dict = data
                self._formSubmitCriteria = self._OriginFormSubmitCriteria
            else:
                self._OriginFormSubmitCriteria = {}
                self._formSubmitCriteria = self._OriginFormSubmitCriteria

            FormSubmitCriteriaSingleton._instance = self

    def getFormSubmitCriteria(self) -> dict:
        return self._formSubmitCriteria

    def setFormSubmitCriteria(self, applicationName: str, url: str, xpath: str):
        Logger().info(f"Find Form Submit Criteria: {applicationName}, {url}, {xpath}")
        byApplicationName = self._OriginFormSubmitCriteria.get(applicationName)
        byUrl = {}
        for key in byApplicationName:
            if key == url:
                byUrl = byApplicationName.get(key)
                break
            if "{}" in key:
                pattern = key.replace("{}", ".+")
                if bool(re.fullmatch(pattern, url)):
                    Logger().info(f"Match criteria: {pattern}")
                    byUrl = byApplicationName.get(key)
                    break

        self._formSubmitCriteria = byUrl.get(xpath, {})
        Logger().info(f"Form Submit Criteria set to : {self._formSubmitCriteria}")
