
import os
import json
import ast
import requests
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.domain.llmService import LlmServiceContainer
from faker import Faker

from RLEnvForApp.domain.formInput.textGeneration.ITextGenerationService import ITextGenerationService
class ValueExtractor:
    @staticmethod
    def get_input_value(aut_name = None, url = None, xpath = None, prompt = None, try_count = 0, is_element_in_feedback = None, textGenerationService: ITextGenerationService = None) -> str:
        # """ 取得 input 值，優先從 default_value.json 取得 """
        # value = ValueExtractor.__check_default_value()
        # if value:
        #     return value['value']

        # url = "http://localhost:4000"
        # if action_type == 25:
        #     value = "password"
        # else:
        #     value = ValueExtractor.__fake_data_map[ValueExtractor.__input_type[action_type - 1]]
        # try:
        #     if value == "password":
        #         return ValueExtractor.__check_default_password()
        #     r = requests.get(url, params={'value': value})
        #     d = ast.literal_eval(r.text.replace("`", ""))
        #     return d["'d'"][0]
        # except requests.exceptions.RequestException as e:
        #     Logger().info(f"Error: {e}")
        #     return "Error occurred while fetching data from the server. Please try again later."
        """ 透過 LLM 取得 input 值 """
        
        if aut_name is not None and url is not None and xpath is not None:
            # 讀取 default_value.json
            default_value = ValueExtractor.__check_default_value(aut_name, url, xpath)
            if default_value != "":
                return default_value['value']
        
        
        if textGenerationService is None:
            Logger().info("textGenerationService is None")
            return ""
        
        # 取得 LLM 回應
        response = textGenerationService.get_form_input(prompt, try_count, is_element_in_feedback)
        print(f"LLM response from textGenerationService: {response}")
        return response
        # TODO: Find a way to more safely distinguish between a LLM response and a Faker function
        try:
            faker = Faker()
            reponse_text = getattr(faker, response)()
            return str(reponse_text)
        except AttributeError as e:
            # 如果無法解析為 Faker 函數，則返回原始響應
            Logger().info(f"Error parsing LLM response: {e}. Response was: {response}, It may not be a faker function")
            # 如果解析失敗，返回原始響應
            return response
    
    @staticmethod
    def get_select_value() -> str:
        """ 透過 LLM 取得選擇值 """
        response = LlmServiceContainer.llm_service_instance.get_response()
        return response

    @staticmethod
    def get_checkbox_state() -> bool:
        """ 透過 LLM 取得 checkbox 狀態 """
        response = LlmServiceContainer.llm_service_instance.get_response()
        try:
            response_clean = response.strip().lower().replace("false", "False").replace("true", "True")
            parsed_response = ast.literal_eval(response_clean)

            # if isinstance(parsed_response, list) and all(isinstance(item, bool) for item in parsed_response):
            if isinstance(parsed_response, bool):
                return parsed_response
        except (SyntaxError, ValueError) as e:
            Logger().info(f"Error parsing LLM response: {e}. Response was: {response}")

        return False

    @staticmethod
    def __check_default_value(aut_name, url, xpath) -> str:
        """ 讀取 default_value.json """
        if os.path.exists("default_value.json"):
            with open("default_value.json", "r") as f:
                data = json.load(f)
                # check if the value is in the fil
                if aut_name in data:
                    if url in data[aut_name]:
                        if xpath in data[aut_name][url]:
                            return data[aut_name][url][xpath]
        return ""
    @staticmethod
    def __check_default_password() -> str:
        """ 讀取 password.json """
        if os.path.exists("password.json"):
            with open("password.json", "r") as f:
                data = json.load(f)
                return data.get("password", "password")
        return "password"