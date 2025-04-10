from lxml import html
from RLEnvForApp.domain.targetPage.FieldRuleService.IFieldRuleService import IFieldRuleService

class RequiredFieldRuleService(IFieldRuleService):
    def isLegal(self, dom_str: str, xpath: str, feedback: dict) -> bool:
        """
        檢查指定 XPath 的元素是否為必填。
        """
        tree = html.fromstring(dom_str)
        elements = tree.xpath(xpath)

        if not elements:
            return False
        for elem in elements:
            if ('required' in elem.attrib or 
                elem.attrib.get('aria-required') == 'true' or
                elem.attrib.get('data-required') == 'true' or
                int(elem.attrib.get('minlength', '0')) > 0):
                print(f"Element {elem.tag} with id {elem.attrib.get('id', '')} is required.")
                return True

            # 檢查 label 內容是否包含 '*'
            label_xpath = f"//label[@for='{elem.attrib.get('id', '')}']"
            labels = tree.xpath(label_xpath)
            for label in labels:
                if '*' in label.text_content():
                    print(f"Label {label.tag} with text {label.text_content()} is required.")
                    return True

            # 檢查 placeholder、title、class 是否有必填相關字詞
            for attr in ['placeholder', 'title', 'class']:
                if any(keyword in elem.attrib.get(attr, '').lower() for keyword in ['必填', '請輸入', 'required', '必須']):
                    print(f"Element {elem.tag} with id {elem.attrib.get('id', '')} has required keyword in {attr}.")
                    return True
            
            # 如果 xpath 存在於 feedback 中，則視為必填
        if feedback is not None and xpath in feedback:
                print(f"XPath {xpath} is in feedback, marking as required.")
                return True

        return False