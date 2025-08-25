import ast
import difflib
import json
import re
from io import StringIO

from lxml import etree

from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.adapter.llmService.Gemma3Service import Gemma3Service
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.targetPage.FeedbackRuleService.IFeedbackRuleService import \
    IFeedbackRuleService
from RLEnvForApp.domain.targetPage.utils import get_new_elements
from RLEnvForApp.logger.logger import Logger


class FormFieldFeedbackRuleService(IFeedbackRuleService):
    def __init__(self):
        super().__init__()

    def getFeedbackAndLocation(self, beforeActionDom: str, afterActionDom: str, fields: list, previous_feedbacks: dict) -> dict:
        if afterActionDom == "":
            Logger().info("afterActionDom is empty string")
            return {}

        feedback_and_location = None
        get_feedback_and_location_try_count = 0
        max_try_count = 3
        new_or_updated_elements = get_new_elements(self._get_elements(beforeActionDom), self._get_elements(afterActionDom))
        while feedback_and_location is None and get_feedback_and_location_try_count < max_try_count:
            try:
                feedback_and_location = ast.literal_eval(self._extract_feedback(new_or_updated_elements, fields, previous_feedbacks))
                Logger().info(f"The feedback is extracted: {feedback_and_location}")
                if isinstance(feedback_and_location, dict):
                    if feedback_and_location == {} and previous_feedbacks == {}:
                        Logger().info(f"Current feedback and previous feedbacks are both empty, the feedback will not be updated")
                        return feedback_and_location
                     
                    updated_feedback_and_location = self._filter_feedback(new_or_updated_elements, fields, previous_feedbacks, feedback_and_location)
                    Logger().info(f"Updated feedback and location: {updated_feedback_and_location}")
                    return updated_feedback_and_location
                else:
                    Logger().info(f"Feedback and location is not a dict: {feedback_and_location}")
                    feedback_and_location = None
                    get_feedback_and_location_try_count += 1
            except (SyntaxError, ValueError) as e:
                get_feedback_and_location_try_count += 1
                Logger().info(f"In FormFieldFeedbackRuleService, Error parsing LLM response: {e}. Response was: {feedback_and_location}")
            
        return {}

    def _get_elements(self, dom):
        parser = etree.HTMLParser()
        doc = etree.parse(StringIO(dom), parser)

        elements = list()
        for el in doc.getroot().iter():
            # 略過 HTML 註解
            if isinstance(el, etree._Comment):
                continue
            tag = el.tag
            classes = el.get('class')
            text = re.sub('\s', '', str(el.text))
            # elements.append(f'{tag} {classes} {text}')

            # 抓取所有屬性，包括 src
            attributes = " ".join(f'{k}={v}' for k, v in el.attrib.items())
            elements.append(f'{tag} {classes} {attributes} {text}')
        return elements


    def _extract_feedback(self, new_or_updated_elements, fields, previous_feedbacks) -> str:
        system_prompt = SystemPromptFactory.get("get_feedback_and_location")
        prompt = """
            fields: {fields}
            newly added or updated elements: {new_or_updated_elements}
        """.format(
            fields=fields,
            new_or_updated_elements=new_or_updated_elements
        )
        
        answer = LlmServiceContainer.llm_service_instance.get_response(prompt, system_prompt)
        # Logger().info(f"fields: {fields}")
        # Logger().info(f"url: {url}")
        # Logger().info(f"new_elements: {new_elements}")
        # Logger().info(f"Prompt: {prompt}")
        Logger().info(f"The get_feedback_and_location: {answer}")
        return answer
    
    def __extract_filtered_feedback(self, llm_response: str) -> dict:
        # for COT
        # match = re.search(r'Final Answer:\s*(\{.*\})', llm_response, re.DOTALL)
        
        match = re.search(r'\s*(\{.*\})', llm_response, re.DOTALL)
        if not match:
            return {}

        raw = match.group(1)

        # 優先嘗試 Python literal_eval
        try:
            result = ast.literal_eval(raw)
            if isinstance(result, dict):
                return result
        except Exception as e1:
            Logger().info(f"literal_eval failed: {e1}")

        # 嘗試 fallback: 修補格式為 JSON
        try:
            # 1. null ➜ None
            # 2. true/false ➜ True/False
            # 3. 單引號 ➜ 雙引號（避免 LLM 混用）

            json_like = (
                raw
                .replace("None", "null")  # 若 LLM 有混用 Python 字面量，也先轉回 JSON
                .replace("True", "true")
                .replace("False", "false")
                .replace("'", '"')
            )

            result = json.loads(json_like)
            if isinstance(result, dict):
                return result
        except Exception as e2:
            Logger().info(f"json.loads fallback failed: {e2}")
            Logger().info(f"Original string:\n{raw}")

        return {}
    
    def _filter_feedback(self, new_or_updated_elements:str, fields: list, previous_feedbacks: dict, current_feedback: dict) -> dict:
        """
        過濾掉不必要的 feedback
        """
        # 如果沒有 feedback，則不需要過濾
        if current_feedback == {}:
            return current_feedback
        filtered_feedback = {}
        for index, field in enumerate(fields):
            # 如果 feedback 中的 key 和 fields 中的 key 不匹配，則刪除該 feedback
            xpath = field.get("xpath")
            if xpath in current_feedback:
                Logger().info(f"Feedback key: {xpath} is in fields: {fields}, so we add the feedback: {current_feedback[xpath]} in filtered_feedback")
                filtered_feedback[xpath] = current_feedback[xpath]
                del current_feedback[xpath]
                continue
        
        system_prompt = SystemPromptFactory.get("filter_feedback")
        prompt = """
            current_feedbacks: {current_feedback}
            previous_feedbacks: {previous_feedbacks}
            fields: {fields}
            new_elements: {new_or_updated_elements}
        """.format(
            current_feedback = filtered_feedback,
            previous_feedbacks = previous_feedbacks,
            fields = fields,
            new_or_updated_elements = new_or_updated_elements
        )

        Logger().info(f"Prompt: {prompt}")
        
        
        # make sure the answer is a dict
        try_count = 0
        answer = ""
        result = {}
        filter_llmeservice = Gemma3Service()
        while try_count < 3:
            answer = filter_llmeservice.get_response(prompt, system_prompt)
            result = self.__extract_filtered_feedback(answer)
            Logger().info(f"_filter_feedback Result:{result}")
            if result == {}:
                try_count+=1
            else:
                filtered_feedback = result
                break
        if previous_feedbacks ==None:
            previous_feedbacks = {}
        if result == {}:
            filtered_feedback = previous_feedbacks | filtered_feedback
        return filtered_feedback