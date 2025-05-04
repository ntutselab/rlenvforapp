from lxml import html
from RLEnvForApp.domain.targetPage.FieldRuleService.IFieldRuleService import IFieldRuleService

class FillAllFieldsRuleService(IFieldRuleService):
    def isLegal(self, dom_str: str, xpath: str, feedback: dict) -> bool:
        """
        不檢查是否為必填欄位，直接返回 True。
        """
        print("FillAllFieldsRuleService: isLegal")
        return True