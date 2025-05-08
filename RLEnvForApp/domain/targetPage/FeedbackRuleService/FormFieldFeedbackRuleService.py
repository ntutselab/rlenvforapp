import ast
import difflib
import re
from io import StringIO

from lxml import etree

from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.targetPage.FeedbackRuleService.IFeedbackRuleService import \
    IFeedbackRuleService
from RLEnvForApp.domain.targetPage.utils import get_new_elements
from RLEnvForApp.logger.logger import Logger


class FormFieldFeedbackRuleService(IFeedbackRuleService):
    def __init__(self):
        super().__init__()

    def getFeedbackAndLocation(self, beforeActionDom: str, afterActionDom: str, fields: list, previous_feedbacks: str) -> dict:
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
                if isinstance(feedback_and_location, dict):
                    updated_feedback_and_location = self._filter_feedback(new_or_updated_elements, fields, previous_feedbacks, feedback_and_location)
                    Logger().info(f"Updated feedback and location: {updated_feedback_and_location}")
                    return updated_feedback_and_location
                else:
                    Logger().info(f"Feedback and location is not a dict: {feedback_and_location}")
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
            previously recorded feedback: {previous_feedbacks}
            newly added or updated elements: {new_or_updated_elements}
        """.format(
            fields=fields,
            previous_feedbacks=previous_feedbacks,
            new_or_updated_elements=new_or_updated_elements
        )
        
        answer = LlmServiceContainer.llm_service_instance.get_response(prompt, system_prompt)
        # Logger().info(f"fields: {fields}")
        # Logger().info(f"url: {url}")
        # Logger().info(f"new_elements: {new_elements}")
        # Logger().info(f"Prompt: {prompt}")
        Logger().info(f"The get_feedback_and_location: {answer}")
        return answer

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
            currently observed feedback: {current_feedback}
            previously recorded feedback: {previous_feedbacks}
            provided fields: {fields}
            newly added or updated elements: {new_or_updated_elements}
        """.format(
            current_feedback = filtered_feedback,
            previous_feedbacks = previous_feedbacks,
            fields = fields,
            new_or_updated_elements = new_or_updated_elements
        )

        Logger().info(f"Prompt: {prompt}")
        
        
        # make sure the answer is a dict
        filtered_feedback = {}
        try_count = 0
        answer = ""
        while not isinstance(answer, dict) and try_count < 3:
            try:
                answer = LlmServiceContainer.llm_service.get_response(prompt, system_prompt)
                Logger().info(f"The _filter_feedback: {answer}")
                answer = ast.literal_eval(answer)
                if isinstance(answer, dict):
                    filtered_feedback = answer
                    break
                else:
                    Logger().info(f"Answer is not a dict: {answer}")
                    try_count += 1
            except (SyntaxError, ValueError) as e:
                Logger().info(f"Error parsing LLM response: {e}. Response was: {answer}")
                try_count += 1
        return filtered_feedback