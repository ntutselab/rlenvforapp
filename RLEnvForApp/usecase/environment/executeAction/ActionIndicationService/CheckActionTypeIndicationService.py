from RLEnvForApp.domain.environment.state.AppElement import AppElement
from RLEnvForApp.domain.environment.state.State import State
from RLEnvForApp.domain.environment.rewardCalculatorService.ActionIndicationService.IActionIndicationService import IActionIndicationService


class CheckActionTypeIndicationService(IActionIndicationService):
    def __init__(self):
        super().__init__()

    def isConform(self, state: State):
        actionType = state.getActionType()
        interactedAppElement = state.getInteractedElement()

        if actionType == "input":
            return self._isValidInputAction(appElement=interactedAppElement)
        if actionType == "click":
            return self._isValidClickAction(appElement=interactedAppElement)
        if actionType == "changeFocus":
            return self._isValidChangeFocusAction(appElement=interactedAppElement)

        return False

    def _isValidInputAction(self, appElement: AppElement):
        if appElement and appElement.getTagName() and appElement.getTagName().lower() == "input":
            return True
        else:
            return False

    def _isValidClickAction(self, appElement: AppElement):
        if appElement and appElement.getType() and appElement.getType().lower() == "submit":
            return True
        else:
            return False

    def _isValidChangeFocusAction(self, appElement: AppElement):
        isValidInputAction = self._isValidInputAction(appElement=appElement)
        isValidClickAction = self._isValidClickAction(appElement=appElement)
        return not(isValidClickAction or isValidInputAction)