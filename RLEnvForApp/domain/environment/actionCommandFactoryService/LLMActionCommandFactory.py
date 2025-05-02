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
from RLEnvForApp.domain.environment.ValueExtractor import ValueExtractor
from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.domain.constants.actions import ACTION_NUMBER

class LLMActionCommandFactory(IActionCommandFactoryService):
    def __init__(self):
        super().__init__()
        self.__aut_name = ''
        self.__url = ''
        self.__xpath = ''
        self.__prompt = ''
        self.__try_count = 0
        self.__is_element_in_feedback = False
        self.__input_data = inputSpace.inputValues
        self.__input_type = PromptModelDirector.classes
        self.__textGenerationService: ITextGenerationService  = None
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



    def createActionCommand(self, actionNumber: int) -> IActionCommand:
        if actionNumber == ACTION_NUMBER["click"]:
            Logger().info(f"Click action number: {actionNumber}")
            return IRobotClickCommand.IRobotClickCommand(actionNumber)
        
        elif actionNumber == ACTION_NUMBER["select"]:
            select_value: str = ValueExtractor.get_select_value()
            # Logger().info(f"Select value: {select_value}")
            return IRobotSelectOptionCommand.IRobotSelectOptionCommand(select_value, actionNumber)
        elif actionNumber == ACTION_NUMBER["checkbox"]:
            checkbox_state: bool = ValueExtractor.get_checkbox_state()
            # Logger().info(f"Checkbox states: {checkbox_states}")
            return IRobotInputValueCommand.IRobotInputValueCommand(str(checkbox_state), actionNumber)
        elif actionNumber == ACTION_NUMBER["input"]:
            
            input_value: str = ValueExtractor.get_input_value(self.__aut_name, self.__url, self.__xpath, self.__prompt, self.__try_count, self.__is_element_in_feedback, self.__textGenerationService)
            # Logger().info(f"Input value: {input_value}")
            return IRobotInputValueCommand.IRobotInputValueCommand(input_value, actionNumber)

        elif actionNumber == ACTION_NUMBER["changeFocus"]:
            return ChangeFocusCommand(actionNumber=actionNumber)

        return IRobotClickCommand.IRobotClickCommand(actionNumber)

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

    def setPrompt(self, prompt: str):
        self.__prompt = prompt

    def setTryCount(self, try_count: int):
        self.__try_count = try_count

    def setIsElementInFeedback(self, is_element_in_feedback: bool):
        self.__is_element_in_feedback = is_element_in_feedback

    def setTextGenerationService(self, textGenerationService: ITextGenerationService):
        self.__textGenerationService = textGenerationService

    