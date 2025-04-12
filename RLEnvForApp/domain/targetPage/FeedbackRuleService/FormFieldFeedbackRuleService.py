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

    def getFeedbackAndLocation(self, beforeActionDom: str, afterActionDom: str, fields: list, form_url: str) -> dict:
        if afterActionDom == "":
            Logger().info("afterActionDom is empty string")
            return {}
        try:
            feedback_and_location = ast.literal_eval(self._get_llm_answer(self._get_elements(beforeActionDom), self._get_elements(afterActionDom), fields, form_url))
            if isinstance(feedback_and_location, dict):
                return feedback_and_location
            else:
                Logger().info(f"Feedback and location is not a dict: {feedback_and_location}")
                
        except (SyntaxError, ValueError) as e:
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


    def _get_llm_answer(self, before_action_elements, after_action_elements, fields, url) -> str:
        new_elements = get_new_elements(before_action_elements, after_action_elements)
        system_prompt = SystemPromptFactory.get("get_feedback_and_location")
        prompt = """
            fields: {fields}
            url: {url}
            new_elements: {new_elements}
        """.format(
            fields=fields,
            url=url,
            new_elements=new_elements
        )
        
        answer = LlmServiceContainer.llm_service.get_response(prompt, system_prompt)
        # Logger().info(f"fields: {fields}")
        # Logger().info(f"url: {url}")
        # Logger().info(f"new_elements: {new_elements}")
        # Logger().info(f"Prompt: {prompt}")
        Logger().info(f"The get_feedback_and_location: {answer}")
        return answer
