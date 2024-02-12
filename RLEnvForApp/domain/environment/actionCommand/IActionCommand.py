from RLEnvForApp.domain.environment.autOperator.IAUTOperator import \
    IAUTOperator


class IActionCommand:
    def __init__(self, actionNumber: int, actionType: str):
        self._actionNumber = actionNumber
        self._actionType = actionType

    def getActionType(self):
        return self._actionType

    def getActionNumber(self):
        return self._actionNumber

    def execute(self, operator: IAUTOperator):
        pass
