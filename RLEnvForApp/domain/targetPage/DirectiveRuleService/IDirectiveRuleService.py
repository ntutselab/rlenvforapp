from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.domain.targetPage.TargetPage import TargetPage


class IDirectiveRuleService:
    def __init__(self):
        pass

    def isLegal(self, targetPageId: str, beforeActionDom: str, afterActionDom="") -> bool:
        return True
