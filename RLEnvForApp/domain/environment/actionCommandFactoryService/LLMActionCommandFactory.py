import ast
import json
import os
import random

import requests

from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector
from RLEnvForApp.domain.environment import inputSpace
from RLEnvForApp.domain.environment.actionCommand import IRobotClickCommand, IRobotInputValueCommand, IRobotSelectOptionCommand
from RLEnvForApp.domain.environment.actionCommand.ChangeFocusCommand import ChangeFocusCommand
from RLEnvForApp.domain.environment.actionCommand.IActionCommand import IActionCommand
from RLEnvForApp.domain.environment.actionCommandFactoryService.IActionCommandFactoryService import \
    IActionCommandFactoryService
from RLEnvForApp.domain.environment.inputSpace import ValueWeightSingleton
from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.domain.llmService import LlmServiceContainer

class LLMActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self.__aut_name = ''
        self.__url = ''
        self.__xpath = ''
        self.__input_data = inputSpace.inputValues
        self.__input_type = PromptModelDirector.classes
        self.__fake_data_map = {
            "first name": "firstname",
            "last name": "lastname",
            "email": "email",
            "gender": -1,
            "string": -1,
            "user name": "username",
            "full name": "name",
            "postal code": "postcode",
            "store name": -1,
            "phone number": "phonenumber",
            "street address": "stateabbr",
            "city": "city",
            "state": "state",
            "province" : -1,
            "region": -1,
            "number": -1,
            "country": "country",
            "display name": "username",
            "address": "address",
            "suburb": -1,
            "company name": -1,
            "card number": -1,
            "expiration date": -1,
            "CVV": -1,
            "date": "date",
            "password": "password",
        }



    def createActionCommand(self, actionNumber: int ) -> IActionCommand:
        if actionNumber == 26:
            option_value: str = self._get_select_value()
            Logger().info(f"Option value: {option_value}")
            return IRobotSelectOptionCommand.IRobotSelectOptionCommand(option_value, actionNumber)
        elif actionNumber == 27:
            checkbox_states = self._get_checkbox_states()
            Logger().info(f"Checkbox state: {checkbox_states}")
            # checkbox_state = False
            checkbox_state = True
            # if len(checkbox_states) > 0:
            #     checkbox_state = checkbox_states[0]
            # return IRobotClickCommand.IRobotClickCommand(actionNumber) if checkbox_state else ChangeFocusCommand(actionNumber=actionNumber)
            return IRobotInputValueCommand.IRobotInputValueCommand(str(checkbox_state), actionNumber)
        elif actionNumber != 0 and actionNumber != -1:
            input_value: str = self._get_input_value(actionNumber)
            Logger().info(f"Input value: {input_value}")
            return IRobotInputValueCommand.IRobotInputValueCommand(input_value, actionNumber)
        elif actionNumber == -1:
            return ChangeFocusCommand(actionNumber=actionNumber)
        return IRobotClickCommand.IRobotClickCommand(actionNumber)

    def _get_input_value(self, action_type: int) -> str:
        # check if the value is in the default_value.json file
        value = self.__check_default_value()
        if value != "":
            return value['value']

        url = "http://localhost:4000"
        if action_type == 25:
            value = "password"
        else:
            value = self.__fake_data_map[self.__input_type[action_type - 1]]
        try:
            if value == "password":
                return self.__check_default_password()
            r = requests.get(url, params={'value': value})
        except requests.exceptions.RequestException as e:
            Logger().info(f"Error: {e}")
            return "Error occurred while fetching data from the server. Please try again later."
        d = ast.literal_eval(r.text.replace("`", ""))
        return d["'d'"][0]
    def _get_select_value(self) -> str:
        systemPrompt = LlmServiceContainer.llm_service_instance.get_system_prompt()
        prompt = LlmServiceContainer.llm_service_instance.get_prompt()
        response = LlmServiceContainer.llm_service_instance.get_response(prompt, systemPrompt)
        parsed_response = ast.literal_eval(response)  # 解析成 Python 列表
        print(f"Select Option Response: {parsed_response[0]}")
        return parsed_response[0]
    def __check_default_password(self) -> str:
        # open the default_value.json file to check if the value is in the file
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                data = json.load(f)
                # check if the value is in the fil
                if self.__aut_name in data:
                    return data[self.__aut_name]
        return "password"
    def _get_checkbox_states(self) -> list[bool]:
        system_prompt = LlmServiceContainer.llm_service_instance.get_system_prompt()
        prompt = LlmServiceContainer.llm_service_instance.get_prompt()
        response = LlmServiceContainer.llm_service_instance.get_response(prompt, system_prompt)
        
        Logger().info(f"Response from LLM: {response}")

        try:
            # 1. 先處理 Response，確保它是標準的 JSON 格式
            response_clean = response.strip().lower().replace("false", "False").replace("true", "True")

            # 2. 嘗試用 ast.literal_eval 解析成 list
            parsed_response = ast.literal_eval(response_clean)

            # 3. 確保它是 list[bool]
            if isinstance(parsed_response, list) and all(isinstance(item, bool) for item in parsed_response):
                return parsed_response
            else:
                Logger().info(f"Parsed response is not a valid list of booleans: {parsed_response}")
                return [False]  # 預設值

        except (SyntaxError, ValueError) as e:
            Logger().info(f"Error parsing LLM response: {e}. Response was: {response}")
            return [False]  # 預設值
    
    def __check_default_value(self) -> str:
        # open the default_value.json file to check if the value is in the file
        if os.path.exists("default_value.json"):
            with open("default_value.json", "r") as f:
                data = json.load(f)
                # check if the value is in the fil
                if self.__aut_name in data:
                    if self.__url in data[self.__aut_name]:
                        if self.__xpath in data[self.__aut_name][self.__url]:
                            return data[self.__aut_name][self.__url][self.__xpath]
        return ""

    def getActionSpaceSize(self) -> int:
        return len(self.__input_data)

    def getActionList(self) -> [str]:
        return self.__input_data

    def setAutName(self, aut_name: str):
        self.__aut_name = aut_name

    def setUrl(self, url: str):
        self.__url = url

    def setXpath(self, xpath: str):
        self.__xpath = xpath