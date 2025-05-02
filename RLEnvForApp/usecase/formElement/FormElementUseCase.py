
import json
from RLEnvForApp.usecase.formElement.FormElementOutput import FormElementOutput
from RLEnvForApp.usecase.formElement.FormElementInput import FormElementInput
from RLEnvForApp.domain.constants.actions import ACTION_NUMBER
from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.llmService import LlmServiceContainer
from RLEnvForApp.domain.llmService.ILlmService import ILlmService
from RLEnvForApp.domain.llmService.SystemPromptFactory import SystemPromptFactory
from RLEnvForApp.domain.targetPage.FieldRuleService.IFieldRuleService import IFieldRuleService
from RLEnvForApp.logger.logger import Logger

class FormElementUseCase:
    def __init__(self, llm_service: ILlmService, field_rule_service: IFieldRuleService):
        self._llm_service = llm_service
        self._field_rule_service = field_rule_service
        self._logger = Logger()
        self.input_types = ["date", "datetime-local", "email", "month", "number", "password", "tel", "text", "time", "url", "week", ""]

    def handle(self, formElementInput: FormElementInput) -> FormElementOutput:
        target_page_dom = formElementInput.get_target_page_dom()
        target_form_xpath = formElementInput.get_target_form_xpath()
        target_element_xpath = formElementInput.get_target_element_xpath()
        feedback = formElementInput.get_feedback()
        try_count = formElementInput.get_try_count()
        app_element = formElementInput.get_app_element()
        form_title = formElementInput.get_form_title()
        pre_fields = formElementInput.get_pre_fields()
        

        if self._is_submit_button(app_element, target_form_xpath, target_element_xpath):
            return FormElementOutput(action_number=ACTION_NUMBER["click"], final_submit=True, execute_action_output_is_done=False)
        elif app_element.getTagName() == "button":
            return FormElementOutput(action_number=ACTION_NUMBER["changeFocus"], final_submit=True, execute_action_output_is_done=False)
        elif not self._is_required(target_page_dom, app_element.getXpath(), feedback) and try_count < 3:
            pre_field = {"name": app_element.getName(), "label": app_element.getLabel(), "placeholder": app_element.getPlaceholder(), "value": "", "xpath": app_element.getXpath()}
            # The app_element is not required, so we want to get all the pre fields to find the feedback location to update the required field in the next try
            pre_fields.append(pre_field)

            self._logger.info(f"The {app_element.getXpath()} is not required")
            self._logger.info(f"Pre fields: {pre_fields}")
            return FormElementOutput(action_number=ACTION_NUMBER["changeFocus"], final_submit=False, execute_action_output_is_done=True)
    
        if app_element.getTagName() == "select":
            return self._handle_select_field(app_element, form_title, feedback, pre_fields)
        elif app_element.getTagName() == "input" and app_element.getType() == "checkbox":
            return self._handle_checkbox_field(app_element, form_title, feedback, pre_fields)
        

        elif (
            (app_element.getTagName() == "input" and app_element.getType() in self.input_types)
            or app_element.getTagName() == "textarea"
        ):

            self._logger.info(f"Input Type: {app_element.getType()}")
            return self._handle_input_field(app_element, form_title, feedback, pre_fields, try_count)
            
        else:
            self._logger.info(f"Unknown element type: {app_element.getTagName()}")
            return FormElementOutput(action_number=ACTION_NUMBER["changeFocus"], final_submit=False, execute_action_output_is_done=True)

    def _is_submit_button(self, app_element: AppElement, form_xpath: str, target_xpath: str) -> bool:
        if app_element.getTagName() != "select" and app_element.getTagName() != "textarea":
            # find the submit button by xpath
            prompt = 'The Form element:\n' + form_xpath + '\nThe target element:\n' + target_xpath
            system_prompt = SystemPromptFactory.get("is_submit_button")
            is_submit_button_str = self._llm_service.get_response(prompt, system_prompt).lower()
            if is_submit_button_str == "yes":
                return True
        return False
    
    def _is_required(self, dom_str: str, xpath: str, feedback:dict) -> bool:
        """
        檢查指定 XPath 的元素是否為必填。
        
        :param dom_str: HTML DOM 的字串表示
        :param xpath: 要檢查的 XPath
        :return: 如果該元素為必填則回傳 True，否則回傳 False
        """
        
        self._logger.info(f"Start check required field: {xpath}")
        return self._field_rule_service.isLegal(dom_str=dom_str, xpath=xpath, feedback=feedback)
    
    def _handle_select_field(self, app_element: AppElement, form_title, feedback, pre_fields) -> FormElementOutput:
        select_fields = "[{\"name\":\"" + app_element.getName() + "\",\"label\":\"" + app_element.getLabel() + "\",\"options\":" + json.dumps(app_element.getOptions()) + "}]"
        prompt = """
            Form Title: {form_title}
            Select Field: {select_field}
            Feedback: {feedback}
            Previous Fields with Values: {pre_fields}
        """.format(form_title=form_title, select_field=select_fields,
                feedback=feedback, pre_fields=pre_fields)
        
        LlmServiceContainer.llm_service_instance.set_prompt(prompt)
        LlmServiceContainer.llm_service_instance.set_system_prompt(SystemPromptFactory.get("select_option"))
        result = FormElementOutput(action_number=ACTION_NUMBER["select"], final_submit=False, execute_action_output_is_done=False, prompt = prompt)
        return result
    
    def _handle_checkbox_field(self, app_element: AppElement, form_title, feedback, pre_fields) -> FormElementOutput:
        checkbox_field = "[{\"name\":\"" + app_element.getName() + "\",\"label\":\"" + app_element.getLabel() + "}]"
        prompt = """
            Form Title: {form_title}
            Checkbox Field: {checkbox_field}
            Feedback: {feedback}
            Previous Fields with Values: {pre_fields}
        """.format(form_title=form_title, checkbox_field=checkbox_field,
                feedback=feedback, pre_fields=pre_fields)
        LlmServiceContainer.llm_service_instance.set_prompt(prompt)
        LlmServiceContainer.llm_service_instance.set_system_prompt(SystemPromptFactory.get("select_option"))
        result = FormElementOutput(action_number=ACTION_NUMBER["checkbox"], final_submit=False, execute_action_output_is_done=False, prompt = prompt)
        return result
    
    def _handle_input_field(self, app_element: AppElement, form_title, feedback, pre_fields, try_count) -> FormElementOutput:
        input_field = "{\"name\":\"" + app_element.getName() + "\",\"label\":\"" + app_element.getLabel() + "\",\"placeholder\":\"" + app_element.getPlaceholder() + "\"}"
        self._logger.info(f"Input Type: {app_element.getType()}, and input field: {input_field}")
        xpath = app_element.getXpath()
        system_prompt = ""
        if try_count >= 3 or (feedback and xpath in feedback):
            system_prompt = SystemPromptFactory.get("get_input_value")
        else:
            system_prompt = SystemPromptFactory.get("select_data_faker")
        prompt = """
            Form Title: {form_title}
            Input Field: {input_field}
            Feedback: {feedback}
            Previous Fields with Values: {pre_fields}
        """.format(form_title=form_title, input_field=input_field, feedback=feedback, pre_fields= pre_fields)
        result = FormElementOutput(action_number=ACTION_NUMBER["input"], final_submit=False, execute_action_output_is_done=False, prompt = prompt)
        return result