

class IDirectiveRuleService:
    def __init__(self):
        pass

    def is_legal(self, targetPageId: str, beforeActionDom: str,
                afterActionDom="") -> bool:
        return True
