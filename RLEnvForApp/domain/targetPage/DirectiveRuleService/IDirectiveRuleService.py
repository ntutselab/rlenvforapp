

class IDirectiveRuleService:
    def __init__(self):
        pass

    def isLegal(self, targetPageId: str, beforeActionDom: str, afterActionDom="") -> bool:
        return True
