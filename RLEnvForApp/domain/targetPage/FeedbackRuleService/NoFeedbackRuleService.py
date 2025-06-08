from RLEnvForApp.domain.targetPage.FeedbackRuleService.IFeedbackRuleService import \
    IFeedbackRuleService
class NoFeedbackRuleService(IFeedbackRuleService):
    def __init__(self):
        super().__init__()

    def getFeedbackAndLocation(self, beforeActionDom: str, afterActionDom: str, fields: list, previous_feedbacks: dict) -> dict:
        print("No feedback rule service")
        return {}
