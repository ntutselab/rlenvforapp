

class IDirectiveRuleService:
    def __init__(self):
        pass

    def is_legal(self, target_page_id: str, beforeActionDom: str,
                afterActionDom="") -> bool:
        return True
