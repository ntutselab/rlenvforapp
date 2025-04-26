
from RLEnvForApp.domain.environment.state.AppElement import AppElement


class FormElementInput:
    def __init__(self, 
                 target_page_dom: str,
                 target_form_xpath: str,
                 target_element_xpath: str,
                 feedback: dict,
                 try_count: int,
                 app_element: AppElement,
                 form_title: str,
                 pre_fields: list):
        self.target_page_dom = target_page_dom
        self.target_form_xpath = target_form_xpath
        self.target_element_xpath = target_element_xpath
        self.feedback = feedback
        self.try_count = try_count
        self.app_element = app_element
        self.form_title = form_title
        self.pre_fields = pre_fields

    def set_target_page_dom(self, target_page_dom: str):
        self.target_page_dom = target_page_dom
    
    def set_target_form_xpath(self, target_form_xpath: str):
        self.target_form_xpath = target_form_xpath
    
    def set_target_element_xpath(self, target_element_xpath: str):
        self.target_element_xpath = target_element_xpath
    
    def set_feedback(self, feedback: dict):
        self.feedback = feedback
    
    def set_try_count(self, try_count: int):
        self.try_count = try_count
    
    def set_app_element(self, app_element: AppElement):
        self.app_element = app_element
    
    def set_form_title(self, form_title: str):
        self.form_title = form_title
    
    def set_pre_fields(self, pre_fields: list):
        self.pre_fields = pre_fields
    
    def get_target_page_dom(self) -> str:
        return self.target_page_dom

    def get_target_form_xpath(self) -> str:
        return self.target_form_xpath
    
    def get_target_element_xpath(self) -> str:
        return self.target_element_xpath
    
    def get_feedback(self) -> dict:
        return self.feedback
    
    def get_try_count(self) -> int:
        return self.try_count
    
    def get_app_element(self) -> AppElement:
        return self.app_element
    
    def get_form_title(self) -> str:
        return self.form_title
    
    def get_pre_fields(self) -> list:
        return self.pre_fields
    
    def to_dict(self) -> dict:
        return {
            "target_page_dom": self.target_page_dom,
            "target_form_xpath": self.target_form_xpath,
            "target_element_xpath": self.target_element_xpath,
            "feedback": self.feedback,
            "try_count": self.try_count,
            "app_element": self.app_element.to_dict() if self.app_element else None,
            "form_title": self.form_title,
            "pre_fields": self.pre_fields
        }